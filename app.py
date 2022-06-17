from flask import Flask
from flask_restful import Api
from resources.admin import Admin, AdminRegister, AdminLogin
from resources.user import User, Users
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_db():
    db.create_all()

api.add_resource(Users, '/users')
api.add_resource(User, '/users/<int:id>')
api.add_resource(Admin, '/admin/<int:id>')
api.add_resource(AdminRegister, '/register')
api.add_resource(AdminLogin, '/login')


if __name__ == '__main__':
    from sql_alchemy import db
    db.init_app(app)
    app.run(debug=True)