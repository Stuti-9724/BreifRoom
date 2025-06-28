import os
import json
from flask import render_template, request, redirect, url_for, flash, jsonify, session, make_response
from werkzeug.utils import secure_filename
from app import app, db
from models import ProcessingSession
from ai_service import transcribe_audio_file, analyze_content, classify_content
from pdf_service import generate_pdf

ALLOWED_EXTENSIONS = {'mp3', 'wav'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_content():
    try:
        content_type = request.form.get('content_type')
        manual_classification = request.form.get('manual_classification')
        
        if content_type == 'audio':
            # Handle audio file upload
            if 'audio_file' not in request.files:
                flash('No audio file selected', 'error')
                return redirect(url_for('index'))
            
            file = request.files['audio_file']
            if file.filename == '':
                flash('No audio file selected', 'error')
                return redirect(url_for('index'))
            
            if not allowed_file(file.filename):
                flash('Invalid file type. Please upload MP3 or WAV files only.', 'error')
                return redirect(url_for('index'))
            
            # Save the uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Transcribe audio
            try:
                transcribed_text = transcribe_audio_file(filepath)
                # Clean up the uploaded file
                os.remove(filepath)
            except Exception as e:
                if os.path.exists(filepath):
                    os.remove(filepath)
                flash(f'Error transcribing audio: {str(e)}', 'error')
                return redirect(url_for('index'))
                
        elif content_type == 'text':
            # Handle text input
            transcribed_text = request.form.get('text_content', '').strip()
            filename = None
            
            if not transcribed_text:
                flash('Please enter some text to analyze', 'error')
                return redirect(url_for('index'))
        else:
            flash('Invalid content type', 'error')
            return redirect(url_for('index'))
        
        # Classify content (automatic or manual)
        if manual_classification and manual_classification in ['client', 'internal']:
            classification = manual_classification
        else:
            try:
                classification = classify_content(transcribed_text)
            except Exception as e:
                app.logger.error(f"Classification error: {str(e)}")
                classification = 'client'  # Default fallback
        
        # Analyze content based on classification
        try:
            analysis_result = analyze_content(transcribed_text, classification)
        except Exception as e:
            flash(f'Error analyzing content: {str(e)}', 'error')
            return redirect(url_for('index'))
        
        # Save to database
        processing_session = ProcessingSession(
            filename=filename,
            content_type=content_type,
            classification=classification,
            original_text=transcribed_text if content_type == 'text' else None,
            transcribed_text=transcribed_text,
            analysis_result=json.dumps(analysis_result)
        )
        
        db.session.add(processing_session)
        db.session.commit()
        
        # Store session ID for results page
        session['current_session_id'] = processing_session.id
        
        return redirect(url_for('results'))
        
    except Exception as e:
        app.logger.error(f"Processing error: {str(e)}")
        flash(f'An error occurred while processing: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/results')
def results():
    session_id = session.get('current_session_id')
    if not session_id:
        flash('No processing session found', 'error')
        return redirect(url_for('index'))
    
    processing_session = ProcessingSession.query.get_or_404(session_id)
    analysis_result = json.loads(processing_session.analysis_result)
    
    return render_template('results.html', 
                         session=processing_session, 
                         analysis=analysis_result)

@app.route('/export/pdf/<int:session_id>')
def export_pdf(session_id):
    processing_session = ProcessingSession.query.get_or_404(session_id)
    analysis_result = json.loads(processing_session.analysis_result)
    
    try:
        pdf_content = generate_pdf(processing_session, analysis_result)
        
        response = make_response(pdf_content)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=briefroom_analysis_{session_id}.pdf'
        
        return response
    except Exception as e:
        flash(f'Error generating PDF: {str(e)}', 'error')
        return redirect(url_for('results'))

@app.route('/api/copy-content/<int:session_id>')
def copy_content(session_id):
    processing_session = ProcessingSession.query.get_or_404(session_id)
    analysis_result = json.loads(processing_session.analysis_result)
    
    # Format content for copying
    content = f"# {analysis_result.get('title', 'Analysis Results')}\n\n"
    
    if processing_session.classification == 'client':
        content += f"**Goals:** {analysis_result.get('goals', 'Not specified')}\n\n"
        content += f"**Deliverables:** {analysis_result.get('deliverables', 'Not specified')}\n\n"
        content += f"**Timeline:** {analysis_result.get('timeline', 'Not specified')}\n\n"
        content += f"**Budget:** {analysis_result.get('budget', 'Not specified')}\n\n"
        content += f"**Tone:** {analysis_result.get('tone', 'Not specified')}\n\n"
        content += f"**Follow-up Email:**\n{analysis_result.get('follow_up_email', 'Not generated')}\n"
    else:
        content += f"**Key Decisions:** {analysis_result.get('decisions', 'None recorded')}\n\n"
        content += f"**Key Points:** {analysis_result.get('key_points', 'None recorded')}\n\n"
        content += f"**Unresolved Questions:** {analysis_result.get('unresolved_questions', 'None recorded')}\n\n"
        content += f"**Action Items:** {analysis_result.get('action_items', 'None recorded')}\n"
    
    if analysis_result.get('scope_flags'):
        content += f"\n**Scope Checker Flags:** {', '.join(analysis_result['scope_flags'])}"
    
    return jsonify({'content': content})

@app.errorhandler(413)
def too_large(e):
    flash('File too large. Please upload files smaller than 50MB.', 'error')
    return redirect(url_for('index'))
