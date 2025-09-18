from flask import Blueprint, request, jsonify
from database import db
from models.BloodDonation.model import BloodDonation
from models.Donor.model import Donor
from flasgger import swag_from
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity

blood_donation_bp = Blueprint('blood_donation', __name__, url_prefix='/blood-donations')

@blood_donation_bp.route('/', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Blood Donation'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'required': True,
            'type': 'string',
            'description': 'Bearer token for authentication'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'BloodDonation',
                'required': ['blood_group', 'donation_date', 'quantity'],
                'properties': {
                    'blood_group': {'type': 'string'},
                    'donation_date': {'type': 'string', 'format': 'date'},
                    'quantity': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Blood donation created successfully'},
        400: {'description': 'Invalid input'},
        403: {'description': 'User is not a registered donor'}
    }
})
def create_blood_donation():
    """Create a new blood donation"""
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid input"}), 400

    user_id = get_jwt_identity()
    donor = Donor.query.filter_by(user_id=user_id).first()

    if not donor:
        return jsonify({"message": "User is not a registered donor"}), 403

    new_donation = BloodDonation(
        donor_id=donor.id,
        blood_group=data['blood_group'],
        donation_date=date.fromisoformat(data['donation_date']),
        quantity=data.get('quantity')
    )

    donor.last_donation = new_donation.donation_date

    db.session.add(new_donation)
    db.session.add(donor)
    db.session.commit()

    return jsonify(new_donation.to_dict()), 201

@blood_donation_bp.route('/', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Blood Donation'],
    'responses': {
        200: {
            'description': 'A list of blood donations',
            'schema': {
                'type': 'array',
                'items': {
                    '$ref': '#/definitions/BloodDonation'
                }
            }
        }
    }
})
def get_blood_donations():
    """Get all blood donations"""
    donations = BloodDonation.query.all()
    return jsonify([donation.to_dict() for donation in donations]), 200

@blood_donation_bp.route('/<int:donation_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Blood Donation'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'name': 'donation_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the blood donation to retrieve'
        }
    ],
    'responses': {
        200: {
            'description': 'A blood donation object',
            'schema': {
                '$ref': '#/definitions/BloodDonation'
            }
        },
        404: {
            'description': 'Blood donation not found'
        }
    }
})
def get_blood_donation(donation_id):
    """Get a blood donation by ID"""
    donation = db.get_or_404(BloodDonation, donation_id)
    return jsonify(donation.to_dict())
