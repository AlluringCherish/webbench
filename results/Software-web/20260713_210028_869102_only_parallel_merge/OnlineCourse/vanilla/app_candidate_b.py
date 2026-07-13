from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATA_DIR = 'data'
CURRENT_USER = 'john'  # Simulating logged-in user

# Helper functions for file I/O and data handling

def read_users():
    users_path = os.path.join(DATA_DIR, 'users.txt')
    users = {}
    if os.path.exists(users_path):
        with open(users_path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                username,email,fullname = line.split('|')
                users[username] = {'email': email, 'fullname': fullname}
    return users

def write_users(users):
    users_path = os.path.join(DATA_DIR, 'users.txt')
    with open(users_path, 'w', encoding='utf-8') as f:
        for username, data in users.items():
            f.write(f"{username}|{data['email']}|{data['fullname']}\n")

def read_courses():
    courses_path = os.path.join(DATA_DIR, 'courses.txt')
    courses = {}
    if os.path.exists(courses_path):
        with open(courses_path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                course_id = parts[0]
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

def read_enrollments():
    enrollments_path = os.path.join(DATA_DIR, 'enrollments.txt')
    enrollments = []
    if os.path.exists(enrollments_path):
        with open(enrollments_path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                enrollment = {
                    'enrollment_id': parts[0],
                    'username': parts[1],
                    'course_id': parts[2],
                    'enrollment_date': parts[3],
                    'progress': int(parts[4]),
                    'status': parts[5]
                }
                enrollments.append(enrollment)
    return enrollments

def write_enrollments(enrollments):
    enrollments_path = os.path.join(DATA_DIR, 'enrollments.txt')
    with open(enrollments_path, 'w', encoding='utf-8') as f:
        for e in enrollments:
            line = f"{e['enrollment_id']}|{e['username']}|{e['course_id']}|{e['enrollment_date']}|{e['progress']}|{e['status']}\n"
            f.write(line)

def read_assignments():
    assignments_path = os.path.join(DATA_DIR, 'assignments.txt')
    assignments = {}
    if os.path.exists(assignments_path):
        with open(assignments_path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                assignment_id = parts[0]
                assignments[assignment_id] = {
                    'assignment_id': assignment_id,
                    'course_id': parts[1],
                    'title': parts[2],
                    'description': parts[3],
                    'due_date': parts[4],
                    'max_points': parts[5]
                }
    return assignments

def read_submissions():
    submissions_path = os.path.join(DATA_DIR, 'submissions.txt')
    submissions = []
    if os.path.exists(submissions_path):
        with open(submissions_path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                submission = {
                    'submission_id': parts[0],
                    'assignment_id': parts[1],
                    'username': parts[2],
                    'submission_text': parts[3],
                    'submit_date': parts[4],
                    'grade': parts[5],
                    'feedback': parts[6]
                }
                submissions.append(submission)
    return submissions

def write_submissions(submissions):
    submissions_path = os.path.join(DATA_DIR, 'submissions.txt')
    with open(submissions_path, 'w', encoding='utf-8') as f:
        for s in submissions:
            line = f"{s['submission_id']}|{s['assignment_id']}|{s['username']}|{s['submission_text']}|{s['submit_date']}|{s['grade']}|{s['feedback']}\n"
            f.write(line)

def read_certificates():
    certificates_path = os.path.join(DATA_DIR, 'certificates.txt')
    certificates = []
    if os.path.exists(certificates_path):
        with open(certificates_path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                cert = {
                    'certificate_id': parts[0],
                    'username': parts[1],
                    'course_id': parts[2],
                    'issue_date': parts[3]
                }
                certificates.append(cert)
    return certificates

def write_certificates(certificates):
    certificates_path = os.path.join(DATA_DIR, 'certificates.txt')
    with open(certificates_path, 'w', encoding='utf-8') as f:
        for c in certificates:
            line = f"{c['certificate_id']}|{c['username']}|{c['course_id']}|{c['issue_date']}\n"
            f.write(line)

# For simplicity, lessons data is simulated as course_id to list of lessons (title, content)
# In real app, lessons data should be loaded from a file or DB
# Here we simulate 5 lessons per course
LESSONS_DATA = {
    '1': [
        {'lesson_no': 1, 'title': 'Introduction to Python', 'content': 'Python basics and setup.'},
        {'lesson_no': 2, 'title': 'Variables and Data Types', 'content': 'Learn variables and types.'},
        {'lesson_no': 3, 'title': 'Control Structures', 'content': 'If statements, loops.'},
        {'lesson_no': 4, 'title': 'Functions', 'content': 'Defining and calling functions.'},
        {'lesson_no': 5, 'title': 'Modules and Packages', 'content': 'Using standard libraries.'},
    ],
    '2': [
        {'lesson_no': 1, 'title': 'Introduction to Web Dev', 'content': 'HTML, CSS basics.'},
        {'lesson_no': 2, 'title': 'JavaScript Basics', 'content': 'Learning JS for interactivity.'},
        {'lesson_no': 3, 'title': 'Frontend Frameworks', 'content': 'React, Vue overview.'},
        {'lesson_no': 4, 'title': 'Backend Development', 'content': 'Flask, Django basics.'},
        {'lesson_no': 5, 'title': 'Deployment', 'content': 'Deploying web apps.'},
    ],
    '3': [
        {'lesson_no': 1, 'title': 'Data Science Intro', 'content': 'What is data science?'},
        {'lesson_no': 2, 'title': 'Data Wrangling', 'content': 'Cleaning data.'},
        {'lesson_no': 3, 'title': 'Data Visualization', 'content': 'Charts and graphs.'},
        {'lesson_no': 4, 'title': 'Machine Learning Basics', 'content': 'Intro to ML algorithms.'},
        {'lesson_no': 5, 'title': 'Project Work', 'content': 'Building a data project.'},
    ],
}

@app.route('/dashboard')
def dashboard():
    users = read_users()
    user = users.get(CURRENT_USER)
    if not user:
        fullname = CURRENT_USER
    else:
        fullname = user['fullname']
    enrollments = read_enrollments()
    courses = read_courses()
    user_enrollments = [e for e in enrollments if e['username'] == CURRENT_USER]
    enrolled_courses = []
    for e in user_enrollments:
        c = courses.get(e['course_id'])
        if c:
            enrolled_courses.append({
                'course_id': c['course_id'],
                'title': c['title'],
                'progress': e['progress'],
                'status': e['status']
            })
    return render_template('dashboard.html', fullname=fullname, enrolled_courses=enrolled_courses)

@app.route('/courses/catalog', methods=['GET', 'POST'])
def course_catalog():
    search_text = ''
    if request.method == 'POST':
        search_text = request.form.get('search', '').lower()
    courses = read_courses()
    active_courses = [c for c in courses.values() if c['status'].lower() == 'active']
    if search_text:
        active_courses = [c for c in active_courses if search_text in c['title'].lower() or search_text in c['category'].lower()]
    return render_template('catalog.html', courses=active_courses, search_text=search_text)

@app.route('/courses/details/<course_id>', methods=['GET', 'POST'])
def course_details(course_id):
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        return "Course not found", 404
    enrollments = read_enrollments()
    user_enrollments = [e for e in enrollments if e['username'] == CURRENT_USER and e['course_id'] == course_id]
    enrolled = len(user_enrollments) > 0
    if request.method == 'POST':
        if not enrolled:
            enrollment_id = 1
            if enrollments:
                enrollment_id = max(int(e['enrollment_id']) for e in enrollments) + 1
            today = datetime.now().strftime('%Y-%m-%d')
            new_enrollment = {
                'enrollment_id': str(enrollment_id),
                'username': CURRENT_USER,
                'course_id': course_id,
                'enrollment_date': today,
                'progress': 0,
                'status': 'In Progress'
            }
            enrollments.append(new_enrollment)
            write_enrollments(enrollments)
            enrolled = True
            flash('Enrollment successful!')
    return render_template('course_details.html', course=course, enrolled=enrolled)

@app.route('/courses/mine')
def my_courses():
    enrollments = read_enrollments()
    courses = read_courses()
    user_enrollments = [e for e in enrollments if e['username'] == CURRENT_USER]
    courses_list = []
    for e in user_enrollments:
        c = courses.get(e['course_id'])
        if c:
            courses_list.append({
                'course_id': c['course_id'],
                'title': c['title'],
                'progress': e['progress'],
                'status': e['status']
            })
    return render_template('my_courses.html', courses=courses_list)

@app.route('/courses/learn/<course_id>', methods=['GET', 'POST'])
def course_learning(course_id):
    lessons = LESSONS_DATA.get(course_id)
    if not lessons:
        return "Lessons not found for this course.", 404

    enrollments = read_enrollments()
    enrollment = None
    for e in enrollments:
        if e['username'] == CURRENT_USER and e['course_id'] == course_id:
            enrollment = e
            break
    if not enrollment:
        flash('You are not enrolled in this course.')
        return redirect(url_for('my_courses'))

    completed_lessons_count = int(enrollment['progress'] * len(lessons) / 100)

    # Determine current lesson: first incomplete one or last completed
    current_lesson_index = completed_lessons_count if completed_lessons_count < len(lessons) else len(lessons) - 1

    if request.method == 'POST':
        # Mark complete logic
        # Allow marking only the next lesson in sequence
        if current_lesson_index < len(lessons):
            # Check if current lesson is the next to be completed
            # Mark current lesson as completed
            completed_lessons_count += 1
            progress = int(completed_lessons_count * 100 / len(lessons))
            enrollment['progress'] = progress
            if progress == 100:
                enrollment['status'] = 'Completed'
                # Generate certificate if not exists
                certificates = read_certificates()
                existing_cert = [c for c in certificates if c['username'] == CURRENT_USER and c['course_id'] == course_id]
                if not existing_cert:
                    certificate_id = 1
                    if certificates:
                        certificate_id = max(int(c['certificate_id']) for c in certificates) + 1
                    today = datetime.now().strftime('%Y-%m-%d')
                    certificates.append({
                        'certificate_id': str(certificate_id),
                        'username': CURRENT_USER,
                        'course_id': course_id,
                        'issue_date': today
                    })
                    write_certificates(certificates)
            # Update enrollments file
            write_enrollments(enrollments)
            flash('Lesson marked as complete.')
            # Refresh current lesson index
            current_lesson_index = completed_lessons_count if completed_lessons_count < len(lessons) else len(lessons) - 1

    current_lesson = lessons[current_lesson_index]

    # Disable mark complete if user tries to skip lessons
    can_mark_complete = (current_lesson_index == completed_lessons_count)

    return render_template('learning.html', lessons=lessons, current_lesson=current_lesson,
                           can_mark_complete=can_mark_complete, progress=enrollment['progress'], course_id=course_id)

@app.route('/assignments')
def my_assignments():
    enrollments = read_enrollments()
    assignments = read_assignments()
    submissions = read_submissions()

    # get course ids user enrolled in
    user_course_ids = {e['course_id'] for e in enrollments if e['username'] == CURRENT_USER}

    # Filter assignments for user's enrolled courses
    user_assignments = [a for a in assignments.values() if a['course_id'] in user_course_ids]

    # For each assignment check submission status
    assignments_info = []
    for a in user_assignments:
        submitted = any(s for s in submissions if s['assignment_id'] == a['assignment_id'] and s['username'] == CURRENT_USER)
        submission_record = next((s for s in submissions if s['assignment_id'] == a['assignment_id'] and s['username'] == CURRENT_USER), None)
        grade = submission_record['grade'] if submission_record else 'N/A'
        status = 'Submitted' if submitted else 'Pending'
        assignments_info.append({
            'assignment_id': a['assignment_id'],
            'title': a['title'],
            'due_date': a['due_date'],
            'status': status,
            'grade': grade
        })

    return render_template('assignments.html', assignments=assignments_info)

@app.route('/assignments/submit/<assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    assignments = read_assignments()
    assignment = assignments.get(assignment_id)
    if not assignment:
        return "Assignment not found", 404

    if request.method == 'POST':
        submission_text = request.form.get('submission_text', '').strip()
        if not submission_text:
            flash('Submission text cannot be empty.')
            return redirect(request.url)

        submissions = read_submissions()
        submission_id = 1
        if submissions:
            submission_id = max(int(s['submission_id']) for s in submissions) + 1
        today = datetime.now().strftime('%Y-%m-%d')
        submissions.append({
            'submission_id': str(submission_id),
            'assignment_id': assignment_id,
            'username': CURRENT_USER,
            'submission_text': submission_text.replace('|',' '),  # sanitize pipe
            'submit_date': today,
            'grade': 'null',
            'feedback': ''
        })
        write_submissions(submissions)
        flash('Assignment submitted successfully!')
        return redirect(url_for('my_assignments'))

    return render_template('submit_assignment.html', assignment=assignment)

@app.route('/certificates')
def certificates():
    certificates = read_certificates()
    courses = read_courses()
    enrollments = read_enrollments()

    user_certs = [c for c in certificates if c['username'] == CURRENT_USER]
    user_enrollments = {e['course_id']: e for e in enrollments if e['username'] == CURRENT_USER and e['status'] == 'Completed'}

    certs_display = []
    for cert in user_certs:
        if cert['course_id'] in user_enrollments:
            course = courses.get(cert['course_id'])
            if course:
                certs_display.append({
                    'certificate_id': cert['certificate_id'],
                    'course_title': course['title'],
                    'issue_date': cert['issue_date'],
                })

    return render_template('certificates.html', certificates=certs_display)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = read_users()
    user = users.get(CURRENT_USER)
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        fullname = request.form.get('fullname', '').strip()
        if user:
            user['email'] = email
            user['fullname'] = fullname
            users[CURRENT_USER] = user
            write_users(users)
            flash('Profile updated successfully!')
        else:
            flash('User not found.')
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user)

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
