from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'some_secret_key_for_sessions'

DATA_DIR = 'data'

# Helper functions to read/write data files

def read_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines


def write_data(filename, lines):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


def get_next_id(lines):
    max_id = 0
    for line in lines:
        parts = line.split('|')
        try:
            id_val = int(parts[0])
            if id_val > max_id:
                max_id = id_val
        except:
            continue
    return max_id + 1

# Get user info (for demo, assume single user 'john')
def get_current_user():
    users = read_data('users.txt')
    for user in users:
        username, email, fullname = user.split('|')
        if username == 'john':
            return {'username': username, 'email': email, 'fullname': fullname}
    # Fallback user
    return {'username': 'john', 'email': 'john@student.com', 'fullname': 'John Student'}

# Get all courses

def get_all_courses():
    courses = read_data('courses.txt')
    course_list = []
    for c in courses:
        parts = c.split('|')
        if len(parts) >= 7:
            course_id, title, description, category, level, duration, status = parts
            if status == 'Active':
                course_list.append({
                    'course_id': course_id,
                    'title': title,
                    'description': description,
                    'category': category,
                    'level': level,
                    'duration': duration,
                    'status': status
                })
    return course_list

# Get course by ID

def get_course_by_id(course_id):
    courses = get_all_courses()
    for c in courses:
        if c['course_id'] == str(course_id):
            return c
    return None

# Get enrollments for user

def get_enrollments(username):
    lines = read_data('enrollments.txt')
    enrollments = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < 6:
            continue
        enrollment_id, usern, course_id, enroll_date, progress, status = parts
        if usern == username:
            enrollments.append({
                'enrollment_id': int(enrollment_id),
                'username': usern,
                'course_id': course_id,
                'enrollment_date': enroll_date,
                'progress': int(progress),
                'status': status
            })
    return enrollments

# Get enrollment by username and course_id

def get_enrollment(username, course_id):
    enrollments = get_enrollments(username)
    for e in enrollments:
        if e['course_id'] == str(course_id):
            return e
    return None

# Save or update enrollment

def save_or_update_enrollment(enrollment):
    lines = read_data('enrollments.txt')
    updated = False
    new_lines = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < 6:
            continue
        enrollment_id, usern, course_id, enroll_date, progress, status = parts
        if int(enrollment_id) == enrollment['enrollment_id']:
            new_line = f"{enrollment['enrollment_id']}|{enrollment['username']}|{enrollment['course_id']}|{enrollment['enrollment_date']}|{enrollment['progress']}|{enrollment['status']}"
            new_lines.append(new_line)
            updated = True
        else:
            new_lines.append(line)
    if not updated:
        # add new
        new_line = f"{enrollment['enrollment_id']}|{enrollment['username']}|{enrollment['course_id']}|{enrollment['enrollment_date']}|{enrollment['progress']}|{enrollment['status']}"
        new_lines.append(new_line)
    write_data('enrollments.txt', new_lines)

# Get assignments by username (from enrolled courses)

def get_assignments(username):
    enrollments = get_enrollments(username)
    enrolled_course_ids = {e['course_id'] for e in enrollments}
    assignment_lines = read_data('assignments.txt')
    assignments = []
    for line in assignment_lines:
        parts = line.split('|')
        if len(parts) < 6:
            continue
        assignment_id, course_id, title, description, due_date, max_points = parts
        if course_id in enrolled_course_ids:
            assignments.append({
                'assignment_id': assignment_id,
                'course_id': course_id,
                'title': title,
                'description': description,
                'due_date': due_date,
                'max_points': max_points
            })
    return assignments

# Get submissions by username

def get_submissions(username):
    lines = read_data('submissions.txt')
    submissions = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < 7:
            continue
        submission_id, assignment_id, usern, submission_text, submit_date, grade, feedback = parts
        if usern == username:
            submissions.append({
                'submission_id': submission_id,
                'assignment_id': assignment_id,
                'username': usern,
                'submission_text': submission_text,
                'submit_date': submit_date,
                'grade': grade,
                'feedback': feedback
            })
    return submissions

# Add new submission

def add_submission(assignment_id, username, submission_text):
    lines = read_data('submissions.txt')
    submission_id = get_next_id(lines)
    submit_date = datetime.now().strftime('%Y-%m-%d')
    grade = ''
    feedback = ''
    new_line = f"{submission_id}|{assignment_id}|{username}|{submission_text}|{submit_date}|{grade}|{feedback}"
    lines.append(new_line)
    write_data('submissions.txt', lines)

