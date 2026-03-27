from flask import Flask, render_template, request, redirect, url_for, abort, flash
from typing import List, Dict, Set
import os
import datetime

app = Flask(__name__)
app.secret_key = 'replace-with-secure-key'

DATA_DIR = 'data'

# Utility functions for reading and writing pipe-delimited files
def read_pipe_delimited_file(filename: str) -> List[List[str]]:
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().strip()
        if not lines:
            return []
        return [line.split('|') for line in lines.split('\n')]

def write_pipe_delimited_file(filename: str, rows: List[List[str]]):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join('|'.join(map(str, row)) for row in rows))

# USERS

def read_users() -> List[Dict[str, str]]:
    rows = read_pipe_delimited_file('users.txt')
    users = []
    for row in rows:
        if len(row) != 3:
            continue
        username, email, fullname = row
        users.append({'username': username, 'email': email, 'fullname': fullname})
    return users

def get_user_by_username(username: str) -> Dict[str, str] or None:
    users = read_users()
    for user in users:
        if user['username'] == username:
            return user
    return None

def update_user_profile(username: str, email: str, fullname: str):
    users = read_pipe_delimited_file('users.txt')
    changed = False
    for i, row in enumerate(users):
        if len(row) != 3:
            continue
        if row[0] == username:
            users[i] = [username, email, fullname]
            changed = True
            break
    if changed:
        write_pipe_delimited_file('users.txt', users)

# COURSES

def read_courses() -> List[Dict[str, str]]:
    rows = read_pipe_delimited_file('courses.txt')
    courses = []
    for row in rows:
        if len(row) != 7:
            continue
        course_id, title, description, category, level, duration, status = row
        courses.append({
            'course_id': course_id, 'title': title, 'description': description,
            'category': category, 'level': level, 'duration': duration, 'status': status
        })
    return courses

def get_course_by_id(course_id: str) -> Dict[str, str] or None:
    courses = read_courses()
    for c in courses:
        if c['course_id'] == course_id:
            return c
    return None

# ENROLLMENTS

def read_enrollments() -> List[Dict]:
    rows = read_pipe_delimited_file('enrollments.txt')
    enrollments = []
    for row in rows:
        if len(row) != 6:
            continue
        enrollment_id, username, course_id, enrollment_date, progress_str, status = row
        try:
            progress = int(progress_str)
        except ValueError:
            progress = 0
        enrollments.append({
            'enrollment_id': enrollment_id, 'username': username, 'course_id': course_id,
            'enrollment_date': enrollment_date, 'progress': progress, 'status': status
        })
    return enrollments

def write_enrollments(enrollments: List[Dict]):
    rows = []
    for e in enrollments:
        rows.append([
            e['enrollment_id'], e['username'], e['course_id'],
            e['enrollment_date'], str(e['progress']), e['status']
        ])
    write_pipe_delimited_file('enrollments.txt', rows)

def get_enrollment(username: str, course_id: str) -> Dict or None:
    enrollments = read_enrollments()
    for e in enrollments:
        if e['username'] == username and e['course_id'] == course_id:
            return e
    return None

def add_enrollment(username: str, course_id: str) -> bool:
    if get_enrollment(username, course_id):
        return False
    enrollments = read_enrollments()
    existing_ids = set(e['enrollment_id'] for e in enrollments)
    new_id = 1
    while str(new_id) in existing_ids:
        new_id += 1
    new_enrollment = {
        'enrollment_id': str(new_id), 'username': username, 'course_id': course_id,
        'enrollment_date': datetime.date.today().isoformat(), 'progress': 0, 'status': "In Progress"
    }
    enrollments.append(new_enrollment)
    write_enrollments(enrollments)
    return True

def update_enrollment_progress(username: str, course_id: str, progress: int):
    enrollments = read_enrollments()
    updated = False
    for e in enrollments:
        if e['username'] == username and e['course_id'] == course_id:
            e['progress'] = max(0, min(100, progress))
            e['status'] = 'Completed' if e['progress'] == 100 else 'In Progress'
            updated = True
            break
    if updated:
        write_enrollments(enrollments)
    return updated

# LESSONS (Assumed file lessons_<course_id>.txt with fields lesson_id|title|content)

def read_lessons(course_id: str) -> List[Dict]:
    filename = f"lessons_{course_id}.txt"
    rows = read_pipe_delimited_file(filename)
    lessons = []
    for row in rows:
        if len(row) != 3:
            continue
        lesson_id, title, content = row
        lessons.append({'lesson_id': lesson_id, 'title': title, 'content': content})
    return lessons

