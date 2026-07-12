from flask import Flask, render_template, request, redirect, url_for, abort
from datetime import datetime
import os

app = Flask(__name__)
DATA_DIR = 'data'

# Helper Functions for Reading and Writing Data Files

def read_users():
    users = {}
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                username, email, fullname = line.split('|')
                users[username] = {'username': username, 'email': email, 'fullname': fullname}
    except FileNotFoundError:
        pass
    return users


def read_courses():
    courses = {}
    try:
        with open(os.path.join(DATA_DIR, 'courses.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                course_id, title, description, category, level, duration, status = line.split('|')
                courses[int(course_id)] = {
                    'course_id': int(course_id),
                    'title': title,
                    'description': description,
                    'category': category,
                    'level': level,
                    'duration': duration,
                    'status': status
                }
    except FileNotFoundError:
        pass
    return courses


def read_enrollments():
    enrollments = []
    try:
        with open(os.path.join(DATA_DIR, 'enrollments.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 6:
                    continue
                enrollment_id, username, course_id, enrollment_date, progress, status = parts
                enrollments.append({
                    'enrollment_id': int(enrollment_id),
                    'username': username,
                    'course_id': int(course_id),
                    'enrollment_date': enrollment_date,
                    'progress': float(progress),
                    'status': status
                })
    except FileNotFoundError:
        pass
    return enrollments


def write_enrollments(enrollments):
    lines = []
    for e in enrollments:
        line = f"{e['enrollment_id']}|{e['username']}|{e['course_id']}|{e['enrollment_date']}|{e['progress']}|{e['status']}"
        lines.append(line)
    with open(os.path.join(DATA_DIR, 'enrollments.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines)+'\n')


def read_assignments():
    assignments = {}
    try:
        with open(os.path.join(DATA_DIR, 'assignments.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                assignment_id, course_id, title, description, due_date, max_points = line.split('|')
                assignments[int(assignment_id)] = {
                    'assignment_id': int(assignment_id),
                    'course_id': int(course_id),
                    'title': title,
                    'description': description,
                    'due_date': due_date,
                    'max_points': int(max_points)
                }
    except FileNotFoundError:
        pass
    return assignments


def read_submissions():
    submissions = []
    try:
        with open(os.path.join(DATA_DIR, 'submissions.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                submission_id, assignment_id, username, submission_text, submit_date, grade, feedback = parts
                submissions.append({
                    'submission_id': int(submission_id),
                    'assignment_id': int(assignment_id),
                    'username': username,
                    'submission_text': submission_text,
                    'submit_date': submit_date,
                    'grade': int(grade) if grade.isdigit() else None,
                    'feedback': feedback
                })
    except FileNotFoundError:
        pass
    return submissions


def write_submissions(submissions):
    lines = []
    for s in submissions:
        grade_str = str(s['grade']) if s['grade'] is not None else ''
        line = f"{s['submission_id']}|{s['assignment_id']}|{s['username']}|{s['submission_text']}|{s['submit_date']}|{grade_str}|{s['feedback']}"
        lines.append(line)
    with open(os.path.join(DATA_DIR, 'submissions.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines)+'\n')


def read_certificates():
    certificates = []
    try:
        with open(os.path.join(DATA_DIR, 'certificates.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                certificate_id, username, course_id, issue_date = line.split('|')
                certificates.append({
                    'certificate_id': int(certificate_id),
                    'username': username,
                    'course_id': int(course_id),
                    'issue_date': issue_date
                })
    except FileNotFoundError:
        pass
    return certificates


def write_certificates(certificates):
    lines = []
    for c in certificates:
        line = f"{c['certificate_id']}|{c['username']}|{c['course_id']}|{c['issue_date']}"
        lines.append(line)
    with open(os.path.join(DATA_DIR, 'certificates.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines)+'\n')


def save_users(users):
    lines = []
    for u in users.values():
        line = f"{u['username']}|{u['email']}|{u['fullname']}"
        lines.append(line)
    with open(os.path.join(DATA_DIR, 'users.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines)+'\n')

# Utilities

def generate_new_id(items, key):
    if not items:
        return 1
    return max(item[key] for item in items) + 1

# Enrollment related

def user_enrolled(username, course_id, enrollments):
    for e in enrollments:
        if e['username'] == username and e['course_id'] == course_id:
            return True
    return False

def get_enrollment(username, course_id, enrollments):
    for e in enrollments:
        if e['username'] == username and e['course_id'] == course_id:
            return e
    return None

# Lessons Handling (simulate lessons by divided chapters of description for demonstration)
# Since lessons are not in provided data files, we'll mock lessons by splitting description into parts.

def get_lessons_for_course(course):
    # Simple mock: split description by sentences or chunks as lessons
    desc = course.get('description', '')
    parts = [part.strip() for part in desc.split('.') if part.strip()]
    lessons = []
    for i, part in enumerate(parts, start=1):
        lessons.append({'lesson_id': i, 'title': f'Lesson {i}', 'content': part})
    return lessons

# User authentication stub (In real app, would integrate login sessions etc.)
# For simplicity, we assume current user is 'john' for all routes.

CURRENT_USER = 'john'

# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    users = read_users()
    if CURRENT_USER not in users:
        abort(404)
    user = users[CURRENT_USER]

    enrollments = read_enrollments()
    courses = read_courses()
    enrolled_courses = []
    for e in enrollments:
        if e['username'] == CURRENT_USER:
            c = courses.get(e['course_id'])
            if c:
                enrolled_courses.append({
                    'course_id': c['course_id'],
                    'title': c['title'],
                    'progress': e['progress']
                })

    return render_template('dashboard.html', username=CURRENT_USER, fullname=user['fullname'], enrolled_courses=enrolled_courses)

@app.route('/catalog')
def course_catalog():
    search_query = request.args.get('search_query', '').strip()
    courses = read_courses()
    filtered_courses = []
    if search_query:
        sq_lower = search_query.lower()
        for c in courses.values():
            if (sq_lower in c['title'].lower() or sq_lower in c['description'].lower() or
                sq_lower in c['category'].lower() or sq_lower in c['level'].lower() or sq_lower in c['status'].lower()):
                filtered_courses.append(c)
    else:
        filtered_courses = list(courses.values())
    return render_template('catalog.html', courses=filtered_courses, search_query=search_query)

@app.route('/course/<int:course_id>', methods=['GET', 'POST'])
def course_details(course_id):
    courses = read_courses()
    users = read_users()
    enrollments = read_enrollments()

    course = courses.get(course_id)
    if not course:
        abort(404)

    enrolled = user_enrolled(CURRENT_USER, course_id, enrollments)

    if request.method == 'POST':
        # Enroll user
        if not enrolled:
            new_id = generate_new_id(enrollments, 'enrollment_id')
            enrollment_date = datetime.today().strftime('%Y-%m-%d')
            enrollments.append({
                'enrollment_id': new_id,
                'username': CURRENT_USER,
                'course_id': course_id,
                'enrollment_date': enrollment_date,
                'progress': 0.0,
                'status': 'In Progress'
            })
            write_enrollments(enrollments)
            enrolled = True

    return render_template('course_details.html', course=course, enrolled=enrolled)

@app.route('/my-courses')
def my_courses():
    users = read_users()
    enrollments = read_enrollments()
    courses = read_courses()

    if CURRENT_USER not in users:
        abort(404)

    enrolled_courses = []
    for e in enrollments:
        if e['username'] == CURRENT_USER:
            c = courses.get(e['course_id'])
            if c:
                enrolled_courses.append({
                    'course_id': c['course_id'],
                    'title': c['title'],
                    'progress': e['progress']
                })

    return render_template('my_courses.html', username=CURRENT_USER, enrolled_courses=enrolled_courses)

@app.route('/learning/<int:course_id>', methods=['GET', 'POST'])
def course_learning(course_id):
    courses = read_courses()
    enrollments = read_enrollments()

    course = courses.get(course_id)
    if not course:
        abort(404)

    enrollment = get_enrollment(CURRENT_USER, course_id, enrollments)
    if not enrollment:
        # User must be enrolled
        return redirect(url_for('course_details', course_id=course_id))

    lessons = get_lessons_for_course(course)

    # Progress: 0% - no lessons done, 100% all lessons done
    # We track progress as percentage of lessons completed.
    # We assume lessons are sequential and user can only mark current lesson complete in order.

    progress = enrollment['progress']
    num_lessons = len(lessons)
    lessons_completed = int(progress / 100.0 * num_lessons) if num_lessons > 0 else 0
    current_lesson_index = lessons_completed if lessons_completed < num_lessons else num_lessons - 1
    current_lesson = lessons[current_lesson_index] if lessons else None

    progress_updated = False
    if request.method == 'POST':
        # Mark current lesson as complete
        if lessons_completed < num_lessons:
            lessons_completed += 1
            new_progress = (lessons_completed / num_lessons) * 100
            enrollment['progress'] = round(new_progress, 2)
            if enrollment['progress'] >= 100:
                enrollment['progress'] = 100.0
                enrollment['status'] = 'Completed'
                # check if certificate exists else create
                certificates = read_certificates()
                cert_exists = False
                for cert in certificates:
                    if cert['username'] == CURRENT_USER and cert['course_id'] == course_id:
                        cert_exists = True
                        break
                if not cert_exists:
                    new_cert_id = generate_new_id(certificates, 'certificate_id')
                    issue_date = datetime.today().strftime('%Y-%m-%d')
                    certificates.append({
                        'certificate_id': new_cert_id,
                        'username': CURRENT_USER,
                        'course_id': course_id,
                        'issue_date': issue_date
                    })
                    write_certificates(certificates)
            enrollment['status'] = 'Completed' if enrollment['progress'] == 100 else 'In Progress'
            write_enrollments(enrollments)
            progress = enrollment['progress']
            progress_updated = True
            if lessons_completed > 0 and lessons_completed <= num_lessons:
                current_lesson = lessons[lessons_completed-1]

    return render_template('course_learning.html',
                           course=course,
                           lessons=lessons,
                           current_lesson=current_lesson,
                           progress=progress,
                           enrollment_id=enrollment['enrollment_id'])

@app.route('/assignments')
def my_assignments():
    assignments = read_assignments()
    enrollments = read_enrollments()
    submissions = read_submissions()
    courses = read_courses()

    # User must have at least one enrollment to get assignments
    user_enrollments = [e for e in enrollments if e['username'] == CURRENT_USER]
    user_course_ids = {e['course_id'] for e in user_enrollments}

    user_assignments = []
    today_str = datetime.today().strftime('%Y-%m-%d')
    
    for assignment in assignments.values():
        if assignment['course_id'] in user_course_ids:
            # Determine submission status
            submissions_for_assignment = [s for s in submissions if s['assignment_id'] == assignment['assignment_id'] and s['username'] == CURRENT_USER]
            status = 'Pending'
            if submissions_for_assignment:
                # Assume latest submission is status
                status = 'Submitted'
            user_assignments.append({
                'assignment_id': assignment['assignment_id'],
                'title': assignment['title'],
                'description': assignment['description'],
                'due_date': assignment['due_date'],
                'max_points': assignment['max_points'],
                'status': status
            })
    return render_template('assignments.html', username=CURRENT_USER, assignments=user_assignments)

@app.route('/submit-assignment/<int:assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    assignments = read_assignments()
    submissions = read_submissions()

    assignment = assignments.get(assignment_id)
    if not assignment:
        abort(404)

    submission_status = 'Not Submitted'
    confirmation_message = None

    # Check if already submitted
    for s in submissions:
        if s['assignment_id'] == assignment_id and s['username'] == CURRENT_USER:
            submission_status = 'Submitted'
            break

    if request.method == 'POST':
        submission_text = request.form.get('submission_text', '').strip()
        if submission_text == '':
            confirmation_message = 'Submission text cannot be empty.'
        else:
            new_id = generate_new_id(submissions, 'submission_id')
            submit_date = datetime.today().strftime('%Y-%m-%d')
            # grade and feedback empty initially
            submissions.append({
                'submission_id': new_id,
                'assignment_id': assignment_id,
                'username': CURRENT_USER,
                'submission_text': submission_text,
                'submit_date': submit_date,
                'grade': None,
                'feedback': ''
            })
            write_submissions(submissions)
            submission_status = 'Submitted'
            confirmation_message = 'Assignment submitted successfully.'

    return render_template('submit_assignment.html', assignment=assignment, submission_status=submission_status, confirmation_message=confirmation_message)

@app.route('/certificates')
def certificates_page():
    certificates = read_certificates()
    courses = read_courses()

    user_certs = []
    for c in certificates:
        if c['username'] == CURRENT_USER:
            course = courses.get(c['course_id'])
            if course:
                user_certs.append({
                    'certificate_id': c['certificate_id'],
                    'course_id': c['course_id'],
                    'title': course['title'],
                    'issue_date': c['issue_date']
                })

    return render_template('certificates.html', username=CURRENT_USER, certificates=user_certs)

@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    users = read_users()
    if CURRENT_USER not in users:
        abort(404)
    user = users[CURRENT_USER]
    update_status = None

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        fullname = request.form.get('fullname', '').strip()
        if not email or not fullname:
            update_status = 'Email and Full Name cannot be empty.'
        else:
            user['email'] = email
            user['fullname'] = fullname
            # Save back
            save_users(users)
            update_status = 'Profile updated successfully.'

    return render_template('profile.html', user=user, update_status=update_status)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
