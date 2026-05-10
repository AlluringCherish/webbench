'''
Main backend Python file for the OnlineCourse web application.
Implements all routing, session management, and business logic using Flask.
Manages data persistence via local text files in the 'data' directory.
'''
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key in production
DATA_DIR = 'data'
# Utility functions for file operations and data parsing
def read_file_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines
def write_file_lines(filename, lines):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
def append_file_line(filename, line):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(line + '\n')
# Parsing functions for each data type
def parse_users():
    users = {}
    for line in read_file_lines('users.txt'):
        parts = line.split('|')
        if len(parts) == 3:
            username, email, fullname = parts
            users[username] = {'email': email, 'fullname': fullname}
    return users
def parse_courses():
    courses = {}
    for line in read_file_lines('courses.txt'):
        parts = line.split('|')
        if len(parts) == 7:
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
def parse_enrollments():
    enrollments = {}
    for line in read_file_lines('enrollments.txt'):
        parts = line.split('|')
        if len(parts) == 6:
            enrollment_id, username, course_id, enrollment_date, progress, status = parts
            try:
                progress_float = float(progress)
            except ValueError:
                progress_float = 0.0
            enrollments[enrollment_id] = {
                'enrollment_id': enrollment_id,
                'username': username,
                'course_id': course_id,
                'enrollment_date': enrollment_date,
                'progress': progress_float,
                'status': status
            }
    return enrollments
def parse_assignments():
    assignments = {}
    for line in read_file_lines('assignments.txt'):
        parts = line.split('|')
        if len(parts) == 6:
            assignment_id, course_id, title, description, due_date, max_points = parts
            try:
                max_points_int = int(max_points)
            except ValueError:
                max_points_int = 0
            assignments[assignment_id] = {
                'assignment_id': assignment_id,
                'course_id': course_id,
                'title': title,
                'description': description,
                'due_date': due_date,
                'max_points': max_points_int
            }
    return assignments
def parse_submissions():
    submissions = {}
    for line in read_file_lines('submissions.txt'):
        parts = line.split('|')
        if len(parts) == 7:
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
def parse_certificates():
    certificates = {}
    for line in read_file_lines('certificates.txt'):
        parts = line.split('|')
        if len(parts) == 4:
            certificate_id, username, course_id, issue_date = parts
            certificates[certificate_id] = {
                'certificate_id': certificate_id,
                'username': username,
                'course_id': course_id,
                'issue_date': issue_date
            }
    return certificates
# Helper functions for ID generation
def get_next_id(data_dict):
    if not data_dict:
        return '1'
    max_id = max(int(k) for k in data_dict.keys())
    return str(max_id + 1)
# Ensure data directory and essential files exist with default data
def ensure_data_files():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    # users.txt with default example user if missing or empty
    users_path = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(users_path) or os.path.getsize(users_path) == 0:
        default_users = [
            "john|john@student.com|John Student",
            "alice|alice@instructor.com|Alice Professor",
            "jane|jane@student.com|Jane Learner"
        ]
        write_file_lines('users.txt', default_users)
    # courses.txt with example data if missing or empty
    courses_path = os.path.join(DATA_DIR, 'courses.txt')
    if not os.path.exists(courses_path) or os.path.getsize(courses_path) == 0:
        default_courses = [
            "1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active",
            "2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active",
            "3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active"
        ]
        write_file_lines('courses.txt', default_courses)
    # Create empty files if missing for other data files
    for filename in ['enrollments.txt', 'assignments.txt', 'submissions.txt', 'certificates.txt']:
        path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(path):
            open(path, 'w', encoding='utf-8').close()
# User session management (simple login simulation for demo)
@app.before_request
def require_login():
    # For simplicity, simulate a logged-in user "john"
    # In real app, implement proper login/logout
    if 'username' not in session:
        session['username'] = 'john'  # Default user for demo
# Get current user info
def get_current_user():
    username = session.get('username')
    users = parse_users()
    return username, users.get(username)
# ROUTES
# 1. Dashboard Page - route '/'
@app.route('/')
def dashboard():
    username, user = get_current_user()
    if not user:
        flash("User not found.")
        return "User not found", 404
    enrollments = parse_enrollments()
    courses = parse_courses()
    # Filter enrollments for current user
    user_enrollments = [e for e in enrollments.values() if e['username'] == username]
    # Prepare enrolled courses with progress
    enrolled_courses = []
    for e in user_enrollments:
        course = courses.get(e['course_id'])
        if course:
            enrolled_courses.append({
                'course_id': course['course_id'],
                'title': course['title'],
                'progress': e['progress'],
                'status': e['status']
            })
    return render_template('dashboard.html',
                           user_fullname=user['fullname'],
                           enrolled_courses=enrolled_courses)
