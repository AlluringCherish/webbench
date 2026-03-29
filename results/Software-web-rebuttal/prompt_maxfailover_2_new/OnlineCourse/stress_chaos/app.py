from flask import Flask, render_template, redirect, url_for, request, abort
import os
from datetime import datetime

app = Flask(__name__)
app.config['DATA_DIR'] = 'data'

# Helper functions for file I/O

def read_file(filename):
    path = os.path.join(app.config['DATA_DIR'], filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return [line.split('|') for line in lines]


def write_file(filename, records):
    path = os.path.join(app.config['DATA_DIR'], filename)
    with open(path, 'w', encoding='utf-8') as f:
        for record in records:
            f.write('|'.join(str(field) for field in record) + '\n')


def get_user(username):
    users = read_file('users.txt')
    for u in users:
        if len(u) >= 3 and u[0] == username:
            return {'username': u[0], 'email': u[1], 'fullname': u[2]}
    return None


def get_courses():
    courses = read_file('courses.txt')
    result = []
    for c in courses:
        if len(c) >= 7:
            result.append({
                'course_id': int(c[0]),
                'title': c[1],
                'description': c[2],
                'category': c[3],
                'level': c[4],
                'duration': c[5],
                'status': c[6]
            })
    return result


def get_enrollments(username):
    enrollments = read_file('enrollments.txt')
    user_enrollments = []
    for e in enrollments:
        if len(e) >= 6 and e[1] == username:
            try:
                user_enrollments.append({
                    'enrollment_id': int(e[0]),
                    'username': e[1],
                    'course_id': int(e[2]),
                    'enrollment_date': e[3],
                    'progress': int(e[4]),
                    'status': e[5]
                })
            except ValueError:
                continue
    return user_enrollments


def save_enrollments(enrollments):
    records = []
    for e in enrollments:
        records.append([
            str(e['enrollment_id']), e['username'], str(e['course_id']), e['enrollment_date'], str(e['progress']), e['status']
        ])
    write_file('enrollments.txt', records)


def get_assignments():
    assigns = read_file('assignments.txt')
    result = []
    for a in assigns:
        if len(a) >= 6:
            try:
                result.append({
                    'assignment_id': int(a[0]),
                    'course_id': int(a[1]),
                    'title': a[2],
                    'description': a[3],
                    'due_date': a[4],
                    'max_points': int(a[5])
                })
            except ValueError:
                continue
    return result


def get_submissions():
    subs = read_file('submissions.txt')
    result = []
    for s in subs:
        if len(s) >= 7:
            try:
                grade = None
                if s[5] != '':
                    grade = int(s[5])
                result.append({
                    'submission_id': int(s[0]),
                    'assignment_id': int(s[1]),
                    'username': s[2],
                    'submission_text': s[3],
                    'submit_date': s[4],
                    'grade': grade,
                    'feedback': s[6]
                })
            except ValueError:
                continue
    return result


def save_submissions(submissions):
    records = []
    for s in submissions:
        grade_field = '' if s['grade'] is None else str(s['grade'])
        records.append([
            str(s['submission_id']), str(s['assignment_id']), s['username'], s['submission_text'], s['submit_date'], grade_field, s['feedback']
        ])
    write_file('submissions.txt', records)


def get_certificates(username):
    certs = read_file('certificates.txt')
    result = []
    for c in certs:
        if len(c) >= 4 and c[1] == username:
            try:
                result.append({
                    'certificate_id': int(c[0]),
                    'username': c[1],
                    'course_id': int(c[2]),
                    'issue_date': c[3]
                })
            except ValueError:
                continue
    return result


def save_certificates(certificates):
    records = []
    for c in certificates:
        records.append([
            str(c['certificate_id']), c['username'], str(c['course_id']), c['issue_date']
        ])
    write_file('certificates.txt', records)


def get_next_id(filename, id_index=0):
    records = read_file(filename)
    max_id = 0
    for r in records:
        try:
            curr_id = int(r[id_index])
            if curr_id > max_id:
                max_id = curr_id
        except:
            continue
    return max_id + 1


@app.route('/')
def root():
    # Redirect to /dashboard
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # For simplicity, assume username is 'john'
    username = 'john'
    user = get_user(username)
    if user is None:
        abort(404)
    enrollments = get_enrollments(username)
    courses = get_courses()
    enrolled_courses = []
    for e in enrollments:
        course = next((c for c in courses if c['course_id'] == e['course_id']), None)
        if course:
            enrolled_courses.append({
                'course_id': course['course_id'],
                'title': course['title'],
                'progress': e['progress']
            })
    return render_template('dashboard.html', username=username, fullname=user['fullname'], enrolled_courses=enrolled_courses)


@app.route('/catalog')
def catalog():
    username = 'john'
    user = get_user(username)
    if not user:
        abort(404)
    courses = get_courses()
    simple_courses = [{'course_id': c['course_id'], 'title': c['title'], 'description': c['description']} for c in courses]
    return render_template('catalog.html', username=username, courses=simple_courses)


@app.route('/course/<int:course_id>', methods=['GET', 'POST'])
def course_details(course_id):
    username = 'john'
    user = get_user(username)
    if not user:
        abort(404)
    course = next((c for c in get_courses() if c['course_id'] == course_id), None)
    if not course:
        abort(404)
    enrollments = get_enrollments(username)
    already_enrolled = any(e['course_id'] == course_id for e in enrollments)

    if request.method == 'POST':
        if not already_enrolled:
            enrollments = get_enrollments(username)
            new_id = get_next_id('enrollments.txt')
            enrollments.append({
                'enrollment_id': new_id,
                'username': username,
                'course_id': course_id,
                'enrollment_date': datetime.now().strftime('%Y-%m-%d'),
                'progress': 0,
                'status': 'In Progress'
            })
            save_enrollments(enrollments)
            return redirect(url_for('my_courses'))

    return render_template('course_details.html', username=username, course=course, already_enrolled=already_enrolled)


@app.route('/my-courses')
def my_courses():
    username = 'john'
    user = get_user(username)
    if not user:
        abort(404)
    enrollments = get_enrollments(username)
    courses = get_courses()
    enrolled_courses = []
    for e in enrollments:
        course = next((c for c in courses if c['course_id'] == e['course_id']), None)
        if course:
            enrolled_courses.append({
                'course_id': course['course_id'],
                'title': course['title'],
                'progress': e['progress'],
                'status': e['status']
            })
    return render_template('my_courses.html', username=username, enrolled_courses=enrolled_courses)


@app.route('/learn/<int:course_id>', methods=['GET', 'POST'])
def course_learning(course_id):
    username = 'john'
    user = get_user(username)
    if not user:
        abort(404)
    course = next((c for c in get_courses() if c['course_id'] == course_id), None)
    if not course:
        abort(404)
    enrollments = get_enrollments(username)
    enrollment = next((e for e in enrollments if e['course_id'] == course_id), None)
    if not enrollment:
        abort(403)  # Not enrolled

    # Hardcoded lessons for demonstration
    lessons = [
        {'lesson_id': 1, 'title': 'Lesson 1', 'content': 'Content of Lesson 1'},
        {'lesson_id': 2, 'title': 'Lesson 2', 'content': 'Content of Lesson 2'},
        {'lesson_id': 3, 'title': 'Lesson 3', 'content': 'Content of Lesson 3'}
    ]

    progress = enrollment['progress']
    total_lessons = len(lessons)
    # current lesson index based on progress
    current_lesson_index = min(progress // (100 // total_lessons), total_lessons - 1)
    current_lesson = lessons[current_lesson_index]

    can_mark_complete = progress < 100

    if request.method == 'POST' and can_mark_complete:
        progress = min(progress + 33, 100)
        enrollment['progress'] = progress
        if progress == 100:
            enrollment['status'] = 'Completed'
            # Issue certificate
            certificates = get_certificates(username)
            already_certified = any(c['course_id'] == course_id for c in certificates)
            if not already_certified:
                new_cert_id = get_next_id('certificates.txt')
                certificate = {
                    'certificate_id': new_cert_id,
                    'username': username,
                    'course_id': course_id,
                    'issue_date': datetime.now().strftime('%Y-%m-%d')
                }
                certificates.append(certificate)
                save_certificates(certificates)
        save_enrollments(enrollments)

    return render_template('course_learning.html', username=username, course=course, lessons=lessons, current_lesson=current_lesson, progress=progress, can_mark_complete=can_mark_complete)


@app.route('/assignments')
def my_assignments():
    username = 'john'
    user = get_user(username)
    if not user:
        abort(404)
    assignments = get_assignments()
    submissions = get_submissions()

    # Map assignment_id to submission dict or None
    submissions_dict = {}
    for a in assignments:
        sub = next((s for s in submissions if s['assignment_id'] == a['assignment_id'] and s['username'] == username), None)
        submissions_dict[a['assignment_id']] = sub

    return render_template('assignments.html', username=username, assignments=assignments, submissions=submissions_dict)


@app.route('/submit-assignment/<int:assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    username = 'john'
    user = get_user(username)
    if not user:
        abort(404)
    assignment = next((a for a in get_assignments() if a['assignment_id'] == assignment_id), None)
    if not assignment:
        abort(404)

    submissions = get_submissions()
    submission_status = None
    already_submitted = any(s['assignment_id'] == assignment_id and s['username'] == username for s in submissions)

    if request.method == 'POST':
        submission_text = request.form.get('submission_text', '').strip()
        if submission_text:
            new_id = get_next_id('submissions.txt')
            now = datetime.now().strftime('%Y-%m-%d')
            # Remove old submission if exists
            submissions = [s for s in submissions if not (s['assignment_id'] == assignment_id and s['username'] == username)]
            submissions.append({
                'submission_id': new_id,
                'assignment_id': assignment_id,
                'username': username,
                'submission_text': submission_text,
                'submit_date': now,
                'grade': None,
                'feedback': ''
            })
            save_submissions(submissions)
            submission_status = 'Submitted'
    else:
        submission_status = 'Submitted' if already_submitted else None

    return render_template('submit_assignment.html', username=username, assignment=assignment, submission_status=submission_status)


@app.route('/certificates')
def certificates():
    username = 'john'
    user = get_user(username)
    if not user:
        abort(404)
    certs = get_certificates(username)
    courses = get_courses()

    certs_with_titles = []
    for c in certs:
        course = next((co for co in courses if co['course_id'] == c['course_id']), None)
        title = course['title'] if course else ''
        certs_with_titles.append({
            'certificate_id': c['certificate_id'],
            'course_id': c['course_id'],
            'title': title,
            'issue_date': c['issue_date']
        })

    return render_template('certificates.html', username=username, certificates=certs_with_titles)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = 'john'
    user = get_user(username)
    if not user:
        abort(404)

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        fullname = request.form.get('fullname', '').strip()
        if email and fullname:
            users = read_file('users.txt')
            for i, u in enumerate(users):
                if u[0] == username:
                    users[i][1] = email
                    users[i][2] = fullname
                    break
            write_file('users.txt', users)
            return redirect(url_for('profile'))

    return render_template('profile.html', username=username, email=user['email'], fullname=user['fullname'])


if __name__ == '__main__':
    app.run(debug=True, port=5000)
