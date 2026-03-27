from flask import Flask, render_template, request, redirect, url_for, flash
import os
import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'supersecretkeyforflasksession'

DATA_DIR = 'data'

# -------- Utility functions for data reading/writing -------- #

def read_pipe_delimited_file(filename, expected_fields_count):
    path = os.path.join(DATA_DIR, filename)
    data = []
    if not os.path.exists(path):
        return data
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != expected_fields_count:
                    continue  # skip malformatted lines
                data.append(parts)
    except Exception:
        pass
    return data


def write_pipe_delimited_file(filename, lines):
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for fields in lines:
                f.write('|'.join(fields) + '\n')
    except Exception:
        pass

# -------- Users -------- #
# users.txt: username|email|fullname

def get_all_users():
    users_raw = read_pipe_delimited_file('users.txt', 3)
    users = []
    for user in users_raw:
        users.append({'username': user[0], 'email': user[1], 'fullname': user[2]})
    return users


def get_user_by_username(username):
    users = get_all_users()
    for user in users:
        if user['username'] == username:
            return user
    return None


def update_user(username, email, fullname):
    users = read_pipe_delimited_file('users.txt', 3)
    updated = False
    for i, fields in enumerate(users):
        if fields[0] == username:
            users[i] = [username, email, fullname]
            updated = True
            break
    if updated:
        write_pipe_delimited_file('users.txt', users)
    return updated


# -------- Courses -------- #
# courses.txt: course_id|title|description|category|level|duration|status

def get_all_courses():
    courses_raw = read_pipe_delimited_file('courses.txt', 7)
    courses = []
    for c in courses_raw:
        courses.append({
            'course_id': c[0], 'title': c[1], 'description': c[2], 'category': c[3],
            'level': c[4], 'duration': c[5], 'status': c[6]
        })
    return courses


def get_course_by_id(course_id):
    courses = get_all_courses()
    for course in courses:
        if course['course_id'] == course_id:
            return course
    return None

# -------- Enrollments -------- #
# enrollments.txt: enrollment_id|username|course_id|enrollment_date|progress|status

def get_all_enrollments():
    enroll_raw = read_pipe_delimited_file('enrollments.txt', 6)
    enrollments = []
    for e in enroll_raw:
        try:
            enrollments.append({
                'enrollment_id': e[0],
                'username': e[1],
                'course_id': e[2],
                'enrollment_date': e[3],
                'progress': int(e[4]),
                'status': e[5]
            })
        except Exception:
            continue
    return enrollments


def get_enrollment(username, course_id):
    enrollments = get_all_enrollments()
    for e in enrollments:
        if e['username'] == username and e['course_id'] == course_id:
            return e
    return None


def add_enrollment(username, course_id):
    enrollments = get_all_enrollments()
    # Generate new enrollment_id as max+1
    max_id = 0
    for e in enrollments:
        try:
            eid = int(e['enrollment_id'])
            if eid > max_id:
                max_id = eid
        except Exception:
            pass
    new_id = str(max_id + 1)
    today_iso = datetime.date.today().isoformat()
    new_entry = [new_id, username, course_id, today_iso, '0', 'In Progress']
    enrollments.append({
        'enrollment_id': new_id, 'username': username, 'course_id': course_id,
        'enrollment_date': today_iso, 'progress': 0, 'status': 'In Progress'
    })
    # Write back all enrollments
    lines = []
    for e in enrollments:
        lines.append([
            e['enrollment_id'], e['username'], e['course_id'], e['enrollment_date'], str(e['progress']), e['status']
        ])
    write_pipe_delimited_file('enrollments.txt', lines)


