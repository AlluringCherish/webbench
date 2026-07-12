from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)

DATA_DIR = 'data'

# Utility functions to load and save pipe-delimited data files for each data type

def load_users():
    path = os.path.join(DATA_DIR, 'users.txt')
    users = []
    if os.path.exists(path):
        with open(path, 'r',encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=3:
                    continue
                user = {'username': parts[0], 'email': parts[1], 'fullname': parts[2]}
                users.append(user)
    return users

def save_users(users):
    path = os.path.join(DATA_DIR, 'users.txt')
    with open(path, 'w',encoding='utf-8') as f:
        for u in users:
            f.write(f"{u['username']}|{u['email']}|{u['fullname']}\n")


def load_courses():
    path = os.path.join(DATA_DIR, 'courses.txt')
    courses = []
    if os.path.exists(path):
        with open(path, 'r',encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=7:
                    continue
                course = {
                    'course_id': int(parts[0]),
                    'title': parts[1],
                    'description': parts[2],
                    'category': parts[3],
                    'level': parts[4],
                    'duration': parts[5],
                    'status': parts[6]
                }
                courses.append(course)
    return courses


def save_courses(courses):
    path = os.path.join(DATA_DIR, 'courses.txt')
    with open(path, 'w',encoding='utf-8') as f:
        for c in courses:
            f.write(f"{c['course_id']}|{c['title']}|{c['description']}|{c['category']}|{c['level']}|{c['duration']}|{c['status']}\n")


def load_enrollments():
    path = os.path.join(DATA_DIR, 'enrollments.txt')
    enrollments = []
    if os.path.exists(path):
        with open(path, 'r',encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=6:
                    continue
                enrollment = {
                    'enrollment_id': int(parts[0]),
                    'username': parts[1],
                    'course_id': int(parts[2]),
                    'enrollment_date': parts[3],
                    'progress': int(parts[4]),
                    'status': parts[5]
                }
                enrollments.append(enrollment)
    return enrollments


def save_enrollments(enrollments):
    path = os.path.join(DATA_DIR, 'enrollments.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for e in enrollments:
            f.write(f"{e['enrollment_id']}|{e['username']}|{e['course_id']}|{e['enrollment_date']}|{e['progress']}|{e['status']}\n")


def load_assignments():
    path = os.path.join(DATA_DIR, 'assignments.txt')
    assignments = []
    if os.path.exists(path):
        with open(path, 'r',encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=6:
                    continue
                assignment = {
                    'assignment_id': int(parts[0]),
                    'course_id': int(parts[1]),
                    'title': parts[2],
                    'description': parts[3],
                    'due_date': parts[4],
                    'max_points': int(parts[5])
                }
                assignments.append(assignment)
    return assignments


def save_assignments(assignments):
    path = os.path.join(DATA_DIR, 'assignments.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for a in assignments:
            f.write(f"{a['assignment_id']}|{a['course_id']}|{a['title']}|{a['description']}|{a['due_date']}|{a['max_points']}\n")


def load_submissions():
    path = os.path.join(DATA_DIR, 'submissions.txt')
    submissions = []
    if os.path.exists(path):
        with open(path, 'r',encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=7:
                    continue
                submission = {
                    'submission_id': int(parts[0]),
                    'assignment_id': int(parts[1]),
                    'username': parts[2],
                    'submission_text': parts[3],
                    'submit_date': parts[4],
                    'grade': parts[5],
                    'feedback': parts[6]
                }
                submissions.append(submission)
    return submissions


def save_submissions(submissions):
    path = os.path.join(DATA_DIR, 'submissions.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for s in submissions:
            f.write(f"{s['submission_id']}|{s['assignment_id']}|{s['username']}|{s['submission_text']}|{s['submit_date']}|{s['grade']}|{s['feedback']}\n")


def load_certificates():
    path = os.path.join(DATA_DIR, 'certificates.txt')
    certificates = []
    if os.path.exists(path):
        with open(path, 'r',encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=4:
                    continue
                certificate = {
                    'certificate_id': int(parts[0]),
                    'username': parts[1],
                    'course_id': int(parts[2]),
                    'issue_date': parts[3]
                }
                certificates.append(certificate)
    return certificates


def save_certificates(certificates):
    path = os.path.join(DATA_DIR, 'certificates.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for c in certificates:
            f.write(f"{c['certificate_id']}|{c['username']}|{c['course_id']}|{c['issue_date']}\n")


# Helper to find user by username

def get_user(username):
    users = load_users()
    for u in users:
        if u['username'] == username:
            return u
    return None


def get_course(course_id):
    courses = load_courses()
    for c in courses:
        if c['course_id'] == course_id:
            return c
    return None


def get_enrollment(username, course_id):
    enrollments = load_enrollments()
    for e in enrollments:
        if e['username'] == username and e['course_id'] == course_id and e['status'] != 'Dropped':
            return e
    return None


def generate_new_enrollment_id(enrollments):
    if not enrollments:
        return 1
    return max(e['enrollment_id'] for e in enrollments) + 1

def generate_new_submission_id(submissions):
    if not submissions:
        return 1
    return max(s['submission_id'] for s in submissions) + 1

def generate_new_certificate_id(certificates):
    if not certificates:
        return 1
    return max(c['certificate_id'] for c in certificates) + 1

# In absence of lesson data file, mock lessons per course
# For each course_id simulate 5 lessons

def get_lessons_for_course(course_id):
    lessons = []
    for i in range(1,6):
        lessons.append({
            'lesson_id': i,
            'title': f'Lesson {i}',
            'content': f'Content of lesson {i} for course {course_id}'
        })
    return lessons

# Simulate progress per lesson: each lesson completion adds 20% (100/5)

# Extract username for current session - HERE we simulate getting username from hardcoded value or query param
# Since no login system specified, assume one user: 'john'

CURRENT_USERNAME = 'john'


@app.route('/')
def root_redirect():
    # Redirect to dashboard
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = CURRENT_USERNAME
    user = get_user(username)
    if not user:
        # User not found
        return "User not found", 404

    enrollments = load_enrollments()
    courses = load_courses()

    user_enrolled_courses = [
        e for e in enrollments 
        if e['username'] == username and e['status'] != 'Dropped'
    ]

    enrolled_courses = []
    user_enrolled_course_ids = []

    for e in user_enrolled_courses:
        course = get_course(e['course_id'])
        if course:
            enrolled_courses.append({'course_id': course['course_id'], 'title': course['title'], 'progress': e['progress']})
            user_enrolled_course_ids.append(course['course_id'])

    return render_template('dashboard.html', username=username, fullname=user['fullname'],
                           enrolled_courses=enrolled_courses, user_enrolled_course_ids=user_enrolled_course_ids)


@app.route('/catalog')
def course_catalog():
    courses = load_courses()
    return render_template('catalog.html', courses=courses)


@app.route('/course/<int:course_id>')
def course_details(course_id):
    username = CURRENT_USERNAME
    course = get_course(course_id)
    if not course:
        return "Course not found", 404

    enrollment = get_enrollment(username, course_id)
    enrolled = enrollment is not None
    enrollment_date = enrollment['enrollment_date'] if enrolled else None

    return render_template('course_details.html', course=course, enrolled=enrolled, enrollment_date=enrollment_date,
                           enroll_success=None, error_message=None)


@app.route('/course/<int:course_id>/enroll', methods=['POST'])
def enroll_course(course_id):
    username = CURRENT_USERNAME
    course = get_course(course_id)
    if not course:
        return "Course not found", 404

    enroll_success = False
    error_message = None

    enrollment = get_enrollment(username, course_id)
    if enrollment:
        enroll_success = False
        error_message = "Already enrolled in this course."
        return render_template('course_details.html', course=course, enrolled=True, 
                               enrollment_date=enrollment['enrollment_date'], enroll_success=enroll_success,
                               error_message=error_message)

    enrollments = load_enrollments()
    new_id = generate_new_enrollment_id(enrollments)
    today_str = datetime.now().strftime('%Y-%m-%d')
    new_enrollment = {
        'enrollment_id': new_id,
        'username': username,
        'course_id': course_id,
        'enrollment_date': today_str,
        'progress': 0,
        'status': 'In Progress'
    }
    enrollments.append(new_enrollment)
    try:
        save_enrollments(enrollments)
        enroll_success = True
        enrollment_date = today_str
        enrolled = True
    except Exception as e:
        enroll_success = False
        error_message = str(e)
        enrolled = False
        enrollment_date = None

    return render_template('course_details.html', course=course, enrolled=enrolled, 
                           enrollment_date=enrollment_date, enroll_success=enroll_success, error_message=error_message)


@app.route('/my-courses')
def my_courses():
    username = CURRENT_USERNAME
    enrollments = load_enrollments()
    courses = load_courses()

    user_enrolled_courses = [e for e in enrollments if e['username'] == username and e['status'] != 'Dropped']
    enrolled_courses = []
    for e in user_enrolled_courses:
        course = get_course(e['course_id'])
        if course:
            enrolled_courses.append({'course_id': course['course_id'], 'title': course['title'], 'progress': e['progress']})

    return render_template('my_courses.html', enrolled_courses=enrolled_courses, username=username)


@app.route('/learning/<int:course_id>')
def course_learning(course_id):
    username = CURRENT_USERNAME
    course = get_course(course_id)
    if not course:
        return "Course not found", 404
    enrollment = get_enrollment(username, course_id)
    if not enrollment:
        return redirect(url_for('course_details', course_id=course_id))

    lessons = get_lessons_for_course(course_id)
    total_lessons = len(lessons)
    progress = enrollment['progress']
    # Calculate current lesson index (0-based)
    # progress is in % (int), each lesson is (100/total_lessons)%
    completed_lessons_count = progress * total_lessons // 100
    lesson_index = completed_lessons_count

    # Current lesson
    if lesson_index < total_lessons:
        current_lesson = lessons[lesson_index]
    else:
        current_lesson = None

    return render_template('course_learning.html', course=course, lessons=lessons, 
                           current_lesson=current_lesson, progress=progress, lesson_index=lesson_index,
                           mark_success=None, error_message=None)


@app.route('/learning/<int:course_id>/mark_complete', methods=['POST'])
def mark_lesson_complete(course_id):
    username = CURRENT_USERNAME
    course = get_course(course_id)
    if not course:
        return "Course not found", 404
    enrollment = get_enrollment(username, course_id)
    if not enrollment:
        return redirect(url_for('course_details', course_id=course_id))

    lessons = get_lessons_for_course(course_id)
    total_lessons = len(lessons)
    progress = enrollment['progress']
    completed_lessons_count = progress * total_lessons // 100

    if completed_lessons_count >= total_lessons:
        # All lessons completed
        mark_success = False
        error_message = "All lessons already completed."
    else:
        # Mark current lesson complete
        new_completed_lessons = completed_lessons_count + 1
        new_progress = new_completed_lessons * 100 // total_lessons

        enrollments = load_enrollments()
        updated = False
        for e in enrollments:
            if e['username'] == username and e['course_id'] == course_id and e['status'] != 'Dropped':
                e['progress'] = new_progress
                if new_progress == 100:
                    e['status'] = 'Completed'
                updated = True
                break

        if updated:
            # Save enrollment progress
            try:
                save_enrollments(enrollments)
                mark_success = True
                error_message = None
                progress = new_progress
            except Exception as e:
                mark_success = False
                error_message = f"Failed to update progress: {str(e)}"
        else:
            mark_success = False
            error_message = "Enrollment not found during update."

        # If progress updated to 100%, generate certificate if not exists
        if mark_success and progress == 100:
            certificates = load_certificates()
            exists = any(c['username'] == username and c['course_id'] == course_id for c in certificates)
            if not exists:
                new_cert_id = generate_new_certificate_id(certificates)
                today_str = datetime.now().strftime('%Y-%m-%d')
                new_cert = {
                    'certificate_id': new_cert_id,
                    'username': username,
                    'course_id': course_id,
                    'issue_date': today_str
                }
                certificates.append(new_cert)
                try:
                    save_certificates(certificates)
                except Exception as e:
                    # Ignore certificate save failure for now
                    pass

    enrollment = get_enrollment(username, course_id)
    progress = enrollment['progress'] if enrollment else 0

    lessons = get_lessons_for_course(course_id)
    completed_lessons_count = progress * len(lessons) // 100
    lesson_index = completed_lessons_count
    current_lesson = lessons[lesson_index] if lesson_index < len(lessons) else None

    return render_template('course_learning.html', course=course, lessons=lessons, current_lesson=current_lesson,
                           progress=progress, lesson_index=lesson_index, mark_success=mark_success, error_message=error_message)


@app.route('/assignments')
def my_assignments():
    username = CURRENT_USERNAME
    assignments = load_assignments()
    enrollments = load_enrollments()
    # Filter assignments for courses the user is enrolled in (and not dropped)
    user_courses_ids = [e['course_id'] for e in enrollments if e['username'] == username and e['status'] != 'Dropped']
    user_assignments = [a for a in assignments if a['course_id'] in user_courses_ids]

    submissions = load_submissions()
    submissions_status = {}
    for a in user_assignments:
        found = False
        for s in submissions:
            if s['assignment_id'] == a['assignment_id'] and s['username'] == username:
                submissions_status[a['assignment_id']] = "Submitted"
                found = True
                break
        if not found:
            submissions_status[a['assignment_id']] = "Pending"

    return render_template('assignments.html', assignments=user_assignments, username=username, submissions_status=submissions_status)


@app.route('/assignment/<int:assignment_id>/submit', methods=['GET'])
def submit_assignment(assignment_id):
    username = CURRENT_USERNAME
    assignments = load_assignments()
    assignment = next((a for a in assignments if a['assignment_id'] == assignment_id), None)
    if not assignment:
        return "Assignment not found", 404

    # Check if user is enrolled in the course
    enrollment = get_enrollment(username, assignment['course_id'])
    if not enrollment:
        return redirect(url_for('my_assignments'))

    return render_template('submit_assignment.html', assignment=assignment, submission_text='')


@app.route('/assignment/<int:assignment_id>/submit', methods=['POST'])
def submit_assignment_post(assignment_id):
    username = CURRENT_USERNAME
    assignments = load_assignments()
    assignment = next((a for a in assignments if a['assignment_id'] == assignment_id), None)
    if not assignment:
        return "Assignment not found", 404

    submission_text = request.form.get('submission_text', '').strip()
    if not submission_text:
        error_message = "Submission text cannot be empty."
        return render_template('submit_assignment.html', assignment=assignment, submission_text=submission_text,
                               submit_success=False, error_message=error_message)

    # Check enrollment
    enrollment = get_enrollment(username, assignment['course_id'])
    if not enrollment:
        error_message = "You are not enrolled in the course for this assignment."
        return render_template('submit_assignment.html', assignment=assignment, submission_text=submission_text,
                               submit_success=False, error_message=error_message)

    # Add submission entry
    submissions = load_submissions()
    new_sub_id = generate_new_submission_id(submissions)
    today_str = datetime.now().strftime('%Y-%m-%d')
    new_submission = {
        'submission_id': new_sub_id,
        'assignment_id': assignment_id,
        'username': username,
        'submission_text': submission_text,
        'submit_date': today_str,
        'grade': '',
        'feedback': ''
    }
    submissions.append(new_submission)
    try:
        save_submissions(submissions)
        submit_success = True
        error_message = None
    except Exception as e:
        submit_success = False
        error_message = f"Failed to save submission: {str(e)}"

    return render_template('submit_assignment.html', assignment=assignment, submission_text=submission_text,
                           submit_success=submit_success, error_message=error_message)


@app.route('/certificates')
def certificates():
    username = CURRENT_USERNAME
    certificates = load_certificates()
    courses = load_courses()
    user_certs = [c for c in certificates if c['username'] == username]

    certs_dicts = []
    for c in user_certs:
        course = get_course(c['course_id'])
        if course:
            certs_dicts.append({'certificate_id': c['certificate_id'], 'course_id': course['course_id'],
                                'title': course['title'], 'issue_date': c['issue_date']})

    return render_template('certificates.html', certificates=certs_dicts, username=username)


@app.route('/profile')
def profile():
    username = CURRENT_USERNAME
    user = get_user(username)
    if not user:
        return "User not found", 404
    return render_template('profile.html', username=username, email=user['email'], fullname=user['fullname'])


@app.route('/profile/update', methods=['POST'])
def update_profile():
    username = CURRENT_USERNAME
    email = request.form.get('email', '').strip()
    fullname = request.form.get('fullname', '').strip()

    update_success = False
    error_message = None

    if not email or not fullname:
        error_message = "Email and Fullname cannot be empty."
        user = get_user(username)
        return render_template('profile.html', update_success=update_success, error_message=error_message,
                               username=username, email=email, fullname=fullname)

    users = load_users()
    user_found = False
    for u in users:
        if u['username'] == username:
            u['email'] = email
            u['fullname'] = fullname
            user_found = True
            break

    if not user_found:
        error_message = "User not found."
        return render_template('profile.html', update_success=update_success, error_message=error_message,
                               username=username, email=email, fullname=fullname)

    try:
        save_users(users)
        update_success = True
    except Exception as e:
        update_success = False
        error_message = f"Failed to update profile: {str(e)}"

    return render_template('profile.html', update_success=update_success, error_message=error_message,
                           username=username, email=email, fullname=fullname)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
