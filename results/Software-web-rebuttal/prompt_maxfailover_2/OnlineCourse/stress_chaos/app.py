from flask import Flask, render_template, request, redirect, url_for, session, abort
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'online_course_secret_key'

DATA_DIR = 'data'

# File paths
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
COURSES_FILE = os.path.join(DATA_DIR, 'courses.txt')
ENROLLMENTS_FILE = os.path.join(DATA_DIR, 'enrollments.txt')
ASSIGNMENTS_FILE = os.path.join(DATA_DIR, 'assignments.txt')
SUBMISSIONS_FILE = os.path.join(DATA_DIR, 'submissions.txt')
CERTIFICATES_FILE = os.path.join(DATA_DIR, 'certificates.txt')

# --------------------------------------------------
# Utility functions for reading and writing pipe-delimited files
# --------------------------------------------------
def read_pipe_delimited_file(filename):
    '''Reads file and returns list of lists of fields'''
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    fields = line.split('|')
                    data.append(fields)
    except FileNotFoundError:
        # File doesn't exist, return empty
        pass
    return data

def write_pipe_delimited_file(filename, data):
    '''Writes list of lists of fields into file'''
    with open(filename, 'w', encoding='utf-8') as f:
        for record in data:
            f.write('|'.join(str(field) for field in record) + '\n')

# --------------------------------------------------
# Users
# fields: username|email|fullname
# --------------------------------------------------
def load_users():
    raw = read_pipe_delimited_file(USERS_FILE)
    users = []
    for fields in raw:
        if len(fields) == 3:
            user = {
                'username': fields[0],
                'email': fields[1],
                'fullname': fields[2]
            }
            users.append(user)
    return users

def get_user(username):
    for user in load_users():
        if user['username'] == username:
            return user
    return None

def update_user(username, email, fullname):
    users = load_users()
    updated = False
    for user in users:
        if user['username'] == username:
            user['email'] = email
            user['fullname'] = fullname
            updated = True
            break
    if updated:
        # Rewrite file
        records = [[u['username'], u['email'], u['fullname']] for u in users]
        write_pipe_delimited_file(USERS_FILE, records)
    return updated

# --------------------------------------------------
# Courses
# fields: course_id|title|description|category|level|duration|status
# --------------------------------------------------
def load_courses():
    raw = read_pipe_delimited_file(COURSES_FILE)
    courses = []
    for fields in raw:
        if len(fields) == 7:
            course = {
                'course_id': fields[0],
                'title': fields[1],
                'description': fields[2],
                'category': fields[3],
                'level': fields[4],
                'duration': fields[5],
                'status': fields[6]
            }
            courses.append(course)
    return courses

def get_course(course_id):
    for course in load_courses():
        if course['course_id'] == course_id:
            return course
    return None

# --------------------------------------------------
# Enrollments
# fields: enrollment_id|username|course_id|enrollment_date|progress|status
# --------------------------------------------------
def load_enrollments():
    raw = read_pipe_delimited_file(ENROLLMENTS_FILE)
    enrollments = []
    for fields in raw:
        if len(fields) == 6:
            enrollment = {
                'enrollment_id': fields[0],
                'username': fields[1],
                'course_id': fields[2],
                'enrollment_date': fields[3],
                'progress': int(fields[4]),
                'status': fields[5]
            }
            enrollments.append(enrollment)
    return enrollments

def get_enrollment(username, course_id):
    for enrollment in load_enrollments():
        if enrollment['username'] == username and enrollment['course_id'] == course_id:
            return enrollment
    return None

def get_user_enrollments(username):
    return [e for e in load_enrollments() if e['username'] == username]

def write_enrollments(enrollments):
    records = []
    for e in enrollments:
        record = [e['enrollment_id'], e['username'], e['course_id'], e['enrollment_date'], str(e['progress']), e['status']]
        records.append(record)
    write_pipe_delimited_file(ENROLLMENTS_FILE, records)

