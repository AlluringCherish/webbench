'''
My Assignments page module for OnlineCourse web application.
Displays assignments and allows submission.
'''
from flask import Blueprint, render_template, session, redirect, url_for
import os
from datetime import datetime
my_assignments_bp = Blueprint('my_assignments', __name__, template_folder='templates')
DATA_DIR = 'data'
def load_assignments():
    assignments = []
    with open(os.path.join(DATA_DIR, 'assignments.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            assignment_id, course_id, title, description, due_date, max_points = line.strip().split('|')
            assignments.append({
                'assignment_id': assignment_id,
                'course_id': course_id,
                'title': title,
                'description': description,
                'due_date': due_date,
                'max_points': max_points
            })
    return assignments
def load_submissions(username):
    submissions = {}
    filepath = os.path.join(DATA_DIR, 'submissions.txt')
    if not os.path.exists(filepath):
        return submissions
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            submission_id, assignment_id, uname, submission_text, submit_date, grade, feedback = line.strip().split('|')
            if uname == username:
                submissions[assignment_id] = {
                    'submission_id': submission_id,
                    'submission_text': submission_text,
                    'submit_date': submit_date,
                    'grade': grade,
                    'feedback': feedback
                }
    return submissions
@my_assignments_bp.route('/my-assignments')
def my_assignments():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    username = session['username']
    assignments = load_assignments()
    submissions = load_submissions(username)
    # Show assignments with submission status
    assignments_status = []
    for assignment in assignments:
        submitted = assignment['assignment_id'] in submissions
        assignments_status.append({
            'assignment_id': assignment['assignment_id'],
            'title': assignment['title'],
            'description': assignment['description'],
            'due_date': assignment['due_date'],
            'max_points': assignment['max_points'],
            'submitted': submitted
        })
    return render_template('my_assignments.html', assignments=assignments_status)