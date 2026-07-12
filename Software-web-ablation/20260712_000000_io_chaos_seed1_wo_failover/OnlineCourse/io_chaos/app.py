from flask import Flask, render_template, redirect, url_for, request, abort
from datetime import datetime
import os

app = Flask(__name__)

DATA_DIR = 'data'

# Helper functions to load and save data from pipe-delimited files

def load_users():
    users = {}
    path = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                username, email, fullname = line.split('|')
                users[username] = {
                    'username': username,
                    'email': email,
                    'fullname': fullname
                }
    return users


def load_courses():
    courses = {}
    path = os.path.join(DATA_DIR, 'courses.txt')
    if not os.path.exists(path):
        return courses
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                (course_id, title, description, category, level,
                 duration, status) = line.split('|')
                courses[course_id] = {
                    'course_id': course_id,
                    'title': title,
                    'description': description,
                    'category': category,
                    'level': level,
                    'duration': duration,
                    'status': status
                }
    return courses


def load_enrollments():
    enrollments = {}
    path = os.path.join(DATA_DIR, 'enrollments.txt')
    if not os.path.exists(path):
        return enrollments
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                (enrollment_id, username, course_id, enrollment_date,
                 progress, status) = line.split('|')
                enrollments[enrollment_id] = {
                    'enrollment_id': enrollment_id,
                    'username': username,
                    'course_id': course_id,
                    'enrollment_date': enrollment_date,
                    'progress': int(progress),
                    'status': status
                }
    return enrollments


def load_assignments():
    assignments = {}
    path = os.path.join(DATA_DIR, 'assignments.txt')
    if not os.path.exists(path):
        return assignments
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                (assignment_id, course_id, title, description, due_date,
                 max_points) = line.split('|')
                assignments[assignment_id] = {
                    'assignment_id': assignment_id,
                    'course_id': course_id,
                    'title': title,
                    'description': description,
                    'due_date': due_date,
                    'max_points': int(max_points)
                }
    return assignments


def load_submissions():
    submissions = {}
    path = os.path.join(DATA_DIR, 'submissions.txt')
    if not os.path.exists(path):
        return submissions
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                (submission_id, assignment_id, username, submission_text, submit_date,
                 grade, feedback) = line.split('|')
                submissions[submission_id] = {
                    'submission_id': submission_id,
                    'assignment_id': assignment_id,
                    'username': username,
                    'submission_text': submission_text,
                    'submit_date': submit_date,
                    'grade': int(grade) if grade.isdigit() else None,
                    'feedback': feedback
                }
    return submissions


def load_certificates():
    certificates = {}
    path = os.path.join(DATA_DIR, 'certificates.txt')
    if not os.path.exists(path):
        return certificates
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                certificate_id, username, course_id, issue_date = line.split('|')
                certificates[certificate_id] = {
                    'certificate_id': certificate_id,
                    'username': username,
                    'course_id': course_id,
                    'issue_date': issue_date
                }
    return certificates


def save_users(users):
    path = os.path.join(DATA_DIR, 'users.txt')
    lines = [f"{u['username']}|{u['email']}|{u['fullname']}" for u in users.values()]
    content = "\n".join(lines) + "\n" if lines else ""
    app.logger.debug(f"Saving users {len(users)}")
    return content


def save_courses(courses):
    path = os.path.join(DATA_DIR, 'courses.txt')
    lines = [f"{c['course_id']}|{c['title']}|{c['description']}|{c['category']}|{c['level']}|{c['duration']}|{c['status']}" for c in courses.values()]
    content = "\n".join(lines) + "\n" if lines else ""
    return content


def save_enrollments(enrollments):
    path = os.path.join(DATA_DIR, 'enrollments.txt')
    lines = [f"{e['enrollment_id']}|{e['username']}|{e['course_id']}|{e['enrollment_date']}|{e['progress']}|{e['status']}" for e in enrollments.values()]
    content = "\n".join(lines) + "\n" if lines else ""
    return content


def save_assignments(assignments):
    lines = [f"{a['assignment_id']}|{a['course_id']}|{a['title']}|{a['description']}|{a['due_date']}|{a['max_points']}" for a in assignments.values()]
    content = "\n".join(lines) + "\n" if lines else ""
    return content


