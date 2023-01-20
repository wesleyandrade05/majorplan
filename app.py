from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_login import LoginManager, login_required, login_user
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

# Setting up Flask environment
app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Definition of the function that requires to be logged in to access a page
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Configure CS50 Library to use the SQLite Database
db = SQL("sqlite:///majorplan.db")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login the user"""

    # Checks if the route was requested via post
    if request.method == "POST":
        # Clear the session to forget any user id
        session.clear()

        # Obtain the netID and password entered by the user
        netID = request.form.get("netID")
        password = request.form.get("password")

        # Query the database to find a student with the specified netID
        users = db.execute("SELECT netID, password FROM students WHERE netID = ?", netID)

        # Check if there is a student with that netID or the password match
        if not users or not check_password_hash(users[0]["password"], password):
            flash("Invalid username/password")
            return redirect("/login")

        # Assign the netID to be the user's session id
        session["user_id"] = users[0]["netID"]

        # Redirect to the main page
        return redirect("/")

    # If the page was requested via get
    else:
        # Render the login page
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register the user"""

    # If the page is accessed by post (e.g. after the user submitted the registration form)
    if request.method == "POST":
        # Store the information given by the user
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        netID = request.form.get("netID")
        year = request.form.get("year")
        major = request.form.get("major")
        college = request.form.get("college")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        email = request.form.get("email")

        # Check if the passwords are matching
        if password != confirmation:
            flash("Passwords don't match")
            return redirect("/register")

        # Insert the user's information into the database
        query = db.execute("INSERT INTO students (netID,first_name,last_name,major,class,college,password,email) VALUES (?,?,?,?,?,?,?,?)",
                           netID, first_name, last_name, major, year, college, generate_password_hash(password), email)

        # Assign a session id to the user to automatically login
        session["user_id"] = netID

        flash("Registered!")

        # Redirect to the main page
        return redirect("/")

    # If requested via get
    else:
        # Render the registration page
        return render_template("register.html")


@app.route("/", methods=["GET", "POST"])
@login_required
def main():
    """Main page: course search"""

    # Query to obtain the offered subjects
    subjects = db.execute("SELECT code FROM subjects")

    # If the user performed a search:
    if request.method == "POST":
        # Get the information from the form
        subject = request.form.get("subject-search")
        term = request.form.get("term-search")
        course = request.form.get("course-search")

        # If any of them was not edited, do not filter by anything
        if not course:
            course = '%'
        if term == 'Term':
            term = '%'
        if subject == 'Subject':
            subject = '%'

        # Query to obtain the courses that match the filters
        course_results = db.execute(
            "SELECT courseTitle, crn, subjectNumber, sectionNumber, description, termCode, prerequisites FROM courses WHERE (subjectCode LIKE ? AND (courseTitle LIKE ? OR subjectNumber LIKE ?) AND termCode LIKE ?)", subject, f'%{course}%', f'%{course}%', term)

        # Initialize a dictionary that will have the courses as keys and a list of the respective distributionals as values
        distributionals = {}

        # Populate the dictionary
        for course in course_results:
            dists = db.execute("SELECT distDesg FROM distributionals WHERE course_crn == ?", course["crn"])
            temp = []

            for dist in dists:

                # Append just if it is an usual distributional
                if dist["distDesg"] in ["YCL1", "YCL2", "YCL3", "YCL4", "YCL5", "YCQR", "YCWR", "YCSC", "YCSO", "YCHU"]:
                    temp.append(dist["distDesg"])

            distributionals[course["subjectNumber"]] = temp

        # Render the results template
        return render_template("results.html", subjects=subjects, course_results=course_results, distributionals=distributionals)

    else:
        # Render the main page template
        return render_template("main.html", subjects=subjects)


@app.route("/add_course", methods=["POST"])
@login_required
def add_course():
    """Add course"""

    if request.method == "POST":
        # Get the entered information
        distributional = request.form.get("distributional")
        major = request.form.get("major")
        crn = request.form.get("course_crn")
        credits = request.form.get("credits")

        # Insert this course into the database
        query = db.execute("INSERT INTO selected_courses (student_id,course_crn,major,credits,distributional) VALUES (?,?,?,?,?)",
                           session["user_id"], int(crn), int(major), float(credits), distributional)

        # Render the main page template
        return render_template("main.html")


@app.route("/logout")
@login_required
def logout():
    """Logout"""

    # Clear the sessions
    session.clear()

    # Redirect to route / and then ask the user to log in
    return redirect("/")


