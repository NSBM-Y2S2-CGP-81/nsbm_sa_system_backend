from app.config import db

class FoodOrder:
    collection = db['food_orders']

    @staticmethod
    def create_food_order(order_data):
        return FoodOrder.collection.insert_one(order_data)

    @staticmethod
    def find_food_order_by_id(order_id):
        return FoodOrder.collection.find_one({"_id": order_id})

    @staticmethod
    def update_food_order(order_id, update_data):
        return FoodOrder.collection.update_one({"_id": order_id}, {"$set": update_data})

    @staticmethod
    def delete_food_order(order_id):
        return FoodOrder.collection.delete_one({"_id": order_id})