from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret-key-for-session'

DATA_DIR = 'data'

# File paths
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
COURSES_FILE = os.path.join(DATA_DIR, 'courses.txt')
ENROLLMENTS_FILE = os.path.join(DATA_DIR, 'enrollments.txt')
ASSIGNMENTS_FILE = os.path.join(DATA_DIR, 'assignments.txt')
SUBMISSIONS_FILE = os.path.join(DATA_DIR, 'submissions.txt')
CERTIFICATES_FILE = os.path.join(DATA_DIR, 'certificates.txt')

# Helper functions

def read_file_lines(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def write_file_lines(filename, lines):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


def read_users():
    users = {}
    lines = read_file_lines(USERS_FILE)
    for line in lines:
        username, email, fullname = line.split('|')
        users[username] = {'email': email, 'fullname': fullname}
    return users


def write_users(users):
    lines = []
    for username, data in users.items():
        lines.append(f"{username}|{data['email']}|{data['fullname']}")
    write_file_lines(USERS_FILE, lines)


def read_courses():
    courses = {}
    lines = read_file_lines(COURSES_FILE)
    for line in lines:
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
    enrollments = []
    lines = read_file_lines(ENROLLMENTS_FILE)
    for line in lines:
        enrollment_id, username, course_id, enrollment_date, progress, status = line.split('|')
        enrollments.append({
            'enrollment_id': enrollment_id,
            'username': username,
            'course_id': course_id,
            'enrollment_date': enrollment_date,
            'progress': int(progress),
            'status': status
        })
    return enrollments


def write_enrollments(enrollments):
    lines = []
    for e in enrollments:
        lines.append(f"{e['enrollment_id']}|{e['username']}|{e['course_id']}|{e['enrollment_date']}|{e['progress']}|{e['status']}")
    write_file_lines(ENROLLMENTS_FILE, lines)


def read_assignments():
    assignments = []
    lines = read_file_lines(ASSIGNMENTS_FILE)
    for line in lines:
        assignment_id, course_id, title, description, due_date, max_points = line.split('|')
        assignments.append({
            'assignment_id': assignment_id,
            'course_id': course_id,
            'title': title,
            'description': description,
            'due_date': due_date,
            'max_points': int(max_points)
        })
    return assignments


def read_submissions():
    submissions = []
    lines = read_file_lines(SUBMISSIONS_FILE)
    for line in lines:
        parts = line.split('|', 6)
        submission_id, assignment_id, username, submission_text, submit_date, grade, feedback = parts
        grade_val = int(grade) if grade.isdigit() else None
        submissions.append({
            'submission_id': submission_id,
            'assignment_id': assignment_id,
            'username': username,
            'submission_text': submission_text,
            'submit_date': submit_date,
            'grade': grade_val,
            'feedback': feedback
        })
    return submissions


def write_submissions(submissions):
    lines = []
    for s in submissions:
        grade_str = str(s['grade']) if s['grade'] is not None else ''
        lines.append(f"{s['submission_id']}|{s['assignment_id']}|{s['username']}|{s['submission_text']}|{s['submit_date']}|{grade_str}|{s['feedback']}")
    write_file_lines(SUBMISSIONS_FILE, lines)


def read_certificates():
    certificates = []
    lines = read_file_lines(CERTIFICATES_FILE)
    for line in lines:
        certificate_id, username, course_id, issue_date = line.split('|')
        certificates.append({
            'certificate_id': certificate_id,
            'username': username,
            'course_id': course_id,
            'issue_date': issue_date
        })
    return certificates


def write_certificates(certificates):
    lines = []
    for c in certificates:
        lines.append(f"{c['certificate_id']}|{c['username']}|{c['course_id']}|{c['issue_date']}")
    write_file_lines(CERTIFICATES_FILE, lines)


# For demonstration, assuming current user is hardcoded
CURRENT_USER = 'john'


@app.route('/')
def dashboard():
    users = read_users()
    courses = read_courses()
    enrollments = read_enrollments()

    user_profile = users.get(CURRENT_USER, {'fullname': CURRENT_USER, 'email': ''})

    # Filter enrollments of current user
    user_enrollments = [e for e in enrollments if e['username'] == CURRENT_USER]

    # For each enrollment, get course info + progress
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
                           fullname=user_profile.get('fullname', CURRENT_USER),
                           enrolled_courses=enrolled_courses)


