from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)

DATA_DIR = "data"

# Assume the logged-in user is 'john' for simplicity since no authentication is described
LOGGED_IN_USERNAME = "john"

# Utility functions for reading and writing pipe-delimited files

def read_pipe_delimited_file(filepath, field_names):
    data = []
    if not os.path.isfile(filepath):
        return data
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != len(field_names):
                continue
            record = dict(zip(field_names, parts))
            data.append(record)
    return data

# Write entire list of dicts to file with delimiter | in order of field_names
# Overwrites file

def write_pipe_delimited_file(filepath, data_list, field_names):
    with open(filepath, 'w', encoding='utf-8') as f:
        for d in data_list:
            line = '|'.join(str(d.get(k, '')) for k in field_names)
            f.write(line + '\n')

# File specific field names
USERS_FIELDS = ['username', 'email', 'fullname']
COURSES_FIELDS = ['course_id', 'title', 'description', 'category', 'level', 'duration', 'status']
ENROLLMENTS_FIELDS = ['enrollment_id', 'username', 'course_id', 'enrollment_date', 'progress', 'status']
ASSIGNMENTS_FIELDS = ['assignment_id', 'course_id', 'title', 'description', 'due_date', 'max_points']
SUBMISSIONS_FIELDS = ['submission_id', 'assignment_id', 'username', 'submission_text', 'submit_date', 'grade', 'feedback']
CERTIFICATES_FIELDS = ['certificate_id', 'username', 'course_id', 'issue_date']

# Data loading functions

def get_all_users():
    return read_pipe_delimited_file(os.path.join(DATA_DIR, 'users.txt'), USERS_FIELDS)

def get_user(username):
    users = get_all_users()
    for u in users:
        if u['username'] == username:
            return u
    return None


def get_all_courses():
    return read_pipe_delimited_file(os.path.join(DATA_DIR, 'courses.txt'), COURSES_FIELDS)

def get_course(course_id):
    courses = get_all_courses()
    course_id_str = str(course_id)
    for c in courses:
        if c['course_id'] == course_id_str:
            return c
    return None


def get_all_enrollments():
    return read_pipe_delimited_file(os.path.join(DATA_DIR, 'enrollments.txt'), ENROLLMENTS_FIELDS)

def get_enrollment(username, course_id):
    enrollments = get_all_enrollments()
    course_id_str = str(course_id)
    for e in enrollments:
        if e['username'] == username and e['course_id'] == course_id_str:
            return e
    return None


def get_all_assignments():
    return read_pipe_delimited_file(os.path.join(DATA_DIR, 'assignments.txt'), ASSIGNMENTS_FIELDS)

def get_assignment(assignment_id):
    assignments = get_all_assignments()
    assignment_id_str = str(assignment_id)
    for a in assignments:
        if a['assignment_id'] == assignment_id_str:
            return a
    return None


def get_all_submissions():
    return read_pipe_delimited_file(os.path.join(DATA_DIR, 'submissions.txt'), SUBMISSIONS_FIELDS)

# Get all submissions by user

def get_user_submissions(username):
    all_subs = get_all_submissions()
    return [s for s in all_subs if s['username'] == username]


def get_all_certificates():
    return read_pipe_delimited_file(os.path.join(DATA_DIR, 'certificates.txt'), CERTIFICATES_FIELDS)

# Get certificates by user

def get_user_certificates(username):
    all_certs = get_all_certificates()
    return [c for c in all_certs if c['username'] == username]

# Helpers for enrollment and certificates

def generate_new_id(existing_items, id_field):
    max_id = 0
    for item in existing_items:
        try:
            val = int(item[id_field])
            if val > max_id:
                max_id = val
        except:
            continue
    return str(max_id + 1)

# Extract lessons for course - no lessons.txt described, so simulate dummy lessons
# We create 5 lessons per course for progress tracking

def get_lessons_for_course(course_id):
    lessons = []
    for i in range(1, 6):
        lessons.append({
            'lesson_id': f'{course_id}-{i}',
            'title': f'Lesson {i}',
            'content': f'Content for lesson {i} of course {course_id}.'
        })
    return lessons

# Calculate progress percent based on lessons completed
# Progress is increments of 20% per completed lesson

