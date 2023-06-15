from flask_sqlalchemy import SQLAlchemy
from .mixin_model import MixinModel

db = SQLAlchemy()

class User(db.Model, MixinModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(120), nullable=False, default='user')

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email, 'role': self.role}
