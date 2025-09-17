from flask import Blueprint, request, jsonify
from database import db
from models.User.model import User
from flasgger import swag_from
from flask_jwt_extended import jwt_required

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/', methods=['POST'])
@swag_from({
    'tags': ['User'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'UserRegistration',
                'required': [
                    'name',
                    'email',
                    'password',
                    'blood_type'
                ],
                'properties': {
                    'name': {'type': 'string', 'example': 'John Doe'},
                    'email': {'type': 'string', 'format': 'email', 'example': 'john.doe@example.com'},
                    'password': {'type': 'string', 'format': 'password', 'example': 'a_strong_password'},
                    'blood_type': {'type': 'string', 'example': 'O+'},
                    'location': {'type': 'string', 'example': 'New York'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'User registered successfully'
        },
        400: {
            'description': 'Invalid input'
        },
        500: {
            'description': 'Failed to register user'
        }
    }
})
def create_user():
    """Register a new user"""
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid input"}), 400

    new_user = User(
        name=data['name'],
        email=data['email'],
        blood_type=data['blood_type'],
        location=data.get('location')
    )
    new_user.set_password(data['password'])

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to register user: {e}'}), 500

    return jsonify({'message': 'User registered successfully'}), 201

@user_bp.route('/', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['User'],
    'responses': {
        200: {
            'description': 'A list of users',
            'schema': {
                'type': 'array',
                'items': {
                    '$ref': '#/definitions/User'
                }
            }
        }
    }
})
def get_users():
    """Get all users"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['User'],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the user to retrieve'
        },
        {
            "name": "Authorization",
            "in": "header",
            "type": "string",
            "required": True,
            "description": "Bearer token for authentication"
        }
    ],
    'responses': {
        200: {
            'description': 'A user object',
            'schema': {
                '$ref': '#/definitions/User'
            }
        },
        404: {
            'description': 'User not found'
        }
    }
})
def get_user(user_id):
    """Get a user by ID"""
    user = db.session.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({'message': 'User not found'}), 404
