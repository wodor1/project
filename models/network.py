from flask_sqlalchemy import SQLAlchemy
from .mixin_model import MixinModel
from typing import TYPE_CHECKING
from db import db

class Network(db.Model, MixinModel):
    __tablename__ = 'networks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    network_type = db.Column(db.String(120), nullable=False)
    network_status = db.Column(db.String(120), nullable=False)

    def __init__(self, user_id, network_type, network_status):
        self.user_id = user_id
        self.network_type = network_type
        self.network_status = network_status

    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'network_type': self.network_type,
            'network_status': self.network_status
        }
