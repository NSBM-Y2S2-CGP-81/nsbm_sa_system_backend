from app.config import db

class Student:
    collection = db['students']

    @staticmethod
    def create_student(student_data):
        return Student.collection.insert_one(student_data)

    @staticmethod
    def find_student_by_id(student_id):
        return Student.collection.find_one({"_id": student_id})

    @staticmethod
    def update_student(student_id, update_data):
        return Student.collection.update_one({"_id": student_id}, {"$set": update_data})

    @staticmethod
    def delete_student(student_id):
        return Student.collection.delete_one({"_id": student_id})