def calculate_progress(completed_lessons_count, total_lessons_count=5):
    if total_lessons_count == 0:
        return 0
    return min(100, int((completed_lessons_count / total_lessons_count) * 100))

# Get completed lessons count from enrollment progress (since no lesson completion file)
# We track lesson completion sequentially via progress in increments of 20.

def get_completed_lessons_count_from_progress(progress):
    try:
        progress_int = int(progress)
        return progress_int // 20
    except:
        return 0

# Update enrollment progress

def update_enrollment_progress(username, course_id, new_progress, new_status=None):
    enrollments = get_all_enrollments()
    updated = False
    for e in enrollments:
        if e['username'] == username and e['course_id'] == str(course_id):
            e['progress'] = str(new_progress)
            if new_status:
                e['status'] = new_status
            updated = True
            break
    if updated:
        write_pipe_delimited_file(os.path.join(DATA_DIR, 'enrollments.txt'), enrollments, ENROLLMENTS_FIELDS)

# Append new enrollment

def add_enrollment(username, course_id):
    enrollments = get_all_enrollments()
    new_id = generate_new_id(enrollments, 'enrollment_id')
    today_str = datetime.now().strftime('%Y-%m-%d')
    new_enrollment = {
        'enrollment_id': new_id,
        'username': username,
        'course_id': str(course_id),
        'enrollment_date': today_str,
        'progress': '0',
        'status': 'In Progress'
    }
    enrollments.append(new_enrollment)
    write_pipe_delimited_file(os.path.join(DATA_DIR, 'enrollments.txt'), enrollments, ENROLLMENTS_FIELDS)

# Append certificate

def add_certificate(username, course_id):
    certificates = get_all_certificates()
    new_id = generate_new_id(certificates, 'certificate_id')
    today_str = datetime.now().strftime('%Y-%m-%d')
    new_certificate = {
        'certificate_id': new_id,
        'username': username,
        'course_id': str(course_id),
        'issue_date': today_str
    }
    certificates.append(new_certificate)
    write_pipe_delimited_file(os.path.join(DATA_DIR, 'certificates.txt'), certificates, CERTIFICATES_FIELDS)

# Check if user already has certificate for course

def user_has_certificate(username, course_id):
    certs = get_user_certificates(username)
    for c in certs:
        if c['course_id'] == str(course_id):
            return True
    return False

# Get assignments for user's enrolled courses

def get_user_assignments(username):
    assignments = get_all_assignments()
    enrollments = get_all_enrollments()
    enrolled_course_ids = {e['course_id'] for e in enrollments if e['username'] == username}
    user_assignments = [a for a in assignments if a['course_id'] in enrolled_course_ids]
    return user_assignments

# Get submissions dict keyed by assignment_id for user

def get_user_submissions_dict(username):
    submissions = get_all_submissions()
    user_subs = [s for s in submissions if s['username'] == username]
    sub_dict = {}
    for s in user_subs:
        sub_dict[s['assignment_id']] = s
    return sub_dict

# Append a new submission

def add_submission(assignment_id, username, submission_text):
    submissions = get_all_submissions()
    new_id = generate_new_id(submissions, 'submission_id')
    today_str = datetime.now().strftime('%Y-%m-%d')
    new_submission = {
        'submission_id': new_id,
        'assignment_id': str(assignment_id),
        'username': username,
        'submission_text': submission_text,
        'submit_date': today_str,
        'grade': '',
        'feedback': ''
    }
    submissions.append(new_submission)
    write_pipe_delimited_file(os.path.join(DATA_DIR, 'submissions.txt'), submissions, SUBMISSIONS_FIELDS)

# Update user profile

def update_user_profile(username, email, fullname):
    users = get_all_users()
    updated = False
    for u in users:
        if u['username'] == username:
            u['email'] = email
            u['fullname'] = fullname
            updated = True
            break
    if updated:
        write_pipe_delimited_file(os.path.join(DATA_DIR, 'users.txt'), users, USERS_FIELDS)


