'''
Course Learning page module for OnlineCourse web application.
Allows viewing lessons, marking completion, and tracking progress.
'''
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
import os
from datetime import datetime
course_learning_bp = Blueprint('course_learning', __name__, template_folder='templates')
DATA_DIR = 'data'
# For simplicity, lessons data is hardcoded here as no lessons.txt is defined in requirements.
# Each course has a list of lessons in sequence.
LESSONS_DATA = {
    '1': [
        {'lesson_id': '1', 'title': 'Introduction to Python', 'content': 'Welcome to Python programming.'},
        {'lesson_id': '2', 'title': 'Variables and Data Types', 'content': 'Learn about variables and data types.'},
        {'lesson_id': '3', 'title': 'Control Structures', 'content': 'If statements, loops, and more.'}
    ],
    '2': [
        {'lesson_id': '1', 'title': 'HTML Basics', 'content': 'Learn the basics of HTML.'},
        {'lesson_id': '2', 'title': 'CSS Styling', 'content': 'Style your web pages with CSS.'},
        {'lesson_id': '3', 'title': 'JavaScript Introduction', 'content': 'Add interactivity with JavaScript.'}
    ],
    '3': [
        {'lesson_id': '1', 'title': 'Data Science Overview', 'content': 'Introduction to data science.'},
        {'lesson_id': '2', 'title': 'Data Analysis with Python', 'content': 'Use Python for data analysis.'},
        {'lesson_id': '3', 'title': 'Machine Learning Basics', 'content': 'Basics of machine learning.'}
    ]
}
def load_enrollment(username, course_id):
    enrollments = []
    with open(os.path.join(DATA_DIR, 'enrollments.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            enrollment_id, uname, cid, enrollment_date, progress, status = line.strip().split('|')
            if uname == username and cid == course_id:
                return {
                    'enrollment_id': enrollment_id,
                    'username': uname,
                    'course_id': cid,
                    'enrollment_date': enrollment_date,
                    'progress': int(progress),
                    'status': status
                }
    return None
def update_enrollment_progress(enrollment_id, username, course_id, new_progress, new_status):
    lines = []
    filepath = os.path.join(DATA_DIR, 'enrollments.txt')
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in lines:
            parts = line.strip().split('|')
            if parts[0] == enrollment_id and parts[1] == username and parts[2] == course_id:
                parts[4] = str(new_progress)
                parts[5] = new_status
                f.write('|'.join(parts) + '\n')
            else:
                f.write(line)
def get_next_certificate_id():
    max_id = 0
    filepath = os.path.join(DATA_DIR, 'certificates.txt')
    if not os.path.exists(filepath):
        return 1
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            certificate_id = int(line.strip().split('|')[0])
            if certificate_id > max_id:
                max_id = certificate_id
    return max_id + 1
def certificate_exists(username, course_id):
    filepath = os.path.join(DATA_DIR, 'certificates.txt')
    if not os.path.exists(filepath):
        return False
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            certificate_id, uname, cid, issue_date = line.strip().split('|')
            if uname == username and cid == course_id:
                return True
    return False
def generate_certificate(username, course_id):
    if certificate_exists(username, course_id):
        return
    certificate_id = get_next_certificate_id()
    issue_date = datetime.now().strftime('%Y-%m-%d')
    entry = f"{certificate_id}|{username}|{course_id}|{issue_date}\n"
    with open(os.path.join(DATA_DIR, 'certificates.txt'), 'a', encoding='utf-8') as f:
        f.write(entry)
@course_learning_bp.route('/course-learning/<course_id>', methods=['GET', 'POST'])
def course_learning(course_id):
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    username = session['username']
    lessons = LESSONS_DATA.get(course_id)
    if not lessons:
        flash('Course lessons not found.')
        return redirect(url_for('my_courses.my_courses'))
    enrollment = load_enrollment(username, course_id)
    if not enrollment:
        flash('You are not enrolled in this course.')
        return redirect(url_for('my_courses.my_courses'))
    completed_lessons_count = int(enrollment['progress'] * len(lessons) / 100)
    current_lesson_index = completed_lessons_count
    if request.method == 'POST':
        # Mark current lesson complete
        if current_lesson_index < len(lessons):
            # Lessons must be completed in sequence
            current_lesson_index += 1
            new_progress = int((current_lesson_index / len(lessons)) * 100)
            new_status = 'Completed' if new_progress == 100 else 'In Progress'
            update_enrollment_progress(enrollment['enrollment_id'], username, course_id, new_progress, new_status)
            if new_progress == 100:
                generate_certificate(username, course_id)
            flash('Lesson marked as complete.')
            return redirect(url_for('course_learning.course_learning', course_id=course_id))
    # Show current lesson content
    if current_lesson_index >= len(lessons):
        current_lesson_index = len(lessons) - 1
    current_lesson = lessons[current_lesson_index]
    return render_template('course_learning.html',
                           lessons=lessons,
                           current_lesson=current_lesson,
                           current_lesson_index=current_lesson_index,
                           progress=enrollment['progress'])