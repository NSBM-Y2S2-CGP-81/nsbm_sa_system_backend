from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app import bcrypt
from app.services.custom_service import custom_function
from app.services.loggerService import LoggerService

custom_bp = Blueprint('custom', __name__)
logger = LoggerService()

def is_admin():
    """Check if the current user is an admin."""
    claims = get_jwt()
    return claims.get("role") == "superuser"

def check_mic():
    """Check if the current user is a MIC."""
    claims = get_jwt()
    return claims.get("role") == "elevateduser"

@custom_bp.route('/execute', methods=['POST'])
@jwt_required()
def execute():
    data = request.json
    logger.info(f"Custom function execution requested with data: {data}")
    return custom_function(data)

@custom_bp.route('/hash-password', methods=['POST'])
@jwt_required()
def hash_password():
    if not is_admin() and not check_mic():
        logger.warning("Non-admin user attempted to access hash-password endpoint")
        return jsonify({"error": "Admin privileges required"}), 403

    data = request.json
    if not data or not data.get("plaintext"):
        logger.warning("Missing plaintext in hash-password request")
        return jsonify({"error": "Plain text is required"}), 400

    try:
        plain_text = data["plaintext"]
        hashed_password = bcrypt.generate_password_hash(plain_text).decode('utf-8')
        logger.info("Password hashing successful")
        return jsonify({
            "hash": hashed_password,
            "message": "Password hashed successfully"
        }), 200
    except Exception as e:
        logger.error(f"Error generating password hash: {str(e)}")
        return jsonify({"error": f"Failed to hash password: {str(e)}"}), 500
