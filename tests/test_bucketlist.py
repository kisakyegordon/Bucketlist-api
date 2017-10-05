import unittest
import os
import json
from app import create_app, db


class BucketlistTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.bucketlist = {'name': 'Go to Borabora for vacation'}
        with self.app.app_context():
            db.create_all()

    def register_user(self, email="user@test.com", password="test1234"):
        """This helper method helps register a test user."""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client.post('/auth/register', data=user_data)

    def login_user(self, email="user@test.com", password="test1234"):
        """This helper method helps log in a test user."""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client.post('/auth/login', data=user_data)

    def test_bucketlist_creation(self):
        self.register_user()
        result = self.login_user()
        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client.post(
            '/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        #res = self.client.post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(res.status_code, 201, msg="The status code is wrong.")
        self.assertIn('Go to Borabora', str(res.data))

    def test_api_can_get_all_bucketlists(self):
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client.post('/bucketlists/',
                               headers=dict(Authorization="Bearer " + access_token),
                                            data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        res = self.client.get('/bucketlists/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to Borabora', str(res.data))

    def test_bucketlist_deletion(self):
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        rv = self.client.post(
            '/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Eat, pray and love'})
        self.assertEqual(rv.status_code, 201)
        res = self.client.delete('/bucketlists/1')
        self.assertEqual(res.status_code, 200)
        result = self.client.get('/bucketlists/1')
        self.assertEqual(result.status_code, 404)

    def test_bucketlist_can_be_edited(self):
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        rv = self.client.post(
            '/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Eat, pray and love'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client.put(
            '/bucketlists/1',
            data={
                "name": "Dont just eat, but also pray and love :-)"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client.get('/bucketlists/1')
        self.assertIn('Dont just eat', str(results.data))

    def test_api_can_get_bucketlist_by_id(self):
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        rv = self.client.post('/bucketlists/',
                              headers=dict(Authorization="Bearer " + access_token),
                              data=self.bucketlist)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client.get(
            '/bucketlists/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go to Borabora', str(result.data))

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
