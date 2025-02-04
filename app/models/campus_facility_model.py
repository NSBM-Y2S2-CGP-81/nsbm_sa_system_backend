from app.config import db

class CampusFacility:
    collection = db['campus_facilities']

    @staticmethod
    def create_facility(facility_data):
        return CampusFacility.collection.insert_one(facility_data)

    @staticmethod
    def find_facility_by_id(facility_id):
        return CampusFacility.collection.find_one({"_id": facility_id})

    @staticmethod
    def update_facility(facility_id, update_data):
        return CampusFacility.collection.update_one({"_id": facility_id}, {"$set": update_data})

    @staticmethod
    def delete_facility(facility_id):
        return CampusFacility.collection.delete_one({"_id": facility_id})