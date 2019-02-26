from werkzeug.security import check_password_hash, generate_password_hash
from app.models.__init__ import db
from datetime import datetime


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True, unique=True)
    email = db.Column('email', db.String(254), nullable=False, unique=True)
    password = db.Column('password', db.String(350), nullable=False)
    verified = db.Column('verified', db.Boolean, nullable=False)

    def __init__(self, email, password):
        self.set_email(email)
        self.set_password(password)
        self.set_verified(False)

    def get_id(self):
        return self.id

    def get_email(self):
        return self.email

    def set_email(self, email):
        if self.user_exists(email):
            return False
        self.email = email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, plaintext_passwd):
        return check_password_hash(self.password, plaintext_passwd)

    def get_verified(self):
        return self.email

    def set_verified(self, verified):
        self.verified = verified

    @staticmethod
    def user_exists(email):
        user = Users.query.filter_by(email=email).first()
        if user:
            return True
        else:
            return False

    def get_json(self):
        data = {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'verified': self.verified
        }
        return data
