from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

DATA_DIR = 'data'

# Utility functions for reading and writing data files in pipe-delimited format

def read_pipe_file(filename):
    filepath = os.path.join(DATA_DIR, filename)
    data = []
    if not os.path.exists(filepath):
        return data
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                cols = line.split('|')
                data.append(cols)
    return data


def write_pipe_file(filename, rows):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        for row in rows:
            row_str = '|'.join(str(e) for e in row)
            f.write(row_str + '\n')


# Users functions

def get_users():
    raw = read_pipe_file('users.txt')
    users = []
    for row in raw:
        if len(row) != 3:
            continue
        users.append({'username': row[0], 'email': row[1], 'fullname': row[2]})
    return users


def get_user(username):
    users = get_users()
    for u in users:
        if u['username'] == username:
            return u
    return None


def update_user(username, email, fullname):
    users = get_users()
    updated = False
    for u in users:
        if u['username'] == username:
            u['email'] = email
            u['fullname'] = fullname
            updated = True
    if updated:
        write_pipe_file('users.txt', [[u['username'], u['email'], u['fullname']] for u in users])
    return updated


# Courses functions

def get_courses():
    raw = read_pipe_file('courses.txt')
    courses = []
    for row in raw:
        if len(row) != 7:
            continue
        try:
            c_id = int(row[0])
        except:
            continue
        courses.append({'course_id': c_id,
                        'title': row[1],
                        'description': row[2],
                        'category': row[3],
                        'level': row[4],
                        'duration': row[5],
                        'status': row[6]})
    return courses


def get_course(course_id):
    courses = get_courses()
    for c in courses:
        if c['course_id'] == course_id:
            return c
    return None


# Enrollments functions

def get_enrollments():
    raw = read_pipe_file('enrollments.txt')
    enrollments = []
    for row in raw:
        if len(row) != 6:
            continue
        try:
            enrollment_id = int(row[0])
            course_id = int(row[2])
            progress = int(row[4])
        except:
            continue
        enrollments.append({'enrollment_id': enrollment_id,
                            'username': row[1],
                            'course_id': course_id,
                            'enrollment_date': row[3],
                            'progress': progress,
                            'status': row[5]})
    return enrollments


def get_user_enrollments(username):
    enrollments = get_enrollments()
    return [e for e in enrollments if e['username'] == username]


def get_enrollment_by_user_course(username, course_id):
    enrollments = get_enrollments()
    for e in enrollments:
        if e['username'] == username and e['course_id'] == course_id:
            return e
    return None


def add_enrollment(username, course_id):
    enrollments = get_enrollments()
    if any(e['username'] == username and e['course_id'] == course_id for e in enrollments):
        return False # Already enrolled
    next_id = max([e['enrollment_id'] for e in enrollments], default=0) + 1
    enrollment_date = datetime.now().strftime('%Y-%m-%d')
    enrollments.append({'enrollment_id': next_id,
                        'username': username,
                        'course_id': course_id,
                        'enrollment_date': enrollment_date,
                        'progress': 0,
                        'status': 'In Progress'})
    write_pipe_file('enrollments.txt', [[e['enrollment_id'], e['username'], e['course_id'], e['enrollment_date'], e['progress'], e['status']] for e in enrollments])
    return True


def update_enrollment_progress(enrollment_id, progress, status=None):
    enrollments = get_enrollments()
    updated = False
    for e in enrollments:
        if e['enrollment_id'] == enrollment_id:
            e['progress'] = progress
            if status is not None:
                e['status'] = status
            updated = True
    if updated:
        write_pipe_file('enrollments.txt', [[e['enrollment_id'], e['username'], e['course_id'], e['enrollment_date'], e['progress'], e['status']] for e in enrollments])
    return updated


# Assignments functions

def get_assignments():
    raw = read_pipe_file('assignments.txt')
    assignments = []
    for row in raw:
        if len(row) != 6:
            continue
        try:
            assignment_id = int(row[0])
            course_id = int(row[1])
            max_points = int(row[5])
        except:
            continue
        assignments.append({'assignment_id': assignment_id,
                            'course_id': course_id,
                            'title': row[2],
                            'description': row[3],
                            'due_date': row[4],
                            'max_points': max_points})
    return assignments


