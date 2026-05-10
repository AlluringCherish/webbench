'''
My Courses page module for OnlineCourse web application.
Displays user's enrolled courses and progress.
'''
from flask import Blueprint, render_template, session, redirect, url_for
import os
my_courses_bp = Blueprint('my_courses', __name__, template_folder='templates')
DATA_DIR = 'data'
def load_enrollments(username):
    enrollments = []
    with open(os.path.join(DATA_DIR, 'enrollments.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            enrollment_id, uname, course_id, enrollment_date, progress, status = line.strip().split('|')
            if uname == username:
                enrollments.append({
                    'enrollment_id': enrollment_id,
                    'course_id': course_id,
                    'enrollment_date': enrollment_date,
                    'progress': int(progress),
                    'status': status
                })
    return enrollments
def load_courses():
    courses = {}
    with open(os.path.join(DATA_DIR, 'courses.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            course_id, title, description, category, level, duration, status = line.strip().split('|')
            courses[course_id] = {
                'title': title,
                'description': description,
                'category': category,
                'level': level,
                'duration': duration,
                'status': status
            }
    return courses
@my_courses_bp.route('/my-courses')
def my_courses():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    username = session['username']
    enrollments = load_enrollments(username)
    courses = load_courses()
    enrolled_courses = []
    for enrollment in enrollments:
        course = courses.get(enrollment['course_id'])
        if course:
            enrolled_courses.append({
                'course_id': enrollment['course_id'],
                'title': course['title'],
                'progress': enrollment['progress'],
                'status': enrollment['status']
            })
    return render_template('my_courses.html', enrolled_courses=enrolled_courses)