def add_enrollment(username, course_id):
    enrollments = load_enrollments()
    # Find max enrollment_id and increment
    max_id = 0
    for e in enrollments:
        try:
            int_id = int(e['enrollment_id'])
            if int_id > max_id:
                max_id = int_id
        except:
            pass
    new_id = str(max_id + 1)
    today = datetime.utcnow().strftime('%Y-%m-%d')
    new_enrollment = {
        'enrollment_id': new_id,
        'username': username,
        'course_id': course_id,
        'enrollment_date': today,
        'progress': 0,
        'status': 'In Progress'
    }
    enrollments.append(new_enrollment)
    write_enrollments(enrollments)
    return new_enrollment

def update_enrollment_progress(username, course_id, new_progress):
    enrollments = load_enrollments()
    updated = False
    for e in enrollments:
        if e['username'] == username and e['course_id'] == course_id:
            e['progress'] = new_progress
            if new_progress >= 100:
                e['progress'] = 100
                e['status'] = 'Completed'
            else:
                e['status'] = 'In Progress'
            updated = True
            break
    if updated:
        write_enrollments(enrollments)
    return updated

# --------------------------------------------------
# Assignments
# fields: assignment_id|course_id|title|description|due_date|max_points
# --------------------------------------------------
def load_assignments():
    raw = read_pipe_delimited_file(ASSIGNMENTS_FILE)
    assignments = []
    for fields in raw:
        if len(fields) == 6:
            assignment = {
                'assignment_id': fields[0],
                'course_id': fields[1],
                'title': fields[2],
                'description': fields[3],
                'due_date': fields[4],
                'max_points': int(fields[5])
            }
            assignments.append(assignment)
    return assignments

def get_assignment(assignment_id):
    for a in load_assignments():
        if a['assignment_id'] == assignment_id:
            return a
    return None

# --------------------------------------------------
# Submissions
# fields: submission_id|assignment_id|username|submission_text|submit_date|grade|feedback
# --------------------------------------------------
def load_submissions():
    raw = read_pipe_delimited_file(SUBMISSIONS_FILE)
    submissions = []
    for fields in raw:
        if len(fields) == 7:
            grade = fields[5]
            try:
                grade = int(grade)
            except:
                grade = None
            submission = {
                'submission_id': fields[0],
                'assignment_id': fields[1],
                'username': fields[2],
                'submission_text': fields[3],
                'submit_date': fields[4],
                'grade': grade,
                'feedback': fields[6]
            }
            submissions.append(submission)
    return submissions

def write_submissions(submissions):
    records = []
    for s in submissions:
        grade_str = str(s['grade']) if s['grade'] is not None else ''
        record = [s['submission_id'], s['assignment_id'], s['username'], s['submission_text'], s['submit_date'], grade_str, s['feedback']]
        records.append(record)
    write_pipe_delimited_file(SUBMISSIONS_FILE, records)

def add_submission(assignment_id, username, submission_text):
    submissions = load_submissions()
    max_id = 0
    for s in submissions:
        try:
            int_id = int(s['submission_id'])
            if int_id > max_id:
                max_id = int_id
        except:
            pass
    new_id = str(max_id + 1)
    today = datetime.utcnow().strftime('%Y-%m-%d')
    new_submission = {
        'submission_id': new_id,
        'assignment_id': assignment_id,
        'username': username,
        'submission_text': submission_text,
        'submit_date': today,
        'grade': None,
        'feedback': ''
    }
    submissions.append(new_submission)
    write_submissions(submissions)
    return new_submission

# --------------------------------------------------
# Certificates
# fields: certificate_id|username|course_id|issue_date
# --------------------------------------------------
def load_certificates():
    raw = read_pipe_delimited_file(CERTIFICATES_FILE)
    certificates = []
    for fields in raw:
        if len(fields) == 4:
            certificate = {
                'certificate_id': fields[0],
                'username': fields[1],
                'course_id': fields[2],
                'issue_date': fields[3],
            }
            certificates.append(certificate)
    return certificates

