from app.models import User, BucketList, BucketListItem, db
from flask_restful import reqparse
from functools import wraps
from app.help import *
from flask import request
from flask import jsonify, current_app
from datetime import datetime, timedelta
from flask.ext.sqlalchemy import sqlalchemy as S
from flask.ext.api.exceptions import AuthenticationFailed, PermissionDenied, \
    NotFound
import jwt
import hashlib

from collections import OrderedDict


def register(username, password):
    """Registers a user on the bucketlist service
    """
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"message": "Username already exist"})
    else:
        args = validate_args({'username': True, 'password': True})
        user = User(args['username'], args['password'])
        return jsonify({"message": "You have been registered. Please login"}) if user.save() \
            else jsonify({"message": "Cannot add user"})


def valid_user(username, password):
    password = hashlib.sha512(password).hexdigest()
    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return False
    else:
        return True


def get_current_user_id(token):
    try:
        secret_key = current_app.config.get('SECRET_KEY')
        decoded = jwt.decode(token, secret_key)
        return User.query.filter_by(username=decoded['username']).first().id
    except:
        raise AuthenticationFailed("Cannot authenticate user")


def login(username, password):
    """Generates a token and persists it in the database until
    user logs out
    """
    if valid_user(username, password):
        user_data = {
            'username': username,
            'password': password
        }

        secret_key = current_app.config.get('SECRET_KEY')
        token = jwt.encode(user_data, secret_key)
        return jsonify({"message": "Succesful login. Please use this token for authentication",
                        "token": token,
                        "user_id": get_current_user_id(token)
                        })
    else:
        return jsonify({"message": "User not found"})

def create_bucketlist(name, created_by):
    bucketlist = BucketList.query.filter_by(
        name=name, created_by=created_by).first()
    if bucketlist:
        return jsonify({"message": "Bucketlist with the name %s already exist" % (name)})
    else:
        bucketlist = BucketList(name, created_by)
        return jsonify({"message": "Saved",
                        "name": name,
                        "created_by": created_by
                        }) if bucketlist.save() \
            else jsonify({"message": "Cannot save bucketlist"})


def get_single_bucketlist(bucketlist_id):
    bucketlist = BucketList.query.filter_by(
        id=bucketlist_id).first()
    out = {"id": bucketlist.id,
           "name": bucketlist.name,
           "date_created": bucketlist.date_created,
           "date_modified": bucketlist.date_modified,
           "items": get_all_bucketlist_item(bucketlist.id),
           "created_by": bucketlist.created_by}
    return out


def get_all_bucketlist(user_id):
    all_bucketlist = BucketList.query.filter_by(
        created_by=user_id).all()
    if all_bucketlist:
        final_output = [get_single_bucketlist(
            bucketlist.id) for bucketlist in all_bucketlist]
        return {"data": final_output}
    else:
        return jsonify({"message": "Cannot locate any bucketlist for user"})


def get_bucketlist_item(bucketlist_id, bucketlist_item_id):
    return []


def get_all_bucketlist_item(bucketlist_id):
    return []


def create_bucketlist_item(bucketlist_id, name, done):
    bucketlist_item = BucketListItem.query.filter_by(
        bucketlist_id=bucketlist_id, name=name).first()
    if not bucketlist_item:
        done = True if str(done).lower == "true" else False
        bucketlist_item = BucketListItem(
            bucketlist_id=bucketlist_id, name=name, done=done)
        return jsonify({"message": "Saved",
                        "name": name,
                        "bucketlist_id": bucketlist_id,
                        "done": done
                        }) if bucketlist_item.save() \
            else jsonify({"message": "Cannot save bucketlist item"})
    else:
        return jsonify({"message": "Item already exist for Buckelist %s" % (bucketlist_id)})


def update_bucketlist(bucketlist_id, name):
    bucketlist = BucketList.query.filter_by(id=bucketlist_id).first()
    token = request.headers.get('Token')
    current_user = get_current_user_id(token)
    check_bucketlist_name = BucketList.query.filter_by(
        name=name, created_by=current_user).first()
    if not check_bucketlist_name:
        bucketlist.name = name
        return jsonify({"data": get_single_bucketlist(bucketlist_id)}) \
            if bucketlist.update() else jsonify({"message": "Cannot update bucketlist"})
    else:
        return jsonify({"message": "Bucketlist with the name %s already exist" % (name)})


def delete_bucket_list(bucketlist_id):
    bucketlist = BucketList.query.filter_by(id=bucketlist_id)
    return jsonify({"message": "Bucketlist deleted"}) if bucketlist.delete() \
        else jsonify({"message": "Unable to delete bucket"})


def user_is_login(f):
    """
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.headers.get('Token')
            secret_key = current_app.config.get('SECRET_KEY')
            decoded = jwt.decode(token, secret_key)
        except:
            raise AuthenticationFailed()
        return f(*args, **kwargs)
    return decorated


def bucketlist_exist(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        bucketlist_id = kwargs.get('id')
        bucketlist = BucketList.query.filter_by(id=bucketlist_id).first()
        try:
            assert bucketlist
        except:
            raise NotFound("Bucketlist with ID: %s does not exist" %
                           (bucketlist_id))
        return f(*args, **kwargs)
    return decorated


def belongs_to_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        bucketlist_id = kwargs.get('id')
        bucketlist_creator = BucketList.query.filter_by(
            id=bucketlist_id).first().created_by
        token = request.headers.get('Token')
        current_user = get_current_user_id(token)
        try:
            assert current_user == bucketlist_creator
        except:
            raise PermissionDenied(
                "Bucketlist with ID: %s does not belong to you" % (bucketlist_id))
        return f(*args, **kwargs)
    return decorated
