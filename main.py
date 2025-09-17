import os
from flask import Flask
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate  # Import Migrate
from database import db, get_database_url
from models.User.model import User
from models.User.route import user_bp
from models.Donor.route import donor_bp
from models.BloodRequest.route import blood_request_bp
from models.BloodDonation.route import blood_donation_bp
from auth import auth_bp

def create_app(config_overrides=None):
    app = Flask(__name__)

    # Load default configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = get_database_url()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "super-secret")

    if config_overrides:
        app.config.update(config_overrides)

    jwt = JWTManager(app)
    db.init_app(app)
    migrate = Migrate(app, db)  # Initialize Migrate

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return db.session.get(User, int(identity))

    swagger = Swagger(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(donor_bp)
    app.register_blueprint(blood_request_bp)
    app.register_blueprint(blood_donation_bp)

    @app.route("/")
    def index():
        return "Welcome to the Blood Donation API!"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
