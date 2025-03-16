from app.config import db
from bson import ObjectId
from flask import jsonify

def get_collection(collection_name):
    """Get a MongoDB collection by its name."""
    return db[collection_name]

def fetch_all_data(collection_name):
    try:
        if collection_name == "users" or collection_name == "admin":
            return {"error": "Access denied"}, 403
        collection = get_collection(collection_name)
        records = list(collection.find())
        for record in records:
            record['_id'] = str(record['_id'])  # Convert ObjectId to string
        return jsonify(records), 200
    except Exception as e:
        return {"error": str(e)}, 500

def store_data(collection_name, data):
    try:
        collection = get_collection(collection_name)
        result = collection.insert_one(data)
        return {"message": "Data stored successfully", "id": str(result.inserted_id)}, 201
    except Exception as e:
        return {"error": str(e)}, 400

def fetch_data_by_id(collection_name, record_id):
    try:
        collection = get_collection(collection_name)
        record = collection.find_one({"_id": ObjectId(record_id)})
        if record:
            record['_id'] = str(record['_id'])
            return jsonify(record), 200
        return {"error": "Record not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500
