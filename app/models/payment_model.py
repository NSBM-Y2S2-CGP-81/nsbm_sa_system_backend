from app.config import db

class Payment:
    collection = db['payments']

    @staticmethod
    def create_payment(payment_data):
        return Payment.collection.insert_one(payment_data)

    @staticmethod
    def find_payment_by_id(payment_id):
        return Payment.collection.find_one({"_id": payment_id})

    @staticmethod
    def update_payment(payment_id, update_data):
        return Payment.collection.update_one({"_id": payment_id}, {"$set": update_data})

    @staticmethod
    def delete_payment(payment_id):
        return Payment.collection.delete_one({"_id": payment_id})