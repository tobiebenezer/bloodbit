from database import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from models.BloodDonation.model import BloodDonation

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    blood_type = db.Column(db.String(3), nullable=False)
    location = db.Column(db.String(120), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)
    
    donor = db.relationship('Donor', uselist=False, back_populates='user')
    donations = db.relationship('BloodDonation', back_populates='user', lazy='dynamic')
    requests = db.relationship('BloodRequest', foreign_keys='BloodRequest.requester_id', back_populates='requester', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'blood_type': self.blood_type,
            'location': self.location,
            'gender': self.gender,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'donations': self.donations.count(),
            'requests': self.requests.count()
        }
