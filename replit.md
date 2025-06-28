# Briefroom - AI-Powered Meeting Analysis System

## Overview

Briefroom is a Flask-based web application that transforms audio recordings and text conversations into structured project briefs and meeting summaries using OpenAI's GPT-4o and Whisper models. The system automatically classifies content as either client conversations or internal meetings, then generates appropriate analysis and documentation.

## System Architecture

### Backend Architecture
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: SQLite (configurable to other databases via DATABASE_URL)
- **AI Integration**: OpenAI API (GPT-4o for analysis, Whisper for transcription)
- **File Handling**: Werkzeug for secure file uploads
- **PDF Generation**: ReportLab for document export

### Frontend Architecture
- **Template Engine**: Jinja2 templates
- **CSS Framework**: Bootstrap 5.3.0
- **Icons**: Feather Icons
- **JavaScript**: Vanilla JS for file upload and form handling

### Application Structure
```
/
├── app.py              # Flask application factory and configuration
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # Web routes and handlers
├── ai_service.py       # OpenAI API integration
├── pdf_service.py      # PDF generation service
├── static/             # Static assets (CSS, JS)
├── templates/          # HTML templates
└── uploads/            # Temporary file storage
```

## Key Components

### 1. Content Processing Pipeline
- **Audio Upload**: Accepts MP3/WAV files up to 50MB
- **Transcription**: Uses OpenAI Whisper for speech-to-text
- **Text Input**: Direct text input for already transcribed content
- **Classification**: AI-powered classification as 'client' or 'internal' meetings
- **Analysis**: Context-aware analysis based on classification type

### 2. Data Models
- **ProcessingSession**: Stores session metadata, content, and analysis results
  - Tracks filename, content type, classification
  - Stores original text, transcribed text, and analysis results
  - Includes timestamp for audit trail

### 3. AI Services
- **Transcription Service**: OpenAI Whisper integration for audio-to-text
- **Classification Service**: GPT-4o powered content classification
- **Analysis Service**: Context-aware analysis generation (implementation pending)

### 4. Export Capabilities
- **PDF Generation**: Professional report generation using ReportLab
- **Copy to Clipboard**: Easy sharing of analysis results

## Data Flow

1. **Content Input**
   - User uploads audio file or inputs text
   - Optional manual classification override

2. **Processing**
   - Audio files are transcribed using Whisper
   - Content is classified as client/internal using GPT-4o
   - Analysis is generated based on classification

3. **Storage**
   - Session data stored in database
   - Temporary files cleaned up after processing

4. **Output**
   - Results displayed in structured web interface
   - Export options available (PDF, copy)

## External Dependencies

### AI Services
- **OpenAI API**: GPT-4o and Whisper models
- **API Key**: Required via OPENAI_API_KEY environment variable

### Python Libraries
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **OpenAI**: Official Python client
- **ReportLab**: PDF generation
- **Werkzeug**: File handling utilities

### Frontend Libraries
- **Bootstrap 5.3.0**: CSS framework (CDN)
- **Feather Icons**: Icon library (CDN)

## Deployment Strategy

### Environment Configuration
- **SESSION_SECRET**: Flask session security
- **DATABASE_URL**: Database connection string (defaults to SQLite)
- **OPENAI_API_KEY**: Required for AI functionality

### File System Requirements
- **Upload Directory**: Temporary storage for audio files
- **Database**: SQLite file or external database connection

### Security Considerations
- File upload validation (type and size limits)
- Secure filename handling
- Session management
- Proxy fix for deployment behind reverse proxy

## Changelog
- June 28, 2025: Initial setup and complete implementation
- June 28, 2025: Added comprehensive README.md with full documentation
- June 28, 2025: Created detailed Render deployment guide (DEPLOY_TO_RENDER.md)

## User Preferences

Preferred communication style: Simple, everyday language.

## Implementation Notes

### Current Status
- Core infrastructure is complete
- Audio transcription is implemented
- Content classification is implemented  
- Analysis generation function exists but implementation is incomplete
- PDF export infrastructure is in place but may need completion
- Frontend provides full user interface for upload and results

### Key Architectural Decisions

1. **Flask + SQLAlchemy**: Chosen for rapid development and flexibility. Allows easy database switching via configuration.

2. **OpenAI Integration**: Uses latest models (GPT-4o, Whisper) for high-quality analysis. Centralized in ai_service.py for maintainability.

3. **File Upload Strategy**: Temporary storage with immediate cleanup to minimize storage requirements and security risks.

4. **Classification-Based Analysis**: Two-tier approach (classify first, then analyze) allows for context-appropriate output generation.

5. **Session-Based Storage**: Each processing session is stored for audit trail and potential re-analysis.

The system is designed for scalability with configurable database backends and clean separation of concerns between web interface, AI processing, and data persistence layers.