def write_certificates(certificates):
    records = []
    for c in certificates:
        record = [c['certificate_id'], c['username'], c['course_id'], c['issue_date']]
        records.append(record)
    write_pipe_delimited_file(CERTIFICATES_FILE, records)

def add_certificate(username, course_id):
    certificates = load_certificates()
    max_id = 0
    for c in certificates:
        try:
            int_id = int(c['certificate_id'])
            if int_id > max_id:
                max_id = int_id
        except:
            pass
    new_id = str(max_id + 1)
    today = datetime.utcnow().strftime('%Y-%m-%d')
    new_certificate = {
        'certificate_id': new_id,
        'username': username,
        'course_id': course_id,
        'issue_date': today
    }
    certificates.append(new_certificate)
    write_certificates(certificates)
    return new_certificate

def certificate_exists(username, course_id):
    for c in load_certificates():
        if c['username'] == username and c['course_id'] == course_id:
            return True
    return False

# --------------------------------------------------
# For lessons data - Not specified in files, but needed for /my-courses/<course_id>/learn and marking lessons complete
# We assume lessons are stored per course in 'data/lessons_<course_id>.txt' with fields: lesson_id|title|content
# --------------------------------------------------
def load_lessons(course_id):
    filename = os.path.join(DATA_DIR, f'lessons_{course_id}.txt')
    raw = read_pipe_delimited_file(filename)
    lessons = []
    for fields in raw:
        if len(fields) == 3:
            lesson = {
                'lesson_id': fields[0],
                'title': fields[1],
                'content': fields[2]
            }
            lessons.append(lesson)
    # Sort by lesson_id assuming numeric or lexicographically sorted
    lessons.sort(key=lambda l: l['lesson_id'])
    return lessons

# --------------------------------------------------
# Helper for progress calculation based on lessons
# progress = floor((completed_lessons / total_lessons) * 100)
# --------------------------------------------------
import math
def calculate_progress(completed_lessons_count, total_lessons_count):
    if total_lessons_count == 0:
        return 100
    progress = math.floor((completed_lessons_count / total_lessons_count) * 100)
    if progress > 100:
        progress = 100
    return progress

# --------------------------------------------------
# For tracking completed lessons per enrollment
# We store completed lessons as a pipe-delimited list in a separate file per enrollment
# File format: data/completion_<enrollment_id>.txt with one line containing lesson_ids pipe delimited
# --------------------------------------------------
def get_completed_lessons(enrollment_id):
    filename = os.path.join(DATA_DIR, f'completion_{enrollment_id}.txt')
    lessons = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            line = f.readline().strip()
            if line:
                lessons = line.split('|')
    except FileNotFoundError:
        pass
    return lessons

def save_completed_lessons(enrollment_id, lessons):
    filename = os.path.join(DATA_DIR, f'completion_{enrollment_id}.txt')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('|'.join(lessons))

# --------------------------------------------------
# Getting current logged in user (simulate session)
# Since authentication is not described, we'll use a simple query param 'user' for demo
# --------------------------------------------------
def get_current_username():
    # Try to get from query parameters for simulation
    username = request.args.get('user', None)
    if username:
        if get_user(username):
            return username
    # Also check session
    if 'username' in session:
        return session['username']
    # For simplicity, just pick the first user if none provided
    users = load_users()
    if len(users) > 0:
        return users[0]['username']
    return None

# --------------------------------------------------
# Route Implementations
# --------------------------------------------------

@app.route('/')
def root():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    username = get_current_username()
    if not username:
        abort(403)
    user = get_user(username)
    enrollments = get_user_enrollments(username)
    enrolled_courses = []
    for enrollment in enrollments:
        course = get_course(enrollment['course_id'])
        if course:
            enrolled_courses.append({
                'course_id': course['course_id'],
                'title': course['title'],
                'progress': enrollment['progress']
            })
    return render_template('dashboard.html', username=username, fullname=user['fullname'], enrolled_courses=enrolled_courses)

