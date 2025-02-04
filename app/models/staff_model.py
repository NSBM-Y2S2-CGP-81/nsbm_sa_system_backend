from app.config import db

class Staff:
    collection = db['staff']

    @staticmethod
    def create_staff(staff_data):
        return Staff.collection.insert_one(staff_data)

    @staticmethod
    def find_staff_by_id(staff_id):
        return Staff.collection.find_one({"_id": staff_id})

    @staticmethod
    def update_staff(staff_id, update_data):
        return Staff.collection.update_one({"_id": staff_id}, {"$set": update_data})

    @staticmethod
    def delete_staff(staff_id):
        return Staff.collection.delete_one({"_id": staff_id})