from flask_sqlalchemy import SQLAlchemy
from .mixin_model import MixinModel

db = SQLAlchemy()

class Incident_Device(db.Model, MixinModel):
    __tablename__ = 'incident_device'

    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), primary_key=True)

    def __init__(self, incident_id, device_id):
        self.incident_id = incident_id
        self.device_id = device_id

    def json(self):
        return {
            'incident_id': self.incident_id,
            'device_id': self.device_id,
        }
