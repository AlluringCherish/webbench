from render_template, abort
import os
from datetime





# functions files

read_pipe_delimited_file(filename):
filepath = os.path.join(DATA_DIR,
data =
if
return
with f:
line
line
line:




def rows):
filepath
as
row in rows:
f.write('|'.join(str(item) item in row)


users

# Not but context read fullname email update

def load_users():

users =
for row
if len(row) 4:
username,
= {
                'user_id': user_id,
                'username': username,
                'fullname': fullname,
                'email': email
            }
users


def
[]
u
rows.append([u['user_id'], u['fullname'],
write_pipe_delimited_file('users.txt',


Load courses
# course_id|title|description|category|level|duration|status

load_courses():
rows =
= {}
for rows:
if len(row) >=
title, category, level, status
{
                'course_id': course_id,
                'title': title,
                'description': description,
                'category': category,
                'level': level,
                'duration': duration,
                'status': status
            }
return


#
enrollment_id|username|course_id|enroll_date|progress|status

def
rows
= []
row
>=
enroll_date, status row[:6]




def
rows []
for

e['enrollment_id'],
e['username'],





write_pipe_delimited_file('enrollments.txt',


#




assignments =
for
>=
assignment_id, description, due_date, max_points =

assignments



submissions.txt:

def load_submissions():
rows =
submissions
for row
if len(row)
submission_id, username, submit_date, grade, feedback =




def save_submissions(submissions):
rows []
for s in submissions:




s['submission_text'],

s['grade'] is
not None




Load certificates
#

def load_certificates():
=
= []
row in rows:
len(row)
course_id,
certificates.append({
                'certificate_id': certificate_id,
                'username': username,
                'course_id': course_id,
                'issue_date': issue_date
            })



save_certificates(certificates):
=
in


c['username'],

c['issue_date']
])






=
e

eid =
except:
=
max_id:

return str(max_id


def generate_new_submission_id(submissions):
max_id = 0
submissions:

int(s['submission_id'])


sid max_id:

str(max_id


def
= 0
for c

cid
except:
0

max_id cid
+


enrollments):
for
if e['username'] == == course_id:

return None


# routes

@app.route('/')

# Redirect dashboard



# Dummy session management
we assume username



@app.route('/dashboard')



users.get(username)
if

fullname =


courses load_courses()
enrolled for user
=
in
e['username'] username:
= e['course_id']



username=username)



def catalog():

course_list



methods=['GET', 'POST'])
def course_details(course_id):
LOGGED_IN_USERNAME

users.get(username)
user:
abort(404)

=
courses.get(course_id)
not course:
abort(404)

enrollments = load_enrollments()
= get_enrollment(username, enrollments)
enrolled not

==
enrolled:
user
new_id generate_new_enrollment_id(enrollments)

enrollments.append({
                'enrollment_id': new_id,
                'username': username,
                'course_id': course_id,
                'enroll_date': enroll_date,
                'progress': 0,
                'status': 'In Progress'
            })
save_enrollments(enrollments)


# and 100%, setting 100% certificate
enrollment['progress']

enrollment['status'] =

# Save update


Check certificate exists
certificates =
cert_exists = username and c['course_id'] course_id in
if not cert_exists:
cert_id = generate_new_certificate_id(certificates)
=

save_certificates(certificates)

course=course, enrolled=enrolled)



def
username =
=
courses

# List only enrolled courses
=
in
if

c = courses.get(cid)
if
enrolled_courses.append({
                    'course_id': cid,
                    'title': c['title'],
                    'progress': e['progress']
                })

render_template('my_courses.html',


@app.route('/my-courses/<course_id>')

username =
enrollments = load_enrollments()
enrollment
not
abort(404)


courses.get(course_id)
if
abort(404)

for
are explicitly the design or
For demonstration create dummy (3 as
lessons [
{'lesson_id': '1', 'title': 'Introduction', 'content': 'Introduction content.'},
{'lesson_id': '2', 'title': 'Intermediate Topic', 'content': 'Intermediate content.'},
{'lesson_id': '3', 'title': 'Advanced Topic', 'content': 'Advanced content.'}


# simulate lessons
# each or 34%

enrollment['progress']
* //

lesson is next incomplete
current_lesson_index completed_lessons_count if completed_lessons_count else total_lessons -
current_lesson lessons[current_lesson_index]

render_template('course_learning.html', course=course, progress=progress)



def assignments():


= load_submissions()

by
= load_enrollments()
set(e['course_id'] username)


for assignments_all:
if enrolled_course_ids:
submission status
= next((s for in if == a['assignment_id'] username),


status


return render_template('my_assignments.html',





= load_assignments()
for None)
not
abort(404)

=
submission = s if s['assignment_id'] assignment_id == username),

if request.method
submission_text
if
# re-render
text required.'
submission_text=submission_text, error=error)





submission_text
= submit_date



Add new submission
new_id
new_submission {
                'submission_id': new_id,
                'assignment_id': assignment_id,
                'username': username,
                'submission_text': submission_text,
                'submit_date': submit_date,
                'grade': None,
                'feedback': None
            }
submissions.append(new_submission)

save_submissions(submissions)
return

GET
= submission['submission_text'] if None
render_template('submit_assignment.html', assignment=assignment,




= LOGGED_IN_USERNAME

= load_courses()

=

if ==
course_title = courses.get(c['course_id'],
user_certificates.append({
                'certificate_id': c['certificate_id'],
                'course_title': course_title,
                'issue_date': c['issue_date']
            })

render_template('certificates.html', certificates=user_certificates)



def user_profile():
username =

= users.get(username)
if not


request.method ==

new_email '').strip()
new_email:



email=user.get('email',



app.run(debug=True,
