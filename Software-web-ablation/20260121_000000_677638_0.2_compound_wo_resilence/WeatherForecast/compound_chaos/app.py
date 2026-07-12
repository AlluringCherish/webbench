from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

DATA_PATH = './data'
COURSES_FILE = os.path.join(DATA_PATH, 'courses.txt')
ENROLLMENTS_FILE = os.path.join(DATA_PATH, 'enrollments.txt')
STUDENTS_FILE = os.path.join(DATA_PATH, 'students.txt')

courses = []
students = []
enrollments = []

# Utility functions to load data

def load_courses():
    global courses
    courses = []
    if os.path.exists(COURSES_FILE):
        with open(COURSES_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    courses.append({'code': parts[0], 'title': parts[1], 'description': parts[2]})


def load_students():
    global students
    students = []
    if os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    students.append({'id': parts[0], 'name': parts[1], 'email': parts[2]})


def load_enrollments():
    global enrollments
    enrollments = []
    if os.path.exists(ENROLLMENTS_FILE):
        with open(ENROLLMENTS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    enrollments.append({'student_id': parts[0], 'course_code': parts[1]})


# Load data before first request
@app.before_first_request
def load_data():
    load_courses()
    load_students()
    load_enrollments()


@app.route('/')
def dashboard():
    return render_template('dashboard.html', students=students, courses=courses)


@app.route('/students')
def students_page():
    return render_template('students.html', students=students)


@app.route('/courses')
def courses_page():
    return render_template('courses.html', courses=courses)


@app.route('/enrollments')
def enrollments_page():
    student_dict = {s['id']: s['name'] for s in students}
    course_dict = {c['code']: c['title'] for c in courses}
    enriched = []
    for e in enrollments:
        enriched.append({
            'student_id': e['student_id'],
            'student_name': student_dict.get(e['student_id'], 'Unknown'),
            'course_code': e['course_code'],
            'course_title': course_dict.get(e['course_code'], 'Unknown')
        })
    return render_template('enrollments.html', enrollments=enriched)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    error = None
    if request.method == 'POST':
        new_id = request.form.get('id', '').strip()
        new_name = request.form.get('name', '').strip()
        new_email = request.form.get('email', '').strip()
        if not new_id or not new_name or not new_email:
            error = 'All fields are required.'
        else:
            # Check duplicates
            for s in students:
                if s['id'] == new_id:
                    error = 'Student ID already exists.'
                    break
        if not error:
            students.append({'id': new_id, 'name': new_name, 'email': new_email})
            with open(STUDENTS_FILE, 'a') as f:
                f.write(f"{new_id}|{new_name}|{new_email}\n")
            return redirect(url_for('students_page'))
    return render_template('add_student.html', error=error)


@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    error = None
    if request.method == 'POST':
        new_code = request.form.get('code', '').strip()
        new_title = request.form.get('title', '').strip()
        new_desc = request.form.get('description', '').strip()
        if not new_code or not new_title or not new_desc:
            error = 'All fields are required.'
        else:
            for c in courses:
                if c['code'] == new_code:
                    error = 'Course code already exists.'
                    break
        if not error:
            courses.append({'code': new_code, 'title': new_title, 'description': new_desc})
            with open(COURSES_FILE, 'a') as f:
                f.write(f"{new_code}|{new_title}|{new_desc}\n")
            return redirect(url_for('courses_page'))
    return render_template('add_course.html', error=error)


@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    error = None
    if request.method == 'POST':
        student_id = request.form.get('student_id', '').strip()
        course_code = request.form.get('course_code', '').strip()
        if not student_id or not course_code:
            error = 'Student and course must be selected.'
        else:
            # Check if enrollment exists
            for e in enrollments:
                if e['student_id'] == student_id and e['course_code'] == course_code:
                    error = 'Enrollment already exists.'
                    break
        if not error:
            enrollments.append({'student_id': student_id, 'course_code': course_code})
            with open(ENROLLMENTS_FILE, 'a') as f:
                f.write(f"{student_id}|{course_code}\n")
            return redirect(url_for('enrollments_page'))
    return render_template('enroll.html', students=students, courses=courses, error=error)


if __name__ == '__main__':
    app.run(debug=True)
