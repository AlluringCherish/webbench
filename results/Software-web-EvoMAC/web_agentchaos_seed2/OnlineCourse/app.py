'''
Flask backend for OnlineCourse web application.
Defines all routes corresponding to the 9 pages as per requirements.
Root route '/' serves the Dashboard page.
All routes use URL parameters where needed.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
def read_users():
    users = {}
    with open(os.path.join(DATA_DIR, 'users.txt'), 'r') as f:
        for line in f:
            username, email, fullname = line.strip().split('|')
            users[username] = {'email': email, 'fullname': fullname}
    return users
def read_courses():
    courses = {}
    with open(os.path.join(DATA_DIR, 'courses.txt'), 'r') as f:
        for line in f:
            course_id, title, description, category, level, duration, status = line.strip().split('|')
            courses[int(course_id)] = {
                'title': title,
                'description': description,
                'category': category,
                'level': level,
                'duration': duration,
                'status': status
            }
    return courses
def read_enrollments():
    enrollments = []
    with open(os.path.join(DATA_DIR, 'enrollments.txt'), 'r') as f:
        for line in f:
            enrollment_id, username, course_id, enrollment_date, progress, status = line.strip().split('|')
            enrollments.append({
                'enrollment_id': int(enrollment_id),
                'username': username,
                'course_id': int(course_id),
                'enrollment_date': enrollment_date,
                'progress': float(progress),
                'status': status
            })
    return enrollments
def read_assignments():
    assignments = []
    with open(os.path.join(DATA_DIR, 'assignments.txt'), 'r') as f:
        for line in f:
            assignment_id, course_id, title, description, due_date, max_points = line.strip().split('|')
            assignments.append({
                'assignment_id': int(assignment_id),
                'course_id': int(course_id),
                'title': title,
                'description': description,
                'due_date': due_date,
                'max_points': int(max_points)
            })
    return assignments
def read_submissions():
    submissions = []
    with open(os.path.join(DATA_DIR, 'submissions.txt'), 'r') as f:
        for line in f:
            submission_id, assignment_id, username, submission_text, submit_date, grade, feedback = line.strip().split('|')
            submissions.append({
                'submission_id': int(submission_id),
                'assignment_id': int(assignment_id),
                'username': username,
                'submission_text': submission_text,
                'submit_date': submit_date,
                'grade': grade,
                'feedback': feedback
            })
    return submissions
def read_certificates():
    certificates = []
    with open(os.path.join(DATA_DIR, 'certificates.txt'), 'r') as f:
        for line in f:
            certificate_id, username, course_id, issue_date = line.strip().split('|')
            certificates.append({
                'certificate_id': int(certificate_id),
                'username': username,
                'course_id': int(course_id),
                'issue_date': issue_date
            })
    return certificates
def write_enrollments(enrollments):
    with open(os.path.join(DATA_DIR, 'enrollments.txt'), 'w') as f:
        for e in enrollments:
            line = f"{e['enrollment_id']}|{e['username']}|{e['course_id']}|{e['enrollment_date']}|{int(e['progress'])}|{e['status']}\n"
            f.write(line)
def write_submissions(submissions):
    with open(os.path.join(DATA_DIR, 'submissions.txt'), 'w') as f:
        for s in submissions:
            # Escape newlines and pipes in submission_text to avoid file format issues
            safe_text = s['submission_text'].replace('\n', '\\n').replace('|', '&#124;')
            line = f"{s['submission_id']}|{s['assignment_id']}|{s['username']}|{safe_text}|{s['submit_date']}|{s['grade']}|{s['feedback']}\n"
            f.write(line)
def write_certificates(certificates):
    with open(os.path.join(DATA_DIR, 'certificates.txt'), 'w') as f:
        for c in certificates:
            line = f"{c['certificate_id']}|{c['username']}|{c['course_id']}|{c['issue_date']}\n"
            f.write(line)
def write_users(users):
    with open(os.path.join(DATA_DIR, 'users.txt'), 'w') as f:
        for username, data in users.items():
            line = f"{username}|{data['email']}|{data['fullname']}\n"
            f.write(line)
# For simplicity, assume logged-in user is 'john'
CURRENT_USER = 'john'
@app.route('/')
def dashboard():
    users = read_users()
    enrollments = read_enrollments()
    courses = read_courses()
    user = users.get(CURRENT_USER)
    user_enrollments = [e for e in enrollments if e['username'] == CURRENT_USER]
    enrolled_courses = []
    for e in user_enrollments:
        course = courses.get(e['course_id'])
        if course:
            enrolled_courses.append({
                'course_id': e['course_id'],
                'title': course['title'],
                'progress': e['progress'],
                'status': e['status']
            })
    return render_template('dashboard.html', fullname=user['fullname'], enrolled_courses=enrolled_courses)
@app.route('/catalog')
def course_catalog():
    courses = read_courses()
    # Only active courses
    active_courses = {cid: c for cid, c in courses.items() if c['status'] == 'Active'}
    return render_template('catalog.html', courses=active_courses)
@app.route('/course/<int:course_id>')
def course_details(course_id):
    courses = read_courses()
    enrollments = read_enrollments()
    course = courses.get(course_id)
    if not course:
        return "Course not found", 404
    # Check if user already enrolled
    enrolled = any(e for e in enrollments if e['username'] == CURRENT_USER and e['course_id'] == course_id)
    return render_template('course_details.html', course=course, course_id=course_id, enrolled=enrolled)
@app.route('/enroll/<int:course_id>', methods=['POST'])
def enroll_course(course_id):
    enrollments = read_enrollments()
    # Check if already enrolled
    for e in enrollments:
        if e['username'] == CURRENT_USER and e['course_id'] == course_id:
            return redirect(url_for('course_details', course_id=course_id))
    new_id = max([e['enrollment_id'] for e in enrollments], default=0) + 1
    today = datetime.now().strftime('%Y-%m-%d')
    enrollments.append({
        'enrollment_id': new_id,
        'username': CURRENT_USER,
        'course_id': course_id,
        'enrollment_date': today,
        'progress': 0,
        'status': 'In Progress'
    })
    write_enrollments(enrollments)
    return redirect(url_for('my_courses'))
@app.route('/my-courses')
def my_courses():
    users = read_users()
    enrollments = read_enrollments()
    courses = read_courses()
    user = users.get(CURRENT_USER)
    user_enrollments = [e for e in enrollments if e['username'] == CURRENT_USER]
    enrolled_courses = []
    for e in user_enrollments:
        course = courses.get(e['course_id'])
        if course:
            enrolled_courses.append({
                'course_id': e['course_id'],
                'title': course['title'],
                'progress': e['progress'],
                'status': e['status']
            })
    return render_template('my_courses.html', enrolled_courses=enrolled_courses, fullname=user['fullname'])
@app.route('/learn/<int:course_id>')
def course_learning(course_id):
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        return "Course not found", 404
    # For demo, define lessons as list of strings
    lessons = [
        "Introduction",
        "Lesson 1: Basics",
        "Lesson 2: Intermediate",
        "Lesson 3: Advanced",
        "Conclusion"
    ]
    enrollments = read_enrollments()
    enrollment = next((e for e in enrollments if e['username'] == CURRENT_USER and e['course_id'] == course_id), None)
    if not enrollment:
        return redirect(url_for('course_details', course_id=course_id))
    # Calculate completed lessons count from progress
    total_lessons = len(lessons)
    completed_lessons = int(enrollment['progress'] * total_lessons / 100)
    current_lesson_index = completed_lessons if completed_lessons < total_lessons else total_lessons - 1
    current_lesson = lessons[current_lesson_index]
    return render_template('course_learning.html',
                           course=course,
                           course_id=course_id,
                           lessons=lessons,
                           current_lesson_index=current_lesson_index,
                           current_lesson=current_lesson,
                           progress=enrollment['progress'])
@app.route('/mark-complete/<int:course_id>', methods=['POST'])
def mark_complete(course_id):
    enrollments = read_enrollments()
    enrollment = next((e for e in enrollments if e['username'] == CURRENT_USER and e['course_id'] == course_id), None)
    if not enrollment:
        return redirect(url_for('course_details', course_id=course_id))
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        return "Course not found", 404
    # For demo, lessons count fixed
    lessons = [
        "Introduction",
        "Lesson 1: Basics",
        "Lesson 2: Intermediate",
        "Lesson 3: Advanced",
        "Conclusion"
    ]
    total_lessons = len(lessons)
    completed_lessons = int(enrollment['progress'] * total_lessons / 100)
    # Lessons must be completed in sequence
    if completed_lessons < total_lessons:
        completed_lessons += 1
        new_progress = (completed_lessons / total_lessons) * 100
        enrollment['progress'] = new_progress
        if new_progress >= 100:
            enrollment['progress'] = 100
            enrollment['status'] = 'Completed'
            # Generate certificate
            certificates = read_certificates()
            existing_cert = next((c for c in certificates if c['username'] == CURRENT_USER and c['course_id'] == course_id), None)
            if not existing_cert:
                new_cert_id = max([c['certificate_id'] for c in certificates], default=0) + 1
                today = datetime.now().strftime('%Y-%m-%d')
                certificates.append({
                    'certificate_id': new_cert_id,
                    'username': CURRENT_USER,
                    'course_id': course_id,
                    'issue_date': today
                })
                write_certificates(certificates)
        write_enrollments(enrollments)
    return redirect(url_for('course_learning', course_id=course_id))
@app.route('/assignments')
def my_assignments():
    assignments = read_assignments()
    submissions = read_submissions()
    enrollments = read_enrollments()
    # Get courses user enrolled in
    user_enrollments = [e for e in enrollments if e['username'] == CURRENT_USER]
    enrolled_course_ids = {e['course_id'] for e in user_enrollments}
    # Filter assignments for enrolled courses
    user_assignments = [a for a in assignments if a['course_id'] in enrolled_course_ids]
    # Map assignment_id to submission for current user
    user_submissions = {s['assignment_id']: s for s in submissions if s['username'] == CURRENT_USER}
    return render_template('assignments.html', assignments=user_assignments, submissions=user_submissions)
@app.route('/submit-assignment/<int:assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    assignments = read_assignments()
    assignment = next((a for a in assignments if a['assignment_id'] == assignment_id), None)
    if not assignment:
        return "Assignment not found", 404
    submissions = read_submissions()
    if request.method == 'POST':
        submission_text = request.form.get('submission-text', '').strip()
        if not submission_text:
            return render_template('submit_assignment.html', assignment=assignment, error="Submission text cannot be empty.")
        new_id = max([s['submission_id'] for s in submissions], default=0) + 1
        today = datetime.now().strftime('%Y-%m-%d')
        submissions.append({
            'submission_id': new_id,
            'assignment_id': assignment_id,
            'username': CURRENT_USER,
            'submission_text': submission_text,
            'submit_date': today,
            'grade': '',
            'feedback': ''
        })
        write_submissions(submissions)
        return render_template('submit_assignment.html', assignment=assignment, success="Submission successful.")
    return render_template('submit_assignment.html', assignment=assignment)
@app.route('/certificates')
def certificates():
    certificates = read_certificates()
    courses = read_courses()
    user_certs = [c for c in certificates if c['username'] == CURRENT_USER]
    certs_with_course = []
    for c in user_certs:
        course = courses.get(c['course_id'])
        if course:
            certs_with_course.append({
                'certificate_id': c['certificate_id'],
                'course_id': c['course_id'],
                'course_title': course['title'],
                'issue_date': c['issue_date']
            })
    return render_template('certificates.html', certificates=certs_with_course)
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = read_users()
    user = users.get(CURRENT_USER)
    if request.method == 'POST':
        email = request.form.get('profile-email', '').strip()
        fullname = request.form.get('profile-fullname', '').strip()
        if email and fullname:
            users[CURRENT_USER]['email'] = email
            users[CURRENT_USER]['fullname'] = fullname
            write_users(users)
            user = users.get(CURRENT_USER)
            return render_template('profile.html', user=user, success="Profile updated successfully.")
        else:
            return render_template('profile.html', user=user, error="Email and Full name cannot be empty.")
    return render_template('profile.html', user=user)
if __name__ == '__main__':
    app.run(debug=True)