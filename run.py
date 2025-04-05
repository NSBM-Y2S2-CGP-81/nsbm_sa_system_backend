from app import create_app
from app.config import db
from pymongo.errors import OperationFailure

def initialize_database():
    # Create collections if they don't exist
    collections = ['users', 'students', 'lecturers', 'staff', 'vendors', 'events', 'event_registrations', 'timetable', 'food_orders', 'food_order_items', 'queue_management', 'campus_facilities', 'payments', 'todays_pick', 'news', 'crowd_uplink']

    for collection_name in collections:
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            print(f"Collection '{collection_name}' created.")
        else:
            print(f"Collection '{collection_name}' already exists.")
    admin_db = db.client["admin"]
    try:
        admin_db.command("createUser", "admin",
                         pwd="admin1234",
                         roles=[
                             {"role": "userAdminAnyDatabase", "db": "admin"},
                             {"role": "readWriteAnyDatabase", "db": "admin"}
                         ])
        print("✅ Admin user created successfully.")
    except OperationFailure as e:
        if "already exists" in str(e):
            print("⚠️ Admin user already exists.")
        else:
            print("❌ Failed to create admin user:", e)

app = create_app()

if __name__ == "__main__":
    app.config["MONGO_URI"] = "mongodb://0.0.0.0:27017/nsbm_sa"
    initialize_database()
    app.run(host="0.0.0.0", port=5000, debug=True)
