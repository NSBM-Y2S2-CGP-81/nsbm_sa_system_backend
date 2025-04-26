from app.config import db
from bson import ObjectId, json_util
from flask import jsonify
from flask import request
from datetime import datetime
import json
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

            if "location" in data and "selectedTime" in data:
                event_requests_collection = get_collection("event_requests")
                existing_event = event_requests_collection.find_one({
                    "location": data["location"],
                    "selectedDate": data["selectedDate"],
                    "selectedTime": data["selectedTime"]
                })

                event_requests_collection = get_collection("events")
                existing_event = event_requests_collection.find_one({
                    "location": data["event_venue"],
                    "selectedDate": data["event_date"],
                    "selectedTime": data["event_time"]
                })

                if existing_event:
                    return {"message": "Location is already taken on the selected date!"}, 409

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

def execute_mongodb_query(data):
    """
    Execute a MongoDB query with pagination, sorting, and filtering
    Only to be used by administrative users
    """
    try:
        collection_name = data.get('collection')
        query = data.get('query', {})
        sort_config = data.get('sort', {'_id': 1})
        page = int(data.get('page', 1))
        limit = int(data.get('limit', 10))

        # Calculate skip amount for pagination
        skip = (page - 1) * limit

        if not collection_name:
            return {"error": "Collection name is required"}, 400

        # Get the collection
        collection = db[collection_name]

        # Get the first key-value pair from sort_config and use it for sorting
        # This handles the conversion from dict to MongoDB sort format
        sort_field, sort_direction = next(iter(sort_config.items()))

        # Execute the query with pagination and sorting
        results = list(collection.find(query).sort(sort_field, sort_direction).skip(skip).limit(limit))

        # Get total count for pagination info
        total_count = collection.count_documents(query)

        # Convert ObjectId to string for JSON serialization
        for result in results:
            if '_id' in result:
                result['_id'] = str(result['_id'])

        # Parse results to ensure JSON serialization works
        parsed_results = json.loads(json_util.dumps(results))

        logger.info(f"Admin executed MongoDB query on {collection_name}: {query}")

        return {
            "data": parsed_results,
            "pagination": {
                "total": total_count,
                "page": page,
                "limit": limit,
                "pages": (total_count + limit - 1) // limit  # Ceiling division for total pages
            }
        }, 200

    except Exception as e:
        logger.error(f"Error executing MongoDB query: {str(e)}")
        return {"error": str(e)}, 500

def create_collection(collection_name):
    """Create a new collection in MongoDB database."""
    try:
        # Check if the collection already exists
        if collection_name in db.list_collection_names():
            logger.warning(f"Collection '{collection_name}' already exists")
            return {"error": f"Collection '{collection_name}' already exists"}, 400

        # Create a new collection by simply inserting and removing a dummy document
        # This is the common way to explicitly create a MongoDB collection
        db.create_collection(collection_name)

        logger.success(f"Collection '{collection_name}' created successfully")
        return {"message": f"Collection '{collection_name}' created successfully"}, 201
    except Exception as e:
        logger.error(f"Error creating collection: {e}")
        return {"error": str(e)}, 500
