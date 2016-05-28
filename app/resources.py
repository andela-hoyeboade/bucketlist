from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class BucketList(Resource):
  def get(self):

  def post(self):
    