# Get certificates for user

def get_certificates(username):
    lines = read_data('certificates.txt')
    certs = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < 4:
            continue
        certificate_id, usern, course_id, issue_date = parts
        if usern == username:
            certs.append({
                'certificate_id': certificate_id,
                'username': usern,
                'course_id': course_id,
                'issue_date': issue_date
            })
    return certs

# Add certificate

def add_certificate(username, course_id):
    lines = read_data('certificates.txt')
    certificate_id = get_next_id(lines)
    issue_date = datetime.now().strftime('%Y-%m-%d')
    new_line = f"{certificate_id}|{username}|{course_id}|{issue_date}"
    lines.append(new_line)
    write_data('certificates.txt', lines)

# Update user profile

def update_user_profile(username, email, fullname):
    lines = read_data('users.txt')
    new_lines = []
    updated = False
    for line in lines:
        parts = line.split('|')
        if len(parts) < 3:
            continue
        uname, uemail, ufullname = parts
        if uname == username:
            new_lines.append(f"{username}|{email}|{fullname}")
            updated = True
        else:
            new_lines.append(line)
    if not updated:
        new_lines.append(f"{username}|{email}|{fullname}")
    write_data('users.txt', new_lines)

# Lessons data hardcoded for course learning page
# For simplicity, lessons are fixed per course
LESSONS = {
    '1': [
        {'lesson_id': '1', 'title': 'Introduction', 'content': 'Welcome to Python Programming!'},
        {'lesson_id': '2', 'title': 'Variables and Data Types', 'content': 'Learn about variables, integers, strings, etc.'},
        {'lesson_id': '3', 'title': 'Control Flow', 'content': 'If statements, loops, and more.'}
    ],
    '2': [
        {'lesson_id': '1', 'title': 'HTML Basics', 'content': 'Learn HTML structure and tags.'},
        {'lesson_id': '2', 'title': 'CSS Styling', 'content': 'Style your pages with CSS.'},
        {'lesson_id': '3', 'title': 'JavaScript Introduction', 'content': 'Get started with JavaScript.'}
    ],
    '3': [
        {'lesson_id': '1', 'title': 'Data Science Overview', 'content': 'What is Data Science? Introduction.'},
        {'lesson_id': '2', 'title': 'Data Analysis Tools', 'content': 'Learn about pandas, numpy, and more.'},
        {'lesson_id': '3', 'title': 'Machine Learning Basics', 'content': 'Intro to ML concepts.'}
    ]
}

# Check if certificate exists for user & course

def certificate_exists(username, course_id):
    certs = get_certificates(username)
    for cert in certs:
        if cert['course_id'] == str(course_id):
            return True
    return False

# Route: Dashboard
@app.route('/')
def dashboard():
    user = get_current_user()
    enrollments = get_enrollments(user['username'])
    courses = []
    for e in enrollments:
        course = get_course_by_id(e['course_id'])
        if course:
            course_copy = course.copy()
            course_copy['progress'] = e['progress']
            courses.append(course_copy)
    return render_template('dashboard.html', user=user, courses=courses)

# Route: Course Catalog
@app.route('/catalog')
def course_catalog():
    user = get_current_user()
    courses = get_all_courses()
    return render_template('catalog.html', user=user, courses=courses)

# Route: Course Details
@app.route('/course/<int:course_id>', methods=['GET', 'POST'])
def course_details(course_id):
    user = get_current_user()
    course = get_course_by_id(course_id)
    if not course:
        flash('Course not found.')
        return redirect(url_for('course_catalog'))
    enrollment = get_enrollment(user['username'], str(course_id))

    if request.method == 'POST':
        # Enroll action
        if enrollment is None:
            enrollments = read_data('enrollments.txt')
            enrollment_id = get_next_id(enrollments)
            enroll_date = datetime.now().strftime('%Y-%m-%d')
            new_enrollment = {
                'enrollment_id': enrollment_id,
                'username': user['username'],
                'course_id': str(course_id),
                'enrollment_date': enroll_date,
                'progress': 0,
                'status': 'In Progress'
            }
            save_or_update_enrollment(new_enrollment)
            flash('Enrollment successful!')
            return redirect(url_for('course_details', course_id=course_id))

    return render_template('course_details.html', user=user, course=course, enrollment=enrollment)

