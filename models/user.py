class UserModel:
    def __init__(self, id, email, expiration_date):
        self.id = id
        self.email = email
        self.expiration_date = expiration_date

    def json(self):
        return {
            'id': self.id,
            'email': self.email,
            'expiration_date': self.expiration_date
        }
