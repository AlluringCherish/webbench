'''
Dashboard page module for OnlineCourse web application.
Displays the learning dashboard with enrolled courses and progress.
'''
from flask import Blueprint, render_template, session, redirect, url_for
import os
dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')
DATA_DIR = 'data'
def load_users():
    users = {}
    with open(os.path.join(DATA_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            username, email, fullname = line.strip().split('|')
            users[username] = {'email': email, 'fullname': fullname}
    return users
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
@dashboard_bp.route('/')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    username = session['username']
    users = load_users()
    fullname = users.get(username, {}).get('fullname', username)
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
    return render_template('dashboard.html',
                           fullname=fullname,
                           enrolled_courses=enrolled_courses)