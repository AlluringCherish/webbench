from flask import Flask, render_template, request, redirect, url_for, abort
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = 'data'

# Helper functions for reading and writing pipe-delimited files

def read_pipe_delimited(filename, fields):
    filepath = os.path.join(DATA_DIR, filename)
    data = []
    if not os.path.exists(filepath):
        return data
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != len(fields):
                continue  # Skip malformed lines
            item = {field: parts[i] for i, field in enumerate(fields)}
            data.append(item)
    return data


def write_pipe_delimited(filename, data, fields):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        for item in data:
            line = '|'.join(str(item[field]) for field in fields)
            f.write(line + '\n')


# Users
USERS_FIELDS = ['username', 'email', 'fullname']

# Courses
COURSES_FIELDS = ['course_id', 'title', 'description', 'category', 'level', 'duration', 'status']

# Enrollments
ENROLLMENTS_FIELDS = ['enrollment_id', 'username', 'course_id', 'enrollment_date', 'progress', 'status']

# Assignments
ASSIGNMENTS_FIELDS = ['assignment_id', 'course_id', 'title', 'description', 'due_date', 'max_points']

# Submissions
SUBMISSIONS_FIELDS = ['submission_id', 'assignment_id', 'username', 'submission_text', 'submit_date', 'grade', 'feedback']

# Certificates
CERTIFICATES_FIELDS = ['certificate_id', 'username', 'course_id', 'issue_date']


# Load functions

def load_users():
    return read_pipe_delimited('users.txt', USERS_FIELDS)

def load_courses():
    return read_pipe_delimited('courses.txt', COURSES_FIELDS)

def load_enrollments():
    return read_pipe_delimited('enrollments.txt', ENROLLMENTS_FIELDS)

def load_assignments():
    return read_pipe_delimited('assignments.txt', ASSIGNMENTS_FIELDS)

def load_submissions():
    return read_pipe_delimited('submissions.txt', SUBMISSIONS_FIELDS)

def load_certificates():
    return read_pipe_delimited('certificates.txt', CERTIFICATES_FIELDS)

# Save functions

def save_enrollments(enrollments):
    write_pipe_delimited('enrollments.txt', enrollments, ENROLLMENTS_FIELDS)

def save_submissions(submissions):
    write_pipe_delimited('submissions.txt', submissions, SUBMISSIONS_FIELDS)

def save_certificates(certificates):
    write_pipe_delimited('certificates.txt', certificates, CERTIFICATES_FIELDS)

# Utility functions

def find_user(username):
    users = load_users()
    for u in users:
        if u['username'] == username:
            return u
    return None


def find_course(course_id):
    courses = load_courses()
    for c in courses:
        if c['course_id'] == str(course_id):
            return c
    return None


def find_enrollment(username, course_id):
    enrollments = load_enrollments()
    for e in enrollments:
        if e['username'] == username and e['course_id'] == str(course_id):
            return e
    return None


def find_enrollment_by_id(enrollment_id):
    enrollments = load_enrollments()
    for e in enrollments:
        if e['enrollment_id'] == enrollment_id:
            return e
    return None


def find_assignments_for_user(username):
    assignments = load_assignments()
    enrollments = load_enrollments()
    user_courses = set()
    for e in enrollments:
        if e['username'] == username:
            user_courses.add(e['course_id'])
    user_assignments = []
    for a in assignments:
        if a['course_id'] in user_courses:
            user_assignments.append(a)
    return user_assignments


def find_assignment(assignment_id):
    assignments = load_assignments()
    for a in assignments:
        if a['assignment_id'] == str(assignment_id):
            return a
    return None


def find_submissions_by_user_assignment(username, assignment_id):
    submissions = load_submissions()
    user_subs = []
    for s in submissions:
        if s['username'] == username and s['assignment_id'] == str(assignment_id):
            user_subs.append(s)
    return user_subs


def find_certificates_by_user(username):
    certificates = load_certificates()
    return [c for c in certificates if c['username'] == username]


def generate_new_id(items, id_field):
    max_id = 0
    for item in items:
        try:
            cur_id = int(item[id_field])
            if cur_id > max_id:
                max_id = cur_id
        except:
            continue
    return str(max_id + 1)

# Enrollment progress update helper

def update_progress(enrollments, username, course_id, new_progress):
    for e in enrollments:
        if e['username'] == username and e['course_id'] == str(course_id):
            e['progress'] = str(new_progress)
            if new_progress >= 100:
                e['progress'] = '100'
                e['status'] = 'Completed'
            else:
                e['status'] = 'In Progress'
            return True
    return False

# Check if user has certificate for course

def has_certificate(username, course_id):
    certs = load_certificates()
    for c in certs:
        if c['username'] == username and c['course_id'] == str(course_id):
            return True
    return False

# Generate certificate

def generate_certificate(username, course_id):
    certificates = load_certificates()
    if has_certificate(username, course_id):
        return
    new_id = generate_new_id(certificates, 'certificate_id')
    issue_date = datetime.now().strftime('%Y-%m-%d')
    certificates.append({
        'certificate_id': new_id,
        'username': username,
        'course_id': str(course_id),
        'issue_date': issue_date
    })
    save_certificates(certificates)


# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_view'))


@app.route('/dashboard')
def dashboard_view():
    # For demonstration, we simulate user logged in as "john"
    username = 'john'
    user = find_user(username)
    if not user:
        abort(404)

    fullname = user['fullname']

    enrollments = load_enrollments()
    courses = load_courses()

    enrolled_courses = []
    for e in enrollments:
        if e['username'] == username:
            course = next((c for c in courses if c['course_id'] == e['course_id']), None)
            if course:
                enrolled_courses.append({
                    'course_id': int(course['course_id']),
                    'title': course['title'],
                    'progress': int(e['progress'])
                })

    return render_template('dashboard.html', username=username, fullname=fullname, enrolled_courses=enrolled_courses)


@app.route('/catalog')
def course_catalog_view():
    username = 'john'
    user = find_user(username)
    if not user:
        abort(404)

    courses = load_courses()
    active_courses = [
        {
            'course_id': int(c['course_id']),
            'title': c['title'],
            'description': c['description']
        } for c in courses if c['status'] == 'Active'
    ]

    return render_template('catalog.html', username=username, courses=active_courses)


@app.route('/course/<int:course_id>')
def course_details_view(course_id):
    username = 'john'
    user = find_user(username)
    if not user:
        abort(404)

    course = find_course(course_id)
    if not course or course['status'] != 'Active':
        abort(404)

    enrollment = find_enrollment(username, course_id)
    enrollment_status = enrollment is not None

    course_dict = {
        'course_id': course_id,
        'title': course['title'],
        'description': course['description'],
        'enrollment_status': enrollment_status
    }

    return render_template('course_details.html', username=username, course=course_dict)


@app.route('/course/<int:course_id>/enroll', methods=['POST'])
def enroll_course(course_id):
    username = 'john'
    user = find_user(username)
    if not user:
        abort(404)

    course = find_course(course_id)
    if not course or course['status'] != 'Active':
        abort(404)

    # Check if already enrolled
    enrollment = find_enrollment(username, course_id)
    if enrollment:
        # Already enrolled, just show details
        enrollment_status = True
    else:
        # Create new enrollment
        enrollments = load_enrollments()
        new_enrollment_id = generate_new_id(enrollments, 'enrollment_id')
        enroll_date = datetime.now().strftime('%Y-%m-%d')
        enrollments.append({
            'enrollment_id': new_enrollment_id,
            'username': username,
            'course_id': str(course_id),
            'enrollment_date': enroll_date,
            'progress': '0',
            'status': 'In Progress'
        })
        save_enrollments(enrollments)
        enrollment_status = True

    course_dict = {
        'course_id': course_id,
        'title': course['title'],
        'description': course['description'],
        'enrollment_status': enrollment_status
    }

    return render_template('course_details.html', username=username, course=course_dict)


@app.route('/my-courses')
def my_courses_view():
    username = 'john'
    user = find_user(username)
    if not user:
        abort(404)

    enrollments = load_enrollments()
    courses = load_courses()
    enrolled_courses = []
    for e in enrollments:
        if e['username'] == username:
            course = next((c for c in courses if c['course_id'] == e['course_id']), None)
            if course:
                enrolled_courses.append({
                    'course_id': int(course['course_id']),
                    'title': course['title'],
                    'progress': int(e['progress'])
                })

    return render_template('my_courses.html', username=username, enrolled_courses=enrolled_courses)


