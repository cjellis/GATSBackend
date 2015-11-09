from pymongo import MongoClient

client = MongoClient("mongodb://admin:admin@ds049864.mongolab.com:49864/activitytracker")
db = client.activitytracker
event_collection = db.Events
skill_collection = db.Skills
dimension_collection = db.Dimensions

dimension_collection.insert_one({"name": "Intellectual Agility"})
dimension_collection.insert_one({"name": "Global Awareness"})
dimension_collection.insert_one({"name": "Social Consciousness & Interpersonal Commitment"})
dimension_collection.insert_one({"name": "Professional & Personal Effectiveness"})
dimension_collection.insert_one({"name": "Well-Being"})

skill_collection.insert_one({
    "name": "Adaptable/Flexible",
    "dimensions": ["Intellectual Agility", "Global Awareness", "Professional & Personal Effectiveness", "Well-Being"]
})
skill_collection.insert_one({
    "name": "Advocacy",
    "dimensions": ["Social Consciousness & Interpersonal Commitment"]
})

