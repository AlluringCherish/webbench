from flask import Flask, request, session, jsonify, redirect, render_template
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Set secret key for sessions

DATA_DIR = 'data'

# Utility functions for file operations

def read_file_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
    return [line for line in lines if line.strip()]

def write_file_lines(filename, lines):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def parse_pipe_line(line):
    return [x.strip() for x in line.split('|')]

def join_pipe_line(fields):
    return '|'.join(str(x) for x in fields)

# Data loading helpers

def load_users():
    lines = read_file_lines('users.txt')
    users = {}
    for line in lines:
        username, email, fullname = parse_pipe_line(line)
        users[username] = {'email': email, 'fullname': fullname}
    return users

def load_courses(include_inactive=False):
    lines = read_file_lines('courses.txt')
    courses = {}
    for line in lines:
        parts = parse_pipe_line(line)
        if len(parts) < 7:
            continue
        course_id = int(parts[0])
        title = parts[1]
        description = parts[2]
        category = parts[3]
        level = parts[4]
        duration = parts[5]
        status = parts[6]
        if not include_inactive and status.lower() != 'active':
            continue
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

def load_enrollments():
    lines = read_file_lines('enrollments.txt')
    enrollments = []
    for line in lines:
        parts = parse_pipe_line(line)
        if len(parts) < 6:
            continue
        enrollment = {
            'enrollment_id': parts[0],
            'username': parts[1],
            'course_id': int(parts[2]),
            'enrollment_date': parts[3],
            'progress': int(parts[4]),
            'status': parts[5]
        }
        enrollments.append(enrollment)
    return enrollments

def load_assignments():
    lines = read_file_lines('assignments.txt')
    assignments = {}
    for line in lines:
        parts = parse_pipe_line(line)
        if len(parts) < 7:
            continue
        assignment_id = int(parts[0])
        assignments[assignment_id] = {
            'assignment_id': assignment_id,
            'course_id': int(parts[1]),
            'title': parts[2],
            'description': parts[3],
            'due_date': parts[4],
            'max_points': parts[5]
        }
    return assignments

def load_submissions():
    lines = read_file_lines('submissions.txt')
    submissions = []
    for line in lines:
        parts = parse_pipe_line(line)
        if len(parts) < 7:
            continue
        submission = {
            'submission_id': parts[0],
            'assignment_id': int(parts[1]),
            'username': parts[2],
            'submission_text': parts[3],
            'submit_date': parts[4],
            'grade': parts[5],
            'feedback': parts[6]
        }
        submissions.append(submission)
    return submissions

def load_certificates():
    lines = read_file_lines('certificates.txt')
    certificates = []
    for line in lines:
        parts = parse_pipe_line(line)
        if len(parts) < 4:
            continue
        certificate = {
            'certificate_id': parts[0],
            'username': parts[1],
            'course_id': int(parts[2]),
            'issue_date': parts[3]
        }
        certificates.append(certificate)
    return certificates

# Write back helpers

def save_enrollments(enrollments):
    lines = []
    for e in enrollments:
        lines.append(join_pipe_line([
            e['enrollment_id'], e['username'], e['course_id'], e['enrollment_date'], e['progress'], e['status']
        ]))
    write_file_lines('enrollments.txt', lines)

def save_submissions(submissions):
    lines = []
    for s in submissions:
        lines.append(join_pipe_line([
            s['submission_id'], s['assignment_id'], s['username'], s['submission_text'], s['submit_date'], s['grade'], s['feedback']
        ]))
    write_file_lines('submissions.txt', lines)

def save_certificates(certificates):
    lines = []
    for c in certificates:
        lines.append(join_pipe_line([
            c['certificate_id'], c['username'], c['course_id'], c['issue_date']
        ]))
    write_file_lines('certificates.txt', lines)

# Helper: Check user login

def get_logged_in_username():
    username = session.get('username')
    if not username:
        return None
    return username

# Generate new unique id for given records list

def generate_new_id(records, key_name):
    max_id = 0
    for r in records:
        try:
            rid = int(r[key_name])
            if rid > max_id:
                max_id = rid
        except ValueError:
            continue
    return str(max_id + 1)

# 1. /dashboard GET
@app.route('/dashboard', methods=['GET'])
def dashboard():
    username = get_logged_in_username()
    if not username:
        return redirect('/login')

    users = load_users()
    user = users.get(username)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    enrollments = load_enrollments()
    user_enrollments = [e for e in enrollments if e['username'] == username]

    courses = load_courses(include_inactive=True)

    enrolled_courses = []
    for e in user_enrollments:
        c = courses.get(e['course_id'])
        if not c:
            continue
        enrolled_courses.append({
            'course_id': e['course_id'],
            'title': c['title'],
            'progress': e['progress']
        })

    return render_template('dashboard.html', fullname=user['fullname'], enrolled_courses=enrolled_courses)

