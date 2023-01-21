import requests
import json
from cs50 import SQL

"""
Information provided by Yale API Portal
"""

# Configure CS50 Library to use the SQLite Database
db = SQL("sqlite:///majorplan.db")

# Query to obtain all the subjects available
subjects = db.execute("SELECT code FROM subjects")

# Terms that will be stored into the database
seasons = ["202203", "202301"]

# Insert the courses of each subject
for subject in subjects:

    # Make a different request for each season
    for season in seasons:
        # Request to obtain the list of courses for that specific subject in that specific term
        courses = requests.get("https://gw.its.yale.edu/soa-gateway/courses/webservice/v3/index?apikey=[APIKEY]&termCode="+season+"&subjectCode="+ subject["code"] +"&mode=json")

        # Convert the responses into a list of dictionaries
        courses = courses.json()

        # Insert the values of each course
        for course in courses:
            db.execute("INSERT INTO courses VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        course["crn"], course["cSectionStatus"], course["courseNumber"], course["courseTitle"], course["department"], course["prerequisites"], course["sectionNumber"], course["sectionStatus"], course["shortTitle"], course["subjectCode"], course["subjectNumber"], course["syllabusLink"], course["termCode"], course["description"])

            #Insert the distributionals of each course into another table, linked by the course's crn
            for item in course["distDesg"]:
                db.execute("INSERT INTO distributionals (course_crn, distDesg) VALUES (?, ?)", course["crn"], item)