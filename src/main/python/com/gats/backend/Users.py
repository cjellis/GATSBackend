import sys, json, datetime
from bson import json_util

'''
Student json model
{
	//required
	"name" : "Free Text",
	"email" : "Free Text", @husky.neu.edu
	"password" : "Free Text", //salted password hash
	
	//optional
	"year" : one of ["Freshman", "Sophomore", "Middler", "Junior", "Senior"],
	"major" : "Free Text",
	"onCoop" : boolean,

	//we set programmatically
	"skills" : [{'name' : Skill, 'value':int}],
	"dimensions" : [{'name' : Dimension, 'value':int}]
    
    //flask login info
    "authDate": null/datetime
    "isAuth": bool
}
'''

'''
Faculty json model
{
	//required
	"name" : "Free Text",
	"email" : "Free Text", //must be @northeastern.edu or @neu.edu
	"password" : "Free Text", //salted password hash
    "admin": int, //0 false, 1 true, leaving as an integer. we can add privlege levels that way

	//we set programatically
	"events" : [Event]
    
    //flask login info
    "authDate": null/datetime //most reacent date user was auuthenticated on
    "isAuth": bool
    
}'''

class User:
    def __init__(self, data):
        self.name = data["name"]
        self.email = data["email"]
        self.password = data["password"]
        self.authDate = data["authDate"]
        self._id = data["_id"]
       
    #flask-login required defs
    def is_athenticated(self):
        return self.authDate != None
    
    def is_active(self):
        return self.is_athenticated()
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self._id;
    
class Student(User):
    def __init__(self, jsonData):
        data = json.loads(data)
        super(User, self).__init__(jsonData)
        self.year = data["year"]
        self.major = data["major"]
        self.onCoop = data["onCoop"]
        self.skills = data["skills"]
        self.dimensions = data["dimensions"]

    
class Faculty(User):
    def __init__(self, jsonData):
        data = json.loads(jsonData)
        super(User, self).__init__(data)
        self.admin = data["admin"]
        self.events = data["events"]
        
        
    

        
        
        