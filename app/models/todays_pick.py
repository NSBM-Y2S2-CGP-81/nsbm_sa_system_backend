from app.config import db

class TodaysPick:
    collection = db['todays_pick']

    @staticmethod
    def create_pick(pick_data):
        return TodaysPick.collection.insert_one(pick_data)

    @staticmethod
    def find_pick_by_id(pick_id):
        return TodaysPick.collection.find_one({"_id": pick_id})

    @staticmethod
    def update_pick(pick_id, update_data):
        return TodaysPick.collection.update_one({"_id": pick_id}, {"$set": update_data})

    @staticmethod
    def delete_pick(pick_id):
        return TodaysPick.collection.delete_one({"_id": pick_id})
