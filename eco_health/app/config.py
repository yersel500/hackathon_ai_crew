from os import environ
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = environ.get('SECRET_KEY', 'your-secret-key')
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/flask_auth')
    SQLALCHEMY_TRACK_MODIFICATIONS = False