@app.route('/learning/<int:course_id>')
def course_learning_view(course_id):
    username = 'john'
    user = find_user(username)
    if not user:
        abort(404)

    course = find_course(course_id)
    if not course or course['status'] != 'Active':
        abort(404)

    enrollment = find_enrollment(username, course_id)
    if not enrollment:
        abort(403)  # Not enrolled

    progress = int(enrollment['progress'])

    # Simulate lessons for the course, for demo assume lessons = 10 lessons
    total_lessons = 10
    lessons = []
    for lesson_id in range(1, total_lessons + 1):
        is_completed = (lesson_id <= (progress // 10))  # each 10% is one lesson completed
        lessons.append({
            'lesson_id': lesson_id,
            'title': f'Lesson {lesson_id}',
            'content': f'Content for lesson {lesson_id} of course {course_id}.',
            'is_completed': is_completed
        })

    course_dict = {
        'course_id': course_id,
        'title': course['title']
    }

    return render_template('course_learning.html', username=username, course=course_dict, lessons=lessons, progress=progress)


@app.route('/learning/<int:course_id>/complete', methods=['POST'])
def mark_lesson_complete(course_id):
    username = 'john'
    user = find_user(username)
    if not user:
        abort(404)

    enrollment = find_enrollment(username, course_id)
    if not enrollment:
        abort(403)  # Not enrolled

    progress = int(enrollment['progress'])
    total_lessons = 10
    current_lesson = (progress // 10) + 1

    # Check if current lesson can be marked complete
    # Sequential completion enforced
    # We assume user sent a form field 'lesson_id' which should be current_lesson
    try:
        lesson_id = int(request.form.get('lesson_id', current_lesson))
    except:
        lesson_id = current_lesson

    if lesson_id != current_lesson or lesson_id > total_lessons:
        # Invalid lesson completion order
        # Reload page without updating
        return redirect(url_for('course_learning_view', course_id=course_id))

    # Update progress by 10%
    new_progress = min(100, progress + 10)
    enrollments = load_enrollments()
    updated = update_progress(enrollments, username, course_id, new_progress)
    if updated:
        save_enrollments(enrollments)

    # Generate certificate if progress reached 100%
    if new_progress == 100:
        generate_certificate(username, course_id)

    return redirect(url_for('course_learning_view', course_id=course_id))


@app.route('/assignments')
def my_assignments_view():
    username = 'john'
    user = find_user(username)
    if not user:
        abort(404)

    assignments = find_assignments_for_user(username)
    submissions = load_submissions()

    assignments_list = []
    today_dt = datetime.now().date()

    for a in assignments:
        assignment_id = a['assignment_id']
        due_date = datetime.strptime(a['due_date'], '%Y-%m-%d').date()

        # Determine status
        status = 'Pending'
        # Check if submission exists for user assignment
        user_subs = [s for s in submissions if s['assignment_id'] == assignment_id and s['username'] == username]
        if user_subs:
            status = 'Submitted'
        elif due_date < today_dt:
            status = 'Late'

        assignments_list.append({
            'assignment_id': int(assignment_id),
            'title': a['title'],
            'description': a['description'],
            'due_date': a['due_date'],
            'status': status
        })

    return render_template('assignments.html', username=username, assignments=assignments_list)


@app.route('/assignment/<int:assignment_id>/submit', methods=['GET'])
def submit_assignment_view(assignment_id):
    username = 'john'
    user = find_user(username)
    if not user:
        abort(404)

    assignment = find_assignment(assignment_id)
    if not assignment:
        abort(404)

    assignment_dict = {
        'assignment_id': int(assignment['assignment_id']),
        'title': assignment['title'],
        'description': assignment['description']
    }

    return render_template('submit_assignment.html', username=username, assignment=assignment_dict)


@app.route('/assignment/<int:assignment_id>/submit', methods=['POST'])
def submit_assignment_post(assignment_id):
    username = 'john'
    user = find_user(username)
    if not user:
        abort(404)

    assignment = find_assignment(assignment_id)
    if not assignment:
        abort(404)

    submission_text = request.form.get('submission_text', '').strip()
    if not submission_text:
        # Reload with error message could be done, but not in spec, so proceed
        confirmation_msg = 'Submission text cannot be empty.'
        assignment_dict = {
            'assignment_id': int(assignment['assignment_id']),
            'title': assignment['title'],
            'description': assignment['description']
        }
        return render_template('submit_assignment.html', username=username, assignment=assignment_dict, confirmation_msg=confirmation_msg)

    submissions = load_submissions()
    new_submission_id = generate_new_id(submissions, 'submission_id')
    submit_date = datetime.now().strftime('%Y-%m-%d')

    submissions.append({
        'submission_id': new_submission_id,
        'assignment_id': str(assignment_id),
        'username': username,
        'submission_text': submission_text,
        'submit_date': submit_date,
        'grade': '',
        'feedback': ''
    })
    save_submissions(submissions)

    confirmation_msg = 'Submission successful.'
    assignment_dict = {
        'assignment_id': int(assignment['assignment_id']),
        'title': assignment['title'],
        'description': assignment['description']
    }

    return render_template('submit_assignment.html', username=username, assignment=assignment_dict, confirmation_msg=confirmation_msg)


@app.route('/certificates')
def certificates_view():
    username = 'john'
    user = find_user(username)
    if not user:
        abort(404)

    certificates = find_certificates_by_user(username)
    courses = load_courses()

    certificates_list = []
    for cert in certificates:
        course = next((c for c in courses if c['course_id'] == cert['course_id']), None)
        if course:
            certificates_list.append({
                'certificate_id': int(cert['certificate_id']),
                'course_title': course['title'],
                'issue_date': cert['issue_date']
            })

    return render_template('certificates.html', username=username, certificates=certificates_list)


@app.route('/profile')
def profile_view():
    username = 'john'
    user = find_user(username)
    if not user:
        abort(404)

    email = user['email']
    fullname = user['fullname']

    return render_template('profile.html', username=username, email=email, fullname=fullname)


@app.route('/profile/update', methods=['POST'])
def update_profile():
    username = 'john'
    user = find_user(username)
    if not user:
        abort(404)

    email = request.form.get('email', '').strip()
    fullname = request.form.get('fullname', '').strip()

    if not email or not fullname:
        update_status = 'Email and Full Name cannot be empty.'
    else:
        users = load_users()
        updated = False
        for u in users:
            if u['username'] == username:
                u['email'] = email
                u['fullname'] = fullname
                updated = True
                break
        if updated:
            write_pipe_delimited('users.txt', users, USERS_FIELDS)
            update_status = 'Profile updated successfully.'
        else:
            update_status = 'User not found.'

    return render_template('profile.html', username=username, email=email, fullname=fullname, update_status=update_status)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
