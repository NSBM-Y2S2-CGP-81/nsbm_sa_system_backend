from app.config import db

class Lecturer:
    collection = db['lecturers']

    @staticmethod
    def create_lecturer(lecturer_data):
        return Lecturer.collection.insert_one(lecturer_data)

    @staticmethod
    def find_lecturer_by_id(lecturer_id):
        return Lecturer.collection.find_one({"_id": lecturer_id})

    @staticmethod
    def update_lecturer(lecturer_id, update_data):
        return Lecturer.collection.update_one({"_id": lecturer_id}, {"$set": update_data})

    @staticmethod
    def delete_lecturer(lecturer_id):
        return Lecturer.collection.delete_one({"_id": lecturer_id})