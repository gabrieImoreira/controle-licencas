from flask import Flask
from flask_restful import Api
from resources.user import User, Users

app = Flask(__name__)
api = Api(app)

api.add_resource(Users, '/users')
api.add_resource(User, '/users/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)