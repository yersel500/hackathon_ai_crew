from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import json
from ..models import db 
from cryptography.fernet import Fernet, InvalidToken
import base64
import os

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255))
    processed_content_hash = db.Column(db.Text)  # Contenido hasheado
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    @property
    def _fernet(self):
        """Lazy initialization of Fernet"""
        if not hasattr(self, '_fernet_instance'):
            try:
                key = base64.urlsafe_b64encode(hashlib.sha256(current_app.config['SECRET_KEY'].encode()).digest())
                self._fernet_instance = Fernet(key)
            except Exception as e:
                current_app.logger.error(f"Error initializing Fernet: {str(e)}")
                raise
        return self._fernet_instance
    
    def set_content(self, content):
        """Encripta el contenido antes de guardarlo"""
        try:
            if isinstance(content, dict):
                content = json.dumps(content)
            
            if not content:
                current_app.logger.warning(f"Empty content for document {self.filename}")
                return
            
            # Encriptar el contenido
            encrypted = self._fernet.encrypt(content.encode())
            self.processed_content_hash = encrypted.decode()
            current_app.logger.info(f"Content encrypted successfully for {self.filename}")
            
        except Exception as e:
            current_app.logger.error(f"Error encrypting content for {self.filename}: {str(e)}")
            raise
    
    def get_content(self):
        """Desencripta y retorna el contenido original"""
        try:
            if not self.processed_content_hash:
                current_app.logger.warning(f"No content hash found for document {self.filename}")
                return None

            # Desencriptar el contenido
            decrypted = self._fernet.decrypt(self.processed_content_hash.encode())
            content = decrypted.decode()
            current_app.logger.info(f"Content decrypted successfully for {self.filename}")
            return content
            
        except InvalidToken:
            current_app.logger.error(f"Invalid token for document {self.filename}. Possible key mismatch.")
            return None
        except Exception as e:
            current_app.logger.error(f"Error decrypting content for {self.filename}: {str(e)}")
            return None