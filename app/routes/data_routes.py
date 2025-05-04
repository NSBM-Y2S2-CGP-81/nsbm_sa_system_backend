from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt
from app.services.data_service import (
    fetch_all_data, store_data, fetch_data_by_id, delete_event_request,
    approve_event_request, update_data, count_field_occurrences,
    execute_mongodb_query, create_collection
)
from app.services.loggerService import LoggerService

data_bp = Blueprint('data', __name__)
logger = LoggerService()

SENSITIVE_COLLECTIONS = {
    "users", "admins", "events"
}
RESTRICTED_COLLECTIONS = {
    "users", "admins", "event_requests", "events"
}

def is_admin():
    """Check if the current user is an admin."""
    claims = get_jwt()
    return claims.get("role") == "superuser"

def check_admin_access(collection_name, action="access"):
    """Common function to check admin access to sensitive collections."""
    if  action == "fetch" and collection_name == "events":
        # Allow non-admins to fetch events
        return None
    if collection_name in SENSITIVE_COLLECTIONS and not is_admin():
        logger.warning(f"Unauthorized {action} attempt to {collection_name} collection.")
        return jsonify({"error": "Elevated privileges required"}), 403
    return None

@data_bp.route('/<collection_name>/store', methods=['POST'])
@jwt_required()
def store(collection_name):
    access_check = check_admin_access(collection_name, "access")
    if access_check:
        return access_check

    data = request.json
    logger.info(f"Storing data in {collection_name} collection, DATA: {data}")
    return store_data(collection_name, data)

@data_bp.route('/<collection_name>/fetch', methods=['GET'])
@jwt_required()
def fetch_all(collection_name):
    access_check = check_admin_access(collection_name, "fetch")
    if access_check:
        return access_check

    logger.info(f"Fetching all data from {collection_name} collection.")
    return fetch_all_data(collection_name)

@data_bp.route('/<collection_name>/fetch/<record_id>', methods=['GET'])
@jwt_required()
def fetch_by_id(collection_name, record_id):
    access_check = check_admin_access(collection_name, "access")
    if access_check:
        return access_check

    logger.info(f"Fetching data by ID from {collection_name} collection, ID: {record_id}")
    return fetch_data_by_id(collection_name, record_id)

@data_bp.route('/<collection_name>/delete/<record_id>', methods=['DELETE'])
@jwt_required()
def delete_request(collection_name, record_id):
    # Check if user is admin and collection is sensitive
    if collection_name in RESTRICTED_COLLECTIONS and not is_admin():
        logger.warning(f"Unauthorized delete attempt in {collection_name} collection.")
        return jsonify({"error": "Elevated privileges required"}), 403

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

    # Check if user is admin
    if collection_name in RESTRICTED_COLLECTIONS and not is_admin():
        # Log the unauthorized access attempt
        logger.warning(f"Unauthorized access attempt to approve request in {collection_name} collection.")
        return jsonify({"error": "Elevated privileges required"}), 403

    logger.info(f"Approving event request with ID: {record_id}")
    return approve_event_request(collection_name, record_id)

@data_bp.route('/<collection_name>/update/<record_id>', methods=['PUT'])
@jwt_required()
def update_record(collection_name, record_id):
    # access_check = check_admin_access(collection_name, "update")
    # if access_check:
    #     return access_check

    data = request.json
    logger.info(f"Updating record in {collection_name} collection with ID: {record_id}, DATA: {data}")
    return update_data(collection_name, record_id, data)

@data_bp.route('/<collection_name>/count', methods=['GET'])
@jwt_required()
def count_occurrences(collection_name):
    access_check = check_admin_access(collection_name, "count occurrences in")
    if access_check:
        return access_check

    event_id = request.args.get('event_data_get')
    field_name = request.args.get('field')
    field_value = request.args.get('value')

    if not field_name or not field_value:
        logger.warning("Field name or value missing in count request.")
        return jsonify({"error": "Field name and value are required"}), 400

    logger.success(f"Counting occurrences of {field_name}='{field_value}' in {collection_name} collection. Event:{event_id}")
    return count_field_occurrences(collection_name, field_name, field_value, event_id)

@data_bp.route('/mongodb/query', methods=['POST'])
@jwt_required()
def mongodb_query():
    # Check if user is admin
    if not is_admin():
        logger.warning("Unauthorized attempt to access MongoDB query endpoint")
        return jsonify({"error": "Admin privileges required"}), 403

    data = request.json
    logger.info(f"MongoDB query requested with params: {data}")

    # Execute the query
    result, status_code = execute_mongodb_query(data)
    return jsonify(result), status_code

@data_bp.route('/create-collection', methods=['POST'])
@jwt_required()
def create_new_collection():
    # Only admin users should be able to create collections
    if not is_admin():
        logger.warning("Unauthorized attempt to create a collection")
        return jsonify({"error": "Admin privileges required"}), 403

    data = request.json
    collection_name = data.get('name')

    if not collection_name:
        logger.warning("Collection name is required but was not provided")
        return jsonify({"error": "Collection name is required"}), 400

    # Validate collection name (optional but recommended)
    if not collection_name.isalnum() and not "_" in collection_name:
        logger.warning(f"Invalid collection name format: {collection_name}")
        return jsonify({"error": "Collection name must contain only alphanumeric characters and underscores"}), 400

    logger.info(f"Creating new collection: {collection_name}")
    return create_collection(collection_name)

@data_bp.route('/<collection_name>/create', methods=['POST'])
@jwt_required()
def create_document(collection_name):
    """Create a new document in the specified collection."""
    access_check = check_admin_access(collection_name, "create document in")
    if access_check:
        return access_check

    data = request.json
    if not data:
        logger.warning(f"No data provided for document creation in {collection_name}")
        return jsonify({"error": "Document data is required"}), 400

    logger.info(f"Creating new document in {collection_name} collection, DATA: {data}")
    return store_data(collection_name, data)
