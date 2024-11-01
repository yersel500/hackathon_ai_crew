from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import json
from ..models import db 

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255))
    processed_content_hash = db.Column(db.String(512))  # Contenido hasheado
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def set_content(self, content):
        """Hash the content before storing"""
        content_str = json.dumps(content) if isinstance(content, dict) else str(content)
        self.processed_content_hash = hashlib.sha256(content_str.encode()).hexdigest()
        
    def get_content(self):
        """Retrieve the hashed content"""
        return self.processed_content_hash
    
    def __repr__(self):
        return f'<Document {self.filename}>'