# Flask Routes Implementation

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    user = get_user(LOGGED_IN_USERNAME)
    if not user:
        return "User not found", 404
    enrollments = get_all_enrollments()
    courses = get_all_courses()
    # Filter enrollments for current user
    user_enrollments = [e for e in enrollments if e['username'] == LOGGED_IN_USERNAME]

    enrolled_courses = []
    for e in user_enrollments:
        course = next((c for c in courses if c['course_id'] == e['course_id']), None)
        if course:
            enrolled_courses.append({
                'course_id': course['course_id'],
                'title': course['title'],
                'progress': int(e['progress'])
            })
    return render_template('dashboard.html', user_name=user['fullname'], enrolled_courses=enrolled_courses)


@app.route('/catalog')
def course_catalog():
    courses = get_all_courses()
    return render_template('course_catalog.html', courses=courses)


@app.route('/course/<int:course_id>')
def course_details(course_id):
    course = get_course(course_id)
    if not course:
        return "Course not found", 404
    enrollment = get_enrollment(LOGGED_IN_USERNAME, course_id)
    is_enrolled = enrollment is not None
    return render_template('course_details.html', course={
        'course_id': course['course_id'],
        'title': course['title'],
        'description': course['description']
    }, is_enrolled=is_enrolled, enroll_success=None)


@app.route('/course/<int:course_id>/enroll', methods=['POST'])
def enroll_course(course_id):
    course = get_course(course_id)
    if not course:
        return "Course not found", 404
    enrollment = get_enrollment(LOGGED_IN_USERNAME, course_id)
    if enrollment:
        # Already enrolled
        is_enrolled = True
        enroll_success = False
    else:
        add_enrollment(LOGGED_IN_USERNAME, course_id)
        is_enrolled = True
        enroll_success = True

    return render_template('course_details.html', course={
        'course_id': course['course_id'],
        'title': course['title'],
        'description': course['description']
    }, is_enrolled=is_enrolled, enroll_success=enroll_success)


@app.route('/mycourses')
def my_courses():
    enrollments = get_all_enrollments()
    courses = get_all_courses()
    user_enrollments = [e for e in enrollments if e['username'] == LOGGED_IN_USERNAME]

    enrolled_courses = []
    for e in user_enrollments:
        course = next((c for c in courses if c['course_id'] == e['course_id']), None)
        if course:
            enrolled_courses.append({
                'course_id': course['course_id'],
                'title': course['title'],
                'progress': int(e['progress'])
            })
    return render_template('my_courses.html', enrolled_courses=enrolled_courses)


@app.route('/course/<int:course_id>/learn')
def course_learning(course_id):
    course = get_course(course_id)
    if not course:
        return "Course not found", 404
    enrollment = get_enrollment(LOGGED_IN_USERNAME, course_id)
    if not enrollment:
        return redirect(url_for('course_details', course_id=course_id))

    lessons = get_lessons_for_course(course_id)

    # Determine current lesson based on progress
    completed_lessons_count = get_completed_lessons_count_from_progress(enrollment['progress'])
    if completed_lessons_count >= len(lessons):
        current_lesson_index = len(lessons) - 1
    else:
        current_lesson_index = completed_lessons_count

    current_lesson = lessons[current_lesson_index]
    progress = int(enrollment['progress'])
    completion_status = (progress == 100)

    return render_template('course_learning.html',
                           course={'course_id': course['course_id'], 'title': course['title']},
                           lessons=lessons,
                           current_lesson=current_lesson,
                           progress=progress,
                           completion_status=completion_status)


