"""Module to test creation of bucket list and bucket list items."""
import unittest
import json
from app import create_app, db


class BucketlistTestCase(unittest.TestCase):
    """Class containing bucket list test cases"""
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.bucketlist = {'name': 'Go to Borabora for vacation'}
        self.bucketlist2 = {'name': 'Go to Borabora for vacation to kenya'}
        self.bucketlist3 = {'name': 'Go to Borabora for vacation to mexico'}
        self.bucketlistitem = {'name': 'Go rafting.'}
        self.new_bucketlist_item = {
            'name':'Go to the GP Kart',
            'completed': True
        }
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
        """This method tests if a user can create a bucktelist."""
        self.register_user()
        result = self.login_user()
        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client.post(
            '/bucketlists/', headers=dict(Authorization=access_token),
            data=self.bucketlist)
        self.assertEqual(res.status_code, 201, msg="The status code is wrong.")
        self.assertIn('Go to Borabora', str(res.data))

    def test_bucketlists_retrieval(self):
        """Method to test if one can retrieve all bucket lists."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client.post('/bucketlists/',
                               headers=dict(Authorization=access_token),
                               data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        res = self.client.get('/bucketlists/', headers=dict(Authorization=access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to Borabora', str(res.data))

    def test_bucketlists_pagination(self):
        """Method to test if one can retrieve all bucket lists with pagination."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client.post('/bucketlists/',
                               headers=dict(Authorization=access_token),
                               data=self.bucketlist)
        res1 = self.client.post('/bucketlists/',
                                headers=dict(Authorization=access_token),
                                data=self.bucketlist2)
        res2 = self.client.post('/bucketlists/',
                                headers=dict(Authorization=access_token),
                                data=self.bucketlist3)
        result = self.client.get('/bucketlists/?limit=1&page=1', headers=dict(Authorization=access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('next_url', str(result.data))
        print(result)
        #self.assertIsNone(result.urls)

    def test_bucketlist_deletion(self):
        """Method to test if one can delete a bucket list."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client.post(
            '/bucketlists/',
            headers=dict(Authorization=access_token),
            data={'name': 'Eat, pray and love'})
        self.assertEqual(res.status_code, 201)
        res1 = self.client.delete('/bucketlists/1', headers=dict(Authorization=access_token))
        self.assertEqual(res1.status_code, 200)
        result = self.client.get('/bucketlists/1', headers=dict(Authorization=access_token))
        self.assertEqual(result.status_code, 404)


    def test_bucketlist_can_be_edited(self):
        """method to test if one can edit a bucket list."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client.post(
            '/bucketlists/',
            headers=dict(Authorization=access_token),
            data={'name': 'Eat, pray and love'})
        self.assertEqual(res.status_code, 201)
        res = self.client.put(
            '/bucketlists/1',
            headers=dict(Authorization=access_token),
            data={
                "name": "Dont just eat, but also pray and love :-)"
            })
        self.assertEqual(res.status_code, 200)
        results = self.client.get('/bucketlists/1', headers=dict(Authorization=access_token))
        self.assertIn('Dont just eat', str(results.data)) #check if string is in the result data

    def test_bucketlist_by_id(self):
        """Method to test if one can retrieve a bucket list by id"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client.post('/bucketlists/',
                               headers=dict(Authorization=access_token),
                               data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        result = self.client.get(
            '/bucketlists/{}'.format(result_in_json['id']),
            headers=dict(Authorization=access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go to Borabora', str(result.data))


    def test_bucketlistitem_creation(self):
        """Method to test if one can create a bucket list item."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client.post('/bucketlists/',
                               headers=dict(Authorization=access_token),
                               data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        result1 = self.client.post(
            '/bucketlists/{}/items'.format(result_in_json['id']),
            headers=dict(Authorization=access_token),
            data=self.bucketlistitem)
        self.assertEqual(result1.status_code, 201)

    def test_bucketlistitem_edit(self):
        """Method to test if one can edit a bucket list item."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client.post('/bucketlists/',
                               headers=dict(Authorization=access_token),
                               data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        #create bucketlist item
        result1 = self.client.post(
            '/bucketlists/{}/items'.format(result_in_json['id']),
            headers=dict(Authorization=access_token),
            data=self.bucketlistitem)
        self.assertEqual(result1.status_code, 201)

        #now edit the item name and the completion
        item_res_in_json = json.loads(result1.data.decode('utf-8').replace("'", "\""))
        edit_item = self.client.put(
            '/bucketlists/{}/items/{}'.format(result_in_json['id'], item_res_in_json['id']),
            headers=dict(Authorization=access_token),
            data=self.new_bucketlist_item)
        self.assertEqual(edit_item.status_code, 200)
        self.assertIn('GP Kart', str(edit_item.data))

    def test_item_delete(self):
        """Method to test if one can delete a bucket list item."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        # create bucketlist
        res = self.client.post('/bucketlists/',
                               headers=dict(Authorization=access_token),
                               data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        # create bucketlist item
        result1 = self.client.post(
            '/bucketlists/{}/items'.format(result_in_json['id']),
            headers=dict(Authorization=access_token),
            data=self.bucketlistitem)
        self.assertEqual(result1.status_code, 201)
        res1 = self.client.delete('/bucketlists/1/items/1',
                                  headers=dict(Authorization=access_token))
        self.assertEqual(res1.status_code, 200)

    def test_app_name_search(self):
        """Method for testing if one can search by name."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        # create bucketlist
        res = self.client.post('/bucketlists/',
                               headers=dict(Authorization=access_token),
                               data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))

        # create bucketlist item
        result1 = self.client.post(
            '/bucketlists/{}/items'.format(result_in_json['id']),
            headers=dict(Authorization=access_token),
            data=self.bucketlistitem)
        search_term = 'Go'
        # search bucketlist item
        result1 = self.client.get(
            '/bucketlists/search',
            headers=dict(Authorization=access_token),
            data=search_term)
        #print(result1.data)
        self.assertEqual(result1.status_code, 200)
        self.assertIn('Go', str(result1 .data))

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
