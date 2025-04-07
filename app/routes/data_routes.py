from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.services.data_service import fetch_all_data, store_data, fetch_data_by_id

data_bp = Blueprint('data', __name__)

def is_admin():
    """Check if the current user is an admin."""
    claims = get_jwt()
    return claims.get("role") == "superuser"

@data_bp.route('/<collection_name>/store', methods=['POST'])
@jwt_required()
def store(collection_name):
    if collection_name in ["users", "admins"] and not is_admin():
        return jsonify({"error": "Elevated privileges required"}), 403

    data = request.json
    return store_data(collection_name, data)

@data_bp.route('/<collection_name>/fetch', methods=['GET'])
@jwt_required()
def fetch_all(collection_name):
    if collection_name in ["users", "admins"] and not is_admin():
        return jsonify({"error": "Elevated privileges required"}), 403

    return fetch_all_data(collection_name)

@data_bp.route('/<collection_name>/fetch/<record_id>', methods=['GET'])
@jwt_required()
def fetch_by_id(collection_name, record_id):
    if collection_name in ["users", "admins"] and not is_admin():
        return jsonify({"error": "Elevated privileges required"}), 403

    return fetch_data_by_id(collection_name, record_id)
