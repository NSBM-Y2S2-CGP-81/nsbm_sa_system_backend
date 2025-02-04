from app.config import db

class Vendor:
    collection = db['vendors']

    @staticmethod
    def create_vendor(vendor_data):
        return Vendor.collection.insert_one(vendor_data)

    @staticmethod
    def find_vendor_by_id(vendor_id):
        return Vendor.collection.find_one({"_id": vendor_id})

    @staticmethod
    def update_vendor(vendor_id, update_data):
        return Vendor.collection.update_one({"_id": vendor_id}, {"$set": update_data})

    @staticmethod
    def delete_vendor(vendor_id):
        return Vendor.collection.delete_one({"_id": vendor_id})