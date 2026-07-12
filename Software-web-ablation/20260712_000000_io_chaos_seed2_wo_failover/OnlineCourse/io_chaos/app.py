from flask import Flask, render_template, request, redirect, url_for, abort
import os
from datetime import datetime

app = Flask(__name__)

data_path = 'data'


# Utility functions for file reading and writing with pipe-delimited fields

def read_pipe_file(filename):
    full_path = os.path.join(data_path, filename)
    if not os.path.exists(full_path):
        return []
    with open(full_path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
    return lines


def write_pipe_file(filename, lines):
    full_path = os.path.join(data_path, filename)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines)+'\n' if lines else '')


# USERS
# Fields: username|email|fullname

def read_users():
    lines = read_pipe_file('users.txt')
    users = {}
    for line in lines:
        parts = line.split('|')
        if len(parts) < 3:
            continue
        username, email, fullname = parts
        users[username] = {
            'username': username,
            'email': email,
            'fullname': fullname
        }
    return users


def save_users(users):
    lines = []
    for u in users.values():
        lines.append(f"{u['username']}|{u['email']}|{u['fullname']}")
    write_pipe_file('users.txt', lines)


# COURSES
# Fields: course_id|title|description|category|level|duration|status

def read_courses():
    lines = read_pipe_file('courses.txt')
    courses = {}
    for line in lines:
        parts = line.split('|')
        if len(parts) < 7:
            continue
        course_id = int(parts[0])
        courses[course_id] = {
            'course_id': course_id,
            'title': parts[1],
            'description': parts[2],
            'category': parts[3],
            'level': parts[4],
            'duration': parts[5],
            'status': parts[6]
        }
    return courses


# ENROLLMENTS
# Fields: enrollment_id|username|course_id|enrollment_date|progress|status

def read_enrollments():
    lines = read_pipe_file('enrollments.txt')
    enrollments = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < 6:
            continue
        enrollment_id = int(parts[0])
        enrollments.append({
            'enrollment_id': enrollment_id,
            'username': parts[1],
            'course_id': int(parts[2]),
            'enrollment_date': parts[3],
            'progress': int(parts[4]),
            'status': parts[5]
        })
    return enrollments


def save_enrollments(enrollments):
    lines = []
    for e in enrollments:
        lines.append(f"{e['enrollment_id']}|{e['username']}|{e['course_id']}|{e['enrollment_date']}|{e['progress']}|{e['status']}")
    write_pipe_file('enrollments.txt', lines)


# ASSIGNMENTS
# Fields: assignment_id|course_id|title|description|due_date|max_points

def read_assignments():
    lines = read_pipe_file('assignments.txt')
    assignments = {}
    for line in lines:
        parts = line.split('|')
        if len(parts) < 6:
            continue
        assignment_id = int(parts[0])
        assignments[assignment_id] = {
            'assignment_id': assignment_id,
            'course_id': int(parts[1]),
            'title': parts[2],
            'description': parts[3],
            'due_date': parts[4],
            'max_points': int(parts[5])
        }
    return assignments


# SUBMISSIONS
# Fields: submission_id|assignment_id|username|submission_text|submit_date|grade|feedback

def read_submissions():
    lines = read_pipe_file('submissions.txt')
    submissions = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < 7:
            continue
        submission_id = int(parts[0])
        submissions.append({
            'submission_id': submission_id,
            'assignment_id': int(parts[1]),
            'username': parts[2],
            'submission_text': parts[3],
            'submit_date': parts[4],
            'grade': int(parts[5]),
            'feedback': parts[6]
        })
    return submissions


def save_submissions(submissions):
    lines = []
    for s in submissions:
        lines.append(f"{s['submission_id']}|{s['assignment_id']}|{s['username']}|{s['submission_text']}|{s['submit_date']}|{s['grade']}|{s['feedback']}")
    write_pipe_file('submissions.txt', lines)


# CERTIFICATES
# Fields: certificate_id|username|course_id|issue_date

def read_certificates():
    lines = read_pipe_file('certificates.txt')
    certificates = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < 4:
            continue
        certificate_id = int(parts[0])
        certificates.append({
            'certificate_id': certificate_id,
            'username': parts[1],
            'course_id': int(parts[2]),
            'issue_date': parts[3]
        })
    return certificates


def save_certificates(certificates):
    lines = []
    for c in certificates:
        lines.append(f"{c['certificate_id']}|{c['username']}|{c['course_id']}|{c['issue_date']}")
    write_pipe_file('certificates.txt', lines)


# LESSONS DATA - Not in specification files. We'll simulate lessons by course from assignments:
# But assignments are different from lessons. Since no lessons file described, we will simulate lessons as dummy data for course_learning route.
# For demo purposes, we simulate lessons count and fixed content.

