from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask import request
from flask.ext.api import FlaskAPI
from flask.ext.api.exceptions import \
    AuthenticationFailed, NotFound, NotAcceptable, ParseError
from decorators import auth
from models import User, BucketList, BucketListItem
from flask_restful import  Api
from resources import *


app = Flask(__name__)
app.config.from_object('config')
app.config["JSON_SORT_KEYS"] = False

api = Api(app)

api.add_resource(LoginUser, "/auth/login")
api.add_resource(RegisterUser, "/auth/register")
api.add_resource(AllBucketLists, "/bucketlists/")
api.add_resource(SingleBucketList, "/bucketlists/<int:id>")
api.add_resource(AllBucketListItems, '/bucketlists/<id>/items/')
#api.add_resource(BucketListItem, '/bucketlists/<id>/items/<item_id>')

@app.route("/", methods = ["GET","POST"])
def home_page(): 
    return 'Hello World! Welcome to BucketList Manager. Please login/register to access our services'

if __name__ == '__main__':
    app.run(debug=True)