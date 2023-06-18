from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from typing import TYPE_CHECKING
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from .mixin_model import MixinModel

class User(UserMixin, db.Model, MixinModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False, default='user')

    def __init__(self, username, email, password, role='user'):
        self.username = username
        self.email = email
        self.set_password(password)  # use set_password method
        self.role = role

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email, 'role': self.role}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()