# 2. /courses/catalog GET
@app.route('/courses/catalog', methods=['GET'])
def courses_catalog():
    username = get_logged_in_username()
    if not username:
        return redirect('/login')

    search = request.args.get('search', '')

    courses = load_courses()  # only active

    filtered = []
    if search:
        query = search.lower()
        for c in courses.values():
            if query in c['title'].lower() or query in c['category'].lower():
                filtered.append(c)
    else:
        filtered = list(courses.values())

    # Only return required fields
    result = []
    for c in filtered:
        result.append({
            'course_id': c['course_id'],
            'title': c['title'],
            'description': c['description'],
            'category': c['category'],
            'level': c['level'],
            'duration': c['duration']
        })

    return render_template('catalog.html', courses=result)

# 3. /courses/<int:course_id> GET and POST /enroll
@app.route('/courses/<int:course_id>', methods=['GET', 'POST'])
def course_details(course_id):
    username = get_logged_in_username()
    if not username:
        return redirect('/login')

    courses = load_courses(include_inactive=True)
    course = courses.get(course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404

    enrollments = load_enrollments()
    user_enrollments = [e for e in enrollments if e['username'] == username and e['course_id'] == course_id]
    is_enrolled = len(user_enrollments) > 0

    syllabus = 'This course covers various important topics related to the subject.'  # placeholder

    if request.method == 'POST':
        # Enroll user
        if is_enrolled:
            return jsonify({'status': 'error', 'message': 'Already enrolled'})

        new_id = generate_new_id(enrollments, 'enrollment_id')
        today_str = datetime.now().strftime('%Y-%m-%d')
        new_enrollment = {
            'enrollment_id': new_id,
            'username': username,
            'course_id': course_id,
            'enrollment_date': today_str,
            'progress': 0,
            'status': 'In Progress'
        }
        enrollments.append(new_enrollment)
        save_enrollments(enrollments)

        return redirect(f'/courses/{course_id}')

    return render_template('course_details.html', course=course, enrolled=is_enrolled, syllabus=syllabus)

# 4. /my-courses GET
@app.route('/my-courses', methods=['GET'])
def my_courses():
    username = get_logged_in_username()
    if not username:
        return redirect('/login')

    enrollments = load_enrollments()
    user_enrollments = [e for e in enrollments if e['username'] == username]
    courses = load_courses(include_inactive=True)

    enrolled_courses = []
    for e in user_enrollments:
        c = courses.get(e['course_id'])
        if not c:
            continue
        enrolled_courses.append({
            'course_id': e['course_id'],
            'title': c['title'],
            'progress': e['progress']
        })

    return render_template('my_courses.html', enrolled_courses=enrolled_courses)

# 5. /course/<int:course_id>/learning GET and POST mark-complete
@app.route('/course/<int:course_id>/learning', methods=['GET', 'POST'])
def course_learning(course_id):
    username = get_logged_in_username()
    if not username:
        return redirect('/login')

    enrollments = load_enrollments()
    enrollment = None
    for e in enrollments:
        if e['username'] == username and e['course_id'] == course_id:
            enrollment = e
            break
    if not enrollment:
        return jsonify({'error': 'Enrollment not found'}), 404

    # Mimic lessons: suppose each course has 5 lessons with fixed titles
    lessons = [
        {'number': 1, 'title': 'Introduction'},
        {'number': 2, 'title': 'Basics'},
        {'number': 3, 'title': 'Intermediate Concepts'},
        {'number': 4, 'title': 'Advanced Topics'},
        {'number': 5, 'title': 'Final Summary'}
    ]

    progress_filename = f'progress_{username}_{course_id}.txt'
    completed_lessons = []
    if os.path.exists(os.path.join(DATA_DIR, progress_filename)):
        lines = read_file_lines(progress_filename)
        for line in lines:
            try:
                lesson_num = int(line.strip())
                completed_lessons.append(lesson_num)
            except Exception:
                continue

    current_lesson = None
    for lesson in lessons:
        if lesson['number'] not in completed_lessons:
            current_lesson = lesson
            break
    if current_lesson is None:
        current_lesson = lessons[-1]

    lesson_content_map = {
        1: 'Welcome to the Introduction lesson.',
        2: 'Basics lesson content goes here.',
        3: 'Intermediate Concepts are explained here.',
        4: 'Advanced Topics for deep dive.',
        5: 'Final Summary and wrap-up.'
    }

    content = lesson_content_map.get(current_lesson['number'], '')

    # Determine if mark complete button enabled: must be next lesson sequentially
    max_completed = max(completed_lessons) if completed_lessons else 0
    can_mark_complete = (current_lesson['number'] == max_completed + 1)

    if request.method == 'POST':
        # Mark lesson complete
        lesson_number = request.form.get('lesson_number')
        try:
            lesson_number_int = int(lesson_number)
        except Exception:
            return jsonify({'status': 'error', 'message': 'Invalid lesson number'}), 400

        if lesson_number_int != max_completed + 1:
            return jsonify({'status': 'error', 'message': 'Lessons must be completed in sequence'}), 400

        completed_lessons.append(lesson_number_int)
        completed_list_sorted = sorted(set(completed_lessons))
        content_lines = [str(num) for num in completed_list_sorted]

        progress = int((len(completed_list_sorted) / len(lessons)) * 100)

        for e in enrollments:
            if e['username'] == username and e['course_id'] == course_id:
                e['progress'] = progress
                if progress == 100:
                    e['status'] = 'Completed'
                break

        certificates = load_certificates()
        cert_exists = any(c['username'] == username and c['course_id'] == course_id for c in certificates)
        if progress == 100 and not cert_exists:
            new_cert_id = generate_new_id(certificates, 'certificate_id')
            issue_date = datetime.now().strftime('%Y-%m-%d')
            certificates.append({
                'certificate_id': new_cert_id,
                'username': username,
                'course_id': course_id,
                'issue_date': issue_date
            })
            save_certificates(certificates)

        # Save progress
        progress_file_path = os.path.join(DATA_DIR, progress_filename)
        with open(progress_file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content_lines))

        save_enrollments(enrollments)

        return redirect(f'/course/{course_id}/learning')

    return render_template('course_learning.html', lessons=lessons, completed_lessons=completed_lessons, current_lesson=current_lesson, can_mark_complete=can_mark_complete)

