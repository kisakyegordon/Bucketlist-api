import unittest
import os
import json
from app import create_app, db

class BucketlistTestCase(unittest.TestCase):

    def setup(self):
        self.app = create_app(config_name='testing')
        self.bucketlist = {'name': 'Go to Borabora for vacation'}
        with self.app.app_context():
            db.create_all()
            self.client = self.app.test_client()

    def test_bucketlist_creation(self):
        res = self.client.post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(res.status_code, 201, msg="The status code is wrong.")
        self.assertIn('Go to Borabora', str(res.data))

if __name__ == "__main__":
    unittest.main()
