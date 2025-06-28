import json
import os
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)

def transcribe_audio_file(audio_file_path):
    """Transcribe audio file using OpenAI Whisper"""
    try:
        with open(audio_file_path, "rb") as audio_file:
            response = openai.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
        return response.text
    except Exception as e:
        raise Exception(f"Failed to transcribe audio: {str(e)}")

def classify_content(text):
    """Classify content as client conversation or internal meeting"""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """You are a business content classifier. Analyze the text and determine if it's:
                    - 'client': A conversation with clients, customers, or external stakeholders about projects, requirements, or business discussions
                    - 'internal': An internal team meeting, standup, planning session, or internal company discussion
                    
                    Respond with JSON in this format: {'classification': 'client' or 'internal', 'confidence': number between 0 and 1}"""
                },
                {"role": "user", "content": text}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get('classification', 'client')
        
    except Exception as e:
        raise Exception(f"Failed to classify content: {str(e)}")

def analyze_content(text, classification):
    """Analyze content based on classification and generate structured output"""
    
    if classification == 'client':
        return analyze_client_conversation(text)
    else:
        return analyze_internal_meeting(text)

def analyze_client_conversation(text):
    """Generate project brief from client conversation"""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """You are a business analyst specializing in client conversations. Analyze the conversation and extract key information to create a professional project brief.

                    Generate a JSON response with the following structure:
                    {
                        "title": "Brief title based on the conversation",
                        "goals": "Primary objectives and goals mentioned",
                        "deliverables": "Specific deliverables or outcomes expected",
                        "timeline": "Timeline, deadlines, or schedule mentioned",
                        "budget": "Budget constraints or financial discussions",
                        "tone": "Overall tone and relationship dynamic (formal/casual/collaborative/etc)",
                        "follow_up_email": "Professional follow-up email draft",
                        "scope_flags": ["list of vague or missing information that needs clarification"]
                    }
                    
                    If any information is not clearly specified, mark it as "Not specified" rather than making assumptions."""
                },
                {"role": "user", "content": text}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # Add scope checking
        result['scope_flags'] = check_scope_completeness(result, 'client')
        
        return result
        
    except Exception as e:
        raise Exception(f"Failed to analyze client conversation: {str(e)}")

def analyze_internal_meeting(text):
    """Generate meeting summary from internal meeting"""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """You are a meeting summarization expert. Analyze the internal meeting transcript and create a structured summary.

                    Generate a JSON response with the following structure:
                    {
                        "title": "Meeting summary title",
                        "decisions": "Key decisions that were made during the meeting",
                        "key_points": "Important discussion points and insights",
                        "unresolved_questions": "Questions that remain unanswered or need follow-up",
                        "action_items": "Specific tasks, assignments, or next steps identified",
                        "scope_flags": ["list of unclear or incomplete items that need clarification"]
                    }
                    
                    If any category has no relevant content, indicate "None recorded" rather than leaving empty."""
                },
                {"role": "user", "content": text}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # Add scope checking
        result['scope_flags'] = check_scope_completeness(result, 'internal')
        
        return result
        
    except Exception as e:
        raise Exception(f"Failed to analyze internal meeting: {str(e)}")

def check_scope_completeness(analysis_result, content_type):
    """Check for vague or missing information and return flags"""
    flags = []
    
    if content_type == 'client':
        # Check client conversation completeness
        if analysis_result.get('goals') in ['Not specified', '', None]:
            flags.append('Goals not clearly defined')
            
        if analysis_result.get('deliverables') in ['Not specified', '', None]:
            flags.append('Deliverables not specified')
            
        if analysis_result.get('timeline') in ['Not specified', '', None]:
            flags.append('Timeline not established')
            
        if analysis_result.get('budget') in ['Not specified', '', None]:
            flags.append('Budget not discussed')
            
        # Check for vague language
        vague_terms = ['maybe', 'possibly', 'might', 'could be', 'not sure', 'unclear']
        content_to_check = f"{analysis_result.get('goals', '')} {analysis_result.get('deliverables', '')}"
        
        if any(term in content_to_check.lower() for term in vague_terms):
            flags.append('Vague requirements detected')
            
    else:
        # Check internal meeting completeness
        if analysis_result.get('decisions') in ['None recorded', '', None]:
            flags.append('No clear decisions recorded')
            
        if analysis_result.get('action_items') in ['None recorded', '', None]:
            flags.append('No action items identified')
            
        if analysis_result.get('unresolved_questions') not in ['None recorded', '', None]:
            flags.append('Unresolved questions need follow-up')
    
    return flags
