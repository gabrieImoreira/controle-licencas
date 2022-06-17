from flask_restful import Resource, reqparse
from models.admin import AdminModel

class Admin(Resource):
    # admin/{id}
    def get(self, id):
        admin = AdminModel.find_admin(id)
        if admin:
            return admin.json()
        return {'message': 'Admin not found.'}, 404
    
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
    
    def post(self):
        attr = reqparse.RequestParser()
        attr.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank.")
        attr.add_argument('password', type=str, required=True, help="The field 'password' cannot be left blank.")
        attr.add_argument('authorization', type=str, required=True, help="The field 'authorization' cannot be left blank.")
        data = attr.parse_args()

        if AdminModel.find_by_login(data['login']):
            return {"message": "The login '{}' already exists.".format(data['login'])}
        
        admin = AdminModel(**data)
        admin.save_admin()
        return {'message': 'User created successfully'}, 201