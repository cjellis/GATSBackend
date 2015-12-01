import unittest
import app
import json
from pymongo import MongoClient
from DBScripts import SetUpDb, ClearMongo


class DBTestCase(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        ClearMongo.clear_mongo()
        self.app = app.app.test_client()

    def test_clear_mongo(self):
        client = MongoClient("mongodb://admin:admin@ds049864.mongolab.com:49864/activitytracker")
        db = client.activitytracker
        user_collection = db.Users
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

        rv = self.app.get('/dimensions/getDimensions')
        obj = json.loads(rv.data)
        assert len(obj["data"]) is 0

        rv = self.app.get('/skills/getSkills')
        obj = json.loads(rv.data)
        assert len(obj["data"]) is 0

        rv = self.app.post('/administrator/addDimension/ADMIN_TOKEN',
                           data=json.dumps(dict(name="TestDimension")),
                           content_type='application/json')

        rv = self.app.get('/dimensions/getDimensions')
        assert "TestDimension" in rv.data
        obj = json.loads(rv.data)
        assert len(obj["data"]) is 1

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

        ClearMongo.clear_mongo()

        rv = self.app.get('/dimensions/getDimensions')
        obj = json.loads(rv.data)
        assert len(obj["data"]) is 0

        rv = self.app.get('/skills/getSkills')
        obj = json.loads(rv.data)
        assert len(obj["data"]) is 0

    def test_add_data(self):
        SetUpDb.add_data()
        rv = self.app.get('/dimensions/getDimensions')
        obj = json.loads(rv.data)
        assert len(obj["data"]) is 5

        rv = self.app.get('/skills/getSkills')
        obj = json.loads(rv.data)
        assert len(obj["data"]) is 8


