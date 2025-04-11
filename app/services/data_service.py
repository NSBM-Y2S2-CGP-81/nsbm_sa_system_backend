from app.config import db
from bson import ObjectId
from flask import jsonify
from flask import request
from datetime import datetime
from app.services.loggerService import LoggerService

logger = LoggerService()


def get_collection(collection_name):
    """Get a MongoDB collection by its name."""
    # verifyTable(collection_name)
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

def store_data(collection_name, data):
    try:
        if collection_name == "event_requests" and "selectedDate" in data:
            selected_date = datetime.strptime(data["selectedDate"], "%Y-%m-%d").date()
            today = datetime.now().date()
            if selected_date <= today:
                return {"message": "Invalid Date"}, 401

        collection = get_collection(collection_name)
        result = collection.insert_one(data)
        return {"message": "Data stored successfully", "id": str(result.inserted_id)}, 201
    except Exception as e:
        logger.error(f"Error storing data in {collection_name}: {e}")
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

def delete_event_request(record_id):
    try:
        collection = get_collection('event_requests')
        result = collection.delete_one({"_id": ObjectId(record_id)})

        if result.deleted_count:
            logger.success(f"Event request with ID {record_id} deleted successfully")
            return {"message": "Event request deleted successfully"}, 200
        else:
            logger.warning(f"Event request with ID {record_id} not found")
            return {"error": "Event request not found"}, 404
    except Exception as e:
        logger.error(f"Error deleting event request: {e}")
        return {"error": str(e)}, 500

def approve_event_request(record_id):
    try:
        # Get the event request
        event_requests_collection = get_collection('event_requests')
        event_request = event_requests_collection.find_one({"_id": ObjectId(record_id)})

        if not event_request:
            logger.warning(f"Event request with ID {record_id} not found")
            return {"error": "Event request not found"}, 404

        # Convert ObjectId to string for the event record
        event_request['_id'] = str(event_request['_id'])

        # Store the event request in the events collection
        events_collection = get_collection('events')
        result = events_collection.insert_one(event_request)

        if result.inserted_id:
            # Delete the event request after successfully adding it to events
            event_requests_collection.delete_one({"_id": ObjectId(record_id)})
            logger.success(f"Event request with ID {record_id} approved and moved to events")
            return {"message": "Event request approved successfully", "event_id": str(result.inserted_id)}, 200
        else:
            logger.error(f"Failed to insert event into events collection")
            return {"error": "Failed to approve event request"}, 500
    except Exception as e:
        logger.error(f"Error approving event request: {e}")
        return {"error": str(e)}, 500
