"""Module containing the application models"""
from datetime import datetime, timedelta
from app import db
from flask import current_app
from flask_bcrypt import Bcrypt
import jwt


class User(db.Model):
    """Class containing User model"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    bucketlists = db.relationship('Bucketlist', order_by='Bucketlist.id', lazy='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def save(self):
        """method that saves the saves user information."""
        db.session.add(self)
        db.session.commit()

    def update_password(self, password):
        """
        This method update a new record to the database
        """
        self.password = Bcrypt().generate_password_hash(password).decode()
        db.session.commit()

    def password_is_valid(self, password):
        """Method that validates user password."""
        return Bcrypt().check_password_hash(self.password, password)

    def generate_token(self, user_id):
        """Method that generates token."""
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
                'gdgfd',
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """method that decodes token."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, 'gdgfd')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"


class Bucketlist(db.Model):
    """model containing bucketlist model."""
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey(User.id))
    name = db.Column(db.String(255), nullable=False)
    items = db.relationship(
        'BucketlistItem',
        backref="bucketlist",
        order_by='BucketlistItem.id',
        cascade="all, delete-orphan")

    def __init__(self, name, user_id):
        self.name = name
        self.userId = user_id

    def save(self):
        """method that saves bucket list information."""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """method that retrieves bucket lists"""
        return Bucketlist.query.all()

    def delete(self):
        """mehtod that deletes bucket lists"""
        db.session.delete(self)
        db.session.commit()

    def edit_list(self, blistname):
        """Methos that edits bucket lists"""
        self.blistname = blistname
        db.session.commit()

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)


class BucketlistItem(db.Model):
    """Class contains bucket list items model"""
    __tablename__ = 'Bucketlistitems'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(255), nullable=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, item_name, bucketlist_id, completed=False):
        self.item_name = item_name
        self.bucketlist_id = bucketlist_id
        self.completed = completed

    def save(self):
        """method that saves bucket list items."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """method that deletes bucket list items."""
        db.session.delete(self)
        db.session.commit()

    def edit_item(self, item_name, status=None):
        """Method that edits bucket list items."""
        self.item_name = item_name
        if status:
            self.completed = status
        db.session.commit()

    def __repr__(self):
        return "<BucketlistItem: {}>".format(self.name)