# We'll simulate lessons as 5 lessons per course with sequential IDs 1..5 with title "Lesson X" and content "Content for Lesson X."

def get_lessons_for_course(course_id):
    lessons = []
    for i in range(1, 6):
        lessons.append({
            'lesson_id': i,
            'title': f"Lesson {i}",
            'content': f"Content for Lesson {i}."
        })
    return lessons


# Helper: Get current user from session or request (for demo hardcoded username)
# Since spec does not define auth, we simulate logged-in user by fixed username

def get_current_username():
    # For demo/testing, we will default to 'john'
    # In real app, session or login would provide this
    return 'john'


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = get_current_username()
    users = read_users()
    if username not in users:
        abort(404)
    fullname = users[username]['fullname']

    enrollments = read_enrollments()
    courses = read_courses()

    # Get user's enrolled courses with progress
    enrolled_courses = []
    for e in enrollments:
        if e['username'] == username:
            cid = e['course_id']
            enrolled_courses.append({
                'course_id': cid,
                'title': courses[cid]['title'] if cid in courses else 'Unknown',
                'progress': e['progress']
            })

    return render_template('dashboard.html', username=username, fullname=fullname, enrolled_courses=enrolled_courses)


@app.route('/catalog')
def course_catalog():
    username = get_current_username()
    users = read_users()
    if username not in users:
        abort(404)

    courses = read_courses()
    # Convert dict to list for template
    courses_list = list(courses.values())

    return render_template('course_catalog.html', username=username, courses=courses_list)


@app.route('/course/<int:course_id>', methods=['GET', 'POST'])
def course_details(course_id):
    username = get_current_username()
    users = read_users()
    if username not in users:
        abort(404)

    courses = read_courses()
    if course_id not in courses:
        abort(404)
    course = courses[course_id]

    enrollments = read_enrollments()

    # Check if user is enrolled in course
    enrolled = False
    enrollment_date = None
    for e in enrollments:
        if e['username'] == username and e['course_id'] == course_id:
            enrolled = True
            enrollment_date = e['enrollment_date']
            break

    if request.method == 'POST':
        # Enroll user if not enrolled
        if not enrolled:
            # Generate new enrollment_id
            max_enroll_id = max([e['enrollment_id'] for e in enrollments], default=0)
            new_enrollment_id = max_enroll_id + 1
            today = datetime.now().strftime('%Y-%m-%d')
            new_enrollment = {
                'enrollment_id': new_enrollment_id,
                'username': username,
                'course_id': course_id,
                'enrollment_date': today,
                'progress': 0,
                'status': 'In Progress'
            }
            enrollments.append(new_enrollment)
            save_enrollments(enrollments)
            enrolled = True
            enrollment_date = today

    return render_template('course_details.html', username=username, course=course, enrolled=enrolled, enrollment_date=enrollment_date)


@app.route('/my-courses')
def my_courses():
    username = get_current_username()
    users = read_users()
    if username not in users:
        abort(404)

    enrollments = read_enrollments()
    courses = read_courses()

    enrolled_courses = []
    for e in enrollments:
        if e['username'] == username:
            cid = e['course_id']
            enrolled_courses.append({
                'course_id': cid,
                'title': courses[cid]['title'] if cid in courses else 'Unknown',
                'progress': e['progress']
            })

    return render_template('my_courses.html', username=username, enrolled_courses=enrolled_courses)


@app.route('/learn/<int:course_id>', methods=['GET', 'POST'])
def course_learning(course_id):
    username = get_current_username()
    users = read_users()
    if username not in users:
        abort(404)

    courses = read_courses()
    if course_id not in courses:
        abort(404)
    course = courses[course_id]

    enrollments = read_enrollments()
    enrollment = None
    for e in enrollments:
        if e['username'] == username and e['course_id'] == course_id:
            enrollment = e
            break

    if enrollment is None:
        # User not enrolled, redirect to course_details
        return redirect(url_for('course_details', course_id=course_id))

    lessons = get_lessons_for_course(course_id)

    completed_lessons = []
    # Determine completed lessons by progress % 0-100 divided by 20 per lesson (5 lessons)
    # progress 0 -> none complete, progress 20 -> lesson1 complete, etc.
    progress = enrollment['progress']
    completed_count = progress // 20
    completed_lessons = [l['lesson_id'] for l in lessons[:completed_count]]

    # Current lesson is first incomplete lesson
    if completed_count < len(lessons):
        current_lesson = lessons[completed_count]
    else:
        current_lesson = lessons[-1]

    can_mark_complete = False
    if request.method == 'POST':
        # Mark current lesson complete, only if current lesson not already complete
        if completed_count < len(lessons):
            # Update enrollment progress
            completed_count += 1
            new_progress = min(completed_count * 20, 100)
            enrollment['progress'] = new_progress
            # Save enrollments
            save_enrollments(enrollments)

            # If progress 100%, update status and generate certificate if not exist
            if new_progress == 100 and enrollment['status'] != 'Completed':
                enrollment['status'] = 'Completed'
                # Save updated enrollments
                save_enrollments(enrollments)

                # Generate certificate if not already
                certificates = read_certificates()
                cert_exists = False
                for c in certificates:
                    if c['username'] == username and c['course_id'] == course_id:
                        cert_exists = True
                        break
                if not cert_exists:
                    max_cert_id = max([c['certificate_id'] for c in certificates], default=0)
                    cert_id = max_cert_id + 1
                    today = datetime.now().strftime('%Y-%m-%d')
                    certificates.append({
                        'certificate_id': cert_id,
                        'username': username,
                        'course_id': course_id,
                        'issue_date': today
                    })
                    save_certificates(certificates)

            return redirect(url_for('course_learning', course_id=course_id))

    # can_mark_complete only if current lesson is not complete
    can_mark_complete = completed_count < len(lessons)

    return render_template(
        'course_learning.html',
        username=username,
        course=course,
        lessons=lessons,
        current_lesson=current_lesson,
        completed_lessons=completed_lessons,
        progress=progress,
        can_mark_complete=can_mark_complete
    )


