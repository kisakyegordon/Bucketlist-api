from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255),unique=True, nullable = False)
    password = db.Column(db.String(255), nullable=False)
    bucketlists = db.relationship('Bucketlist',  order_by='Bucketlist.id', lazy='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
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
    items = db.relationship('BucketlistItem', order_by='BucketlistItem.id',  lazy='dynamic')

    def __init__(self, blistname):
        self.blistname = blistname

    def save(self):
        db.session.add(self)
        db.session.commit()

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
    completed = db.Column(db.Boolean, default=False, nullable=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'), nullable=False)

    def __init__(self, item_name):
        self.item_name = item_name

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


