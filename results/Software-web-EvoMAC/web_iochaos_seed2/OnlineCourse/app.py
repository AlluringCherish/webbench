'''
Main backend Python application for the OnlineCourse web application.
Implements routing, session management, data processing, and business logic
for all nine pages using local text files in the 'data' directory.
'''
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management
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
        for username, data in users.items():
            f.write(f"{username}|{data['email']}|{data['fullname']}\n")
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
        for eid, data in enrollments.items():
            f.write(f"{eid}|{data['username']}|{data['course_id']}|{data['enrollment_date']}|{int(data['progress'])}|{data['status']}\n")
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
        for sid, data in submissions.items():
            f.write(f"{sid}|{data['assignment_id']}|{data['username']}|{data['submission_text']}|{data['submit_date']}|{data['grade']}|{data['feedback']}\n")
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
                        'username': parts[1],
                        'course_id': parts[2],
                        'issue_date': parts[3]
                    }
    return certificates
def write_certificates(certificates):
    path = os.path.join(DATA_DIR, 'certificates.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for cid, data in certificates.items():
            f.write(f"{cid}|{data['username']}|{data['course_id']}|{data['issue_date']}\n")
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
    for e in enrollments.values():
        if e['username'] == username and e['course_id'] == course_id:
            return True
    return False
def get_enrollment(username, course_id):
    enrollments = read_enrollments()
    for eid, e in enrollments.items():
        if e['username'] == username and e['course_id'] == course_id:
            return eid, e
    return None, None
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
        'username': username,
        'course_id': course_id,
        'issue_date': issue_date
    }
    write_certificates(certificates)
def get_user_enrollments(username):
    enrollments = read_enrollments()
    user_enrollments = {}
    for eid, e in enrollments.items():
        if e['username'] == username:
            user_enrollments[eid] = e
    return user_enrollments
def get_course_lessons(course_id):
    # Since lessons are not defined in data files, we simulate lessons as numbered lessons
    # For demonstration, assume each course has 5 lessons titled "Lesson 1" to "Lesson 5"
    lessons = []
    for i in range(1, 6):
        lessons.append({
            'lesson_number': i,
            'title': f'Lesson {i}',
            'content': f'Content for Lesson {i} of course {course_id}.'
        })
    return lessons
def get_completed_lessons(username, course_id):
    # We will store completed lessons in a separate file or in enrollments progress only?
    # The requirements do not specify a file for lessons completion.
    # We will store completed lessons in a file named 'lesson_progress.txt' with format:
    # enrollment_id|lesson_number
    # For simplicity, we implement this file here.
    lesson_progress = {}
    path = os.path.join(DATA_DIR, 'lesson_progress.txt')
    if not os.path.exists(path):
        return set()
    enrollment_id, _ = get_enrollment(username, course_id)
    if not enrollment_id:
        return set()
    completed = set()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                eid, lesson_num = line.split('|')
                if eid == enrollment_id:
                    completed.add(int(lesson_num))
    return completed
def mark_lesson_complete(username, course_id, lesson_number):
    enrollment_id, enrollment = get_enrollment(username, course_id)
    if not enrollment_id:
        return False
    lessons = get_course_lessons(course_id)
    total_lessons = len(lessons)
    completed_lessons = get_completed_lessons(username, course_id)
    # Lessons must be completed in sequence
    if lesson_number > 1 and (lesson_number - 1) not in completed_lessons:
        return False  # Cannot complete this lesson before previous
    if lesson_number in completed_lessons:
        return True  # Already completed
    # Append to lesson_progress.txt
    path = os.path.join(DATA_DIR, 'lesson_progress.txt')
    with open(path, 'a', encoding='utf-8') as f:
        f.write(f"{enrollment_id}|{lesson_number}\n")
    # Update progress in enrollments.txt
    completed_lessons.add(lesson_number)
    progress = (len(completed_lessons) / total_lessons) * 100
    update_enrollment_progress(enrollment_id, progress)
    # If progress is 100%, generate certificate
    if progress >= 100:
        generate_certificate(username, course_id)
    return True
def get_assignments_for_user(username):
    assignments = read_assignments()
    enrollments = read_enrollments()
    user_enrollments = {e['course_id'] for e in enrollments.values() if e['username'] == username}
    user_assignments = {}
    for aid, a in assignments.items():
        if a['course_id'] in user_enrollments:
            user_assignments[aid] = a
    return user_assignments
