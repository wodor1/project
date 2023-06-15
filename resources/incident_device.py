from flask_restful import Resource
from models.incident_device import Incident_Device
from models.incident import Incident
from models.device import Device

class Incident_DeviceResource(Resource):
    def post(self, incident_id, device_id):
        incident = Incident.find_by_id(incident_id)
        device = Device.find_by_id(device_id)
        if incident and device:
            incident_device = Incident_Device(incident_id=incident_id, device_id=device_id)
            incident_device.save_to_db()
            return {'message': 'Device added to the incident.'}, 201
        return {'message': 'Incident or device not found.'}, 404

    def delete(self, incident_id, device_id):
        incident_device = Incident_Device.find_by_attribute(incident_id=incident_id, device_id=device_id)
        if incident_device:
            incident_device.delete_from_db()
            return {'message': 'Device removed from the incident.'}, 200
        return {'message': 'Incident_Device not found.'}, 404
