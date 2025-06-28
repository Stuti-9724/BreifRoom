# Briefroom - AI-Powered Meeting Analysis System

Transform audio recordings and text conversations into structured project briefs and meeting summaries using OpenAI's GPT-4o and Whisper models.

![Briefroom Screenshot](https://via.placeholder.com/800x400/6366f1/ffffff?text=Briefroom+Interface)

## Features

### 🎤 **Audio Transcription**
- Upload MP3 or WAV files (up to 50MB)
- Automatic transcription using OpenAI Whisper
- Drag-and-drop file upload interface

### 🤖 **Intelligent Classification**
- Automatically classifies content as:
  - **Client Conversations** → Generate professional project briefs
  - **Internal Meetings** → Create structured meeting summaries
- Manual classification override option

### 📋 **Client Conversation Analysis**
Generates comprehensive project briefs including:
- **Goals** - Primary objectives and project goals
- **Deliverables** - Specific outcomes and deliverables
- **Timeline** - Deadlines and project schedule
- **Budget** - Financial constraints and discussions
- **Tone** - Relationship dynamic and communication style
- **Follow-up Email** - Professional email draft for next steps

### 📝 **Internal Meeting Summaries**
Creates structured summaries with:
- **Key Decisions** - Important decisions made during the meeting
- **Key Points** - Critical discussion points and insights
- **Unresolved Questions** - Items requiring follow-up
- **Action Items** - Specific tasks and assignments

### ✅ **Scope Checker**
Automatically flags:
- Missing or vague requirements
- Undefined timelines or budgets
- Unclear deliverables
- Unresolved questions needing follow-up

### 📤 **Export Options**
- **PDF Export** - Professional report generation
- **Copy to Clipboard** - Easy sharing of analysis results
- Clean, formatted output for documentation

## Technology Stack

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - Database ORM
- **OpenAI API** - GPT-4o for analysis, Whisper for transcription
- **ReportLab** - PDF generation
- **Gunicorn** - WSGI HTTP server

### Frontend
- **Bootstrap 5** - CSS framework
- **Feather Icons** - Icon library
- **Vanilla JavaScript** - Client-side functionality
- **Responsive Design** - Mobile-friendly interface

### Database
- **SQLite** - Default database (configurable)
- **PostgreSQL** - Production-ready option

## Installation

### Prerequisites
- Python 3.11 or higher
- OpenAI API key

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd briefroom
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export SESSION_SECRET="your-secret-key"
   export DATABASE_URL="sqlite:///briefroom.db"  # Optional
   ```

4. **Run the application**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --reload main:app
   ```

5. **Access the application**
   Open your browser to `http://localhost:5000`

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI services | Yes | - |
| `SESSION_SECRET` | Flask session secret key | Recommended | Auto-generated |
| `DATABASE_URL` | Database connection string | No | `sqlite:///briefroom.db` |

## Usage

### 1. Upload Content
- **Audio Files**: Drag and drop or click to upload MP3/WAV files
- **Text Input**: Paste meeting transcripts, emails, or chat conversations

### 2. Choose Classification (Optional)
- Let AI automatically detect content type
- Or manually select "Client Conversation" or "Internal Meeting"

### 3. Process and Review
- AI analyzes content and generates structured output
- Review scope checker flags for missing information
- Export as PDF or copy to clipboard

### 4. Export Results
- **PDF Export**: Professional report with all analysis details
- **Copy to Clipboard**: Formatted text for easy sharing

## Project Structure

```
briefroom/
├── app.py              # Flask application setup
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # Web routes and handlers
├── ai_service.py       # OpenAI API integration
├── pdf_service.py      # PDF generation service
├── static/             # Static assets
│   ├── css/style.css   # Custom styles
│   └── js/main.js      # JavaScript functionality
├── templates/          # HTML templates
│   ├── base.html       # Base template
│   ├── index.html      # Home page
│   └── results.html    # Results page
├── uploads/            # Temporary file storage
└── README.md           # This file
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with upload interface |
| `/process` | POST | Process uploaded content |
| `/results` | GET | Display analysis results |
| `/export/pdf/<session_id>` | GET | Export results as PDF |
| `/api/copy-content/<session_id>` | GET | Get formatted content for clipboard |

## Database Schema

### ProcessingSession
- `id` - Primary key
- `filename` - Original file name (if uploaded)
- `content_type` - 'audio' or 'text'
- `classification` - 'client' or 'internal'
- `original_text` - Original text input
- `transcribed_text` - Transcribed/processed text
- `analysis_result` - JSON analysis results
- `created_at` - Timestamp

## Security Features

- File type validation for uploads
- File size limits (50MB maximum)
- Secure filename handling
- Session management
- Temporary file cleanup
- Input sanitization

## Performance Considerations

- Automatic cleanup of uploaded files
- Connection pooling for database
- Efficient PDF generation
- Responsive design for mobile devices
- Graceful error handling

## Error Handling

The application includes comprehensive error handling for:
- Invalid file types or sizes
- OpenAI API failures
- Database connection issues
- Network timeouts
- Missing required fields

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For questions or issues:
1. Check the error logs in the application
2. Verify your OpenAI API key is valid
3. Ensure all environment variables are set correctly
4. Check file size and format requirements

## Changelog

### Version 1.0.0 (June 28, 2025)
- Initial release
- Audio transcription with OpenAI Whisper
- Content classification and analysis
- PDF export functionality
- Scope checker implementation
- Responsive web interface

---

**Built with ❤️ using Flask and OpenAI**