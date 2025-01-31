from flask import jsonify
from app import mongo

def store_data(data):
    mongo.db.data.insert_one(data)
    return jsonify({"message": "Data stored successfully"}), 201

def fetch_data():
    data = list(mongo.db.data.find({}, {"_id": 0}))
    return jsonify(data), 200
