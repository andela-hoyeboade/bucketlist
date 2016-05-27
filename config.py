import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'bucketlist.sqlite')
AVAILABLE_ENDPOINTS = [
        ("POST /auth/login/", {"PUBLIC_ACCESS": True}),
        ("GET /auth/logout/", {"PUBLIC_ACCESS": False}),
        ("POST /bucketlists/", {"PUBLIC_ACCESS": False}),
        ("GET /bucketlists/", {"PUBLIC_ACCESS": False}),
        ("GET /bucketlists/<id>/", {"PUBLIC_ACCESS": False}),
        ("PUT /bucketlists/<id>/", {"PUBLIC_ACCESS": False}),
        ("DELETE /bucketlists/<id>/", {"PUBLIC_ACCESS": False}),
        ("POST /bucketlists/<id>/items/", {"PUBLIC_ACCESS": False}),
        ("PUT /bucketlists/<id>/items/<item_id>", {"PUBLIC_ACCESS": False}),
        ("DELETE /bucketlists/<id>/items/<item_id>", {"PUBLIC_ACCESS": False}),
    ]
SECRET_KEY = 'secret'
#SQLALCHEMY_TRACK_MODIFICATIONS = False
#SQLALCHEMY_DATABASE_URI = 'postgresql://sunday:@localhost/bucketlist'
#SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')