@app.route('/catalog', methods=['GET'])
def course_catalog():
    courses = load_courses()
    return render_template('catalog.html', courses=courses)

@app.route('/catalog/search', methods=['POST'])
def course_catalog_search():
    search_term = request.form.get('search', '').strip().lower()
    courses = load_courses()
    if search_term:
        filtered_courses = []
        for c in courses:
            if (search_term in c['title'].lower() or
                search_term in c['description'].lower() or
                search_term in c['category'].lower() or
                search_term in c['level'].lower()):
                filtered_courses.append(c)
        courses = filtered_courses
    return render_template('catalog.html', courses=courses)

@app.route('/course/<course_id>', methods=['GET'])
def course_details(course_id):
    username = get_current_username()
    course = get_course(course_id)
    if course is None:
        abort(404)
    is_enrolled = False
    if username:
        enrollment = get_enrollment(username, course_id)
        is_enrolled = enrollment is not None
    return render_template('course_details.html', course=course, is_enrolled=is_enrolled)

@app.route('/course/<course_id>/enroll', methods=['POST'])
def enroll_course(course_id):
    username = get_current_username()
    if not username:
        abort(403)
    course = get_course(course_id)
    if not course:
        abort(404)
    enrollment = get_enrollment(username, course_id)
    if enrollment:
        # Already enrolled
        return render_template('course_details.html', course=course, is_enrolled=True, error_message='You are already enrolled in this course.')
    # Add new enrollment
    new_enrollment = add_enrollment(username, course_id)
    success_message = 'Enrollment successful!'
    return render_template('course_details.html', course=course, is_enrolled=True, success_message=success_message)

@app.route('/my-courses')
def my_courses():
    username = get_current_username()
    if not username:
        abort(403)
    enrollments = get_user_enrollments(username)
    enrolled_courses = []
    for enrollment in enrollments:
        course = get_course(enrollment['course_id'])
        if course:
            enrolled_courses.append({
                'course_id': course['course_id'],
                'title': course['title'],
                'progress': enrollment['progress']
            })
    return render_template('my_courses.html', enrolled_courses=enrolled_courses)

@app.route('/my-courses/<course_id>/learn', methods=['GET'])
def course_learning(course_id):
    username = get_current_username()
    if not username:
        abort(403)
    course = get_course(course_id)
    if course is None:
        abort(404)
    enrollment = get_enrollment(username, course_id)
    if not enrollment:
        # Not enrolled
        abort(403)
    lessons = load_lessons(course_id)
    if not lessons:
        # No lessons
        abort(404)
    enrollment_id = enrollment['enrollment_id']
    completed_lessons = get_completed_lessons(enrollment_id)
    # Determine current lesson (next incomplete)
    current_lesson = None
    for lesson in lessons:
        if lesson['lesson_id'] not in completed_lessons:
            current_lesson = lesson
            break
    if current_lesson is None and lessons:
        # All lessons complete, show last lesson
        current_lesson = lessons[-1]
    return render_template('course_learning.html', course=course, lessons=lessons, current_lesson=current_lesson, progress=enrollment['progress'])

