from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

DATA_DIR = 'data'

# Helper functions to read and write pipe-delimited data files

def read_users():
    users = []
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    username, email, fullname = line.split('|')
                    users.append({'username': username, 'email': email, 'fullname': fullname})
    except FileNotFoundError:
        pass
    return users


def write_users(users):
    with open(os.path.join(DATA_DIR, 'users.txt'), 'w', encoding='utf-8') as f:
        for user in users:
            f.write(f"{user['username']}|{user['email']}|{user['fullname']}\n")


def read_courses():
    courses = []
    try:
        with open(os.path.join(DATA_DIR, 'courses.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    course_id, title, description, category, level, duration, status = line.split('|')
                    courses.append({
                        'course_id': course_id,
                        'title': title,
                        'description': description,
                        'category': category,
                        'level': level,
                        'duration': duration,
                        'status': status
                    })
    except FileNotFoundError:
        pass
    return courses


def write_courses(courses):
    with open(os.path.join(DATA_DIR, 'courses.txt'), 'w', encoding='utf-8') as f:
        for course in courses:
            f.write(f"{course['course_id']}|{course['title']}|{course['description']}|{course['category']}|{course['level']}|{course['duration']}|{course['status']}\n")


def read_enrollments():
    enrollments = []
    try:
        with open(os.path.join(DATA_DIR, 'enrollments.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
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
    with open(os.path.join(DATA_DIR, 'enrollments.txt'), 'w', encoding='utf-8') as f:
        for e in enrollments:
            f.write(f"{e['enrollment_id']}|{e['username']}|{e['course_id']}|{e['enrollment_date']}|{e['progress']}|{e['status']}\n")


def read_assignments():
    assignments = []
    try:
        with open(os.path.join(DATA_DIR, 'assignments.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    assignment_id, course_id, title, description, due_date, max_points = line.split('|')
                    assignments.append({
                        'assignment_id': assignment_id,
                        'course_id': course_id,
                        'title': title,
                        'description': description,
                        'due_date': due_date,
                        'max_points': int(max_points)
                    })
    except FileNotFoundError:
        pass
    return assignments


def write_assignments(assignments):
    with open(os.path.join(DATA_DIR, 'assignments.txt'), 'w', encoding='utf-8') as f:
        for a in assignments:
            f.write(f"{a['assignment_id']}|{a['course_id']}|{a['title']}|{a['description']}|{a['due_date']}|{a['max_points']}\n")


def read_submissions():
    submissions = []
    try:
        with open(os.path.join(DATA_DIR, 'submissions.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
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
                    else:
                        # Defensive fallback if data length incorrect
                        continue
    except FileNotFoundError:
        pass
    return submissions


def write_submissions(submissions):
    with open(os.path.join(DATA_DIR, 'submissions.txt'), 'w', encoding='utf-8') as f:
        for s in submissions:
            f.write(f"{s['submission_id']}|{s['assignment_id']}|{s['username']}|{s['submission_text']}|{s['submit_date']}|{s['grade']}|{s['feedback']}\n")


def read_certificates():
    certificates = []
    try:
        with open(os.path.join(DATA_DIR, 'certificates.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
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
    with open(os.path.join(DATA_DIR, 'certificates.txt'), 'w', encoding='utf-8') as f:
        for c in certificates:
            f.write(f"{c['certificate_id']}|{c['username']}|{c['course_id']}|{c['issue_date']}\n")


# We define a "logged-in user" for demonstration purposes.
# TODO: For real application, integrate proper authentication
LOGGED_IN_USERNAME = 'john'  # Default logged-in user for demonstration


def get_logged_in_user():
    users = read_users()
    for user in users:
        if user['username'] == LOGGED_IN_USERNAME:
            return user
    return None  # If user not found


def get_course_by_id(course_id):
    courses = read_courses()
    for course in courses:
        if course['course_id'] == course_id:
            return course
    return None


def get_enrollment(username, course_id):
    enrollments = read_enrollments()
    for e in enrollments:
        if e['username'] == username and e['course_id'] == course_id:
            return e
    return None


def create_enrollment(username, course_id):
    enrollments = read_enrollments()
    # Generate a new enrollment_id
    max_id = 0
    for e in enrollments:
        try:
            eid = int(e['enrollment_id'])
            if eid > max_id:
                max_id = eid
        except:
            pass
    new_id = str(max_id + 1)
    enrollment_date = datetime.now().strftime('%Y-%m-%d')
    new_enrollment = {
        'enrollment_id': new_id,
        'username': username,
        'course_id': course_id,
        'enrollment_date': enrollment_date,
        'progress': 0,
        'status': 'In Progress'
    }
    enrollments.append(new_enrollment)
    write_enrollments(enrollments)
    return new_enrollment


def update_enrollment_progress(username, course_id, progress):
    enrollments = read_enrollments()
    updated = False
    for e in enrollments:
        if e['username'] == username and e['course_id'] == course_id:
            e['progress'] = progress
            if progress >= 100:
                e['progress'] = 100
                e['status'] = 'Completed'
            else:
                e['status'] = 'In Progress'
            updated = True
            break
    if updated:
        write_enrollments(enrollments)
    return updated


def get_lessons_for_course(course_id):
    # For demonstration, we simulate lessons
    # Since lessons are not persisted, create dummy lessons
    # We'll create 5 lessons per course with ids 1 to 5
    lessons = []
    for i in range(1, 6):
        lessons.append({
            'lesson_id': str(i),
            'title': f'Lesson {i}',
            'content': f'Content for lesson {i} of course {course_id}'
        })
    return lessons


def get_assignments_for_user(username):
    assignments = read_assignments()
    submissions = read_submissions()
    user_courses = set(e['course_id'] for e in read_enrollments() if e['username'] == username)
    user_assignments = [a for a in assignments if a['course_id'] in user_courses]
    # No filtering for status
    return user_assignments, submissions


def get_assignment_by_id(assignment_id):
    assignments = read_assignments()
    for a in assignments:
        if a['assignment_id'] == assignment_id:
            return a
    return None


def get_submissions_for_assignment(assignment_id, username=None):
    submissions = read_submissions()
    if username:
        return [s for s in submissions if s['assignment_id'] == assignment_id and s['username'] == username]
    else:
        return [s for s in submissions if s['assignment_id'] == assignment_id]


def create_submission(assignment_id, username, submission_text):
    submissions = read_submissions()
    max_id = 0
    for s in submissions:
        try:
            sid = int(s['submission_id'])
            if sid > max_id:
                max_id = sid
        except:
            pass
    new_id = str(max_id + 1)
    submit_date = datetime.now().strftime('%Y-%m-%d')
    new_sub = {
        'submission_id': new_id,
        'assignment_id': assignment_id,
        'username': username,
        'submission_text': submission_text,
        'submit_date': submit_date,
        'grade': '',
        'feedback': ''
    }
    submissions.append(new_sub)
    write_submissions(submissions)
    return new_sub


def get_certificates_for_user(username):
    certificates = read_certificates()
    user_certs = [c for c in certificates if c['username'] == username]
    return user_certs


def create_certificate(username, course_id):
    certificates = read_certificates()
    max_id = 0
    for c in certificates:
        try:
            cid = int(c['certificate_id'])
            if cid > max_id:
                max_id = cid
        except:
            pass
    new_id = str(max_id + 1)
    issue_date = datetime.now().strftime('%Y-%m-%d')
    new_cert = {
        'certificate_id': new_id,
        'username': username,
        'course_id': course_id,
        'issue_date': issue_date
    }
    certificates.append(new_cert)
    write_certificates(certificates)
    return new_cert


def update_user_profile(username, email, fullname):
    users = read_users()
    updated = False
    for user in users:
        if user['username'] == username:
            user['email'] = email
            user['fullname'] = fullname
            updated = True
            break
    if updated:
        write_users(users)
    return updated


# Flask Routes Implementations

@app.route('/')
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    user = get_logged_in_user()
    if not user:
        return "User not found", 404

    enrollments = read_enrollments()
    courses = read_courses()
    enrolled_courses = []
    for e in enrollments:
        if e['username'] == user['username']:
            course = get_course_by_id(e['course_id'])
            if course:
                enrolled_courses.append({
                    'course_id': course['course_id'],
                    'title': course['title'],
                    'progress': e['progress']
                })

    return render_template('dashboard.html', username=user['username'], fullname=user['fullname'], enrolled_courses=enrolled_courses)


@app.route('/catalog')
def course_catalog():
    courses = read_courses()
    return render_template('catalog.html', courses=courses)


@app.route('/catalog/search', methods=['POST'])
def course_catalog_search():
    query = request.form.get('search', '').strip().lower()
    all_courses = read_courses()
    if not query:
        filtered_courses = all_courses
    else:
        filtered_courses = [c for c in all_courses if query in c['title'].lower() or query in c['description'].lower() or query in c['category'].lower() or query in c['level'].lower()]
    return render_template('catalog.html', courses=filtered_courses)


@app.route('/course/<course_id>')
def course_details(course_id):
    user = get_logged_in_user()
    if not user:
        return "User not found", 404
    course = get_course_by_id(course_id)
    if not course:
        return "Course not found", 404

    enrollment = get_enrollment(user['username'], course_id)
    already_enrolled = enrollment is not None

    return render_template('course_details.html', course=course, already_enrolled=already_enrolled)


@app.route('/course/<course_id>/enroll', methods=['POST'])
def enroll_course(course_id):
    user = get_logged_in_user()
    if not user:
        return "User not found", 404
    course = get_course_by_id(course_id)
    if not course:
        return "Course not found", 404

    enrollment = get_enrollment(user['username'], course_id)
    already_enrolled = enrollment is not None
    enrollment_success = False

    if not already_enrolled:
        create_enrollment(user['username'], course_id)
        enrollment_success = True

    # Refresh enrollment status
    enrollment = get_enrollment(user['username'], course_id)
    already_enrolled = enrollment is not None

    return render_template('course_details.html', course=course, already_enrolled=already_enrolled, enrollment_success=enrollment_success)


@app.route('/my-courses')
def my_courses():
    user = get_logged_in_user()
    if not user:
        return "User not found", 404
    enrollments = read_enrollments()
    courses = read_courses()
    enrolled_courses = []
    for e in enrollments:
        if e['username'] == user['username']:
            course = get_course_by_id(e['course_id'])
            if course:
                enrolled_courses.append({
                    'course_id': course['course_id'],
                    'title': course['title'],
                    'progress': e['progress']
                })
    return render_template('my_courses.html', enrolled_courses=enrolled_courses)


@app.route('/course/<course_id>/learn')
def course_learning(course_id):
    user = get_logged_in_user()
    if not user:
        return "User not found", 404

    course = get_course_by_id(course_id)
    if not course:
        return "Course not found", 404

    enrollment = get_enrollment(user['username'], course_id)
    if not enrollment:
        return redirect(url_for('course_details', course_id=course_id))  # Not enrolled, redirect

    lessons = get_lessons_for_course(course_id)

    # progress (% complete) correlates to how many lessons completed
    # Calculate current lesson index based on progress
    # 5 lessons total

    # progress = (completed_lessons / total_lessons) * 100
    total_lessons = len(lessons)
    progress = enrollment['progress']
    completed_lessons_count = int(round(progress / 100 * total_lessons))
    # completed lessons indices (0-based)
    completed_lessons = list(range(completed_lessons_count))

    current_lesson_index = completed_lessons_count if completed_lessons_count < total_lessons else total_lessons - 1

    return render_template('course_learning.html', course=course, lessons=lessons, current_lesson_index=current_lesson_index, completed_lessons=completed_lessons)


@app.route('/course/<course_id>/learn/complete', methods=['POST'])
def mark_lesson_complete(course_id):
    user = get_logged_in_user()
    if not user:
        return "User not found", 404

    course = get_course_by_id(course_id)
    if not course:
        return "Course not found", 404

    enrollment = get_enrollment(user['username'], course_id)
    if not enrollment:
        return redirect(url_for('course_details', course_id=course_id))  # Not enrolled

    lessons = get_lessons_for_course(course_id)
    total_lessons = len(lessons)

    current_progress = enrollment['progress']
    completed_lessons_count = int(round(current_progress / 100 * total_lessons))

    if completed_lessons_count < total_lessons:
        completed_lessons_count += 1
    # Calculate new progress
    new_progress = int(round((completed_lessons_count / total_lessons) * 100))

    update_enrollment_progress(user['username'], course_id, new_progress)

    # Check if need to generate certificate
    certificate_generated = False
    if new_progress >= 100:
        # Check if certificate exists
        certificates = read_certificates()
        existing_cert = next((c for c in certificates if c['username'] == user['username'] and c['course_id'] == course_id), None)
        if not existing_cert:
            create_certificate(user['username'], course_id)
            certificate_generated = True

    # Refresh enrollment and progress after updating
    enrollment = get_enrollment(user['username'], course_id)
    current_progress = enrollment['progress']
    completed_lessons = list(range(completed_lessons_count))
    current_lesson_index = completed_lessons_count if completed_lessons_count < total_lessons else total_lessons - 1

    return render_template('course_learning.html', course=course, lessons=lessons, current_lesson_index=current_lesson_index, progress=current_progress, certificate_generated=certificate_generated, completed_lessons=completed_lessons)


@app.route('/assignments')
def my_assignments():
    user = get_logged_in_user()
    if not user:
        return "User not found", 404
    assignments, submissions = get_assignments_for_user(user['username'])
    return render_template('assignments.html', assignments=assignments, submissions=submissions)


@app.route('/assignment/<assignment_id>/submit', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    user = get_logged_in_user()
    if not user:
        return "User not found", 404

    assignment = get_assignment_by_id(assignment_id)
    if not assignment:
        return "Assignment not found", 404

    if request.method == 'GET':
        return render_template('submit_assignment.html', assignment=assignment)

    # POST handling
    submission_text = request.form.get('submission-text', '').strip()
    submission_success = False
    if submission_text:
        # Create a submission record
        create_submission(assignment_id, user['username'], submission_text)
        submission_success = True

    return render_template('submit_assignment.html', assignment=assignment, submission_success=submission_success)


@app.route('/certificates')
def certificates_page():
    user = get_logged_in_user()
    if not user:
        return "User not found", 404
    certificates = get_certificates_for_user(user['username'])
    courses = {c['course_id']: c['title'] for c in read_courses()}
    return render_template('certificates.html', certificates=certificates, courses=courses)


@app.route('/profile')
def user_profile():
    user = get_logged_in_user()
    if not user:
        return "User not found", 404
    return render_template('user_profile.html', user=user)


@app.route('/profile/update', methods=['POST'])
def update_profile():
    user = get_logged_in_user()
    if not user:
        return "User not found", 404

    email = request.form.get('email', '').strip()
    fullname = request.form.get('fullname', '').strip()

    update_success = False
    if email and fullname:
        update_success = update_user_profile(user['username'], email, fullname)

    # Refresh user data
    user = get_logged_in_user()
    return render_template('user_profile.html', user=user, update_success=update_success)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
