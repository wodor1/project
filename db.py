# db.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()
