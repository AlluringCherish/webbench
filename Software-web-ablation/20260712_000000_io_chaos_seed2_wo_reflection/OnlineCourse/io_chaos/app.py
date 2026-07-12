from flask import Flask, render_template, redirect, url_for, request
from datetime import date
import os

app = Flask(__name__)

# Data file paths
USERS_FILE = 'data/users.txt'
COURSES_FILE = 'data/courses.txt'
ENROLLMENTS_FILE = 'data/enrollments.txt'
ASSIGNMENTS_FILE = 'data/assignments.txt'
SUBMISSIONS_FILE = 'data/submissions.txt'
CERTIFICATES_FILE = 'data/certificates.txt'

# Helper functions to read and write pipe-delimited data

def read_pipe_delimited_file(filename, fields_count):
    data = []
    if not os.path.exists(filename):
        return data
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != fields_count:
                continue
            data.append(parts)
    return data

def write_pipe_delimited_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        for record in data:
            f.write('|'.join(str(x) for x in record) + '\n')

# Users
# username|email|fullname

def load_users():
    lines = read_pipe_delimited_file(USERS_FILE, 3)
    users = {}
    for username, email, fullname in lines:
        users[username] = {'username': username, 'email': email, 'fullname': fullname}
    return users

# Courses
# course_id|title|description|category|level|duration|status

def load_courses():
    lines = read_pipe_delimited_file(COURSES_FILE,7)
    courses = {}
    for course_id, title, description, category, level, duration, status in lines:
        try:
            cid = int(course_id)
        except:
            continue
        courses[cid] = {'course_id': cid, 'title': title, 'description': description, 'category': category, 'level': level, 'duration': duration, 'status': status}
    return courses

# Enrollments
# enrollment_id|username|course_id|enrollment_date|progress|status

def load_enrollments():
    lines = read_pipe_delimited_file(ENROLLMENTS_FILE, 6)
    enrollments = []
    for enrollment_id, username, course_id, enrollment_date, progress, status in lines:
        try:
            eid = int(enrollment_id)
            cid = int(course_id)
            prog = int(progress)
        except:
            continue
        enrollments.append({
            'enrollment_id': eid,
            'username': username,
            'course_id': cid,
            'enrollment_date': enrollment_date,
            'progress': prog,
            'status': status
        })
    return enrollments

def save_enrollments(enrollments):
    lines = []
    for e in enrollments:
        lines.append([
            e['enrollment_id'], e['username'], e['course_id'], e['enrollment_date'], e['progress'], e['status']
        ])
    write_pipe_delimited_file(ENROLLMENTS_FILE, lines)

# Assignments
# assignment_id|course_id|title|description|due_date|max_points

def load_assignments():
    lines = read_pipe_delimited_file(ASSIGNMENTS_FILE, 6)
    assignments = []
    for assignment_id, course_id, title, description, due_date, max_points in lines:
        try:
            aid = int(assignment_id)
            cid = int(course_id)
            maxp = int(max_points)
        except:
            continue
        assignments.append({
            'assignment_id': aid,
            'course_id': cid,
            'title': title,
            'description': description,
            'due_date': due_date,
            'max_points': maxp
        })
    return assignments

# Submissions
# submission_id|assignment_id|username|submission_text|submit_date|grade|feedback

def load_submissions():
    lines = read_pipe_delimited_file(SUBMISSIONS_FILE, 7)
    submissions = []
    for submission_id, assignment_id, username, submission_text, submit_date, grade, feedback in lines:
        try:
            sid = int(submission_id)
            aid = int(assignment_id)
            grd = int(grade)
        except:
            continue
        submissions.append({
            'submission_id': sid,
            'assignment_id': aid,
            'username': username,
            'submission_text': submission_text,
            'submit_date': submit_date,
            'grade': grd,
            'feedback': feedback
        })
    return submissions

def save_submissions(submissions):
    lines = []
    for s in submissions:
        lines.append([
            s['submission_id'], s['assignment_id'], s['username'], s['submission_text'], s['submit_date'], s['grade'], s['feedback']
        ])
    write_pipe_delimited_file(SUBMISSIONS_FILE, lines)