def get_assignment(assignment_id):
    assignments = get_assignments()
    for a in assignments:
        if a['assignment_id'] == assignment_id:
            return a
    return None


# Submissions functions

def get_submissions():
    raw = read_pipe_file('submissions.txt')
    submissions = []
    for row in raw:
        if len(row) != 7:
            continue
        try:
            submission_id = int(row[0])
            assignment_id = int(row[1])
            grade = int(row[5])
        except:
            continue
        submissions.append({'submission_id': submission_id,
                            'assignment_id': assignment_id,
                            'username': row[2],
                            'submission_text': row[3],
                            'submit_date': row[4],
                            'grade': grade,
                            'feedback': row[6]})
    return submissions


def get_submission(username, assignment_id):
    submissions = get_submissions()
    for s in submissions:
        if s['username'] == username and s['assignment_id'] == assignment_id:
            return s
    return None


def add_submission(assignment_id, username, submission_text, submit_date, grade=0, feedback=''):
    submissions = get_submissions()
    next_id = max([s['submission_id'] for s in submissions], default=0) + 1
    submissions.append({'submission_id': next_id,
                        'assignment_id': assignment_id,
                        'username': username,
                        'submission_text': submission_text,
                        'submit_date': submit_date,
                        'grade': grade,
                        'feedback': feedback})
    write_pipe_file('submissions.txt', [[s['submission_id'], s['assignment_id'], s['username'], s['submission_text'], s['submit_date'], s['grade'], s['feedback']] for s in submissions])
    return True


def update_submission(submission_id, submission_text, submit_date, grade=None, feedback=None):
    submissions = get_submissions()
    updated = False
    for s in submissions:
        if s['submission_id'] == submission_id:
            s['submission_text'] = submission_text
            s['submit_date'] = submit_date
            if grade is not None:
                s['grade'] = grade
            if feedback is not None:
                s['feedback'] = feedback
            updated = True
    if updated:
        write_pipe_file('submissions.txt', [[s['submission_id'], s['assignment_id'], s['username'], s['submission_text'], s['submit_date'], s['grade'], s['feedback']] for s in submissions])
    return updated


# Certificates functions

def get_certificates():
    raw = read_pipe_file('certificates.txt')
    certificates = []
    for row in raw:
        if len(row) != 4:
            continue
        try:
            certificate_id = int(row[0])
            course_id = int(row[2])
        except:
            continue
        certificates.append({'certificate_id': certificate_id,
                             'username': row[1],
                             'course_id': course_id,
                             'issue_date': row[3]})
    return certificates


def get_user_certificates(username):
    certificates = get_certificates()
    return [c for c in certificates if c['username'] == username]


def add_certificate(username, course_id):
    certificates = get_certificates()
    if any(c['username'] == username and c['course_id'] == course_id for c in certificates):
        return False # Already has certificate
    next_id = max([c['certificate_id'] for c in certificates], default=0) + 1
    issue_date = datetime.now().strftime('%Y-%m-%d')
    certificates.append({'certificate_id': next_id,
                         'username': username,
                         'course_id': course_id,
                         'issue_date': issue_date})
    write_pipe_file('certificates.txt', [[c['certificate_id'], c['username'], c['course_id'], c['issue_date']] for c in certificates])
    return True


# Lessons are not explicitly defined in specifications, but for learning page we must implement lessons list and completion.
# Since lessons data schema is not defined, we can simulate lessons as numbered lessons 1 to 10 per course as a stub.
# Completion is stored in enrollments progress percentage, so we infer completed lessons from progress.

# For simplicity, assume each course has 10 lessons. Progress increments 10% per lesson completed.
# Each lesson has lesson_id from 1 to 10, title as 'Lesson {lesson_id}' and content as 'Content for lesson {lesson_id} of course {course_id}'.

NUM_LESSONS_PER_COURSE = 10


def get_lessons(course_id, progress):
    completed_lessons_count = progress // 10
    lessons = []
    for lesson_id in range(1, NUM_LESSONS_PER_COURSE + 1):
        lessons.append({'lesson_id': lesson_id,
                        'title': f'Lesson {lesson_id}',
                        'completed': lesson_id <= completed_lessons_count})
    return lessons


