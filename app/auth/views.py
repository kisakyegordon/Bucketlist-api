from . import auth_blueprint
from flask import make_response, request, jsonify
from app.models import User
from flask.views import MethodView


class RegistrationView(MethodView):

    def post(self):
        user = User.query.filter_by(email=request.data['email']).first()
        if not user:
            try:
                post_data = request.data
                # Register the user
                email = post_data['email']
                password = post_data['password']
                user = User(email=email, password=password)
                #request.post("/auth/register", data={'email': email, 'password': password})
                user.save()


                response = {
                    'message': 'You registered successfully.'
                }
                return make_response(jsonify(response)), 201

            except Exception as e:
                # An error occured, therefore return a string message containing the error
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'message': 'User already exists. Please login.'
            }
            return make_response(jsonify(response)), 202

registration_view = RegistrationView.as_view('register_view')
# Define the rule for the registration url --->  /auth/register
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])