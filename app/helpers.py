from models import User
from flask import current_app
from flask.ext.api.exceptions import AuthenticationFailed, PermissionDenied, \
    NotFound
import jwt
from flask import jsonify, request
from flask_restful import reqparse


def get_current_user_id(token):
    #try:
        secret_key = current_app.config.get('SECRET_KEY')
        decoded = jwt.decode(token, secret_key)
        return User.query.filter_by(username=decoded['username']).first().id
    #except:
    #    raise AuthenticationFailed("Cannot authenticate user")

def validate_args(fields={}):
    """
    This method helps to parse and validate provided parameters.
    It will return parsed argument if the required fields are in request
    """
    parser = reqparse.RequestParser()
    for field in fields.keys():
        help_message = field + ' can not be blank'
        parser.add_argument(field, required=fields[field], help=help_message)

    return parser.parse_args()

messages = {"username_not_found": {"message": "username does not exist"},
            "password_incorrect": {"message": "Password incorrect"},
            "bucketlist_updated": {"message": "Bucketlist updated"},
            "bucketlist_not_updated": {"message": "Bucketlist not updated"},
            "bucketlist_not_exist": {"message": "Bucketlist does not exist"},
            "bucketlist_exist": {"message": "Bucketlist already exist"},
            "no_bucketlist": {"message": "Cannot locate any bucketlist for user"},
            "user_pass_blank": {"message": "Username or Password cannot be blank"},
            "registered": {"message": "You have been registered. Please login"},
            "not_registered": {"message": "Unable to register user. Please try again"},
            "user_exist": {"message": "Username already exists"},
            "bucketlist_not_saved":{"message" "Unable to save bucketlist. Please try again"},
             "no_bucketlist_name":{"message": "Please supply bucketlist name"},
             "bucketlist_not_deleted": {"message": "Unable to delete the bucketlist"},
              "bucketlist_deleted": {"message": "Bucketlist deleted"}


}
