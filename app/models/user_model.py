from app.config import db

class User:
    collection = db['users']

    @staticmethod
    def create_user(user_data):
        return User.collection.insert_one(user_data)

    @staticmethod
    def find_user_by_email(email):
        return User.collection.find_one({"email": email})

    @staticmethod
    def update_user(user_id, update_data):
        return User.collection.update_one({"_id": user_id}, {"$set": update_data})

    @staticmethod
    def delete_user(user_id):
        return User.collection.delete_one({"_id": user_id})