def get_user_submissions(username):
    submissions = read_submissions()
    user_subs = {}
    for sid, s in submissions.items():
        if s['username'] == username:
            user_subs[s['assignment_id']] = s
    return user_subs
def save_submission(assignment_id, username, submission_text):
    submissions = read_submissions()
    submission_id = get_next_id(submissions)
    submit_date = datetime.now().strftime('%Y-%m-%d')
    submissions[submission_id] = {
        'assignment_id': assignment_id,
        'username': username,
        'submission_text': submission_text.replace('\n', ' ').replace('|', ' '),
        'submit_date': submit_date,
        'grade': '',
        'feedback': ''
    }
    write_submissions(submissions)
def get_certificates_for_user(username):
    certificates = read_certificates()
    user_certs = {}
    for cid, c in certificates.items():
        if c['username'] == username:
            user_certs[cid] = c
    return user_certs
# Routes and views
@app.route('/')
def dashboard():
    username = get_logged_in_username()
    if not username:
        # For simplicity, auto-login as 'john' if no session
        session['username'] = 'john'
        username = 'john'
    fullname = get_user_fullname(username)
    enrollments = get_user_enrollments(username)
    courses = read_courses()
    enrolled_courses = []
    for eid, e in enrollments.items():
        course = courses.get(e['course_id'])
        if course:
            enrolled_courses.append({
                'enrollment_id': eid,
                'course_id': e['course_id'],
                'title': course['title'],
                'progress': int(e['progress']),
                'status': e['status']
            })
    return render_template('dashboard.html',
                           dashboard_page_id='dashboard-page',
                           welcome_message=f"Welcome, {fullname}!",
                           enrolled_courses=enrolled_courses)
@app.route('/course_catalog', methods=['GET', 'POST'])
def course_catalog():
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('dashboard'))
    courses = read_courses()
    search_query = ''
    filtered_courses = courses
    if request.method == 'POST':
        search_query = request.form.get('search-input', '').strip().lower()
        if search_query:
            filtered_courses = {cid: c for cid, c in courses.items()
                                if search_query in c['title'].lower() or search_query in c['description'].lower()}
    return render_template('course_catalog.html',
                           catalog_page_id='catalog-page',
                           courses=filtered_courses,
                           search_query=search_query)
@app.route('/course_details/<course_id>', methods=['GET', 'POST'])
def course_details(course_id):
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('dashboard'))
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        flash('Course not found.')
        return redirect(url_for('course_catalog'))
    enrolled = is_enrolled(username, course_id)
    if request.method == 'POST':
        if not enrolled:
            enrollments = read_enrollments()
            enrollment_id = get_next_id(enrollments)
            enrollment_date = datetime.now().strftime('%Y-%m-%d')
            enrollments[enrollment_id] = {
                'username': username,
                'course_id': course_id,
                'enrollment_date': enrollment_date,
                'progress': 0,
                'status': 'In Progress'
            }
            write_enrollments(enrollments)
            flash('Successfully enrolled in the course.')
            return redirect(url_for('my_courses'))
        else:
            flash('You are already enrolled in this course.')
    return render_template('course_details.html',
                           course_details_page_id='course-details-page',
                           course_title=course['title'],
                           course_description=course['description'],
                           enrolled=enrolled)
@app.route('/my_courses')
def my_courses():
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('dashboard'))
    enrollments = get_user_enrollments(username)
    courses = read_courses()
    courses_list = []
    for eid, e in enrollments.items():
        course = courses.get(e['course_id'])
        if course:
            courses_list.append({
                'enrollment_id': eid,
                'course_id': e['course_id'],
                'title': course['title'],
                'progress': int(e['progress']),
                'status': e['status']
            })
    return render_template('my_courses.html',
                           my_courses_page_id='my-courses-page',
                           courses_list=courses_list)
