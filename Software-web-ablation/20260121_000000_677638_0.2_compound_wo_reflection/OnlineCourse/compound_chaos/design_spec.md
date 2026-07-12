Application



Routes Specification Backend

Path | HTTP Method | File
|------------|---------------|-------------|---------------|------------------|
/ | None |
/dashboard | | username {course_id (str), title (str), progress (int)})
/catalog catalog | {course_id (str), title (str), description (str), category (str), level (str), duration (str), status (str)}) |
/catalog/course/<course_id> course_details POST | course {course_id (str), title (str), description (str), category (str), level (str), duration (str), status (str)}), enrolled
my_courses my_courses.html {course_id (str), title (str), progress (int)}) |
/my-courses/<course_id> | course_learning GET, course (dict: {course_id (str), title (str), description (str), category (str), level (str), duration (str), status (str)}), (list of {lesson_id (str), title (str), content (str)}), {lesson_id (str), title (str), content (str)}), progress (int), |
| assignments GET my_assignments.html | (list dict: {assignment_id (str), course_id (str), title (str), description (str), due_date (str), max_points (int), status (str: Submitted or Pending)})
/assignments/submit/<assignment_id> | | GET, assignment {assignment_id (str), title (str), description (str)}), (str: None Submitted |
certificates GET | {certificate_id (str), course_title (str), issue_date (str)})
| user_profile | POST | (str), email (str)


Root route '/dashboard'.
POST on /catalog/course/<course_id> handles if not
- complete, generates in 100%.
POST on /assignments/submit/<assignment_id> handles
POST on the in

---

HTML Specifications (For Frontend Developer)

### 1. templates/dashboard.html
Dashboard and <h1>)
IDs:
- dashboard-page:
welcome-message: element showing {{ fullname }}"
enrolled-courses: of courses progress
- button course catalog
to to
-
username

(list of {course_id (str), title (str), progress (int)})
Navigation:
browse-courses-button ->
->



###
- Courses
Element
- div container
search-input: input for
- course-grid: div cards
view-course-button-{{ course.course_id }}: to view details
back-to-dashboard: button back dashboard
- Variables:
(list as
-
-> course_id=course.course_id)


---

###
Title:

-
course-title: h1 course.title
- course.description
- button enroll disabled with "Already
- button to back to catalog
- Variables:
-
-
Navigation:
- submit current
->
State:
enroll-button disabled and Enrolled" ==



4.
- Page Courses
-
container
enrolled
button to continue learning
- back-to-dashboard: to navigate to
Context
enrolled_courses of
Navigation:
- ->
- back-to-dashboard

---

5. templates/course_learning.html
Course
- Element
- div
-
lesson-content: div showing content
complete
- go to
Context Variables:
course
- dict {lesson_id, title, content})
current_lesson
(int)
can_mark_complete

route)
-> url_for('my_courses')



### 6. templates/my_assignments.html
Page Title: Assignments
IDs:
- assignments-page:
- showing all
button to submit
to go back dashboard
Context
dict 5Submitted6 or 5Pending6)
- Navigation:
-> url_for('submit_assignment', assignment_id=assignment.assignment_id)
back-to-dashboard url_for('dashboard')

---

templates/submit_assignment.html
- Page Title: Submit
IDs:
- div
- assignment-info: div assignment title and
-
submit-button: button to
to back
Context
assignment (dict: assignment_id, title,
- (str: "Late")
Navigation:
(POST route)
-> url_for('assignments')



### 8. templates/certificates.html
Page Title:

certificates-page: div
div certificate cards
- back-to-dashboard: button to dashboard
Context Variables:
certificates (list

- back-to-dashboard

---

### templates/profile.html
- Page Profile
-
profile-page:
- input email
profile-fullname: fullname
changes
to go
-
(str)
email
-
- Navigation:
current




## Section 3: Backend Developer)



-


- fullname: user




Learner


---

### data/courses.txt
-
-
unique course
course (str)
description: description
course category like Data (str)
level: difficulty (Beginner,
duration (str)
course (e.g.,
-
```
Programming|Learn from
2|Web websites|Web|Intermediate|60
analysis|Data|Advanced|80




data/enrollments.txt
-
- Description:
- enrollment_id: enrollment identifier (str)
enrolled
of enrolled
string
- integer 0-100 (percentage (int)
Progress", "Completed") (str)
-

1|john|1|2024-11-01|75|In Progress
2|jane|1|2024-10-15|100|Completed






assignment_id|course_id|title|description|due_date|max_points
Description:

assignment belongs (str)
- title: title
full (str)
due in format (str)

Examples:

1|1|Python Basics Quiz|Complete the quiz types|2024-12-01|100
a application|2024-12-15|200
```

---

###
- submission_id|assignment_id|username|submission_text|submit_date|grade|feedback
Description:
unique (str)
id (str)
username: user (str)
response
of
grade: empty graded
- feedback: or graded
Examples:
```
1|1|john|My
2|2|jane|Here my project...|2024-11-20|95|Excellent!




data/certificates.txt
- Fields: certificate_id|username|course_id|issue_date
Description:
certificate_id: id
username: user earned (str)
for (str)
YYYY-MM-DD (str)
Examples:
```




