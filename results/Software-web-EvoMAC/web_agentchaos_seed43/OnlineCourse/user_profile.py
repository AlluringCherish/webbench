'''
User Profile page module for OnlineCourse web application.
Allows viewing and editing user profile.
'''
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
import os
user_profile_bp = Blueprint('user_profile', __name__, template_folder='templates')
DATA_DIR = 'data'
def load_users():
    users = {}
    with open(os.path.join(DATA_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            username, email, fullname = line.strip().split('|')
            users[username] = {'email': email, 'fullname': fullname}
    return users
def save_users(users):
    with open(os.path.join(DATA_DIR, 'users.txt'), 'w', encoding='utf-8') as f:
        for username, data in users.items():
            f.write(f"{username}|{data['email']}|{data['fullname']}\n")
@user_profile_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    username = session['username']
    users = load_users()
    user = users.get(username)
    if not user:
        flash('User not found.')
        return redirect(url_for('dashboard.dashboard'))
    if request.method == 'POST':
        email = request.form.get('profile-email', '').strip()
        fullname = request.form.get('profile-fullname', '').strip()
        if not email or not fullname:
            flash('Email and Full name cannot be empty.')
            return render_template('profile.html', email=email, fullname=fullname)
        users[username]['email'] = email
        users[username]['fullname'] = fullname
        save_users(users)
        flash('Profile updated successfully.')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('profile.html', email=user['email'], fullname=user['fullname'])