# LESSON PROGRESS

def read_lesson_progress() -> List[Dict]:
    rows = read_pipe_delimited_file('lesson_progress.txt')
    progress = []
    for row in rows:
        if len(row) != 5:
            continue
        progress_id, username, course_id, lesson_id, completed_str = row
        completed = completed_str.lower() == 'true'
        progress.append({
            'progress_id': progress_id, 'username': username,
            'course_id': course_id, 'lesson_id': lesson_id, 'completed': completed
        })
    return progress

def write_lesson_progress(progress: List[Dict]):
    rows = []
    for p in progress:
        rows.append([
            p['progress_id'], p['username'], p['course_id'], p['lesson_id'],
            'True' if p['completed'] else 'False'
        ])
    write_pipe_delimited_file('lesson_progress.txt', rows)

def get_lesson_progress_for_user_course(username: str, course_id: str) -> Dict[str, bool]:
    all_progress = read_lesson_progress()
    mapping = {}
    for p in all_progress:
        if p['username'] == username and p['course_id'] == course_id:
            mapping[p['lesson_id']] = p['completed']
    return mapping

def mark_lesson_complete(username: str, course_id: str, lesson_id: str) -> bool:
    progress = read_lesson_progress()
    for p in progress:
        if p['username'] == username and p['course_id'] == course_id and p['lesson_id'] == lesson_id:
            if p['completed']:
                return False
            p['completed'] = True
            write_lesson_progress(progress)
            return True
    ids = set(p['progress_id'] for p in progress)
    new_id = 1
    while str(new_id) in ids:
        new_id += 1
    progress.append({
        'progress_id': str(new_id), 'username': username, 'course_id': course_id,
        'lesson_id': lesson_id, 'completed': True
    })
    write_lesson_progress(progress)
    return True

# ASSIGNMENTS

def read_assignments() -> List[Dict]:
    rows = read_pipe_delimited_file('assignments.txt')
    assignments = []
    for row in rows:
        if len(row) != 6:
            continue
        assignment_id, course_id, title, description, due_date, max_points_str = row
        try:
            max_points = int(max_points_str)
        except ValueError:
            max_points = 0
        assignments.append({
            'assignment_id': assignment_id, 'course_id': course_id, 'title': title,
            'description': description, 'due_date': due_date, 'max_points': max_points
        })
    return assignments

def get_assignment_by_id(assignment_id: str) -> Dict or None:
    assignments = read_assignments()
    for a in assignments:
        if a['assignment_id'] == assignment_id:
            return a
    return None

# SUBMISSIONS

def read_submissions() -> List[Dict]:
    rows = read_pipe_delimited_file('submissions.txt')
    submissions = []
    for row in rows:
        if len(row) != 7:
            continue
        submission_id, assignment_id, username, submission_text, submit_date, grade_str, feedback = row
        try:
            grade = int(grade_str)
        except ValueError:
            grade = None
        submissions.append({
            'submission_id': submission_id,'assignment_id': assignment_id,'username': username,
            'content': submission_text,'submit_date': submit_date,'grade': grade,'feedback': feedback
        })
    return submissions

def write_submissions(submissions: List[Dict]):
    rows = []
    for s in submissions:
        grade_str = str(s['grade']) if s['grade'] is not None else ''
        rows.append([
            s['submission_id'], s['assignment_id'], s['username'], s['content'], s['submit_date'], grade_str, s['feedback']
        ])
    write_pipe_delimited_file('submissions.txt', rows)

def add_submission(assignment_id: str, username: str, content: str, submit_date: str) -> bool:
    submissions = read_submissions()
    existing_ids = set(s['submission_id'] for s in submissions)
    new_id = 1
    while str(new_id) in existing_ids:
        new_id += 1
    submissions.append({
        'submission_id': str(new_id), 'assignment_id': assignment_id, 'username': username,
        'content': content, 'submit_date': submit_date, 'grade': None, 'feedback': ''
    })
    write_submissions(submissions)
    return True

# CERTIFICATES

def read_certificates() -> List[Dict]:
    rows = read_pipe_delimited_file('certificates.txt')
    certs = []
    for row in rows:
        if len(row) !=4:
            continue
        certificate_id, username, course_id, issue_date = row
        certs.append({
            'certificate_id': certificate_id, 'username': username, 'course_id': course_id, 'issue_date': issue_date
        })
    return certs

def write_certificates(certs: List[Dict]):
    rows = []
    for c in certs:
        rows.append([c['certificate_id'], c['username'], c['course_id'], c['issue_date']])
    write_pipe_delimited_file('certificates.txt', rows)

