"""Module containing authentication routes."""
from app.models import User
from flask.views import MethodView
from flask import make_response, request, jsonify
from . import auth_blueprint


class RegistrationView(MethodView):
    """Class containing user registration methods."""
    def post(self):
        """method for registering users."""
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


class LoginView(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        """Handle POST request for this view. Url ---> /auth/login"""
        try:
            # Get the user object using their email (unique to every user)
            user = User.query.filter_by(email=request.data['email']).first()

            # Try to authenticate the found user using their password
            if user and user.password_is_valid(request.data['password']):
                # Generate the access token. This will be used as the authorization header
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                # User does not exist. Therefore, we return an error message
                response = {
                    'message': 'Invalid email or password, Please try again'
                }
                return make_response(jsonify(response)), 401

        except Exception as e:
            # Create a response containing an string error message
            response = {
                'message': str(e)
            }
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            return make_response(jsonify(response)), 500


class LogoutView(MethodView):
    """This class-based view handles user logout"""

    def get(self):
        try:
            response = {
                'message': 'You logged out successfully.',
                'access_token': None
            }
            return make_response(jsonify(response)), 200
        except Exception as e:
            # An error occured, therefore return a string message containing the error
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 401


class PasswordresetView(MethodView):
    """Method to reset the user password."""
    def post(self):
        user = User.query.filter_by(email=request.data['email']).first()
        if user:
            email = request.data['email']
            password = str(request.data['password'])
            user.update_password(password)
            response = {
                "message": "User password was successfully reset.",
                "email": email
            }
            return make_response(jsonify(response)), 201
        else:
            response = {
                "message": "The account whose password you are trying to reset doesnt exist."
            }
            return make_response(jsonify(response)), 201


# Define the API resource
registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')
logout_view = LogoutView.as_view('logout_view')
passwordreset_view = PasswordresetView.as_view('passwordreset_view')

# Define the rule for the registration url --->  /auth/register
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])

# Define the rule for the registration url --->  /auth/login
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)

# Define the rule for the registration url --->  /auth/login
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['GET']
)

# Define the rule for the registration url --->  /auth/login
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/reset-password',
    view_func=passwordreset_view,
    methods=['POST']
)
