from flask import Flask, render_template, request, redirect, url_for, abort, flash
from datetime import datetime
import os
import re

app = Flask(__name__)
app.secret_key = 'onlinecourse-secret-key'  # Needed for flash messages

DATA_DIR = 'data'

# Utility functions for file IO and parsing

def get_file_path(filename):
    return os.path.join(DATA_DIR, filename)

# Users.txt fields: username|email|fullname
# Return list of dicts

def read_users():
    users = []
    path = get_file_path('users.txt')
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
            users.append({
                'username': username,
                'email': email,
                'fullname': fullname
            })
    return users


def write_users(users):
    path = get_file_path('users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for user in users:
            line = f"{user['username']}|{user['email']}|{user['fullname']}"
            f.write(line + '\n')

# Validate email

def valid_email(email):
    # Simple regex email validation
    regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(regex, email) is not None

# Courses.txt fields: course_id|title|description|category|level|duration|status

def read_courses():
    courses = []
    path = get_file_path('courses.txt')
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
            courses.append({
                'course_id': course_id,
                'title': title,
                'description': description,
                'category': category,
                'level': level,
                'duration': duration,
                'status': status
            })
    return courses

# Helper to find course by id

def find_course(course_id):
    courses = read_courses()
    for course in courses:
        if course['course_id'] == course_id:
            return course
    return None

# Enrollments.txt fields: enrollment_id|username|course_id|enrollment_date|progress|status

def read_enrollments():
    enrollments = []
    path = get_file_path('enrollments.txt')
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
            enrollment_id, username, course_id, enrollment_date, progress_str, status = parts
            try:
                progress = int(progress_str)
            except:
                progress = 0
            enrollments.append({
                'enrollment_id': enrollment_id,
                'username': username,
                'course_id': course_id,
                'enrollment_date': enrollment_date,
                'progress': progress,
                'status': status
            })
    return enrollments


def write_enrollments(enrollments):
    path = get_file_path('enrollments.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for e in enrollments:
            line = f"{e['enrollment_id']}|{e['username']}|{e['course_id']}|{e['enrollment_date']}|{e['progress']}|{e['status']}"
            f.write(line + '\n')

# Assignments.txt fields: assignment_id|course_id|title|description|due_date|max_points

def read_assignments():
    assignments = []
    path = get_file_path('assignments.txt')
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
            assignment_id, course_id, title, description, due_date, max_points_str = parts
            max_points = 0
            try:
                max_points = int(max_points_str)
            except:
                max_points = 0
            assignments.append({
                'assignment_id': assignment_id,
                'course_id': course_id,
                'title': title,
                'description': description,
                'due_date': due_date,
                'max_points': max_points
            })
    return assignments

# Helper find assignment by id

def find_assignment(assignment_id):
    assignments = read_assignments()
    for a in assignments:
        if a['assignment_id'] == assignment_id:
            return a
    return None

# Submissions.txt fields: submission_id|assignment_id|username|submission_text|submit_date|grade|feedback

def read_submissions():
    submissions = []
    path = get_file_path('submissions.txt')
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
            submission_id, assignment_id, username, submission_text, submit_date, grade_str, feedback = parts
            try:
                grade = int(grade_str)
            except:
                grade = None
            submissions.append({
                'submission_id': submission_id,
                'assignment_id': assignment_id,
                'username': username,
                'submission_text': submission_text,
                'submit_date': submit_date,
                'grade': grade,
                'feedback': feedback
            })
    return submissions


def write_submissions(submissions):
    path = get_file_path('submissions.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for s in submissions:
            grade_str = str(s['grade']) if s['grade'] is not None else ''
            line = f"{s['submission_id']}|{s['assignment_id']}|{s['username']}|{s['submission_text']}|{s['submit_date']}|{grade_str}|{s['feedback']}"
            f.write(line + '\n')

# Certificates.txt fields: certificate_id|username|course_id|issue_date

def read_certificates():
    certificates = []
    path = get_file_path('certificates.txt')
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
    path = get_file_path('certificates.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for c in certificates:
            line = f"{c['certificate_id']}|{c['username']}|{c['course_id']}|{c['issue_date']}"
            f.write(line + '\n')

# Helper: generate next id for enrollments, submissions, certificates

def generate_next_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            _id = int(item[id_key])
            if _id > max_id:
                max_id = _id
        except:
            continue
    return str(max_id + 1)

# Helper to get enrollment by username and course_id

def find_enrollment(username, course_id):
    enrollments = read_enrollments()
    for e in enrollments:
        if e['username'] == username and e['course_id'] == course_id:
            return e
    return None

# Helper to get all enrollments for a username

def get_user_enrollments(username):
    enrollments = read_enrollments()
    return [e for e in enrollments if e['username'] == username]

# A placeholder for the current logged-in user
# In a real app, would use authentication. Here fixed username for demonstration
CURRENT_USER = 'john'  # We will assume 'john' is logged in for all routes


@app.route('/')
def dashboard():
    username = CURRENT_USER
    users = read_users()
    user = next((u for u in users if u['username'] == username), None)
    if user is None:
        abort(404)

    enrollments = get_user_enrollments(username)
    courses = read_courses()

    enrolled_courses = []
    for enrollment in enrollments:
        course = find_course(enrollment['course_id'])
        if course:
            enrolled_courses.append({
                'course_id': course['course_id'],
                'title': course['title'],
                'description': course['description'],
                'duration': course['duration'],
                'status': enrollment['status'],
                'progress': enrollment['progress']
            })

    return render_template('dashboard.html', username=username, enrolled_courses=enrolled_courses)

@app.route('/catalog')
def catalog():
    username = CURRENT_USER
    courses = read_courses()
    courses_display = []
    for course in courses:
        courses_display.append({
            'course_id': course['course_id'],
            'title': course['title'],
            'description': course['description'],
            'category': course['category'],
            'level': course['level'],
            'duration': course['duration'],
            'status': course['status']
        })

    return render_template('catalog.html', username=username, courses=courses_display)

@app.route('/course/<course_id>', methods=['GET', 'POST'])
def course_details(course_id):
    username = CURRENT_USER
    course = find_course(course_id)
    if course is None:
        abort(404)

    enrollment = find_enrollment(username, course_id)
    already_enrolled = enrollment is not None
    enroll_status = False

    if request.method == 'POST':
        if not already_enrolled:
            enrollments = read_enrollments()
            new_id = generate_next_id(enrollments, 'enrollment_id')
            enrollment_date = datetime.now().strftime('%Y-%m-%d')
            new_enrollment = {
                'enrollment_id': new_id,
                'username': username,
                'course_id': course_id,
                'enrollment_date': enrollment_date,
                'progress': 0,
                'status': 'In Progress'
            }
            enrollments.append(new_enrollment)
            write_enrollments(enrollments)
            already_enrolled = True
            enroll_status = True
            flash('Successfully enrolled in the course.', 'success')
        else:
            flash('Already enrolled in this course.', 'info')
        return redirect(url_for('course_details', course_id=course_id))

    return render_template('course_details.html', username=username, course=course, enroll_status=enroll_status, already_enrolled=already_enrolled)

@app.route('/my-courses')
def my_courses():
    username = CURRENT_USER
    enrollments = get_user_enrollments(username)
    courses = read_courses()

    enrolled_courses = []
    for enrollment in enrollments:
        course = find_course(enrollment['course_id'])
        if course:
            enrolled_courses.append({
                'course_id': course['course_id'],
                'title': course['title'],
                'progress': enrollment['progress'],
                'status': enrollment['status']
            })

    return render_template('my_courses.html', username=username, enrolled_courses=enrolled_courses)

# Lessons mock data: since lessons.txt or similar not defined
MOCK_LESSONS = {
    '1': [
        {'lesson_id': '1', 'title': 'Python Basics', 'content': 'Introduction to Python Programming.'},
        {'lesson_id': '2', 'title': 'Data Types', 'content': 'Understanding data types in Python.'},
        {'lesson_id': '3', 'title': 'Control Flow', 'content': 'If statements, loops and more.'},
        {'lesson_id': '4', 'title': 'Functions', 'content': 'Defining and using functions.'},
        {'lesson_id': '5', 'title': 'Modules & Packages', 'content': 'Using Python modules and packages.'},
    ],
    '2': [
        {'lesson_id': '1', 'title': 'HTML Basics', 'content': 'Introduction to HTML.'},
        {'lesson_id': '2', 'title': 'CSS Fundamentals', 'content': 'Styling with CSS.'},
        {'lesson_id': '3', 'title': 'JavaScript Introduction', 'content': 'Basics of JavaScript programming.'},
        {'lesson_id': '4', 'title': 'Building a Website', 'content': 'Putting it all together.'},
    ],
    '3': [
        {'lesson_id': '1', 'title': 'Data Science Overview', 'content': 'What is Data Science?'},
        {'lesson_id': '2', 'title': 'Data Analysis Tools', 'content': 'Tools used in data science.'},
        {'lesson_id': '3', 'title': 'Statistics Basics', 'content': 'Basic statistics concepts.'},
        {'lesson_id': '4', 'title': 'Machine Learning Intro', 'content': 'Introduction to ML.'},
        {'lesson_id': '5', 'title': 'Project Work', 'content': 'Apply what you learned.'},
    ]
}

@app.route('/learn/<course_id>', methods=['GET', 'POST'])
def course_learning(course_id):
    username = CURRENT_USER
    course = find_course(course_id)
    if course is None:
        abort(404)

    enrollment = find_enrollment(username, course_id)
    if enrollment is None:
        flash('You must enroll in the course to learn.', 'warning')
        return redirect(url_for('course_details', course_id=course_id))

    lessons = MOCK_LESSONS.get(course_id, [])
    total_lessons = len(lessons)

    progress = enrollment['progress']  # 0-100 integer

    completed_lesson_count = int(progress * total_lessons / 100) if total_lessons > 0 else 0

    # Determine current lesson index based on lessons completed
    if completed_lesson_count < total_lessons:
        current_lesson_idx = completed_lesson_count
    else:
        current_lesson_idx = total_lessons - 1 if total_lessons > 0 else None

    current_lesson_id = lessons[current_lesson_idx]['lesson_id'] if current_lesson_idx is not None else None

    completed_lessons = set(lesson['lesson_id'] for lesson in lessons[:completed_lesson_count])

    if request.method == 'POST':
        # Only allow marking complete if progress < 100
        if progress >= 100:
            flash('You have already completed this course.', 'info')
            return redirect(url_for('course_learning', course_id=course_id))

        # Mark current lesson complete, update progress
        new_completed_count = completed_lesson_count + 1
        if new_completed_count > total_lessons:
            new_completed_count = total_lessons
        new_progress = int(new_completed_count * 100 / total_lessons) if total_lessons > 0 else 100

        enrollments = read_enrollments()
        updated = False
        for e in enrollments:
            if e['username'] == username and e['course_id'] == course_id:
                e['progress'] = new_progress
                e['status'] = 'Completed' if new_progress == 100 else 'In Progress'
                updated = True
                break
        if updated:
            write_enrollments(enrollments)

            # Generate certificate automatically if progress is 100 and no certificate exists
            if new_progress == 100:
                certificates = read_certificates()
                already_certified = any(c['username'] == username and c['course_id'] == course_id for c in certificates)
                if not already_certified:
                    new_cert_id = generate_next_id(certificates, 'certificate_id')
                    issue_date = datetime.now().strftime('%Y-%m-%d')
                    new_certificate = {
                        'certificate_id': new_cert_id,
                        'username': username,
                        'course_id': course_id,
                        'issue_date': issue_date
                    }
                    certificates.append(new_certificate)
                    write_certificates(certificates)
                    flash('Congratulations! You have completed the course and earned a certificate.', 'success')

        return redirect(url_for('course_learning', course_id=course_id))

    return render_template('learning.html', username=username, course=course, lessons=lessons,
                           current_lesson_id=current_lesson_id, completed_lessons=completed_lessons,
                           progress=progress, enrollment=enrollment)

@app.route('/assignments')
def assignments():
    username = CURRENT_USER
    enrollments = get_user_enrollments(username)
    user_courses_ids = {e['course_id'] for e in enrollments}

    all_assignments = read_assignments()

    assignments_to_show = []

    for assignment in all_assignments:
        if assignment['course_id'] in user_courses_ids:
            assignments_to_show.append(assignment)

    return render_template('assignments.html', username=username, assignments=assignments_to_show)

@app.route('/submit/<assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    username = CURRENT_USER
    assignment = find_assignment(assignment_id)
    if assignment is None:
        abort(404)

    submissions = read_submissions()
    previous_submission = None
    for s in submissions:
        if s['assignment_id'] == assignment_id and s['username'] == username:
            previous_submission = s
            break

    if request.method == 'POST':
        submission_text = request.form.get('submission_text', '').strip()
        if not submission_text:
            flash('Submission text cannot be empty.', 'error')
            return redirect(url_for('submit_assignment', assignment_id=assignment_id))

        # Update or new submission
        found_index = None
        for i, s in enumerate(submissions):
            if s['assignment_id'] == assignment_id and s['username'] == username:
                found_index = i
                break

        submit_date = datetime.now().strftime('%Y-%m-%d')

        if found_index is not None:
            submissions[found_index]['submission_text'] = submission_text
            submissions[found_index]['submit_date'] = submit_date
        else:
            new_id = generate_next_id(submissions, 'submission_id')
            submissions.append({
                'submission_id': new_id,
                'assignment_id': assignment_id,
                'username': username,
                'submission_text': submission_text,
                'submit_date': submit_date,
                'grade': None,
                'feedback': ''
            })

        write_submissions(submissions)
        flash('Submission saved successfully.', 'success')
        return redirect(url_for('submit_assignment', assignment_id=assignment_id))

    return render_template('submit.html', username=username, assignment=assignment, previous_submission=previous_submission)

@app.route('/certificates')
def certificates():
    username = CURRENT_USER
    certificates = read_certificates()
    user_certificates = [c for c in certificates if c['username'] == username]

    courses = read_courses()
    certs_with_titles = []
    for c in user_certificates:
        course = find_course(c['course_id'])
        course_title = course['title'] if course else 'Unknown'
        certs_with_titles.append({
            'certificate_id': c['certificate_id'],
            'course_id': c['course_id'],
            'issue_date': c['issue_date'],
            'course_title': course_title
        })

    return render_template('certificates.html', username=username, certificates=certs_with_titles)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = CURRENT_USER
    users = read_users()
    user = next((u for u in users if u['username'] == username), None)
    if user is None:
        abort(404)

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        fullname = request.form.get('fullname', '').strip()

        if not email:
            flash('Email cannot be empty.', 'error')
            return redirect(url_for('profile'))
        if not valid_email(email):
            flash('Invalid email format.', 'error')
            return redirect(url_for('profile'))
        if not fullname:
            flash('Full name cannot be empty.', 'error')
            return redirect(url_for('profile'))

        for u in users:
            if u['username'] == username:
                u['email'] = email
                u['fullname'] = fullname
                break
        write_users(users)
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html', username=username, user_email=user['email'], user_fullname=user['fullname'])


if __name__ == '__main__':
    app.run(debug=True, port=5000)
