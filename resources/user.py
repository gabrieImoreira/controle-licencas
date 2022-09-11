from datetime import datetime
import sqlite3
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.user import UserModel

# /users?email=gabriel.moreira@google.com&initial_date=2022-06-01&final_date=2022-12-31
def normalize_path_params(email=None,
                        initial_date='01-01-1900',
                        final_date='3000-01-01',
                        limit = 50,
                        offset = 0, **data):
    if email:
        return { 
            'email': email,
            'initial_date': initial_date,
            'final_date': final_date,
            'limit': limit,
            'offset': offset
        }
    return { 
            'initial_date': initial_date,
            'final_date': final_date,
            'limit': limit,
            'offset': offset
        }

class Inicial(Resource):
    def get(self):
        return 'API Titanium.'

class Users(Resource):
    # @jwt_required()
    def get(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        data = request.args
        params = normalize_path_params(**data)

        if not params.get('email'):
            query = "SELECT * from users WHERE \
                (expiration_date >= ? and expiration_date <= ?) \
                    LIMIT ? OFFSET ?"
            tupla = tuple(params[key] for key in params)
            result = cursor.execute(query, tupla)
        else: 
            query = "SELECT * from users WHERE email = ? and \
                (expiration_date >= ? and expiration_date <= ?) \
                    LIMIT ? OFFSET ?"
            tupla = tuple(params[key] for key in params)
            result = cursor.execute(query, tupla)
        
        users = []
        for line in result:
            users.append({
                'id': line[0],
                'email': line[1],
                'expiration_date': (line[2])[:10]
            })
        return {'users': users}

    #@jwt_required()
    def post(self):
        data = User.attr.parse_args()
        try:
            data['expiration_date'] = datetime.strptime(data['expiration_date'], '%Y-%m-%d')
        except:
            return {'message': 'Invalid date.'}, 404
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
    
    # @jwt_required()
    def get(self, id):
        user = UserModel.find_user(id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404

    # @jwt_required()
    def put(self, id):
        data = User.attr.parse_args()
        try:
            data['expiration_date'] = datetime.strptime(data['expiration_date'], '%Y-%m-%d')
        except:
            return {'message': 'Invalid date.'}, 404
        user = UserModel.find_user(id)
        if user:
            user_check = UserModel.check_email(data['email'])
            if user_check is not None and user_check.get_id() != id:
                return {'message': 'Email already exists in another register.'}, 400
            user.update_user(**data)
            try:
                user.save_user()
            except:
                return {'message': 'An internal error ocurred trying to save user.'}, 500
            return user.json(), 200
        return {'message': 'User not found.'}, 404
    
    # @jwt_required()
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
