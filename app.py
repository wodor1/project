from flask import Flask, render_template
from flask_restful import Api
from db import db
from models.mixin_model import MixinModel

from models.user import User
from models.device import Device
from models.incident import Incident
from models.network import Network
from models.incident_device import Incident_Device
from models.incident_network import Incident_Network

from resources.user import UserResource, UserListResource
from resources.device import DeviceResource, DeviceListResource
from resources.incident import IncidentResource, IncidentListResource
from resources.network import NetworkResource, NetworkListResource

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy inicializálása
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html.j2')

@app.route('/incidents')
def incidents():
    return render_template('incidents.html.j2')

@app.route('/documentations')
def documentations():
    return render_template('documentations.html.j2')

@app.route('/about')
def about():
    return render_template('about.html.j2')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# API végpontok
api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(UserListResource, '/users')
api.add_resource(DeviceResource, '/devices', '/devices/<int:device_id>')
api.add_resource(DeviceListResource, '/devices')
api.add_resource(IncidentResource, '/incidents', '/incidents/<int:incident_id>')
api.add_resource(IncidentListResource, '/incidents')
api.add_resource(NetworkResource, '/networks', '/networks/<int:network_id>')
api.add_resource(NetworkListResource, '/networks')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