# Certificates
# certificate_id|username|course_id|issue_date

def load_certificates():
    lines = read_pipe_delimited_file(CERTIFICATES_FILE, 4)
    certs = []
    for certificate_id, username, course_id, issue_date in lines:
        try:
            cid = int(certificate_id)
            coid = int(course_id)
        except:
            continue
        certs.append({
            'certificate_id': cid,
            'username': username,
            'course_id': coid,
            'issue_date': issue_date
        })
    return certs

def save_certificates(certs):
    lines = []
    for c in certs:
        lines.append([
            c['certificate_id'], c['username'], c['course_id'], c['issue_date']
        ])
    write_pipe_delimited_file(CERTIFICATES_FILE, lines)

# Utility to get next id by max existing id

def get_next_id(records, id_field):
    if not records:
        return 1
    return max(r[id_field] for r in records) + 1

# Fake current user for demonstration (normally from session)
CURRENT_USERNAME = 'john'

# Assumed lessons for courses (since lessons are not defined in design)
# We'll mock some lessons per course_id
LESSONS = {
    1: [
        {'lesson_id': 1, 'title': 'Introduction to Python', 'content': 'Welcome to Python programming!'},
        {'lesson_id': 2, 'title': 'Variables and Data Types', 'content': 'Learn about variables and data types.'},
        {'lesson_id': 3, 'title': 'Control Flow', 'content': 'If statements, loops, and more.'}
    ],
    2: [
        {'lesson_id': 1, 'title': 'Intro to Web Development', 'content': 'Building basics of websites.'},
        {'lesson_id': 2, 'title': 'HTML and CSS', 'content': 'Styling your webpage.'}
    ],
    3: [
        {'lesson_id': 1, 'title': 'Data Science Overview', 'content': 'Introduction to data science concepts.'},
        {'lesson_id': 2, 'title': 'Data Analysis Tools', 'content': 'Using libraries to analyze data.'},
        {'lesson_id': 3, 'title': 'Machine Learning Basics', 'content': 'Basic ML concepts.'}
    ]
}

# Routes Implementation

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    users = load_users()
    courses = load_courses()
    enrollments = load_enrollments()

    user = users.get(CURRENT_USERNAME)
    if not user:
        return "User not found", 404

    # Get enrolled courses for this user
    enrolled_courses = []
    for e in enrollments:
        if e['username'] == CURRENT_USERNAME:
            c = courses.get(e['course_id'])
            if c:
                enrolled_courses.append({
                    'course_id': c['course_id'],
                    'title': c['title'],
                    'progress': e['progress']
                })

    return render_template('dashboard.html', username=CURRENT_USERNAME, fullname=user['fullname'], enrolled_courses=enrolled_courses)

@app.route('/catalog')
def course_catalog():
    courses = load_courses()
    courses_list = list(courses.values())
    return render_template('catalog.html', courses=courses_list)

@app.route('/course/<int:course_id>')
def course_details(course_id):
    courses = load_courses()
    enrollments = load_enrollments()
    course = courses.get(course_id)
    if not course:
        return "Course not found", 404

    is_enrolled = any(e for e in enrollments if e['username'] == CURRENT_USERNAME and e['course_id'] == course_id)

    return render_template('course_details.html', course=course, is_enrolled=is_enrolled)

@app.route('/course/<int:course_id>/enroll', methods=['POST'])
def enroll_course(course_id):
    users = load_users()
    courses = load_courses()
    enrollments = load_enrollments()

    course = courses.get(course_id)
    if not course:
        return "Course not found", 404

    # Check if already enrolled
    existing = [e for e in enrollments if e['username'] == CURRENT_USERNAME and e['course_id'] == course_id]
    if existing:
        is_enrolled = True
        message = "You are already enrolled in this course."
    else:
        # Add new enrollment
        new_enrollment_id = get_next_id(enrollments, 'enrollment_id')
        enrollment_date = date.today().isoformat()
        enrollments.append({
            'enrollment_id': new_enrollment_id,
            'username': CURRENT_USERNAME,
            'course_id': course_id,
            'enrollment_date': enrollment_date,
            'progress': 0,
            'status': 'In Progress'
        })
        save_enrollments(enrollments)
        is_enrolled = True
        message = "Enrollment successful!"

    return render_template('course_details.html', course=course, is_enrolled=is_enrolled, message=message)

