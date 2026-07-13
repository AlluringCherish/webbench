from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_placeholder'

DATA_DIR = 'data'

# Utility functions to load and save data

def load_users():
    users = {}
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r') as f:
            for line in f:
                username, email, fullname = line.strip().split('|')
                users[username] = {'username': username, 'email': email, 'fullname': fullname}
    except FileNotFoundError:
        pass
    return users


def save_users(users):
    with open(os.path.join(DATA_DIR, 'users.txt'), 'w') as f:
        for user in users.values():
            f.write(f"{user['username']}|{user['email']}|{user['fullname']}\n")


def load_courses():
    courses = {}
    try:
        with open(os.path.join(DATA_DIR, 'courses.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split('|')
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
    except FileNotFoundError:
        pass
    return courses


def load_enrollments():
    enrollments = []
    try:
        with open(os.path.join(DATA_DIR, 'enrollments.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    enrollment_id, username, course_id, enrollment_date, progress, status = parts
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


def save_enrollments(enrollments):
    with open(os.path.join(DATA_DIR, 'enrollments.txt'), 'w') as f:
        for e in enrollments:
            f.write(f"{e['enrollment_id']}|{e['username']}|{e['course_id']}|{e['enrollment_date']}|{e['progress']}|{e['status']}\n")


def load_assignments():
    assignments = {}
    try:
        with open(os.path.join(DATA_DIR, 'assignments.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    assignment_id, course_id, title, description, due_date, max_points = parts
                    assignments[assignment_id] = {
                        'assignment_id': assignment_id,
                        'course_id': course_id,
                        'title': title,
                        'description': description,
                        'due_date': due_date,
                        'max_points': int(max_points)
                    }
    except FileNotFoundError:
        pass
    return assignments


def load_submissions():
    submissions = []
    try:
        with open(os.path.join(DATA_DIR, 'submissions.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    submission_id, assignment_id, username, submission_text, submit_date, grade, feedback = parts
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


def save_submissions(submissions):
    with open(os.path.join(DATA_DIR, 'submissions.txt'), 'w') as f:
        for s in submissions:
            f.write(f"{s['submission_id']}|{s['assignment_id']}|{s['username']}|{s['submission_text']}|{s['submit_date']}|{s['grade']}|{s['feedback']}\n")


def load_certificates():
    certificates = []
    try:
        with open(os.path.join(DATA_DIR, 'certificates.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    certificate_id, username, course_id, issue_date = parts
                    certificates.append({
                        'certificate_id': certificate_id,
                        'username': username,
                        'course_id': course_id,
                        'issue_date': issue_date
                    })
    except FileNotFoundError:
        pass
    return certificates


def save_certificates(certificates):
    with open(os.path.join(DATA_DIR, 'certificates.txt'), 'w') as f:
        for c in certificates:
            f.write(f"{c['certificate_id']}|{c['username']}|{c['course_id']}|{c['issue_date']}\n")


# For demonstration purposes, user authentication is simplified
# Assuming a fixed logged-in user for draft

@app.before_request
def load_logged_in_user():
    # For draft, we assume user 'john' is logged in
    session['username'] = 'john'


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    users = load_users()
    fullname = users.get(username, {}).get('fullname', 'User')
    enrollments = load_enrollments()
    courses = load_courses()

    # Filter enrolled courses for current user with progress
    enrolled_courses = []
    for e in enrollments:
        if e['username'] == username:
            course = courses.get(e['course_id'])
            if course:
                enrolled_courses.append({
                    'course_id': course['course_id'],
                    'title': course['title'],
                    'progress': e['progress']
                })

    return render_template('dashboard.html', username=username, fullname=fullname, enrolled_courses=enrolled_courses)


@app.route('/catalog')
def course_catalog():
    courses = list(load_courses().values())
    return render_template('course_catalog.html', courses=courses)


@app.route('/course/<course_id>')
def course_details(course_id):
    courses = load_courses()
    course = courses.get(course_id)
    if not course:
        return "Course not found", 404

    username = session.get('username')
    enrollments = load_enrollments()
    enrolled = any(e['username'] == username and e['course_id'] == course_id for e in enrollments)

    return render_template('course_details.html', course=course, enrolled=enrolled)


@app.route('/course/<course_id>/enroll', methods=['POST'])
def enroll_course(course_id):
    username = session.get('username')
    enrollments = load_enrollments()
    # Check if already enrolled
    if any(e['username'] == username and e['course_id'] == course_id for e in enrollments):
        return jsonify({'status': 'already_enrolled'})
    new_enrollment_id = str(len(enrollments) + 1)
    enrollment_date = datetime.date.today().isoformat()
    enrollments.append({
        'enrollment_id': new_enrollment_id,
        'username': username,
        'course_id': course_id,
        'enrollment_date': enrollment_date,
        'progress': 0,
        'status': 'In Progress'
    })
    save_enrollments(enrollments)
    return jsonify({'status': 'enrolled'})


@app.route('/my-courses')
def my_courses():
    username = session.get('username')
    enrollments = load_enrollments()
    courses = load_courses()

    enrolled_courses = []
    for e in enrollments:
        if e['username'] == username:
            course = courses.get(e['course_id'])
            if course:
                enrolled_courses.append({
                    'course_id': course['course_id'],
                    'title': course['title'],
                    'progress': e['progress'],
                    'status': e['status']
                })

    return render_template('my_courses.html', enrolled_courses=enrolled_courses)


# Placeholder lesson content for each course - in real app this would be stored or fetched
LESSON_SAMPLE_CONTENT = {
    '1': [
        {'lesson_id': '1', 'title': 'Intro to Python', 'content': 'Welcome to Python programming.', 'completed': False},
        {'lesson_id': '2', 'title': 'Data Types', 'content': 'Learn about data types.', 'completed': False}
    ],
    '2': [
        {'lesson_id': '1', 'title': 'HTML Basics', 'content': 'Introduction to HTML.', 'completed': False},
        {'lesson_id': '2', 'title': 'CSS Basics', 'content': 'Introduction to CSS.', 'completed': False}
    ]
}

@app.route('/course/<course_id>/learn')
def course_learning(course_id):
    username = session.get('username')
    courses = load_courses()
    enrollments = load_enrollments()
    course = courses.get(course_id)
    if not course:
        return "Course not found", 404

    # Check enrollment for progress
    enrollment = None
    for e in enrollments:
        if e['username'] == username and e['course_id'] == course_id:
            enrollment = e
            break
    if not enrollment:
        return "Not enrolled", 403

    # Fetch lessons (placeholder) and completed status
    lessons_raw = LESSON_SAMPLE_CONTENT.get(course_id, [])

    # Align lessons with completed from enrollment progress if possible
    # For draft, mark lessons as completed based on enrollment progress roughly
    completed_lessons_count = int(enrollment['progress'] / 50)  # assume 2 lessons -> 50% each
    lessons = []
    for idx, l in enumerate(lessons_raw):
        lessons.append({
            'lesson_id': l['lesson_id'],
            'title': l['title'],
            'content': l['content'],
            'completed': idx < completed_lessons_count
        })

    # Current lesson is first incomplete lesson or last
    current_lesson = next((l for l in lessons if not l['completed']), lessons[-1] if lessons else None)
    progress = enrollment['progress']

    course_with_lessons = {
        'course_id': course['course_id'],
        'title': course['title'],
        'lessons': lessons
    }

    return render_template('course_learning.html', course=course_with_lessons, current_lesson=current_lesson, progress=progress)


@app.route('/course/<course_id>/learn/complete', methods=['POST'])
def mark_lesson_complete(course_id):
    username = session.get('username')
    enrollments = load_enrollments()

    # Find enrollment
    enrollment = None
    for e in enrollments:
        if e['username'] == username and e['course_id'] == course_id:
            enrollment = e
            break
    if not enrollment:
        return jsonify({'status': 'not_enrolled'}), 403

    # Update progress - for draft, increase by fixed amount
    new_progress = min(enrollment['progress'] + 50, 100)
    enrollment['progress'] = new_progress
    if new_progress == 100:
        enrollment['status'] = 'Completed'

        # Issue certificate
        certificates = load_certificates()
        certificate_exists = any(c['username'] == username and c['course_id'] == course_id for c in certificates)
        if not certificate_exists:
            new_cert_id = str(len(certificates) + 1)
            issue_date = datetime.date.today().isoformat()
            certificates.append({
                'certificate_id': new_cert_id,
                'username': username,
                'course_id': course_id,
                'issue_date': issue_date
            })
            save_certificates(certificates)

    save_enrollments(enrollments)
    return jsonify({'status': 'updated', 'progress': enrollment['progress']})


@app.route('/assignments')
def my_assignments():
    assignments = list(load_assignments().values())
    return render_template('my_assignments.html', assignments=assignments)


@app.route('/assignment/<assignment_id>/submit', methods=['GET'])
def submit_assignment_form(assignment_id):
    assignments = load_assignments()
    assignment = assignments.get(assignment_id)
    if not assignment:
        return "Assignment not found", 404
    return render_template('submit_assignment.html', assignment=assignment)


@app.route('/assignment/<assignment_id>/submit', methods=['POST'])
def submit_assignment(assignment_id):
    username = session.get('username')
    submission_text = request.form.get('submission_text', '')

    submissions = load_submissions()
    new_submission_id = str(len(submissions) + 1)
    submit_date = datetime.date.today().isoformat()

    submissions.append({
        'submission_id': new_submission_id,
        'assignment_id': assignment_id,
        'username': username,
        'submission_text': submission_text,
        'submit_date': submit_date,
        'grade': '',
        'feedback': ''
    })
    save_submissions(submissions)
    return redirect(url_for('my_assignments'))


@app.route('/certificates')
def certificates():
    username = session.get('username')
    certificates = load_certificates()
    courses = load_courses()

    # Prepare certificate list with course_title
    certs = []
    for c in certificates:
        if c['username'] == username:
            course = courses.get(c['course_id'], {})
            certs.append({
                'certificate_id': c['certificate_id'],
                'username': c['username'],
                'course_id': c['course_id'],
                'issue_date': c['issue_date'],
                'course_title': course.get('title', 'Unknown')
            })

    return render_template('certificates.html', certificates=certs)


@app.route('/profile')
def user_profile():
    username = session.get('username')
    users = load_users()
    user = users.get(username, {'username': username, 'email': '', 'fullname': ''})
    return render_template('profile.html', user=user)


@app.route('/profile/update', methods=['POST'])
def update_profile():
    username = session.get('username')
    email = request.form.get('email', '')
    fullname = request.form.get('fullname', '')

    users = load_users()
    if username in users:
        users[username]['email'] = email
        users[username]['fullname'] = fullname
        save_users(users)
    return redirect(url_for('user_profile'))


if __name__ == '__main__':
    app.run(debug=True)