@app.route('/course/<int:course_id>/learn/mark_complete', methods=['POST'])
def mark_lesson_complete(course_id):
    course = get_course(course_id)
    if not course:
        return "Course not found", 404
    enrollment = get_enrollment(LOGGED_IN_USERNAME, course_id)
    if not enrollment:
        return redirect(url_for('course_details', course_id=course_id))

    lessons = get_lessons_for_course(course_id)
    completed_lessons_count = get_completed_lessons_count_from_progress(enrollment['progress'])

    # Mark next lesson as complete if not already completed all
    if completed_lessons_count < len(lessons):
        completed_lessons_count += 1
        new_progress = calculate_progress(completed_lessons_count, len(lessons))
        new_status = 'Completed' if new_progress == 100 else 'In Progress'
        update_enrollment_progress(LOGGED_IN_USERNAME, course_id, new_progress, new_status)

        # Generate certificate on completion if not yet issued
        if new_progress == 100 and not user_has_certificate(LOGGED_IN_USERNAME, course_id):
            add_certificate(LOGGED_IN_USERNAME, course_id)

    # Refresh data for rendering
    enrollment = get_enrollment(LOGGED_IN_USERNAME, course_id)
    lessons = get_lessons_for_course(course_id)
    completed_lessons_count = get_completed_lessons_count_from_progress(enrollment['progress'])
    if completed_lessons_count >= len(lessons):
        current_lesson_index = len(lessons) - 1
    else:
        current_lesson_index = completed_lessons_count
    current_lesson = lessons[current_lesson_index]

    progress = int(enrollment['progress'])
    completion_status = (progress == 100)

    return render_template('course_learning.html',
                           course={'course_id': course['course_id'], 'title': course['title']},
                           lessons=lessons,
                           current_lesson=current_lesson,
                           progress=progress,
                           completion_status=completion_status)


@app.route('/assignments')
def my_assignments():
    assignments = get_user_assignments(LOGGED_IN_USERNAME)
    submissions_dict = get_user_submissions_dict(LOGGED_IN_USERNAME)
    # Prepare submission info keyed by assignment_id
    submissions = {}
    for a in assignments:
        submission = submissions_dict.get(a['assignment_id'])
        if submission:
            submissions[a['assignment_id']] = submission
        else:
            submissions[a['assignment_id']] = None

    return render_template('assignments.html', assignments=assignments, submissions=submissions)


@app.route('/assignment/<int:assignment_id>/submit', methods=['GET'])
def submit_assignment(assignment_id):
    assignment = get_assignment(assignment_id)
    if not assignment:
        return "Assignment not found", 404
    submissions_dict = get_user_submissions_dict(LOGGED_IN_USERNAME)
    submission = submissions_dict.get(str(assignment_id))
    submission_status = (submission is not None)
    return render_template('submit_assignment.html', assignment=assignment, submission_status=submission_status, submission_success=None)


@app.route('/assignment/<int:assignment_id>/submit', methods=['POST'])
def submit_assignment_post(assignment_id):
    assignment = get_assignment(assignment_id)
    if not assignment:
        return "Assignment not found", 404
    submissions_dict = get_user_submissions_dict(LOGGED_IN_USERNAME)
    submission = submissions_dict.get(str(assignment_id))
    submission_status = (submission is not None)
    if submission_status:
        # Already submitted
        return render_template('submit_assignment.html', assignment=assignment, submission_status=True, submission_success=False)

    submission_text = request.form.get('submission_text', '').strip()
    if not submission_text:
        return render_template('submit_assignment.html', assignment=assignment, submission_status=False, submission_success=False)

    add_submission(assignment_id, LOGGED_IN_USERNAME, submission_text)
    return render_template('submit_assignment.html', assignment=assignment, submission_status=True, submission_success=True)


@app.route('/certificates')
def certificates_page():
    certs = get_user_certificates(LOGGED_IN_USERNAME)
    courses = get_all_courses()

    certificates = []
    for c in certs:
        course = next((co for co in courses if co['course_id'] == c['course_id']), None)
        course_title = course['title'] if course else 'Unknown Course'
        certificates.append({
            'certificate_id': c['certificate_id'],
            'course_title': course_title,
            'issue_date': c['issue_date']
        })
    return render_template('certificates.html', certificates=certificates)


@app.route('/profile')
def user_profile():
    user = get_user(LOGGED_IN_USERNAME)
    if not user:
        return "User not found", 404
    return render_template('profile.html', user_profile=user, update_success=None)


@app.route('/profile/update', methods=['POST'])
def update_profile():
    email = request.form.get('email', '').strip()
    fullname = request.form.get('fullname', '').strip()

    if not email or not fullname:
        user = get_user(LOGGED_IN_USERNAME)
        return render_template('profile.html', user_profile=user, update_success=False)

    update_user_profile(LOGGED_IN_USERNAME, email, fullname)
    user = get_user(LOGGED_IN_USERNAME)  # Reload updated user data
    return render_template('profile.html', user_profile=user, update_success=True)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
