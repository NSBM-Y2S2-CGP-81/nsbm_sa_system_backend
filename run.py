from app import create_app
from app.config import db
from pymongo.errors import OperationFailure
from app.services.loggerService import LoggerService

logger = LoggerService()

def initialize_database():
    collections = [
        'users', 'students', 'lecturers', 'staff', 'vendors',
        'events', 'event_registrations', 'timetable', 'food_orders',
        'food_order_items', 'queue_management', 'campus_facilities',
        'payments', 'todays_pick', 'news', 'crowd_uplink', 'mic_users'
    ]

    for collection_name in collections:
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            logger.info(f"Collection '{collection_name}' created.")
        else:
            logger.info(f"Collection '{collection_name}' already exists.")

app = create_app()

if __name__ == "__main__":
    app.config["MONGO_URI"] = "mongodb://0.0.0.0:27017/nsbm_sa"
    initialize_database()
    app.run(host="0.0.0.0", port=5000, debug=True)
