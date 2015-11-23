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

        self.app = app.app.test_client()

    def test_add_dimension(self):
        rv = self.app.post('/administrator/addDimension',
                           data=json.dumps(dict(name="TestDimension")),
                           content_type='application/json')
        assert "Success" in rv.data

        rv = self.app.post('/administrator/addDimension',
                           data=json.dumps(dict(name="TestDimension")),
                           content_type='application/json')
        assert "Dimension already exists with given name" in rv.data

    def test_add_skill(self):
        rv = self.app.post('/administrator/addDimension',
                           data=json.dumps(dict(name="TestDimension")),
                           content_type='application/json')

        rv = self.app.post('/administrator/addSkill',
                           data=json.dumps(dict(name="TestSkill",
                                                dimensions=['TestDimension'])),
                           content_type='application/json')
        assert "Success" in rv.data

        rv = self.app.post('/administrator/addSkill',
                           data=json.dumps(dict(name="TestSkill",
                                                dimensions=['TestDimension'])),
                           content_type='application/json')
        assert "Skill already exists with given name" in rv.data

        rv = self.app.post('/administrator/addSkill',
                           data=json.dumps(dict(name="TestOtherSkill",
                                                dimensions=['FakeTestDimension'])),
                           content_type='application/json')
        assert "Dimension does not exist" in rv.data

    def test_get_dimension(self):
        rv = self.app.post('/administrator/addDimension',
                           data=json.dumps(dict(name="TestDimension")),
                           content_type='application/json')

        rv = self.app.get('/dimensions/getDimensions')
        assert "TestDimension" in rv.data
        obj = json.loads(rv.data)
        assert len(obj["dimensions"]) is 1

    def test_get_skills(self):
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

    def test_add_event(self):
        test_user = {
                        "firstname": "John",
                        "lastname": "Smith",
                        "email": "smith.j@neu.edu",
                        "password": "password"
                    }
        rv = self.app.post('/users/addUser',
                       data=json.dumps(test_user),
                       content_type='application/json')

        token = json.loads(rv.data)['data']['user']['token']

        rv = self.app.post('/administrator/addDimension',
                           data=json.dumps(dict(name="TestDimension")),
                           content_type='application/json')

        rv = self.app.post('/administrator/addSkill',
                           data=json.dumps(dict(name="TestSkill",
                                                dimensions=['TestDimension'])),
                           content_type='application/json')

        rv = self.app.post('/events/addEvent/{}'.format(token),
                           data=json.dumps({
    "title": "Northeastern University Growth Opportunities for Asian American Leaders (NUGOAL)",
    "format": "Training and development program",
    "topics": ["Multicultural", "Leadership", "Community Engagement", "Exploring Identity"],
    "description": "Northeastern University Growth and Opportunity for"
                   " Asian American Leaders is a program specifically designed for first and second year "
                   "Asian American students who are looking to increase and gain experiences to empower themselves as"
                   " leaders at Northeastern University and beyond. A cohort of students will be chosen based on their "
                   "potential as future leaders and need for leadership development. This seven week program will focus"
                   " on the intersection of leadership and Asian American racial identity through discussions and"
                   " projects. It will be facilitated by current Asian American student leaders and AAC staff. Apply by"
                   " December 1, 2015.",
    "begin": "12/1/2015",
    "end": "3/1/2015",
    "engagementLengthValue": 1,
    "engagementLengthUnit": "Semester",
    "recurrence": "Yearly",
    "location": "Boston Campus",
    "sponsoringDepartment": "Asian American Center",
    "pointOfContact": {"name": "Kristine Din", "number": "6173735554", "email": "k.din@neu.edu"},
    "outcomes": ["Students will be able to define leadership in relationship to their own racial identity.",
                 "Students will be able to describe their leadership strengths.",
                 "Students will be able to employ their leadership style and strengths in their daily lives.",
                 "Students will be able to analyze leadership in the Asian American community.",
                 "Students will be able to propose a meaningful intervention for building Asian American leadership"
                 " capacity.",
                 "Students will be able to assess the need for leadership development within the Asian American"
                 " community at Northeastern."],
    "skills": ["TestSkill"],
    "engagementLevel": "Active",

    "coopFriendly": True,
    "academicStanding": ["First Year", "Second Year"],
    "major": "Any",
    "residentStatus": "both",
    "otherRequirements": ["Identify as Asian American"]
}), content_type='application/json')
        assert "Success" in rv.data

        rv = self.app.get('/events/getAllEvents')
        obj = json.loads(rv.data)
        assert len(obj["events"]) is 1

        rv = self.app.post('/events/addEvent/{}'.format(token),
                           data=json.dumps({
    "title": "Northeastern University Growth Opportunities for Asian American Leaders (NUGOAL)",
    "format": "Training and development program",
    "topics": ["Multicultural", "Leadership", "Community Engagement", "Exploring Identity"],
    "description": "Northeastern University Growth and Opportunity for"
                   " Asian American Leaders is a program specifically designed for first and second year "
                   "Asian American students who are looking to increase and gain experiences to empower themselves as"
                   " leaders at Northeastern University and beyond. A cohort of students will be chosen based on their "
                   "potential as future leaders and need for leadership development. This seven week program will focus"
                   " on the intersection of leadership and Asian American racial identity through discussions and"
                   " projects. It will be facilitated by current Asian American student leaders and AAC staff. Apply by"
                   " December 1, 2015.",
    "begin": "12/1/2015",
    "end": "3/2015",
    "engagementLengthValue": 1,
    "engagementLengthUnit": "Semester",
    "recurrence": "Yearly",
    "location": "Boston Campus",
    "sponsoringDepartment": "Asian American Center",
    "pointOfContact": {"name": "Kristine Din", "number": "617373555", "email": "k.din@ne.edu"},
    "outcomes": ["Students will be able to define leadership in relationship to their own racial identity.",
                 "Students will be able to describe their leadership strengths.",
                 "Students will be able to employ their leadership style and strengths in their daily lives.",
                 "Students will be able to analyze leadership in the Asian American community.",
                 "Students will be able to propose a meaningful intervention for building Asian American leadership"
                 " capacity.",
                 "Students will be able to assess the need for leadership development within the Asian American"
                 " community at Northeastern."],
    "skills": ["TestSkill", "OtherTestSkill"],
    "engagementLevel": "Active",

    "coopFriendly": True,
    "academicStanding": ["First Year", "Second Year"],
    "major": "Any",
    "residentStatus": "both",
    "otherRequirements": ["Identify as Asian American"]
}), content_type='application/json')
        assert "Date not in correct format" in rv.data
        assert "Skill does not exist" in rv.data
        assert "Event already exists with given title" in rv.data
        assert "Phone Number not long enough" in rv.data
        assert "Email is not an @neu email" in rv.data

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

    def test_event_attendance(self):
        test_user = {
                        "firstname": "John",
                        "lastname": "Smith",
                        "email": "smith.j@neu.edu",
                        "password": "password"
                    }
        rv = self.app.post('/users/addUser',
                       data=json.dumps(test_user),
                       content_type='application/json')
        token = json.loads(rv.data)['data']['user']['token']

        test_user = {
            "firstname": "John",
            "lastname": "Smith",
            "email": "smith.j2@husky.neu.edu",
            "password": "password",
            "year": "Sophomore",
            "major": "Psycology"
        }

        rv = self.app.post('/users/addUser',
                                 data=json.dumps(test_user),
                                 content_type='application/json')
        token_student = json.loads(rv.data)['data']['user']['token']

        rv = self.app.post('/administrator/addDimension',
                           data=json.dumps(dict(name="TestDimension")),
                           content_type='application/json')

        rv = self.app.post('/administrator/addSkill',
                           data=json.dumps(dict(name="TestSkill",
                                                dimensions=['TestDimension'])),
                           content_type='application/json')

        rv = self.app.post('/events/addEvent/{}'.format(token),
                           data=json.dumps({
    "title": "Northeastern University Growth Opportunities for Asian American Leaders (NUGOAL)",
    "format": "Training and development program",
    "topics": ["Multicultural", "Leadership", "Community Engagement", "Exploring Identity"],
    "description": "Northeastern University Growth and Opportunity for"
                   " Asian American Leaders is a program specifically designed for first and second year "
                   "Asian American students who are looking to increase and gain experiences to empower themselves as"
                   " leaders at Northeastern University and beyond. A cohort of students will be chosen based on their "
                   "potential as future leaders and need for leadership development. This seven week program will focus"
                   " on the intersection of leadership and Asian American racial identity through discussions and"
                   " projects. It will be facilitated by current Asian American student leaders and AAC staff. Apply by"
                   " December 1, 2015.",
    "begin": "12/1/2015",
    "end": "3/1/2015",
    "engagementLengthValue": 1,
    "engagementLengthUnit": "Semester",
    "recurrence": "Yearly",
    "location": "Boston Campus",
    "sponsoringDepartment": "Asian American Center",
    "pointOfContact": {"name": "Kristine Din", "number": "6173735554", "email": "k.din@neu.edu"},
    "outcomes": ["Students will be able to define leadership in relationship to their own racial identity.",
                 "Students will be able to describe their leadership strengths.",
                 "Students will be able to employ their leadership style and strengths in their daily lives.",
                 "Students will be able to analyze leadership in the Asian American community.",
                 "Students will be able to propose a meaningful intervention for building Asian American leadership"
                 " capacity.",
                 "Students will be able to assess the need for leadership development within the Asian American"
                 " community at Northeastern."],
    "skills": ["TestSkill"],
    "engagementLevel": "Active",

    "coopFriendly": True,
    "academicStanding": ["First Year", "Second Year"],
    "major": "Any",
    "residentStatus": "both",
    "otherRequirements": ["Identify as Asian American"]
}), content_type='application/json')
        assert "Success" in rv.data

        rv = self.app.get('/events/getAllEvents')
        obj = json.loads(rv.data)
        event_id = obj["events"][0]["id"]

        rv = self.app.post('/events/submitAttendance/{}/{}'.format(event_id, token_student))
        assert "Success" in rv.data

    def test_event_point_distribution(self):
        rv = self.app.post('/administrator/addDimension',
                           data=json.dumps(dict(name="TestDimension")),
                           content_type='application/json')

        rv = self.app.post('/administrator/addSkill',
                           data=json.dumps(dict(name="TestSkill",
                                                dimensions=['TestDimension'])),
                           content_type='application/json')

        test_user = {
                "firstname": "John",
                "lastname": "Smith",
                "email": "smith.j@neu.edu",
                "password": "password"
        }
        rv = self.app.post('/users/addUser',
                       data=json.dumps(test_user),
                       content_type='application/json')
        token = json.loads(rv.data)['data']['user']['token']

        rv = self.app.post('/events/addEvent/{}'.format(token),
                           data=json.dumps({
    "title": "Northeastern University Growth Opportunities for Asian American Leaders (NUGOAL)",
    "format": "Training and development program",
    "topics": ["Multicultural", "Leadership", "Community Engagement", "Exploring Identity"],
    "description": "Northeastern University Growth and Opportunity for"
                   " Asian American Leaders is a program specifically designed for first and second year "
                   "Asian American students who are looking to increase and gain experiences to empower themselves as"
                   " leaders at Northeastern University and beyond. A cohort of students will be chosen based on their "
                   "potential as future leaders and need for leadership development. This seven week program will focus"
                   " on the intersection of leadership and Asian American racial identity through discussions and"
                   " projects. It will be facilitated by current Asian American student leaders and AAC staff. Apply by"
                   " December 1, 2015.",
    "begin": "12/1/2015",
    "end": "3/1/2015",
    "engagementLengthValue": 1,
    "engagementLengthUnit": "Semester",
    "recurrence": "Yearly",
    "location": "Boston Campus",
    "sponsoringDepartment": "Asian American Center",
    "pointOfContact": {"name": "Kristine Din", "number": "6173735554", "email": "k.din@neu.edu"},
    "outcomes": ["Students will be able to define leadership in relationship to their own racial identity.",
                 "Students will be able to describe their leadership strengths.",
                 "Students will be able to employ their leadership style and strengths in their daily lives.",
                 "Students will be able to analyze leadership in the Asian American community.",
                 "Students will be able to propose a meaningful intervention for building Asian American leadership"
                 " capacity.",
                 "Students will be able to assess the need for leadership development within the Asian American"
                 " community at Northeastern."],
    "skills": ["TestSkill"],
    "engagementLevel": "Active",

    "coopFriendly": True,
    "academicStanding": ["First Year", "Second Year"],
    "major": "Any",
    "residentStatus": "both",
    "otherRequirements": ["Identify as Asian American"]
}), content_type='application/json')
        assert "Success" in rv.data

        rv = self.app.get('/events/getAllEvents')
        obj = json.loads(rv.data)
        event_id = obj["events"][0]["id"]


        test_user = {
            "firstname": "John",
            "lastname": "Smith",
            "email": "smith.j2@husky.neu.edu",
            "password": "password",
            "year": "Sophomore",
            "major": "Psycology"
        }

        rv = self.app.post('/users/addUser',
                                 data=json.dumps(test_user),
                                 content_type='application/json')
        resp = json.loads(rv.data)
        token_student = json.loads(rv.data)['data']['user']['token']

        other_test_user = {
                "firstname": "Jim",
                "lastname": "Doe",
                "email": "doe.j@neu.edu",
                "password": "password"
        }
        rv = self.app.post('/users/addUser',
                       data=json.dumps(other_test_user),
                       content_type='application/json')
        other_token = json.loads(rv.data)['data']['user']['token']

        rv = self.app.post('/events/overEvent/{}/{}'.format(event_id, other_token))
        assert "ERROR: Not the owner of this event" in rv.data

        rv = self.app.post('/events/closeEvent/{}/{}'.format(event_id, other_token))
        assert "ERROR: Not the owner of this event" in rv.data

        rv = self.app.post('/events/closeEvent/{}/{}'.format(event_id, token))
        assert "ERROR: Event not over" in rv.data

        rv = self.app.post('/events/overEvent/{}/{}'.format(event_id, token))
        assert "Success" in rv.data

        rv = self.app.post('/events/submitAttendance/{}/{}'.format(event_id, token_student))
        assert "Success" in rv.data

        rv = self.app.post('/events/closeEvent/{}/{}'.format(event_id, token))
        assert "Success" in rv.data

        rv = self.app.post('/events/overEvent/{}/{}'.format(event_id, token))
        assert "ERROR: Event not open, cannot be set to over" in rv.data

        rv = self.app.post('/events/distributePoints/{}/{}'.format(event_id, token_student))
        assert "ERROR: You do not have permission to alter an event" in rv.data

        rv = self.app.post('/events/overEvent/{}/{}'.format(event_id, token_student))
        assert "ERROR: You do not have permission to set an event to over" in rv.data

        rv = self.app.post('/events/closeEvent/{}/{}'.format(event_id, token_student))
        assert "ERROR: You do not have permission to close an event" in rv.data

        rv = self.app.post('/events/distributePoints/{}/{}'.format(event_id, token))
        assert "Success" in rv.data

        url = '/users/getUser/em/{0}/{1}'.format(test_user['email'],
                                            resp['data']['user']['token'])
        rv = self.app.get(url, data=json.dumps(test_user), content_type='application/json')
        data = json.loads(rv.data)
        dim = data['data']['dimensions']
        assert len(dim) == 1
        d = dim[0]
        assert d['dimension'] == 'TestDimension'
        assert d['value'] == 4