@app.route('/my-courses/<course_id>/mark-complete', methods=['POST'])
def mark_lesson_complete(course_id):
    username = get_current_username()
    if not username:
        abort(403)
    course = get_course(course_id)
    if course is None:
        abort(404)
    enrollment = get_enrollment(username, course_id)
    if not enrollment:
        abort(403)
    enrollment_id = enrollment['enrollment_id']
    lessons = load_lessons(course_id)
    if not lessons:
        abort(404)
    completed_lessons = get_completed_lessons(enrollment_id)
    # Find current lesson incomplete
    current_lesson = None
    for lesson in lessons:
        if lesson['lesson_id'] not in completed_lessons:
            current_lesson = lesson
            break
    if current_lesson is None:
        # All lessons already complete
        return render_template('course_learning.html', course=course, lessons=lessons, current_lesson=lessons[-1], progress=enrollment['progress'], error_message='All lessons are already completed.')
    # Mark current lesson as complete
    completed_lessons.append(current_lesson['lesson_id'])
    save_completed_lessons(enrollment_id, completed_lessons)
    # Update progress
    total_lessons = len(lessons)
    completed_count = len(completed_lessons)
    new_progress = calculate_progress(completed_count, total_lessons)
    update_enrollment_progress(username, course_id, new_progress)
    enrollment = get_enrollment(username, course_id)  # reload updated
    # Check for certificate generation if progress==100
    if enrollment['progress'] == 100:
        if not certificate_exists(username, course_id):
            add_certificate(username, course_id)
    success_message = 'Lesson marked as complete.'
    current_lesson = None
    for lesson in lessons:
        if lesson['lesson_id'] not in completed_lessons:
            current_lesson = lesson
            break
    if current_lesson is None and lessons:
        current_lesson = lessons[-1]
    return render_template('course_learning.html', course=course, lessons=lessons, current_lesson=current_lesson, progress=enrollment['progress'], success_message=success_message)

@app.route('/assignments', methods=['GET'])
def my_assignments():
    username = get_current_username()
    if not username:
        abort(403)
    # Show assignments for courses user is enrolled in
    enrollments = get_user_enrollments(username)
    enrolled_course_ids = set(e['course_id'] for e in enrollments)
    assignments = load_assignments()
    filtered_assignments = [a for a in assignments if a['course_id'] in enrolled_course_ids]
    return render_template('assignments.html', assignments=filtered_assignments)

@app.route('/assignments/<assignment_id>/submit', methods=['GET'])
def submit_assignment_form(assignment_id):
    username = get_current_username()
    if not username:
        abort(403)
    assignment = get_assignment(assignment_id)
    if assignment is None:
        abort(404)
    return render_template('submit_assignment.html', assignment=assignment)

@app.route('/assignments/<assignment_id>/submit', methods=['POST'])
def submit_assignment(assignment_id):
    username = get_current_username()
    if not username:
        abort(403)
    assignment = get_assignment(assignment_id)
    if assignment is None:
        abort(404)
    submission_text = request.form.get('submission_text', '').strip()
    if not submission_text:
        error_message = 'Submission text cannot be empty.'
        return render_template('submit_assignment.html', assignment=assignment, error_message=error_message)
    # Add new submission
    add_submission(assignment_id, username, submission_text)
    success_message = 'Assignment submitted successfully.'
    return render_template('submit_assignment.html', assignment=assignment, success_message=success_message)

@app.route('/certificates', methods=['GET'])
def certificates():
    username = get_current_username()
    if not username:
        abort(403)
    certs = load_certificates()
    user_certs = [c for c in certs if c['username'] == username]
    # Attach course_title for context
    for c in user_certs:
        course = get_course(c['course_id'])
        c['course_title'] = course['title'] if course else 'Unknown'
    return render_template('certificates.html', certificates=user_certs)

@app.route('/profile', methods=['GET'])
def user_profile():
    username = get_current_username()
    if not username:
        abort(403)
    user = get_user(username)
    if user is None:
        abort(404)
    return render_template('profile.html', user=user)

@app.route('/profile/update', methods=['POST'])
def update_profile():
    username = get_current_username()
    if not username:
        abort(403)
    user = get_user(username)
    if user is None:
        abort(404)
    email = request.form.get('email', '').strip()
    fullname = request.form.get('fullname', '').strip()
    if not email or not fullname:
        error_message = 'Email and Full name are required.'
        return render_template('profile.html', user=user, error_message=error_message)
    update_user(username, email, fullname)
    user = get_user(username)
    success_message = 'Profile updated successfully.'
    return render_template('profile.html', user=user, success_message=success_message)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
