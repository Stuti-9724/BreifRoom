import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime

def generate_pdf(processing_session, analysis_result):
    """Generate PDF report from analysis results"""
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, 
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#2c3e50')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.HexColor('#34495e'),
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        leading=14
    )
    
    # Build the document content
    story = []
    
    # Title
    title = analysis_result.get('title', 'Briefroom Analysis Report')
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 12))
    
    # Metadata table
    metadata = [
        ['Generated:', datetime.now().strftime('%B %d, %Y at %I:%M %p')],
        ['Content Type:', processing_session.content_type.title()],
        ['Classification:', processing_session.classification.title()],
    ]
    
    if processing_session.filename:
        metadata.append(['Source File:', processing_session.filename])
    
    metadata_table = Table(metadata, colWidths=[1.5*inch, 4*inch])
    metadata_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(metadata_table)
    story.append(Spacer(1, 20))
    
    # Content based on classification
    if processing_session.classification == 'client':
        add_client_content(story, analysis_result, heading_style, body_style)
    else:
        add_internal_content(story, analysis_result, heading_style, body_style)
    
    # Scope flags if any
    if analysis_result.get('scope_flags'):
        story.append(Spacer(1, 20))
        story.append(Paragraph("⚠️ Scope Checker Flags", heading_style))
        for flag in analysis_result['scope_flags']:
            story.append(Paragraph(f"• {flag}", body_style))
    
    # Original transcript
    story.append(Spacer(1, 30))
    story.append(Paragraph("Original Transcript", heading_style))
    transcript = processing_session.transcribed_text or "No transcript available"
    story.append(Paragraph(transcript, body_style))
    
    # Build PDF
    doc.build(story)
    pdf_content = buffer.getvalue()
    buffer.close()
    
    return pdf_content

def add_client_content(story, analysis_result, heading_style, body_style):
    """Add client conversation content to PDF"""
    
    sections = [
        ('Goals', 'goals'),
        ('Deliverables', 'deliverables'),
        ('Timeline', 'timeline'),
        ('Budget', 'budget'),
        ('Tone', 'tone')
    ]
    
    for section_title, key in sections:
        story.append(Paragraph(section_title, heading_style))
        content = analysis_result.get(key, 'Not specified')
        story.append(Paragraph(content, body_style))
        story.append(Spacer(1, 12))
    
    # Follow-up email
    if analysis_result.get('follow_up_email'):
        story.append(Paragraph("Follow-up Email Draft", heading_style))
        story.append(Paragraph(analysis_result['follow_up_email'], body_style))

def add_internal_content(story, analysis_result, heading_style, body_style):
    """Add internal meeting content to PDF"""
    
    sections = [
        ('Key Decisions', 'decisions'),
        ('Key Points', 'key_points'),
        ('Unresolved Questions', 'unresolved_questions'),
        ('Action Items', 'action_items')
    ]
    
    for section_title, key in sections:
        story.append(Paragraph(section_title, heading_style))
        content = analysis_result.get(key, 'None recorded')
        story.append(Paragraph(content, body_style))
        story.append(Spacer(1, 12))