# 2. Course Catalog Page
@app.route('/catalog', methods=['GET', 'POST'])
def course_catalog():
    username, user = get_current_user()
    if not user:
        flash("User not found.")
        return "User not found", 404
    courses = parse_courses()
    enrollments = parse_enrollments()
    user_enrolled_course_ids = {e['course_id'] for e in enrollments.values() if e['username'] == username}
    search_query = ''
    filtered_courses = list(courses.values())
    if request.method == 'POST':
        search_query = request.form.get('search', '').strip().lower()
        if search_query:
            filtered_courses = [c for c in filtered_courses if search_query in c['title'].lower() or search_query in c['description'].lower()]
    return render_template('course_catalog.html',
                           courses=filtered_courses,
                           user_enrolled_course_ids=user_enrolled_course_ids,
                           search_query=search_query)
# 3. Course Details Page
@app.route('/course/<course_id>', methods=['GET', 'POST'])
def course_details(course_id):
    username, user = get_current_user()
    if not user:
        flash("User not found.")
        return "User not found", 404
    courses = parse_courses()
    course = courses.get(course_id)
    if not course:
        flash("Course not found.")
        return redirect(url_for('course_catalog'))
    enrollments = parse_enrollments()
    # Check if user already enrolled
    already_enrolled = any(e['username'] == username and e['course_id'] == course_id for e in enrollments.values())
    if request.method == 'POST':
        if not already_enrolled:
            # Enroll user
            enrollment_id = get_next_id(enrollments)
            enrollment_date = datetime.now().strftime('%Y-%m-%d')
            new_enrollment_line = f"{enrollment_id}|{username}|{course_id}|{enrollment_date}|0|In Progress"
            append_file_line('enrollments.txt', new_enrollment_line)
            flash("Successfully enrolled in the course.")
            return redirect(url_for('my_courses'))
        else:
            flash("You are already enrolled in this course.")
    return render_template('course_details.html',
                           course=course,
                           already_enrolled=already_enrolled)
# 4. My Courses Page
@app.route('/my-courses')
def my_courses():
    username, user = get_current_user()
    if not user:
        flash("User not found.")
        return "User not found", 404
    enrollments = parse_enrollments()
    courses = parse_courses()
    user_enrollments = [e for e in enrollments.values() if e['username'] == username]
    courses_list = []
    for e in user_enrollments:
        course = courses.get(e['course_id'])
        if course:
            courses_list.append({
                'course_id': course['course_id'],
                'title': course['title'],
                'progress': e['progress'],
                'status': e['status']
            })
    return render_template('my_courses.html',
                           courses_list=courses_list)