@app.route("/my_courses", methods=["GET", "POST"])
@login_required
def my_courses():
    """My Courses Page"""

    # Query to obtain information of all courses added by the user
    courses = db.execute(
        "SELECT selected_courses.taking, selected_courses.term, selected_courses.distributional, courses.crn, courses.courseTitle, courses.subjectNumber, courses.syllabusLink, courses.termCode FROM selected_courses INNER JOIN courses ON courses.crn = selected_courses.course_crn WHERE selected_courses.student_id == ?", session["user_id"])

    # Change the termcode to Fall/Spring
    for course in courses:
        if course["termCode"] == 202203:
            course["termCode"] = "Fall"

        elif course["termCode"] == 202301:
            course["termCode"] = "Spring"

    # If the user hits save
    if request.method == "POST":
        # Loop through every couse
        for course in courses:
            # If the slider is checked
            if request.form.get("add_" + str(course["crn"])) == "on":
                # Update the course's status
                db.execute("UPDATE selected_courses SET taking = 1 WHERE course_crn == ? AND student_id == ?",
                           course["crn"], session["user_id"])

                # Set term to null if none was entered
                if not request.form.get("term-selection_" + str(course["crn"])):
                    db.execute("UPDATE selected_courses SET term = NULL WHERE course_crn == ? AND student_id == ?",
                               course["crn"], session["user_id"])

                # Else, set term to the one informed by the user
                else:
                    db.execute("UPDATE selected_courses SET term = ? WHERE course_crn == ? AND student_id == ?",
                               request.form.get("term-selection_" + str(course["crn"])), course["crn"], session["user_id"])

            # If not, just set term to NULL and taking to 0 (No)
            else:
                db.execute("UPDATE selected_courses SET taking = 0, term = NULL WHERE course_crn == ? AND student_id == ?",
                           course["crn"], session["user_id"])

        # Redirect to /my_courses
        return redirect("/my_courses")

    # If accessed via get
    else:
        # Initialize a dictionary which has the terms as keys and the courses of each term as values
        plan = {"First Year Fall": [], "First Year Spring": [], "Sophomore Fall": [], "Sophomore Spring": [], "Junior Fall": [],
                "Junior Spring": [], "Senior Fall": [], "Senior Spring": []}

        # Populate the dictionary
        for course in courses:
            if course["taking"] == 1:
                plan[course["term"]].append(course["subjectNumber"])

        # Render my_courses.html
        return render_template("my_courses.html", courses=courses, plan=plan)


@app.route("/remove_course", methods=["POST"])
@login_required
def remove_course():
    """Remove a course from my courses"""

    # Get which course was removed by the user
    crn = request.form.get("course")

    # Delete it from the database
    query = db.execute("DELETE FROM selected_courses WHERE course_crn == ? AND student_id == ?", crn, session["user_id"])

    # Redirect to /my_courses
    return redirect("/my_courses")


@app.route("/my_requirements")
@login_required
def my_requirements():
    """Load the requirements page"""

    # Standard requirements of the user
    std_reqs = (db.execute(
        "SELECT major_requirements, hum_requirements, sci_requirements, social_requirements, lang_requirements, qr_requirements, wri_requirements, grad_requirements, cert_requirements FROM students WHERE netID == ?", session["user_id"]))[0]

    # If any of them are set to none. use Yale's standards
    if std_reqs["major_requirements"] == None:
        std_reqs["major_requirements"] = 12

    if std_reqs["grad_requirements"] == None:
        std_reqs["grad_requirements"] = 36

    if std_reqs["hum_requirements"] == None:
        std_reqs["hum_requirements"] = 2

    if std_reqs["social_requirements"] == None:
        std_reqs["social_requirements"] = 2

    if std_reqs["sci_requirements"] == None:
        std_reqs["sci_requirements"] = 2

    if std_reqs["lang_requirements"] == None:
        std_reqs["lang_requirements"] = 2

    if std_reqs["qr_requirements"] == None:
        std_reqs["qr_requirements"] = 2

    if std_reqs["wri_requirements"] == None:
        std_reqs["wri_requirements"] = 2

    """General Requirements Calculation"""

    # Count how many credits the user has taken of each distributional
    query = db.execute(
        "SELECT SUM(credits), distributional FROM selected_courses WHERE student_id == ? AND taking == 1 GROUP BY distributional", session["user_id"])

    # Dictionary to count how many credits are missing
    reqs = {"YCHU": 0, "YCSC": 0, "YCLA": 0, "YCQR": 0, "YCSO": 0, "YCWR": 0}

    # Dictionary to count how many credits have been taken
    control = {"YCHU": 0, "YCSC": 0, "YCLA": 0, "YCQR": 0, "YCSO": 0, "YCWR": 0}

    # Populate the dictionaries
    for row in query:
        reqs[row["distributional"]] = row["SUM(credits)"]
        control[row["distributional"]] = row["SUM(credits)"]

    # Update reqs values for each distributional. If the distributional has already been fulfilled, set the reqs value to None
    if std_reqs["hum_requirements"] > reqs["YCHU"]:
        reqs["YCHU"] = std_reqs["hum_requirements"] - float(reqs["YCHU"])

    else:
        reqs["YCHU"] = "None!"

    if std_reqs["sci_requirements"] > reqs["YCSC"]:
        reqs["YCSC"] = std_reqs["sci_requirements"] - float(reqs["YCSC"])

    else:
        reqs["YCSC"] = "None!"

    if std_reqs["social_requirements"] > reqs["YCSO"]:
        reqs["YCSO"] = int(std_reqs["social_requirements"]) - float(reqs["YCSO"])

    else:
        reqs["YCSO"] = "None!"

    if std_reqs["lang_requirements"] > reqs["YCLA"]:
        reqs["YCLA"] = std_reqs["lang_requirements"] - float(reqs["YCLA"])

    else:
        reqs["YCLA"] = "None!"

    if std_reqs["qr_requirements"] > reqs["YCQR"]:
        reqs["YCQR"] = std_reqs["qr_requirements"] - float(reqs["YCQR"])

    else:
        reqs["YCQR"] = "None!"

    if std_reqs["wri_requirements"] > reqs["YCWR"]:
        reqs["YCWR"] = std_reqs["wri_requirements"] - float(reqs["YCWR"])

    else:
        reqs["YCWR"] = "None!"

    # Calculate the number of credits needed to graduate
    grad_reqs = db.execute("SELECT SUM(credits) FROM selected_courses WHERE taking == 1 AND student_id == ?", session["user_id"])

    to_graduate = std_reqs["grad_requirements"] - grad_reqs[0]["SUM(credits)"]

    # Render my_requirements.html
    return render_template("my_requirements.html", reqs=reqs, control=control, std_reqs=std_reqs, to_graduate=to_graduate)


