from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import sqlalchemy
import hashlib

import app
db = SQLAlchemy()
class_mapper = sqlalchemy.orm.class_mapper

class Base(db.Model):
    """Base model that other models inherit from
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def save(self):
        
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False
    def update(self):
        try:
            db.session.commit()
            return True
        except:
            return False
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            return False

class User(Base):
    """User model that maps to users table
    """
    __tablename__ = "user"
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    bucketlists = db.relationship("BucketList", order_by="BucketList.id")

    def __init__(self, username, password):
        """Initialize with <username> and <password>
        """
        self.username = username
        self.password = hashlib.sha512(password).hexdigest()

    def is_valid_password(self, password):
        """Validates user password
        """
        return self.password == hashlib.sha512(password).hexdigest()

    def __repr__(self):
        return '<User %r>' % self.username

class BucketList(Base):
    """Maps to the bucketlist table
    """
    __tablename__ = 'bucket_list'
    name = db.Column(db.String(256), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship("User")
    bucketlistitems = db.relationship("BucketListItem")

    def __init__(self, name, created_by):
        """Initialize with <creator>, <name>
        """
        self.name = name
        self.created_by = created_by

class BucketListItem(Base):
    __tablename__ = "bucket_list_item"
    name = db.Column(db.String(256), nullable=False)
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(BucketList.id))

    def __init__(self, bucketlist_id, name, done=False):
        """Initializes model with <bucketlist_id> and <name>.
        <done> is optional
        """
        self.bucketlist_id = bucketlist_id
        self.name = name
        self.done = done
