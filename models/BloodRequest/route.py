from flask import Blueprint, request, jsonify
from database import db
from models.BloodRequest.model import BloodRequest
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

blood_request_bp = Blueprint('blood-request', __name__, url_prefix='/blood-requests')

@blood_request_bp.route('/', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Blood Request'],
    'responses': {
        200: {
            'description': 'A list of blood requests',
            'schema': {
                'type': 'array',
                'items': {
                    '$ref': '#/definitions/BloodRequest'
                }
            }
        }
    },
    'parameters': [
        {
            'name': 'donor_id',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filter requests by donor ID'
        },
        {
            'name': 'requester_id',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filter requests by requester ID'
        },
        {
            'name': 'blood_type',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filter requests by blood type'
        }
    ]
}
)
def get_blood_requests():
    query = BloodRequest.query

    donor_id = request.args.get('donor_id')
    requester_id = request.args.get('requester_id')
    blood_type = request.args.get('blood_type')

    if donor_id:
        query = query.filter_by(donor_id=donor_id)
    if requester_id:
        query = query.filter_by(requester_id=requester_id)
    if blood_type:
        query = query.filter_by(blood_type=blood_type)

    return jsonify([req.to_dict() for req in query.all()]), 200

@blood_request_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Blood Request'],
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
            'description': 'A single blood request',
            'schema': {
                '$ref': '#/definitions/BloodRequest'
            }
        },
        404: {
            'description': 'Blood request not found'
        }
    }
})
def get_blood_request(id):
    req = db.session.get(BloodRequest, id)
    if req:
        return jsonify(req.to_dict()), 200
    return jsonify({'message': 'Blood request not found'}), 404

@blood_request_bp.route('/', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Blood Request'],
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'required': ['blood_type', 'quantity', 'location'],
                'properties': {
                    'blood_type': {'type': 'string'},
                'name': {'type': 'string'},
                                    'quantity': {'type': 'integer'},
                'phone': {'type': 'string'},
                    'location': {'type': 'string'},
                    'donor_id': {'type': 'string', 'nullable': True}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Blood request created successfully',
            'schema': {
                '$ref': '#/definitions/BloodRequest'
            }
        }
    }
})
def create_blood_request():
    data = request.get_json()
    requester_id = get_jwt_identity()

    new_request = BloodRequest(
        requester_id=requester_id,
        blood_type=data.get('blood_type'),
        quantity=data.get('quantity'),
        name=data.get('name'),
        phone=data.get('phone'),
        location=data.get('location'),
        donor_id=data.get('donor_id')
    )
    db.session.add(new_request)
    db.session.commit()
    return jsonify(new_request.to_dict()), 201

@blood_request_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['Blood Request'],
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
                    'donor_id': {'type': 'string', 'nullable': True},
                    'status': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Blood request updated successfully',
            'schema': {
                '$ref': '#/definitions/BloodRequest'
            }
        },
        401: {
            'description': 'Unauthorized'
        },
        404: {
            'description': 'Blood request not found'
        }
    }
})
def update_blood_request(id):
    req = db.session.get(BloodRequest, id)
    if not req:
        return jsonify({'message': 'Blood request not found'}), 404
    
    # Ensure the user is updating their own request
    if str(req.requester_id) != get_jwt_identity():
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    req.donor_id = data.get('donor_id', req.donor_id)
    req.status = data.get('status', req.status)
    db.session.commit()
    return jsonify(req.to_dict()), 200