# 5. Course Learning Page
@app.route('/learning/<course_id>', methods=['GET', 'POST'])
def course_learning(course_id):
    username, user = get_current_user()
    if not user:
        flash("User not found.")
        return "User not found", 404
    courses = parse_courses()
    course = courses.get(course_id)
    if not course:
        flash("Course not found.")
        return redirect(url_for('my_courses'))
    enrollments = parse_enrollments()
    enrollment = None
    for e in enrollments.values():
        if e['username'] == username and e['course_id'] == course_id:
            enrollment = e
            break
    if not enrollment:
        flash("You are not enrolled in this course.")
        return redirect(url_for('my_courses'))
    # For simplicity, simulate lessons as numbered lessons equal to duration in hours / 10 rounded down
    try:
        duration_hours = int(course['duration'].split()[0])
    except Exception:
        duration_hours = 40  # default fallback
    total_lessons = max(1, duration_hours // 10)
    # Track completed lessons count from progress
    completed_lessons = int(round(enrollment['progress'] * total_lessons / 100))
    # Current lesson index (0-based)
    current_lesson_index = completed_lessons
    # If POST and mark complete pressed
    if request.method == 'POST':
        # Mark current lesson complete only if it is the next in sequence
        if current_lesson_index < total_lessons:
            completed_lessons += 1
            progress = (completed_lessons / total_lessons) * 100
            progress = round(progress, 2)
            # Update enrollment progress and status
            enrollment['progress'] = progress
            if progress >= 100:
                enrollment['progress'] = 100.0
                enrollment['status'] = 'Completed'
                # Generate certificate if not exists
                generate_certificate(username, course_id)
            else:
                enrollment['status'] = 'In Progress'
            # Save updated enrollments
            update_enrollment(enrollment)
            flash(f"Lesson {completed_lessons} marked as completed.")
            return redirect(url_for('course_learning', course_id=course_id))
        else:
            flash("All lessons already completed.")
    # Prepare lessons list
    lessons_list = []
    for i in range(total_lessons):
        lessons_list.append({
            'lesson_number': i + 1,
            'completed': i < completed_lessons
        })
    # Current lesson content (dummy content)
    lesson_content = f"Content for Lesson {current_lesson_index + 1} of {total_lessons} in {course['title']}."
    return render_template('course_learning.html',
                           course=course,
                           lessons_list=lessons_list,
                           lesson_content=lesson_content,
                           current_lesson_index=current_lesson_index,
                           total_lessons=total_lessons,
                           enrollment=enrollment)
def update_enrollment(updated_enrollment):
    enrollments = parse_enrollments()
    enrollments[updated_enrollment['enrollment_id']] = updated_enrollment
    lines = []
    for e in enrollments.values():
        line = f"{e['enrollment_id']}|{e['username']}|{e['course_id']}|{e['enrollment_date']}|{e['progress']}|{e['status']}"
        lines.append(line)
    write_file_lines('enrollments.txt', lines)
def generate_certificate(username, course_id):
    certificates = parse_certificates()
    # Check if certificate already exists
    for cert in certificates.values():
        if cert['username'] == username and cert['course_id'] == course_id:
            return  # Already exists
    certificate_id = get_next_id(certificates)
    issue_date = datetime.now().strftime('%Y-%m-%d')
    new_cert_line = f"{certificate_id}|{username}|{course_id}|{issue_date}"
    append_file_line('certificates.txt', new_cert_line)
# 6. My Assignments Page
@app.route('/assignments')
def my_assignments():
    username, user = get_current_user()
    if not user:
        flash("User not found.")
        return "User not found", 404
    assignments = parse_assignments()
    enrollments = parse_enrollments()
    submissions = parse_submissions()
    # Get user's enrolled course IDs
    user_course_ids = {e['course_id'] for e in enrollments.values() if e['username'] == username}
    # Filter assignments for user's courses
    user_assignments = [a for a in assignments.values() if a['course_id'] in user_course_ids]
    # Map assignment_id to submission for this user (if any)
    user_submissions = {s['assignment_id']: s for s in submissions.values() if s['username'] == username}
    # Prepare assignments data with submission status
    assignments_data = []
    for a in user_assignments:
        submission = user_submissions.get(a['assignment_id'])
        status = 'Pending'
        if submission:
            status = 'Submitted'
        assignments_data.append({
            'assignment_id': a['assignment_id'],
            'title': a['title'],
            'description': a['description'],
            'due_date': a['due_date'],
            'max_points': a['max_points'],
            'status': status
        })
    return render_template('my_assignments.html',
                           assignments=assignments_data)
# 7. Submit Assignment Page
@app.route('/submit-assignment/<assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    username, user = get_current_user()
    if not user:
        flash("User not found.")
        return "User not found", 404
    assignments = parse_assignments()
    assignment = assignments.get(assignment_id)
    if not assignment:
        flash("Assignment not found.")
        return redirect(url_for('my_assignments'))
    submissions = parse_submissions()
    # Check if user already submitted
    for s in submissions.values():
        if s['assignment_id'] == assignment_id and s['username'] == username:
            flash("You have already submitted this assignment.")
            return redirect(url_for('my_assignments'))
    if request.method == 'POST':
        submission_text = request.form.get('submission-text', '').strip()
        if not submission_text:
            flash("Submission text cannot be empty.")
            return render_template('submit_assignment.html', assignment=assignment)
        submission_id = get_next_id(submissions)
        submit_date = datetime.now().strftime('%Y-%m-%d')
        # Grade and feedback empty initially
        new_submission_line = f"{submission_id}|{assignment_id}|{username}|{submission_text}|{submit_date}||"
        append_file_line('submissions.txt', new_submission_line)
        flash("Assignment submitted successfully.")
        return redirect(url_for('my_assignments'))
    return render_template('submit_assignment.html', assignment=assignment)
# 8. Certificates Page
@app.route('/certificates')
def certificates():
    username, user = get_current_user()
    if not user:
        flash("User not found.")
        return "User not found", 404
    certificates = parse_certificates()
    courses = parse_courses()
    user_certificates = [c for c in certificates.values() if c['username'] == username]
    certificates_data = []
    for c in user_certificates:
        course = courses.get(c['course_id'])
        if course:
            certificates_data.append({
                'certificate_id': c['certificate_id'],
                'course_title': course['title'],
                'issue_date': c['issue_date']
            })
    return render_template('certificates.html',
                           certificates=certificates_data)
# 9. User Profile Page
@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    username, user = get_current_user()
    if not user:
        flash("User not found.")
        return "User not found", 404
    users = parse_users()
    if request.method == 'POST':
        email = request.form.get('profile-email', '').strip()
        fullname = request.form.get('profile-fullname', '').strip()
        if not email or not fullname:
            flash("Email and Full name cannot be empty.")
            return render_template('user_profile.html', user=user)
        # Update user info
        users[username]['email'] = email
        users[username]['fullname'] = fullname
        # Write back all users
        lines = []
        for uname, udata in users.items():
            line = f"{uname}|{udata['email']}|{udata['fullname']}"
            lines.append(line)
        write_file_lines('users.txt', lines)
        flash("Profile updated successfully.")
        # Update session user info
        user['email'] = email
        user['fullname'] = fullname
    return render_template('user_profile.html', user=user)
# Run the app on local port 5000
if __name__ == '__main__':
    # Ensure data directory and essential files exist with default data
    ensure_data_files()
    app.run(host='0.0.0.0', port=5000, debug=True)