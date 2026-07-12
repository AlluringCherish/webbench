from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

DATA_DIR = 'data'

# ===== Utility functions to read and write data files =====

def read_users():
    path = os.path.join(DATA_DIR, 'users.txt')
    users = {}
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            username, email, fullname = parts
            users[username] = {
                'username': username,
                'email': email,
                'fullname': fullname
            }
    return users

def write_users(users):
    path = os.path.join(DATA_DIR, 'users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for u in users.values():
            line = '|'.join([u['username'], u['email'], u['fullname']])
            f.write(line + '\n')


def read_courses():
    path = os.path.join(DATA_DIR, 'courses.txt')
    courses = {}
    if not os.path.exists(path):
        return courses
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            course_id, title, description, category, level, duration, status = parts
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

def write_courses(courses):
    path = os.path.join(DATA_DIR, 'courses.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for c in courses.values():
            line = '|'.join([c['course_id'], c['title'], c['description'], c['category'], c['level'], c['duration'], c['status']])
            f.write(line + '\n')


def read_enrollments():
    path = os.path.join(DATA_DIR, 'enrollments.txt')
    enrollments = []
    if not os.path.exists(path):
        return enrollments
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            enrollment_id, username, course_id, enrollment_date, progress, status = parts
            enrollments.append({
                'enrollment_id': enrollment_id,
                'username': username,
                'course_id': course_id,
                'enrollment_date': enrollment_date,
                'progress': int(progress),
                'status': status
            })
    return enrollments

def write_enrollments(enrollments):
    path = os.path.join(DATA_DIR, 'enrollments.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for e in enrollments:
            line = '|'.join([
                e['enrollment_id'],
                e['username'],
                e['course_id'],
                e['enrollment_date'],
                str(e['progress']),
                e['status']
            ])
            f.write(line + '\n')


def read_assignments():
    path = os.path.join(DATA_DIR, 'assignments.txt')
    assignments = {}
    if not os.path.exists(path):
        return assignments
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            assignment_id, course_id, title, description, due_date, max_points = parts
            assignments[assignment_id] = {
                'assignment_id': assignment_id,
                'course_id': course_id,
                'title': title,
                'description': description,
                'due_date': due_date,
                'max_points': int(max_points)
            }
    return assignments


def write_assignments(assignments):
    # assignments is dict
    path = os.path.join(DATA_DIR, 'assignments.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for a in assignments.values():
            line = '|'.join([
                a['assignment_id'],
                a['course_id'],
                a['title'],
                a['description'],
                a['due_date'],
                str(a['max_points'])
            ])
            f.write(line + '\n')


def read_submissions():
    path = os.path.join(DATA_DIR, 'submissions.txt')
    submissions = []
    if not os.path.exists(path):
        return submissions
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            submission_id, assignment_id, username, submission_text, submit_date, grade, feedback = parts
            submissions.append({
                'submission_id': submission_id,
                'assignment_id': assignment_id,
                'username': username,
                'submission_text': submission_text,
                'submit_date': submit_date,
                'grade': int(grade) if grade.isdigit() else None,
                'feedback': feedback
            })
    return submissions

def write_submissions(submissions):
    path = os.path.join(DATA_DIR, 'submissions.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for s in submissions:
            grade_str = str(s['grade']) if s['grade'] is not None else ''
            line = '|'.join([
                s['submission_id'],
                s['assignment_id'],
                s['username'],
                s['submission_text'],
                s['submit_date'],
                grade_str,
                s['feedback']
            ])
            f.write(line + '\n')


def read_certificates():
    path = os.path.join(DATA_DIR, 'certificates.txt')
    certificates = []
    if not os.path.exists(path):
        return certificates
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 4:
                continue
            certificate_id, username, course_id, issue_date = parts
            certificates.append({
                'certificate_id': certificate_id,
                'username': username,
                'course_id': course_id,
                'issue_date': issue_date
            })
    return certificates

def write_certificates(certificates):
    path = os.path.join(DATA_DIR, 'certificates.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for c in certificates:
            line = '|'.join([
                c['certificate_id'],
                c['username'],
                c['course_id'],
                c['issue_date']
            ])
            f.write(line + '\n')

# =========== Helper functions for business logic ===========

def get_next_enrollment_id(enrollments):
    max_id = 0
    for e in enrollments:
        try:
            i = int(e['enrollment_id'])
            if i > max_id:
                max_id = i
        except:
            continue
    return str(max_id+1)

def get_next_submission_id(submissions):
    max_id = 0
    for s in submissions:
        try:
            i = int(s['submission_id'])
            if i > max_id:
                max_id = i
        except:
            continue
    return str(max_id+1)

def get_next_certificate_id(certificates):
    max_id = 0
    for c in certificates:
        try:
            i = int(c['certificate_id'])
            if i > max_id:
                max_id = i
        except:
            continue
    return str(max_id+1)

def get_enrollment(username, course_id):
    enrollments = read_enrollments()
    for e in enrollments:
        if e['username'] == username and e['course_id'] == course_id:
            return e
    return None


def update_enrollment(enrollment):
    enrollments = read_enrollments()
    new_enrollments = []
    found = False
    for e in enrollments:
        if e['enrollment_id'] == enrollment['enrollment_id']:
            new_enrollments.append(enrollment)
            found = True
        else:
            new_enrollments.append(e)
    if not found:
        new_enrollments.append(enrollment)
    write_enrollments(new_enrollments)

# We'll create a stub to get lessons for a course, since lessons structure is not defined in data files.
# We'll simulate lessons by creating 5 lessons per course with ids 1..5, order 1..5, titles "Lesson 1" etc.
# Content is dummy text.
def get_lessons_for_course(course_id):
    lessons = []
    for i in range(1,6):
        lessons.append({
            'lesson_id': str(i),
            'title': f'Lesson {i}',
            'content': f'Content for lesson {i} of course {course_id}.',
            'order': i
        })
    return lessons

# Calculate progress in percent based on completed lessons
# Assuming equal weight for each lesson.
def calculate_progress(completed_lessons, lessons):
    if not lessons:
        return 0
    total = len(lessons)
    completed_count = len(completed_lessons)
    progress = int((completed_count / total) * 100)
    return progress

# Check if user should be awarded certificate for a course
# Award if enrollment progress is 100 and no certificate exists

def certificate_exists(username, course_id):
    certificates = read_certificates()
    for cert in certificates:
        if cert['username'] == username and cert['course_id'] == course_id:
            return True
    return False

def generate_certificate(username, course_id):
    certificates = read_certificates()
    new_id = get_next_certificate_id(certificates)
    issue_date = datetime.now().strftime('%Y-%m-%d')
    certificates.append({
        'certificate_id': new_id,
        'username': username,
        'course_id': course_id,
        'issue_date': issue_date
    })
    write_certificates(certificates)
    return certificates[-1]

# Get all certificates for a user with course title

def get_user_certificates_with_title(username):
    certificates = read_certificates()
    courses = read_courses()
    user_certs = []
    for c in certificates:
        if c['username'] == username:
            course_title = courses.get(c['course_id'], {}).get('title', '')
            user_certs.append({
                'certificate_id': c['certificate_id'],
                'course_id': c['course_id'],
                'issue_date': c['issue_date'],
                'course_title': course_title
            })
    return user_certs

# Get assignments for user courses (courses user is enrolled in)
def get_assignments_for_user(username):
    enrollments = read_enrollments()
    user_courses = set(e['course_id'] for e in enrollments if e['username'] == username)
    assignments_all = read_assignments()
    user_assignments = [a for a in assignments_all.values() if a['course_id'] in user_courses]
    return user_assignments

# Get submissions dict keyed by assignment_id for user
# Use the first found submission per assignment

def get_submissions_for_user(username):
    submissions = read_submissions()
    subs_dict = {}
    for s in submissions:
        if s['username'] == username and s['assignment_id'] not in subs_dict:
            subs_dict[s['assignment_id']] = s
    return subs_dict

# Get enrollment progress records of completed lessons for user and course
# We do not have a separate tracking for completed lessons, so we store progress only.
# For lesson completion, we assume sequential completion and update progress accordingly.

@app.route('/')
def root_redirect():
    return redirect(url_for('show_dashboard'))

# We do NOT have authentication in spec.
# We will assume username is fixed as 'john' (student john) for all operations requiring user context.
USERNAME = 'john'

@app.route('/dashboard')
def show_dashboard():
    users = read_users()
    user = users.get(USERNAME)
    if not user:
        return "User not found", 404
    enrollments = read_enrollments()
    courses = read_courses()
    enrolled_courses = []
    for e in enrollments:
        if e['username'] == USERNAME:
            c = courses.get(e['course_id'])
            if c:
                enrolled_courses.append({
                    'course_id': e['course_id'],
                    'title': c['title'],
                    'progress': e['progress']
                })
    return render_template('dashboard.html', username=user['username'], fullname=user['fullname'], enrolled_courses=enrolled_courses)

@app.route('/catalog')
def show_catalog():
    courses = list(read_courses().values())
    return render_template('course_catalog.html', courses=courses)

@app.route('/catalog/search', methods=['POST'])
def search_courses():
    search_term = request.form.get('search_term', '').strip().lower()
    all_courses = list(read_courses().values())
    if search_term == '':
        filtered = all_courses
    else:
        filtered = []
        for c in all_courses:
            if (
                search_term in c['title'].lower() or
                search_term in c['description'].lower() or
                search_term in c['category'].lower() or
                search_term in c['level'].lower() or
                search_term in c['status'].lower()
            ):
                filtered.append(c)
    return render_template('course_catalog.html', courses=filtered, search_term=search_term)

@app.route('/course/<course_id>')
def show_course_details(course_id):
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        return "Course not found", 404
    enrolled = False
    enrollment = get_enrollment(USERNAME, course_id)
    if enrollment:
        enrolled = True
    return render_template('course_details.html', course=course, enrolled=enrolled)

@app.route('/course/<course_id>/enroll', methods=['POST'])
def enroll_course(course_id):
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        return "Course not found", 404
    enrolled = False
    enrollment = get_enrollment(USERNAME, course_id)
    if enrollment:
        enrolled = True
    if enrolled:
        # Already enrolled
        return render_template('course_details.html', course=course, enrolled=True, enrollment_success=False, enrollment_date=enrollment['enrollment_date'])

    enrollments = read_enrollments()
    new_id = get_next_enrollment_id(enrollments)
    enrollment_date = datetime.now().strftime('%Y-%m-%d')
    new_enrollment = {
        'enrollment_id': new_id,
        'username': USERNAME,
        'course_id': course_id,
        'enrollment_date': enrollment_date,
        'progress': 0,
        'status': 'In Progress'
    }
    enrollments.append(new_enrollment)
    write_enrollments(enrollments)
    return render_template('course_details.html', course=course, enrolled=True, enrollment_success=True, enrollment_date=enrollment_date)

@app.route('/my-courses')
def show_my_courses():
    users = read_users()
    user = users.get(USERNAME)
    if not user:
        return "User not found", 404
    enrollments = read_enrollments()
    courses = read_courses()
    user_courses = []
    for e in enrollments:
        if e['username'] == USERNAME:
            c = courses.get(e['course_id'])
            if c:
                user_courses.append({
                    'course_id': e['course_id'],
                    'title': c['title'],
                    'progress': e['progress']
                })
    return render_template('my_courses.html', username=user['username'], courses=user_courses)

@app.route('/learning/<course_id>')
def learn_course(course_id):
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        return "Course not found", 404

    enrollment = get_enrollment(USERNAME, course_id)
    if not enrollment:
        # Not enrolled
        return redirect(url_for('show_course_details', course_id=course_id))

    lessons = get_lessons_for_course(course_id)
    # We store completed lessons as numbers from 1 to progress/percent?
    # Progress is percentage, with 5 lessons assume each lesson worth 20%
    completed_count = int(enrollment['progress'] / 20)
    completed_lessons = [str(i) for i in range(1, completed_count+1)]
    progress = enrollment['progress']

    return render_template('course_learning.html', course=course, lessons=lessons, completed_lessons=completed_lessons, progress=progress)

@app.route('/learning/<course_id>/complete', methods=['POST'])
def complete_lesson(course_id):
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        return "Course not found", 404

    enrollment = get_enrollment(USERNAME, course_id)
    if not enrollment:
        return redirect(url_for('show_course_details', course_id=course_id))

    lessons = get_lessons_for_course(course_id)
    completed_count = int(enrollment['progress'] / 20)  # Each lesson 20%
    total_lessons = len(lessons)

    lesson_completed = False
    certificate_generated = False

    # Complete next lesson if any left
    if completed_count < total_lessons:
        completed_count += 1
        new_progress = completed_count * 20
        enrollment['progress'] = new_progress
        if new_progress >= 100:
            enrollment['status'] = 'Completed'
        else:
            enrollment['status'] = 'In Progress'
        update_enrollment(enrollment)
        lesson_completed = True

        # Check certificate generation
        if enrollment['progress'] == 100:
            if not certificate_exists(USERNAME, course_id):
                generate_certificate(USERNAME, course_id)
                certificate_generated = True

    completed_lessons = [str(i) for i in range(1, completed_count+1)]
    progress = enrollment['progress']

    return render_template('course_learning.html', course=course, lessons=lessons, completed_lessons=completed_lessons, progress=progress, lesson_completed=lesson_completed, certificate_generated=certificate_generated)

@app.route('/assignments')
def show_assignments():
    users = read_users()
    user = users.get(USERNAME)
    if not user:
        return "User not found", 404
    assignments = get_assignments_for_user(USERNAME)
    submissions = get_submissions_for_user(USERNAME)
    return render_template('my_assignments.html', username=USERNAME, assignments=assignments, submissions=submissions)

@app.route('/assignments/<assignment_id>/submit', methods=['GET'])
def show_submit_assignment(assignment_id):
    assignments = read_assignments()
    assignment = assignments.get(assignment_id)
    if not assignment:
        return "Assignment not found", 404
    return render_template('submit_assignment.html', assignment=assignment)

@app.route('/assignments/<assignment_id>/submit', methods=['POST'])
def submit_assignment_post(assignment_id):
    assignments = read_assignments()
    assignment = assignments.get(assignment_id)
    if not assignment:
        return "Assignment not found", 404

    submission_text = request.form.get('submission_text', '').strip()
    if not submission_text:
        return render_template('submit_assignment.html', assignment=assignment, submission_success=False, confirmation_message='Submission text cannot be empty.')

    submissions = read_submissions()
    # Check if user already submitted
    for s in submissions:
        if s['assignment_id'] == assignment_id and s['username'] == USERNAME:
            return render_template('submit_assignment.html', assignment=assignment, submission_success=False, confirmation_message='You have already submitted this assignment.')

    new_id = get_next_submission_id(submissions)
    submit_date = datetime.now().strftime('%Y-%m-%d')
    new_submission = {
        'submission_id': new_id,
        'assignment_id': assignment_id,
        'username': USERNAME,
        'submission_text': submission_text,
        'submit_date': submit_date,
        'grade': None,
        'feedback': ''
    }
    submissions.append(new_submission)
    write_submissions(submissions)

    return render_template('submit_assignment.html', assignment=assignment, submission_success=True, confirmation_message='Assignment submitted successfully.')

@app.route('/certificates')
def show_certificates():
    users = read_users()
    user = users.get(USERNAME)
    if not user:
        return "User not found", 404
    user_certificates = get_user_certificates_with_title(USERNAME)
    return render_template('certificates.html', username=USERNAME, certificates=user_certificates)

@app.route('/profile')
def show_profile():
    users = read_users()
    user = users.get(USERNAME)
    if not user:
        return "User not found", 404
    return render_template('user_profile.html', username=USERNAME, email=user['email'], fullname=user['fullname'])

@app.route('/profile/update', methods=['POST'])
def update_profile():
    users = read_users()
    user = users.get(USERNAME)
    if not user:
        return "User not found", 404
    email = request.form.get('email', '').strip()
    fullname = request.form.get('fullname', '').strip()
    errors = []
    if not email:
        errors.append('Email cannot be empty.')
    if not fullname:
        errors.append('Full name cannot be empty.')
    if errors:
        return render_template('user_profile.html', username=USERNAME, email=email, fullname=fullname, update_success=False, errors=errors)

    # Update user info
    user['email'] = email
    user['fullname'] = fullname
    users[USERNAME] = user
    write_users(users)

    return render_template('user_profile.html', username=USERNAME, email=email, fullname=fullname, update_success=True, errors=None)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
