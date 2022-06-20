from flask_restful import Resource
from flask import request
import re
from models.user import UserModel

class Auth(Resource):

    def get(self):
        data = request.args
        email = data.get('email')
        if email is None:
            return {"message": "Account not recognized."}, 200
        if email is not None and not re.match(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[-]?\w+[.]?\w+[.]?\w{2,3}$", email):
            return {"message": "Invalid e-mail."}
        user_object = [user.json() for user in UserModel.query.filter_by(email=email)]
        if len(user_object) > 0:
            return {
                "email": user_object[0]['email'],
                "expiration_date": user_object[0]['expiration_date']
            }
        else:
            return {"message": "Account not registered."}, 200