def get_current_lesson(course_id, progress):
    next_lesson_id = (progress // 10) + 1
    if next_lesson_id > NUM_LESSONS_PER_COURSE:
        next_lesson_id = NUM_LESSONS_PER_COURSE
    title = f'Lesson {next_lesson_id}'
    content = f'Content for lesson {next_lesson_id} of course {course_id}'
    return {'title': title, 'content': content, 'lesson_id': next_lesson_id}


# Business logic for marking lesson completed and updating progress

def mark_lesson_complete(username, course_id, lesson_id):
    enrollment = get_enrollment_by_user_course(username, course_id)
    if not enrollment:
        return False
    progress = enrollment['progress']
    completed_lessons = progress // 10
    # Can only mark next lesson in sequence completed
    expected_lesson = completed_lessons + 1
    if lesson_id != expected_lesson or lesson_id > NUM_LESSONS_PER_COURSE:
        return False

    new_progress = min(100, progress + 10)
    status = enrollment['status']
    if new_progress == 100:
        status = 'Completed'
    update_enrollment_progress(enrollment['enrollment_id'], new_progress, status)
    # If progress is now 100%, add certificate if not already
    if new_progress == 100:
        add_certificate(username, course_id)
    return True


# For simplicity, assume logged-in user is 'john' (from users.txt example)
# This is hardcoded for this backend implementation as no auth is implemented
LOGGED_IN_USERNAME = 'john'


# -------------------- ROUTES IMPLEMENTATION ---------------------

@app.route('/')
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    user = get_user(LOGGED_IN_USERNAME)
    if user is None:
        return "User not found", 404
    # Get enrollments for user with course and progress
    enrollments = get_user_enrollments(LOGGED_IN_USERNAME)
    enrollment_list = []
    for e in enrollments:
        course = get_course(e['course_id'])
        if course:
            enrollment_list.append({'course_title': course['title'], 'progress': e['progress']})
    return render_template('dashboard.html', user_name=user['fullname'], enrollments=enrollment_list)


@app.route('/courses')
def available_courses():
    courses = get_courses()
    active_courses = [c for c in courses if c['status'] == 'Active']
    # Compose minimal dicts for template context
    course_list = [{'course_id': c['course_id'], 'title': c['title'], 'description': c['description']} for c in active_courses]
    return render_template('available_courses.html', courses=course_list)


@app.route('/course/<int:course_id>')
def course_details(course_id):
    user = get_user(LOGGED_IN_USERNAME)
    if user is None:
        return "User not found", 404
    course = get_course(course_id)
    if not course or course['status'] != 'Active':
        return "Course not found or inactive", 404

    enrollment = get_enrollment_by_user_course(LOGGED_IN_USERNAME, course_id)
    enrolled = enrollment is not None
    enrollment_date = enrollment['enrollment_date'] if enrolled else None
    progress = enrollment['progress'] if enrolled else 0

    course_dict = {
        'course_id': course['course_id'],
        'title': course['title'],
        'description': course['description']
    }

    return render_template('course_details.html', course=course_dict, enrolled=enrolled, enrollment_date=enrollment_date, progress=progress)


@app.route('/enroll/<int:course_id>', methods=['POST'])
def enroll(course_id):
    user = get_user(LOGGED_IN_USERNAME)
    if user is None:
        return "User not found", 404
    course = get_course(course_id)
    if not course or course['status'] != 'Active':
        return "Course not found or inactive", 404

    success = add_enrollment(LOGGED_IN_USERNAME, course_id)
    # Redirect to dashboard regardless
    return redirect(url_for('dashboard'))


@app.route('/my-courses')
def my_courses():
    user = get_user(LOGGED_IN_USERNAME)
    if user is None:
        return "User not found", 404
    enrollments = get_user_enrollments(LOGGED_IN_USERNAME)
    my_courses_list = []
    for e in enrollments:
        course = get_course(e['course_id'])
        if course and course['status'] == 'Active':
            my_courses_list.append({'course_id': course['course_id'], 'title': course['title'], 'progress': e['progress']})
    return render_template('my_courses.html', my_courses=my_courses_list)


@app.route('/learning/<int:course_id>')
def learning_page(course_id):
    user = get_user(LOGGED_IN_USERNAME)
    if user is None:
        return "User not found", 404
    course = get_course(course_id)
    if not course or course['status'] != 'Active':
        return "Course not found or inactive", 404

    enrollment = get_enrollment_by_user_course(LOGGED_IN_USERNAME, course_id)
    if not enrollment:
        return redirect(url_for('course_details', course_id=course_id))

    progress = enrollment['progress']
    lessons = get_lessons(course_id, progress)
    current_lesson = get_current_lesson(course_id, progress)

    # For current lesson, we provide title and content
    current_lesson_dict = {'title': current_lesson['title'], 'content': current_lesson['content']}

    return render_template('learning_page.html', course_id=course_id, lessons=lessons, current_lesson=current_lesson_dict)


@app.route('/mark-lesson-completed/<int:course_id>/<int:lesson_id>', methods=['POST'])
def mark_lesson_completed(course_id, lesson_id):
    success = mark_lesson_complete(LOGGED_IN_USERNAME, course_id, lesson_id)
    return redirect(url_for('learning_page', course_id=course_id))


@app.route('/assignments')
def assignments():
    user = get_user(LOGGED_IN_USERNAME)
    if user is None:
        return "User not found", 404
    assignments_data = get_assignments()
    submissions = get_submissions()

    assignments_list = []
    for a in assignments_data:
        # Determine status: "Pending", "Submitted", "Graded"
        submission = None
        for s in submissions:
            if s['username'] == LOGGED_IN_USERNAME and s['assignment_id'] == a['assignment_id']:
                submission = s
                break
        status = "Pending"
        if submission:
            if submission['grade'] > 0:
                status = "Graded"
            else:
                status = "Submitted"

        assignments_list.append({'assignment_id': a['assignment_id'], 'title': a['title'], 'due_date': a['due_date'], 'status': status})

    return render_template('assignments.html', assignments=assignments_list)


@app.route('/submit-assignment/<int:assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    user = get_user(LOGGED_IN_USERNAME)
    if user is None:
        return "User not found", 404

    assignment = get_assignment(assignment_id)
    if not assignment:
        return "Assignment not found", 404

    if request.method == 'GET':
        assignment_dict = {'title': assignment['title'], 'description': assignment['description']}
        return render_template('assignment_submission.html', assignment=assignment_dict)

    # POST
    submission_text = request.form.get('submission_text', '').strip()
    if not submission_text:
        # Return the form again with error message? Spec doesn't say, so just redirect back
        return redirect(url_for('submit_assignment', assignment_id=assignment_id))

    submit_date = datetime.now().strftime('%Y-%m-%d')
    # For simplicity, grade and feedback are initially 0 and empty
    existing_submission = get_submission(LOGGED_IN_USERNAME, assignment_id)
    if existing_submission:
        # Update existing submission
        update_submission(existing_submission['submission_id'], submission_text, submit_date, grade=0, feedback='')
    else:
        add_submission(assignment_id, LOGGED_IN_USERNAME, submission_text, submit_date, grade=0, feedback='')

    return redirect(url_for('assignments'))


@app.route('/certificates')
def certificates():
    user = get_user(LOGGED_IN_USERNAME)
    if user is None:
        return "User not found", 404
    user_certificates = get_user_certificates(LOGGED_IN_USERNAME)
    courses = get_courses()

    certificates_list = []
    for c in user_certificates:
        course = next((course for course in courses if course['course_id'] == c['course_id']), None)
        if course:
            certificates_list.append({'certificate_id': c['certificate_id'],
                                      'username': c['username'],
                                      'course_title': course['title'],
                                      'issue_date': c['issue_date']})
    return render_template('certificates.html', certificates=certificates_list)


@app.route('/profile')
def user_profile():
    user = get_user(LOGGED_IN_USERNAME)
    if user is None:
        return "User not found", 404
    user_dict = {'email': user['email'], 'name': user['fullname']}
    return render_template('user_profile.html', user=user_dict)


@app.route('/profile/update', methods=['POST'])
def update_profile():
    user = get_user(LOGGED_IN_USERNAME)
    if user is None:
        return "User not found", 404

    email = request.form.get('email', '').strip()
    name = request.form.get('name', '').strip()

    if not email or not name:
        # Invalid input, redirect back without changes
        return redirect(url_for('user_profile'))

    update_user(LOGGED_IN_USERNAME, email, name)
    return redirect(url_for('user_profile'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
