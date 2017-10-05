import unittest
import json
from app import create_app, db


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.user_data = {
            'email': 'brian@example.com',
            'password': 'password'
        }
        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_user_registration(self):
        res = self.client.post('/auth/register', data = self.user_data)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "You registered successfully.")
        self.assertEqual(res.status_code, 201)

    def test_registered_already(self):
        res = self.client.post('/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        second_res = self.client.post('/auth/register', data=self.user_data)
        self.assertEqual(second_res.status_code, 202)
        result = json.loads(second_res.data.decode())
        self.assertEqual(result['message'], "User already exists. Please login.")

    def test_user_login(self):
        res = self.client.post('/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client.post('/auth/login', data=self.user_data)
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "You logged in successfully.")
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(result['access_token'])
        #print(result['access_token'])

    def test_non_registered_user_login(self):
        """Test non registered users cannot login."""
        # define a dictionary to represent an unregistered user
        not_a_user = {
            'email': 'not_a_user@example.com',
            'password': 'nope'
        }
        # send a POST request to /auth/login with the data above
        res = self.client.post('/auth/login', data=not_a_user)
        # get the result in json
        result = json.loads(res.data.decode())

        # assert that this response must contain an error message
        # and an error status code 401(Unauthorized)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            result['message'], "Invalid email or password, Please try again")

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()