@app.route('/my-courses')
def my_courses():
    enrollments = load_enrollments()
    courses = load_courses()

    enrolled_courses = []
    for e in enrollments:
        if e['username'] == CURRENT_USERNAME:
            c = courses.get(e['course_id'])
            if c:
                enrolled_courses.append({
                    'course_id': c['course_id'],
                    'title': c['title'],
                    'progress': e['progress']
                })

    return render_template('my_courses.html', enrolled_courses=enrolled_courses)

@app.route('/learning/<int:course_id>')
def course_learning(course_id):
    courses = load_courses()
    enrollments = load_enrollments()

    course = courses.get(course_id)
    if not course:
        return "Course not found", 404

    # Check enrollment
    enrollment = next((e for e in enrollments if e['username'] == CURRENT_USERNAME and e['course_id'] == course_id), None)
    if not enrollment:
        return redirect(url_for('course_details', course_id=course_id))

    lessons = LESSONS.get(course_id, [])

    # Determine completed lessons based on progress percent
    completed_lessons = []
    progress = enrollment['progress']
    num_lessons = len(lessons)
    if num_lessons == 0:
        current_lesson_id = None
    else:
        completed_count = (progress * num_lessons) // 100
        # completed lessons are 1-based lesson_id from 1 up to completed_count
        completed_lessons = list(range(1, completed_count+1))
        # Current lesson is next not completed
        current_lesson_id = completed_count + 1 if completed_count < num_lessons else num_lessons

    return render_template('course_learning.html', course=course, lessons=lessons, current_lesson_id=current_lesson_id,
                           completed_lessons=completed_lessons, progress=progress)

