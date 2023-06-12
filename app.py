from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Az adatbázis konfigurációja
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'  # A SQLite adatbázis helyét jelzi

db = SQLAlchemy(app)

# Egy egyszerű modell az adatbázishoz
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

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

if __name__ == '__main__':
    db.create_all()  # Az adatbázis séma létrehozása
    app.run(debug=True)  # Az alkalmazás futtatása debug módban