@app.route('/course_learning/<course_id>', methods=['GET', 'POST'])
def course_learning(course_id):
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('dashboard'))
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        flash('Course not found.')
        return redirect(url_for('my_courses'))
    enrollment_id, enrollment = get_enrollment(username, course_id)
    if not enrollment:
        flash('You are not enrolled in this course.')
        return redirect(url_for('my_courses'))
    lessons = get_course_lessons(course_id)
    completed_lessons = get_completed_lessons(username, course_id)
    current_lesson_number = 1
    # Determine current lesson to show: first incomplete lesson in sequence
    for lesson in lessons:
        if lesson['lesson_number'] not in completed_lessons:
            current_lesson_number = lesson['lesson_number']
            break
    else:
        # All lessons completed, show last lesson
        current_lesson_number = lessons[-1]['lesson_number']
    if request.method == 'POST':
        # Mark current lesson complete
        mark_success = mark_lesson_complete(username, course_id, current_lesson_number)
        if not mark_success:
            flash('Please complete previous lessons first.')
        else:
            flash(f'Lesson {current_lesson_number} marked as completed.')
        return redirect(url_for('course_learning', course_id=course_id))
    # Prepare lesson content for current lesson
    current_lesson = next((l for l in lessons if l['lesson_number'] == current_lesson_number), None)
    lessons_status = []
    for l in lessons:
        lessons_status.append({
            'lesson_number': l['lesson_number'],
            'title': l['title'],
            'completed': l['lesson_number'] in completed_lessons
        })
    return render_template('course_learning.html',
                           learning_page_id='learning-page',
                           lessons_list=lessons_status,
                           lesson_content=current_lesson['content'] if current_lesson else '',
                           current_lesson_number=current_lesson_number,
                           course_id=course_id)
@app.route('/my_assignments')
def my_assignments():
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('dashboard'))
    assignments = get_assignments_for_user(username)
    submissions = get_user_submissions(username)
    assignments_list = []
    for aid, a in assignments.items():
        submitted = aid in submissions
        assignments_list.append({
            'assignment_id': aid,
            'course_id': a['course_id'],
            'title': a['title'],
            'description': a['description'],
            'due_date': a['due_date'],
            'max_points': a['max_points'],
            'submitted': submitted
        })
    return render_template('my_assignments.html',
                           assignments_page_id='assignments-page',
                           assignments=assignments_list)
@app.route('/submit_assignment/<assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('dashboard'))
    assignments = read_assignments()
    assignment = assignments.get(assignment_id)
    if not assignment:
        flash('Assignment not found.')
        return redirect(url_for('my_assignments'))
    submissions = read_submissions()
    # Check if already submitted
    for s in submissions.values():
        if s['assignment_id'] == assignment_id and s['username'] == username:
            flash('You have already submitted this assignment.')
            return redirect(url_for('my_assignments'))
    if request.method == 'POST':
        submission_text = request.form.get('submission-text', '').strip()
        if not submission_text:
            flash('Submission text cannot be empty.')
            return redirect(url_for('submit_assignment', assignment_id=assignment_id))
        save_submission(assignment_id, username, submission_text)
        flash('Assignment submitted successfully.')
        return redirect(url_for('my_assignments'))
    return render_template('submit_assignment.html',
                           submit_page_id='submit-page',
                           assignment_info=assignment)
@app.route('/certificates')
def certificates():
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('dashboard'))
    certificates = get_certificates_for_user(username)
    courses = read_courses()
    certs_list = []
    for cid, c in certificates.items():
        course = courses.get(c['course_id'])
        if course:
            certs_list.append({
                'certificate_id': cid,
                'course_id': c['course_id'],
                'course_title': course['title'],
                'issue_date': c['issue_date']
            })
    return render_template('certificates.html',
                           certificates_page_id='certificates-page',
                           certificates=certs_list)
@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('dashboard'))
    users = read_users()
    user = users.get(username)
    if not user:
        flash('User not found.')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('profile-email', '').strip()
        fullname = request.form.get('profile-fullname', '').strip()
        if not email or not fullname:
            flash('Email and Full name cannot be empty.')
            return redirect(url_for('user_profile'))
        # Update user info
        users[username]['email'] = email
        users[username]['fullname'] = fullname
        write_users(users)
        flash('Profile updated successfully.')
        return redirect(url_for('dashboard'))
    return render_template('user_profile.html',
                           profile_page_id='profile-page',
                           profile_email=user['email'],
                           profile_fullname=user['fullname'])
# Run the app
if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)