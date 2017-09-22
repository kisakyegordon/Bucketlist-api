from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import Bucketlist
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config['testing'])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/bucketlists/', methods=['GET', 'POST'])
    def bucketlists():
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
    return app
