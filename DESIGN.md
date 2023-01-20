# Fetchig Yale's API

## SubjectsAPIv2

First of all, in **fetch_subjets.py**, I made requests to Yale's API to populate my database. I created an API Key using Yale's Developer Portal and used it to perform the requests. After storing them in **subjects** with json format, I used json's library to make it readable for Python. After that, I put each of their codes and descriptions (their actual name) into the table **subjects** of the database.

## CoursesWebServicev3

Here, I used this API to populate the **courses** table of the database. First, I queried the database to obtain the subject codes and defined a list of the terms that will be in the database: Fall 2022 (202203) and Spring 2023(202301). After that, I performed different requests for each subject in each term. So, for each course of each response, I inserted the following information into the **courses** table: crn, course number, the course title, department, prerequisites, section number, section status, short title, subject code, subject number, link to the syllabus, term code, and description. Besides that, since the distributionals were given in the format of a list by the API, I put them into the **distributionals** table that related to the courses by the course registration number(crn).

# Database

Besides the three tables I already introduced, I also have the **students** database, where I record the following information of each user: netID, First Name, Last Name, Major, Class, Major Requirements, Humanities Requirements, Science Requirements, Social Science Requirements, Language Requirements, QR Requirements, Writing Requirements, Graduation Requirements, Certificate Requirements, College, password hash, and email. During the project, I ended up not using the certificate requirements, but they might be useful in future updates of the website.

The other table is the **selected_courses** one, where I store the courses that every user has added to their profile. In each row, I store the user's id, the course's crn, whether the student wants to use it on the major(0: No, 1: Yes), how many credits it is worth, to which distributional it is going to be applied, whether the user decided to really take it or not, and when they are going to take it. It is important to notice that adding the course and taking it are 2 different things: when you add you just put it into a list of intended courses, but when you take it, it is added to your worksheet.

The structure can be seen at **schema.sql**

# MajorPlan Website

## Flask Server

### Initialization Steps

First, I set up the flask environment and configure the session to use filesystems instead of signed cookies. After that, I copied the login_required function that was used in finance to set which pages required the user to be logged in. After that, I configured the CS50 Library to use the SQLite database.

### /login Route

Here, if the user requested via get, they will be prompted with **login.html**. After submitting the login form and requesting the route via post, the server will clear any session that might be saved, and get the user's netID and password. After that, I queried the database to check if there is a user with the given netID and if the password is correct. If one of these fails, the server flashes a warning message to the user. Otherwise, a session[user_id] will be given to the user and they will be redirected to the main page

### /register Route

If the page is requested via get, **register.html** is rendered. If it is requested via post, the server gets the information entered by the user, checks if the password and the confirmation are matching, and then insert this information into the database. After that, the user is logged in and taken to the main page.

### / Route

This is the main page of the website. It works as a course search for the user. First, I query the database again to obtain the subjects being offered. If the route is requested via get, i.e., no course search was made, it just renders **main.html**. Otherwise, the server searches through the database to find the courses that match the condition given by the user. To do that, I first get the values entered and then check if any of them were not edited. If this is the case, the user does not want to filter that parameter, and then they are set to '%', which is the regular expression symbol that represents "any amount of any character".

After that, I check which courses match the specified filters. To do that, they must have a subject code like the one given by the user and match the specified term, and either match a course title or a course number (or both, if that could be possible). In the last case, matching means having the entered text in any position. With that information, I then initialize a dictionary that will have the subject numbers as keys and their respective distributionals as values in the format of a list. So, for each course, I create a list of their distributionals and assign it to the dictionary key. It is important to mention that I put a conditional that just the usual distributionals are added (the API has many distributionals that do not matter for the general requirements, such as specific tracks of each discipline, so I decided not to add them since it would confuse the users).

Finally, a list of all the courses is shown by rendering **results.html**.

### /add_course Route

If a user clicks on any of the courses from the results page, a modal will be opened that let the user add the course. So, after the button is clicked, the route is called via post and the server gets the values given by the user. After that, they are inserted into the database and the user is redirected to the main page.

### /logout Route

It simply clears the session and redirects the user to the route /. Since the user will not be logged in, @login_required acts and the user goes to the login page.

### /my_courses Route

