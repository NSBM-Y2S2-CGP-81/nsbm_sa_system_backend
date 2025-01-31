from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.data_service import store_data, fetch_data

data_bp = Blueprint('data', __name__)

@data_bp.route('/store', methods=['POST'])
@jwt_required()
def store():
    data = request.json
    return store_data(data)

@data_bp.route('/fetch', methods=['GET'])
@jwt_required()
def fetch():
    return fetch_data()
