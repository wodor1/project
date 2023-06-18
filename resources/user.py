from flask_restful import Resource, reqparse
from models.user import User

class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('role',
                        type=str,
                        required=False,
                        help="This field can be left blank!"
                        )
    
    def get(self, user_id):
        user = User.find_by_id(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404

    def post(self):
        data = UserResource.parser.parse_args()
        user = User(**data)
        user.save_to_db()
        return user.json(), 201

    def put(self, user_id):
        data = UserResource.parser.parse_args()
        user = User.find_by_id(user_id)

        if user:
            user.username = data['username'] or user.username
            user.email = data['email'] or user.email
            user.save_to_db()
            return user.json()
        return {'message': 'User not found'}, 404

    def delete(self, user_id):
        user = User.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return {'message': 'User deleted.'}
        return {'message': 'User not found'}, 404


class UserListResource(Resource):
    def get(self):
        return {'users': [user.json() for user in User.query.all()]}
