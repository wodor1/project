from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, reqparse
from .mixin_model import MixinModel

db = SQLAlchemy()

class Device(db.Model, MixinModel):
    __tablename__ = 'devices'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    device_type = db.Column(db.String(120), nullable=False)
    device_status = db.Column(db.String(120), nullable=False)

    def __init__(self, user_id, device_type, device_status):
        self.user_id = user_id
        self.device_type = device_type
        self.device_status = device_status

    def json(self):
        return {
            'user_id': self.user_id,
            'device_type': self.device_type,
            'device_status': self.device_status
        }
