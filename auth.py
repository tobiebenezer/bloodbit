import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.User.model import User
from flasgger import swag_from

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["POST"])
@swag_from({
    'tags': ['Auth'],
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'id': 'UserLogin',
                'required': ['email', 'password'],
                'properties': {
                    'email': {'type': 'string', 'format': 'email', 'example': 'john.doe@example.com'},
                    'password': {'type': 'string', 'format': 'password', 'example': 'a_strong_password'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login successful',
            'schema': {
                'properties': {
                    'access_token': {'type': 'string'},
                    'user': {
                        '$ref': '#/definitions/User'
                    }
                }
            }
        },
        401: {
            'description': 'Bad email or password'
        }
    }
})
def login():
    data = request.get_json()
    email = data.get("email", None)
    password = data.get("password", None)

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token, user=user.to_dict()), 200
    
    return jsonify({"msg": "Bad email or password"}), 401
