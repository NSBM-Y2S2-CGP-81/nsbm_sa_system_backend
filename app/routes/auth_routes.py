from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user, admin_login
from app.services.loggerService import LoggerService

auth_bp = Blueprint('auth', __name__)
logger = LoggerService()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    logger.info(f"Registering a new user triggered, DATA: {data}")
    return register_user(data)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    logger.info(f"Login triggered, DATA: {data}")
    return login_user(data)

@auth_bp.route('/admin', methods=['POST'])
def admin():
    data = request.json
    logger.info(f"Admin login triggered, DATA: {data}")
    return admin_login(data)
