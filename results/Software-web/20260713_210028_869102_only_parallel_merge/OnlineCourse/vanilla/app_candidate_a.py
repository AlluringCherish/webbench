from flask import Flask, render_template, request, redirect, url_for, flash
import os
import datetime

app = Flask(__name__)
app.secret_key = 'some_secret_key'

DATA_DIR = 'data'

# Assume current logged in user is 'john' for demonstration
CURRENT_USERNAME = 'john'

# Utility functions for reading and writing data files

def read_users():
    users = {}
    path = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                username, email, fullname = line.split('|')
                users[username] = {'email': email, 'fullname': fullname}
    return users


def save_users(users):
    lines = []
    for username, data in users.items():
        lines.append(f"{username}|{data['email']}|{data['fullname']}")
    path = os.path.join(DATA_DIR, 'users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


def read_courses():
    courses = {}
    path = os.path.join(DATA_DIR, 'courses.txt')
    if not os.path.exists(path):
        return courses
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) != 7:
                    continue
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
    path = os.path.join(DATA_DIR, 'enrollments.txt')
    if not os.path.exists(path):
        return enrollments
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                enrollment = {
                    'enrollment_id': parts[0],
                    'username': parts[1],
                    'course_id': parts[2],
                    'enrollment_date': parts[3],
                    'progress': int(parts[4]),
                    'status': parts[5]
                }
                enrollments.append(enrollment)
    return enrollments


