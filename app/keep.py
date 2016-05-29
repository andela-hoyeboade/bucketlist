"""
@app.route("/", methods=["GET"])
def hello_world(): 
    return 'Hello World! Welcome to BucketList Manager. Please login/register to access our services'
    
@app.route("/auth/register", methods=["POST"])
def register():
        '''Returns a message for a POST request to register a
         new user.
        '''
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            if username and password:
                return auth.register(username, password)
            else:
                return jsonify({ "message": "Username or Password cannot be blank"})
        else:
            return jsonify({"message": "Methods not allowed"})


@app.route("/auth/login", methods=["POST"])
def login():
    '''A valid POST request login a user and returns a token in
       the JSON response returned.
    '''
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            return auth.login(username, password)
        else:
            return jsonify({"message": "Username or Password cannot be blank"})
    else:
       return jsonify({ "message": "Methods not allowed"})


@app.route('/bucketlists/<int:id>', methods=['GET','PUT','DELETE'])
@auth.user_is_login
@auth.bucketlist_exist
@auth.belongs_to_user
def manage_single_bucketlist(id):
    if request.method == 'GET':
        response = {"data": auth.get_single_bucketlist(id)}
        print(response)
        return jsonify(response)
    elif request.method == 'PUT':
        name = request.form.get("name")
        if name:
            return auth.update_bucketlist(id,name)
        else:
            return jsonify({"message": "Please supply bucketlist name"})
    elif request.method == 'DELETE':
        return auth.delete_bucket_list(id)
    else:
        return 'Method not allowed'

@app.route('/bucketlists/', methods=['GET','POST'])
@auth.user_is_login
def manage_bucketlist():
    token = request.headers.get('Token')
    user_id = auth.get_current_user_id(token)
    name = request.form.get("name")
    if token:
        if request.method == 'GET':
            response = auth.get_all_bucketlist(user_id)
            
            return jsonify(response)
        elif request.method == 'POST':
            if name:
                return auth.create_bucketlist(name=name,created_by=user_id)
            else:
                return jsonify({"message": "Please supply bucketlist name"})
        else:
             return 'Methods not allowed'
    else:
        return jsonify({"message": "Please supply token in the headers field with the key Token"})

@app.route('/bucketlists/<int:id>/items/', methods=['POST'])
@auth.user_is_login
@auth.bucketlist_exist
@auth.belongs_to_user
def create_bucketlist_item(id):
    name = request.form.get("name")
    done = request.form.get("done")
    if name:
        return auth.create_bucketlist_item(id,name,done=False)
    else:
        return jsonify({"message": "Please specify item name"})
@app.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['PUT','DELETE'])
def manage_bucketlist_item(id,item_id):
    if request.method == 'PUT':
        return 'You are updating item %s in bucketlist %s.' % (item_id,id)
    elif request.method == 'DELETE':
        return 'You are deleting item %s in bucketlists %s'  % (item_id,id)
    else:
        return 'Methods not allowed'

@app.errorhandler(404)
def handle_error(message):
    return jsonify({"message":"Cannot locate item"})
"""
