from flask_restful import Resource, reqparse
from models.user import UserModel

class Users(Resource):
    def get(self):
        return {'users': [user.json() for user in UserModel.query.all()]}

class User(Resource):
    attr = reqparse.RequestParser()
    attr.add_argument('email', type=str, required=True, help="The field 'email' cannot be left blank.")
    attr.add_argument('expiration_date', type=str, required=True, help="The field 'expiration_date' cannot be left blank.")
    def get(self, id):
        user = UserModel.find_user(id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404

    def post(self, id):
        if UserModel.find_user(id):
            return {'message': 'User already exists.'}, 400
        data = User.attr.parse_args()
        user = UserModel(id, **data)
        try:
            user.save_user()
        except:
            return {'message': 'An internal error ocurred trying to save user.'}, 500
        return user.json()

    def put(self, id):
        data = User.attr.parse_args()
        user = UserModel.find_user(id)
        if user:
            user.update_user(**data)
            try:
                user.save_user()
            except:
                return {'message': 'An internal error ocurred trying to save user.'}, 500
            return user.json(), 200
        return {'message': 'User not found.'}, 404
    
    def delete(self, id):
        user = UserModel.find_user(id)
        if user:
            try:
                user.save_user()
            except:
                return {'message': 'An internal error ocurred trying to delete user.'}, 500
            user.delete_user()
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404
