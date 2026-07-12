from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# ------------------------------
# Helper functions to read/write pipe-delimited files
# ------------------------------

def read_users():
    users_file = os.path.join(DATA_DIR, 'users.txt')
    users = {}
    if os.path.exists(users_file):
        with open(users_file, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line: continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                username, email, fullname = parts
                users[username] = {'username': username, 'email': email, 'fullname': fullname}
    return users


def write_users(users):
    users_file = os.path.join(DATA_DIR, 'users.txt')
    with open(users_file, 'w', encoding='utf-8') as f:
        for user in users.values():
            f.write(f"{user['username']}|{user['email']}|{user['fullname']}\n")


def read_courses():
    courses_file = os.path.join(DATA_DIR, 'courses.txt')
    courses = {}
    if os.path.exists(courses_file):
        with open(courses_file, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line: continue
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
    courses_file = os.path.join(DATA_DIR, 'courses.txt')
    with open(courses_file, 'w', encoding='utf-8') as f:
        for course in courses.values():
            f.write(f"{course['course_id']}|{course['title']}|{course['description']}|{course['category']}|{course['level']}|{course['duration']}|{course['status']}\n")


def read_enrollments():
    enroll_file = os.path.join(DATA_DIR, 'enrollments.txt')
    enrollments = {}
    # enrollment_id|username|course_id|enrollment_date|progress|status
    if os.path.exists(enroll_file):
        with open(enroll_file, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line: continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                enrollment_id, username, course_id, enrollment_date, progress, status = parts
                enrollments[enrollment_id] = {
                    'enrollment_id': enrollment_id,
                    'username': username,
                    'course_id': course_id,
                    'enrollment_date': enrollment_date,
                    'progress': int(progress),
                    'status': status
                }
    return enrollments


def write_enrollments(enrollments):
    enroll_file = os.path.join(DATA_DIR, 'enrollments.txt')
    with open(enroll_file, 'w', encoding='utf-8') as f:
        for enroll in enrollments.values():
            f.write(f"{enroll['enrollment_id']}|{enroll['username']}|{enroll['course_id']}|{enroll['enrollment_date']}|{enroll['progress']}|{enroll['status']}\n")


def read_assignments():
    assignments_file = os.path.join(DATA_DIR, 'assignments.txt')
    assignments = {}
    # assignment_id|course_id|title|description|due_date|max_points
    if os.path.exists(assignments_file):
        with open(assignments_file, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line: continue
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
                    'max_points': max_points
                }
    return assignments


def write_assignments(assignments):
    assignments_file = os.path.join(DATA_DIR, 'assignments.txt')
    with open(assignments_file, 'w', encoding='utf-8') as f:
        for a in assignments.values():
            f.write(f"{a['assignment_id']}|{a['course_id']}|{a['title']}|{a['description']}|{a['due_date']}|{a['max_points']}\n")


def read_submissions():
    submissions_file = os.path.join(DATA_DIR, 'submissions.txt')
    submissions = {}
    # submission_id|assignment_id|username|submission_text|submit_date|grade|feedback
    if os.path.exists(submissions_file):
        with open(submissions_file, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line: continue
                parts = line.split('|')
                if len(parts) !=7:
                    continue
                submission_id, assignment_id, username, submission_text, submit_date, grade, feedback = parts
                submissions[submission_id] = {
                    'submission_id': submission_id,
                    'assignment_id': assignment_id,
                    'username': username,
                    'submission_text': submission_text,
                    'submit_date': submit_date,
                    'grade': grade,
                    'feedback': feedback
                }
    return submissions


def write_submissions(submissions):
    submissions_file = os.path.join(DATA_DIR, 'submissions.txt')
    with open(submissions_file, 'w', encoding='utf-8') as f:
        for s in submissions.values():
            f.write(f"{s['submission_id']}|{s['assignment_id']}|{s['username']}|{s['submission_text']}|{s['submit_date']}|{s['grade']}|{s['feedback']}\n")


def read_certificates():
    certificates_file = os.path.join(DATA_DIR, 'certificates.txt')
    certificates = {}
    # certificate_id|username|course_id|issue_date
    if os.path.exists(certificates_file):
        with open(certificates_file, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line: continue
                parts = line.split('|')
                if len(parts) != 4:
                    continue
                certificate_id, username, course_id, issue_date = parts
                certificates[certificate_id] = {
                    'certificate_id': certificate_id,
                    'username': username,
                    'course_id': course_id,
                    'issue_date': issue_date
                }
    return certificates


def write_certificates(certificates):
    certificates_file = os.path.join(DATA_DIR, 'certificates.txt')
    with open(certificates_file, 'w', encoding='utf-8') as f:
        for c in certificates.values():
            f.write(f"{c['certificate_id']}|{c['username']}|{c['course_id']}|{c['issue_date']}\n")


# Helper to get next id for given dict keyed by id string
def get_next_id(data_dict):
    if not data_dict:
        return '1'
    else:
        max_id = max(int(k) for k in data_dict.keys())
        return str(max_id + 1)


# Helper function to get enrolled courses for username with progress info
# returns list of dicts with course info plus progress

def get_enrolled_courses_for_user(username):
    enrollments = read_enrollments()
    courses = read_courses()

    enrolled = []
    for enroll in enrollments.values():
        if enroll['username'] == username:
            course = courses.get(enroll['course_id'])
            if course:
                enrolled.append({
                    'course_id': course['course_id'],
                    'title': course['title'],
                    'progress': enroll['progress']
                })
    return enrolled


# Helper function to check if user enrolled in a course
# returns enrollment_id or None

def get_enrollment_id(username, course_id):
    enrollments = read_enrollments()
    for enroll in enrollments.values():
        if enroll['username'] == username and enroll['course_id'] == course_id:
            return enroll['enrollment_id']
    return None


# Helper to get enrollment record by enrollment_id

def get_enrollment_by_id(enrollment_id):
    enrollments = read_enrollments()
    return enrollments.get(enrollment_id)


# Helper to update enrollment progress and status

def update_enrollment_progress(enrollment_id, progress):
    enrollments = read_enrollments()
    enrollment = enrollments.get(enrollment_id)
    if enrollment:
        enrollment['progress'] = progress
        enrollment['status'] = 'Completed' if progress == 100 else 'In Progress'
        write_enrollments(enrollments)


# Helper to check if user already has certificate for a course

def has_certificate(username, course_id):
    certificates = read_certificates()
    for cert in certificates.values():
        if cert['username'] == username and cert['course_id'] == course_id:
            return True
    return False

# Helper to add certificate

def add_certificate(username, course_id):
    certificates = read_certificates()
    certificate_id = get_next_id(certificates)
    issue_date = datetime.now().strftime('%Y-%m-%d')
    certificates[certificate_id] = {
        'certificate_id': certificate_id,
        'username': username,
        'course_id': course_id,
        'issue_date': issue_date
    }
    write_certificates(certificates)


# Helper to get lessons for a course
# Not described in design spec Section 3, so we assume lessons data is inside course details or somewhere static.
# For completeness, we create some dummy lessons we can reuse.
# We'll assume 5 lessons for each course with ids 1-5.

def get_lessons_for_course(course_id):
    lessons = []
    for i in range(1, 6):
        lessons.append({
            'lesson_id': str(i),
            'title': f'Lesson {i}',
            'content': f'Content for lesson {i} of course {course_id}.'
        })
    return lessons


# Helper to get progress and determine current lesson
# progress in % increments of 20 for each lesson (5 lessons)
# so 0% means no lessons done, current lesson is lesson 1
# progress 20% means lesson 1 done, current lesson is lesson 2
# progress 100% means all lessons done, no current lesson

def get_current_lesson_and_is_completed(progress):
    if progress >= 100:
        return None, True
    # Determine current lesson index
    completed_lessons = progress // 20
    current_lesson_index = completed_lessons + 1
    if current_lesson_index > 5:
        current_lesson_index = 5
    # Lesson ids are strings 1-5
    current_lesson = {'lesson_id': str(current_lesson_index), 'title': f'Lesson {current_lesson_index}', 'content': f'Content for lesson {current_lesson_index} of course.'}
    return current_lesson, False


# Helper to get user submissions by username

def get_user_submissions(username):
    submissions = read_submissions()
    return [s for s in submissions.values() if s['username'] == username]


# Helper to get submissions by assignment_id and username

def get_submission_by_assignment_and_user(assignment_id, username):
    submissions = read_submissions()
    for s in submissions.values():
        if s['assignment_id'] == assignment_id and s['username'] == username:
            return s
    return None


# Helper to add submission

def add_submission(assignment_id, username, submission_text):
    submissions = read_submissions()
    submission_id = get_next_id(submissions)
    submit_date = datetime.now().strftime('%Y-%m-%d')
    # grade and feedback empty initially
    submissions[submission_id] = {
        'submission_id': submission_id,
        'assignment_id': assignment_id,
        'username': username,
        'submission_text': submission_text,
        'submit_date': submit_date,
        'grade': '',
        'feedback': ''
    }
    write_submissions(submissions)


# Helper to get assignments enriched with submission status for a user

def get_assignments_for_user(username):
    assignments = read_assignments()
    submissions = read_submissions()
    # create a dict for quick lookup of submissions per assignment
    submission_lookup = {}
    for sub in submissions.values():
        if sub['username'] == username:
            submission_lookup[sub['assignment_id']] = sub

    assignments_list = []
    for a in assignments.values():
        status = 'Not Submitted'
        if a['assignment_id'] in submission_lookup:
            status = 'Submitted'
        assignments_list.append({
            'assignment_id': a['assignment_id'],
            'course_id': a['course_id'],
            'title': a['title'],
            'description': a['description'],
            'due_date': a['due_date'],
            'max_points': a['max_points'],
            'submission_status': status
        })
    return assignments_list


# For this implementation, we assume a fixed logged-in username for simplicity
# Since design_spec does not specify authentication, we choose 'john' for all routes
# This username should be consistent across all route handlers
LOGGED_IN_USERNAME = 'john'


# ------------------------------
# Flask Routes Implementation
# ------------------------------

@app.route('/')
def root():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    users = read_users()
    user = users.get(LOGGED_IN_USERNAME)
    if not user:
        # Redirect to catalog if user not found
        return redirect(url_for('course_catalog'))

    enrolled_courses = get_enrolled_courses_for_user(LOGGED_IN_USERNAME)
    fullname = user['fullname']
    return render_template('dashboard.html', username=LOGGED_IN_USERNAME, fullname=fullname, enrolled_courses=enrolled_courses)


@app.route('/catalog')
def course_catalog():
    courses = read_courses()
    courses_list = list(courses.values())
    return render_template('catalog.html', courses=courses_list)


@app.route('/course/<course_id>')
def course_details(course_id):
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        return redirect(url_for('course_catalog'))

    enrollments = read_enrollments()
    is_enrolled = any(e['username'] == LOGGED_IN_USERNAME and e['course_id'] == course_id for e in enrollments.values())

    return render_template('course_details.html', course_id=course_id, course=course, is_enrolled=is_enrolled)


@app.route('/course/<course_id>/enroll', methods=['POST'])
def enroll_course(course_id):
    courses = read_courses()
    course = courses.get(course_id)
    if not course or course['status'].lower() != 'active':
        # Course not active or not exist
        error_message = 'Course not available for enrollment.'
        return render_template('course_details.html', course_id=course_id, course=course, enrollment_success=False, is_enrolled=False, error_message=error_message)

    enrollments = read_enrollments()
    # Check if already enrolled
    for e in enrollments.values():
        if e['username'] == LOGGED_IN_USERNAME and e['course_id'] == course_id:
            # Already enrolled
            return render_template('course_details.html', course_id=course_id, course=course, enrollment_success=False, is_enrolled=True, error_message='Already enrolled in this course.')

    enrollment_id = get_next_id(enrollments)
    enrollment_date = datetime.now().strftime('%Y-%m-%d')
    new_enrollment = {
        'enrollment_id': enrollment_id,
        'username': LOGGED_IN_USERNAME,
        'course_id': course_id,
        'enrollment_date': enrollment_date,
        'progress': 0,
        'status': 'In Progress'
    }
    enrollments[enrollment_id] = new_enrollment
    write_enrollments(enrollments)

    return render_template('course_details.html', course_id=course_id, course=course, enrollment_success=True, is_enrolled=True)


@app.route('/my_courses')
def my_courses_page():
    users = read_users()
    user = users.get(LOGGED_IN_USERNAME)
    if not user:
        return redirect(url_for('dashboard_page'))

    enrolled_courses = get_enrolled_courses_for_user(LOGGED_IN_USERNAME)
    return render_template('my_courses.html', username=LOGGED_IN_USERNAME, enrolled_courses=enrolled_courses)


@app.route('/course/<course_id>/learn')
def course_learning(course_id):
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        return redirect(url_for('my_courses_page'))

    enrollments = read_enrollments()
    enrollment = None
    for e in enrollments.values():
        if e['username'] == LOGGED_IN_USERNAME and e['course_id'] == course_id:
            enrollment = e
            break
    if not enrollment:
        return redirect(url_for('course_details', course_id=course_id))

    progress = enrollment['progress']
    lessons = get_lessons_for_course(course_id)
    current_lesson, is_completed = get_current_lesson_and_is_completed(progress)

    # If current_lesson is None but not completed, fallback to lesson 1
    if current_lesson is None and not is_completed:
        current_lesson = lessons[0] if lessons else None

    return render_template('course_learning.html', course_id=course_id, lessons=lessons, current_lesson=current_lesson, progress=progress, is_completed=is_completed)


@app.route('/course/<course_id>/learn/mark_complete', methods=['POST'])
def mark_lesson_complete(course_id):
    enrollments = read_enrollments()
    enrollment = None
    for e in enrollments.values():
        if e['username'] == LOGGED_IN_USERNAME and e['course_id'] == course_id:
            enrollment = e
            break
    if not enrollment:
        return redirect(url_for('course_details', course_id=course_id))

    progress = enrollment['progress']
    if progress < 100:
        # Increase progress by 20 (one lesson)
        new_progress = progress + 20
        if new_progress > 100:
            new_progress = 100
        enrollment['progress'] = new_progress
        enrollment['status'] = 'Completed' if new_progress == 100 else 'In Progress'

        write_enrollments(enrollments)

        # If course just completed, generate certificate
        if new_progress == 100 and not has_certificate(LOGGED_IN_USERNAME, course_id):
            add_certificate(LOGGED_IN_USERNAME, course_id)

    lessons = get_lessons_for_course(course_id)
    current_lesson, is_completed = get_current_lesson_and_is_completed(enrollment['progress'])

    return render_template('course_learning.html', course_id=course_id, lessons=lessons, current_lesson=current_lesson, progress=enrollment['progress'], is_completed=is_completed)


@app.route('/assignments')
def my_assignments():
    assignments = get_assignments_for_user(LOGGED_IN_USERNAME)
    return render_template('assignments.html', assignments=assignments)


@app.route('/assignment/<assignment_id>/submit', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    assignments = read_assignments()
    assignment = assignments.get(assignment_id)
    if not assignment:
        return redirect(url_for('my_assignments'))

    submission = get_submission_by_assignment_and_user(assignment_id, LOGGED_IN_USERNAME)
    submission_status = 'Submitted' if submission else 'Not Submitted'

    if request.method == 'GET':
        return render_template('submit_assignment.html', assignment=assignment, submission_status=submission_status)

    # POST - handle submission
    submission_text = request.form.get('submission_text', '').strip()

    if not submission_text:
        error_message = 'Submission text cannot be empty.'
        return render_template('submit_assignment.html', assignment=assignment, submission_status=submission_status, submission_success=False, error_message=error_message)

    if submission:
        # Overwrite previous submission
        submissions = read_submissions()
        submissions[submission['submission_id']]['submission_text'] = submission_text
        submissions[submission['submission_id']]['submit_date'] = datetime.now().strftime('%Y-%m-%d')
        submissions[submission['submission_id']]['grade'] = ''
        submissions[submission['submission_id']]['feedback'] = ''
        write_submissions(submissions)
    else:
        add_submission(assignment_id, LOGGED_IN_USERNAME, submission_text)

    # Update submission status
    submission_status = 'Submitted'

    return render_template('submit_assignment.html', assignment=assignment, submission_status=submission_status, submission_success=True)


@app.route('/certificates')
def certificates_page():
    certificates_all = read_certificates()
    user_certs = [c for c in certificates_all.values() if c['username'] == LOGGED_IN_USERNAME]
    return render_template('certificates.html', certificates=user_certs, username=LOGGED_IN_USERNAME)


@app.route('/profile')
def user_profile_page():
    users = read_users()
    user = users.get(LOGGED_IN_USERNAME)
    if not user:
        return redirect(url_for('dashboard_page'))

    return render_template('profile.html', username=LOGGED_IN_USERNAME, email=user['email'], fullname=user['fullname'])


@app.route('/profile/update', methods=['POST'])
def update_profile():
    users = read_users()
    user = users.get(LOGGED_IN_USERNAME)
    if not user:
        return redirect(url_for('dashboard_page'))

    fullname = request.form.get('fullname', '').strip()
    email = request.form.get('email', '').strip()

    if not fullname or not email:
        error_message = 'Full name and email cannot be empty.'
        return render_template('profile.html', username=LOGGED_IN_USERNAME, email=user['email'], fullname=user['fullname'], update_success=False, error_message=error_message)

    # Update user info
    user['fullname'] = fullname
    user['email'] = email
    users[LOGGED_IN_USERNAME] = user
    write_users(users)

    return render_template('profile.html', username=LOGGED_IN_USERNAME, email=email, fullname=fullname, update_success=True)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
