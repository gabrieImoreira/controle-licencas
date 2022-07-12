from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from models.admin import AdminModel
from blacklist import BLACKLIST
from safe_cmp import safe_cmp
from passlib.hash import bcrypt


class Admin(Resource):
    hasher = bcrypt.using(rounds=13)
    # admin/{id}
    # @jwt_required()
    def get(self, id):
        admin = AdminModel.find_admin(id)
        if admin:
            return admin.json()
        return {'message': 'Admin not found.'}, 404
    
    # @jwt_required()
    def delete(self, id):
        admin = AdminModel.find_admin(id)
        if admin:
            try:
                admin.save_admin()
            except:
                return {'message': 'An internal error ocurred trying to delete admin.'}, 500
            admin.delete_admin()
            return {'message': 'Admin deleted.'}, 200
        return {'message': 'Admin not found.'}, 404

class AdminRegister(Resource):
    # /register
    attr = reqparse.RequestParser()
    attr.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank.")
    attr.add_argument('password', type=str, required=True, help="The field 'password' cannot be left blank.")
    
    # @jwt_required()
    def post(self):
        self.attr.add_argument('authorization', type=str, required=False, help="The field 'authorization' cannot be left blank.")
        data = self.attr.parse_args()

        if AdminModel.find_by_login(data['login']):
            return {"message": "The login '{}' already exists.".format(data['login'])}
        
        data['password'] = Admin.hasher.hash(data['password'])
        admin = AdminModel(**data)
        admin.save_admin()
        return {'message': 'User created successfully'}, 201

class AdminLogin(Resource):
    #login
    @classmethod
    def post(cls):
        data = AdminRegister.attr.parse_args()
        admin = AdminModel.find_by_login(data['login'])
        if admin and Admin.hasher.verify(data['password'] ,admin.password) == 1:
            access_token = create_access_token(identity=admin.id)
            return {'access_token': access_token}, 200
        return {'message': 'The username or password is incorrect.'}, 401

class AdminLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!'}, 200
