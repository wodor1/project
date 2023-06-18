from flask import Flask, render_template, request, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from db import db
from web_auth import init_app as init_auth_app

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
from resources.incident_device import Incident_DeviceResource
from resources.incident_network import Incident_NetworkResource
from resources.auth import Auth, Register
from resources.register import UserRegister

app = Flask(__name__)

db_path: str = os.path.join(os.path.dirname(__file__), 'data.db')
db_uri: str = f'sqlite:///{db_path}'

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
jwt = JWTManager(app)
CORS(app)

db.init_app(app)
init_auth_app(app)

@app.before_first_request
def create_tables() -> None:
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        response = UserRegister().post()
        if response[1] != 201:
            return render_template('register.html.j2', error=response[0]['message'])
        else:
            return jsonify(response[0])
    return render_template('register.html.j2')

# API végpontok
api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(UserListResource, '/users')
api.add_resource(DeviceResource, '/devices', '/devices/<int:device_id>')
api.add_resource(DeviceListResource, '/devices')
api.add_resource(IncidentResource, '/incidents', '/incidents/<int:incident_id>')
api.add_resource(IncidentListResource, '/incidents')
api.add_resource(NetworkResource, '/networks', '/networks/<int:network_id>')
api.add_resource(NetworkListResource, '/networks')
api.add_resource(Incident_DeviceResource, '/incidents/<int:incident_id>/devices/<int:device_id>')
api.add_resource(Incident_NetworkResource, '/incidents/<int:incident_id>/networks/<int:network_id>')
api.add_resource(Auth, '/auth')