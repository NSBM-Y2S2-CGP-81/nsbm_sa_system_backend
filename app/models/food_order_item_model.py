from app.config import db

class FoodOrderItem:
    collection = db['food_order_items']

    @staticmethod
    def create_food_order_item(item_data):
        return FoodOrderItem.collection.insert_one(item_data)

    @staticmethod
    def find_food_order_item_by_id(item_id):
        return FoodOrderItem.collection.find_one({"_id": item_id})

    @staticmethod
    def update_food_order_item(item_id, update_data):
        return FoodOrderItem.collection.update_one({"_id": item_id}, {"$set": update_data})

    @staticmethod
    def delete_food_order_item(item_id):
        return FoodOrderItem.collection.delete_one({"_id": item_id})