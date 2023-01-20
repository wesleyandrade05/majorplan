This was my CPSC 100's Final Project at Yale University. Collaboration on it is more than welcome, just please email me at wesleyantonio.andrade@yale.edu

# Where to Compile?

The website was designed to run in the codespace. To do it, you just have to run **flask run** in the console. The database can be seen using **phpliteadmin majorplan.db**

# What is MajorPlan?

MajorPlan is a website that intends to be a user-friendlier version of Yale's SIS Degree Audit. Being connected to a customized database with Yale's courses and subjects, the website works both as a course search and as s planner: the student can add every course they intend to take and organize them throughout the years at college. After doing that, the website automatically calculates the fulfilled requirements, the worksheet, and the major path of the student.

# Login Page:

On the login page, the student has to insert their netID and password (not Yale's password, i.e., the website is not connected to CAS). There is also the option to **register** if the student does not have an account on the website.

# Registration Page:

Here, the user has to insert their personal information. They must insert their full First name and Last Name, their netID, their Class Year, their intended Major, their Yale Email, and their College. They must also provide a password twice (to avoid typos)

# First Page (Course Search):

After logging in, the user lands into the Course Search mechanism of the website. Here, they have 3 options to specify their search: the subject, course's name/number, and term. After performing the search, the user will see a list of results (the courses that match the specifications). Here, in the space of each course, they can see the course's name in bold and big letters and the course's number in the top right. Below it, the user sees the section (this is more to inner control since different sections have different registration numbers at Yale's system), the term in which that course is offered (this is useful to plan the coursework), the distributional requirements to which the course might be applied, and the prerequisites to take the course.

Regarding the distributionals that the user will see, the designations have the following meanings:

- YCQR: Quantitative Reasoning Skill
- YCWR: Writing Skill
- YCL#: Language Skill (from L1 to L5)
- YCSC: Science Area
- YCHU: Humanities Area
- YCSO: Social Science Area

There is also the feature of adding the course to "My Courses". Adding a course means that you have an interest in it, but you just add it to your worksheet on the "My Courses" tab. So, to add the course, you just have to click on the course and a customized modal will show up. On the modal, the user can see the course's description and review its requirement. Before adding the course, the student has to indicate if it is going to count towards the major or not, how many credits it has, and to which distributional requirement the student intends to use the course. The options that appear for the distributional are not limited to the ones that appear on the website. So, if the user wants to use ENGL114, for example, as a language requirement (which is an option for international students), they can do that here. After clicking to add the course, the user will be redirected to the search page again.

# My Courses

This is the most complex (and most beautiful in my opinion) page of the website. Here, a table showing all the added courses will be displayed. For each course, the user will be able to see the courses' numbers, the term in which the course is offered, the distributional requirement to which the courses are being applied, and a link to the syllabus. Besides that, there is a column saying whether the student is taking that course or not (i.e. if the course has been added to the worksheet), and a column that says when the course is being taken or with a dropdown for the user to select when they are going to take it (in case they are not taking yet). The last column has a slider that has the function of adding the course to the worksheet. Finally, they can hit the save button below the table to update the coursework. Finally, If the user is not willing to take one of these courses anymore, they can remove it by clicking on the red button. If they want to change when they are taking the course, they have to first unselect it and then choose the term again.

Below the save button, we have an automatic worksheet that is updated with the information given by the user. There, the courses are added in a way the user is allowed to have a complete overview of their time at Yale. This can be used to simulate course sequences when to take each distributional, and check the workload of each semester. It is also important to mention that I left the opportunity of adding the same course twice. This allows the user to simulate at the same time different coursework by putting the course in multiple terms.

# My Requirements

This page does not have any user interaction. It shows how many courses credits the user still needs to take to graduate and keeps track of the distributional requirements. The table displays how many credits the user took for each distributional, how many credits they are obligated to take, and how many they still have to take. If they have already taken a sufficient amount of credits, it shows "None!" on the "To Go" column. If the user has taken all the necessary credits to graduate, it shows a congratulations message and asks the user to double-check if the distributionals are also done.

# My Major

On the top of the page, it shows how many credits it is still necessary to take to finish the major. Besides that, a list is shown with all the courses the user has taken (i.e. added to the worksheet) that are counting towards the major. So, it is possible to see the course's number, prerequisites, title, and time when it was taken. This allows the student to have a complete overview of how the major is going and what gaps they may be having.

# Logout

The Logout button simply logouts the user and takes them back to the login page.

# Profile

Lastly, the profile page shows all the personal information of the user. It is important to notice that, by default, the requirements are going to be set to none. This is because they can change in some situations, so I did not want to set them to the standard value automatically. However, the user is free to use all of the website's features without setting any value for the requirements on the profile page: in this case, the values used in the calculations are going to be the standard ones.

To change their personal information, the user can click on the button "Edit/Change Password "at the bottom. There, the user will be allowed to change every piece of information, besides the netID -- this is just to avoid a lot of changes since if one day I make this website public and allow users to see some of each other's information, it is necessary to keep the same id for every account. It is also possible to change the password (but you are not required to fill this field with anything if you are not willing to change it) by confirming the current one and then typing twice the new one.

If the password is changed, the user is taken to the login page after clicking on "Submit". If the password is not changed, they are taken back to the profile page.

# Presentation Video

Here is a link to a youtube video where I give a visual presentation about the website: https://youtu.be/hSEGqfGrbao
