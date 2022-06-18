from flask import Flask, jsonify
from flask_restful import Api
from blacklist import BLACKLIST
from resources.admin import Admin, AdminRegister, AdminLogin, AdminLogout
from resources.user import User, Users
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_db():
    db.create_all()

@jwt.token_in_blocklist_loader
def verify_blacklist(self, token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def access_token_invalidated(jwt_header, jwt_payload):
    return jsonify({'message': 'You have been logged out.'}), 401

api.add_resource(Users, '/users')
api.add_resource(User, '/users/<int:id>')
api.add_resource(Admin, '/admin/<int:id>')
api.add_resource(AdminRegister, '/register')
api.add_resource(AdminLogin, '/login')
api.add_resource(AdminLogout, '/logout')

if __name__ == '__main__':
    from sql_alchemy import db
    db.init_app(app)
    app.run(debug=True)