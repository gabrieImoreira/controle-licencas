from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.user import UserModel

class Users(Resource):
    @jwt_required()
    def get(self):
        return {'users': [user.json() for user in UserModel.query.all()]}

    @jwt_required()
    def post(self):
        data = User.attr.parse_args()
        email_exists = UserModel.check_email(data['email'])
        if email_exists:
            return {'message': 'Email already exists.'}, 500
        user = UserModel(**data)
        try:
            user.save_user()
        except:
            return {'message': 'An internal error ocurred trying to save user.'}, 500
        return user.json()

class User(Resource):
    attr = reqparse.RequestParser()
    attr.add_argument('email', type=str, required=True, help="The field 'email' cannot be left blank.")
    attr.add_argument('expiration_date', type=str, required=True, help="The field 'expiration_date' cannot be left blank.")
    
    @jwt_required()
    def get(self, id):
        user = UserModel.find_user(id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404

    @jwt_required()
    def put(self, id):
        data = User.attr.parse_args()
        user = UserModel.find_user(id)
        if user:
            user = UserModel.check_email(data['email'])
            if user.get_id() != id:
                return {'message': 'Email already exists in another register.'}, 400
            user.update_user(**data)
            try:
                user.save_user()
            except:
                return {'message': 'An internal error ocurred trying to save user.'}, 500
            return user.json(), 200
        return {'message': 'User not found.'}, 404
    
    @jwt_required()
    def delete(self, id):
        user = UserModel.find_user(id)
        if user:
            try:
                user.save_user()
            except:
                return {'message': 'An internal error ocurred trying to delete user.'}, 500
            user.delete_user()
            return {'message': 'User deleted.'}, 200
        return {'message': 'User not found.'}, 404
