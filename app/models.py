from app import db



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable = False)
    password = db.Column(db.String(255), nullable=False)
    bucketlists = db.relationships('Bucketlist', lazy='dynamic')

    def __init__(self, fname, lname, email, password):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_all(self):
        return User.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Bucketlist(db.Model):
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    blistname = db.Column(db.String(255), nullable=False)
    items = db.Column(db.relationships('BucketListItems', lazy="dynamic"), nullable=False)

    def __init__(self, blistname):
        self.blistname = blistname


class BucketlistItem(db.Model):
    __tablename__ = 'Bucketlistitems'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'), nullable=False)

    def __init__(self, item_name):
        self.item_name = item_name


