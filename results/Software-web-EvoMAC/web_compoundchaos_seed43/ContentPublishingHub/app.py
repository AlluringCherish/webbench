'''
Flask route and view function for the Dashboard page of ContentPublishingHub.
Displays welcome message, quick stats, and recent activity feed.
Reads data from local text files in 'data' directory.
'''
from flask import Blueprint, render_template, session
import os
from datetime import datetime
dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')
DATA_DIR = 'data'
def read_users():
    users = {}
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                username, email, fullname, created_date = line.split('|')
                users[username] = {
                    'email': email,
                    'fullname': fullname,
                    'created_date': created_date
                }
    except FileNotFoundError:
        pass
    return users
def read_articles():
    articles = []
    try:
        with open(os.path.join(DATA_DIR, 'articles.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 10:
                    continue
                article = {
                    'article_id': parts[0],
                    'title': parts[1],
                    'author': parts[2],
                    'category': parts[3],
                    'status': parts[4],
                    'tags': parts[5].split(',') if parts[5] else [],
                    'featured_image': parts[6],
                    'meta_description': parts[7],
                    'created_date': parts[8],
                    'publish_date': parts[9] if len(parts) > 9 else ''
                }
                articles.append(article)
    except FileNotFoundError:
        pass
    return articles
def read_article_versions():
    versions = []
    try:
        with open(os.path.join(DATA_DIR, 'article_versions.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                version = {
                    'version_id': parts[0],
                    'article_id': parts[1],
                    'version_number': int(parts[2]),
                    'content': parts[3],
                    'author': parts[4],
                    'created_date': parts[5],
                    'change_summary': parts[6]
                }
                versions.append(version)
    except FileNotFoundError:
        pass
    return versions
def read_approvals():
    approvals = []
    try:
        with open(os.path.join(DATA_DIR, 'approvals.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                approval = {
                    'approval_id': parts[0],
                    'article_id': parts[1],
                    'version_id': parts[2],
                    'approver': parts[3],
                    'status': parts[4],
                    'comments': parts[5],
                    'timestamp': parts[6]
                }
                approvals.append(approval)
    except FileNotFoundError:
        pass
    return approvals
def read_comments():
    comments = []
    try:
        with open(os.path.join(DATA_DIR, 'comments.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 6:
                    continue
                comment = {
                    'comment_id': parts[0],
                    'article_id': parts[1],
                    'version_id': parts[2],
                    'user': parts[3],
                    'comment_text': parts[4],
                    'timestamp': parts[5]
                }
                comments.append(comment)
    except FileNotFoundError:
        pass
    return comments
@dashboard_bp.route('/dashboard')
def dashboard():
    # For demonstration, assume username is stored in session
    username = session.get('username', 'guest')
    users = read_users()
    fullname = users.get(username, {}).get('fullname', username)
    articles = read_articles()
    approvals = read_approvals()
    comments = read_comments()
    # Quick stats calculation
    total_articles = len(articles)
    published_articles = len([a for a in articles if a['status'] == 'published'])
    drafts = len([a for a in articles if a['status'] == 'draft'])
    pending_reviews = len([a for a in articles if a['status'] in ('pending_review', 'under_review')])
    quick_stats = {
        'total_articles': total_articles,
        'published_articles': published_articles,
        'drafts': drafts,
        'pending_reviews': pending_reviews
    }
    # Recent activity feed: combine approvals and comments, sort by timestamp desc, limit 10
    activity = []
    for approval in approvals:
        try:
            ts = datetime.strptime(approval['timestamp'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            ts = datetime.min
        activity.append({
            'type': 'approval',
            'article_id': approval['article_id'],
            'version_id': approval['version_id'],
            'user': approval['approver'],
            'status': approval['status'],
            'comments': approval['comments'],
            'timestamp': ts
        })
    for comment in comments:
        try:
            ts = datetime.strptime(comment['timestamp'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            ts = datetime.min
        activity.append({
            'type': 'comment',
            'article_id': comment['article_id'],
            'version_id': comment['version_id'],
            'user': comment['user'],
            'comment_text': comment['comment_text'],
            'timestamp': ts
        })
    # Sort descending by timestamp
    activity.sort(key=lambda x: x['timestamp'], reverse=True)
    recent_activity = activity[:10]
    return render_template('dashboard.html',
                           username=username,
                           fullname=fullname,
                           quick_stats=quick_stats,
                           recent_activity=recent_activity)