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

        if collection_name == "event_registrations":
            collection = get_collection(collection_name)
            existing_registration = collection.find_one({"user_email": data.get("user_email"), "event_id": data.get("event_id")})
            if existing_registration:
                return {"message": "User already signed up for this event"}, 409

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

def delete_event_request(collection_name, record_id):
    try:
        collection = get_collection(collection_name)
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

def approve_event_request(collection_name, record_id):
    try:
        # Get the event request
        event_requests_collection = get_collection(collection_name)
        event_request = event_requests_collection.find_one({"_id": ObjectId(record_id)})

        if not event_request:
            logger.warning(f"Event request with ID {record_id} not found")
            return {"error": "Event request not found"}, 404

        event_requests_collection.delete_one({"_id": ObjectId(record_id)})
        logger.success(f"Event request with ID {record_id} approved and moved to events")
        return {"message": "Event request approved successfully", "event_id": record_id}, 200

    except Exception as e:
        logger.error(f"Error approving event request: {e}")
        return {"error": str(e)}, 500

def update_data(collection_name, record_id, updated_data):
    try:
        collection = get_collection(collection_name)
        result = collection.update_one(
            {"_id": ObjectId(record_id)},
            {"$set": updated_data}
        )

        if result.matched_count == 0:
            logger.warning(f"Update failed. Record with ID {record_id} not found in {collection_name}")
            return {"error": "Record not found"}, 404

        logger.success(f"Record with ID {record_id} updated successfully in {collection_name}")
        return {"message": "Record updated successfully"}, 200

    except Exception as e:
        logger.error(f"Error updating data in {collection_name}: {e}")
        return {"error": str(e)}, 500


def count_field_occurrences(collection_name, field_name, field_value, event_id):
    try:
        collection = get_collection(collection_name)
        count = collection.count_documents({
            field_name: field_value,
            "event_id": event_id
        })
        logger.info(f"Counted {count} occurrences of {field_name}='{field_value}' with event_id='{event_id}' in {collection_name} collection.")
        return {"count": count}, 200
    except Exception as e:
        logger.error(f"Error counting occurrences in {collection_name}: {e}")
        return {"error": str(e)}, 500
