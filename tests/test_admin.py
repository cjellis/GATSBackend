import unittest
import app
import json
from pymongo import MongoClient


class AdminTestCase(unittest.TestCase):

    # runs before each test method
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

        self.app = app.app.test_client()

        test_user = {
                        "firstname": "John",
                        "lastname": "Smith",
                        "email": "smith.j@neu.edu",
                        "password": "password"
                    }
        rv = self.app.post('/users/addUser',
                       data=json.dumps(test_user),
                       content_type='application/json')
        self.token = json.loads(rv.data)['data']['user']['token']

    # tests adding a dimension
    def test_add_dimension(self):
        rv = self.app.post('/administrator/addDimension/{}'.format(self.token),
                           data=json.dumps(dict(name="TestDimension")),
                           content_type='application/json')
        assert "ERROR: You do not have permission to create a dimension" in rv.data

        rv = self.app.post('/administrator/addDimension/ADMIN_TOKEN',
                           data=json.dumps(dict(name="TestDimension")),
                           content_type='application/json')
        assert "Success" in rv.data

        rv = self.app.post('/administrator/addDimension/ADMIN_TOKEN',
                           data=json.dumps(dict(name="TestDimension")),
                           content_type='application/json')
        assert "Dimension already exists with given name" in rv.data

    # tests adding a skill
    def test_add_skill(self):
        rv = self.app.post('/administrator/addDimension/ADMIN_TOKEN',
                           data=json.dumps(dict(name="TestDimension")),
                           content_type='application/json')

        rv = self.app.post('/administrator/addSkill/{}'.format(self.token),
                           data=json.dumps(dict(name="TestDimension")),
                           content_type='application/json')
        assert "ERROR: You do not have permission to create a skill" in rv.data

        rv = self.app.post('/administrator/addSkill/ADMIN_TOKEN',
                           data=json.dumps(dict(name="TestSkill",
                                                dimensions=['TestDimension'])),
                           content_type='application/json')
        assert "Success" in rv.data

        rv = self.app.post('/administrator/addSkill/ADMIN_TOKEN',
                           data=json.dumps(dict(name="TestSkill",
                                                dimensions=['TestDimension'])),
                           content_type='application/json')
        assert "Skill already exists with given name" in rv.data

        rv = self.app.post('/administrator/addSkill/ADMIN_TOKEN',
                           data=json.dumps(dict(name="TestOtherSkill",
                                                dimensions=['FakeTestDimension'])),
                           content_type='application/json')
        assert "Dimension does not exist" in rv.data