def save_enrollments(enrollments):
    lines = []
    for e in enrollments:
        lines.append(f"{e['enrollment_id']}|{e['username']}|{e['course_id']}|{e['enrollment_date']}|{e['progress']}|{e['status']}")
    path = os.path.join(DATA_DIR, 'enrollments.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


def read_assignments():
    assignments = []
    path = os.path.join(DATA_DIR, 'assignments.txt')
    if not os.path.exists(path):
        return assignments
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                assignment = {
                    'assignment_id': parts[0],
                    'course_id': parts[1],
                    'title': parts[2],
                    'description': parts[3],
                    'due_date': parts[4],
                    'max_points': parts[5]
                }
                assignments.append(assignment)
    return assignments


def read_submissions():
    submissions = []
    path = os.path.join(DATA_DIR, 'submissions.txt')
    if not os.path.exists(path):
        return submissions
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                submission = {
                    'submission_id': parts[0],
                    'assignment_id': parts[1],
                    'username': parts[2],
                    'submission_text': parts[3],
                    'submit_date': parts[4],
                    'grade': parts[5] if parts[5] != 'null' else None,
                    'feedback': parts[6]
                }
                submissions.append(submission)
    return submissions


def save_submissions(submissions):
    lines = []
    for s in submissions:
        grade_str = s['grade'] if s['grade'] is not None else 'null'
        lines.append(f"{s['submission_id']}|{s['assignment_id']}|{s['username']}|{s['submission_text']}|{s['submit_date']}|{grade_str}|{s['feedback']}")
    path = os.path.join(DATA_DIR, 'submissions.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


def read_certificates():
    certificates = []
    path = os.path.join(DATA_DIR, 'certificates.txt')
    if not os.path.exists(path):
        return certificates
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) != 4:
                    continue
                cert = {
                    'certificate_id': parts[0],
                    'username': parts[1],
                    'course_id': parts[2],
                    'issue_date': parts[3]
                }
                certificates.append(cert)
    return certificates


def save_certificates(certificates):
    lines = []
    for c in certificates:
        lines.append(f"{c['certificate_id']}|{c['username']}|{c['course_id']}|{c['issue_date']}")
    path = os.path.join(DATA_DIR, 'certificates.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

# As lessons data is not defined in provided files, simulate lessons for each course
# For demonstration, assume each course has 5 lessons with titles: Lesson 1 to Lesson 5

LESSONS_PER_COURSE = 5
LESSONS_CONTENT = {
    str(cid): [f"Lesson {i+1} content for course {cid}" for i in range(LESSONS_PER_COURSE)]
    for cid in range(1, 100)
}


@app.route('/dashboard')
def dashboard():
    users = read_users()
    user = users.get(CURRENT_USERNAME, {'fullname': 'User'})
    fullname = user['fullname']

    enrollments = [e for e in read_enrollments() if e['username'] == CURRENT_USERNAME]
    courses = read_courses()

    enrolled_courses = []
    for e in enrollments:
        course = courses.get(e['course_id'])
        if course:
            enrolled_courses.append({
                'course_id': e['course_id'],
                'title': course['title'],
                'progress': e['progress'],
                'status': e['status']
            })

    return render_template('dashboard.html', fullname=fullname, enrolled_courses=enrolled_courses)


@app.route('/courses/catalog', methods=['GET', 'POST'])
def course_catalog():
    courses = read_courses()
    active_courses = [c for c in courses.values() if c['status'] == 'Active']

    search_query = ''
    if request.method == 'POST':
        search_query = request.form.get('search', '').strip().lower()
        if search_query:
            active_courses = [c for c in active_courses if search_query in c['title'].lower() or search_query in c['category'].lower()]

    return render_template('course_catalog.html', courses=active_courses, search_query=search_query)


@app.route('/courses/details/<course_id>', methods=['GET', 'POST'])
def course_details(course_id):
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        return "Course not found", 404

    enrollments = read_enrollments()
    user_enrollment = None
    for e in enrollments:
        if e['username'] == CURRENT_USERNAME and e['course_id'] == course_id:
            user_enrollment = e
            break

    if request.method == 'POST':
        if not user_enrollment:
            # enroll the user
            max_id = 0
            if enrollments:
                max_id = max(int(e['enrollment_id']) for e in enrollments)
            new_id = str(max_id + 1)
            today = datetime.date.today().isoformat()
            new_enrollment = {
                'enrollment_id': new_id,
                'username': CURRENT_USERNAME,
                'course_id': course_id,
                'enrollment_date': today,
                'progress': 0,
                'status': 'In Progress'
            }
            enrollments.append(new_enrollment)
            save_enrollments(enrollments)
            user_enrollment = new_enrollment
            flash('Enrolled successfully!')

    return render_template('course_details.html', course=course, enrolled=(user_enrollment is not None))


@app.route('/courses/mine')
def my_courses():
    enrollments = read_enrollments()
    user_enrollments = [e for e in enrollments if e['username'] == CURRENT_USERNAME]
    courses = read_courses()

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

    return render_template('my_courses.html', enrolled_courses=enrolled_courses)


@app.route('/courses/learn/<course_id>', methods=['GET', 'POST'])
def course_learning(course_id):
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        return "Course not found", 404

    enrollments = read_enrollments()
    enrollment = None
    for e in enrollments:
        if e['username'] == CURRENT_USERNAME and e['course_id'] == course_id:
            enrollment = e
            break

    if not enrollment:
        flash('You are not enrolled in this course.')
        return redirect(url_for('my_courses'))

    # Get lessons for the course
    lessons = LESSONS_CONTENT.get(course_id, [])
    total_lessons = len(lessons)

    # Assume we store completed lessons count based on progress (integer progress percent)
    # Calculate completed lessons as integer portion of progress * total_lessons / 100
    completed_lessons = int(enrollment['progress'] * total_lessons / 100)

    current_lesson_index = completed_lessons if completed_lessons < total_lessons else total_lessons - 1

    if request.method == 'POST':
        # Mark current lesson complete if it's next in sequence
        # Only allow marking complete if current lesson is the next incomplete one
        if completed_lessons < total_lessons and completed_lessons == current_lesson_index:
            completed_lessons += 1
            new_progress = int((completed_lessons / total_lessons) * 100)
            enrollment['progress'] = new_progress
            if new_progress >= 100:
                enrollment['progress'] = 100
                enrollment['status'] = 'Completed'
                # Generate certificate if not exists
                certificates = read_certificates()
                cert_exists = any(c['username'] == CURRENT_USERNAME and c['course_id'] == course_id for c in certificates)
                if not cert_exists:
                    max_cert_id = 0
                    if certificates:
                        max_cert_id = max(int(c['certificate_id']) for c in certificates)
                    new_cert = {
                        'certificate_id': str(max_cert_id + 1),
                        'username': CURRENT_USERNAME,
                        'course_id': course_id,
                        'issue_date': datetime.date.today().isoformat()
                    }
                    certificates.append(new_cert)
                    save_certificates(certificates)
            # Save enrollment update
            save_enrollments(enrollments)
            flash('Lesson marked as completed.')
        else:
            flash('You must complete lessons in sequence.')

    lesson_content = lessons[current_lesson_index] if lessons else 'No lessons available.'

    return render_template('course_learning.html', course=course, lessons=lessons, current_index=current_lesson_index, lesson_content=lesson_content, can_mark_complete=(completed_lessons == current_lesson_index and completed_lessons < total_lessons))


@app.route('/assignments')
def my_assignments():
    enrollments = read_enrollments()
    user_courses = {e['course_id'] for e in enrollments if e['username'] == CURRENT_USERNAME}
    assignments = read_assignments()
    submissions = read_submissions()

    relevant_assignments = [a for a in assignments if a['course_id'] in user_courses]

    assignments_status = []
    for a in relevant_assignments:
        submission = next((s for s in submissions if s['assignment_id'] == a['assignment_id'] and s['username'] == CURRENT_USERNAME), None)
        status = 'Submitted' if submission else 'Pending'
        grade = submission['grade'] if submission and submission['grade'] else ''
        assignments_status.append({
            'assignment_id': a['assignment_id'],
            'title': a['title'],
            'due_date': a['due_date'],
            'status': status,
            'grade': grade
        })

    return render_template('my_assignments.html', assignments=assignments_status)


@app.route('/assignments/submit/<assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    assignments = read_assignments()
    assignment = next((a for a in assignments if a['assignment_id'] == assignment_id), None)
    if not assignment:
        return "Assignment not found", 404

    if request.method == 'POST':
        submission_text = request.form.get('submission_text', '').strip()
        if not submission_text:
            flash('Submission text cannot be empty')
        else:
            submissions = read_submissions()
            max_id = 0
            if submissions:
                max_id = max(int(s['submission_id']) for s in submissions)
            new_id = str(max_id + 1)
            today = datetime.date.today().isoformat()
            new_submission = {
                'submission_id': new_id,
                'assignment_id': assignment_id,
                'username': CURRENT_USERNAME,
                'submission_text': submission_text.replace('|',' '),
                'submit_date': today,
                'grade': None,
                'feedback': ''
            }
            submissions.append(new_submission)
            save_submissions(submissions)
            flash('Assignment submitted successfully!')
            return redirect(url_for('my_assignments'))

    return render_template('submit_assignment.html', assignment=assignment)


@app.route('/certificates')
def certificates():
    certificates = read_certificates()
    user_certificates = [c for c in certificates if c['username'] == CURRENT_USERNAME]
    courses = read_courses()
    enrollments = read_enrollments()

    # Only show certificates if enrollment status is Completed
    completed_course_ids = {e['course_id'] for e in enrollments if e['username'] == CURRENT_USERNAME and e['status'] == 'Completed'}

    filtered_certificates = [c for c in user_certificates if c['course_id'] in completed_course_ids]

    certs_display = []
    for cert in filtered_certificates:
        course = courses.get(cert['course_id'])
        if course:
            certs_display.append({
                'certificate_id': cert['certificate_id'],
                'course_id': cert['course_id'],
                'course_title': course['title'],
                'issue_date': cert['issue_date']
            })

    return render_template('certificates.html', certificates=certs_display)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = read_users()
    user = users.get(CURRENT_USERNAME)
    if not user:
        return "User not found", 404

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        fullname = request.form.get('fullname', '').strip()

        if not email or not fullname:
            flash('Email and Full name cannot be empty')
        else:
            users[CURRENT_USERNAME]['email'] = email
            users[CURRENT_USERNAME]['fullname'] = fullname
            save_users(users)
            flash('Profile updated successfully!')

    return render_template('profile.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)
