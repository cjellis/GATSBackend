from pymongo import MongoClient
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import config

##
# Adds the dimensions, skills, and one administrator
def add_data():
    client = MongoClient(config.MONGODB_URL)
    db = client.activitytracker
    skill_collection = db.Skills
    dimension_collection = db.Dimensions
    user_collection = db.Users

    dimension_collection.insert_one({"name": "Intellectual Agility"})
    dimension_collection.insert_one({"name": "Global Awareness"})
    dimension_collection.insert_one({"name": "Social Consciousness & Interpersonal Commitment"})
    dimension_collection.insert_one({"name": "Professional & Personal Effectiveness"})
    dimension_collection.insert_one({"name": "Well-Being"})

    skill_collection.insert_one({'name': 'Adaptable/Flexible', 'dimensions': ['Intellectual Agility', 'Global Awareness', 'Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'Advocacy', 'dimensions': ['Social Consciousness & Interpersonal Commitment']})
    skill_collection.insert_one({'name': 'CC-Creative Thinking', 'dimensions': ['Intellectual Agility', 'Global Awareness', 'Social Consciousness & Interpersonal Commitment', 'Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'CC-Critical Thinking', 'dimensions': ['Intellectual Agility', 'Global Awareness', 'Social Consciousness & Interpersonal Commitment', 'Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'CC-Decision-Making', 'dimensions': ['Intellectual Agility', 'Global Awareness', 'Social Consciousness & Interpersonal Commitment', 'Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'CC-Emotional Intelligence', 'dimensions': ['Intellectual Agility', 'Global Awareness', 'Social Consciousness & Interpersonal Commitment', 'Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'CC-Innovation/Design Thinking', 'dimensions': ['Intellectual Agility', 'Global Awareness', 'Social Consciousness & Interpersonal Commitment', 'Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'CC-Inquiry & Analysis', 'dimensions': ['Intellectual Agility', 'Global Awareness', 'Social Consciousness & Interpersonal Commitment', 'Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'CC-Integrative Thinking', 'dimensions': ['Intellectual Agility', 'Global Awareness', 'Social Consciousness & Interpersonal Commitment', 'Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'CC-Knowledge Acquisition', 'dimensions': ['Intellectual Agility', 'Global Awareness', 'Social Consciousness & Interpersonal Commitment', 'Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'CC-Problem Solving', 'dimensions': ['Intellectual Agility', 'Global Awareness', 'Social Consciousness & Interpersonal Commitment', 'Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'CC-Quantitative Reasoning', 'dimensions': ['Intellectual Agility', 'Global Awareness', 'Social Consciousness & Interpersonal Commitment', 'Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'CC-Reasoning', 'dimensions': ['Intellectual Agility', 'Global Awareness', 'Social Consciousness & Interpersonal Commitment', 'Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'CC-Self-awareness of Learning Process', 'dimensions': ['Intellectual Agility', 'Global Awareness', 'Social Consciousness & Interpersonal Commitment', 'Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'CC-Strategic Thinking', 'dimensions': ['Intellectual Agility', 'Global Awareness', 'Social Consciousness & Interpersonal Commitment', 'Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'Civically Minded', 'dimensions': ['Social Consciousness & Interpersonal Commitment']})
    skill_collection.insert_one({'name': 'Collaboration/Teamwork', 'dimensions': ['Intellectual Agility', 'Global Awareness', 'Professional & Personal Effectiveness']})
    skill_collection.insert_one({'name': 'Communication', 'dimensions': ['Intellectual Agility', 'Global Awareness', 'Social Consciousness & Interpersonal Commitment', 'Professional & Personal Effectiveness']})
    skill_collection.insert_one({'name': 'Conflict Analysis and Resolution/Transformation', 'dimensions': ['Social Consciousness & Interpersonal Commitment']})
    skill_collection.insert_one({'name': 'Creative expression', 'dimensions': ['Intellectual Agility']})
    skill_collection.insert_one({'name': 'Cultural and Aesthetic Arts', 'dimensions': ['Intellectual Agility', 'Professional & Personal Effectiveness']})
    skill_collection.insert_one({'name': 'Curiosity/Inquisitiveness', 'dimensions': ['Intellectual Agility', 'Global Awareness', 'Social Consciousness & Interpersonal Commitment']})
    skill_collection.insert_one({'name': 'Emotionally Healthy', 'dimensions': ['Well-Being']})
    skill_collection.insert_one({'name': 'Empathy', 'dimensions': ['Global Awareness', 'Social Consciousness & Interpersonal Commitment']})
    skill_collection.insert_one({'name': 'Ethical Reasoning', 'dimensions': ['Global Awareness', 'Social Consciousness & Interpersonal Commitment', 'Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'Financial Literacy', 'dimensions': ['Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'Global Citizenship', 'dimensions': ['Social Consciousness & Interpersonal Commitment']})
    skill_collection.insert_one({'name': 'Global Mindset', 'dimensions': ['Global Awareness', 'Social Consciousness & Interpersonal Commitment']})
    skill_collection.insert_one({'name': 'Independence/Autonomy', 'dimensions': ['Well-Being']})
    skill_collection.insert_one({'name': 'Information Literacy', 'dimensions': ['Intellectual Agility', 'Global Awareness', 'Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'Initiative/Resourcefulness', 'dimensions': ['Intellectual Agility', 'Social Consciousness & Interpersonal Commitment', 'Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'Integrity', 'dimensions': ['Global Awareness', 'Professional & Personal Effectiveness']})
    skill_collection.insert_one({'name': 'Intercultural Understanding', 'dimensions': ['Global Awareness', 'Social Consciousness & Interpersonal Commitment']})
    skill_collection.insert_one({'name': 'Interpersonal Skills', 'dimensions': ['Global Awareness', 'Social Consciousness & Interpersonal Commitment']})
    skill_collection.insert_one({'name': 'Networking', 'dimensions': ['Social Consciousness & Interpersonal Commitment', 'Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'Observation and interpretation', 'dimensions': ['Global Awareness', 'Social Consciousness & Interpersonal Commitment']})
    skill_collection.insert_one({'name': 'Open-Mindedness', 'dimensions': ['Global Awareness', 'Social Consciousness & Interpersonal Commitment']})
    skill_collection.insert_one({'name': 'Organization', 'dimensions': ['Intellectual Agility', 'Social Consciousness & Interpersonal Commitment']})
    skill_collection.insert_one({'name': 'Perseverance', 'dimensions': ['Intellectual Agility', 'Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'Physical Self-Care', 'dimensions': ['Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'Planning', 'dimensions': ['Intellectual Agility']})
    skill_collection.insert_one({'name': 'Positive Self-Esteem/Self-Compassion', 'dimensions': ['Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'Realistic Self-Confidence/Empowered', 'dimensions': ['Social Consciousness & Interpersonal Commitment', 'Professional & Personal Effectiveness']})
    skill_collection.insert_one({'name': 'Resilience', 'dimensions': ['Professional & Personal Effectiveness', 'Well-Being']})
    skill_collection.insert_one({'name': 'Scientific Imagination', 'dimensions': ['Intellectual Agility', 'Professional & Personal Effectiveness']})
    skill_collection.insert_one({'name': 'Scientific Literacy', 'dimensions': ['Intellectual Agility']})
    skill_collection.insert_one({'name': 'Self-directed learner', 'dimensions': ['Intellectual Agility', 'Professional & Personal Effectiveness']})
    skill_collection.insert_one({'name': 'Social Awareness', 'dimensions': ['Social Consciousness & Interpersonal Commitment']})
    skill_collection.insert_one({'name': 'Social Consciousness', 'dimensions': ['Global Awareness']})
    skill_collection.insert_one({'name': 'Socially Integrated', 'dimensions': ['Well-Being']})

    user_collection.insert_one({
            'firstname': 'Admin',
            'lastname': 'Admin',
            'email': 'admin@neu.edu',
            'password': '625bc94a6b5e5b5046a0d4b44b84fddc',  # CATLRAdmin
            'token': 'ADMIN_TOKEN',
            'tokenTTL': 1000,
            'is_auth': True,
            'events': [],
            'roles': ['administrator', 'faculty', 'superuser'],
            'year': None,
            'major': None,
            'skills': [],
            'dimensions': []
        })

if __name__ == '__main__':
    add_data()
