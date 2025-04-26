import threading
import time
from datetime import datetime
from bson.errors import InvalidId
from app.config import db
from app.services.loggerService import LoggerService

logger = LoggerService()

def get_events_collection():
    """Get the MongoDB events collection."""
    return db["events"]

def is_valid_event(event):
    """
    Check if an event is valid.
    An event is considered valid if it has all required fields with appropriate values.
    """
    if not event:
        return False

    required_fields = ["event_name", "event_description", "selectedDate"]

    # Check if all required fields exist and are not None/empty
    for field in required_fields:
        if field not in event or event[field] is None or event[field] == "":
            logger.warning(f"Event {event.get('_id', 'unknown')} missing or has empty {field}")
            return False

    # Additional validation can be added here if needed

    return True

def cleanup_events():
    """
    Clean up events collection by removing:
    1. Invalid or null events
    """
    try:
        collection = get_events_collection()

        # Find all events to check validity
        all_events = list(collection.find())
        invalid_count = 0

        for event in all_events:
            if not is_valid_event(event):
                collection.delete_one({"_id": event["_id"]})
                invalid_count += 1

        if invalid_count > 0:
            logger.warning(f"Deleted {invalid_count} invalid events")

    except Exception as e:
        logger.error(f"Error cleaning up events: {e}")

def start_events_cleanup():
    """Run the events cleanup task every second."""
    while True:
        try:
            cleanup_events()
        except Exception as e:
            logger.error(f"Error in events cleanup thread: {e}")
        time.sleep(1)  # Wait for 1 second before next cleanup

def initialize_events_cleanup():
    """Start the events cleanup service in a separate thread."""
    logger.info("Starting events cleanup service...")
    cleanup_thread = threading.Thread(target=start_events_cleanup, daemon=True)
    cleanup_thread.start()
    logger.success("Events cleanup service started successfully")
