from datetime import datetime
from app import db

class ProcessingSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    content_type = db.Column(db.String(50))  # 'audio' or 'text'
    classification = db.Column(db.String(50))  # 'client' or 'internal'
    original_text = db.Column(db.Text)
    transcribed_text = db.Column(db.Text)
    analysis_result = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ProcessingSession {self.id}>'
