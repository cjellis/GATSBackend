import unittest
import app
import json
from pymongo import MongoClient


class SkillsTestCase(unittest.TestCase):

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

    def test_get_skills(self):
        rv = self.app.post('/administrator/addDimension/ADMIN_TOKEN',
                           data=json.dumps(dict(name="TestDimension")),
                           content_type='application/json')

        rv = self.app.post('/administrator/addSkill/ADMIN_TOKEN',
                           data=json.dumps(dict(name="TestSkill",
                                                dimensions=['TestDimension'])),
                           content_type='application/json')

        rv = self.app.get('/skills/getSkills')
        assert "TestSkill" in rv.data
        obj = json.loads(rv.data)
        assert len(obj["data"]) is 1
