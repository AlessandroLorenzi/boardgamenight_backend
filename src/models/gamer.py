from db import db
import string
import secrets
from passlib.hash import bcrypt

class GamerModel(db.Model):
    __tablename__ = 'gamers'

    id = db.Column(db.String(10), primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(60), unique=True)

    events = db.relationship('EventModel', lazy='dynamic')


    def __init__(self, username, email, password):
        alphabet = string.ascii_letters + string.digits
        self.id = ''.join(secrets.choice(alphabet) for i in range(10))
        self.username = username
        self.update(email, password)


    def update(self, email, password):
        self.email = email
        self.password = bcrypt.hash(password)

    def json(self):
        return {
            'username': self.username,
            'id' : self.id,
            'email' : self.email
        }

    @classmethod
    def authenticate(cls, username, password):
        gamer = cls.find_by_username(username)
        if gamer and bcrypt.verify(password, gamer.password):
            return gamer

        gamer = cls.find_by_email(username)
        if gamer is None:
            return False
        if bcrypt.verify(password, gamer.password):
            return gamer

        return False

    @classmethod
    def identity(cls, payload):
        id = payload['identity']
        return cls.find_by_id(id, None)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
