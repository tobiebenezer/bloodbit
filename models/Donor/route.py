from flask import Blueprint, jsonify, request
from models.Donor.model import Donor
from models.User.model import User
from database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

donor_bp = Blueprint('donor_bp', __name__, url_prefix='/donors')

@donor_bp.route('/', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Donor'],
    'parameters': [
        {
            'name': 'blood_group',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filter by blood group (e.g., A+, O-)'
        },
        {
            'name': 'location',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filter by location (case-insensitive)'
        },
        {
            'name': 'name',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filter by donor name (case-insensitive)'
        }
    ],
    'responses': {
        200: {
            'description': 'A list of donors, optionally filtered',
            'schema': {
                'type': 'array',
                'items': {
                    '$ref': '#/definitions/Donor'
                }
            }
        }
    }
})
def get_donors():
    query = Donor.query.join(User)

    blood_group = request.args.get('blood_group')
    location = request.args.get('location')
    name = request.args.get('name')

    if blood_group:
        query = query.filter(User.blood_type == blood_group)

    if location:
        query = query.filter(User.location.ilike(f'%{location}%'))

    if name:
        query = query.filter(User.name.ilike(f'%{name}%'))

    donors = query.all()
    return jsonify([donor.to_dict() for donor in donors]), 200

@donor_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Donor'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {
            'description': 'A single donor',
            'schema': {
                '$ref': '#/definitions/Donor'
            }
        },
        404: {
            'description': 'Donor not found'
        }
    }
})
def get_donor(id):
    donor = db.session.get(Donor, id)
    if donor:
        return jsonify(donor.to_dict()), 200
    return jsonify({'message': 'Donor not found'}), 404

@donor_bp.route('/', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Donor'],
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['medical_history'],
                'properties': {
                    'medical_history': {'type': 'string'},
                    'is_available': {'type': 'boolean'},
                    'last_donation': {'type': 'string', 'format': 'date'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Donor profile created successfully',
            'schema': {
                '$ref': '#/definitions/Donor'
            }
        }
    }
})
def create_donor():
    data = request.get_json()
    new_donor = Donor(
        user_id=int(get_jwt_identity()),
        medical_history=data.get('medical_history'),
        is_available=data.get('is_available', True),
        last_donation=data.get('last_donation')
    )
    db.session.add(new_donor)
    db.session.commit()
    return jsonify(new_donor.to_dict()), 201

@donor_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['Donor'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True
        },
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'medical_history': {'type': 'string'},
                    'is_available': {'type': 'boolean'},
                    'last_donation': {'type': 'string', 'format': 'date'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Donor profile updated successfully',
            'schema': {
                '$ref': '#/definitions/Donor'
            }
        },
        401: {
            'description': 'Unauthorized'
        },
        404: {
            'description': 'Donor not found'
        }
    }
})
def update_donor(id):
    donor = db.session.get(Donor, id)
    if not donor:
        return jsonify({'message': 'Donor not found'}), 404
    
    # Ensure the user is updating their own donor profile
    if donor.user_id != int(get_jwt_identity()):
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    donor.medical_history = data.get('medical_history', donor.medical_history)
    donor.is_available = data.get('is_available', donor.is_available)
    donor.last_donation = data.get('last_donation', donor.last_donation)
    db.session.commit()
    return jsonify(donor.to_dict()), 200
