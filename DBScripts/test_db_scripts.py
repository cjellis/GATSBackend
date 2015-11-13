import sys
sys.path.append('..')

import unittest
import app
import json
from DBScripts import SetUpDb, ClearMongo


class DBTestCase(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        ClearMongo.clear_mongo()
        self.app = app.app.test_client()

    def test_clear_mongo(self):
        rv = self.app.get('/dimensions/getDimensions')
        obj = json.loads(rv.data)
        assert len(obj["dimensions"]) is 0

        rv = self.app.get('/skills/getSkills')
        obj = json.loads(rv.data)
        assert len(obj["skills"]) is 0

        rv = self.app.post('/administrator/addDimension',
                           data=json.dumps(dict(name="TestDimension")),
                           content_type='application/json')

        rv = self.app.get('/dimensions/getDimensions')
        assert "TestDimension" in rv.data
        obj = json.loads(rv.data)
        assert len(obj["dimensions"]) is 1

        rv = self.app.post('/administrator/addDimension',
                           data=json.dumps(dict(name="TestDimension")),
                           content_type='application/json')

        rv = self.app.post('/administrator/addSkill',
                           data=json.dumps(dict(name="TestSkill",
                                                dimensions=['TestDimension'])),
                           content_type='application/json')

        rv = self.app.get('/skills/getSkills')
        assert "TestSkill" in rv.data
        obj = json.loads(rv.data)
        assert len(obj["skills"]) is 1

        ClearMongo.clear_mongo()

        rv = self.app.get('/dimensions/getDimensions')
        obj = json.loads(rv.data)
        assert len(obj["dimensions"]) is 0

        rv = self.app.get('/skills/getSkills')
        obj = json.loads(rv.data)
        assert len(obj["skills"]) is 0

    def test_add_data(self):
        SetUpDb.add_data()
        rv = self.app.get('/dimensions/getDimensions')
        obj = json.loads(rv.data)
        assert len(obj["dimensions"]) is 5

        rv = self.app.get('/skills/getSkills')
        obj = json.loads(rv.data)
        assert len(obj["skills"]) is 8


