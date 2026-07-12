from flask import Flask, render_template, request, redirect, url_for, abort
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = 'data'

# Helper functions for file I/O

def read_users():
    users = {}
    path = os.path.join(DATA_DIR, 'users.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    username,email,fullname = line.split('|')
                    users[username] = {'username': username, 'email': email, 'fullname': fullname}
    return users

def write_users(users):
    lines = []
    for user in users.values():
        lines.append(f"{user['username']}|{user['email']}|{user['fullname']}")
    content = '\n'.join(lines)
    return content

def read_courses():
    courses = {}
    path = os.path.join(DATA_DIR, 'courses.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    (
                        course_id, title, description, category,
                        level, duration, status
                    ) = line.split('|')
                    courses[int(course_id)] = {
                        'course_id': int(course_id), 'title': title, 'description': description,
                        'category': category, 'level': level, 'duration': duration, 'status': status
                    }
    return courses


def read_enrollments():
    enrollments = {}
    path = os.path.join(DATA_DIR, 'enrollments.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    (
                        enrollment_id, username, course_id, enrollment_date,
                        progress, status
                    ) = line.split('|')
                    enrollment_id = int(enrollment_id)
                    enrollments[enrollment_id] = {
                        'enrollment_id': enrollment_id, 'username': username, 'course_id': int(course_id),
                        'enrollment_date': enrollment_date, 'progress': int(progress), 'status': status
                    }
    return enrollments

def write_enrollments(enrollments):
    lines = []
    for enroll in enrollments.values():
        lines.append(f"{enroll['enrollment_id']}|{enroll['username']}|{enroll['course_id']}|{enroll['enrollment_date']}|{enroll['progress']}|{enroll['status']}")
    content = '\n'.join(lines)
    return content


def read_assignments():
    assignments = {}
    path = os.path.join(DATA_DIR, 'assignments.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    (
                        assignment_id, course_id, title, description, due_date, max_points
                    ) = line.split('|')
                    assignments[int(assignment_id)] = {
                        'assignment_id': int(assignment_id), 'course_id': int(course_id), 'title': title,
                        'description': description, 'due_date': due_date, 'max_points': int(max_points)
                    }
    return assignments


def read_submissions():
    submissions = {}
    path = os.path.join(DATA_DIR, 'submissions.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    (
                        submission_id, assignment_id, username, submission_text, submit_date, grade, feedback
                    ) = line.split('|')
                    submissions[int(submission_id)] = {
                        'submission_id': int(submission_id), 'assignment_id': int(assignment_id), 'username': username,
                        'submission_text': submission_text, 'submit_date': submit_date, 'grade': int(grade), 'feedback': feedback
                    }
    return submissions


def write_submissions(submissions):
    lines = []
    for sub in submissions.values():
        lines.append(f"{sub['submission_id']}|{sub['assignment_id']}|{sub['username']}|{sub['submission_text']}|{sub['submit_date']}|{sub['grade']}|{sub['feedback']}")
    content = '\n'.join(lines)
    return content


def read_certificates():
    certificates = {}
    path = os.path.join(DATA_DIR, 'certificates.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    (
                        certificate_id, username, course_id, issue_date
                    ) = line.split('|')
                    certificates[int(certificate_id)] = {
                        'certificate_id': int(certificate_id), 'username': username,
                        'course_id': int(course_id), 'issue_date': issue_date
                    }
    return certificates


def write_certificates(certificates):
    lines = []
    for cert in certificates.values():
        lines.append(f"{cert['certificate_id']}|{cert['username']}|{cert['course_id']}|{cert['issue_date']}")
    content = '\n'.join(lines)
    return content


# Extra Helper functions

def get_next_id(items):
    if not items:
        return 1
    return max(items.keys()) + 1


def get_user_enrollments(username):
    enrollments = read_enrollments()
    user_enrolls = [e for e in enrollments.values() if e['username'] == username]
    return user_enrolls


def get_user_courses(username):
    enrolls = get_user_enrollments(username)
    courses = read_courses()
    user_courses = []
    for enr in enrolls:
        c = courses.get(enr['course_id'])
        if c:
            user_courses.append({'course_id': c['course_id'], 'title': c['title'], 'progress': enr['progress']})
    return user_courses


def get_course_lessons(course_id):
    # Lessons will be mimicked as numbered lessons 1 to N for simplicity
    # Since lessons data is not specified, assume 10 lessons per course
    lessons = []
    for i in range(1, 11):
        lessons.append({'lesson_id': i, 'title': f'Lesson {i}', 'content': f'Content for Lesson {i} in Course {course_id}'})
    return lessons


def get_completed_lessons(username, course_id):
    enrollments = read_enrollments()
    for enr in enrollments.values():
        if enr['username'] == username and enr['course_id'] == course_id:
            progress = enr['progress']
            # calculate completed lessons based on progress percentage
            # Each lesson is 10% (assuming 10 lessons) progress
            completed_count = progress // 10
            return list(range(1, completed_count+1))
    return []


def find_enrollment(username, course_id):
    enrollments = read_enrollments()
    for enr in enrollments.values():
        if enr['username'] == username and enr['course_id'] == course_id:
            return enr
    return None


def update_enrollment_progress(enrollment_id, progress):
    enrollments = read_enrollments()
    enrollment = enrollments.get(enrollment_id)
    if enrollment:
        enrollment['progress'] = progress
        if progress == 100:
            enrollment['status'] = 'Completed'
        else:
            enrollment['status'] = 'In Progress'
        enrollments[enrollment_id] = enrollment
        content = write_enrollments(enrollments)
        with open(os.path.join(DATA_DIR, 'enrollments.txt'), 'w', encoding='utf-8') as f:
            f.write(content)


def user_has_certificate(username, course_id):
    certificates = read_certificates()
    for cert in certificates.values():
        if cert['username'] == username and cert['course_id'] == course_id:
            return True
    return False


def generate_certificate(username, course_id):
    certs = read_certificates()
    if user_has_certificate(username, course_id):
        return
    cert_id = get_next_id(certs)
    today = datetime.now().strftime('%Y-%m-%d')
    certs[cert_id] = {
        'certificate_id': cert_id,
        'username': username,
        'course_id': course_id,
        'issue_date': today
    }
    content = write_certificates(certs)
    with open(os.path.join(DATA_DIR, 'certificates.txt'), 'w', encoding='utf-8') as f:
        f.write(content)


# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # Get username from query param or default for demo
    username = request.args.get('username', None)
    if not username:
        abort(400, 'Must provide username param')
    users = read_users()
    user = users.get(username)
    if not user:
        abort(404, 'User not found')
    enrolled_courses = get_user_courses(username)
    return render_template('dashboard.html', username=username, fullname=user['fullname'], enrolled_courses=enrolled_courses)


@app.route('/courses')
def course_catalog():
    courses_dict = read_courses()
    courses = list(courses_dict.values())
    return render_template('course_catalog.html', courses=courses)


@app.route('/courses/<int:course_id>')
def course_details(course_id):
    username = request.args.get('username', None)
    if not username:
        abort(400, 'Username required')
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        abort(404, 'Course not found')
    enrolled = find_enrollment(username, course_id)
    already_enrolled = enrolled is not None
    return render_template('course_details.html', course=course, already_enrolled=already_enrolled)


@app.route('/courses/<int:course_id>/enroll', methods=['POST'])
def enroll_course(course_id):
    username = request.form.get('username', None)
    if not username:
        abort(400, 'Username required')
    users = read_users()
    if username not in users:
        abort(404, 'User not found')
    courses = read_courses()
    if course_id not in courses:
        abort(404, 'Course not found')
    enrollments = read_enrollments()
    # check if already enrolled
    for enr in enrollments.values():
        if enr['username'] == username and enr['course_id'] == course_id:
            abort(400, 'User already enrolled')
    enrollment_id = get_next_id(enrollments)
    today = datetime.now().strftime('%Y-%m-%d')
    enrollment = {
        'enrollment_id': enrollment_id,
        'username': username,
        'course_id': course_id,
        'enrollment_date': today,
        'progress': 0,
        'status': 'In Progress'
    }
    enrollments[enrollment_id] = enrollment
    content = write_enrollments(enrollments)
    with open(os.path.join(DATA_DIR, 'enrollments.txt'), 'w', encoding='utf-8') as f:
        f.write(content)
    # Redirect to course details with enrollment status updated
    return redirect(url_for('course_details', course_id=course_id, username=username))


@app.route('/mycourses')
def my_courses():
    username = request.args.get('username', None)
    if not username:
        abort(400, 'Username required')
    users = read_users()
    if username not in users:
        abort(404, 'User not found')
    enrolled_courses = get_user_courses(username)
    return render_template('my_courses.html', username=username, enrolled_courses=enrolled_courses)


@app.route('/learn/<int:course_id>')
def course_learning(course_id):
    username = request.args.get('username', None)
    if not username:
        abort(400, 'Username required')
    users = read_users()
    if username not in users:
        abort(404, 'User not found')
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        abort(404, 'Course not found')

    enrollment = find_enrollment(username, course_id)
    if not enrollment:
        abort(403, 'User not enrolled in this course')

    lessons = get_course_lessons(course_id)
    completed_lessons = get_completed_lessons(username, course_id)
    progress = enrollment['progress']

    return render_template('course_learning.html', username=username, course={'course_id': course_id, 'title': course['title'], 'lessons': lessons}, completed_lessons=completed_lessons, progress=progress)


@app.route('/learn/<int:course_id>/mark_complete', methods=['POST'])
def mark_lesson_complete(course_id):
    username = request.form.get('username', None)
    lesson_id = request.form.get('lesson_id', None)
    if not username or not lesson_id:
        abort(400, 'Username and lesson_id required')
    try:
        lesson_id = int(lesson_id)
    except ValueError:
        abort(400, 'lesson_id must be integer')

    users = read_users()
    if username not in users:
        abort(404, 'User not found')
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        abort(404, 'Course not found')

    enrollment = find_enrollment(username, course_id)
    if not enrollment:
        abort(403, 'User not enrolled in this course')

    lessons = get_course_lessons(course_id)
    lesson_ids = [l['lesson_id'] for l in lessons]

    if lesson_id not in lesson_ids:
        abort(400, 'Invalid lesson_id')

    # Check if lesson_id is next in line (sequential progress)
    completed_lessons = get_completed_lessons(username, course_id)
    # ensure sequential completion
    # next lesson must be exactly len(completed_lessons)+1
    expected_next = len(completed_lessons) + 1
    if lesson_id != expected_next:
        abort(400, f'Lessons must be completed sequentially. Next lesson to complete is {expected_next}')

    # update progress
    enrollment_id = enrollment['enrollment_id']
    new_progress = lesson_id * 10  # each lesson 10%
    update_enrollment_progress(enrollment_id, new_progress)

    # generate certificate if progress 100%
    if new_progress == 100:
        generate_certificate(username, course_id)

    return '', 204


@app.route('/assignments')
def my_assignments():
    username = request.args.get('username', None)
    if not username:
        abort(400, 'Username required')
    users = read_users()
    if username not in users:
        abort(404, 'User not found')

    assignments_all = read_assignments()
    enrollments = read_enrollments()
    # get courses user is enrolled in
    enrolled_courses_ids = set()
    for enr in enrollments.values():
        if enr['username'] == username:
            enrolled_courses_ids.add(enr['course_id'])

    # filter assignments for user's enrolled courses
    user_assignments = []
    today = datetime.now().strftime('%Y-%m-%d')
    for ass in assignments_all.values():
        if ass['course_id'] in enrolled_courses_ids:
            # Determine status: due_date passed or not
            status = 'Open' if ass['due_date'] >= today else 'Closed'
            user_assignments.append({
                'assignment_id': ass['assignment_id'], 'title': ass['title'], 'description': ass['description'],
                'due_date': ass['due_date'], 'max_points': ass['max_points'], 'status': status
            })
    return render_template('my_assignments.html', username=username, assignments=user_assignments)


@app.route('/assignments/<int:assignment_id>/submit', methods=['GET'])
def submit_assignment(assignment_id):
    username = request.args.get('username', None)
    if not username:
        abort(400, 'Username required')
    users = read_users()
    if username not in users:
        abort(404, 'User not found')
    assignments = read_assignments()
    assignment = assignments.get(assignment_id)
    if not assignment:
        abort(404, 'Assignment not found')
    return render_template('submit_assignment.html', username=username, assignment=assignment)


@app.route('/assignments/<int:assignment_id>/submit', methods=['POST'])
def submit_assignment_post(assignment_id):
    username = request.form.get('username', None)
    submission_text = request.form.get('submission_text', '')
    if not username:
        abort(400, 'Username required')

    users = read_users()
    if username not in users:
        abort(404, 'User not found')

    assignments = read_assignments()
    if assignment_id not in assignments:
        abort(404, 'Assignment not found')

    submissions = read_submissions()
    submission_id = get_next_id(submissions)
    today = datetime.now().strftime('%Y-%m-%d')
    # New submissions have grade 0 and empty feedback as initial state
    submissions[submission_id] = {
        'submission_id': submission_id,
        'assignment_id': assignment_id,
        'username': username,
        'submission_text': submission_text,
        'submit_date': today,
        'grade': 0,
        'feedback': ''
    }
    content = write_submissions(submissions)
    with open(os.path.join(DATA_DIR, 'submissions.txt'), 'w', encoding='utf-8') as f:
        f.write(content)

    return redirect(url_for('my_assignments', username=username))


@app.route('/certificates')
def certificates():
    username = request.args.get('username', None)
    if not username:
        abort(400, 'Username required')
    users = read_users()
    if username not in users:
        abort(404, 'User not found')

    certificates_all = read_certificates()
    courses = read_courses()
    user_certificates = []
    for cert in certificates_all.values():
        if cert['username'] == username:
            course = courses.get(cert['course_id'])
            course_title = course['title'] if course else 'Unknown'
            user_certificates.append({
                'certificate_id': cert['certificate_id'], 'course_id': cert['course_id'],
                'course_title': course_title, 'issue_date': cert['issue_date']
            })
    return render_template('certificates.html', username=username, certificates=user_certificates)


@app.route('/profile')
def user_profile():
    username = request.args.get('username', None)
    if not username:
        abort(400, 'Username required')
    users = read_users()
    user = users.get(username)
    if not user:
        abort(404, 'User not found')
    return render_template('profile.html', username=username, email=user['email'], fullname=user['fullname'])


@app.route('/profile/update', methods=['POST'])
def update_profile():
    username = request.form.get('username', None)
    email = request.form.get('email', None)
    fullname = request.form.get('fullname', None)

    if not username or not email or not fullname:
        abort(400, 'All fields required')

    users = read_users()
    if username not in users:
        abort(404, 'User not found')

    users[username]['email'] = email
    users[username]['fullname'] = fullname
    content = write_users(users)

    with open(os.path.join(DATA_DIR, 'users.txt'), 'w', encoding='utf-8') as f:
        f.write(content)

    return '', 204


if __name__ == '__main__':
    app.run(debug=True, port=5000)
