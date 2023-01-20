import requests
import json
from cs50 import SQL

"""
Information provided by Yale API Portal
"""

# Configure CS50 Library to use the SQLite Database
db = SQL("sqlite:///majorplan.db")

# Request subjects from API
subjects = requests.get("https://gw.its.yale.edu/soa-gateway/course/webservice/v2/subjects?apikey=[APIKEY]&mode=json")

# Convert the responses into a list of dictionaries
readable= subjects.json()

# Add each of them into the database
for subject in readable:
    db.execute("INSERT INTO subjects VALUES (?, ?, 202301)", subject["code"], subject["description"])