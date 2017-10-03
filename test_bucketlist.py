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



    def test_bucketlist_creation(self):
        res = self.client.post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(res.status_code, 201, msg="The status code is wrong.")
        self.assertIn('Go to Borabora', str(res.data))

    def test_api_can_get_all_bucketlists(self):
        res = self.client.post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        res = self.client.get('/bucketlists/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to Borabora', str(res.data))

    def test_api_can_get_bucketlist_by_id(self):
        rv = self.client.post('/bucketlists/', data=self.bucketlist)
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
