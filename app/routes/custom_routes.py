from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.custom_service import custom_function

custom_bp = Blueprint('custom', __name__)

@custom_bp.route('/execute', methods=['POST'])
@jwt_required()
def execute():
    data = request.json
    return custom_function(data)
