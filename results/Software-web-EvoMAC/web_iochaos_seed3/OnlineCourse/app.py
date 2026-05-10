'''
Main application file for OnlineCourse web application.
Defines all backend routes corresponding to frontend pages,
ensures root route '/' serves the Dashboard page as required,
and uses consistent URL routing for navigation.
Includes 404 error handler for improved user experience.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
import datetime
app = Flask(__name__, template_folder='templates')
DATA_DIR = 'data'
def read_users():
    users = {}
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    username, email, fullname = line.split('|')
                    users[username] = {'email': email, 'fullname': fullname}
    except FileNotFoundError:
        pass
    return users
def read_courses():
    courses = {}
    try:
        with open(os.path.join(DATA_DIR, 'courses.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    course_id = parts[0]
                    courses[course_id] = {
                        'title': parts[1],
                        'description': parts[2],
                        'category': parts[3],
                        'level': parts[4],
                        'duration': parts[5],
                        'status': parts[6]
                    }
    except FileNotFoundError:
        pass
    return courses
def read_enrollments():
    enrollments = []
    try:
        with open(os.path.join(DATA_DIR, 'enrollments.txt'), 'r') as f:
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
    with open(os.path.join(DATA_DIR, 'enrollments.txt'), 'w') as f:
        for e in enrollments:
            line = '|'.join([
                e['enrollment_id'],
                e['username'],
                e['course_id'],
                e['enrollment_date'],
                str(e['progress']),
                e['status']
            ])
            f.write(line + '\n')
def read_assignments():
    assignments = []
    try:
        with open(os.path.join(DATA_DIR, 'assignments.txt'), 'r') as f:
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
                        'max_points': max_points
                    })
    except FileNotFoundError:
        pass
    return assignments
def read_submissions():
    submissions = []
    try:
        with open(os.path.join(DATA_DIR, 'submissions.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    submission_id, assignment_id, username, submission_text, submit_date, grade, feedback = line.split('|')
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
    with open(os.path.join(DATA_DIR, 'submissions.txt'), 'w') as f:
        for s in submissions:
            line = '|'.join([
                s['submission_id'],
                s['assignment_id'],
                s['username'],
                s['submission_text'],
                s['submit_date'],
                s['grade'],
                s['feedback']
            ])
            f.write(line + '\n')
def read_certificates():
    certificates = []
    try:
        with open(os.path.join(DATA_DIR, 'certificates.txt'), 'r') as f:
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
    with open(os.path.join(DATA_DIR, 'certificates.txt'), 'w') as f:
        for c in certificates:
            line = '|'.join([
                c['certificate_id'],
                c['username'],
                c['course_id'],
                c['issue_date']
            ])
            f.write(line + '\n')
def get_next_id(items, id_field):
    max_id = 0
    for item in items:
        try:
            current_id = int(item[id_field])
            if current_id > max_id:
                max_id = current_id
        except:
            continue
    return str(max_id + 1)
# For demonstration, assume logged in user is 'john'
LOGGED_IN_USER = 'john'
@app.route('/')
def dashboard():
    '''
    Root route serving the Dashboard page as required.
    Loads user info and enrolled courses with progress.
    '''
    users = read_users()
    courses = read_courses()
    enrollments = read_enrollments()
    user = users.get(LOGGED_IN_USER, {'fullname': 'User'})
    user_enrollments = [e for e in enrollments if e['username'] == LOGGED_IN_USER]
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
    return render_template('dashboard.html',
                           fullname=user['fullname'],
                           enrolled_courses=enrolled_courses)
@app.route('/catalog')
def course_catalog():
    '''
    Course Catalog page route.
    Displays all active courses with search functionality.
    '''
    courses = read_courses()
    search_query = request.args.get('search', '').lower()
    filtered_courses = []
    for course_id, course in courses.items():
        if course['status'] != 'Active':
            continue
        if search_query in course['title'].lower() or search_query in course['description'].lower():
            filtered_courses.append({'course_id': course_id, **course})
    return render_template('course_catalog.html', courses=filtered_courses, search_query=search_query)
@app.route('/course/<course_id>')
def course_details(course_id):
    '''
    Course Details page route.
    Shows detailed info and enrollment option.
    '''
    courses = read_courses()
    enrollments = read_enrollments()
    course = courses.get(course_id)
    if not course:
        return "Course not found", 404
    # Check if user already enrolled
    already_enrolled = any(e['username'] == LOGGED_IN_USER and e['course_id'] == course_id for e in enrollments)
    return render_template('course_details.html',
                           course_id=course_id,
                           title=course['title'],
                           description=course['description'],
                           already_enrolled=already_enrolled)
@app.route('/course/<course_id>/enroll', methods=['POST'])
def enroll_course(course_id):
    '''
    Enroll logged in user in the course if not already enrolled.
    Adds entry to enrollments.txt with 0% progress and current date.
    '''
    enrollments = read_enrollments()
    # Check if already enrolled
    for e in enrollments:
        if e['username'] == LOGGED_IN_USER and e['course_id'] == course_id:
            return redirect(url_for('course_details', course_id=course_id))
    new_id = get_next_id(enrollments, 'enrollment_id')
    today = datetime.date.today().isoformat()
    enrollments.append({
        'enrollment_id': new_id,
        'username': LOGGED_IN_USER,
        'course_id': course_id,
        'enrollment_date': today,
        'progress': 0,
        'status': 'In Progress'
    })
    write_enrollments(enrollments)
    return redirect(url_for('my_courses'))
@app.route('/my-courses')
def my_courses():
    '''
    My Courses page route.
    Displays enrolled courses with progress and continue learning buttons.
    '''
    users = read_users()
    courses = read_courses()
    enrollments = read_enrollments()
    user = users.get(LOGGED_IN_USER, {'fullname': 'User'})
    user_enrollments = [e for e in enrollments if e['username'] == LOGGED_IN_USER]
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
    return render_template('my_courses.html',
                           fullname=user['fullname'],
                           enrolled_courses=enrolled_courses)
@app.route('/learning/<course_id>')
def course_learning(course_id):
    '''
    Course Learning page route.
    Displays lessons and current lesson content with progress tracking.
    For simplicity, lessons are simulated as numbered lessons.
    '''
    courses = read_courses()
    enrollments = read_enrollments()
    course = courses.get(course_id)
    if not course:
        return "Course not found", 404
    enrollment = None
    for e in enrollments:
        if e['username'] == LOGGED_IN_USER and e['course_id'] == course_id:
            enrollment = e
            break
    if not enrollment:
        return redirect(url_for('course_details', course_id=course_id))
    # Simulate lessons as 10 lessons
    total_lessons = 10
    completed_lessons = int(enrollment['progress'] * total_lessons / 100)
    # Current lesson is next incomplete lesson
    current_lesson = completed_lessons + 1 if completed_lessons < total_lessons else total_lessons
    lessons = [{'lesson_number': i+1, 'completed': i < completed_lessons} for i in range(total_lessons)]
    lesson_content = f"Content for lesson {current_lesson} of {course['title']}."
    return render_template('course_learning.html',
                           course_id=course_id,
                           title=course['title'],
                           lessons=lessons,
                           current_lesson=current_lesson,
                           lesson_content=lesson_content,
                           progress=enrollment['progress'])
@app.route('/learning/<course_id>/complete', methods=['POST'])
def mark_lesson_complete(course_id):
    '''
    Marks current lesson as completed, updates progress in enrollments.txt,
    generates certificate if progress reaches 100%.
    Lessons must be completed in sequence.
    '''
    enrollments = read_enrollments()
    certificates = read_certificates()
    courses = read_courses()
    course = courses.get(course_id)
    if not course:
        return "Course not found", 404
    enrollment = None
    for e in enrollments:
        if e['username'] == LOGGED_IN_USER and e['course_id'] == course_id:
            enrollment = e
            break
    if not enrollment:
        return redirect(url_for('course_details', course_id=course_id))
    total_lessons = 10
    completed_lessons = int(enrollment['progress'] * total_lessons / 100)
    if completed_lessons >= total_lessons:
        # Already completed
        return redirect(url_for('course_learning', course_id=course_id))
    # Mark next lesson complete
    completed_lessons += 1
    new_progress = int((completed_lessons / total_lessons) * 100)
    enrollment['progress'] = new_progress
    if new_progress == 100:
        enrollment['status'] = 'Completed'
        # Generate certificate if not exists
        cert_exists = any(c['username'] == LOGGED_IN_USER and c['course_id'] == course_id for c in certificates)
        if not cert_exists:
            new_cert_id = get_next_id(certificates, 'certificate_id')
            today = datetime.date.today().isoformat()
            certificates.append({
                'certificate_id': new_cert_id,
                'username': LOGGED_IN_USER,
                'course_id': course_id,
                'issue_date': today
            })
            write_certificates(certificates)
    write_enrollments(enrollments)
    return redirect(url_for('course_learning', course_id=course_id))
@app.route('/assignments')
def my_assignments():
    '''
    My Assignments page route.
    Displays all assignments for courses user is enrolled in.
    '''
    assignments = read_assignments()
    enrollments = read_enrollments()
    user_enrollments = [e for e in enrollments if e['username'] == LOGGED_IN_USER]
    enrolled_course_ids = {e['course_id'] for e in user_enrollments}
    user_assignments = [a for a in assignments if a['course_id'] in enrolled_course_ids]
    submissions = read_submissions()
    submitted_assignment_ids = {s['assignment_id'] for s in submissions if s['username'] == LOGGED_IN_USER}
    return render_template('my_assignments.html',
                           assignments=user_assignments,
                           submitted_assignment_ids=submitted_assignment_ids)
@app.route('/assignments/submit/<assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    '''
    Submit Assignment page route.
    GET: Show assignment info and submission form.
    POST: Save submission to submissions.txt with status "Submitted".
    '''
    assignments = read_assignments()
    assignment = None
    for a in assignments:
        if a['assignment_id'] == assignment_id:
            assignment = a
            break
    if not assignment:
        return "Assignment not found", 404
    if request.method == 'POST':
        submission_text = request.form.get('submission_text', '').strip()
        if not submission_text:
            return render_template('submit_assignment.html',
                                   assignment=assignment,
                                   error="Submission text cannot be empty.")
        submissions = read_submissions()
        new_id = get_next_id(submissions, 'submission_id')
        today = datetime.date.today().isoformat()
        submissions.append({
            'submission_id': new_id,
            'assignment_id': assignment_id,
            'username': LOGGED_IN_USER,
            'submission_text': submission_text.replace('\n', ' '),
            'submit_date': today,
            'grade': '',
            'feedback': ''
        })
        write_submissions(submissions)
        confirmation = "Assignment submitted successfully."
        return render_template('submit_assignment.html',
                               assignment=assignment,
                               confirmation=confirmation)
    else:
        return render_template('submit_assignment.html', assignment=assignment)
@app.route('/certificates')
def my_certificates():
    '''
    Certificates page route.
    Displays certificates for completed courses.
    '''
    certificates = read_certificates()
    courses = read_courses()
    user_certs = [c for c in certificates if c['username'] == LOGGED_IN_USER]
    certs_display = []
    for c in user_certs:
        course = courses.get(c['course_id'])
        if course:
            certs_display.append({
                'certificate_id': c['certificate_id'],
                'course_id': c['course_id'],
                'course_title': course['title'],
                'issue_date': c['issue_date']
            })
    return render_template('certificates.html', certificates=certs_display)
@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    '''
    User Profile page route.
    GET: Display profile info.
    POST: Update profile info in users.txt.
    '''
    users = read_users()
    user = users.get(LOGGED_IN_USER)
    if not user:
        return "User not found", 404
    if request.method == 'POST':
        email = request.form.get('profile_email', '').strip()
        fullname = request.form.get('profile_fullname', '').strip()
        if not email or not fullname:
            return render_template('user_profile.html',
                                   email=user['email'],
                                   fullname=user['fullname'],
                                   error="Email and Full name cannot be empty.")
        # Update user info
        users[LOGGED_IN_USER]['email'] = email
        users[LOGGED_IN_USER]['fullname'] = fullname
        # Write back to users.txt
        with open(os.path.join(DATA_DIR, 'users.txt'), 'w') as f:
            for username, info in users.items():
                line = '|'.join([username, info['email'], info['fullname']])
                f.write(line + '\n')
        return render_template('user_profile.html',
                               email=email,
                               fullname=fullname,
                               confirmation="Profile updated successfully.")
    else:
        return render_template('user_profile.html',
                               email=user['email'],
                               fullname=user['fullname'])
@app.errorhandler(404)
def page_not_found(e):
    '''
    Custom 404 error handler to improve user experience.
    '''
    return render_template('404.html'), 404
if __name__ == '__main__':
    app.run(debug=True)