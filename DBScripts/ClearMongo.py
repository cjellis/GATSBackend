from pymongo import MongoClient
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import config


##
# clears out all of the collections in Mongo
def clear_mongo():
    client = MongoClient(config.MONGODB_URL)
    db = client.activitytracker
    event_collection = db.Events
    skill_collection = db.Skills
    dimension_collection = db.Dimensions
    user_collection = db.Users

    event_collection.remove({})
    skill_collection.remove({})
    dimension_collection.remove({})
    user_collection.remove({})

if __name__ == '__main__':
    clear_mongo()
