from app.config import db

class Event:
    collection = db['events']

    @staticmethod
    def create_event(event_data):
        return Event.collection.insert_one(event_data)

    @staticmethod
    def find_event_by_id(event_id):
        return Event.collection.find_one({"_id": event_id})

    @staticmethod
    def update_event(event_id, update_data):
        return Event.collection.update_one({"_id": event_id}, {"$set": update_data})

    @staticmethod
    def delete_event(event_id):
        return Event.collection.delete_one({"_id": event_id})