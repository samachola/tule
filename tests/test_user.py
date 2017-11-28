import unittest
import os
import json
from app import create_app, db

class UserTestCase(unittest.TestCase):
    """This class represents the users test case."""
    def setUp(self):
        """Define test variables and initialize the app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.user = {'email': 'sam.achola@live.com', 'name': 'Sam Achola', 'role': 'customer', 'password': 'Ongorotiaf'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_user_creation(self):
        """Test that the API can post a user."""
        res = self.client.post('/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Sam Achola', str(res.data))

    def test_get_users(self):
        """ Test API can get all registered users."""
        res = self.client.post('/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        res = self.client.get('/users')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Sam Achola', str(res.data))

    def test_get_user_by_id(self):
       """ Test API can get single user by id."""
       rv = self.client.post('/auth/register', data=self.user)
       self.assertEqual(rv.status_code, 201)
       result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
       result = self.client.get('/users/{}'.format(result_in_json['id']))
       self.assertEqual(result.status_code, 200)
       self.assertIn('Sam Achola', str(result.data))

    def test_edit_user(self):
        """Test API can edit user."""
        rv = self.client.post('/auth/register', data=self.user)
        self.assertEqual(rv.status_code, 201)
        rv = self.client.put('users/1', data={'name': 'Edited User', 'email': 'sam.achola@live.com', 'role': 'partner'})
        self.assertEqual(rv.status_code, 200)
        results = self.client.get('/users/1')
        self.assertIn('Edited User', str(results.data))

    def tearDown(self):
        """Tear down all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    if __name__ == '__main__':
        unittest.main()