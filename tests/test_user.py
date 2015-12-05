import unittest
import app
import json
from pymongo import MongoClient


class AppTestCase(unittest.TestCase):

    # runs before each test
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
            'roles': ['admin', 'faculty', 'superuser'],
            'year': None,
            'major': None,
            'skills': [],
            'dimensions': []
        })

        user_collection.insert_one({
            'firstname': 'Joe',
            'lastname': 'Sixpack',
            'email': 'sixpack.j@neu.edu',
            'password': 'P@$$w0rD',
            'token': 'SUPER_SPECIAL_TOKEN',
            'tokenTTL': 1000,
            'is_auth': True,
            'events': [],
            'roles': ['student'],
            'year': 'Sophomore',
            'major': 'Jobless',
            'skills': [],
            'dimensions': []
        })
        
        self.app = app.app.test_client()

    # tests adding a user to the system
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

    # tests getting a user from the system
    def test_get_user(self):
        test_user = {
            "firstname": "John",
            "lastname": "Smith",
            "email": "smith.j@husky.neu.edu",
            "password": "password",
            "year": "Sophomore",
            "major": "Psycology"
        }

        response = self.app.post('/users/addUser',
                       data=json.dumps(test_user),
                       content_type='application/json')
        resp = json.loads(response.data)
        student_token = resp['data']['user']['token']
        url = '/users/getUser/tk/{0}/{1}'.format(test_user['email'], student_token)
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

        url = '/users/getUser/tk/{0}/{1}'.format(test_user['email'],
                                            student_token)
        rv = self.app.get(url, data=json.dumps(test_user), content_type='application/json')
        data = json.loads(rv.data)
        assert data['response']['code'] is 200

        assert data['data']['email'] == test_user['email']
        
        url = '/users/getUser/pw/{0}/{1}'.format(test_user['email'],
                                            'password')
        rv = self.app.get(url, data=json.dumps(test_user), content_type='application/json')
        data = json.loads(rv.data)
        assert data['response']['code'] is 200
        assert data['data']['email'] == test_user['email']
            
        url = '/users/getUser/tk/{0}/{1}'.format(test_user['email'],
                                    'SUPER_SPECIAL_TOKEN')
        rv = self.app.get(url, data=json.dumps(test_user), content_type='application/json')
        data = json.loads(rv.data)
        assert 'permission denied' in data['data']['error']