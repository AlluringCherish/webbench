from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Data file paths
data_dir = 'data'
courses_file = os.path.join(data_dir, 'courses.txt')
enrollments_file = os.path.join(data_dir, 'enrollments.txt')
assignments_file = os.path.join(data_dir, 'assignments.txt')
submissions_file = os.path.join(data_dir, 'submissions.txt')
certificates_file = os.path.join(data_dir, 'certificates.txt')
users_file = os.path.join(data_dir, 'users.txt')

# Helper functions to read data

def read_courses():
    courses = []
    with open(courses_file) as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            # course_id|title|category|level|duration|status
            if len(parts) == 6:
                course = {
                    'course_id': parts[0],
                    'title': parts[1],
                    'category': parts[2],
                    'level': parts[3],
                    'duration': parts[4],
                    'status': parts[5],
                }
                courses.append(course)
    return courses

def read_enrollments():
    enrollments = []
    with open(enrollments_file) as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            # enrollment_id|username|course_id|enrollment_date|progress|status
            parts = line.split('|')
            if len(parts) == 6:
                enrollment = {
                    'enrollment_id': parts[0],
                    'username': parts[1],
                    'course_id': parts[2],
                    'enrollment_date': parts[3],
                    'progress': parts[4],
                    'status': parts[5],
                }
                enrollments.append(enrollment)
    return enrollments

def read_assignments():
    assignments = []
    with open(assignments_file) as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            # assignment_id|course_id|title|description|due_date|max_points
            parts = line.split('|')
            if len(parts) == 6:
                assignment = {
                    'assignment_id': parts[0],
                    'course_id': parts[1],
                    'title': parts[2],
                    'description': parts[3],
                    'due_date': parts[4],
                    'max_points': parts[5],
                }
                assignments.append(assignment)
    return assignments

def read_submissions():
    submissions = []
    with open(submissions_file) as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            # submission_id|assignment_id|username|submission_text|submit_date|grade|feedback
            parts = line.split('|')
            if len(parts) == 7:
                submission = {
                    'submission_id': parts[0],
                    'assignment_id': parts[1],
                    'username': parts[2],
                    'submission_text': parts[3],
                    'submit_date': parts[4],
                    'grade': parts[5],
                    'feedback': parts[6],
                }
                submissions.append(submission)
    return submissions

def read_certificates():
    certificates = []
    with open(certificates_file) as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            # certificate_id|username|course_id|issue_date
            parts = line.split('|')
            if len(parts) == 4:
                certificate = {
                    'certificate_id': parts[0],
                    'username': parts[1],
                    'course_id': parts[2],
                    'issue_date': parts[3],
                }
                certificates.append(certificate)
    return certificates

def read_users():
    users = []
    with open(users_file) as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            # username|email|fullname
            parts = line.split('|')
            if len(parts) == 3:
                user = {
                    'username': parts[0],
                    'email': parts[1],
                    'fullname': parts[2],
                }
                users.append(user)
    return users

# Route: Dashboard (no root '/', using /dashboard)
@app.route('/dashboard')
def dashboard():
    # Show overview of enrolled courses with progress and status
    enrollments = read_enrollments()
    courses = read_courses()
    users = read_users()
    current_user = users[0] if users else {'username': 'john', 'email': 'john@example.com', 'fullname': 'John Doe'}
    # Filter enrollments by current user
    user_enrollments = [e for e in enrollments if e['username'] == current_user['username']]
    # Attach course titles
    for e in user_enrollments:
        for c in courses:
            if c['course_id'] == e['course_id']:
                e['course_title'] = c['title']
                break
    return render_template('dashboard.html', enrollments=user_enrollments, user=current_user)

# Route: Courses catalog page (GET) showing all courses
@app.route('/catalog')
def catalog():
    courses = read_courses()
    return render_template('catalog.html', courses=courses)

# Route: Enroll in a course (POST)
@app.route('/enroll/<course_id>', methods=['POST'])
def enroll(course_id):
    users = read_users()
    current_user = users[0] if users else {'username': 'john'}
    enrollments = read_enrollments()
    new_id = str(len(enrollments)+1)
    from datetime import datetime
    today = datetime.today().strftime('%Y-%m-%d')
    # Append the enrollment
    with open(enrollments_file, 'a') as f:
        f.write(f"{new_id}|{current_user['username']}|{course_id}|{today}|0|Active\n")
    return redirect(url_for('dashboard'))

# Route: Course details page (GET)
@app.route('/course/<course_id>')
def course_details(course_id):
    courses = read_courses()
    enrollments = read_enrollments()
    assignments = read_assignments()
    users = read_users()
    current_user = users[0] if users else {'username': 'john'}
    course = next((c for c in courses if c['course_id'] == course_id), None)
    if not course:
        return redirect(url_for('catalog'))
    # Get user's enrollment
    enrollment = next((e for e in enrollments if e['course_id'] == course_id and e['username'] == current_user['username']), None)
    # Course assignments
    course_assignments = [a for a in assignments if a['course_id'] == course_id]
    return render_template('course_details.html', course=course, enrollment=enrollment, assignments=course_assignments, user=current_user)

# Route: Assignment submission page (GET)
@app.route('/assignment/<assignment_id>/submit', methods=['GET'])
def assignment_submit_get(assignment_id):
    assignments = read_assignments()
    assignment = next((a for a in assignments if a['assignment_id'] == assignment_id), None)
    users = read_users()
    current_user = users[0] if users else {'username': 'john'}
    if not assignment:
        return redirect(url_for('dashboard'))
    return render_template('assignment_submit.html', assignment=assignment, user=current_user)

# Route: Assignment submission page (POST)
@app.route('/assignment/<assignment_id>/submit', methods=['POST'])
def assignment_submit_post(assignment_id):
    submission_text = request.form.get('submission_text', '')
    submissions = read_submissions()
    users = read_users()
    current_user = users[0] if users else {'username': 'john'}
    new_id = str(len(submissions)+1)
    from datetime import datetime
    today = datetime.today().strftime('%Y-%m-%d')
    with open(submissions_file, 'a') as f:
        f.write(f"{new_id}|{assignment_id}|{current_user['username']}|{submission_text}|{today}| | \n")
    return redirect(url_for('dashboard'))

# Route: Certificates page (GET)
@app.route('/certificates')
def certificates():
    certificates = read_certificates()
    courses = read_courses()
    users = read_users()
    current_user = users[0] if users else {'username': 'john'}
    user_certs = [c for c in certificates if c['username'] == current_user['username']]
    for c in user_certs:
        course = next((cs for cs in courses if cs['course_id'] == c['course_id']), None)
        c['course_title'] = course['title'] if course else 'Unknown'
    return render_template('certificates.html', certificates=user_certs, user=current_user)

if __name__ == '__main__':
    app.run(debug=True)
