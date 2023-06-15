from flask_restful import Resource, reqparse
from models.network import Network

class NetworkResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('network_type',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('network_status',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, network_id):
        network = Network.find_by_id(network_id)
        if network:
            return network.json()
        return {'message': 'Network not found'}, 404

    def post(self):
        data = NetworkResource.parser.parse_args()
        network = Network(**data)
        network.save_to_db()
        return network.json(), 201

    def put(self, network_id):
        data = NetworkResource.parser.parse_args()
        network = Network.find_by_id(network_id)

        if network:
            network.user_id = data['user_id'] or network.user_id
            network.network_type = data['network_type'] or network.network_type
            network.network_status = data['network_status'] or network.network_status
            network.save_to_db()
            return network.json()
        return {'message': 'Network not found'}, 404

    def delete(self, network_id):
        network = Network.find_by_id(network_id)
        if network:
            network.delete_from_db()
            return {'message': 'Network deleted.'}
        return {'message': 'Network not found'}, 404


class NetworkListResource(Resource):
    def get(self):
        return {'networks': [network.json() for network in Network.query.all()]}
