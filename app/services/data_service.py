from app.config import db
from bson import ObjectId
from flask import jsonify
from flask import request


def get_collection(collection_name):
    """Get a MongoDB collection by its name."""
    return db[collection_name]

def is_local_request():
    return request.remote_addr in ("127.0.0.1", "::1")

def fetch_all_data(collection_name):
    if collection_name in ["admin", "users"] and not is_local_request():
        return {"error": "Unauthorized: Only localhost can update this collection"}, 403
    try:
        if collection_name == "users" or collection_name == "admin":
            return {"error": "Access denied"}, 403
        collection = get_collection(collection_name)
        records = list(collection.find())
        for record in records:
            record['_id'] = str(record['_id'])
        return jsonify(records), 200
    except Exception as e:
        return {"error": str(e)}, 500

def store_data(collection_name, data):
    if collection_name in ["admin", "users"] and not is_local_request():
        return {"error": "Unauthorized: Only localhost can update this collection"}, 403
    try:
        collection = get_collection(collection_name)
        result = collection.insert_one(data)
        return {"message": "Data stored successfully", "id": str(result.inserted_id)}, 201
    except Exception as e:
        return {"error": str(e)}, 400

def fetch_data_by_id(collection_name, record_id):
    if collection_name in ["admin", "users"] and not is_local_request():
        return {"error": "Unauthorized: Only localhost can update this collection"}, 403
    try:
        collection = get_collection(collection_name)
        record = collection.find_one({"_id": ObjectId(record_id)})
        if record:
            record['_id'] = str(record['_id'])
            return jsonify(record), 200
        return {"error": "Record not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500
