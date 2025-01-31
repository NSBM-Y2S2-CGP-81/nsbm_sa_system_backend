from flask import jsonify
from app import mongo, bcrypt
from flask_jwt_extended import create_access_token

def register_user(data):
    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "Missing fields"}), 400

    existing_user = mongo.db.users.find_one({"username": data["username"]})
    if existing_user:
        return jsonify({"error": "User already exists"}), 409

    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
    mongo.db.users.insert_one({"username": data["username"], "password": hashed_pw})

    return jsonify({"message": "User registered successfully"}), 201

def login_user(data):
    user = mongo.db.users.find_one({"username": data["username"]})
    if not user or not bcrypt.check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user["username"])
    return jsonify({"access_token": access_token}), 200
