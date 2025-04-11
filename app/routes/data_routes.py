from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.services.data_service import fetch_all_data, store_data, fetch_data_by_id, delete_event_request, approve_event_request
from app.services.loggerService import LoggerService
from flask import request, jsonify, make_response

data_bp = Blueprint('data', __name__)
logger = LoggerService()

def is_admin():
    """Check if the current user is an admin."""
    claims = get_jwt()
    return claims.get("role") == "superuser"

@data_bp.route('/<collection_name>/store', methods=['POST'])
@jwt_required()
def store(collection_name):
    if collection_name in ["users", "admins"] and not is_admin():
        logger.warning(f"Unauthorized access attempt to {collection_name} collection.")
        return jsonify({"error": "Elevated privileges required"}), 403
    data = request.json
    logger.info(f"Storing data in {collection_name} collection, DATA: {data}")
    return store_data(collection_name,data)

@data_bp.route('/<collection_name>/fetch', methods=['GET'])
@jwt_required()
def fetch_all(collection_name):
    if collection_name in ["users", "admins"] and not is_admin():
        logger.warning(f"Unauthorized access attempt to {collection_name} collection.")
        return jsonify({"error": "Elevated privileges required"}), 403

    logger.info(f"Fetching all data from {collection_name} collection.")
    return fetch_all_data(collection_name)

@data_bp.route('/<collection_name>/fetch/<record_id>', methods=['GET'])
@jwt_required()
def fetch_by_id(collection_name, record_id):
    if collection_name in ["users", "admins"] and not is_admin():
        logger.warning(f"Unauthorized access attempt to {collection_name} collection.")
        return jsonify({"error": "Elevated privileges required"}), 403

    logger.info(f"Fetching data by ID from {collection_name} collection, ID: {record_id}")
    return fetch_data_by_id(collection_name, record_id)

@data_bp.route('/<collection_name>/delete/<record_id>', methods=['DELETE'])
@jwt_required()
def delete_request(collection_name, record_id):
    logger.info(f"Deleting event request with ID: {record_id}")
    return delete_event_request(collection_name, record_id)

@data_bp.route('/<collection_name>/approve/<record_id>', methods=['POST', 'OPTIONS'])
@jwt_required(optional=True)
def approve_request(collection_name, record_id):
    if request.method == 'OPTIONS':
        # Return a 200 OK for preflight requests
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response
    logger.info(f"Approving event request with ID: {record_id}")
    return approve_event_request(collection_name, record_id)

@data_bp.route('/<collection_name>/update/<record_id>', methods=['PUT'])
@jwt_required()
def update_record(collection_name, record_id):
    if collection_name in ["users", "admins"] and not is_admin():
        logger.warning(f"Unauthorized update attempt in {collection_name} collection.")
        return jsonify({"error": "Elevated privileges required"}), 403

    data = request.json
    logger.info(f"Updating record in {collection_name} collection with ID: {record_id}, DATA: {data}")
    return update_data(collection_name, record_id, data)
