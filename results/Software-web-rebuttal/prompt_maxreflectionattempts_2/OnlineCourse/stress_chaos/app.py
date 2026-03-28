from flask import Flask, render_template, request, redirect, url_for, abort
import os
import datetime

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# Helper functions to read/write data files

# USERS

def read_users():
    users = []
    path = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts)!=3:
                continue
            users.append({'username': parts[0], 'email': parts[1], 'fullname': parts[2]})
    return users

def write_users(users):
    path = os.path.join(DATA_DIR, 'users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for u in users:
            f.write(f"{u['username']}|{u['email']}|{u['fullname']}\n")

# COURSES

def read_courses():
    courses = []
    path = os.path.join(DATA_DIR, 'courses.txt')
    if not os.path.exists(path):
        return courses
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts)!=7:
                continue
            courses.append({'course_id': parts[0], 'title': parts[1], 'description': parts[2], 'category': parts[3], 'level': parts[4], 'duration': parts[5], 'status': parts[6]})
    return courses

# ENROLLMENTS

def read_enrollments():
    enrollments = []
    path = os.path.join(DATA_DIR, 'enrollments.txt')
    if not os.path.exists(path):
        return enrollments
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts)!=6:
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

def write_enrollments(enrollments):
    path = os.path.join(DATA_DIR, 'enrollments.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for e in enrollments:
            f.write(f"{e['enrollment_id']}|{e['username']}|{e['course_id']}|{e['enrollment_date']}|{e['progress']}|{e['status']}\n")

# ASSIGNMENTS

def read_assignments():
    assignments = []
    path = os.path.join(DATA_DIR, 'assignments.txt')
    if not os.path.exists(path):
        return assignments
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts)!=6:
                continue
            assignment = {
                'assignment_id': parts[0],
                'course_id': parts[1],
                'title': parts[2],
                'description': parts[3],
                'due_date': parts[4],
                'max_points': int(parts[5])
            }
            assignments.append(assignment)
    return assignments

# SUBMISSIONS

def read_submissions():
    submissions = []
    path = os.path.join(DATA_DIR, 'submissions.txt')
    if not os.path.exists(path):
        return submissions
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts)!=7:
                continue
            grade = None
            if parts[5].isdigit():
                grade = int(parts[5])
            elif parts[5] != '' and parts[5] != 'None':
                try:
                    grade = int(parts[5])
                except:
                    grade = None
            feedback = None if parts[6]=='None' or parts[6]=='' else parts[6]
            submission = {
                'submission_id': parts[0],
                'assignment_id': parts[1],
                'username': parts[2],
                'submission_text': parts[3],
                'submit_date': parts[4],
                'grade': grade,
                'feedback': feedback
            }
            submissions.append(submission)
    return submissions

def write_submissions(submissions):
    path = os.path.join(DATA_DIR, 'submissions.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for s in submissions:
            grade_str = '' if s['grade'] is None else str(s['grade'])
            feedback_str = 'None' if s['feedback'] is None else s['feedback']
            f.write(f"{s['submission_id']}|{s['assignment_id']}|{s['username']}|{s['submission_text']}|{s['submit_date']}|{grade_str}|{feedback_str}\n")

# CERTIFICATES

def read_certificates():
    certificates = []
    path = os.path.join(DATA_DIR, 'certificates.txt')
    if not os.path.exists(path):
        return certificates
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts)!=4:
                continue
            certificate = {
                'certificate_id': parts[0],
                'username': parts[1],
                'course_id': parts[2],
                'issue_date': parts[3]
            }
            certificates.append(certificate)
    return certificates

