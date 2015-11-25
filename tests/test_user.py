import unittest
import app
import json
from pymongo import MongoClient


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        client = MongoClient("mongodb://admin:admin@ds049864.mongolab.com:49864/activitytracker")
        db = client.activitytracker
        event_collection = db.Events
        skill_collection = db.Skills
        dimension_collection = db.Dimensions
        user_collection = db.Users

        event_collection.remove({})
        skill_collection.remove({})
        dimension_collection.remove({})
        user_collection.remove({})

        user_collection.insert_one({
            'firstname': 'Admin',
            'lastname': 'Admin',
            'email': 'admin@neu.edu',
            'password': 'P@$$w0rD',
            'token': 'ADMIN_TOKEN',
            'tokenTTL': 1000,
            'is_auth': True,
            'events': [],
            'roles': ['administrator', 'faculty', 'superuser'],
            'year': None,
            'major': None,
            'skills': [],
            'dimensions': []
        })

        self.app = app.app.test_client()

    def test_add_user(self):
        test_user = {
                        "firstname": "John",
                        "lastname": "Smith",
                        "email": "smith.j@husky.neu.edu",
                        "password": "password",
                        "year": "Sophomore",
                        "major": "Psycology"
                    }
        rv = self.app.post('/users/addUser',
                       data=json.dumps(test_user),
                       content_type='application/json')
        data = json.loads(rv.data)
        assert data['response']['code'] == 200
        assert "Success" in data['response']['msg']

        rv = self.app.post('/users/addUser',
                       data=json.dumps(test_user),
                       content_type='application/json')
        data = json.loads(rv.data)
        assert "is not unique" in data['data']['email']

    def test_get_user(self):
        test_user = {
            "firstname": "John",
            "lastname": "Smith",
            "email": "smith.j2@husky.neu.edu",
            "password": "password",
            "year": "Sophomore",
            "major": "Psycology"
        }

        response = self.app.post('/users/addUser',
                       data=json.dumps(test_user),
                       content_type='application/json')
        resp = json.loads(response.data)
        url = '/users/getUser/em/{0}/{1}'.format(test_user['email'],
                                            resp['data']['user']['token'])
        rv = self.app.get(url, data=json.dumps(test_user), content_type='application/json')
        data = json.loads(rv.data)
        assert data['response']['code'] is 200
        assert data['data']['email'] == test_user['email']

        other_test_user = {
            "firstname": "John",
            "lastname": "Smith",
            "email": "smith.j@neu.edu",
            "password": "password"
        }
        rv = self.app.post('/users/addUser',
                       data=json.dumps(other_test_user),
                       content_type='application/json')
        token = json.loads(rv.data)['data']['user']['token']

        url = '/users/getUser/em/{0}/{1}'.format(test_user['email'],
                                            token)
        rv = self.app.get(url, data=json.dumps(test_user), content_type='application/json')
        data = json.loads(rv.data)
        assert 'permission denied' in data['data']['error']