def save_submissions(submissions):
    lines = []
    for s in submissions.values():
        grade_str = str(s['grade']) if s['grade'] is not None else ""
        lines.append(f"{s['submission_id']}|{s['assignment_id']}|{s['username']}|{s['submission_text']}|{s['submit_date']}|{grade_str}|{s['feedback']}")
    content = "\n".join(lines) + "\n" if lines else ""
    return content


def save_certificates(certificates):
    lines = [f"{c['certificate_id']}|{c['username']}|{c['course_id']}|{c['issue_date']}" for c in certificates.values()]
    content = "\n".join(lines) + "\n" if lines else ""
    return content


# Utility functions

def generate_new_id(entries):
    if not entries:
        return '1'
    max_id = max(int(k) for k in entries.keys())
    return str(max_id + 1)


def get_user_enrollments(username, enrollments):
    return [e for e in enrollments.values() if e['username'] == username]


def get_course_lessons(course_id):
    # No lessons.txt provided; assume lessons are enumerated per course by fixed data or mocked here
    # We must simulate lessons list for the purpose of course_learning
    # For implementation, stub with 5 lessons for any course
    lessons = []
    for i in range(1, 6):
        lesson_id = f"{course_id}-{i}"
        lessons.append({
            'lesson_id': lesson_id,
            'title': f"Lesson {i}",
            'content': f"Content of lesson {i} for course {course_id}."
        })
    return lessons


def find_enrollment_by_user_course(username, course_id, enrollments):
    for e in enrollments.values():
        if e['username'] == username and e['course_id'] == course_id:
            return e
    return None


def get_user_assignments(username, assignments, enrollments):
    # Return assignments from courses user is enrolled in
    user_courses = set(e['course_id'] for e in enrollments.values() if e['username'] == username)
    filtered = []
    for a in assignments.values():
        if a['course_id'] in user_courses:
            filtered.append(a)
    return filtered


def find_submission(username, assignment_id, submissions):
    for s in submissions.values():
        if s['username'] == username and s['assignment_id'] == assignment_id:
            return s
    return None


# Session simulation (No authentication specified, so we assume a fixed logged in user for demo)
# For realistic usage, integrate Flask-Login or session management
# Here we use a default user 'john'
DEFAULT_USERNAME = 'john'


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = DEFAULT_USERNAME
    users = load_users()
    user = users.get(username)
    if not user:
        abort(404, description='User not found')
    enrollments = load_enrollments()
    courses = load_courses()
    user_enrollments = get_user_enrollments(username, enrollments)

    enrolled_courses = []
    for e in user_enrollments:
        course = courses.get(e['course_id'])
        if course:
            enrolled_courses.append({
                'course_id': course['course_id'],
                'title': course['title'],
                'progress': e['progress']
            })

    return render_template('dashboard.html', username=username, fullname=user['fullname'], enrolled_courses=enrolled_courses)


@app.route('/courses')
def course_catalog():
    courses = load_courses()
    search_query = request.args.get('search_query', '').strip()

    filtered_courses = []
    if search_query:
        sq_lower = search_query.lower()
        for c in courses.values():
            if (sq_lower in c['title'].lower() or
                sq_lower in c['description'].lower() or
                sq_lower in c['category'].lower() or
                sq_lower in c['level'].lower()):
                filtered_courses.append(c)
    else:
        filtered_courses = list(courses.values())

    return render_template('course_catalog.html', courses=filtered_courses, search_query=search_query)


@app.route('/course/<course_id>')
def course_details(course_id):
    username = DEFAULT_USERNAME
    courses = load_courses()
    course = courses.get(course_id)
    if not course:
        abort(404, description='Course not found')

    enrollments = load_enrollments()
    enrollment = find_enrollment_by_user_course(username, course_id, enrollments)

    enrolled = enrollment is not None

    return render_template('course_details.html', course=course, enrolled=enrolled)


