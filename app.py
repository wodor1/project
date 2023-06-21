from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from db import db
from web_auth import init_app as init_auth_app
from werkzeug.exceptions import BadRequestKeyError
from datetime import timedelta

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
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
# app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.secret_key = 'secret-key'

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

@app.route('/incidentpage')
def incidents():
    incidents = Incident.query.all()  # Fetch all incidents from the database
    return render_template('incidents.html.j2', incidents=incidents)

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

@app.route('/login_web', methods=['GET', 'POST'])
def login_web():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
        except BadRequestKeyError:
            flash("Username or Password not provided")
            return render_template('login.html.j2', error="Username or Password not provided")

        if not username or not password:
            flash("Username or Password cannot be empty")
            return render_template('login.html.j2', error="Username or Password cannot be empty")

        response = Auth().post()

        if response[1] != 200:
            flash("Wrong username or password")
            return render_template('login.html.j2', error="Wrong username or password")
        else:
            flash("Login successful")
            return redirect(url_for('home'))  # Redirect to home page after successful login

    return render_template('login.html.j2')

@app.route('/incident/update/<int:incident_id>', methods=['GET', 'POST'])
def update_incident(incident_id):
    resource = IncidentResource()
    if request.method == 'POST':
        resource.put(incident_id)
        return redirect(url_for('incidents'))
    else:
        incident = Incident.find_by_id(incident_id)
        return render_template('update_incident.html.j2', incident=incident)

@app.route('/incident/delete/<int:incident_id>', methods=['POST'])
def delete_incident(incident_id):
    resource = IncidentResource()
    resource.delete(incident_id)
    return redirect(url_for('incidentlist'))

# API végpontok
api.add_resource(UserResource, '/user', '/user/<int:user_id>')
api.add_resource(UserListResource, '/users')
api.add_resource(DeviceResource, '/device', '/device/<int:device_id>')
api.add_resource(DeviceListResource, '/devices')
api.add_resource(IncidentResource, '/incident', '/incident/<int:incident_id>')
api.add_resource(IncidentListResource, '/incidents')
api.add_resource(NetworkResource, '/network', '/network/<int:network_id>')
api.add_resource(NetworkListResource, '/networks')
api.add_resource(Incident_DeviceResource, '/incidents/<int:incident_id>/devices/<int:device_id>')
api.add_resource(Incident_NetworkResource, '/incidents/<int:incident_id>/networks/<int:network_id>')
api.add_resource(Auth, '/auth')