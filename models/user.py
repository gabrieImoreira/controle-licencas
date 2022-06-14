from enum import unique
from sql_alchemy import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(320), unique=True)
    expiration_date = db.Column(db.String(10))


    def __init__(self, email, expiration_date):
        self.email = email
        self.expiration_date = expiration_date

    def json(self):
        return {
            'id': self.id,
            'email': self.email,
            'expiration_date': self.expiration_date
        }

    @classmethod
    def find_user(cls, id):
        user = cls.query.filter_by(id=id).first()
        if user:
            return user
        return None
    
    @classmethod
    def check_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return False

    def get_id(self):
        return self.id
    
    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def update_user(self, email, expiration_date):
        self.email = email
        self.expiration_date = expiration_date
    
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()