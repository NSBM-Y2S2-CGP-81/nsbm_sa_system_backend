from app.config import db

class QueueManagement:
    collection = db['queue_management']

    @staticmethod
    def create_queue_entry(queue_data):
        return QueueManagement.collection.insert_one(queue_data)

    @staticmethod
    def find_queue_entry_by_id(queue_id):
        return QueueManagement.collection.find_one({"_id": queue_id})

    @staticmethod
    def update_queue_entry(queue_id, update_data):
        return QueueManagement.collection.update_one({"_id": queue_id}, {"$set": update_data})

    @staticmethod
    def delete_queue_entry(queue_id):
        return QueueManagement.collection.delete_one({"_id": queue_id})