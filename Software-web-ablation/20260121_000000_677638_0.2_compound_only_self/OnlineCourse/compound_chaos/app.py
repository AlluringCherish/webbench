from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['DATA_DIR'] = 'data'

# Helper to get data file path

def get_data_path(filename):
    return os.path.join(app.config['DATA_DIR'], filename)

# --- Load and Save functions for each data file ---

def load_users():
    users = {}
    path = get_data_path('users.txt')
    if not os.path.isfile(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts)!=3:
                continue
            username, email, fullname = parts
            users[username] = {'username': username, 'email': email, 'fullname': fullname}
    return users

def save_users(users):
    path = get_data_path('users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for user in users.values():
            f.write('|'.join([user['username'], user['email'], user['fullname']]) + '\n')


def load_courses():
    courses = {}
    path = get_data_path('courses.txt')
    if not os.path.isfile(path):
        return courses
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            course_id = int(parts[0])
            courses[course_id] = {
                'course_id': course_id,
                'title': parts[1],
                'description': parts[2],
                'category': parts[3],
                'level': parts[4],
                'duration': parts[5],
                'status': parts[6]
            }
    return courses

def save_courses(courses):
    path = get_data_path('courses.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for course in courses.values():
            f.write('|'.join([
                str(course['course_id']), course['title'], course['description'], course['category'],
                course['level'], course['duration'], course['status']
            ]) + '\n')


def load_enrollments():
    enrollments = {}
    path = get_data_path('enrollments.txt')
    if not os.path.isfile(path):
        return enrollments
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            enrollment_id = int(parts[0])
            enrollments[enrollment_id] = {
                'enrollment_id': enrollment_id,
                'username': parts[1],
                'course_id': int(parts[2]),
                'enrollment_date': parts[3],
                'progress': int(parts[4]),
                'status': parts[5]
            }
    return enrollments

def save_enrollments(enrollments):
    path = get_data_path('enrollments.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for enrollment in enrollments.values():
            f.write('|'.join([
                str(enrollment['enrollment_id']), enrollment['username'], str(enrollment['course_id']),
                enrollment['enrollment_date'], str(enrollment['progress']), enrollment['status']
            ]) + '\n')


def load_assignments():
    assignments = {}
    path = get_data_path('assignments.txt')
    if not os.path.isfile(path):
        return assignments
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            assignment_id = int(parts[0])
            assignments[assignment_id] = {
                'assignment_id': assignment_id,
                'course_id': int(parts[1]),
                'title': parts[2],
                'description': parts[3],
                'due_date': parts[4],
                'max_points': int(parts[5])
            }
    return assignments

def save_assignments(assignments):
    path = get_data_path('assignments.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for assignment in assignments.values():
            f.write('|'.join([
                str(assignment['assignment_id']), str(assignment['course_id']), assignment['title'],
                assignment['description'], assignment['due_date'], str(assignment['max_points'])
            ]) + '\n')


def load_submissions():
    submissions = {}
    path = get_data_path('submissions.txt')
    if not os.path.isfile(path):
        return submissions
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            submission_id = int(parts[0])
            submissions[submission_id] = {
                'submission_id': submission_id,
                'assignment_id': int(parts[1]),
                'username': parts[2],
                'submission_text': parts[3],
                'submit_date': parts[4],
                'grade': int(parts[5]),
                'feedback': parts[6]
            }
    return submissions

def save_submissions(submissions):
    path = get_data_path('submissions.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for submission in submissions.values():
            f.write('|'.join([
                str(submission['submission_id']), str(submission['assignment_id']), submission['username'],
                submission['submission_text'], submission['submit_date'], str(submission['grade']), submission['feedback']
            ]) + '\n')


def load_certificates():
    certificates = {}
    path = get_data_path('certificates.txt')
    if not os.path.isfile(path):
        return certificates
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 4:
                continue
            certificate_id = int(parts[0])
            certificates[certificate_id] = {
                'certificate_id': certificate_id,
                'username': parts[1],
                'course_id': int(parts[2]),
                'issue_date': parts[3]
            }
    return certificates

def save_certificates(certificates):
    path = get_data_path('certificates.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for certificate in certificates.values():
            f.write('|'.join([
                str(certificate['certificate_id']), certificate['username'], str(certificate['course_id']), certificate['issue_date']
            ]) + '\n')


# Generate new unique ID

def generate_new_id(dic):
    if not dic:
        return 1
    return max(dic.keys()) + 1


# Hardcode current user
CURRENT_USER = 'john'


# Get user dict by username

def get_user(username):
    users = load_users()
    return users.get(username)


# Get enrollment record for user and course

def get_enrollment(username, course_id):
    enrollments = load_enrollments()
    for enrollment in enrollments.values():
        if enrollment['username'] == username and enrollment['course_id'] == course_id:
            return enrollment
    return None


# Get enrolled courses with progress for user

def get_courses_for_user(username):
    enrollments = load_enrollments()
    courses = load_courses()
    enrolled_courses = []
    for enrollment in enrollments.values():
        if enrollment['username'] == username:
            course = courses.get(enrollment['course_id'])
            if course:
                enrolled_courses.append({
                    'course_id': course['course_id'],
                    'title': course['title'],
                    'progress': enrollment['progress']
                })
    return enrolled_courses


# Simulate lessons for a course (no lessons.txt provided)

def get_lessons_for_course(course_id):
    courses = load_courses()
    course = courses.get(course_id)
    if not course:
        return []
    lessons = []
    for i in range(1, 6):  # 5 lessons
        lessons.append({
            'lesson_number': i,
            'title': f'Lesson {i}',
            'content': f'Content for Lesson {i} of course {course["title"]}.'
        })
    return lessons


# Get assignments for user courses

def get_assignments_for_user(username):
    assignments = load_assignments()
    enrollments = load_enrollments()
    user_courses = {e['course_id'] for e in enrollments.values() if e['username'] == username}
    return [a for a in assignments.values() if a['course_id'] in user_courses]


# Get submission for assignment and user

def get_submission_for_assignment_user(assignment_id, username):
    submissions = load_submissions()
    for sub in submissions.values():
        if sub['assignment_id'] == assignment_id and sub['username'] == username:
            return sub
    return None


# Check if certificate exists

def has_certificate(username, course_id):
    certificates = load_certificates()
    for c in certificates.values():
        if c['username'] == username and c['course_id'] == course_id:
            return True
    return False


# Create certificate record

def create_certificate(username, course_id):
    if has_certificate(username, course_id):
        return
    certificates = load_certificates()
    certificate_id = generate_new_id(certificates)
    issue_date = datetime.now().strftime('%Y-%m-%d')
    certificates[certificate_id] = {
        'certificate_id': certificate_id,
        'username': username,
        'course_id': course_id,
        'issue_date': issue_date
    }
    save_certificates(certificates)


# Routes

@app.route('/')
def home_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    user = get_user(CURRENT_USER)
    if not user:
        return "User not found", 404
    enrolled_courses = get_courses_for_user(CURRENT_USER)
    return render_template('dashboard.html', username=user['username'], fullname=user['fullname'], enrolled_courses=enrolled_courses)


@app.route('/catalog')
def course_catalog():
    courses = load_courses()
    search_query = request.args.get('search_query', '').strip()
    if search_query:
        sq = search_query.lower()
        filtered = [c for c in courses.values() if sq in c['title'].lower() or sq in c['category'].lower() or sq in c['level'].lower()]
    else:
        filtered = list(courses.values())
    return render_template('catalog.html', courses=filtered, search_query=search_query)


@app.route('/course/<int:course_id>', methods=['GET', 'POST'])
def course_details(course_id):
    courses = load_courses()
    course = courses.get(course_id)
    if not course:
        return "Course not found", 404
    user = get_user(CURRENT_USER)
    if not user:
        return "User not found", 404

    enrollments = load_enrollments()
    already_enrolled = any(e['username'] == CURRENT_USER and e['course_id'] == course_id for e in enrollments.values())

    if request.method == 'POST' and not already_enrolled:
        enrollment_id = generate_new_id(enrollments)
        enrollments[enrollment_id] = {
            'enrollment_id': enrollment_id,
            'username': CURRENT_USER,
            'course_id': course_id,
            'enrollment_date': datetime.now().strftime('%Y-%m-%d'),
            'progress': 0,
            'status': 'In Progress'
        }
        save_enrollments(enrollments)
        already_enrolled = True

    return render_template('course_details.html', course=course, already_enrolled=already_enrolled)


@app.route('/my-courses')
def my_courses():
    user = get_user(CURRENT_USER)
    if not user:
        return "User not found", 404
    enrolled_courses = get_courses_for_user(CURRENT_USER)
    return render_template('my_courses.html', enrolled_courses=enrolled_courses)


@app.route('/learning/<int:course_id>', methods=['GET', 'POST'])
def course_learning(course_id):
    courses = load_courses()
    course = courses.get(course_id)
    if not course:
        return "Course not found", 404
    user = get_user(CURRENT_USER)
    if not user:
        return "User not found", 404

    enrollments = load_enrollments()
    enrollment = None
    for e in enrollments.values():
        if e['username'] == CURRENT_USER and e['course_id'] == course_id:
            enrollment = e
            break
    if not enrollment:
        return redirect(url_for('course_details', course_id=course_id))

    lessons = get_lessons_for_course(course_id)
    total_lessons = len(lessons)

    progress = enrollment['progress']
    completed_lessons = int((progress / 100) * total_lessons) if total_lessons > 0 else 0

    if completed_lessons < total_lessons:
        current_lesson = lessons[completed_lessons]
        can_mark_complete = True
    else:
        current_lesson = lessons[-1]
        can_mark_complete = False

    if request.method == 'POST' and can_mark_complete:
        completed_lessons += 1
        new_progress = int((completed_lessons / total_lessons) * 100) if total_lessons > 0 else 0
        enrollment['progress'] = new_progress
        enrollment['status'] = 'Completed' if new_progress == 100 else 'In Progress'
        enrollments[enrollment['enrollment_id']] = enrollment
        save_enrollments(enrollments)
        progress = new_progress

        if new_progress == 100:
            create_certificate(CURRENT_USER, course_id)

        if completed_lessons < total_lessons:
            current_lesson = lessons[completed_lessons]
            can_mark_complete = True
        else:
            current_lesson = lessons[-1]
            can_mark_complete = False

    return render_template('learning.html', course=course, lessons=lessons, current_lesson=current_lesson, progress=progress, can_mark_complete=can_mark_complete)


@app.route('/assignments')
def my_assignments():
    user = get_user(CURRENT_USER)
    if not user:
        return "User not found", 404
    assignments = get_assignments_for_user(CURRENT_USER)
    return render_template('assignments.html', assignments=assignments)


@app.route('/submit-assignment/<int:assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    assignments = load_assignments()
    assignment = assignments.get(assignment_id)
    if not assignment:
        return "Assignment not found", 404
    user = get_user(CURRENT_USER)
    if not user:
        return "User not found", 404
    submissions = load_submissions()
    submission = get_submission_for_assignment_user(assignment_id, CURRENT_USER)

    submission_status = None
    confirmation = None

    if request.method == 'POST':
        submission_text = request.form.get('submission_text', '').strip()
        if not submission_text:
            submission_status = 'Submission text cannot be empty.'
        else:
            if submission:
                submission['submission_text'] = submission_text
                submission['submit_date'] = datetime.now().strftime('%Y-%m-%d')
                submission['grade'] = 0
                submission['feedback'] = ''
                submissions[submission['submission_id']] = submission
            else:
                submission_id = generate_new_id(submissions)
                submissions[submission_id] = {
                    'submission_id': submission_id,
                    'assignment_id': assignment_id,
                    'username': CURRENT_USER,
                    'submission_text': submission_text,
                    'submit_date': datetime.now().strftime('%Y-%m-%d'),
                    'grade': 0,
                    'feedback': ''
                }
            save_submissions(submissions)
            submission_status = 'Submitted'
            confirmation = 'Your assignment has been submitted successfully.'

    return render_template('submit_assignment.html', assignment=assignment, submission_status=submission_status, confirmation=confirmation)


@app.route('/certificates')
def certificates():
    user = get_user(CURRENT_USER)
    if not user:
        return "User not found", 404
    certificates = load_certificates()
    user_certs = [c for c in certificates.values() if c['username'] == CURRENT_USER]
    return render_template('certificates.html', certificates=user_certs)


@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    users = load_users()
    user = users.get(CURRENT_USER)
    if not user:
        return "User not found", 404
    update_status = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        fullname = request.form.get('fullname', '').strip()
        if not email or not fullname:
            update_status = 'Email and Full name cannot be empty.'
        else:
            user['email'] = email
            user['fullname'] = fullname
            users[CURRENT_USER] = user
            save_users(users)
            update_status = 'Profile updated successfully.'
    return render_template('profile.html', user_profile=user, update_status=update_status)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
