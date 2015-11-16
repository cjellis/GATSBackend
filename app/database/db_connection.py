from pymongo import MongoClient

client = MongoClient("mongodb://admin:admin@ds049864.mongolab.com:49864/activitytracker")
db = client.activitytracker
event_collection = db.Events
skill_collection = db.Skills
dimension_collection = db.Dimensions
user_collection = db.Users

