from enum import unique
from sql_alchemy import db

class AdminModel(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(320), unique=True)
    password = db.Column(db.String(40))
    authorization = db.Column(db.String(40))


    def __init__(self, login, password, authorization):
        self.login = login
        self.password = password
        self.authorization = authorization

    def json(self):
        return {
            'id': self.id,
            'login': self.login,
             'authorization': self.authorization 
        }
    @classmethod
    def find_admin(cls, id):
        admin = cls.query.filter_by(id=id).first()
        if admin:
            return admin
        return None
    
    def save_admin(self):
        db.session.add(self)
        db.session.commit()

    def update_admin(self,login, password):
        self.login = login
        self.password = password
    
    def delete_admin(self):
        db.session.delete(self)
        db.session.commit()
    
    def return_permission(self, authorization):
        if authorization == 'HIGH':
            return True
        return False