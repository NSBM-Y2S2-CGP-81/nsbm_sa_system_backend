from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user, admin_login

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    return register_user(data)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    return login_user(data)

@auth_bp.route('/admin', methods=['POST'])
def admin():
    data = request.json
    return admin_login(data)
