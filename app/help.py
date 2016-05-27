from flask_restful import reqparse
from models import db
import app


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


def stringify(arg):
    if arg == False:
        return "False"
    elif arg == True:
        return "True"
    else:
        return arg
