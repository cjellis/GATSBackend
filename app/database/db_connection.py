from pymongo import MongoClient
import config

##
# creates a connection to the remote Mongo DB
# and sets up variables for each collection we use
client = MongoClient(config.MONGODB_URL)
db = client.activitytracker
event_collection = db.Events
skill_collection = db.Skills
dimension_collection = db.Dimensions
user_collection = db.Users

