'''
Submit Assignment page module for OnlineCourse web application.
Allows users to submit assignment text responses.
'''
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
import os
from datetime import datetime
submit_assignment_bp = Blueprint('submit_assignment', __name__, template_folder='templates')
DATA_DIR = 'data'
def load_assignment(assignment_id):
    with open(os.path.join(DATA_DIR, 'assignments.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            aid, course_id, title, description, due_date, max_points = line.strip().split('|')
            if aid == assignment_id:
                return {
                    'assignment_id': aid,
                    'course_id': course_id,
                    'title': title,
                    'description': description,
                    'due_date': due_date,
                    'max_points': max_points
                }
    return None
def get_next_submission_id():
    max_id = 0
    filepath = os.path.join(DATA_DIR, 'submissions.txt')
    if not os.path.exists(filepath):
        return 1
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            submission_id = int(line.strip().split('|')[0])
            if submission_id > max_id:
                max_id = submission_id
    return max_id + 1
@submit_assignment_bp.route('/submit-assignment/<assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    username = session['username']
    assignment = load_assignment(assignment_id)
    if not assignment:
        flash('Assignment not found.')
        return redirect(url_for('my_assignments.my_assignments'))
    if request.method == 'POST':
        submission_text = request.form.get('submission-text', '').strip()
        if not submission_text:
            flash('Submission text cannot be empty.')
            return render_template('submit_assignment.html', assignment=assignment)
        submission_id = get_next_submission_id()
        submit_date = datetime.now().strftime('%Y-%m-%d')
        entry = f"{submission_id}|{assignment_id}|{username}|{submission_text}|{submit_date}|0|Pending\n"
        with open(os.path.join(DATA_DIR, 'submissions.txt'), 'a', encoding='utf-8') as f:
            f.write(entry)
        flash('Assignment submitted successfully.')
        return redirect(url_for('my_assignments.my_assignments'))
    return render_template('submit_assignment.html', assignment=assignment)