import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.User.model import User # Assuming User model is in models/User/model.py
from flasgger import swag_from
from database import db

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
                'type': 'object',
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
                'type': 'object',
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

@auth_bp.route("/register", methods=["POST"])
@swag_from({
    'tags': ['Auth'],
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['email', 'password', 'name', 'blood_type', 'location'],
                'properties': {
                    'email': {'type': 'string', 'format': 'email', 'example': 'jane.doe@example.com'},
                    'password': {'type': 'string', 'format': 'password', 'example': 'another_strong_password'},
                    'name': {'type': 'string', 'example': 'Jane Doe'},
                    'blood_type': {'type': 'string', 'example': 'A+'},
                    'gender': {'type': 'string', 'example': 'female'},
                    'location': {'type': 'string', 'example': 'City, Country'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'User registered successfully',
            'schema': {
                '$ref': '#/definitions/User'
            }
        },
        400: {
            'description': 'Invalid input'
        },
        409: {
            'description': 'Email already registered'
        }
    }
})
def register():
    data = request.get_json()
    # Basic validation - you might want more robust validation
    if not all(key in data for key in ('email', 'password', 'name', 'blood_type', 'location')):
        return jsonify({"msg": "Missing required fields"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Email already registered"}), 409

    new_user = User(
        email=data['email'],
        name=data['name'],
        blood_type=data['blood_type'],
        gender = data['gender'],
        location=data['location']
    )
    new_user.set_password(data['password']) # Assuming you have a set_password method

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201 # Assuming you have a to_dict method

@auth_bp.route("/logout", methods=["POST"])
@jwt_required() # Requires a valid JWT token
@swag_from({
    'tags': ['Auth'],
    'security': [{'jwt': []}],
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token for authentication (e.g., "Bearer <token>")'
        },
    ],
    'responses': {
        200: {
            'description': 'Successfully logged out'
        },
        401: {
            'description': 'Missing or invalid token'
        }
    }
})
def logout():
    # JWT is handled by the @jwt_required() decorator.
    # On the client side, you would simply discard the token.
    # If you have a token blocklist, you would add the token here.
    jti = get_jwt_identity() # Get the identity from the token if needed
    print(f"User {jti} logged out") # Log the logout event

    return jsonify({"msg": "Successfully logged out"}), 200