def write_certificates(certificates):
    path = os.path.join(DATA_DIR, 'certificates.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for c in certificates:
            f.write(f"{c['certificate_id']}|{c['username']}|{c['course_id']}|{c['issue_date']}\n")

# LESSONS
# Lessons are part of courses, but there's no file specified in Section 3.
# The spec does not specify data source for lessons.
# We assume lessons exist embedded in courses or a separate file missing in spec.
# Since spec requires course_learning route to provide lessons with fields lesson_id,title,content,
# but no file is specified. Without file, we cannot implement lesson data properly.
# For the sake of functionality, will create a dummy lessons structure for each course with fixed lessons.
# In a real scenario, lessons would be stored in a separate file.

# For simplicity, lessons will be generated with 5 lessons per course.

def generate_lessons_for_course(course_id):
    lessons = []
    for i in range(5):
        lesson_id = f"{course_id}_lesson_{i+1}"
        lessons.append({
            'lesson_id': lesson_id,
            'title': f"Lesson {i+1}",
            'content': f"Content for lesson {i+1} of course {course_id}."
        })
    return lessons

# AUTHENTICATION SIMULATION
# Spec does not mention login system. We assume a fixed user for demo.
# For simplicity, we pick 'john' as logged in user for all routes requiring username.

LOGGED_IN_USERNAME = 'john'

# Helpers

def get_user_by_username(username):
    users = read_users()
    for u in users:
        if u['username'] == username:
            return u
    return None

def get_course_by_id(course_id):
    courses = read_courses()
    for c in courses:
        if c['course_id'] == course_id:
            return c
    return None

def get_enrollment(username, course_id):
    enrollments = read_enrollments()
    for e in enrollments:
        if e['username'] == username and e['course_id'] == course_id:
            return e
    return None

# Route Implementations

@app.route('/')
def root():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    # username logged in
    username = LOGGED_IN_USERNAME
    user = get_user_by_username(username)
    if not user:
        abort(404)
    fullname = user['fullname']

    enrollments = read_enrollments()
    courses = read_courses()

    enrolled_courses = []
    for enrollment in enrollments:
        if enrollment['username'] == username:
            course = get_course_by_id(enrollment['course_id'])
            if course:
                enrolled_courses.append({'course_id': course['course_id'], 'title': course['title'], 'progress': enrollment['progress']})

    return render_template('dashboard.html', username=username, fullname=fullname, enrolled_courses=enrolled_courses)

@app.route('/catalog')
def course_catalog():
    courses = read_courses()
    # Filter only Active courses
    active_courses = [c for c in courses if c['status'].lower() == 'active']
    return render_template('catalog.html', courses=active_courses)

@app.route('/catalog/search', methods=['POST'])
def course_catalog_search():
    query = request.form.get('search', '').strip().lower()
    courses = read_courses()
    active_courses = [c for c in courses if c['status'].lower() == 'active']
    if query == '':
        filtered_courses = active_courses
    else:
        filtered_courses = []
        for c in active_courses:
            if query in c['title'].lower() or query in c['description'].lower() or query in c['category'].lower() or query in c['level'].lower():
                filtered_courses.append(c)
    return render_template('catalog.html', courses=filtered_courses)

@app.route('/course/<course_id>')
def course_details(course_id):
    course = get_course_by_id(course_id)
    if course is None:
        abort(404)
    username = LOGGED_IN_USERNAME
    enrollment = get_enrollment(username, course_id)
    already_enrolled = enrollment is not None
    enrollment_success = request.args.get('enrollment_success') == '1'
    return render_template('course_details.html', course=course, already_enrolled=already_enrolled, enrollment_success=enrollment_success)

@app.route('/course/<course_id>/enroll', methods=['POST'])
def enroll_course(course_id):
    username = LOGGED_IN_USERNAME
    course = get_course_by_id(course_id)
    if course is None:
        abort(404)
    enrollments = read_enrollments()
    existing = get_enrollment(username, course_id)
    enrollment_success = False
    if existing is None:
        # Create new enrollment
        if enrollments:
            new_id = str(int(enrollments[-1]['enrollment_id']) + 1)
        else:
            new_id = '1'
        enrollment_date = datetime.date.today().isoformat()
        enrollment = {
            'enrollment_id': new_id,
            'username': username,
            'course_id': course_id,
            'enrollment_date': enrollment_date,
            'progress': 0,
            'status': 'In Progress'
        }
        enrollments.append(enrollment)
        write_enrollments(enrollments)
        enrollment_success = True
    # Redirect back to course_details with enrollment_success flag
    return redirect(url_for('course_details', course_id=course_id, enrollment_success='1' if enrollment_success else '0'))

@app.route('/my-courses')
def my_courses():
    username = LOGGED_IN_USERNAME
    enrollments = read_enrollments()
    courses = read_courses()
    enrolled_courses = []
    for enrollment in enrollments:
        if enrollment['username'] == username:
            course = get_course_by_id(enrollment['course_id'])
            if course:
                enrolled_courses.append({'course_id': course['course_id'],
                                         'title': course['title'],
                                         'progress': enrollment['progress']})
    return render_template('my_courses.html', enrolled_courses=enrolled_courses)

@app.route('/course/<course_id>/learn')
def course_learning(course_id):
    username = LOGGED_IN_USERNAME
    course = get_course_by_id(course_id)
    if course is None:
        abort(404)
    enrollment = get_enrollment(username, course_id)
    if enrollment is None:
        # Not enrolled, redirect to course_details
        return redirect(url_for('course_details', course_id=course_id))
    lessons = generate_lessons_for_course(course_id)

    progress = enrollment['progress']
    total_lessons = len(lessons)
    # Calculate current lesson index = number of lessons completed
    completed_lessons_count = int((progress * total_lessons) / 100)
    if completed_lessons_count >= total_lessons:
        current_lesson_index = total_lessons - 1
    else:
        current_lesson_index = completed_lessons_count

    # completed lessons indexes
    completed_lessons = list(range(completed_lessons_count))

    return render_template('course_learning.html', course=course, lessons=lessons, 
                           current_lesson_index=current_lesson_index,
                           completed_lessons=completed_lessons)

@app.route('/course/<course_id>/learn/complete', methods=['POST'])
def mark_lesson_complete(course_id):
    username = LOGGED_IN_USERNAME
    course = get_course_by_id(course_id)
    if course is None:
        abort(404)
    enrollment = get_enrollment(username, course_id)
    if enrollment is None:
        # Not enrolled
        return redirect(url_for('course_details', course_id=course_id))

    lessons = generate_lessons_for_course(course_id)
    total_lessons = len(lessons)

    progress = enrollment['progress']
    completed_lessons_count = int((progress * total_lessons) / 100)

    # Only allow to complete the lesson that is the next one in sequence
    next_lesson_to_complete = completed_lessons_count

    if next_lesson_to_complete >= total_lessons:
        # All lessons completed already
        certificate_generated = False
        return render_template('course_learning.html', course=course, lessons=lessons, 
                               current_lesson_index=total_lessons-1,
                               completed_lessons=list(range(total_lessons)),
                               progress=progress,
                               certificate_generated=certificate_generated)

    # Update progress: each lesson equals 100/total_lessons percent
    lesson_progress_increment = 100 // total_lessons
    # To avoid rounding issues sum we recalc progress by count

    new_completed_lessons_count = completed_lessons_count + 1

    new_progress = (new_completed_lessons_count * 100) // total_lessons
    # Clamp progress at 100
    if new_progress > 100:
        new_progress = 100

    # Update enrollment progress and status
    enrollments = read_enrollments()
    updated = False
    for e in enrollments:
        if e['username'] == username and e['course_id'] == course_id:
            e['progress'] = new_progress
            e['status'] = 'Completed' if new_progress == 100 else 'In Progress'
            updated = True
            break
    if updated:
        write_enrollments(enrollments)

    certificate_generated = False
    if new_progress == 100:
        # Check if certificate already exists
        certificates = read_certificates()
        exists = any(c['username'] == username and c['course_id'] == course_id for c in certificates)
        if not exists:
            if certificates:
                new_cert_id = str(int(certificates[-1]['certificate_id']) + 1)
            else:
                new_cert_id = '1'
            issue_date = datetime.date.today().isoformat()
            certificates.append({
                'certificate_id': new_cert_id,
                'username': username,
                'course_id': course_id,
                'issue_date': issue_date
            })
            write_certificates(certificates)
            certificate_generated = True

    # Recalculate data to render
    lessons = generate_lessons_for_course(course_id)
    completed_lessons = list(range(new_completed_lessons_count))

    current_lesson_index = 0 if new_completed_lessons_count >= total_lessons else new_completed_lessons_count

    return render_template('course_learning.html', course=course, lessons=lessons, 
                           current_lesson_index=current_lesson_index,
                           progress=new_progress,
                           completed_lessons=completed_lessons,
                           certificate_generated=certificate_generated)

@app.route('/assignments')
def my_assignments():
    username = LOGGED_IN_USERNAME
    assignments = read_assignments()
    submissions = read_submissions()
    # Show all assignments for courses user is enrolled in
    enrollments = read_enrollments()
    enrolled_course_ids = set(e['course_id'] for e in enrollments if e['username'] == username)
    user_assignments = [a for a in assignments if a['course_id'] in enrolled_course_ids]
    user_submissions = [s for s in submissions if s['username'] == username]

    return render_template('assignments.html', assignments=user_assignments, submissions=user_submissions)

@app.route('/assignments/<assignment_id>/submit', methods=['GET'])
def submit_assignment(assignment_id):
    username = LOGGED_IN_USERNAME
    assignments = read_assignments()
    assignment = None
    for a in assignments:
        if a['assignment_id'] == assignment_id:
            assignment = a
            break
    if assignment is None:
        abort(404)
    return render_template('submit_assignment.html', assignment=assignment)

@app.route('/assignments/<assignment_id>/submit', methods=['POST'])
def post_assignment(assignment_id):
    username = LOGGED_IN_USERNAME
    submission_text = request.form.get('submission_text', '').strip()
    if submission_text == '':
        # Re-render form with error maybe (not specified), just pass False success
        assignments = read_assignments()
        assignment = None
        for a in assignments:
            if a['assignment_id'] == assignment_id:
                assignment = a
                break
        return render_template('submit_assignment.html', assignment=assignment, submission_success=False)

    submissions = read_submissions()

    if submissions:
        new_id = str(int(submissions[-1]['submission_id']) + 1)
    else:
        new_id = '1'

    today_str = datetime.date.today().isoformat()

    # add new submission with no grade and no feedback
    new_submission = {
        'submission_id': new_id,
        'assignment_id': assignment_id,
        'username': username,
        'submission_text': submission_text,
        'submit_date': today_str,
        'grade': None,
        'feedback': None
    }
    submissions.append(new_submission)
    write_submissions(submissions)

    assignments = read_assignments()
    assignment = None
    for a in assignments:
        if a['assignment_id'] == assignment_id:
            assignment = a
            break

    return render_template('submit_assignment.html', assignment=assignment, submission_success=True)

@app.route('/certificates')
def certificates():
    username = LOGGED_IN_USERNAME
    certificates = read_certificates()
    user_certificates = [c for c in certificates if c['username'] == username]
    all_courses = read_courses()
    courses_dict = {c['course_id']:c['title'] for c in all_courses}
    return render_template('certificates.html', certificates=user_certificates, courses=courses_dict)

@app.route('/profile')
def user_profile():
    username = LOGGED_IN_USERNAME
    user = get_user_by_username(username)
    if user is None:
        abort(404)
    return render_template('profile.html', user=user)

@app.route('/profile/update', methods=['POST'])
def update_profile():
    username = LOGGED_IN_USERNAME
    email = request.form.get('email', '').strip()
    fullname = request.form.get('fullname', '').strip()
    if email == '' or fullname == '':
        user = get_user_by_username(username)
        return render_template('profile.html', user=user, update_success=False)
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
    user = get_user_by_username(username)
    return render_template('profile.html', user=user, update_success=updated)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
