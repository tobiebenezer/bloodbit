from database import db
import datetime

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    medical_history = db.Column(db.Text, nullable=True)
    is_available = db.Column(db.Boolean, default=True)
    last_donation = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)

    user = db.relationship('User', back_populates='donor')

    def __init__(self, user_id, medical_history=None, is_available=True, last_donation=None):
        self.user_id = user_id
        self.medical_history = medical_history
        self.is_available = is_available
        self.last_donation = last_donation

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.to_dict(),
            'medical_history': self.medical_history,
            'is_available': self.is_available,
            'last_donation': self.last_donation.isoformat() if self.last_donation else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
