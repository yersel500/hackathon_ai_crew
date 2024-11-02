# app/models/deletion_request.py
from datetime import datetime
from . import db

class DeletionRequest(db.Model):
    __tablename__ = 'deletion_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, processed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)

    # Relación con el usuario
    user = db.relationship('User', backref=db.backref('deletion_requests', lazy=True))