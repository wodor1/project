from flask_restful import Resource, reqparse
from models.device import Device

class DeviceResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('device_type',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('device_status',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, device_id):
        device = Device.find_by_id(device_id)
        if device:
            return device.json()
        return {'message': 'Device not found'}, 404

    def put(self, device_id):
        data = DeviceResource.parser.parse_args()
        device = Device.find_by_id(device_id)

        if device:
            device.device_type = data['device_type']
            device.device_status = data['device_status']
            device.save_to_db()
            return device.json()
        return {'message': 'Device not found'}, 404

    def delete(self, device_id):
        device = Device.find_by_id(device_id)
        if device:
            device.delete_from_db()
            return {'message': 'Device deleted.'}
        return {'message': 'Device not found'}, 404


class DeviceListResource(Resource):
    def get(self):
        return {'devices': [device.json() for device in Device.query.all()]}

    def post(self):
        data = DeviceResource.parser.parse_args()
        device = Device(**data)
        device.save_to_db()

        return device.json(), 201