@app.route('/learning/<int:course_id>/complete-lesson', methods=['POST'])
def complete_lesson(course_id):
    enrollments = load_enrollments()
    courses = load_courses()

    course = courses.get(course_id)
    if not course:
        return "Course not found", 404

    # Get enrollment
    enrollment = next((e for e in enrollments if e['username'] == CURRENT_USERNAME and e['course_id'] == course_id), None)
    if not enrollment:
        return redirect(url_for('course_details', course_id=course_id))

    lessons = LESSONS.get(course_id, [])
    num_lessons = len(lessons)
    if num_lessons == 0:
        # No lessons to complete
        return redirect(url_for('course_learning', course_id=course_id))

    # Calculate completed lessons
    progress = enrollment['progress']
    completed_count = (progress * num_lessons) // 100
    current_lesson_id = completed_count + 1 if completed_count < num_lessons else None

    if current_lesson_id is None:
        # All lessons completed
        message = "All lessons already completed."
    else:
        # Complete current lesson
        if current_lesson_id <= num_lessons:
            # Update progress
            completed_count += 1
            new_progress = (completed_count * 100) // num_lessons
            if new_progress > 100:
                new_progress = 100

            # Update enrollment
            for e in enrollments:
                if e['enrollment_id'] == enrollment['enrollment_id']:
                    e['progress'] = new_progress
                    if new_progress == 100:
                        e['status'] = 'Completed'
                    else:
                        e['status'] = 'In Progress'
                    break

            # If progress reached 100%, issue certificate if not exists
            if new_progress == 100:
                certificates = load_certificates()
                cert_exists = any(c for c in certificates if c['username'] == CURRENT_USERNAME and c['course_id'] == course_id)
                if not cert_exists:
                    new_cert_id = get_next_id(certificates, 'certificate_id')
                    issue_date = date.today().isoformat()
                    certificates.append({
                        'certificate_id': new_cert_id,
                        'username': CURRENT_USERNAME,
                        'course_id': course_id,
                        'issue_date': issue_date
                    })
                    save_certificates(certificates)

            save_enrollments(enrollments)
            message = "Lesson completed successfully."
        else:
            message = "Invalid lesson completion request."

    # Recalculate progress and state for rendering
    updated_enrollment = next(e for e in enrollments if e['username'] == CURRENT_USERNAME and e['course_id'] == course_id)
    updated_progress = updated_enrollment['progress']
    completed_lessons = list(range(1, (updated_progress * num_lessons)//100 + 1))
    current_lesson_id = (updated_progress * num_lessons)//100 + 1
    if current_lesson_id > num_lessons:
        current_lesson_id = num_lessons

    return render_template('course_learning.html', course=course, lessons=lessons, current_lesson_id=current_lesson_id,
                           completed_lessons=completed_lessons, progress=updated_progress, message=message)

@app.route('/assignments')
def my_assignments():
    assignments = load_assignments()
    submissions = load_submissions()

    # Only assignments for courses user is enrolled in
    enrollments = load_enrollments()
    enrolled_course_ids = {e['course_id'] for e in enrollments if e['username'] == CURRENT_USERNAME}

    filtered_assignments = [a for a in assignments if a['course_id'] in enrolled_course_ids]

    # Prepare submissions for this user
    user_submissions = [s for s in submissions if s['username'] == CURRENT_USERNAME]

    return render_template('assignments.html', assignments=filtered_assignments, submissions=user_submissions)

@app.route('/submit-assignment/<int:assignment_id>', methods=['GET'])
def submit_assignment(assignment_id):
    assignments = load_assignments()
    assignment = next((a for a in assignments if a['assignment_id'] == assignment_id), None)
    if not assignment:
        return "Assignment not found", 404

    message = ""
    return render_template('submit_assignment.html', assignment=assignment, username=CURRENT_USERNAME, message=message)

@app.route('/submit-assignment/<int:assignment_id>', methods=['POST'])
def submit_assignment_post(assignment_id):
    assignments = load_assignments()
    assignment = next((a for a in assignments if a['assignment_id'] == assignment_id), None)
    if not assignment:
        return "Assignment not found", 404

    submission_text = request.form.get('submission_text', '').strip()
    if not submission_text:
        message = "Submission text cannot be empty."
        return render_template('submit_assignment.html', assignment=assignment, username=CURRENT_USERNAME, message=message)

    submissions = load_submissions()
    new_submission_id = get_next_id(submissions, 'submission_id')
    submit_date = date.today().isoformat()

    submissions.append({
        'submission_id': new_submission_id,
        'assignment_id': assignment_id,
        'username': CURRENT_USERNAME,
        'submission_text': submission_text,
        'submit_date': submit_date,
        'grade': 0,
        'feedback': ''
    })

    save_submissions(submissions)

    message = "Assignment submitted successfully."
    return render_template('submit_assignment.html', assignment=assignment, username=CURRENT_USERNAME, message=message)

@app.route('/certificates')
def certificates():
    certificates = load_certificates()
    courses = load_courses()

    user_certs = []
    for c in certificates:
        if c['username'] == CURRENT_USERNAME:
            course = courses.get(c['course_id'])
            if course:
                user_certs.append({
                    'certificate_id': c['certificate_id'],
                    'course_id': c['course_id'],
                    'title': course['title'],
                    'issue_date': c['issue_date']
                })

    return render_template('certificates.html', certificates=user_certs)

@app.route('/profile')
def profile():
    users = load_users()
    user = users.get(CURRENT_USERNAME)
    if not user:
        return "User not found", 404

    return render_template('profile.html', username=CURRENT_USERNAME, email=user['email'], fullname=user['fullname'], message='')

@app.route('/profile/update', methods=['POST'])
def update_profile():
    email = request.form.get('profile-email', '').strip()
    fullname = request.form.get('profile-fullname', '').strip()

    users = load_users()
    user = users.get(CURRENT_USERNAME)
    if not user:
        return "User not found", 404

    if not email or not fullname:
        message = 'Email and fullname cannot be empty.'
        return render_template('profile.html', username=CURRENT_USERNAME, email=user['email'], fullname=user['fullname'], message=message)

    # Update user info
    user['email'] = email
    user['fullname'] = fullname

    # Save back all users
    all_user_data = [[u['username'], u['email'], u['fullname']] for u in users.values()]
    write_pipe_delimited_file(USERS_FILE, all_user_data)

    message = 'Profile updated successfully.'
    return render_template('profile.html', username=CURRENT_USERNAME, email=email, fullname=fullname, message=message)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
