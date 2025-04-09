from app.config import db
from bson import ObjectId
from flask import jsonify, request
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_collection(collection_name):
    """Get a MongoDB collection by its name."""
    return db[collection_name]


def fetch_all_data(collection_name):
    try:
        collection = get_collection(collection_name)
        records = list(collection.find())
        for record in records:
            record['_id'] = str(record['_id'])
        return jsonify(records), 200
    except Exception as e:
        return {"error": str(e)}, 500


def store_data(collection_name, data=None):
    try:
        collection = get_collection(collection_name)

        if request.content_type.startswith("multipart/form-data"):
            form = request.form

            event_data = {
                "eventName": form.get("eventName"),
                "description": form.get("description"),
                "selectedDate": form.get("selectedDate"),
                "location": form.get("location"),
            }

            if 'file' in request.files:
                uploaded_file = request.files['file']
                if uploaded_file.filename != '':
                    filename = secure_filename(uploaded_file.filename)
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    uploaded_file.save(file_path)
                    event_data['file'] = file_path

            if 'image' in request.files:
                uploaded_image = request.files['image']
                if uploaded_image.filename != '':
                    image_filename = secure_filename(uploaded_image.filename)
                    image_path = os.path.join(UPLOAD_FOLDER, image_filename)
                    uploaded_image.save(image_path)
                    event_data['image'] = image_path

            result = collection.insert_one(event_data)
            return {
                "message": "Event created successfully",
                "id": str(result.inserted_id)
            }, 200

        else:
            if data is None:
                data = request.json
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
