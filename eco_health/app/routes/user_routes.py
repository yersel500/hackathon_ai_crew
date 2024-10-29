# app/routes/user_routes.py
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, make_response
from ..models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from os import getenv

user_routes = Blueprint('user_routes', __name__)
user_model = User()

# Configuración JWT
JWT_SECRET = getenv('JWT_SECRET', 'your-secret-key')

# app/routes/user_routes.py
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print("\n=== Entering token_required decorator ===")
        print(f"Request method: {request.method}")
        print(f"Request path: {request.path}")
        print(f"Request headers:")
        for header, value in request.headers:
            print(f"  {header}: {value}")
        
        print("\nRequest cookies:")
        for key, value in request.cookies.items():
            print(f"  {key}: {value}")
        
        # Print raw cookie string
        raw_cookies = request.headers.get('Cookie')
        print(f"\nRaw Cookie string: {raw_cookies}")
        
        # Manually parse cookies
        cookies = {}
        if raw_cookies:
            for cookie in raw_cookies.split(';'):
                parts = cookie.strip().split('=')
                if len(parts) == 2:
                    cookies[parts[0]] = parts[1]
        
        print("\nManually parsed cookies:")
        for key, value in cookies.items():
            print(f"  {key}: {value}")
        
        token = cookies.get('token') or request.cookies.get('token')
        print(f"\nToken from cookie: {token}")
        print(f"JWT_SECRET: {JWT_SECRET}")  # Be careful with this in production
        
        if not token:
            print("Token is missing in the request")
            print("Redirecting to login page")
            return redirect(url_for('user_routes.login_page'))

        try:
            print(f"\nAttempting to decode token: {token}")
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            print(f"Decoded token data: {data}")
            current_user = user_model.get_user(data['user_id'])
            
            if not current_user:
                print(f"User not found for user_id: {data['user_id']}")
                return jsonify({'error': 'User not found'}), 401
            
            print(f"User authenticated: {current_user['email']}")
            print("=== Exiting token_required decorator ===\n")
            return f(current_user, *args, **kwargs)
            
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            print(f"\nInvalid or expired token: {str(e)}")
            print(f"Token: {token}")
            print(f"JWT_SECRET: {JWT_SECRET}")  # Be careful with this in production
            print("Redirecting to login page")
            return redirect(url_for('user_routes.login_page'))
        except Exception as e:
            print(f"\nException in token_required: {str(e)}")
            print(f"Exception type: {type(e)}")
            print(f"Exception args: {e.args}")
            print(f"Token: {token}")
            print(f"JWT_SECRET: {JWT_SECRET}")  # Be careful with this in production
            print("Redirecting to login page")
            return redirect(url_for('user_routes.login_page'))
            
    return decorated

@user_routes.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        # Validar datos requeridos
        required_fields = ['email', 'password', 'name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing {field}'}), 400

        # Verificar si el usuario ya existe
        existing_user = user_model.get_user(data['email'])
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400

        # Crear usuario nuevo
        user_data = {
            'email': data['email'],
            'password': generate_password_hash(data['password']),
            'name': data['name'],
            'medical_conditions': data.get('medical_conditions', []),
            'age': data.get('age'),
            'location': data.get('location')
        }

        result = user_model.create_user(user_data)
        
        # Generar token
        token = jwt.encode({
            'user_id': result['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }, JWT_SECRET)

        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': {
                'id': result['id'],
                'name': result['name'],
                'email': result['email']
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_routes.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print(f"Login attempt for email: {data.get('email')}")

        user = user_model.get_user(data['email'])
        if not user:
            print("User not found")
            return jsonify({'error': 'User not found'}), 404

        if not check_password_hash(user['password'], data['password']):
            print("Invalid password")
            return jsonify({'error': 'Invalid password'}), 401

        # Generate token with id as identifier
        token = jwt.encode({
            'user_id': user['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }, JWT_SECRET)

        print(f"Token generated: {token}")
        print(f"JWT_SECRET used for encoding: {JWT_SECRET}")  # Be careful with this in production

        # Set token as a HTTP-only cookie, secure only in production
        is_secure = getenv('FLASK_ENV') == 'production'
        
        # Create a JSON response
        response = jsonify({
            'message': 'Login successful',
            'redirect': url_for('map_routes.show_map')
        })
        response.set_cookie('token', token, httponly=True, secure=is_secure, samesite='Lax', max_age=86400, path='/')
        
        print(f"Response headers: {response.headers}")
        print(f"Response cookies: {response.headers.get('Set-Cookie')}")
        
        # Log the entire response object
        print(f"Full response object: {response}")
        print(f"Response status code: {response.status_code}")
        print(f"Response mimetype: {response.mimetype}")
        
        return response, 200

    except Exception as e:
        print(f"Login error: {e}")
        print(f"Exception type: {type(e)}")
        print(f"Exception args: {e.args}")
        return jsonify({'error': str(e)}), 500

@user_routes.route('/api/auth/logout', methods=['POST'])
def logout():
    response = jsonify({'message': 'Logout successful'})
    response.delete_cookie('token')
    return response


@user_routes.route('/api/user/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    try:
        return jsonify(current_user)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_routes.route('/api/user/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    try:
        data = request.get_json()
        
        # No permitir actualización de email o password por esta ruta
        update_data = {
            'name': data.get('name', current_user['name']),
            'medical_conditions': data.get('medical_conditions', current_user.get('medical_conditions', [])),
            'age': data.get('age', current_user.get('age')),
            'location': data.get('location', current_user.get('location'))
        }

        result = user_model.update_user(current_user['id'], update_data)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_routes.route('/api/auth/change-password', methods=['POST'])
@token_required
def change_password(current_user):
    try:
        data = request.get_json()
        
        if not data.get('current_password') or not data.get('new_password'):
            return jsonify({'error': 'Current and new password are required'}), 400

        # Verificar contraseña actual
        if not check_password_hash(current_user['password'], data['current_password']):
            return jsonify({'error': 'Current password is incorrect'}), 401

        # Actualizar contraseña
        update_data = {
            'password': generate_password_hash(data['new_password'])
        }
        
        user_model.update_user(current_user['id'], update_data)
        return jsonify({'message': 'Password updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@user_routes.route('/register', methods=['GET'])
def register_page():
    return render_template('auth/register.html')

@user_routes.route('/login', methods=['GET'])
def login_page():
    return render_template('auth/login.html')

@user_routes.route('/profile', methods=['GET'])
@token_required
def profile_page(current_user):
    try:
        if not current_user:
            return redirect(url_for('user_routes.login_page'))
        return render_template('auth/profile.html', user=current_user)
    except Exception as e:
        print(f"Error en profile_page: {e}")  # Para debugging
        return redirect(url_for('user_routes.login_page'))
    
def get_user_from_token(token):
    """Utilidad para obtener el usuario desde un token"""
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return user_model.get_user(data['user_id'])
    except:
        return None