# app/routes/data_routes.py
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.data_service import fetch_all_data, store_data, fetch_data_by_id

data_bp = Blueprint('data', __name__)

@data_bp.route('/<collection_name>/store', methods=['POST'])
@jwt_required()
def store(collection_name):
    data = request.json
    return store_data(collection_name, data)

@data_bp.route('/<collection_name>/fetch', methods=['GET'])
@jwt_required()
def fetch_all(collection_name):
    return fetch_all_data(collection_name)

@data_bp.route('/<collection_name>/fetch/<record_id>', methods=['GET'])
@jwt_required()
def fetch_by_id(collection_name, record_id):
    return fetch_data_by_id(collection_name, record_id)
