'''
Course Catalog page module for OnlineCourse web application.
Allows browsing and searching available courses.
'''
from flask import Blueprint, render_template, request, session, redirect, url_for
import os
catalog_bp = Blueprint('catalog', __name__, template_folder='templates')
DATA_DIR = 'data'
def load_courses():
    courses = []
    with open(os.path.join(DATA_DIR, 'courses.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            course_id, title, description, category, level, duration, status = line.strip().split('|')
            if status == 'Active':
                courses.append({
                    'course_id': course_id,
                    'title': title,
                    'description': description,
                    'category': category,
                    'level': level,
                    'duration': duration,
                    'status': status
                })
    return courses
@catalog_bp.route('/catalog', methods=['GET', 'POST'])
def catalog():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    search_query = ''
    courses = load_courses()
    if request.method == 'POST':
        search_query = request.form.get('search-input', '').strip().lower()
        if search_query:
            courses = [c for c in courses if search_query in c['title'].lower() or search_query in c['description'].lower()]
    return render_template('catalog.html', courses=courses, search_query=search_query)