# Route: My Courses
@app.route('/my_courses')
def my_courses():
    user = get_current_user()
    enrollments = get_enrollments(user['username'])
    courses = []
    for e in enrollments:
        course = get_course_by_id(e['course_id'])
        if course:
            course_copy = course.copy()
            course_copy['progress'] = e['progress']
            courses.append(course_copy)
    return render_template('my_courses.html', user=user, courses=courses)

# Route: Course Learning
@app.route('/learn/<int:course_id>', methods=['GET', 'POST'])
def course_learning(course_id):
    user = get_current_user()
    course = get_course_by_id(course_id)
    if not course:
        flash('Course not found.')
        return redirect(url_for('my_courses'))
    enrollment = get_enrollment(user['username'], str(course_id))
    if not enrollment:
        flash('You are not enrolled in this course.')
        return redirect(url_for('my_courses'))

    lessons = LESSONS.get(str(course_id), [])
    total_lessons = len(lessons)

    # Determine completed lessons count from progress
    completed_lessons = int(round(enrollment['progress'] * total_lessons / 100))

    # Get current lesson index from query parameter or default
    lesson_index = int(request.args.get('lesson', completed_lessons))
    if lesson_index >= total_lessons:
        lesson_index = total_lessons - 1

    current_lesson = lessons[lesson_index] if lessons else None

    if request.method == 'POST':
        # Mark complete action
        # Can only mark complete if prior lessons completed
        if lesson_index == completed_lessons:
            completed_lessons += 1
            progress = int(round(completed_lessons / total_lessons * 100))
            enrollment['progress'] = progress
            if progress >= 100:
                enrollment['progress'] = 100
                enrollment['status'] = 'Completed'
                # Generate certificate if not exists
                if not certificate_exists(user['username'], str(course_id)):
                    add_certificate(user['username'], str(course_id))
                    flash('Congratulations! You have completed the course and earned a certificate.')
            save_or_update_enrollment(enrollment)
            flash('Lesson marked as complete.')
            # Move to next lesson if any
            if completed_lessons < total_lessons:
                return redirect(url_for('course_learning', course_id=course_id, lesson=completed_lessons))
            else:
                return redirect(url_for('my_courses'))
        else:
            flash('Please complete previous lessons first.')

    return render_template('course_learning.html', user=user, course=course, lessons=lessons, current_lesson=current_lesson, lesson_index=lesson_index, total_lessons=total_lessons, progress=enrollment['progress'])

# Route: My Assignments
@app.route('/assignments')
def my_assignments():
    user = get_current_user()
    assignments = get_assignments(user['username'])
    submissions = get_submissions(user['username'])
    submitted_assignment_ids = {s['assignment_id'] for s in submissions}
    # Mark assignments with submission status
    for assignment in assignments:
        assignment['submitted'] = assignment['assignment_id'] in submitted_assignment_ids
    return render_template('assignments.html', user=user, assignments=assignments)

# Route: Submit Assignment
@app.route('/submit_assignment/<int:assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    user = get_current_user()
    assignments = get_assignments(user['username'])
    assignment = None
    for a in assignments:
        if int(a['assignment_id']) == assignment_id:
            assignment = a
            break
    if not assignment:
        flash('Assignment not found or not available.')
        return redirect(url_for('my_assignments'))

    if request.method == 'POST':
        submission_text = request.form.get('submission_text', '').strip()
        if submission_text == '':
            flash('Submission text cannot be empty.')
        else:
            add_submission(str(assignment_id), user['username'], submission_text)
            flash('Assignment submitted successfully!')
            return redirect(url_for('my_assignments'))

    return render_template('submit_assignment.html', user=user, assignment=assignment)

# Route: Certificates
@app.route('/certificates')
def certificates():
    user = get_current_user()
    certs = get_certificates(user['username'])
    courses = get_all_courses()
    courses_dict = {c['course_id']: c for c in courses}
    certs_with_course = []
    for c in certs:
        course = courses_dict.get(c['course_id'], None)
        if course:
            certs_with_course.append({
                'certificate_id': c['certificate_id'],
                'course_id': c['course_id'],
                'course_title': course['title'],
                'issue_date': c['issue_date']
            })
    return render_template('certificates.html', user=user, certificates=certs_with_course)

# Route: Profile
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = get_current_user()
    if request.method == 'POST':
        email = request.form.get('profile_email', '').strip()
        fullname = request.form.get('profile_fullname', '').strip()
        if email == '' or fullname == '':
            flash('All fields are required.')
        else:
            update_user_profile(user['username'], email, fullname)
            flash('Profile updated successfully.')
            return redirect(url_for('profile'))
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)
