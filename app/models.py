from app import db
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import jwt
from flask import current_app


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255),unique=True, nullable = False)
    password = db.Column(db.String(255), nullable=False)
    bucketlists = db.relationship('Bucketlist',  order_by='Bucketlist.id', lazy='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def password_is_valid(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    def generate_token(self, user_id):
        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Bucketlist(db.Model):
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey(User.id))
    name = db.Column(db.String(255), nullable=False)
    items = db.relationship(
        'BucketlistItem', backref="bucketlist", order_by='BucketlistItem.id', cascade="all, delete-orphan")

    def __init__(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Bucketlist.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def edit_list(self, blistname):
        self.blistname = blistname
        db.session.commit()


class BucketlistItem(db.Model):
    __tablename__ = 'Bucketlistitems'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(255), nullable=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, item_name, bucketlist_id, completed=False):
        self.item_name = item_name
        self.bucketlist_id= bucketlist_id
        self.completed = completed

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def edit_item(self, item_name, status=None):
        self.item_name = item_name
        if status:
            self.completed = status
        db.session.commit()


