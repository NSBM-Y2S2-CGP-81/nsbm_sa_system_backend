from app.config import db

class Timetable:
    collection = db['timetable']

    @staticmethod
    def create_timetable_entry(timetable_data):
        return Timetable.collection.insert_one(timetable_data)

    @staticmethod
    def find_timetable_entry_by_id(timetable_id):
        return Timetable.collection.find_one({"_id": timetable_id})

    @staticmethod
    def update_timetable_entry(timetable_id, update_data):
        return Timetable.collection.update_one({"_id": timetable_id}, {"$set": update_data})

    @staticmethod
    def delete_timetable_entry(timetable_id):
        return Timetable.collection.delete_one({"_id": timetable_id})