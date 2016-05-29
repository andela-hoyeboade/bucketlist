from models import BucketList, BucketListItem
from decorators import auth
from flask_restful import Resource
from flask import jsonify, request
from helpers import *
from models import db


class LoginUser(Resource):
    def post(self):
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            if auth.valid_username(username):
                if auth.valid_password(username,password):
                    user_data = { 'username': username, 'password': password}
                    secret_key = current_app.config.get('SECRET_KEY')
                    token = jwt.encode(user_data, secret_key)
                    return jsonify({"message": "Succesful login. Please use this token for authentication",
                                    "token": token,
                                    "user_id": get_current_user_id(token)
                                    })
                else:
                    return messages["password_incorrect"]

            else:
                return messages["username_not_found"]
        else:
            return messages["user_pass_blank"]

class RegisterUser(Resource):
    def post(self):
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            if not auth.valid_username(username):
              user = User(username, password)
              return messages["registered"] if user.save() else messages["not_registered"]
            else:
              return messages["user_exist"]
        else:
            return messages["user_pass_blank"]


class SingleBucketList(Resource):
    @auth.user_is_login
    @auth.bucketlist_exist
    def get(self, id):
        bucketlist = BucketList.query.filter_by(
            id=id).first()
        out = {"id": bucketlist.id,
               "name": bucketlist.name,
               "date_created": bucketlist.date_created,
               "date_modified": bucketlist.date_modified,
               "items": [],  # get_all_bucketlist_item(bucketlist.id),
               "created_by": bucketlist.created_by}
        return jsonify({"data": out})

    @auth.user_is_login
    @auth.bucketlist_exist
    def put(self, id):
      name = request.form.get("name")
      bucketlist = BucketList.query.filter_by(id=id).first()
      token = request.headers.get('Token')
      current_user = get_current_user_id(token)
      check_bucketlist_name = BucketList.query.filter_by(
          name=name, created_by=current_user).first()
      if not check_bucketlist_name:
          try:
            bucketlist.name = name
            db.session.commit()
            return messages["bucketlist_updated"], 201
          except:
            return messages["bucketlist_not_updated"]
      else:
        return messages["bucketlist_exist"]

    @auth.user_is_login
    @auth.bucketlist_exist
    def delete(self, id):
        try:          
            bucketlist = BucketList.query.filter_by(id=id).first()
            db.session.delete(bucketlist)
            db.session.commit()
            return messages["bucketlist_deleted"]
        except:
            return messages["bucketlist_not_deleted"]



class AllBucketLists(Resource):
    @auth.user_is_login
    def get(self):
        token = request.headers.get('Token')
        user_id = get_current_user_id(token)
        all_bucketlist = BucketList.query.filter_by(
        created_by=user_id).all()
        if all_bucketlist:
            final_output = [{"id": bucketlist.id,
                           "name": bucketlist.name,
                           "date_created": bucketlist.date_created,
                           "date_modified": bucketlist.date_modified,
                           "items": [],  # get_all_bucketlist_item(bucketlist.id),
                           "created_by": bucketlist.created_by} for bucketlist in all_bucketlist]
            return jsonify({"data": final_output})    
        else:
            return messages["no_bucketlist"]

    @auth.user_is_login
    def post(self):
        name = request.form.get("name")
        token = request.headers.get('Token')
        current_user = get_current_user_id(token)
        bucketlist = BucketList.query.filter_by(
            name=name, created_by=current_user).first()
        if name:
            if bucketlist:
                return messages["bucketlist_exist"]
            else:
                bucketlist = BucketList(name, current_user)
                return jsonify({"message": "Saved",
                                "name": name,
                                "created_by": current_user
                                }) if bucketlist.save() \
                    else messages["bucketlist_not_saved"]
        else:
            return messages["no_bucketlist_name"]

class AllBucketListItems(Resource):
    @auth.user_is_login
    @auth.bucketlist_exist
    def get(self, id):
      return "Viewing all items on bucketlist {}".format(id)

    @auth.user_is_login
    @auth.bucketlist_exist
    def post(self, id):
      return "post item on bucketlist {}".format(id)