# 6. /assignments GET
@app.route('/assignments', methods=['GET'])
def assignments():
    username = get_logged_in_username()
    if not username:
        return redirect('/login')

    enrollments = load_enrollments()
    enrolled_course_ids = set(e['course_id'] for e in enrollments if e['username'] == username)

    assignments = load_assignments()
    submissions = load_submissions()

    result = []

    for assignment in assignments.values():
        if assignment['course_id'] not in enrolled_course_ids:
            continue
        submitted = any(
            s['assignment_id'] == assignment['assignment_id'] and s['username'] == username
            for s in submissions
        )
        submission_status = 'Submitted' if submitted else 'Pending'

        result.append({
            'assignment_id': assignment['assignment_id'],
            'course_id': assignment['course_id'],
            'title': assignment['title'],
            'description': assignment['description'],
            'due_date': assignment['due_date'],
            'max_points': assignment['max_points'],
            'submission_status': submission_status
        })

    return render_template('my_assignments.html', assignments=result)

# 7. /assignments/<int:assignment_id>/submit GET and POST
@app.route('/assignments/<int:assignment_id>/submit', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    username = get_logged_in_username()
    if not username:
        return redirect('/login')

    assignments = load_assignments()
    assignment = assignments.get(assignment_id)
    if not assignment:
        return jsonify({'status': 'error', 'message': 'Assignment not found'}), 404

    if request.method == 'GET':
        return render_template('submit_assignment.html', assignment=assignment)

    # POST
    submission_text = request.form.get('submission_text', '').strip()
    if not submission_text:
        return render_template('submit_assignment.html', assignment=assignment, error='Submission text cannot be empty')

    enrollments = load_enrollments()
    enrolled_courses = [e['course_id'] for e in enrollments if e['username'] == username]
    if assignment['course_id'] not in enrolled_courses:
        return render_template('submit_assignment.html', assignment=assignment, error='Not enrolled in course for this assignment')

    submissions = load_submissions()
    new_sub_id = generate_new_id(submissions, 'submission_id')
    submit_date = datetime.now().strftime('%Y-%m-%d')

    new_submission = {
        'submission_id': new_sub_id,
        'assignment_id': assignment_id,
        'username': username,
        'submission_text': submission_text,
        'submit_date': submit_date,
        'grade': '',
        'feedback': ''
    }

    submissions.append(new_submission)
    save_submissions(submissions)

    return redirect('/assignments')

# 8. /certificates GET
@app.route('/certificates', methods=['GET'])
def certificates():
    username = get_logged_in_username()
    if not username:
        return redirect('/login')

    certificates = load_certificates()
    courses = load_courses(include_inactive=True)

    user_certs = [
        {
            'certificate_id': c['certificate_id'],
            'course_id': c['course_id'],
            'course_title': courses[c['course_id']]['title'] if c['course_id'] in courses else 'Unknown',
            'issue_date': c['issue_date']
        }
        for c in certificates if c['username'] == username
    ]

    return render_template('certificates.html', certificates=user_certs)

# 9. /profile GET and POST
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = get_logged_in_username()
    if not username:
        return redirect('/login')

    users = load_users()

    if request.method == 'GET':
        user = users.get(username)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        profile_data = {
            'username': username,
            'email': user['email'],
            'fullname': user['fullname']
        }
        return render_template('profile.html', profile=profile_data)

    # POST
    email = request.form.get('email')
    fullname = request.form.get('fullname')
    if not email or not fullname:
        return render_template('profile.html', profile={'email': email, 'fullname': fullname}, error='Email and fullname required')

    updated = False
    for uname, udata in users.items():
        if uname == username:
            udata['email'] = email
            udata['fullname'] = fullname
            updated = True
            break

    if not updated:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

    lines = []
    for uname, udata in users.items():
        lines.append(join_pipe_line([uname, udata['email'], udata['fullname']]))
    write_file_lines('users.txt', lines)

    return redirect('/profile')

# Login/logout handlers for completeness
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        users = load_users()
        if username in users:
            session['username'] = username
            return redirect('/dashboard')
        else:
            return 'Invalid username', 401
    return '''<form method="post">
                Username: <input type="text" name="username">
                <input type="submit" value="Login">
              </form>'''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
