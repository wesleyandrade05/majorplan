CREATE TABLE 'students' (
netID TEXT,
first_name TEXT,
last_name TEXT,
major TEXT,
class INTEGER,
major_requirements NUMERIC,
hum_requirements NUMERIC,
sci_requirements NUMERIC,
social_requirements NUMERIC,
lang_requirements NUMERIC,
qr_requirements NUMERIC,
wri_requirements NUMERIC,
grad_requirements NUMERIC DEFAULT 36,
cert_requirements NUMERIC DEFAULT 0,'college' TEXT, 'password' TEXT, 'email' TEXT DEFAULT NULL,
PRIMARY KEY(netID)
);

CREATE TABLE subjects (
code TEXT,
description TEXT, 'termCode' INTEGER,
PRIMARY KEY(code)
);

CREATE TABLE 'courses' (
crn NUMERIC UNIQUE,
cSectionStatus TEXT,
courseNumber NUMERIC,
courseTitle TEXT,
department TEXT,
prerequisites TEXT,
sectionNumber NUMERIC,
sectionStatus TEXT,
shortTitle TEXT,
subjectCode TEXT,
subjectNumber NUMERIC,
syllabusLink TEXT,
termCode NUMERIC, 'description' TEXT,
PRIMARY KEY(crn)
);

CREATE TABLE distributionals (
id INTEGER,
course_crn INTEGER NOT NULL,
distDesg TEXT,
PRIMARY KEY(id),
FOREIGN KEY(course_crn) REFERENCES courses(crn)
);

CREATE TABLE selected_courses (
student_id TEXT,
course_crn INTEGER NOT NULL,
major BOOLEAN,
credits NUMERIC,
distributional TEXT, 'taking' BOOLEAN DEFAULT 0, 'term' TEXT DEFAULT NULL,
FOREIGN KEY(course_crn) REFERENCES courses(crn)
FOREIGN KEY(student_id) REFERENCES students(netID)
);