@app.route('/catalog', methods=['GET', 'POST'])
def course_catalog():
    courses = read_courses()
    search_term = ''
    filtered_courses = list(courses.values())

    if request.method == 'POST':
        search_term = request.form.get('search', '').strip().lower()
        if search_term:
            filtered_courses = [c for c in courses.values() if search_term in c['title'].lower()]

    return render_template('catalog.html', courses=filtered_courses, search_term=search_term)


@app.route('/course/<course_id>', methods=['GET', 'POST'])
def course_details(course_id):
    courses = read_courses()
    enrollments = read_enrollments()
    course = courses.get(course_id)
    if not course:
        flash('Course not found', 'error')
        return redirect(url_for('course_catalog'))

    # Check if current user is enrolled in this course
    enrolled = any(e['username'] == CURRENT_USER and e['course_id'] == course_id for e in enrollments)

    if request.method == 'POST':
        if not enrolled:
            # Enroll the user
            enrollment_id = 1
            if enrollments:
                enrollment_id = max(int(e['enrollment_id']) for e in enrollments) + 1
            new_enrollment = {
                'enrollment_id': str(enrollment_id),
                'username': CURRENT_USER,
                'course_id': course_id,
                'enrollment_date': datetime.now().strftime('%Y-%m-%d'),
                'progress': 0,
                'status': 'In Progress'
            }
            enrollments.append(new_enrollment)
            write_enrollments(enrollments)
            flash('Enrollment successful!', 'success')
            return redirect(url_for('course_details', course_id=course_id))

    return render_template('course_details.html', course=course, enrolled=enrolled)


@app.route('/mycourses')
def my_courses():
    users = read_users()
    courses = read_courses()
    enrollments = read_enrollments()

    user_enrollments = [e for e in enrollments if e['username'] == CURRENT_USER]

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

    return render_template('mycourses.html', courses=courses_list)


@app.route('/learn/<course_id>/<int:lesson_num>', methods=['GET', 'POST'])
def course_learning(course_id, lesson_num):
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        flash('Course not found', 'error')
        return redirect(url_for('my_courses'))

    # Fake lessons data: For this spec, we do not have lessons.txt file, so dummy lessons
    # Let's assume each course has 5 lessons, numbered 1 to 5
    total_lessons = 5
    lessons = [f'Lesson {i+1} content for {course["title"]}' for i in range(total_lessons)]

    enrollments = read_enrollments()
    user_enrollment = None
    for e in enrollments:
        if e['username'] == CURRENT_USER and e['course_id'] == course_id:
            user_enrollment = e
            break

    if not user_enrollment:
        flash('You are not enrolled in this course.', 'error')
        return redirect(url_for('my_courses'))

    if request.method == 'POST':
        # Mark lesson as complete only if the lesson matches current progress sequence
        current_progress = user_enrollment['progress']
        completed_lessons = int(total_lessons * current_progress / 100)
        if lesson_num == completed_lessons + 1:
            # Mark this lesson complete
            completed_lessons += 1
            new_progress = int((completed_lessons / total_lessons) * 100)
            user_enrollment['progress'] = new_progress
            if new_progress == 100:
                user_enrollment['status'] = 'Completed'
                # Generate certificate
                certificates = read_certificates()
                certificate_id = 1
                if certificates:
                    certificate_id = max(int(c['certificate_id']) for c in certificates) + 1
                new_certificate = {
                    'certificate_id': str(certificate_id),
                    'username': CURRENT_USER,
                    'course_id': course_id,
                    'issue_date': datetime.now().strftime('%Y-%m-%d')
                }
                certificates.append(new_certificate)
                write_certificates(certificates)
            write_enrollments(enrollments)
        else:
            flash('Please complete lessons in order.', 'error')

    # Update lesson content for current lesson_num
    if lesson_num < 1 or lesson_num > total_lessons:
        flash('Invalid lesson number.', 'error')
        return redirect(url_for('my_courses'))

    lesson_content = lessons[lesson_num - 1]

    # Calculate which lessons are completed
    progress = user_enrollment['progress']
    completed_lessons = int(total_lessons * progress / 100)

    # Prepare lesson list with completion status
    lesson_list = []
    for i in range(total_lessons):
        lesson_list.append({
            'lesson_num': i + 1,
            'title': f'Lesson {i+1}',
            'completed': (i < completed_lessons)
        })

    return render_template('learning.html', course=course, lessons=lesson_list, lesson_content=lesson_content, lesson_num=lesson_num)


