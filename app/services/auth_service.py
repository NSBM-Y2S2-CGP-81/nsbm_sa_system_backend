from flask import jsonify
from app import mongo, bcrypt
from flask_jwt_extended import create_access_token

def register_user(data):
    required_fields = [
    "full_name", "email", "password", "phone_number",
    "user_type", "profile_picture", "created_at", "updated_at"
    ]
    if not all(data.get(field) for field in required_fields):
        return {"error": "Missing required fields"}

    existing_user = mongo.db.users.find_one({"email": data["email"]})
    if existing_user:
        print("User already exists")
        return jsonify({"error": "User already exists"}), 409

    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
    mongo.db.users.insert_one({
        "full_name": data["full_name"],
        "email": data["email"],
        "password": hashed_pw,
        "phone_number": data["phone_number"],
        "user_type": data["user_type"],
        "profile_picture": data["profile_picture"],
        "created_at": data["created_at"],
        "updated_at": data["updated_at"]
    })
    access_token = create_access_token(identity=data["email"])
    return jsonify({"message": "User registered successfully", "access_token": access_token}), 201

def login_user(data):
    user = mongo.db.users.find_one({"email": data["email"]})
    if not user or not bcrypt.check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user["email"])
    return jsonify({"access_token": access_token}), 200
