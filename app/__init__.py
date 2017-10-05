from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import Bucketlist, User, BucketlistItem
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config['testing'])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/bucketlists/', methods=['GET', 'POST'])
    def bucketlists():
        #auth_header = request.headers.get('Authorization')
        #access_token = auth_header.split(" ")[1]
        #if access_token:
            #user_id = User.decode_token(access_token)
            #if not isinstance(user_id, str):
                if request.method == 'POST':
                    name = str(request.data.get('name', ''))
                    if name:
                        bucketlist = Bucketlist(name=name)
                        bucketlist.save()
                        response = jsonify({
                            'id': bucketlist.id,
                            'name': bucketlist.name
                        })
                        response.status_code = 201
                        return response
                else:
                    bucket_lists = Bucketlist.get_all()
                    results = []

                    for bucketlist in bucket_lists:
                        obj = {
                            'id': bucketlist.id,
                            'name': bucketlist.name,
                        }
                        results.append(obj)
                    response = jsonify(results)
                    response.status_code = 200
                    return response

    @app.route('/bucketlists/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
    def bucketlist_manipulation(id, **kwargs):
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            abort(404)
        if request.method == 'DELETE':
            bucketlist.delete()
            return {
                       "message": "bucketlist {} deleted successfully".format(bucketlist.id)
                   }, 200
        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            bucketlist.name = name
            bucketlist.save()
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name
            })
            response.status_code = 200
            return response

    @app.route('/bucketlists/<int:id>/items', methods=['GET', 'POST'])
    def bucketlistitem(id):
        #auth_header = request.headers.get('Authorization')
        #access_token = auth_header.split(" ")[1]
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        #if access_token:
            #user_id = User.decode_token(access_token)
            #f not isinstance(user_id, str):
        if not bucketlist:
            abort(404)
        if request.method == 'POST':
            name = str(request.data.get('name', ''))
            if name:
                bucketlistitem = BucketlistItem(
                    item_name=name)
                bucketlistitem.save()
                response = jsonify({
                    'id': bucketlistitem.id,
                    'name': bucketlistitem.item_name
                })
                response.status_code = 201
                return response
            if request.method == 'GET':
                bucketlistitems = BucketlistItem.query.filter_by(bucketlist_id=id).first()
                results = []
                for listitem in bucketlistitems:
                    obj = {
                        'id': listitem.id,
                        'name': listitem.item_name,
                        'status': listitem.completed
                    }
                    results.append(obj)
                response = jsonify(results)
                response.status_code = 200
                return response


    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app