@app.route('/assignments')
def my_assignments():
    courses = read_courses()
    assignments = read_assignments()
    submissions = read_submissions()

    # Get assignments for courses where user is enrolled
    enrollments = read_enrollments()
    user_enrolled_course_ids = set(e['course_id'] for e in enrollments if e['username'] == CURRENT_USER)

    user_assignments = [a for a in assignments if a['course_id'] in user_enrolled_course_ids]

    # Map assignment_id -> submission for current user
    submissions_map = {s['assignment_id']: s for s in submissions if s['username'] == CURRENT_USER}

    # Prepare assignments data with submission status
    assignments_data = []
    for assignment in user_assignments:
        submission = submissions_map.get(assignment['assignment_id'])
        assignments_data.append({
            'assignment_id': assignment['assignment_id'],
            'title': assignment['title'],
            'due_date': assignment['due_date'],
            'submitted': submission is not None,
            'grade': submission['grade'] if submission else None
        })

    return render_template('assignments.html', assignments=assignments_data)


@app.route('/submit/<assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    assignments = read_assignments()
    assignment = next((a for a in assignments if a['assignment_id'] == assignment_id), None)
    if not assignment:
        flash('Assignment not found', 'error')
        return redirect(url_for('my_assignments'))

    submissions = read_submissions()
    existing_submission = next((s for s in submissions if s['assignment_id'] == assignment_id and s['username'] == CURRENT_USER), None)

    if existing_submission:
        flash('You have already submitted this assignment.', 'info')
        return redirect(url_for('my_assignments'))

    if request.method == 'POST':
        submission_text = request.form.get('submission_text', '').strip()
        if not submission_text:
            flash('Submission text cannot be empty.', 'error')
            return redirect(url_for('submit_assignment', assignment_id=assignment_id))

        submission_id = 1
        if submissions:
            submission_id = max(int(s['submission_id']) for s in submissions) + 1

        new_submission = {
            'submission_id': str(submission_id),
            'assignment_id': assignment_id,
            'username': CURRENT_USER,
            'submission_text': submission_text,
            'submit_date': datetime.now().strftime('%Y-%m-%d'),
            'grade': None,
            'feedback': ''
        }

        submissions.append(new_submission)
        write_submissions(submissions)

        flash('Assignment submitted successfully!', 'success')
        return redirect(url_for('my_assignments'))

    return render_template('submit_assignment.html', assignment=assignment)


@app.route('/certificates')
def certificates():
    certificates = read_certificates()
    courses = read_courses()

    user_certificates = [c for c in certificates if c['username'] == CURRENT_USER]

    certificates_list = []
    for c in user_certificates:
        course = courses.get(c['course_id'])
        if course:
            certificates_list.append({
                'certificate_id': c['certificate_id'],
                'course_title': course['title'],
                'issue_date': c['issue_date']
            })

    return render_template('certificates.html', certificates=certificates_list)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = read_users()
    user = users.get(CURRENT_USER, {'email': '', 'fullname': ''})

    if request.method == 'POST':
        email = request.form.get('profile-email', '').strip()
        fullname = request.form.get('profile-fullname', '').strip()

        if not email or not fullname:
            flash('Email and Full name cannot be empty.', 'error')
        else:
            # Save changes
            users[CURRENT_USER] = {'email': email, 'fullname': fullname}
            write_users(users)
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))

    return render_template('profile.html', email=user.get('email', ''), fullname=user.get('fullname', ''))


if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)
