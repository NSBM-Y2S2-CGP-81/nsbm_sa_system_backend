from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.services.data_service import fetch_all_data, store_data, fetch_data_by_id
from app.services.loggerService import LoggerService  # Fixed typo here

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
