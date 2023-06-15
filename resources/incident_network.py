from flask_restful import Resource
from models.incident_network import Incident_Network
from models.incident import Incident
from models.network import Network

class Incident_NetworkResource(Resource):
    def post(self, incident_id, network_id):
        incident = Incident.find_by_id(incident_id)
        network = Network.find_by_id(network_id)
        if incident and network:
            incident_network = Incident_Network(incident_id=incident_id, network_id=network_id)
            incident_network.save_to_db()
            return {'message': 'Network added to the incident.'}, 201
        return {'message': 'Incident or network not found.'}, 404

    def delete(self, incident_id, network_id):
        incident_network = Incident_Network.find_by_attribute(incident_id=incident_id, network_id=network_id)
        if incident_network:
            incident_network.delete_from_db()
            return {'message': 'Network removed from the incident.'}, 200
        return {'message': 'Incident_Network not found.'}, 404
