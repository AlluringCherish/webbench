'''
Course Details page module for OnlineCourse web application.
Displays detailed course info and allows enrollment.
'''
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
import os
from datetime import datetime
course_details_bp = Blueprint('course_details', __name__, template_folder='templates')
DATA_DIR = 'data'
def load_course(course_id):
    with open(os.path.join(DATA_DIR, 'courses.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            cid, title, description, category, level, duration, status = line.strip().split('|')
            if cid == course_id and status == 'Active':
                return {
                    'course_id': cid,
                    'title': title,
                    'description': description,
                    'category': category,
                    'level': level,
                    'duration': duration,
                    'status': status
                }
    return None
def is_enrolled(username, course_id):
    with open(os.path.join(DATA_DIR, 'enrollments.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            enrollment_id, uname, cid, enrollment_date, progress, status = line.strip().split('|')
            if uname == username and cid == course_id:
                return True
    return False
def get_next_enrollment_id():
    max_id = 0
    with open(os.path.join(DATA_DIR, 'enrollments.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            enrollment_id = int(line.strip().split('|')[0])
            if enrollment_id > max_id:
                max_id = enrollment_id
    return max_id + 1
@course_details_bp.route('/course/<course_id>', methods=['GET', 'POST'])
def course_details(course_id):
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    username = session['username']
    course = load_course(course_id)
    if not course:
        flash('Course not found or inactive.')
        return redirect(url_for('catalog.catalog'))
    enrolled = is_enrolled(username, course_id)
    if request.method == 'POST':
        if not enrolled:
            enrollment_id = get_next_enrollment_id()
            enrollment_date = datetime.now().strftime('%Y-%m-%d')
            new_entry = f"{enrollment_id}|{username}|{course_id}|{enrollment_date}|0|In Progress\n"
            with open(os.path.join(DATA_DIR, 'enrollments.txt'), 'a', encoding='utf-8') as f:
                f.write(new_entry)
            flash('Successfully enrolled in the course.')
            return redirect(url_for('my_courses.my_courses'))
        else:
            flash('You are already enrolled in this course.')
    return render_template('course_details.html', course=course, enrolled=enrolled)