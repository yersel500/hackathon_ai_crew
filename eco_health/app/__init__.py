# app/__init__.py
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from .models import db
from .models.user import User
from .models.document import Document
from .config import Config
from sqlalchemy import inspect

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.login_view = 'user_routes.login'
    login_manager.init_app(app)

    # Define user_loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register blueprints
    from .routes.user_routes import user_routes
    from .routes.map_routes import map_routes
    from .routes.chat_routes import chat_routes
    from .routes.main import main
    from .routes.document_routes import document_routes
    
    app.register_blueprint(user_routes)
    app.register_blueprint(map_routes)
    app.register_blueprint(chat_routes)
    app.register_blueprint(main)
    app.register_blueprint(document_routes)

    return app

def init_db(app):
    with app.app_context():
        try:
            # Create all tables
            print("Creating all tables...")
            db.create_all()
            
            # Verify the users table exists
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print("Created tables:", tables)
            
            if 'users' in tables and 'documents' in tables:
                print("Users table created successfully!")
            else:
                print("Users table was not created!")
            
        except Exception as e:
            print("Error during database initialization:", str(e))
            raise e