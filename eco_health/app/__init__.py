# app/__init__.py
from flask import Flask, g, request
from flask_cors import CORS
from dotenv import load_dotenv
from .routes.user_routes import token_required, get_user_from_token
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Middleware para verificar el usuario actual en cada petición
    @app.before_request
    def before_request():
        g.user = None
        token = request.cookies.get('token') or request.headers.get('Authorization')
        if token:
            if token.startswith('Bearer '):
                token = token.split(' ')[1]
            user = get_user_from_token(token)
            if user:
                g.user = user

    # Context processor para hacer current_user disponible en todos los templates
    @app.context_processor
    def inject_user():
        return dict(current_user=g.get('user', None))

    # Importar y registrar blueprints
    from .routes.user_routes import user_routes
    from .routes.map_routes import map_routes
    
    app.register_blueprint(user_routes)
    app.register_blueprint(map_routes)

    return app