def update_enrollment(enrollment):
    if not enrollment or 'enrollment_id' not in enrollment:
        return False
    enrollments = get_all_enrollments()
    updated = False
    for i, e in enumerate(enrollments):
        if e['enrollment_id'] == enrollment['enrollment_id']:
            enrollments[i] = enrollment
            updated = True
            break
    if updated:
        lines = []
        for e in enrollments:
            lines.append([
                e['enrollment_id'], e['username'], e['course_id'], e['enrollment_date'], str(e['progress']), e['status']
            ])
        write_pipe_delimited_file('enrollments.txt', lines)
    return updated

# -------- Assignments -------- #
# assignments.txt: assignment_id|course_id|title|description|due_date|max_points

def get_all_assignments():
    assigns_raw = read_pipe_delimited_file('assignments.txt', 6)
    assignments = []
    for a in assigns_raw:
        try:
            assignments.append({
                'assignment_id': a[0],
                'course_id': a[1],
                'title': a[2],
                'description': a[3],
                'due_date': a[4],
                'max_points': int(a[5])
            })
        except Exception:
            continue
    return assignments


def get_assignment_by_id(aid):
    assignments = get_all_assignments()
    for a in assignments:
        if a['assignment_id'] == aid:
            return a
    return None

# -------- Submissions -------- #
# submissions.txt: submission_id|assignment_id|username|submission_text|submit_date|grade|feedback

def get_all_submissions():
    subs_raw = read_pipe_delimited_file('submissions.txt', 7)
    submissions = []
    for s in subs_raw:
        submissions.append({
            'submission_id': s[0],
            'assignment_id': s[1],
            'username': s[2],
            'submission_text': s[3],
            'submit_date': s[4],
            'grade': s[5],
            'feedback': s[6]
        })
    return submissions


def get_submission(username, assignment_id):
    submissions = get_all_submissions()
    for s in submissions:
        if s['username'] == username and s['assignment_id'] == assignment_id:
            return s
    return None


def add_or_update_submission(username, assignment_id, submission_text):
    submissions = get_all_submissions()
    today_iso = datetime.date.today().isoformat()
    existing = None
    max_id = 0
    for s in submissions:
        try:
            sid = int(s['submission_id'])
            if sid > max_id:
                max_id = sid
        except Exception:
            pass
        if s['username'] == username and s['assignment_id'] == assignment_id:
            existing = s
    if existing:
        # update existing
        existing['submission_text'] = submission_text
        existing['submit_date'] = today_iso
        existing['grade'] = ''
        existing['feedback'] = ''
    else:
        # add new
        new_id = str(max_id + 1)
        submissions.append({
            'submission_id': new_id,
            'assignment_id': assignment_id,
            'username': username,
            'submission_text': submission_text,
            'submit_date': today_iso,
            'grade': '',
            'feedback': ''
        })
    # write back
    lines = []
    for s in submissions:
        lines.append([
            s['submission_id'], s['assignment_id'], s['username'], s['submission_text'], s['submit_date'], s['grade'], s['feedback']
        ])
    write_pipe_delimited_file('submissions.txt', lines)

# -------- Certificates -------- #
# certificates.txt: certificate_id|username|course_id|issue_date

def get_all_certificates():
    certs_raw = read_pipe_delimited_file('certificates.txt', 4)
    certificates = []
    for c in certs_raw:
        certificates.append({
            'certificate_id': c[0], 'username': c[1], 'course_id': c[2], 'issue_date': c[3]
        })
    return certificates


def add_certificate(username, course_id):
    certificates = get_all_certificates()
    max_id = 0
    for c in certificates:
        try:
            cid = int(c['certificate_id'])
            if cid > max_id:
                max_id = cid
        except Exception:
            pass
    new_id = str(max_id + 1)
    today_iso = datetime.date.today().isoformat()
    certificates.append({'certificate_id': new_id, 'username': username, 'course_id': course_id, 'issue_date': today_iso})
    lines = []
    for c in certificates:
        lines.append([c['certificate_id'], c['username'], c['course_id'], c['issue_date']])
    write_pipe_delimited_file('certificates.txt', lines)
    return {'certificate_id': new_id, 'username': username, 'course_id': course_id, 'issue_date': today_iso}

