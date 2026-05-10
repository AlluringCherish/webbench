'''
Authentication module for OnlineCourse web application.
Provides user login and logout functionality with session management.
'''
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import os
auth = Blueprint('auth', __name__, template_folder='templates')
DATA_DIR = 'data'
def load_users():
    users = {}
    filepath = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(filepath):
        return users
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 3:
                username, email, fullname = parts
                users[username] = {'email': email, 'fullname': fullname}
    return users
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        # Already logged in, redirect to dashboard
        return redirect(url_for('dashboard.dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()  # Password is mocked, not used
        users = load_users()
        if username in users:
            # Mock authentication: accept any password if username exists
            session['username'] = username
            flash(f'Welcome, {users[username]["fullname"]}!', 'success')
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Invalid username.', 'error')
            return render_template('login.html', username=username)
    return render_template('login.html')
@auth.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))