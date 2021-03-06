"""Module that contains routes for bucket lists and bucket list items."""
from flask import request, jsonify, abort, make_response
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    """Method containing the bucket list routes."""
    from app.models import Bucketlist, User, BucketlistItem
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config['testing'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/bucketlists/', methods=['GET', 'POST'])
    def bucketlists():
        """method for retrieving and creating bucket lists."""
        access_token = request.headers.get("Authorization")
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                if request.method == 'POST':
                    name = str(request.data.get('name', ''))
                    u_id = user_id
                    if name:
                        bucketlist = Bucketlist(name=name, user_id=u_id)
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
        response = {
            "message": "Please login first."
        }
        response.status_code = 403
        return jsonify(response)

    @app.route('/bucketlists/page=1', methods=['GET'])
    def bucketlists_list():
        """Method for returning paginated bucket lists."""
        page = int(request.args['page'])
        limit = int(request.args['limit'])
        bucket_lists = Bucketlist.query.filter_by().paginate(page, limit, False).items
        results = []
        for bucketlist in bucket_lists:
            list_of_buckets = {}
            list_of_buckets['id']: bucketlist.id
            list_of_buckets['name']: bucketlist.name
            results.append(list_of_buckets)

        base_url = '/bucketlists/'
        if page <= 1:
            prev_url = ""
        else:
            page_value = page - 1
            prev_url = base_url + '?limit={}&page={}'.format(limit, page_value)
        next_url = base_url + '?limit={}&page={}'.format(limit, page + 1)

        urls = {
            'prev_url': prev_url,
            'next_url': next_url
        }

        response = jsonify(urls, results)
        response.status_code = 200
        return response

    @app.route('/bucketlists/<int:bucket_id>', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist_manipulation(bucket_id):
        """Method for retrieving bucket list by id."""
        access_token = request.headers.get('Authorization')
        if access_token:
            user_id = User.decode_token(access_token)
            if not access_token:
                response = {
                    "message": "Please login first."
                }
                response.status_code = 403
                return jsonify(response)
            if not isinstance(user_id, str):
                bucketlist = Bucketlist.query.filter_by(id=bucket_id).first()
                if not bucketlist:
                    abort(404)
                elif request.method == 'DELETE':
                    bucketlist.delete()
                    return {"message": "bucketlist"
                                       " {} deleted successfully".format(bucketlist.name)}, 200
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
            return {"message": "Please login first."}
        return {
            "message": "Please login first."
        }

    @app.route('/bucketlists/<int:id>/items', methods=['GET', 'POST'])
    def bucketlistitem(id):
        """Method for creating and retrieving bucket list items."""
        access_token = request.headers.get('Authorization')
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                bucketlist = Bucketlist.query.filter_by(id=id).first()
                if not bucketlist:
                    return {"message": "No bucket lists exists please create some."}
                if request.method == 'POST':
                    name = str(request.data.get('name', ''))
                    if name:
                        bucketlistitem = BucketlistItem(item_name=name, bucketlist_id=id)
                        bucketlistitem.save()
                        response = jsonify({
                            'id': bucketlistitem.id,
                            'name': bucketlistitem.item_name,
                            'bucketlist_id': bucketlistitem.bucketlist_id
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
        return {
            "message": "Please login first."
        }

    @app.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
    def bucketlistitem_manipulation(id, item_id):
        """method for editing, deleting, and retriving bucket list item."""
        access_token = request.headers.get('Authorization')
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                bucketlistitems = BucketlistItem.query.filter_by(bucketlist_id=item_id).first()
                if not bucketlistitems:
                    abort(404)
                if request.method == 'PUT':
                    name = str(request.data.get('name', ''))
                    completed = str(request.data.get('completed', ''))
                    bucketlistitems.name = name
                    bucketlistitems.completed = completed
                    bucketlistitems.save()
                    response = jsonify({
                        'id': bucketlistitems.id,
                        'name': bucketlistitems.name,
                        'completed': bucketlistitems.completed
                    })
                    response.status_code = 200
                    return response
                if request.method == 'DELETE':
                    bucketlistitems.delete()
                    return {
                        "message": "Bucketlist item deleted successfully"
                    }
        return {
            "message": "Please login first."
        }

    @app.route('/bucketlists/search', methods=['GET'])
    def application_search():
        """Method for searching bucket lists and bucket list items by name."""
        search_term = str(request.args.get('q', ''))
        #search name in bucketlist
        bucketlist_results = Bucketlist.query.filter(
            Bucketlist.name.like('%' + search_term + '%')).all()
        #search name in bucketlistitems
        item_results = BucketlistItem.query.filter(
            BucketlistItem.item_name.like('%' + search_term + '%')).all()
        matches = []
        for obj in bucketlist_results:
            bucketlist = {
                'id': obj.id,
                'name': obj.name
            }
            matches.append(bucketlist)

        for obj in item_results:
            items = {
                'id': obj.id,
                'name': obj.item_name,
                'completed': obj.completed

            }
            matches.append(items)

        return make_response(jsonify(matches)), 200

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app