def add_certificate(username: str, course_id: str) -> bool:
    certs = read_certificates()
    for c in certs:
        if c['username'] == username and c['course_id'] == course_id:
            return False
    existing_ids = set(c['certificate_id'] for c in certs)
    new_id = 1
    while str(new_id) in existing_ids:
        new_id += 1
    certs.append({
        'certificate_id': str(new_id), 'username': username, 'course_id': course_id, 'issue_date': datetime.date.today().isoformat()
    })
    write_certificates(certs)
    return True

# Simulate current user context
CURRENT_USERNAME = 'john'

def get_current_user() -> Dict[str, str]:
    user = get_user_by_username(CURRENT_USERNAME)
    if user is None:
        user = {'username': CURRENT_USERNAME, 'email': 'john@student.com', 'fullname': 'John Student'}
    return user

# --- ROUTES ---

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'), code=302)

@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    username = user['username']
    fullname = user['fullname']
    enrollments = read_enrollments()
    user_enrollments = [e for e in enrollments if e['username'] == username]
    enrolled_courses = []
    for e in user_enrollments:
        course = get_course_by_id(e['course_id'])
        if course is None:
            continue
        enrolled_courses.append({'course_id': course['course_id'], 'title': course['title'], 'progress': e['progress']})
    return render_template('dashboard.html', username=username, fullname=fullname, enrolled_courses=enrolled_courses)

@app.route('/courses/catalog')
def course_catalog():
    courses = read_courses()
    active_courses = [c for c in courses if c['status'].lower() == 'active']
    return render_template('course_catalog.html', courses=active_courses)

@app.route('/courses/<course_id>')
def course_details(course_id):
    user = get_current_user()
    username = user['username']
    course = get_course_by_id(course_id)
    if course is None:
        abort(404)
    enrolled = get_enrollment(username, course_id) is not None
    course_simple = {'course_id': course['course_id'], 'title': course['title'], 'description': course['description']}
    return render_template('course_details.html', course=course_simple, enrolled=enrolled)

@app.route('/courses/<course_id>/enroll', methods=['POST'])
def enroll_course(course_id):
    user = get_current_user()
    username = user['username']
    course = get_course_by_id(course_id)
    if course is None:
        abort(404)
    enrollment_success = add_enrollment(username, course_id)
    course_simple = {'course_id': course['course_id'], 'title': course['title'], 'description': course['description']}
    enrolled = enrollment_success or get_enrollment(username, course_id) is not None
    return render_template('course_details.html', course=course_simple, enrolled=enrolled, enrollment_success=enrollment_success if enrollment_success else None)

@app.route('/my-courses')
def my_courses():
    user = get_current_user()
    username = user['username']
    enrollments = read_enrollments()
    user_enrollments = [e for e in enrollments if e['username'] == username]
    enrolled_courses = []
    for e in user_enrollments:
        course = get_course_by_id(e['course_id'])
        if course is None:
            continue
        enrolled_courses.append({'course_id': course['course_id'], 'title': course['title'], 'progress': e['progress']})
    return render_template('my_courses.html', enrolled_courses=enrolled_courses)

@app.route('/my-courses/<course_id>')
def course_learning(course_id):
    user = get_current_user()
    username = user['username']
    course = get_course_by_id(course_id)
    if course is None:
        abort(404)
    enrollment = get_enrollment(username, course_id)
    if enrollment is None:
        flash('You are not enrolled in this course.', 'error')
        return redirect(url_for('my_courses'))
    lessons = read_lessons(course_id)
    completed_lessons_map = get_lesson_progress_for_user_course(username, course_id)
    completed_lessons_ids: Set[str] = {lid for lid, done in completed_lessons_map.items() if done}
    current_lesson = None
    for lesson in lessons:
        if lesson['lesson_id'] not in completed_lessons_ids:
            current_lesson = lesson
            break
    if current_lesson is None and lessons:
        current_lesson = lessons[-1]
    return render_template('course_learning.html', course_id=course['course_id'], course_title=course['title'], lessons=lessons, current_lesson=current_lesson, completed_lessons_ids=completed_lessons_ids, progress=enrollment['progress'])

