from flask import Flask, render_template, redirect, url_for, request, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'replace_with_secure_key'

DATA_PATH = 'data'

# Helper functions for Data Handling

def read_users():
    path = os.path.join(DATA_PATH, 'users.txt')
    users = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                username, email, fullname = line.split('|')
                users[username] = {'username': username, 'email': email, 'fullname': fullname}
    except FileNotFoundError:
        pass
    return users


def read_courses():
    path = os.path.join(DATA_PATH, 'courses.txt')
    courses = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                (course_id, title, description, category, level, duration, status) = line.split('|')
                courses[course_id] = {
                    'course_id': course_id, 'title': title, 'description': description, 'category': category,
                    'level': level, 'duration': duration, 'status': status
                }
    except FileNotFoundError:
        pass
    return courses


def read_enrollments():
    path = os.path.join(DATA_PATH, 'enrollments.txt')
    enrollments = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                enrollment_id, username, course_id, enrollment_date, progress, status = line.split('|')
                enrollments.append({
                    'enrollment_id': enrollment_id,
                    'username': username,
                    'course_id': course_id,
                    'enrollment_date': enrollment_date,
                    'progress': int(progress),
                    'status': status
                })
    except FileNotFoundError:
        pass
    return enrollments


def write_enrollments(enrollments):
    path = os.path.join(DATA_PATH, 'enrollments.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for e in enrollments:
            line = '|'.join([
                e['enrollment_id'], e['username'], e['course_id'], e['enrollment_date'],
                str(e['progress']), e['status']
            ])
            f.write(line + '\n')


def read_assignments():
    path = os.path.join(DATA_PATH, 'assignments.txt')
    assignments = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                (assignment_id, course_id, title, description, due_date, max_points) = line.split('|')
                assignments[assignment_id] = {
                    'assignment_id': assignment_id,
                    "course_id": course_id,
                    'title': title,
                    'description': description,
                    'due_date': due_date,
                    'max_points': int(max_points)
                }
    except FileNotFoundError:
        pass
    return assignments


def read_submissions():
    path = os.path.join(DATA_PATH, 'submissions.txt')
    submissions = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                (submission_id, assignment_id, username, submission_text, submit_date, grade, feedback) = line.split('|')
                submissions.append({
                    'submission_id': submission_id,
                    'assignment_id': assignment_id,
                    'username': username,
                    'submission_text': submission_text,
                    'submit_date': submit_date,
                    'grade': grade,
                    'feedback': feedback
                })
    except FileNotFoundError:
        pass
    return submissions


def write_submissions(submissions):
    path = os.path.join(DATA_PATH, 'submissions.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for s in submissions:
            line = '|'.join([
                s['submission_id'], s['assignment_id'], s['username'], s['submission_text'],
                s['submit_date'], s['grade'], s['feedback']
            ])
            f.write(line + '\n')


def read_certificates():
    path = os.path.join(DATA_PATH, 'certificates.txt')
    certificates = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                certificate_id, username, course_id, issue_date = line.split('|')
                certificates.append({
                    'certificate_id': certificate_id,
                    'username': username,
                    'course_id': course_id,
                    'issue_date': issue_date
                })
    except FileNotFoundError:
        pass
    return certificates


def write_certificates(certificates):
    path = os.path.join(DATA_PATH, 'certificates.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for c in certificates:
            line = '|'.join([
                c['certificate_id'], c['username'], c['course_id'], c['issue_date']
            ])
            f.write(line + '\n')


# For simplicity, lessons are hardcoded in-memory due to spec statement that lessons are assumed available from other means
# Normally, lessons would be read from a file or database
lessons_data = {
    '1': [
        {'lesson_id': '1-1', 'title': 'Introduction to Python', 'content': 'Python basics content...'},
        {'lesson_id': '1-2', 'title': 'Data Types', 'content': 'Details about data types.'},
        {'lesson_id': '1-3', 'title': 'Control Flow', 'content': 'If statements, loops, etc.'}
    ],
    '2': [
        {'lesson_id': '2-1', 'title': 'HTML Basics', 'content': 'Learn HTML tags and structure.'},
        {'lesson_id': '2-2', 'title': 'CSS Styling', 'content': 'CSS basics, colors, fonts.'},
        {'lesson_id': '2-3', 'title': 'JavaScript Intro', 'content': 'Basic JavaScript programming.'}
    ],
    '3': [
        {'lesson_id': '3-1', 'title': 'Data Analysis Introduction', 'content': 'Overview of data analysis.'},
        {'lesson_id': '3-2', 'title': 'Pandas Basics', 'content': 'Using pandas library.'},
        {'lesson_id': '3-3', 'title': 'Data Visualization', 'content': 'Charts and graphs.'}
    ],
}


def get_current_user():
    # For this spec, mock user is always 'john'
    # In real app, session or auth would be used
    return 'john'


def generate_new_id(existing_ids):
    if not existing_ids:
        return '1'
    try:
        max_id = max(int(i) for i in existing_ids)
        return str(max_id + 1)
    except Exception:
        return '1'

# Routes implementation

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = get_current_user()
    users = read_users()
    user = users.get(username)
    if not user:
        return "User not found.", 404

    enrollments = read_enrollments()
    courses = read_courses()

    # Filter enrollments by user
    user_enrollments = [e for e in enrollments if e['username'] == username]

    enrolled_courses = []
    for e in user_enrollments:
        c = courses.get(e['course_id'])
        if c:
            enrolled_courses.append({
                'course_id': c['course_id'],
                'title': c['title'],
                'progress': e['progress']
            })

    return render_template('dashboard.html', username=username, fullname=user['fullname'], enrolled_courses=enrolled_courses)


@app.route('/catalog')
def catalog():
    courses = read_courses()
    # Show only active courses
    active_courses = [c for c in courses.values() if c['status'] == 'Active']
    return render_template('course_catalog.html', courses=active_courses)


@app.route('/catalog/course/<course_id>')
def course_details(course_id):
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        return "Course not found.", 404

    username = get_current_user()
    enrollments = read_enrollments()
    is_enrolled = any(e for e in enrollments if e['username'] == username and e['course_id'] == course_id)

    return render_template('course_details.html', course=course, is_enrolled=is_enrolled)


@app.route('/catalog/course/<course_id>/enroll', methods=['POST'])
def enroll_course(course_id):
    username = get_current_user()
    enrollments = read_enrollments()
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        return "Course not found.", 404

    is_enrolled = any(e for e in enrollments if e['username'] == username and e['course_id'] == course_id)

    enrollment_success = None
    if not is_enrolled:
        # Generate new enrollment_id
        existing_ids = [e['enrollment_id'] for e in enrollments]
        new_enrollment_id = generate_new_id(existing_ids)
        new_enrollment = {
            'enrollment_id': new_enrollment_id,
            'username': username,
            'course_id': course_id,
            'enrollment_date': datetime.now().strftime('%Y-%m-%d'),
            'progress': 0,
            'status': 'In Progress'
        }
        enrollments.append(new_enrollment)
        write_enrollments(enrollments)
        enrollment_success = True
        is_enrolled = True
    else:
        enrollment_success = False

    return render_template('course_details.html', course=course, is_enrolled=is_enrolled, enrollment_success=enrollment_success)


@app.route('/my-courses')
def my_courses():
    username = get_current_user()
    enrollments = read_enrollments()
    courses = read_courses()

    user_enrollments = [e for e in enrollments if e['username'] == username]

    enrolled_courses = []
    for e in user_enrollments:
        course = courses.get(e['course_id'])
        if course:
            enrolled_courses.append({
                'course_id': course['course_id'],
                'title': course['title'],
                'progress': e['progress']
            })

    return render_template('my_courses.html', enrolled_courses=enrolled_courses)


@app.route('/my-courses/course/<course_id>')
def course_learning(course_id):
    username = get_current_user()
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        return "Course not found.", 404

    enrollments = read_enrollments()
    enrollment = next((e for e in enrollments if e['username'] == username and e['course_id'] == course_id), None)
    if not enrollment:
        return redirect(url_for('course_details', course_id=course_id))

    lessons = lessons_data.get(course_id, [])

    # Count completed lessons from progress percentage
    total_lessons = len(lessons)
    if total_lessons == 0:
        completed_lessons_count = 0
        progress = 0
    else:
        # Progress is integer percentage, each lesson equally weighted
        completed_lessons_count = enrollment['progress'] * total_lessons // 100
        progress = enrollment['progress']

    return render_template('course_learning.html', course=course, lessons=lessons, 
                           completed_lessons_count=completed_lessons_count, total_lessons=total_lessons, progress=progress)


@app.route('/my-courses/course/<course_id>/mark-complete', methods=['POST'])
def mark_lesson_complete(course_id):
    username = get_current_user()
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        return "Course not found.", 404

    lessons = lessons_data.get(course_id, [])
    total_lessons = len(lessons)
    if total_lessons == 0:
        # No lessons, nothing to mark
        return redirect(url_for('course_learning', course_id=course_id))

    enrollments = read_enrollments()
    enrollment = next((e for e in enrollments if e['username'] == username and e['course_id'] == course_id), None)
    if not enrollment:
        return redirect(url_for('course_details', course_id=course_id))

    # Calculate completed lessons from progress
    completed_lessons_count = enrollment['progress'] * total_lessons // 100

    # We enforce sequential completion: only next lesson can be marked complete
    if completed_lessons_count >= total_lessons:
        # All lessons already completed
        certificate_generated = False
    else:
        # Mark next lesson complete
        completed_lessons_count += 1

        # Calculate new progress
        new_progress = int(completed_lessons_count * 100 / total_lessons)

        # Update enrollment progress
        enrollment['progress'] = new_progress
        if new_progress >= 100:
            enrollment['progress'] = 100
            enrollment['status'] = 'Completed'
        else:
            enrollment['status'] = 'In Progress'

        # Write back enrollments
        write_enrollments(enrollments)

        # On completion generate certificate if not already generated
        certificate_generated = False
        if enrollment['progress'] == 100:
            certificates = read_certificates()
            already_certified = any(c for c in certificates if c['username'] == username and c['course_id'] == course_id)
            if not already_certified:
                existing_ids = [c['certificate_id'] for c in certificates]
                new_cert_id = generate_new_id(existing_ids)
                new_certificate = {
                    'certificate_id': new_cert_id,
                    'username': username,
                    'course_id': course_id,
                    'issue_date': datetime.now().strftime('%Y-%m-%d')
                }
                certificates.append(new_certificate)
                write_certificates(certificates)
                certificate_generated = True

    # Refresh data to render
    # Recalculate completed_lessons_count and progress
    enrollment_updated = next((e for e in read_enrollments() if e['username'] == username and e['course_id'] == course_id), enrollment)
    lessons = lessons_data.get(course_id, [])
    total_lessons = len(lessons)
    completed_lessons_count = enrollment_updated['progress'] * total_lessons // 100
    progress = enrollment_updated['progress']

    return render_template('course_learning.html', course=course, lessons=lessons, 
                           completed_lessons_count=completed_lessons_count, total_lessons=total_lessons, 
                           progress=progress, certificate_generated=certificate_generated)


@app.route('/assignments')
def assignments():
    username = get_current_user()
    assignments_all = read_assignments()
    submissions = read_submissions()

    # Filter assignments that belong to courses user is enrolled in
    enrollments = read_enrollments()
    user_courses_ids = set(e['course_id'] for e in enrollments if e['username'] == username)

    user_assignments = []
    for a in assignments_all.values():
        if a['course_id'] in user_courses_ids:
            # Determine status: Submitted or Pending
            sub = next((s for s in submissions if s['username'] == username and s['assignment_id'] == a['assignment_id']), None)
            status = 'Submitted' if sub else 'Pending'
            user_assignments.append({
                'assignment_id': a['assignment_id'],
                'course_id': a['course_id'],
                'title': a['title'],
                'description': a['description'],
                'due_date': a['due_date'],
                'max_points': a['max_points'],
                'status': status
            })

    return render_template('my_assignments.html', assignments=user_assignments)


@app.route('/assignments/submit/<assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    username = get_current_user()
    assignments = read_assignments()
    assignment = assignments.get(assignment_id)
    if not assignment:
        return "Assignment not found.", 404

    submissions = read_submissions()
    submission_status = None
    confirmation_message = None

    if request.method == 'POST':
        submission_text = request.form.get('submission_text', '').strip()
        if not submission_text:
            submission_status = 'Please provide submission text.'
        else:
            # Check if user already submitted for this assignment
            existing_submission = next((s for s in submissions if s['username'] == username and s['assignment_id'] == assignment_id), None)
            if existing_submission:
                # Update submission
                existing_submission['submission_text'] = submission_text
                existing_submission['submit_date'] = datetime.now().strftime('%Y-%m-%d')
                existing_submission['grade'] = ''
                existing_submission['feedback'] = ''
            else:
                # Create new submission
                existing_ids = [s['submission_id'] for s in submissions]
                new_submission_id = generate_new_id(existing_ids)
                new_submission = {
                    'submission_id': new_submission_id,
                    'assignment_id': assignment_id,
                    'username': username,
                    'submission_text': submission_text,
                    'submit_date': datetime.now().strftime('%Y-%m-%d'),
                    'grade': '',
                    'feedback': ''
                }
                submissions.append(new_submission)

            write_submissions(submissions)

            submission_status = 'Submitted successfully.'
            confirmation_message = 'Your assignment has been submitted.'

    return render_template('submit_assignment.html', assignment=assignment,
                           submission_status=submission_status, confirmation_message=confirmation_message)


@app.route('/certificates')
def certificates():
    username = get_current_user()
    certificates = read_certificates()
    courses = read_courses()

    user_certificates = []
    for c in certificates:
        if c['username'] == username:
            course = courses.get(c['course_id'])
            course_title = course['title'] if course else 'Unknown Course'
            user_certificates.append({
                'certificate_id': c['certificate_id'],
                'username': c['username'],
                'course_id': c['course_id'],
                'issue_date': c['issue_date'],
                'course_title': course_title
            })

    return render_template('certificates.html', certificates=user_certificates)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = get_current_user()
    users = read_users()
    user = users.get(username)
    if not user:
        return "User not found.", 404

    update_success = None

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        fullname = request.form.get('fullname', '').strip()

        if email and fullname:
            # Update user info
            user['email'] = email
            user['fullname'] = fullname

            # Write back all users
            path = os.path.join(DATA_PATH, 'users.txt')
            with open(path, 'w', encoding='utf-8') as f:
                for u in users.values():
                    line = '|'.join([u['username'], u['email'], u['fullname']])
                    f.write(line + '\n')

            update_success = True
        else:
            update_success = False

    return render_template('profile.html', username=username, email=user['email'], fullname=user['fullname'], update_success=update_success)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
