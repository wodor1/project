from flask_restful import Resource, reqparse
from models.user import User
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

class Auth(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('username',
                      type=str,
                      required=True,
                      help='This field cannot be left blank')
  parser.add_argument('password',
                      type=str,
                      required=True,
                      help='This field cannot be left blank')

  def post(self):
    data = Auth.parser.parse_args()
    user = User.find_by_username(data['username'])
    if user and check_password_hash(user.password_hash, data['password']):
      access_token = create_access_token(identity=user.id,
                                         expires_delta=timedelta(minutes=30))
      return {'access_token': access_token}, 200
    return {'message': 'Wrong username or password'}, 401

class Register(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field cannot be left blank')
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help='This field cannot be left blank')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field cannot be left blank')

    def post(self):
        data = Register.parser.parse_args()
        
        if User.find_by_username(data['username']):
            return {"message": "A user with that username already exists."}, 400

        user = User(data['username'], data['email'])
        user.password_hash = generate_password_hash(data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201