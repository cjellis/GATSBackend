import csv
import os


##
# prints out all of the calls that would need to be amde to Mongo in order
# to insert all of the skills in skills.csv
def create_text():
    with open(os.path.join(os.path.dirname(__file__), 'skills.csv'), 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for arr in reader:
            dimensions = ""
            name = arr[0]
            if arr[1] == "x" or arr[1] == "X":
                dimensions += "'Intellectual Agility', "
            if arr[2] == "x" or arr[2] == "X":
                dimensions += "'Global Awareness', "
            if arr[3] == "x" or arr[3] == "X":
                dimensions += "'Social Consciousness & Interpersonal Commitment', "
            if arr[4] == "x" or arr[4] == "X":
                dimensions += "'Professional & Personal Effectiveness', "
            if arr[5] == "x" or arr[5] == "X":
                dimensions += "'Well-Being', "
            print "skill_collection.insert_one({" + "'name': '{0}', 'dimensions': [{1}]".format(name, dimensions[:-2]) + "})"

if __name__ == '__main__':
    create_text()
