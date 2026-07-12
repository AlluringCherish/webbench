from flask import Flask, render_template, redirect, url_for, request, session, flash
import os
import datetime
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # session secret key

DATA_DIR = 'data'

# Helper functions to read/write pipe-delimited data files

def read_users():
    path = os.path.join(DATA_DIR, 'users.txt')
    users = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                username, email, fullname = line.split('|')
                users[username] = {'username': username, 'email': email, 'fullname': fullname}
    except FileNotFoundError:
        pass
    return users


def write_users(users):
    path = os.path.join(DATA_DIR, 'users.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for user in users.values():
                line = f"{user['username']}|{user['email']}|{user['fullname']}\n"
                f.write(line)
    except Exception as e:
        print('Error writing users.txt:', e)


def read_courses():
    path = os.path.join(DATA_DIR, 'courses.txt')
    courses = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
    except FileNotFoundError:
        pass
    return courses


def write_courses(courses):
    path = os.path.join(DATA_DIR, 'courses.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for c in courses.values():
                line = f"{c['course_id']}|{c['title']}|{c['description']}|{c['category']}|{c['level']}|{c['duration']}|{c['status']}\n"
                f.write(line)
    except Exception as e:
        print('Error writing courses.txt:', e)


def read_enrollments():
    path = os.path.join(DATA_DIR, 'enrollments.txt')
    enrollments = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                enrollment_id = int(parts[0])
                enrollments[enrollment_id] = {
                    'enrollment_id': enrollment_id,
                    'username': parts[1],
                    'course_id': int(parts[2]),
                    'enrollment_date': parts[3],
                    'progress': int(parts[4]),
                    'status': parts[5]
                }
    except FileNotFoundError:
        pass
    return enrollments


def write_enrollments(enrollments):
    path = os.path.join(DATA_DIR, 'enrollments.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for e in enrollments.values():
                line = f"{e['enrollment_id']}|{e['username']}|{e['course_id']}|{e['enrollment_date']}|{e['progress']}|{e['status']}\n"
                f.write(line)
    except Exception as e:
        print('Error writing enrollments.txt:', e)


def read_assignments():
    path = os.path.join(DATA_DIR, 'assignments.txt')
    assignments = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                assignment_id = int(parts[0])
                assignments[assignment_id] = {
                    'assignment_id': assignment_id,
                    'course_id': int(parts[1]),
                    'title': parts[2],
                    'description': parts[3],
                    'due_date': parts[4],
                    'max_points': int(parts[5])
                }
    except FileNotFoundError:
        pass
    return assignments


def write_assignments(assignments):
    path = os.path.join(DATA_DIR, 'assignments.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for a in assignments.values():
                line = f"{a['assignment_id']}|{a['course_id']}|{a['title']}|{a['description']}|{a['due_date']}|{a['max_points']}\n"
                f.write(line)
    except Exception as e:
        print('Error writing assignments.txt:', e)


def read_submissions():
    path = os.path.join(DATA_DIR, 'submissions.txt')
    submissions = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
    except FileNotFoundError:
        pass
    return submissions


def write_submissions(submissions):
    path = os.path.join(DATA_DIR, 'submissions.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for s in submissions.values():
                line = f"{s['submission_id']}|{s['assignment_id']}|{s['username']}|{s['submission_text']}|{s['submit_date']}|{s['grade']}|{s['feedback']}\n"
                f.write(line)
    except Exception as e:
        print('Error writing submissions.txt:', e)


def read_certificates():
    path = os.path.join(DATA_DIR, 'certificates.txt')
    certificates = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                certificate_id = int(parts[0])
                certificates[certificate_id] = {
                    'certificate_id': certificate_id,
                    'username': parts[1],
                    'course_id': int(parts[2]),
                    'issue_date': parts[3]
                }
    except FileNotFoundError:
        pass
    return certificates


def write_certificates(certificates):
    path = os.path.join(DATA_DIR, 'certificates.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for c in certificates.values():
                line = f"{c['certificate_id']}|{c['username']}|{c['course_id']}|{c['issue_date']}\n"
                f.write(line)
    except Exception as e:
        print('Error writing certificates.txt:', e)


# For simplicity, assume a logged-in user stored in session (for demo purposes).
# In a real app, authentication middleware would be required.
# For demonstration, we hardcode a user login as 'john'.
@app.before_request
def set_demo_user():
    if 'username' not in session:
        session['username'] = 'john'  # default logged-in user


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    users = read_users()
    user = users.get(username)
    if not user:
        return "User not found", 404

    enrollments = read_enrollments()
    courses = read_courses()

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

    return render_template('dashboard.html', username=username, fullname=user['fullname'], enrolled_courses=enrolled_courses)


@app.route('/catalog')
def course_catalog():
    courses = read_courses()
    course_list = []
    for course in courses.values():
        course_list.append({
            'course_id': course['course_id'],
            'title': course['title'],
            'category': course['category'],
            'level': course['level'],
            'duration': course['duration'],
            'status': course['status']
        })
    return render_template('catalog.html', courses=course_list)


@app.route('/course/<int:course_id>', methods=['GET', 'POST'])
def course_details(course_id):
    username = session.get('username')
    users = read_users()
    user = users.get(username)
    if not user:
        return "User not found", 404

    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        return "Course not found", 404

    enrollments = read_enrollments()
    # Check enrollment for this user and course
    is_enrolled = False
    for enrollment in enrollments.values():
        if enrollment['username'] == username and enrollment['course_id'] == course_id:
            is_enrolled = True
            break

    if request.method == 'POST':
        # Enrollment POST
        if not is_enrolled and course['status'] == 'Active':
            # Create new enrollment
            new_enrollment_id = max(enrollments.keys(), default=0) + 1
            today_str = datetime.date.today().isoformat()
            enrollments[new_enrollment_id] = {
                'enrollment_id': new_enrollment_id,
                'username': username,
                'course_id': course_id,
                'enrollment_date': today_str,
                'progress': 0,
                'status': 'In Progress'
            }
            write_enrollments(enrollments)
            is_enrolled = True
        # After enrollment, redirect to course details GET
        return redirect(url_for('course_details', course_id=course_id))

    # GET request
    return render_template('course_details.html', course=course, is_enrolled=is_enrolled)


@app.route('/my-courses')
def my_courses():
    username = session.get('username')
    enrollments = read_enrollments()
    courses = read_courses()

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

    return render_template('my_courses.html', enrolled_courses=enrolled_courses)


@app.route('/learn/<int:course_id>', methods=['GET', 'POST'])
def course_learning(course_id):
    username = session.get('username')

    users = read_users()
    user = users.get(username)
    if not user:
        return "User not found", 404

    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        return "Course not found", 404

    enrollments = read_enrollments()
    enrollment = None
    for e in enrollments.values():
        if e['username'] == username and e['course_id'] == course_id:
            enrollment = e
            break
    if enrollment is None:
        flash('You are not enrolled in this course.')
        return redirect(url_for('my_courses'))

    # We need to load lessons with lesson_number, lesson_title, lesson_content
    # Lessons are not specified in the data files explicitly - Assuming from course description or add placeholder
    # Since not in spec, we will simulate lessons as numbered blocks from description (simplified)
    # Let's create mock lessons for demo: assuming 5 lessons with titles "Lesson 1".. etc.

    lessons = []
    # For realistic approach, split the description by lines and assign
    # But we're just mocking 5 lessons
    for i in range(1,6):
        lessons.append({
            'lesson_number': i,
            'lesson_title': f'Lesson {i}',
            'lesson_content': f'Content for lesson {i} of the course "{course["title"]}".'
        })

    # Track completed lessons in enrollments.txt via progress
    # progress = integer percentage -> completed lessons count = progress / 20 (since 5 lessons -> 20% each)
    completed_lessons_count = enrollment['progress'] // 20
    completed_lessons = set(range(1, completed_lessons_count + 1))

    # Current lesson number (show first not completed)
    current_lesson_number = 1
    for i in range(1, 6):
        if i not in completed_lessons:
            current_lesson_number = i
            break
    else:
        # All completed
        current_lesson_number = 5

    can_mark_complete = False

    if request.method == 'POST':
        # Mark current lesson complete
        # Only consecutive lessons can be marked complete
        # Check if current_lesson_number is exactly next to completed lessons count + 1
        if current_lesson_number == completed_lessons_count + 1:
            # Mark complete by updating progress
            completed_lessons.add(current_lesson_number)
            new_completed_count = len(completed_lessons)
            new_progress = min(100, new_completed_count * 20)
            enrollment['progress'] = new_progress
            if new_progress == 100:
                enrollment['status'] = 'Completed'
            else:
                enrollment['status'] = 'In Progress'

            # Save changes
            write_enrollments(enrollments)

            # Check and generate certificate if completed
            if new_progress == 100:
                certificates = read_certificates()
                # Check if already issued
                cert_exists = False
                for cert in certificates.values():
                    if cert['username'] == username and cert['course_id'] == course_id:
                        cert_exists = True
                        break
                if not cert_exists:
                    new_cert_id = max(certificates.keys(), default=0) + 1
                    issue_date = datetime.date.today().isoformat()
                    certificates[new_cert_id] = {
                        'certificate_id': new_cert_id,
                        'username': username,
                        'course_id': course_id,
                        'issue_date': issue_date
                    }
                    write_certificates(certificates)

            return redirect(url_for('course_learning', course_id=course_id))

    # Update completed lessons set in case POST did not change it
    completed_lessons_count = enrollment['progress'] // 20
    completed_lessons = set(range(1, completed_lessons_count + 1))

    # Recalculate current_lesson_number and can_mark_complete
    current_lesson_number = 1
    for i in range(1, 6):
        if i not in completed_lessons:
            current_lesson_number = i
            break
    else:
        # All completed
        current_lesson_number = 5

    can_mark_complete = (current_lesson_number == max(completed_lessons) + 1) if completed_lessons else (current_lesson_number == 1)

    # Special case: if all lessons completed, can_mark_complete should be False
    if enrollment['progress'] == 100:
        can_mark_complete = False

    return render_template('course_learning.html',
                           course={'course_id': course['course_id'], 'title': course['title'], 'lessons': lessons},
                           current_lesson_number=current_lesson_number,
                           completed_lessons=completed_lessons,
                           progress=enrollment['progress'],
                           can_mark_complete=can_mark_complete)


@app.route('/assignments')
def my_assignments():
    username = session.get('username')
    assignments = read_assignments()
    submissions = read_submissions()

    # Prepare list of assignments for the user with status:
    # status can be Pending (not submitted), Submitted (submitted but not graded), Graded
    assignment_list = []
    for assignment in assignments.values():
        # Only assignments for courses user is enrolled in
        # Check enrollment
        enrollments = read_enrollments()
        enrolled_courses = set()
        for e in enrollments.values():
            if e['username'] == username:
                enrolled_courses.add(e['course_id'])
        if assignment['course_id'] not in enrolled_courses:
            continue

        # Find submission for this assignment and user
        submission = None
        for s in submissions.values():
            if s['assignment_id'] == assignment['assignment_id'] and s['username'] == username:
                submission = s
                break

        status = 'Pending'
        if submission:
            if submission['grade'] >= 0:
                status = 'Graded'
            else:
                status = 'Submitted'

        assignment_list.append({
            'assignment_id': assignment['assignment_id'],
            'title': assignment['title'],
            'due_date': assignment['due_date'],
            'status': status
        })

    return render_template('assignments.html', assignments=assignment_list)


@app.route('/submit-assignment/<int:assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    username = session.get('username')

    assignments = read_assignments()
    assignment = assignments.get(assignment_id)
    if not assignment:
        return "Assignment not found", 404

    submissions = read_submissions()
    confirmation_message = None

    if request.method == 'POST':
        submission_text = request.form.get('submission_text')
        if submission_text is None or submission_text.strip() == '':
            flash('Submission text cannot be empty.')
        else:
            # Create new submission
            new_submission_id = max(submissions.keys(), default=0) + 1
            today_str = datetime.date.today().isoformat()
            # grade and feedback initially set to -1 and empty string (not graded)
            submissions[new_submission_id] = {
                'submission_id': new_submission_id,
                'assignment_id': assignment_id,
                'username': username,
                'submission_text': submission_text.strip().replace('|', ' '),
                'submit_date': today_str,
                'grade': -1,
                'feedback': ''
            }
            write_submissions(submissions)
            confirmation_message = 'Submission successful.'

    return render_template('submit_assignment.html', assignment=assignment, confirmation_message=confirmation_message)


@app.route('/certificates')
def certificates():
    username = session.get('username')
    certificates = read_certificates()
    courses = read_courses()

    user_certs = []
    for cert in certificates.values():
        if cert['username'] == username:
            course = courses.get(cert['course_id'])
            if course:
                user_certs.append({
                    'certificate_id': cert['certificate_id'],
                    'course_title': course['title'],
                    'issue_date': cert['issue_date']
                })

    return render_template('certificates.html', certificates=user_certs)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = session.get('username')
    users = read_users()
    user = users.get(username)
    if not user:
        return "User not found", 404

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        fullname = request.form.get('fullname', '').strip()

        # Update only if provided
        if email:
            user['email'] = email
        if fullname:
            user['fullname'] = fullname

        users[username] = user
        write_users(users)

        flash('Profile updated successfully.')
        return redirect(url_for('profile'))

    return render_template('profile.html', username=user['username'], email=user['email'], fullname=user['fullname'])


if __name__ == '__main__':
    app.run(debug=True, port=5000)
