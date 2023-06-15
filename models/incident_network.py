from flask_sqlalchemy import SQLAlchemy
from .mixin_model import MixinModel

db = SQLAlchemy()

class Incident_Network(db.Model, MixinModel):
    __tablename__ = 'incident_network'

    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), primary_key=True)
    network_id = db.Column(db.Integer, db.ForeignKey('networks.id'), primary_key=True)

    def __init__(self, incident_id, network_id):
        self.incident_id = incident_id
        self.network_id = network_id

    def json(self):
        return {
            'incident_id': self.incident_id,
            'network_id': self.network_id,
        }
