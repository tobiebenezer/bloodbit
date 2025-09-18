from flask import Flask
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from database import db
from auth import auth_bp
from models.User.route import user_bp
from models.Donor.route import donor_bp
from models.BloodRequest.route import blood_request_bp
from models.User.model import User

def create_app(config_overrides=None):
    app = Flask(__name__)
    app.config.from_object('config.Config')

    if config_overrides:
        app.config.update(config_overrides)

    jwt = JWTManager(app)
    db.init_app(app)
    migrate = Migrate(app, db)  # Initialize Migrate

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return db.session.get(User, int(identity))

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
        "definitions": {
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "blood_type": {"type": "string", "example": "O+"},
                    "location": {"type": "string"},
                    "gender": {"type": "string"}
                }
            },
            "BloodRequest": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "requester_id": {"type": "integer"},
                    "donor_id": {"type": "integer"},
                    "blood_type": {"type": "string"},
                    "quantity": {"type": "integer"},
                    "status": {"type": "string", "enum": ["pending", "fulfilled", "cancelled"]},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"}
                }
            }
        }
    }
    swagger = Swagger(app, config=swagger_config)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(donor_bp, url_prefix='/donors')
    app.register_blueprint(blood_request_bp, url_prefix='/blood-requests')

    @app.route("/")
    def index():
        return "Welcome to Bloodit!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
