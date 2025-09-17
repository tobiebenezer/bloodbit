from database import db
import datetime

class BloodRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blood_type = db.Column(db.String(3), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)

    requester = db.relationship('User', foreign_keys=[requester_id], back_populates='requests')
    donor = db.relationship('User', foreign_keys=[donor_id])

    def __init__(self, requester_id, blood_type, quantity, location, name, phone, donor_id=None):
        self.requester_id = requester_id
        self.blood_type = blood_type
        self.quantity = quantity
        self.location = location
        self.donor_id = donor_id
        self.name = name
        self.phone = phone
        self.status = 'Pending'

    def to_dict(self):
        return {
            'id': self.id,
            'requester_id': self.requester_id,
            'blood_type': self.blood_type,
            'quantity': self.quantity,
            'location': self.location,
            'name': self.name,
            'phone': self.phone,
            'status': self.status,
            'donor_id': self.donor_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