@app.route("/my_major")
@login_required
def my_major():
    """Load the major page"""

    # Query to obtain the courses counting towards the major
    courses = db.execute(
        "SELECT selected_courses.term, selected_courses.course_crn, selected_courses.credits, courses.courseTitle, courses.subjectNumber, courses.prerequisites FROM selected_courses JOIN courses ON courses.crn == selected_courses.course_crn WHERE student_id == ? AND major == 1", session["user_id"])

    # Query to obtain the credits necessary to finish the major
    major_requirements = db.execute("SELECT major_requirements FROM students WHERE netID == ?", session["user_id"])

    # Set to 12 if no value was given
    if not major_requirements[0]['major_requirements']:
        major_requirements[0]['major_requirements'] = 12

    # Calculate the missing credits
    missing = major_requirements[0]['major_requirements'] - len(courses)

    # Render my_major.html
    return render_template("my_major.html", courses=courses, missing=missing)


@app.route("/profile")
@login_required
def profile():
    """Load profile page"""

    # Query to obtain all the user's information
    user = db.execute("SELECT * FROM students WHERE netID == ?", session["user_id"])

    # Render profile.html
    return render_template("profile.html", user=user[0])


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    """Edit the user's information"""

    # Query to obtain the current information
    user = db.execute("SELECT * FROM students WHERE netID == ?", session["user_id"])

    # If the route was requested via post
    if request.method == "POST":
        # Update the database to match the new information
        edit_profile = db.execute("UPDATE students SET first_name = ?, last_name = ?, major = ?, college = ?, class = ?, email = ?, major_requirements = ?, hum_requirements = ?, sci_requirements = ?, social_requirements = ?, qr_requirements = ?, wri_requirements = ?, lang_requirements = ?, grad_requirements = ? WHERE netID == ?", request.form.get("first_name"), request.form.get("last_name"), request.form.get(
            "major"), request.form.get("college"), request.form.get("class"), request.form.get("email"), request.form.get("major_requirements"), request.form.get("hum_requirements"), request.form.get("sci_requirements"), request.form.get("social_requirements"), request.form.get("qr_requirements"), request.form.get("wri_requirements"), request.form.get("lang_requirements"), request.form.get("grad_requirements"), session["user_id"])

        # If the user changed the password
        if request.form.get("current_password"):
            # Check if the current password is correct
            if not check_password_hash(user[0]["password"], request.form.get("current_password")):
                flash("Incorrect Password!")
                return redirect("/edit")

            # Check if they inserted a new password
            if not request.form.get("new_password") or not request.form.get("confirmation"):
                flash("Missing new password!")
                return redirect("/edit")

            # Check if the new password matches the confirmation
            if request.form.get("new_password") != request.form.get("confirmation"):
                flash("Passwords do not match!")
                return redirect("/edit")

            # Update the database
            update = db.execute("UPDATE students SET password = ? WHERE netID = ?",
                                generate_password_hash(request.form.get("new_password")), session["user_id"])

            # Redirect to logout
            return redirect("/logout")

        flash("You successfully changed your information!")

        # Redirect to /profile
        return redirect("/profile")

    else:
        # Render edit.html
        return render_template("edit.html", user=user[0])