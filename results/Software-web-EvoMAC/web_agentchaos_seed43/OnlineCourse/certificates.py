'''
Certificates page module for OnlineCourse web application.
Displays earned course completion certificates.
'''
from flask import Blueprint, render_template, session, redirect, url_for
import os
certificates_bp = Blueprint('certificates', __name__, template_folder='templates')
DATA_DIR = 'data'
def load_certificates(username):
    certificates = []
    filepath = os.path.join(DATA_DIR, 'certificates.txt')
    if not os.path.exists(filepath):
        return certificates
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            certificate_id, uname, course_id, issue_date = line.strip().split('|')
            if uname == username:
                certificates.append({
                    'certificate_id': certificate_id,
                    'course_id': course_id,
                    'issue_date': issue_date
                })
    return certificates
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
@certificates_bp.route('/certificates')
def certificates():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    username = session['username']
    certificates = load_certificates(username)
    courses = load_courses()
    certificates_info = []
    for cert in certificates:
        course = courses.get(cert['course_id'])
        if course:
            certificates_info.append({
                'certificate_id': cert['certificate_id'],
                'course_title': course['title'],
                'issue_date': cert['issue_date']
            })
    return render_template('certificates.html', certificates=certificates_info)