from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS  # Import CORS
from dotenv import load_dotenv
from app.services.system_status_service import start_monitoring
import os

# Load environment variables
load_dotenv()

# Initialize Flask extensions
mongo = PyMongo()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    print("NSBM-SA-BACKEND STARTED!")
    print("Starting system status monitoring in the background...")
    start_monitoring()
    print("Monitoring started!")

    # Initialize extensions
    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Enable CORS for all routes
    CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.data_routes import data_bp
    from app.routes.custom_routes import custom_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(data_bp, url_prefix='/data')
    app.register_blueprint(custom_bp, url_prefix='/custom')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)  # Run on all available interfaces
