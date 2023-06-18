from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from .mixin_model import MixinModel
from db import db

class Incident(db.Model, MixinModel):
    __tablename__ = 'incidents'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    type = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(120), nullable=False)

    def __init__(self, user_id, type, status, description=None):
        self.user_id = user_id
        self.type = type
        self.status = status
        self.description = description

    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'type': self.type,
            'status': self.status,
            'description': self.description
        }
