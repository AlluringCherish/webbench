from flask import Flask, render_template, request, redirect, url_for, abort
from datetime import datetime
import os

app = Flask(__name__)
app.config['DATA_DIR'] = 'data'

# Utility Functions for file operations and data parsing

def get_data_path(filename):
    return os.path.join(app.config['DATA_DIR'], filename)


def read_pipe_delimited_file(filename):
    path = get_data_path(filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
        if lines == ['']:
            return []
        return [line.split('|') for line in lines]


def write_pipe_delimited_file(filename, rows):
    path = get_data_path(filename)
    lines = ['|'.join(map(str, row)) for row in rows]
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# Users

def load_users():
    users = []
    for fields in read_pipe_delimited_file('users.txt'):
        if len(fields) >= 3:
            users.append({
                'username': fields[0],
                'email': fields[1],
                'fullname': fields[2]
            })
    return users


def save_users(users):
    rows = [(u['username'], u['email'], u['fullname']) for u in users]
    write_pipe_delimited_file('users.txt', rows)


def get_user_by_username(username):
    for user in load_users():
        if user['username'] == username:
            return user
    return None

# Courses

def load_courses():
    courses = []
    for fields in read_pipe_delimited_file('courses.txt'):
        if len(fields) >= 7:
            courses.append({
                'course_id': fields[0],
                'title': fields[1],
                'description': fields[2],
                'category': fields[3],
                'level': fields[4],
                'duration': fields[5],
                'status': fields[6]
            })
    return courses


def get_course_by_id(course_id):
    for course in load_courses():
        if course['course_id'] == course_id:
            return course
    return None

# Enrollments

def load_enrollments():
    enrollments = []
    for fields in read_pipe_delimited_file('enrollments.txt'):
        if len(fields) >= 6:
            enrollments.append({
                'enrollment_id': fields[0],
                'username': fields[1],
                'course_id': fields[2],
                'enrollment_date': fields[3],
                'progress': int(fields[4]),
                'status': fields[5]
            })
    return enrollments


def save_enrollments(enrollments):
    rows = []
    for e in enrollments:
        rows.append((e['enrollment_id'], e['username'], e['course_id'], e['enrollment_date'], str(e['progress']), e['status']))
    write_pipe_delimited_file('enrollments.txt', rows)


def get_enrollment(username, course_id):
    for e in load_enrollments():
        if e['username'] == username and e['course_id'] == course_id:
            return e
    return None

# Assignments

def load_assignments():
    assignments = []
    for fields in read_pipe_delimited_file('assignments.txt'):
        if len(fields) >= 6:
            assignments.append({
                'assignment_id': fields[0],
                'course_id': fields[1],
                'title': fields[2],
                'description': fields[3],
                'due_date': fields[4],
                'max_points': int(fields[5])
            })
    return assignments


def get_assignment_by_id(assignment_id):
    for a in load_assignments():
        if a['assignment_id'] == assignment_id:
            return a
    return None

# Submissions

def load_submissions():
    submissions = []
    for fields in read_pipe_delimited_file('submissions.txt'):
        if len(fields) >= 7:
            submissions.append({
                'submission_id': fields[0],
                'assignment_id': fields[1],
                'username': fields[2],
                'submission_text': fields[3],
                'submit_date': fields[4],
                'grade': fields[5],
                'feedback': fields[6]
            })
    return submissions


def save_submissions(submissions):
    rows = []
    for s in submissions:
        rows.append((s['submission_id'], s['assignment_id'], s['username'], s['submission_text'], s['submit_date'], s['grade'], s['feedback']))
    write_pipe_delimited_file('submissions.txt', rows)


def get_submission(username, assignment_id):
    for s in load_submissions():
        if s['username'] == username and s['assignment_id'] == assignment_id:
            return s
    return None

# Certificates

def load_certificates():
    certificates = []
    for fields in read_pipe_delimited_file('certificates.txt'):
        if len(fields) >= 4:
            certificates.append({
                'certificate_id': fields[0],
                'username': fields[1],
                'course_id': fields[2],
                'issue_date': fields[3]
            })
    return certificates


def save_certificates(certificates):
    rows = []
    for c in certificates:
        rows.append((c['certificate_id'], c['username'], c['course_id'], c['issue_date']))
    write_pipe_delimited_file('certificates.txt', rows)


def certificate_exists(username, course_id):
    for c in load_certificates():
        if c['username'] == username and c['course_id'] == course_id:
            return True
    return False

# Lessons (Assuming each course has a fixed list of lessons hardcoded as lesson_id, title, content)
# The design spec does not provide a data file for lessons, so we simulate lessons per course.

LESSONS_DATA = {
    '1': [
        {'lesson_id': '1', 'title': 'Introduction to Python', 'content': 'Welcome to Python programming!'},
        {'lesson_id': '2', 'title': 'Variables and Data Types', 'content': 'Learn about variables and types.'},
        {'lesson_id': '3', 'title': 'Control Structures', 'content': 'If, for, while loops explained.'},
        {'lesson_id': '4', 'title': 'Functions', 'content': 'Defining and using functions.'},
        {'lesson_id': '5', 'title': 'Modules and Packages', 'content': 'Organizing code with modules.'},
    ],
    '2': [
        {'lesson_id': '1', 'title': 'HTML Basics', 'content': 'Introduction to HTML markup.'},
        {'lesson_id': '2', 'title': 'CSS Basics', 'content': 'Styling with CSS.'},
        {'lesson_id': '3', 'title': 'JavaScript Basics', 'content': 'Interactive web pages using JS.'},
    ],
    '3': [
        {'lesson_id': '1', 'title': 'Data Science Overview', 'content': 'What is Data Science?'},
        {'lesson_id': '2', 'title': 'Python for Data Science', 'content': 'Using Python in data science.'},
        {'lesson_id': '3', 'title': 'Data Analysis Techniques', 'content': 'Techniques for analyzing data.'},
        {'lesson_id': '4', 'title': 'Machine Learning Basics', 'content': 'Intro to ML concepts.'},
    ]
}

# Root redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

# Assuming current user is fixed for demonstration, normally would come from session or login
CURRENT_USERNAME = 'john'

# Dashboard
@app.route('/dashboard')
def dashboard():
    username = CURRENT_USERNAME
    user = get_user_by_username(username)
    if not user:
        abort(404)

    enrollments = load_enrollments()
    user_enrollments = [e for e in enrollments if e['username'] == username]
    courses = load_courses()

    enrolled_courses = []
    for e in user_enrollments:
        course = get_course_by_id(e['course_id'])
        if course:
            enrolled_courses.append({
                'course_id': course['course_id'],
                'title': course['title'],
                'progress': e['progress']
            })

    return render_template('dashboard.html', username=username, fullname=user['fullname'], enrolled_courses=enrolled_courses)

# Course catalog
@app.route('/catalog')
def course_catalog():
    username = CURRENT_USERNAME
    courses = load_courses()
    return render_template('course_catalog.html', username=username, courses=courses)

# Course details
@app.route('/catalog/<course_id>', methods=['GET'])
def course_details(course_id):
    username = CURRENT_USERNAME
    course = get_course_by_id(course_id)
    if not course:
        abort(404)

    enrollment = get_enrollment(username, course_id)
    enrolled = enrollment is not None
    return render_template('course_details.html', username=username, course=course, enrolled=enrolled)

# Enroll course
@app.route('/catalog/<course_id>/enroll', methods=['POST'])
def enroll_course(course_id):
    username = CURRENT_USERNAME
    course = get_course_by_id(course_id)
    if not course:
        abort(404)

    enrollments = load_enrollments()
    already_enrolled = any(e['username'] == username and e['course_id'] == course_id for e in enrollments)
    enroll_success = False
    error_msg = None

    if already_enrolled:
        error_msg = 'Already enrolled in this course.'
    else:
        # Add enrollment
        new_id = 1
        if enrollments:
            new_id = max(int(e['enrollment_id']) for e in enrollments) + 1
        new_enrollment = {
            'enrollment_id': str(new_id),
            'username': username,
            'course_id': course_id,
            'enrollment_date': datetime.now().strftime('%Y-%m-%d'),
            'progress': 0,
            'status': 'In Progress'
        }
        enrollments.append(new_enrollment)
        save_enrollments(enrollments)
        enroll_success = True

    enrollment = get_enrollment(username, course_id)
    enrolled = enrollment is not None
    return render_template('course_details.html', username=username, course=course, enrolled=enrolled, enroll_success=enroll_success, error_msg=error_msg)

# My courses
@app.route('/my-courses')
def my_courses():
    username = CURRENT_USERNAME
    enrollments = load_enrollments()
    user_enrollments = [e for e in enrollments if e['username'] == username]
    courses = []
    for e in user_enrollments:
        course = get_course_by_id(e['course_id'])
        if course:
            courses.append({
                'course_id': course['course_id'],
                'title': course['title'],
                'progress': e['progress']
            })
    return render_template('my_courses.html', username=username, courses=courses)

# Course learning
@app.route('/learning/<course_id>', methods=['GET'])
def course_learning(course_id):
    username = CURRENT_USERNAME
    course = get_course_by_id(course_id)
    if not course:
        abort(404)

    enrollment = get_enrollment(username, course_id)
    if not enrollment:
        return redirect(url_for('course_details', course_id=course_id))

    lessons = LESSONS_DATA.get(course_id, [])
    completed_lessons = []
    # Determine completed lessons by progress
    completed_count = int(enrollment['progress'] * len(lessons) / 100) if lessons else 0
    if completed_count > len(lessons):
        completed_count = len(lessons)
    completed_lessons = [lesson['lesson_id'] for lesson in lessons[:completed_count]]

    # Determine current lesson to display: next lesson after completed lessons
    current_lesson_id = None
    if completed_count < len(lessons):
        current_lesson_id = lessons[completed_count]['lesson_id']
    elif lessons:
        current_lesson_id = lessons[-1]['lesson_id']

    return render_template('course_learning.html', username=username, course={'title': course['title']}, lessons=lessons, current_lesson_id=current_lesson_id, completed_lessons=completed_lessons, progress=enrollment['progress'])

# Mark lesson complete
@app.route('/learning/<course_id>/mark-complete', methods=['POST'])
def mark_lesson_complete(course_id):
    username = CURRENT_USERNAME
    course = get_course_by_id(course_id)
    if not course:
        abort(404)

    enrollment = get_enrollment(username, course_id)
    if not enrollment:
        abort(403)

    lessons = LESSONS_DATA.get(course_id, [])
    if not lessons:
        abort(404)

    completed_count = int(enrollment['progress'] * len(lessons) / 100) if lessons else 0
    if completed_count > len(lessons):
        completed_count = len(lessons)

    # Next lesson to complete is lessons[completed_count]
    if completed_count >= len(lessons):
        # All lessons completed
        current_lesson_id = lessons[-1]['lesson_id']
        return redirect(url_for('course_learning', course_id=course_id))

    next_lesson = lessons[completed_count]

    # Mark the lesson complete (i.e. increase completed count by 1)
    new_completed_count = completed_count + 1
    progress = int(new_completed_count * 100 / len(lessons))

    # Update enrollment progress
    enrollments = load_enrollments()
    updated = False
    for e in enrollments:
        if e['username'] == username and e['course_id'] == course_id:
            e['progress'] = progress
            if progress == 100:
                e['status'] = 'Completed'
            updated = True
            break
    if updated:
        save_enrollments(enrollments)

    # Check if certificate needed
    completion_certificate_generated = False
    if progress == 100 and not certificate_exists(username, course_id):
        certificates = load_certificates()
        new_cert_id = 1
        if certificates:
            new_cert_id = max(int(c['certificate_id']) for c in certificates) + 1
        new_cert = {
            'certificate_id': str(new_cert_id),
            'username': username,
            'course_id': course_id,
            'issue_date': datetime.now().strftime('%Y-%m-%d')
        }
        certificates.append(new_cert)
        save_certificates(certificates)
        completion_certificate_generated = True

    # Reload completed lessons
    completed_lessons = [lesson['lesson_id'] for lesson in lessons[:new_completed_count]]

    return render_template('course_learning.html', username=username, course={'title': course['title']}, lessons=lessons, current_lesson_id=next_lesson['lesson_id'], completed_lessons=completed_lessons, progress=progress, completion_certificate_generated=completion_certificate_generated)

# My assignments
@app.route('/assignments')
def my_assignments():
    username = CURRENT_USERNAME
    assignments = load_assignments()

    # For each assignment determine status (Submitted or Pending)
    submissions = load_submissions()
    user_submissions = {s['assignment_id']: s for s in submissions if s['username'] == username}

    assignment_list = []
    for a in assignments:
        status = 'Pending'
        if a['assignment_id'] in user_submissions:
            status = 'Submitted'
        assignment_list.append({
            'assignment_id': a['assignment_id'],
            'title': a['title'],
            'description': a['description'],
            'due_date': a['due_date'],
            'max_points': a['max_points'],
            'status': status
        })

    return render_template('my_assignments.html', username=username, assignments=assignment_list)

# Submit assignment page
@app.route('/assignments/<assignment_id>/submit', methods=['GET'])
def submit_assignment_page(assignment_id):
    username = CURRENT_USERNAME
    assignment = get_assignment_by_id(assignment_id)
    if not assignment:
        abort(404)
    return render_template('submit_assignment.html', username=username, assignment=assignment)

# Submit assignment POST
@app.route('/assignments/<assignment_id>/submit', methods=['POST'])
def submit_assignment(assignment_id):
    username = CURRENT_USERNAME
    assignment = get_assignment_by_id(assignment_id)
    if not assignment:
        abort(404)

    submission_text = request.form.get('submission_text', '').strip()
    if not submission_text:
        return render_template('submit_assignment.html', username=username, assignment=assignment, submission_success=False, error_msg='Submission text cannot be empty.')

    submissions = load_submissions()
    existing_submission = get_submission(username, assignment_id)

    if existing_submission:
        return render_template('submit_assignment.html', username=username, assignment=assignment, submission_success=False, error_msg='You have already submitted this assignment.')

    new_id = 1
    if submissions:
        new_id = max(int(s['submission_id']) for s in submissions) + 1

    new_submission = {
        'submission_id': str(new_id),
        'assignment_id': assignment_id,
        'username': username,
        'submission_text': submission_text,
        'submit_date': datetime.now().strftime('%Y-%m-%d'),
        'grade': '',
        'feedback': ''
    }
    submissions.append(new_submission)
    save_submissions(submissions)

    return render_template('submit_assignment.html', username=username, assignment=assignment, submission_success=True)

# My certificates
@app.route('/certificates')
def my_certificates():
    username = CURRENT_USERNAME
    certificates = load_certificates()
    user_certificates = [c for c in certificates if c['username'] == username]

    courses = load_courses()
    courses_dict = {c['course_id']: c for c in courses}

    certs_display = []
    for c in user_certificates:
        course = courses_dict.get(c['course_id'])
        if course:
            certs_display.append({
                'course_id': c['course_id'],
                'title': course['title'],
                'issue_date': c['issue_date']
            })

    return render_template('certificates.html', username=username, certificates=certs_display)

# User profile
@app.route('/profile')
def user_profile():
    username = CURRENT_USERNAME
    user = get_user_by_username(username)
    if not user:
        abort(404)

    return render_template('user_profile.html', username=username, email=user['email'], fullname=user['fullname'])

# Update profile
@app.route('/profile/update', methods=['POST'])
def update_profile():
    username = CURRENT_USERNAME
    users = load_users()

    email = request.form.get('email', '').strip()
    fullname = request.form.get('fullname', '').strip()

    if not email or not fullname:
        user = get_user_by_username(username)
        return render_template('user_profile.html', username=username, email=user['email'], fullname=user['fullname'], update_success=False, error_msg='Email and Fullname cannot be empty.')

    # Update user info
    updated = False
    for u in users:
        if u['username'] == username:
            u['email'] = email
            u['fullname'] = fullname
            updated = True
            break

    if updated:
        save_users(users)

    return render_template('user_profile.html', username=username, email=email, fullname=fullname, update_success=updated)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
