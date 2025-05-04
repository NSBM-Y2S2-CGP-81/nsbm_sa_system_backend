from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.services.email_service import EmailService
from app.services.loggerService import LoggerService

email_bp = Blueprint('email', __name__)
logger = LoggerService()
email_service = EmailService()

def is_admin():
    """Check if the current user is an admin."""
    claims = get_jwt()
    return claims.get("role") == "superuser"

@email_bp.route('/send', methods=['POST'])
@jwt_required()
def send_email():
    data = request.json

    # Validate required fields
    if not all(key in data for key in ['to', 'subject', 'message']):
        logger.warning("Missing required fields in email request")
        return jsonify({"error": "Missing required fields. 'to', 'subject', and 'message' are required"}), 400

    # Get the email data
    recipient_email = data['to']
    subject = data['subject']
    message = data['message']
    html_content = data.get('html_content')  # Optional HTML content

    # Send the email
    success, msg = email_service.send_email(recipient_email, subject, message, html_content)

    if success:
        return jsonify({"message": msg}), 200
    else:
        return jsonify({"error": msg}), 500