@app.route('/course/<course_id>/enroll', methods=['POST'])
def enroll_course(course_id):
    username = DEFAULT_USERNAME
    users = load_users()
    if username not in users:
        abort(404, description='User not found')

    courses = load_courses()
    if course_id not in courses:
        abort(404, description='Course not found')

    enrollments = load_enrollments()
    # Check if already enrolled
    old_enrollment = find_enrollment_by_user_course(username, course_id, enrollments)
    if old_enrollment:
        # Already enrolled, redirect back
        return redirect(url_for('course_details', course_id=course_id))

    # Create new enrollment
    new_enrollment_id = generate_new_id(enrollments)
    enrollment_date = datetime.now().date().isoformat()
    enrollments[new_enrollment_id] = {
        'enrollment_id': new_enrollment_id,
        'username': username,
        'course_id': course_id,
        'enrollment_date': enrollment_date,
        'progress': 0,
        'status': 'In Progress'
    }

    # Save enrollments
    from functions import write_text_file
    content = save_enrollments(enrollments)
    write_text_file({"filename": os.path.join(DATA_DIR, 'enrollments.txt'), "content": content})

    return redirect(url_for('course_details', course_id=course_id))


@app.route('/my-courses')
def my_courses():
    username = DEFAULT_USERNAME
    users = load_users()
    if username not in users:
        abort(404, description='User not found')

    enrollments = load_enrollments()
    courses = load_courses()
    user_enrollments = get_user_enrollments(username, enrollments)

    enrolled_courses = []
    for e in user_enrollments:
        course = courses.get(e['course_id'])
        if course:
            enrolled_courses.append({
                'course_id': course['course_id'],
                'title': course['title'],
                'progress': e['progress']
            })

    return render_template('my_courses.html', username=username, enrolled_courses=enrolled_courses)