First of all, I query the database to collect all the desired information to use. So, I join the tables **courses** and **selected_courses**, which allowed me to get the course's information and the information given by the user about taking the course. After that, I convert the term codes to fall and spring to be user-friendlier.

Then, if the route is called via get, the server initializes a dictionary that has the terms as keys and a list of their courses as values. This is used to display the student's coursework throughout the years. The **my_courses.html** is rendered. If the route is called via post, I first check if the user added the course to the coursework. If not, I update the database to reflect it. If so, I check if the student specified a term or not. If not, the term is updated to NULL, and if so the term has its value updated on the database. Then, the user is redirected to /my_courses.

Detail: I am passing the prerequisites with the filter | safe because they are given as HTML code by Yale's API

### /remove_course Route

Here, if the user clicks the button to remove the course, we delete the course's entry from the **selected_courses** table that was related to the user. After that, the user is just redirected to /my_courses

### /my_requirements Route

This is one of the biggest routes but it is straightforward. First of all, I query the **student** tables to see how many credits the students have said they are required to take. If the user has not configured that, I set them to be at Yale's standard. After that, I query the database to sum up how many credits the student has taken for each distributional. With that, I create two dictionaries, the reqs, and the control. The first one will be updated with how many credits are missing, and the second will be how many the student has taken. After that, I just check for each requirement if the student has already fulfilled them or not. Finally, I also perform a query to see the total amount of credits the student has taken and then calculate the number of credits missing to graduate. The server then renders **my_requirements.html**.

### /my_major Route

Here, I query the database to see which courses the user has taken that are counting towards the major. After that, I get how many credits he has to finish the major (if no value was set I just take the standard) and then calculate how many are missing. After that, the server just renders **my_major.html**

### /profile Route

Here, I just query the database to obtain the user's personal information and render **profile.html** to display it.

### /edit Route

First of all, I get the user's current information from the database. Then, if the route was requested via get, **edit.html** is rendered. Otherwise, such as when the user submits the form, I execute a query that will update the user's information but the password. I then check if the user decided to change their password and if so I check if the current one is correct if he inserted a new one, and if the new one and the confirmation are matching. If so, I update the database and redirect them to /log out. If they did not change the password, they are just redirected to /profile.

## Frontend

I used jinja to connect my flask server to my HTML templates. Also, I used mostly Bootstrap's framework to design my website. I have my **styles.css** file where I have some general properties, but in some cases, I mixed them with the HTML code to make it more readable since they were just some details about margin or color. Then, since doing personalized CSS is not the focus of my project, I decided to leave it like that. In many cases, I referred to W3School and MDN Web Docs to double-check HTML and CSS syntaxes

### main.html

It simply shows a form that allows the user to perform the course search. I aligned them horizontally and in the middle of the line.

### results.html

Here, I repeated the form of **main.html** and added a list group to display the results. The list-group items were buttons that opened a modal. In these models, there were the description and prerequisites of the specific course, and a form to add the course. To make a customized modal, I used Bootstrap's JavaScript code and classes. The script basically collects the information from the button and changes the modal's HTML accordingly. In the form to add the course, I let the user choose any option of distributional requirements because some courses can be applied to distributionals other than the official ones. So, I did not limit the choice in this case.

### my_courses.html

I first have a table with all the functionalities done on this page. I am also using bootstrap's sliders to switch the course's status. Their value is set to on if they are checked. After that, I have two tables, and inside each of them, I have four more: one for each term. Then, I just use Jinja's loop to display all the information.

### my_requirements.html

I have a title showing how many credits are still necessary to graduate and a table that shows the details about each distributional requirement.

### my_major.html

I display a title saying how many credits are still missing and then I create one horizontal list group for each course. I am fixing a width to the course's name to improve their alignment. I am again using the filter safe on the prerequisites because they are given as HTML code.

### profile.html

It is just a table showing all the user's information. I also implemented a button below the table to let the user change that information.

### edit.html

It is very similar to the previous one, but here the user can change the entries and change their password. Notice that the default values and placeholder are set to the user's current information. This is because they will just have to change what they need to, instead of retyping everything.

### register.html

It is a big form where the user can insert their information. I used Bootstrap's classes row and col to better align the input boxes.

### login.html

This is a simple form to enter the netID and password. It also has a link that redirects the user to the registration page.

### layout.html

Finally, all pages link to this one. It has a menu and a container to enter the main text of the page.