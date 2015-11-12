from pymongo import MongoClient


def add_data():
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
    # ...
    skill_collection.insert_one({
        "name": "Collaboration/Teamwork",
        "dimensions": ["Intellectual Agility", "Global Awareness", "Professional & Personal Effectiveness"]
    })

    skill_collection.insert_one({
        "name": "Communication",
        "dimensions": ["Intellectual Agility", "Global Awareness", "Social Consciousness & Interpersonal Commitment",
                       "Professional & Personal Effectiveness"]
    })
    # ...
    skill_collection.insert_one({
        "name": "Networking",
        "dimensions": ["Social Consciousness & Interpersonal Commitment", "Professional & Personal Effectiveness",
                       "Well-Being"]
    })
    # ...
    skill_collection.insert_one({
        "name": "Organization",
        "dimensions": ["Intellectual Agility", "Social Consciousness & Interpersonal Commitment"]
    })
    # ...
    skill_collection.insert_one({
        "name": "Planning",
        "dimensions": ["Intellectual Agility"]
    })
    # ...
    skill_collection.insert_one({
        "name": "Social Awareness",
        "dimensions": ["Social Consciousness & Interpersonal Commitment"]
    })





    # event_collection.insert_one({
    #     "title": "Northeastern University Growth Opportunities for Asian American Leaders (NUGOAL)",
    #     "format": "Training and development program",
    #     "topics": ["Multicultural", "Leadership", "Community Engagement", "Exploring Identity"],
    #     "description": "Northeastern University Growth and Opportunity for"
    #                    " Asian American Leaders is a program specifically designed for first and second year "
    #                    "Asian American students who are looking to increase and gain experiences to empower themselves as"
    #                    " leaders at Northeastern University and beyond. A cohort of students will be chosen based on their "
    #                    "potential as future leaders and need for leadership development. This seven week program will focus"
    #                    " on the intersection of leadership and Asian American racial identity through discussions and"
    #                    " projects. It will be facilitated by current Asian American student leaders and AAC staff. Apply by"
    #                    " December 1, 2015.",
    #     "begin": "12/1/2015",
    #     "end": "3/2015",
    #     "engagementLengthValue": 1,
    #     "engagementLengthUnit": "Semester",
    #     "recurrence": "Yearly",
    #     "location": "Boston Campus",
    #     "sponsoringDepartment": "Asian American Center",
    #     "pointOfContact": {"name": "Kristine Din", "number": "6173735554", "email": "k.din@neu.edu"},
    #     "outcomes": ["Students will be able to define leadership in relationship to their own racial identity.",
    #                  "Students will be able to describe their leadership strengths.",
    #                  "Students will be able to employ their leadership style and strengths in their daily lives.",
    #                  "Students will be able to analyze leadership in the Asian American community.",
    #                  "Students will be able to propose a meaningful intervention for building Asian American leadership"
    #                  " capacity.",
    #                  "Students will be able to assess the need for leadership development within the Asian American"
    #                  " community at Northeastern."],
    #     "skills": ["Communication", "Collaboration/Teamwork", "Social Awareness", "Networking", "Organization", "Planning"],
    #     "engagementLevel": "Active",
    #
    #     "coopFriendly": True,
    #     "academicStanding": ["First Year", "Second Year"],
    #     "major": "Any",
    #     "residentStatus": "Both",
    #     "otherRequirements": ["Identify as Asian American"]
    # })


if __name__ == '__main__':
    add_data()
