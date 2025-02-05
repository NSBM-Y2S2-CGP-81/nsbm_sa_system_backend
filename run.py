from app import create_app
from app.config import db


def initialize_database():
    # Create collections if they don't exist
    collections = ['users', 'students', 'lecturers', 'staff', 'vendors', 'events', 'event_registrations', 'timetable', 'food_orders', 'food_order_items', 'queue_management', 'campus_facilities', 'payments']
    
    for collection_name in collections:
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            print(f"Collection '{collection_name}' created.")
        else:
            print(f"Collection '{collection_name}' already exists.")

app = create_app()

if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000, debug=True)