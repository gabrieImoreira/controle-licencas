from flask import Flask
from flask_restful import Api
from resources.admin import Admin, AdminRegister
from resources.user import User, Users


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_first_request
def create_db():
    db.create_all()

api.add_resource(Users, '/users')
api.add_resource(User, '/users/<int:id>')
api.add_resource(Admin, '/admin/<int:id>')
api.add_resource(AdminRegister, '/register')


if __name__ == '__main__':
    from sql_alchemy import db
    db.init_app(app)
    app.run(debug=True)