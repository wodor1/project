from flask_restful import Resource, reqparse
from models.user import User
from werkzeug.security import generate_password_hash

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('role',
                        type=str,
                        required=False,
                        default='user',
                        help="This field is not required.")

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = User(data['username'], data['email'], data['password'], data['role'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201
