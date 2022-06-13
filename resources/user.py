from flask_restful import Resource, reqparse
from models.user import UserModel

users = [
    {
        'id': 0,
        'email': 'gantonio155@gmail.com',
        'expiration_date': '30/09/2022'
    },
    {
        'id': 1,
        'email': 'fabio@outlook.com',
        'expiration_date': '12/06/2022'
    },
    {
        'id': 2,
        'email': 'maria@gmail.com',
        'expiration_date': '14/01/2023'
    }
]

class Users(Resource):
    def get(self):
        return {'users': users}

class User(Resource):
    attr = reqparse.RequestParser()
    attr.add_argument('email')
    attr.add_argument('expiration_date')

    def find_user(id):
        for user in users:
            if user['id'] == id:
                return user
        return False

    def get(self, id):
        user = User.find_user(id)
        print(user)
        if user:
            return user
        return {'message': 'User not found.'}, 404

    def post(self, id):
        data = User.attr.parse_args()
        user_object = UserModel(id, **data)
        new_user = user_object.json()
        users.append(new_user)
        return new_user, 201

    def put(self, id):
        data = User.attr.parse_args()
        user_object = UserModel(id, **data)
        edit_user = user_object.json()
        user = User.find_user(id)
        if user:
            user.update(edit_user)
            return user, 200
        return {'message': 'User not found.'}, 404
    
    def delete(self, id):
        global users
        users = [user for user in users if user['id'] != id]
        return {'message': 'User deleted.'}

