from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from datetime import datetime
from ..models.user import db
from ..models.deletion_request import DeletionRequest 

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')

@main.route('/privacy')
def privacy():
    return render_template('auth/privacy.html')

@main.route('/api/accept-privacy', methods=['POST'])
@login_required
def accept_privacy():
    try:
        # Guardar la aceptación en la base de datos
        current_user.privacy_accepted = True
        current_user.privacy_accepted_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/request-deletion', methods=['POST'])
@login_required
def request_deletion():
    try:
        data = request.get_json()
        # Crear registro de solicitud de eliminación
        deletion_request = DeletionRequest(
            user_id=current_user.id,
            reason=data.get('reason'),
            status='pending'
        )
        db.session.add(deletion_request)
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500