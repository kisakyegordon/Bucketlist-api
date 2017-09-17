from app import app, db, bcrypt


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable = False)
    password = db.Column(db.String(255), nullable=False)
    bucketlists = db.relationships('Bucketlist', backref = bucketlist, lazy = 'dynamic')

    def __init__(self):
        pass



class Bucketlist(db.Model):
    pass


class BucketlistItem(db.Model):
    pass

