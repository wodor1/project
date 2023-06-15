from flask_restful import Resource, reqparse
from models.incident import Incident

class IncidentResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('type',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('status',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('description',
                        type=str,
                        )

    def get(self, incident_id):
        incident = Incident.find_by_id(incident_id)
        if incident:
            return incident.json()
        return {'message': 'Incident not found'}, 404

    def post(self):
        data = IncidentResource.parser.parse_args()
        incident = Incident(**data)
        incident.save_to_db()
        return incident.json(), 201

    def put(self, incident_id):
        data = IncidentResource.parser.parse_args()
        incident = Incident.find_by_id(incident_id)

        if incident:
            incident.user_id = data['user_id'] or incident.user_id
            incident.type = data['type'] or incident.type
            incident.status = data['status'] or incident.status
            incident.description = data['description'] or incident.description
            incident.save_to_db()
            return incident.json()
        return {'message': 'Incident not found'}, 404

    def delete(self, incident_id):
        incident = Incident.find_by_id(incident_id)
        if incident:
            incident.delete_from_db()
            return {'message': 'Incident deleted.'}
        return {'message': 'Incident not found'}, 404


class IncidentListResource(Resource):
    def get(self):
        return {'incidents': [incident.json() for incident in Incident.query.all()]}