# -------- Helper Functions -------- #

# Simulate lessons as subset of assignments titles for progress counting
# Since no separate lessons file, and lessons must be sequenced for progress
# We will consider each assignment of course as a lesson for demo progress

def get_lessons_for_course(course_id):
    assignments = [a for a in get_all_assignments() if a['course_id'] == course_id]
    lessons = []
    for a in assignments:
        lessons.append({'lesson_id': a['assignment_id'], 'title': a['title'], 'content': a['description']})
    return lessons

# Get completed lessons count by counting assignments submission for user and course

def get_completed_lessons_count(username, course_id):
    lessons = get_lessons_for_course(course_id)
    submissions = get_all_submissions()
    completed_lesson_ids = set()
    for sub in submissions:
        if sub['username'] == username:
            # If submission exists for lesson (assignment), consider completed
            for lesson in lessons:
                if lesson['lesson_id'] == sub['assignment_id']:
                    completed_lesson_ids.add(lesson['lesson_id'])
    return len(completed_lesson_ids)


# -------- Routes Implementations -------- #

@app.route('/')
def root():
    # Redirect root to dashboard
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # Since no auth system, assume first user in users.txt is logged in for demo
    users = get_all_users()
    if not users:
        return "No users found", 404
    user = users[0]
    username = user['username']
    fullname = user['fullname']
    # Find user's enrolled courses
    enrollments = [e for e in get_all_enrollments() if e['username'] == username]
    enrolled_courses = []
    for e in enrollments:
        course = get_course_by_id(e['course_id'])
        if course:
            enrolled_courses.append({
                'course_id': course['course_id'],
                'title': course['title'],
                'progress': e['progress']
            })
    return render_template('dashboard.html', username=username, fullname=fullname, enrolled_courses=enrolled_courses)


@app.route('/catalog')
def course_catalog():
    courses = get_all_courses()
    return render_template('catalog.html', courses=courses)


@app.route('/catalog/search', methods=['POST'])
def course_catalog_search():
    query = request.form.get('search', '').strip().lower()
    courses = get_all_courses()
    if query:
        filtered = []
        for c in courses:
            if query in c['title'].lower() or query in c['description'].lower() or query in c['category'].lower():
                filtered.append(c)
        courses = filtered
    return render_template('catalog.html', courses=courses)


@app.route('/course/<course_id>')
def course_details(course_id):
    course = get_course_by_id(course_id)
    if not course:
        return "Course not found", 404
    # Current user
    user = get_all_users()[0] if get_all_users() else None
    username = user['username'] if user else None
    already_enrolled = False
    if username:
        enrollment = get_enrollment(username, course_id)
        already_enrolled = enrollment is not None
    return render_template('course_details.html', course=course, already_enrolled=already_enrolled)


@app.route('/course/<course_id>/enroll', methods=['POST'])
def enroll_course(course_id):
    course = get_course_by_id(course_id)
    if not course:
        return "Course not found", 404
    user = get_all_users()[0] if get_all_users() else None
    if not user:
        return "User not found", 404
    username = user['username']
    enrollment = get_enrollment(username, course_id)
    already_enrolled = enrollment is not None
    enrollment_success = False
    if not already_enrolled:
        add_enrollment(username, course_id)
        enrollment_success = True
        already_enrolled = True
    # Return course details with enrollment_success flag
    return render_template('course_details.html', course=course, already_enrolled=already_enrolled, enrollment_success=enrollment_success)


@app.route('/my-courses')
def my_courses():
    user = get_all_users()[0] if get_all_users() else None
    if not user:
        return "User not found", 404
    username = user['username']
    enrollments = [e for e in get_all_enrollments() if e['username'] == username]
    enrolled_courses = []
    for e in enrollments:
        course = get_course_by_id(e['course_id'])
        if course:
            enrolled_courses.append({
                'course_id': course['course_id'],
                'title': course['title'],
                'progress': e['progress']
            })
    return render_template('my_courses.html', enrolled_courses=enrolled_courses)


