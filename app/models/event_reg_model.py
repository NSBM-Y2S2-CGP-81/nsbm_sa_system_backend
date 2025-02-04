from app.config import db

class EventRegistration:
    collection = db['event_registrations']

    @staticmethod
    def create_event_registration(registration_data):
        return EventRegistration.collection.insert_one(registration_data)

    @staticmethod
    def find_registration_by_id(registration_id):
        return EventRegistration.collection.find_one({"_id": registration_id})

    @staticmethod
    def update_registration(registration_id, update_data):
        return EventRegistration.collection.update_one({"_id": registration_id}, {"$set": update_data})

    @staticmethod
    def delete_registration(registration_id):
        return EventRegistration.collection.delete_one({"_id": registration_id})