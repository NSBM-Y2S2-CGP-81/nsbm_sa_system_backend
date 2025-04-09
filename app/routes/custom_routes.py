from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.custom_service import custom_function
from app.services.loggerService import LoggerService

custom_bp = Blueprint('custom', __name__)
logger = LoggerService()

@custom_bp.route('/execute', methods=['POST'])
@jwt_required()
def execute():
    data = request.json
    logger.info(f"Custom function execution requested with data: {data}")
    return custom_function(data)
