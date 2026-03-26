'''
Main backend Python application for OnlineCourse web application.
Implements the web server, routing, and all business logic using Flask.
Handles reading from and writing to local text files in the 'data' directory.
Manages user sessions, course enrollment, progress tracking, assignment submissions, and certificate generation.
Serves HTML templates and handles form submissions.
Includes a login page to allow user authentication and session management.
'''
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key in production
DATA_DIR = 'data'
# Utility functions for file operations and data parsing
def read_users():
    users = {}
    path = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                username, email, fullname = line.split('|')
                users[username] = {'email': email, 'fullname': fullname}
    return users
def write_users(users):
    path = os.path.join(DATA_DIR, 'users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for username, info in users.items():
            f.write(f"{username}|{info['email']}|{info['fullname']}\n")
def read_courses():
    courses = {}
    path = os.path.join(DATA_DIR, 'courses.txt')
    if not os.path.exists(path):
        return courses
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 7:
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
    enrollments = {}
    path = os.path.join(DATA_DIR, 'enrollments.txt')
    if not os.path.exists(path):
        return enrollments
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 6:
                    enrollment_id = parts[0]
                    enrollments[enrollment_id] = {
                        'enrollment_id': enrollment_id,
                        'username': parts[1],
                        'course_id': parts[2],
                        'enrollment_date': parts[3],
                        'progress': float(parts[4]),
                        'status': parts[5]
                    }
    return enrollments
def write_enrollments(enrollments):
    path = os.path.join(DATA_DIR, 'enrollments.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for enrollment in enrollments.values():
            f.write(f"{enrollment['enrollment_id']}|{enrollment['username']}|{enrollment['course_id']}|{enrollment['enrollment_date']}|{int(enrollment['progress'])}|{enrollment['status']}\n")
def read_assignments():
    assignments = {}
    path = os.path.join(DATA_DIR, 'assignments.txt')
    if not os.path.exists(path):
        return assignments
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 6:
                    assignment_id = parts[0]
                    assignments[assignment_id] = {
                        'assignment_id': assignment_id,
                        'course_id': parts[1],
                        'title': parts[2],
                        'description': parts[3],
                        'due_date': parts[4],
                        'max_points': int(parts[5])
                    }
    return assignments
def read_submissions():
    submissions = {}
    path = os.path.join(DATA_DIR, 'submissions.txt')
    if not os.path.exists(path):
        return submissions
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 7:
                    submission_id = parts[0]
                    submissions[submission_id] = {
                        'submission_id': submission_id,
                        'assignment_id': parts[1],
                        'username': parts[2],
                        'submission_text': parts[3],
                        'submit_date': parts[4],
                        'grade': parts[5],
                        'feedback': parts[6]
                    }
    return submissions
def write_submissions(submissions):
    path = os.path.join(DATA_DIR, 'submissions.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for sub in submissions.values():
            f.write(f"{sub['submission_id']}|{sub['assignment_id']}|{sub['username']}|{sub['submission_text']}|{sub['submit_date']}|{sub['grade']}|{sub['feedback']}\n")
def read_certificates():
    certificates = {}
    path = os.path.join(DATA_DIR, 'certificates.txt')
    if not os.path.exists(path):
        return certificates
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 4:
                    certificate_id = parts[0]
                    certificates[certificate_id] = {
                        'certificate_id': certificate_id,
                        'username': parts[1],
                        'course_id': parts[2],
                        'issue_date': parts[3]
                    }
    return certificates
def write_certificates(certificates):
    path = os.path.join(DATA_DIR, 'certificates.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for cert in certificates.values():
            f.write(f"{cert['certificate_id']}|{cert['username']}|{cert['course_id']}|{cert['issue_date']}\n")
# Helper functions
def get_next_id(data_dict):
    if not data_dict:
        return '1'
    else:
        max_id = max(int(k) for k in data_dict.keys())
        return str(max_id + 1)
def get_logged_in_username():
    return session.get('username')
def get_user_fullname(username):
    users = read_users()
    user = users.get(username)
    if user:
        return user['fullname']
    return None
def is_enrolled(username, course_id):
    enrollments = read_enrollments()
    for enrollment in enrollments.values():
        if enrollment['username'] == username and enrollment['course_id'] == course_id:
            return enrollment
    return None
def update_enrollment_progress(enrollment_id, progress):
    enrollments = read_enrollments()
    if enrollment_id in enrollments:
        enrollments[enrollment_id]['progress'] = progress
        if progress >= 100:
            enrollments[enrollment_id]['progress'] = 100
            enrollments[enrollment_id]['status'] = 'Completed'
        else:
            enrollments[enrollment_id]['status'] = 'In Progress'
        write_enrollments(enrollments)
def generate_certificate(username, course_id):
    certificates = read_certificates()
    # Check if certificate already exists
    for cert in certificates.values():
        if cert['username'] == username and cert['course_id'] == course_id:
            return  # Already exists
    certificate_id = get_next_id(certificates)
    issue_date = datetime.now().strftime('%Y-%m-%d')
    certificates[certificate_id] = {
        'certificate_id': certificate_id,
        'username': username,
        'course_id': course_id,
        'issue_date': issue_date
    }
    write_certificates(certificates)
# For simplicity, define lessons per course here (since not specified in data files)
# Each course_id maps to a list of lessons (lesson_id, title, content)
# In a real app, lessons would be stored in a file or DB, but here we hardcode for demo
COURSE_LESSONS = {
    '1': [
        {'lesson_id': '1', 'title': 'Introduction to Python', 'content': 'Welcome to Python programming!'},
        {'lesson_id': '2', 'title': 'Variables and Data Types', 'content': 'Learn about variables and data types.'},
        {'lesson_id': '3', 'title': 'Control Structures', 'content': 'If statements, loops, and more.'},
        {'lesson_id': '4', 'title': 'Functions', 'content': 'Defining and using functions.'},
        {'lesson_id': '5', 'title': 'Modules and Packages', 'content': 'Organizing code with modules.'}
    ],
    '2': [
        {'lesson_id': '1', 'title': 'HTML Basics', 'content': 'Learn the structure of web pages.'},
        {'lesson_id': '2', 'title': 'CSS Styling', 'content': 'Make your pages look great.'},
        {'lesson_id': '3', 'title': 'JavaScript Introduction', 'content': 'Add interactivity to your site.'},
        {'lesson_id': '4', 'title': 'Responsive Design', 'content': 'Make your site mobile-friendly.'}
    ],
    '3': [
        {'lesson_id': '1', 'title': 'Data Science Overview', 'content': 'What is data science?'},
        {'lesson_id': '2', 'title': 'Data Cleaning', 'content': 'Prepare your data for analysis.'},
        {'lesson_id': '3', 'title': 'Data Visualization', 'content': 'Visualize data effectively.'},
        {'lesson_id': '4', 'title': 'Machine Learning Basics', 'content': 'Introduction to ML concepts.'},
        {'lesson_id': '5', 'title': 'Project', 'content': 'Apply what you learned in a project.'}
    ]
}
# To track completed lessons per enrollment, we will store in a separate file or in-memory dictionary
# Since not specified, we will create a file 'lesson_progress.txt' with format:
# enrollment_id|lesson_id1,lesson_id2,...
# This file will track which lessons are completed per enrollment
LESSON_PROGRESS_FILE = os.path.join(DATA_DIR, 'lesson_progress.txt')
def read_lesson_progress():
    progress = {}
    if not os.path.exists(LESSON_PROGRESS_FILE):
        return progress
    with open(LESSON_PROGRESS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                enrollment_id, lessons_str = line.split('|')
                lessons_completed = lessons_str.split(',') if lessons_str else []
                progress[enrollment_id] = lessons_completed
    return progress
def write_lesson_progress(progress):
    with open(LESSON_PROGRESS_FILE, 'w', encoding='utf-8') as f:
        for enrollment_id, lessons_completed in progress.items():
            lessons_str = ','.join(lessons_completed)
            f.write(f"{enrollment_id}|{lessons_str}\n")
def get_completed_lessons(enrollment_id):
    progress = read_lesson_progress()
    return progress.get(enrollment_id, [])
def mark_lesson_complete(enrollment_id, lesson_id):
    progress = read_lesson_progress()
    lessons_completed = progress.get(enrollment_id, [])
    if lesson_id not in lessons_completed:
        lessons_completed.append(lesson_id)
        progress[enrollment_id] = lessons_completed
        write_lesson_progress(progress)
# User login page and session management
@app.before_request
def require_login():
    # Allow static files, login and logout routes without login
    allowed_routes = ['login', 'logout', 'static']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        users = read_users()
        if username in users:
            session['username'] = username
            flash(f'Logged in as {username}.')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username. Please try again.')
            return render_template('login.html')
    else:
        return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out.')
    return redirect(url_for('login'))
# 1. Dashboard Page - route '/'
@app.route('/')
def dashboard():
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('login'))
    fullname = get_user_fullname(username)
    enrollments = read_enrollments()
    courses = read_courses()
    user_enrollments = []
    for enrollment in enrollments.values():
        if enrollment['username'] == username:
            course = courses.get(enrollment['course_id'])
            if course:
                user_enrollments.append({
                    'enrollment_id': enrollment['enrollment_id'],
                    'course_id': course['course_id'],
                    'title': course['title'],
                    'progress': int(enrollment['progress']),
                    'status': enrollment['status']
                })
    return render_template('dashboard.html',
                           fullname=fullname,
                           enrolled_courses=user_enrollments)
# 2. Course Catalog Page
@app.route('/course_catalog', methods=['GET', 'POST'])
def course_catalog():
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('login'))
    courses = read_courses()
    search_query = ''
    filtered_courses = list(courses.values())
    if request.method == 'POST':
        search_query = request.form.get('search-input', '').strip().lower()
        if search_query:
            filtered_courses = [c for c in courses.values() if search_query in c['title'].lower() or search_query in c['description'].lower()]
    return render_template('course_catalog.html',
                           courses=filtered_courses,
                           search_query=search_query)
# 3. Course Details Page
@app.route('/course_details/<course_id>', methods=['GET', 'POST'])
def course_details(course_id):
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('login'))
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        flash('Course not found.')
        return redirect(url_for('course_catalog'))
    enrollment = is_enrolled(username, course_id)
    already_enrolled = enrollment is not None
    if request.method == 'POST':
        if not already_enrolled:
            enrollments = read_enrollments()
            enrollment_id = get_next_id(enrollments)
            enrollment_date = datetime.now().strftime('%Y-%m-%d')
            enrollments[enrollment_id] = {
                'enrollment_id': enrollment_id,
                'username': username,
                'course_id': course_id,
                'enrollment_date': enrollment_date,
                'progress': 0.0,
                'status': 'In Progress'
            }
            write_enrollments(enrollments)
            flash('Enrolled successfully.')
            return redirect(url_for('my_courses'))
        else:
            flash('You are already enrolled in this course.')
    return render_template('course_details.html',
                           course=course,
                           already_enrolled=already_enrolled)
# 4. My Courses Page
@app.route('/my_courses')
def my_courses():
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('login'))
    enrollments = read_enrollments()
    courses = read_courses()
    user_enrollments = []
    for enrollment in enrollments.values():
        if enrollment['username'] == username:
            course = courses.get(enrollment['course_id'])
            if course:
                user_enrollments.append({
                    'enrollment_id': enrollment['enrollment_id'],
                    'course_id': course['course_id'],
                    'title': course['title'],
                    'progress': int(enrollment['progress']),
                    'status': enrollment['status']
                })
    return render_template('my_courses.html',
                           enrolled_courses=user_enrollments)
# 5. Course Learning Page
@app.route('/course_learning/<course_id>', methods=['GET', 'POST'])
def course_learning(course_id):
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('login'))
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        flash('Course not found.')
        return redirect(url_for('my_courses'))
    enrollment = is_enrolled(username, course_id)
    if not enrollment:
        flash('You are not enrolled in this course.')
        return redirect(url_for('my_courses'))
    enrollment_id = enrollment['enrollment_id']
    lessons = COURSE_LESSONS.get(course_id, [])
    if not lessons:
        flash('No lessons found for this course.')
        return redirect(url_for('my_courses'))
    completed_lessons = get_completed_lessons(enrollment_id)
    # Determine current lesson to show: first incomplete lesson in sequence
    current_lesson = None
    for lesson in lessons:
        if lesson['lesson_id'] not in completed_lessons:
            current_lesson = lesson
            break
    if current_lesson is None:
        # All lessons completed
        current_lesson = lessons[-1]
    if request.method == 'POST':
        # Mark current lesson complete
        # Check if user is allowed to mark this lesson complete (must be next in sequence)
        if current_lesson['lesson_id'] in completed_lessons:
            flash('Lesson already completed.')
        else:
            # Check if previous lessons are completed (sequence)
            lesson_index = next((i for i, l in enumerate(lessons) if l['lesson_id'] == current_lesson['lesson_id']), None)
            if lesson_index is None:
                flash('Invalid lesson.')
            else:
                # All previous lessons must be completed
                if lesson_index == 0 or all(lessons[i]['lesson_id'] in completed_lessons for i in range(lesson_index)):
                    mark_lesson_complete(enrollment_id, current_lesson['lesson_id'])
                    # Update progress
                    completed_lessons = get_completed_lessons(enrollment_id)
                    progress = (len(completed_lessons) / len(lessons)) * 100
                    update_enrollment_progress(enrollment_id, progress)
                    if progress >= 100:
                        generate_certificate(username, course_id)
                        flash('Course completed! Certificate generated.')
                    else:
                        flash('Lesson marked as complete.')
                    return redirect(url_for('course_learning', course_id=course_id))
                else:
                    flash('Please complete previous lessons first.')
    # Refresh completed lessons after possible update
    completed_lessons = get_completed_lessons(enrollment_id)
    progress = (len(completed_lessons) / len(lessons)) * 100
    return render_template('course_learning.html',
                           course=course,
                           lessons=lessons,
                           current_lesson=current_lesson,
                           completed_lessons=completed_lessons,
                           progress=int(progress))