@app.route('/learn/<course_id>')
def course_learning(course_id):
    username = DEFAULT_USERNAME
    users = load_users()
    if username not in users:
        abort(404, description='User not found')

    courses = load_courses()
    course = courses.get(course_id)
    if not course:
        abort(404, description='Course not found')

    enrollments = load_enrollments()
    enrollment = find_enrollment_by_user_course(username, course_id, enrollments)
    if not enrollment:
        # Not enrolled
        return redirect(url_for('course_details', course_id=course_id))

    lessons = get_course_lessons(course_id)
    # Determine current lesson based on progress
    current_progress = enrollment['progress']
    current_lesson_index = min(len(lessons)-1, current_progress // (100 // len(lessons)))
    current_lesson = lessons[current_lesson_index]

    return render_template('course_learning.html', username=username, course=course, lessons=lessons, current_lesson=current_lesson, progress=enrollment['progress'])


@app.route('/learn/<course_id>/complete_lesson', methods=['POST'])
def complete_lesson(course_id):
    username = DEFAULT_USERNAME
    lesson_id = request.form.get('lesson_id')
    if not lesson_id:
        abort(400, description='Missing lesson_id in form data')

    enrollments = load_enrollments()
    enrollment = find_enrollment_by_user_course(username, course_id, enrollments)
    if not enrollment:
        abort(403, description='Not enrolled in course')

    lessons = get_course_lessons(course_id)
    # Find lesson index
    lesson_index = None
    for idx, les in enumerate(lessons):
        if les['lesson_id'] == lesson_id:
            lesson_index = idx
            break
    if lesson_index is None:
        abort(404, description='Lesson not found')

    # Enforce sequential completion
    expected_progress = enrollment['progress']
    expected_index = expected_progress // (100 // len(lessons))
    if lesson_index != expected_index:
        # Trying to complete out of order
        abort(400, description='Cannot complete lessons out of order')

    # Update progress
    progress_per_lesson = 100 // len(lessons)
    new_progress = enrollment['progress'] + progress_per_lesson
    if new_progress > 100:
        new_progress = 100

    enrollment['progress'] = new_progress
    if new_progress == 100:
        enrollment['status'] = 'Completed'
        # Generate certificate
        certificates = load_certificates()
        already_certified = False
        for cert in certificates.values():
            if cert['username'] == username and cert['course_id'] == course_id:
                already_certified = True
                break
        if not already_certified:
            new_cert_id = generate_new_id(certificates)
            issue_date = datetime.now().date().isoformat()
            certificates[new_cert_id] = {
                'certificate_id': new_cert_id,
                'username': username,
                'course_id': course_id,
                'issue_date': issue_date
            }
            # Save certificates
            from functions import write_text_file
            content_cert = save_certificates(certificates)
            write_text_file({"filename": os.path.join(DATA_DIR, 'certificates.txt'), "content": content_cert})

    # Save updated enrollments
    from functions import write_text_file
    content_enr = save_enrollments(enrollments)
    write_text_file({"filename": os.path.join(DATA_DIR, 'enrollments.txt'), "content": content_enr})

    return redirect(url_for('course_learning', course_id=course_id))


@app.route('/assignments')
def my_assignments():
    username = DEFAULT_USERNAME
    users = load_users()
    if username not in users:
        abort(404, description='User not found')

    assignments = load_assignments()
    enrollments = load_enrollments()
    submissions = load_submissions()
    user_assignments = get_user_assignments(username, assignments, enrollments)

    results = []
    for a in user_assignments:
        submission = find_submission(username, a['assignment_id'], submissions)
        submission_status = 'Not Submitted'
        if submission:
            submission_status = 'Submitted'
        results.append({
            'assignment_id': a['assignment_id'],
            'course_id': a['course_id'],
            'title': a['title'],
            'description': a['description'],
            'due_date': a['due_date'],
            'max_points': a['max_points'],
            'submission_status': submission_status
        })

    return render_template('my_assignments.html', username=username, assignments=results)


@app.route('/assignment/<assignment_id>')
def submit_assignment_form(assignment_id):
    username = DEFAULT_USERNAME
    assignments = load_assignments()
    assignment = assignments.get(assignment_id)
    if not assignment:
        abort(404, description='Assignment not found')

    submissions = load_submissions()
    submission = find_submission(username, assignment_id, submissions)
    submission_text = submission['submission_text'] if submission else ''

    return render_template('submit_assignment.html', assignment=assignment, username=username, submission_text=submission_text)


@app.route('/assignment/<assignment_id>/submit', methods=['POST'])
def submit_assignment(assignment_id):
    username = DEFAULT_USERNAME
    submission_text = request.form.get('submission_text', '').strip()
    if not submission_text:
        abort(400, description='Submission text cannot be empty')

    assignments = load_assignments()
    if assignment_id not in assignments:
        abort(404, description='Assignment not found')

    submissions = load_submissions()
    # Check if submission already exists
    existing_sub = find_submission(username, assignment_id, submissions)
    from functions import write_text_file

    submit_date = datetime.now().date().isoformat()

    if existing_sub:
        # Update submission
        existing_sub['submission_text'] = submission_text
        existing_sub['submit_date'] = submit_date
        existing_sub['grade'] = None
        existing_sub['feedback'] = ''
    else:
        new_sub_id = generate_new_id(submissions)
        submissions[new_sub_id] = {
            'submission_id': new_sub_id,
            'assignment_id': assignment_id,
            'username': username,
            'submission_text': submission_text,
            'submit_date': submit_date,
            'grade': None,
            'feedback': ''
        }
    content = save_submissions(submissions)
    write_text_file({"filename": os.path.join(DATA_DIR, 'submissions.txt'), "content": content})

    return redirect(url_for('my_assignments'))


@app.route('/certificates')
def my_certificates():
    username = DEFAULT_USERNAME
    certificates = load_certificates()
    courses = load_courses()

    user_certs = []
    for cert in certificates.values():
        if cert['username'] == username:
            course = courses.get(cert['course_id'])
            course_title = course['title'] if course else ''
            user_certs.append({
                'certificate_id': cert['certificate_id'],
                'course_title': course_title,
                'issue_date': cert['issue_date']
            })

    return render_template('certificates.html', username=username, certificates=user_certs)


@app.route('/profile')
def user_profile():
    username = DEFAULT_USERNAME
    users = load_users()
    user = users.get(username)
    if not user:
        abort(404, description='User not found')

    return render_template('profile.html', username=username, email=user['email'], fullname=user['fullname'])


@app.route('/profile/update', methods=['POST'])
def update_profile():
    username = DEFAULT_USERNAME
    updated_email = request.form.get('updated_email', '').strip()
    updated_fullname = request.form.get('updated_fullname', '').strip()

    if not updated_email or not updated_fullname:
        abort(400, description='Email and fullname cannot be empty')

    users = load_users()
    if username not in users:
        abort(404, description='User not found')

    users[username]['email'] = updated_email
    users[username]['fullname'] = updated_fullname

    content = save_users(users)
    from functions import write_text_file
    write_text_file({"filename": os.path.join(DATA_DIR, 'users.txt'), "content": content})

    return redirect(url_for('user_profile'))


if __name__ == '__main__':
    # Make sure data dir exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True, port=5000)