@app.route('/my-courses/<course_id>/mark-complete', methods=['POST'])
def mark_lesson_complete_route(course_id):
    user = get_current_user()
    username = user['username']
    lesson_id = request.form.get('lesson_id')
    if not lesson_id:
        flash('Lesson id not specified', 'error')
        return redirect(url_for('course_learning', course_id=course_id))
    course = get_course_by_id(course_id)
    if course is None:
        abort(404)
    enrollment = get_enrollment(username, course_id)
    if enrollment is None:
        flash('You are not enrolled in this course.', 'error')
        return redirect(url_for('my_courses'))
    lessons = read_lessons(course_id)
    lesson_ids = [l['lesson_id'] for l in lessons]
    if lesson_id not in lesson_ids:
        flash('Invalid lesson id.', 'error')
        return redirect(url_for('course_learning', course_id=course_id))
    # enforce sequential completion
    completed_lessons_map = get_lesson_progress_for_user_course(username, course_id)
    ordered_lessons = lessons
    for i, lesson in enumerate(ordered_lessons):
        if lesson['lesson_id'] == lesson_id:
            if i > 0:
                prev_lesson_id = ordered_lessons[i-1]['lesson_id']
                if not completed_lessons_map.get(prev_lesson_id, False):
                    flash('You must complete previous lessons first.', 'error')
                    return redirect(url_for('course_learning', course_id=course_id))
            break
    lesson_completed = mark_lesson_complete(username, course_id, lesson_id)
    completed_lessons_map = get_lesson_progress_for_user_course(username, course_id)
    completed_count = sum(1 for done in completed_lessons_map.values() if done)
    total_lessons = len(lessons)
    progress = round((completed_count / total_lessons) * 100) if total_lessons > 0 else 0
    update_enrollment_progress(username, course_id, progress)
    certificate_generated = False
    if progress == 100:
        certificate_generated = add_certificate(username, course_id)
    return render_template('course_learning.html', course_id=course_id, course_title=course['title'], lessons=lessons, current_lesson=None, completed_lessons_ids=set(lid for lid, done in completed_lessons_map.items() if done), progress=progress, lesson_completed=lesson_completed, certificate_generated=certificate_generated)

@app.route('/assignments')
def my_assignments():
    user = get_current_user()
    username = user['username']
    enrollments = read_enrollments()
    enrolled_courses = {e['course_id'] for e in enrollments if e['username'] == username}
    assignments_all = read_assignments()
    assignments = [a for a in assignments_all if a['course_id'] in enrolled_courses]
    return render_template('my_assignments.html', assignments=assignments)

@app.route('/assignments/<assignment_id>')
def submit_assignment(assignment_id):
    assignment = get_assignment_by_id(assignment_id)
    if assignment is None:
        abort(404)
    return render_template('submit_assignment.html', assignment=assignment)

@app.route('/assignments/<assignment_id>/submit', methods=['POST'])
def submit_assignment_post(assignment_id):
    assignment = get_assignment_by_id(assignment_id)
    if assignment is None:
        abort(404)
    user = get_current_user()
    username = user['username']
    submission_text = request.form.get('submission_text')
    if not submission_text or submission_text.strip() == '':
        return render_template('submit_assignment.html', assignment=assignment, submission_success=False)
    submit_date = datetime.date.today().isoformat()
    add_submission(assignment_id, username, submission_text.strip(), submit_date)
    return render_template('submit_assignment.html', assignment=assignment, submission_success=True)

@app.route('/certificates')
def certificates():
    user = get_current_user()
    username = user['username']
    certs_all = read_certificates()
    courses = {c['course_id']: c for c in read_courses()}
    user_certs = []
    for c in certs_all:
        if c['username'] == username:
            course = courses.get(c['course_id'])
            course_title = course['title'] if course else ''
            user_certs.append({
                'certificate_id': c['certificate_id'], 'username': c['username'], 'course_id': c['course_id'],
                'issue_date': c['issue_date'], 'course_title': course_title
            })
    return render_template('certificates.html', certificates=user_certs)

@app.route('/profile')
def user_profile():
    user = get_current_user()
    return render_template('user_profile.html', username=user['username'], email=user['email'], fullname=user['fullname'])

@app.route('/profile/update', methods=['POST'])
def update_profile():
    user = get_current_user()
    username = user['username']
    email = request.form.get('email', '').strip()
    fullname = request.form.get('fullname', '').strip()
    if not email or not fullname:
        return render_template('user_profile.html', username=username, email=email, fullname=fullname, update_success=False)
    update_user_profile(username, email, fullname)
    user_updated = get_user_by_username(username)
    return render_template('user_profile.html', username=username, email=user_updated['email'], fullname=user_updated['fullname'], update_success=True)

if __name__ == '__main__':
    app.run(port=5000, debug=False)