# 6. My Assignments Page
@app.route('/my_assignments')
def my_assignments():
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('login'))
    assignments = read_assignments()
    enrollments = read_enrollments()
    user_courses = {e['course_id'] for e in enrollments.values() if e['username'] == username}
    user_assignments = [a for a in assignments.values() if a['course_id'] in user_courses]
    submissions = read_submissions()
    # Map assignment_id to submission for this user
    user_submissions = {}
    for sub in submissions.values():
        if sub['username'] == username:
            user_submissions[sub['assignment_id']] = sub
    # Prepare assignment list with submission status
    assignments_list = []
    for a in user_assignments:
        sub = user_submissions.get(a['assignment_id'])
        status = 'Pending'
        if sub:
            status = 'Submitted'
        assignments_list.append({
            'assignment_id': a['assignment_id'],
            'title': a['title'],
            'description': a['description'],
            'due_date': a['due_date'],
            'max_points': a['max_points'],
            'status': status
        })
    return render_template('my_assignments.html',
                           assignments=assignments_list)
# 7. Submit Assignment Page
@app.route('/submit_assignment/<assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('login'))
    assignments = read_assignments()
    assignment = assignments.get(assignment_id)
    if not assignment:
        flash('Assignment not found.')
        return redirect(url_for('my_assignments'))
    submissions = read_submissions()
    # Check if user already submitted
    for sub in submissions.values():
        if sub['assignment_id'] == assignment_id and sub['username'] == username:
            flash('You have already submitted this assignment.')
            return redirect(url_for('my_assignments'))
    if request.method == 'POST':
        submission_text = request.form.get('submission-text', '').strip()
        if not submission_text:
            flash('Submission text cannot be empty.')
            return render_template('submit_assignment.html', assignment=assignment)
        submission_id = get_next_id(submissions)
        submit_date = datetime.now().strftime('%Y-%m-%d')
        submissions[submission_id] = {
            'submission_id': submission_id,
            'assignment_id': assignment_id,
            'username': username,
            'submission_text': submission_text.replace('\n', ' ').replace('|', ' '),  # sanitize
            'submit_date': submit_date,
            'grade': '',
            'feedback': ''
        }
        write_submissions(submissions)
        flash('Assignment submitted successfully.')
        return redirect(url_for('my_assignments'))
    return render_template('submit_assignment.html', assignment=assignment)
# 8. Certificates Page
@app.route('/certificates')
def certificates():
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('login'))
    certificates = read_certificates()
    courses = read_courses()
    user_certs = []
    for cert in certificates.values():
        if cert['username'] == username:
            course = courses.get(cert['course_id'])
            if course:
                user_certs.append({
                    'certificate_id': cert['certificate_id'],
                    'course_id': course['course_id'],
                    'title': course['title'],
                    'issue_date': cert['issue_date']
                })
    return render_template('certificates.html', certificates=user_certs)
# 9. User Profile Page
@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('login'))
    users = read_users()
    user = users.get(username)
    if not user:
        flash('User not found.')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('profile-email', '').strip()
        fullname = request.form.get('profile-fullname', '').strip()
        if not email or not fullname:
            flash('Email and full name cannot be empty.')
            return render_template('user_profile.html', email=user['email'], fullname=user['fullname'])
        # Update user info
        users[username]['email'] = email
        users[username]['fullname'] = fullname
        write_users(users)
        flash('Profile updated successfully.')
        return redirect(url_for('dashboard'))
    return render_template('user_profile.html', email=user['email'], fullname=user['fullname'])
# Run the app
if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)