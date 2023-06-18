from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def init_app(app):
    login_manager.init_app(app)

    @app.route('/register_web', methods=['GET', 'POST'])
    def register_web():
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role')
            if User.find_by_username(username):
                return "Username already exists", 400
            user = User(username, email, generate_password_hash(password), role)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.find_by_username(username)
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('protected'))
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/protected')
    @login_required
    def protected():
        return f'Logged in as: {current_user.username}'