@app.route('/my-courses/learn/<course_id>')
def course_learning(course_id):
    user = get_all_users()[0] if get_all_users() else None
    if not user:
        return "User not found", 404
    username = user['username']
    course = get_course_by_id(course_id)
    if not course:
        return "Course not found", 404
    enrollment = get_enrollment(username, course_id)
    if not enrollment:
        return redirect(url_for('course_details', course_id=course_id))

    lessons = get_lessons_for_course(course_id)
    if not lessons:
        lessons = []
    # Determine current lesson to show
    # We'll assume lessons ordered by assignment_id string lex order for sequence
    lessons = sorted(lessons, key=lambda x: x['lesson_id'])

    # completed lessons by submission
    submissions = get_all_submissions()
    completed_lesson_ids = set()
    for sub in submissions:
        if sub['username'] == username and sub['assignment_id'] in [l['lesson_id'] for l in lessons]:
            completed_lesson_ids.add(sub['assignment_id'])

    # current lesson is first lesson not completed (in sequence)
    current_lesson = None
    for lesson in lessons:
        if lesson['lesson_id'] not in completed_lesson_ids:
            current_lesson = lesson
            break
    if not current_lesson and lessons:
        # all completed
        current_lesson = lessons[-1]

    progress = enrollment['progress']

    # Check for certificate if progress is 100
    completion_certificate = None
    if enrollment['status'] == 'Completed':
        certs = get_all_certificates()
        for cert in certs:
            if cert['username'] == username and cert['course_id'] == course_id:
                completion_certificate = cert
                break

    return render_template('course_learning.html', course={'course_id': course['course_id'], 'title': course['title']},
                           lessons=lessons, current_lesson_id=current_lesson['lesson_id'] if current_lesson else None,
                           progress=progress, completion_certificate=completion_certificate)


@app.route('/my-courses/learn/<course_id>/complete', methods=['POST'])
def mark_lesson_complete(course_id):
    user = get_all_users()[0] if get_all_users() else None
    if not user:
        flash('User not found')
        return redirect(url_for('course_learning', course_id=course_id))
    username = user['username']
    course = get_course_by_id(course_id)
    if not course:
        flash('Course not found')
        return redirect(url_for('my_courses'))

    enrollment = get_enrollment(username, course_id)
    if not enrollment:
        flash('Not enrolled in this course')
        return redirect(url_for('course_details', course_id=course_id))

    lessons = get_lessons_for_course(course_id)
    lessons = sorted(lessons, key=lambda x: x['lesson_id'])

    # completed lessons by submission
    submissions = get_all_submissions()
    completed_lesson_ids = set()
    for sub in submissions:
        if sub['username'] == username and sub['assignment_id'] in [l['lesson_id'] for l in lessons]:
            completed_lesson_ids.add(sub['assignment_id'])

    # current lesson is first lesson not completed (in sequence)
    current_lesson = None
    for lesson in lessons:
        if lesson['lesson_id'] not in completed_lesson_ids:
            current_lesson = lesson
            break

    if not current_lesson:
        # all lessons already completed
        flash('All lessons completed')
        return redirect(url_for('course_learning', course_id=course_id))

    # Mark current lesson complete by creating a dummy submission with empty text if none exists
    sub = get_submission(username, current_lesson['lesson_id'])
    if not sub:
        # Add a submission with empty text
        add_or_update_submission(username, current_lesson['lesson_id'], '')

    # Update progress
    total_lessons = len(lessons)
    completed_count = get_completed_lessons_count(username, course_id)
    progress = int((completed_count / total_lessons) * 100) if total_lessons else 0

    enrollment['progress'] = progress

    # If 100% progress, update enrollment status and add certificate
    completion_certificate = None
    if progress >= 100 and enrollment['status'] != 'Completed':
        enrollment['status'] = 'Completed'
        update_enrollment(enrollment)
        completion_certificate = add_certificate(username, course_id)
    else:
        update_enrollment(enrollment)

    lessons = get_lessons_for_course(course_id)
    lessons = sorted(lessons, key=lambda x: x['lesson_id'])

    return render_template('course_learning.html', course={'course_id': course['course_id'], 'title': course['title']},
                           lessons=lessons, current_lesson_id=current_lesson['lesson_id'],
                           progress=progress, completion_certificate=completion_certificate)