@app.route('/assignments')
def my_assignments():
    username = get_current_username()
    users = read_users()
    if username not in users:
        abort(404)

    assignments = read_assignments()
    submissions = read_submissions()

    # Filter assignments for courses the user is enrolled in
    enrollments = read_enrollments()
    user_course_ids = {e['course_id'] for e in enrollments if e['username'] == username}
    user_assignments = [a for a in assignments.values() if a['course_id'] in user_course_ids]

    # Build submissions dict keyed by assignment_id for user's submissions
    submissions_dict = {}
    for sub in submissions:
        if sub['username'] == username:
            submissions_dict[sub['assignment_id']] = {
                'submission_id': sub['submission_id'],
                'submission_text': sub['submission_text'],
                'submit_date': sub['submit_date'],
                'grade': sub['grade'],
                'feedback': sub['feedback']
            }

    return render_template('my_assignments.html', username=username, assignments=user_assignments, submissions=submissions_dict)


@app.route('/submit-assignment/<int:assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    username = get_current_username()
    users = read_users()
    if username not in users:
        abort(404)

    assignments = read_assignments()
    if assignment_id not in assignments:
        abort(404)
    assignment = assignments[assignment_id]

    submissions = read_submissions()

    submission_status = None
    # Check if user already submitted this assignment
    submission = None
    for sub in submissions:
        if sub['username'] == username and sub['assignment_id'] == assignment_id:
            submission = sub
            submission_status = 'Submitted'
            break

    if request.method == 'POST':
        submission_text = request.form.get('submission_text', '').strip()
        if submission_text == '':
            submission_status = 'Please enter submission text.'
        else:
            today = datetime.now().strftime('%Y-%m-%d')
            if submission is None:
                max_sub_id = max([s['submission_id'] for s in submissions], default=0)
                new_sub_id = max_sub_id + 1
                # Grade and feedback default to 0 and empty (since grading not described)
                new_submission = {
                    'submission_id': new_sub_id,
                    'assignment_id': assignment_id,
                    'username': username,
                    'submission_text': submission_text.replace('|',' '),
                    'submit_date': today,
                    'grade': 0,
                    'feedback': ''
                }
                submissions.append(new_submission)
            else:
                # Update existing submission
                submission['submission_text'] = submission_text.replace('|',' ')
                submission['submit_date'] = today
            save_submissions(submissions)
            submission_status = 'Submitted'

    return render_template('submit_assignment.html', username=username, assignment=assignment, submission_status=submission_status)


@app.route('/certificates')
def certificates():
    username = get_current_username()
    users = read_users()
    if username not in users:
        abort(404)

    certificates = read_certificates()
    courses = read_courses()

    user_certs = []
    for c in certificates:
        if c['username'] == username:
            course_title = courses[c['course_id']]['title'] if c['course_id'] in courses else 'Unknown'
            user_certs.append({
                'certificate_id': c['certificate_id'],
                'course_id': c['course_id'],
                'issue_date': c['issue_date'],
                'course_title': course_title
            })

    return render_template('certificates.html', username=username, certificates=user_certs)


@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    username = get_current_username()
    users = read_users()
    if username not in users:
        abort(404)

    user = users[username]
    update_status = None

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        fullname = request.form.get('fullname', '').strip()
        if email == '' or fullname == '':
            update_status = 'Email and Full Name cannot be empty.'
        else:
            user['email'] = email
            user['fullname'] = fullname
            save_users(users)
            update_status = 'Profile updated successfully.'

    return render_template('profile.html', username=username, email=user['email'], fullname=user['fullname'], update_status=update_status)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
