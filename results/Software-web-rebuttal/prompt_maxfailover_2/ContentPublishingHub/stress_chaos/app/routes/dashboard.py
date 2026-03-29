from flask import Blueprint, render_template, session

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    # Dummy user info and recent activity
    user_info = {'username': session.get('username', 'guest')}
    recent_activity = []
    # Render dashboard view
    return render_template('dashboard.html', user=user_info, recent_activity=recent_activity)