@app.route('/assignments')
def my_assignments():
    user = get_all_users()[0] if get_all_users() else None
    if not user:
        return "User not found", 404
    username = user['username']
    assignments = get_all_assignments()
    submissions = get_all_submissions()

    assignments_with_status = []
    for a in assignments:
        if a['course_id'] not in [e['course_id'] for e in get_all_enrollments() if e['username'] == username]:
            continue  # skip assignments from courses not enrolled
        submission_status = 'Not Submitted'
        for s in submissions:
            if s['assignment_id'] == a['assignment_id'] and s['username'] == username:
                submission_status = 'Submitted'
                break
        assignments_with_status.append({
            'assignment_id': a['assignment_id'],
            'course_id': a['course_id'],
            'title': a['title'],
            'description': a['description'],
            'due_date': a['due_date'],
            'max_points': a['max_points'],
            'submission_status': submission_status
        })
    return render_template('assignments.html', assignments=assignments_with_status)


@app.route('/assignments/submit/<assignment_id>')
def submit_assignment(assignment_id):
    assignment = get_assignment_by_id(assignment_id)
    if not assignment:
        return "Assignment not found", 404
    return render_template('submit_assignment.html', assignment=assignment)


@app.route('/assignments/submit/<assignment_id>', methods=['POST'])
def submit_assignment_post(assignment_id):
    assignment = get_assignment_by_id(assignment_id)
    if not assignment:
        return "Assignment not found", 404
    user = get_all_users()[0] if get_all_users() else None
    if not user:
        return "User not found", 404
    username = user['username']
    submission_text = request.form.get('submission_text', '').strip()

    submission_success = False
    error_message = None
    if not submission_text:
        error_message = 'Submission text cannot be empty.'
    else:
        try:
            add_or_update_submission(username, assignment_id, submission_text)
            submission_success = True
        except Exception as e:
            error_message = 'Failed to save submission.'

    return render_template('submit_assignment.html', assignment=assignment, submission_success=submission_success, error_message=error_message)


@app.route('/certificates')
def my_certificates():
    user = get_all_users()[0] if get_all_users() else None
    if not user:
        return "User not found", 404
    username = user['username']
    certificates = get_all_certificates()
    user_certs = []
    for c in certificates:
        if c['username'] == username:
            course = get_course_by_id(c['course_id'])
            if course:
                user_certs.append({
                    'certificate_id': c['certificate_id'],
                    'course_id': c['course_id'],
                    'title': course['title'],
                    'issue_date': c['issue_date']
                })
    return render_template('certificates.html', certificates=user_certs)


@app.route('/profile')
def user_profile():
    user = get_all_users()[0] if get_all_users() else None
    if not user:
        return "User not found", 404
    return render_template('profile.html', username=user['username'], email=user['email'], fullname=user['fullname'])


@app.route('/profile/update', methods=['POST'])
def update_profile():
    user = get_all_users()[0] if get_all_users() else None
    if not user:
        flash('User not found')
        return redirect(url_for('user_profile'))

    username = user['username']
    email = request.form.get('email', '').strip()
    fullname = request.form.get('fullname', '').strip()
    if not email or not fullname:
        flash('Email and Full name cannot be empty.')
        return redirect(url_for('user_profile'))
    updated = update_user(username, email, fullname)
    if updated:
        flash('Profile updated successfully.')
    else:
        flash('Failed to update profile.')
    return redirect(url_for('user_profile'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
