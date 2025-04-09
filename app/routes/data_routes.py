from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.services.data_service import fetch_all_data, store_data, fetch_data_by_id
import os
from werkzeug.utils import secure_filename
os.makedirs('uploads', exist_ok=True)

data_bp = Blueprint('data', __name__)

def is_admin():
    """Check if the current user is an admin."""
    claims = get_jwt()
    return claims.get("role") == "superuser"

@data_bp.route('/<collection_name>/store', methods=['POST'])
@jwt_required()
@data_bp.route('/<collection_name>/store', methods=['POST'])
@jwt_required()
def store(collection_name):
    if collection_name in ["users", "admins"] and not is_admin():
        return jsonify({"error": "Elevated Privileges Required"}), 403

    data = {}

    if request.content_type and 'multipart/form-data' in request.content_type:
        for key in request.form:
            data[key] = request.form.get(key)

        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join('uploads', filename)
                file.save(filepath)
                data['file_path'] = filepath

        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename:
                image_filename = secure_filename(image.filename)
                image_path = os.path.join('uploads', image_filename)
                image.save(image_path)
                data['image_path'] = image_path
    else:
        try:
            data = request.get_json(force=True)
        except:
            return jsonify({"error": "Invalid or missing data"}), 400

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
