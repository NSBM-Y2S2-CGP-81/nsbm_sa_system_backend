from app.config import db

class News:
    collection = db['news']

    @staticmethod
    def create_news(news_data):
        return News.collection.insert_one(news_data)

    @staticmethod
    def find_news_by_id(news_id):
        return News.collection.find_one({"_id": news_id})

    @staticmethod
    def update_news(news_id, update_data):
        return News.collection.update_one({"_id": news_id}, {"$set": news_data})

    @staticmethod
    def delete_news(news_id):
        return News.collection.delete_one({"_id": news_id})