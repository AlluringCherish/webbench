"""
ContentPublishingHub Web Application
Management system for content scheduling, analytics, editorial history, comments, and content testing.
This module implements the Flask backend with routes and logic for the ContentPublishingHub system.
Note on URLs and routing:
To avoid hardcoded URLs in frontend JavaScript and templates, all URLs are generated using Flask's `url_for()` function.
These URLs are passed to templates and injected into JavaScript variables to ensure consistency and compliance with routing under any subpath.
Data files are stored locally in DATA_DIR with formats as specified in the documentation.
"""
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key in production
DATA_DIR = 'data'
# --- File operation helpers ---
def read_file_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]
def write_file_lines(filename, lines):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
# --- Loaders and savers for data ---
def load_users():
    users = {}
    lines = read_file_lines('users.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) < 3:
            continue
        username = parts[0]
        email = parts[1]
        fullname = parts[2]
        created_date = parts[3] if len(parts) > 3 else ''
        users[username] = {
            'username': username,
            'email': email,
            'fullname': fullname,
            'created_date': created_date
        }
    return users
def load_articles():
    articles = {}
    lines = read_file_lines('articles.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) < 9:
            continue
        article_id = parts[0]
        articles[article_id] = {
            'article_id': article_id,
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
    return articles
def save_articles(articles):
    lines = []
    for a in articles.values():
        tags_str = ','.join(a['tags']) if a['tags'] else ''
        line = '|'.join([
            a['article_id'],
            a['title'],
            a['author'],
            a['category'],
            a['status'],
            tags_str,
            a['featured_image'],
            a['meta_description'],
            a['created_date'],
            a['publish_date']
        ])
        lines.append(line)
    write_file_lines('articles.txt', lines)
def load_article_versions():
    versions = {}
    lines = read_file_lines('article_versions.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) < 7:
            continue
        article_id = parts[1]
        try:
            version_number = int(parts[2])
        except ValueError:
            continue
        version = {
            'version_id': parts[0],
            'article_id': article_id,
            'version_number': version_number,
            'content': parts[3],
            'author': parts[4],
            'created_date': parts[5],
            'change_summary': parts[6]
        }
        versions.setdefault(article_id, []).append(version)
    # Sort versions by version_number ascending
    for vlist in versions.values():
        vlist.sort(key=lambda v: v['version_number'])
    return versions
def save_article_versions(versions):
    lines = []
    for vers_list in versions.values():
        for v in vers_list:
            line = '|'.join([
                v['version_id'],
                v['article_id'],
                str(v['version_number']),
                v['content'],
                v['author'],
                v['created_date'],
                v['change_summary']
            ])
            lines.append(line)
    write_file_lines('article_versions.txt', lines)
def load_approvals():
    approvals = []
    lines = read_file_lines('approvals.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) < 6:
            continue
        approval = {
            'stage_id': parts[0],
            'category': parts[1],
            'stage_name': parts[2],
            'stage_order': parts[3],
            'is_required': parts[4],
            'timestamp': parts[5]
        }
        approvals.append(approval)
    return approvals
def load_workflow_stages():
    stages = []
    lines = read_file_lines('workflow_stages.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) < 4:
            continue
        stage = {
            'stage_id': parts[0],
            'category': parts[1],
            'stage_name': parts[2],
            'stage_order': int(parts[3]),
            'is_required': parts[4] if len(parts) > 4 else 'no'
        }
        stages.append(stage)
    return stages
def load_comments():
    comments = []
    lines = read_file_lines('comments.txt')
    for line in lines:
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
    return comments
def save_comments(comments):
    lines = []
    for c in comments:
        line = '|'.join([
            c['comment_id'],
            c['article_id'],
            c['version_id'],
            c['user'],
            c['comment_text'],
            c['timestamp']
        ])
        lines.append(line)
    write_file_lines('comments.txt', lines)
def load_analytics():
    analytics = []
    lines = read_file_lines('analytics.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) < 7:
            continue
        analytic = {
            'analytics_id': parts[0],
            'article_id': parts[1],
            'date': parts[2],
            'views': int(parts[3]),
            'unique_visitors': int(parts[4]),
            'avg_time_seconds': int(parts[5]),
            'shares': int(parts[6])
        }
        analytics.append(analytic)
    return analytics
def save_analytics(analytics):
    lines = []
    for a in analytics:
        line = '|'.join([
            a['analytics_id'],
            a['article_id'],
            a['date'],
            str(a['views']),
            str(a['unique_visitors']),
            str(a['avg_time_seconds']),
            str(a['shares'])
        ])
        lines.append(line)
    write_file_lines('analytics.txt', lines)
# --- Helper functions ---
def get_next_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            val = int(item[id_key])
            if val > max_id:
                max_id = val
        except Exception:
            continue
    return max_id + 1
def get_next_version_number(versions, article_id):
    if article_id not in versions:
        return 1
    return max(v['version_number'] for v in versions[article_id]) + 1
def get_next_version_id(all_versions):
    max_id = 0
    for v in all_versions:
        try:
            val = int(v['version_id'])
            if val > max_id:
                max_id = val
        except Exception:
            continue
    return max_id + 1
def get_next_comment_id(comments):
    max_id = 0
    for c in comments:
        try:
            val = int(c['comment_id'])
            if val > max_id:
                max_id = val
        except Exception:
            continue
    return max_id + 1
def get_next_analytics_id(analytics):
    max_id = 0
    for a in analytics:
        try:
            val = int(a['analytics_id'])
            if val > max_id:
                max_id = val
        except Exception:
            continue
    return max_id + 1
# --- Simulated user session/auth ---
def get_current_user():
    # For demo/testing, return a fixed user
    return 'alice'
def get_current_user_fullname():
    users = load_users()
    user = get_current_user()
    return users.get(user, {}).get('fullname', user)
# --- Routes ---
@app.route('/')
def root():
    return redirect(url_for('dashboard'))
@app.route('/dashboard')
def dashboard():
    users = load_users()
    articles = load_articles()
    article_versions = load_article_versions()
    approvals = load_approvals()
    analytics = load_analytics()
    comments = load_comments()
    user = get_current_user()
    fullname = get_current_user_fullname()
    # Count articles by status for quick stats
    status_counts = {}
    for a in articles.values():
        status_counts[a['status']] = status_counts.get(a['status'], 0) + 1
    # Recent activities: combine versions and comments by current user, sorted by date desc
    recent_activities = []
    for vers_list in article_versions.values():
        for v in vers_list:
            if v['author'] == user:
                recent_activities.append({
                    'type': 'version',
                    'date': v['created_date'],
                    'summary': f"Version {v['version_number']} saved for article ID {v['article_id']}: {v['change_summary']}"
                })
    for c in comments:
        if c['user'] == user:
            recent_activities.append({
                'type': 'comment',
                'date': c['timestamp'],
                'summary': f"Commented on article ID {c['article_id']} version {c['version_id']}: {c['comment_text']}"
            })
    recent_activities.sort(key=lambda x: x['date'], reverse=True)
    # Pass URLs for frontend JS to avoid hardcoded URLs
    urls = {
        'create_article': url_for('create_article'),
        'dashboard': url_for('dashboard'),
        'my_articles': url_for('my_articles'),
        'published_articles': url_for('published_articles'),
        'content_calendar': url_for('content_calendar'),
    }
    return render_template('dashboard.html',
                           username=fullname,
                           quick_stats=status_counts,
                           recent_activity=recent_activities,
                           urls=urls)
@app.route('/article/create', methods=['GET', 'POST'])
def create_article():
    user = get_current_user()
    if request.method == 'POST':
        title = request.form.get('article-title', '').strip()
        content = request.form.get('article-content', '').strip()
        if not title:
            flash('Article title is required.', 'error')
            return redirect(url_for('create_article'))
        articles = load_articles()
        article_versions = load_article_versions()
        # Generate new article_id as next integer string
        new_article_id = str(get_next_id(articles.values(), 'article_id'))
        created_date = datetime.now().strftime('%Y-%m-%d')
        new_article = {
            'article_id': new_article_id,
            'title': title,
            'author': user,
            'category': 'blog',  # default category
            'status': 'draft',
            'tags': [],
            'featured_image': '',
            'meta_description': '',
            'created_date': created_date,
            'publish_date': ''
        }
        articles[new_article_id] = new_article
        save_articles(articles)
        # Create initial version
        all_versions_flat = [v for vers in article_versions.values() for v in vers]
        new_version_id = str(get_next_version_id(all_versions_flat))
        version_number = 1
        created_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_version = {
            'version_id': new_version_id,
            'article_id': new_article_id,
            'version_number': version_number,
            'content': content,
            'author': user,
            'created_date': created_date_time,
            'change_summary': 'Initial draft'
        }
        article_versions.setdefault(new_article_id, []).append(new_version)
        save_article_versions(article_versions)
        flash('Article created and initial version saved successfully.', 'success')
        return redirect(url_for('edit_article', article_id=new_article_id))
    # GET request
    urls = {
        'dashboard': url_for('dashboard'),
    }
    return render_template('create_article.html', urls=urls)
@app.route('/article/<article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    user = get_current_user()
    articles = load_articles()
    article_versions = load_article_versions()
    article = articles.get(article_id)
    if not article:
        flash('Article not found.', 'error')
        return redirect(url_for('dashboard'))
    versions = article_versions.get(article_id, [])
    versions.sort(key=lambda v: v['version_number'])
    if request.method == 'POST':
        title = request.form.get('edit-article-title', '').strip()
        content = request.form.get('edit-article-content', '').strip()
        change_summary = request.form.get('change-summary', '').strip() or 'Updated content'
        if not title:
            flash('Article title cannot be empty.', 'error')
            return redirect(url_for('edit_article', article_id=article_id))
        # Update article title
        article['title'] = title
        articles[article_id] = article
        save_articles(articles)
        # Save new version if content changed
        latest_version = versions[-1] if versions else None
        if not latest_version or latest_version['content'] != content:
            all_versions_flat = [v for vers in article_versions.values() for v in vers]
            new_version_id = str(get_next_version_id(all_versions_flat))
            new_version_number = (latest_version['version_number'] + 1) if latest_version else 1
            created_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_version = {
                'version_id': new_version_id,
                'article_id': article_id,
                'version_number': new_version_number,
                'content': content,
                'author': user,
                'created_date': created_date_time,
                'change_summary': change_summary
            }
            article_versions.setdefault(article_id, []).append(new_version)
            save_article_versions(article_versions)
            flash(f'Version {new_version_number} saved successfully.', 'success')
        else:
            flash('No changes detected in content.', 'info')
        return redirect(url_for('edit_article', article_id=article_id))
    # GET request
    latest_version = versions[-1] if versions else None
    content = latest_version['content'] if latest_version else ''
    urls = {
        'dashboard': url_for('dashboard'),
        'version_history': url_for('version_history', article_id=article_id),
    }
    return render_template('edit_article.html',
                           article=article,
                           content=content,
                           urls=urls)
@app.route('/article/<article_id>/versions', methods=['GET', 'POST'])
def version_history(article_id):
    user = get_current_user()
    articles = load_articles()
    article_versions = load_article_versions()
    article = articles.get(article_id)
    if not article:
        flash('Article not found.', 'error')
        return redirect(url_for('dashboard'))
    versions = article_versions.get(article_id, [])
    versions.sort(key=lambda v: v['version_number'])
    if request.method == 'POST':
        restore_version_id = request.form.get('restore_version_id')
        if not restore_version_id:
            flash('No version selected to restore.', 'error')
            return redirect(url_for('version_history', article_id=article_id))
        restore_version = next((v for v in versions if v['version_id'] == restore_version_id), None)
        if not restore_version:
            flash('Selected version not found.', 'error')
            return redirect(url_for('version_history', article_id=article_id))
        # Create new version identical to restored content
        all_versions_flat = [v for vers in article_versions.values() for v in vers]
        new_version_id = str(get_next_version_id(all_versions_flat))
        new_version_number = versions[-1]['version_number'] + 1 if versions else 1
        created_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_version = {
            'version_id': new_version_id,
            'article_id': article_id,
            'version_number': new_version_number,
            'content': restore_version['content'],
            'author': user,
            'created_date': created_date_time,
            'change_summary': f"Restored version {restore_version['version_number']}"
        }
        article_versions.setdefault(article_id, []).append(new_version)
        save_article_versions(article_versions)
        flash(f"Restored version {restore_version['version_number']} as new version {new_version_number}.", 'success')
        return redirect(url_for('edit_article', article_id=article_id))
    urls = {
        'edit_article': url_for('edit_article', article_id=article_id),
        'dashboard': url_for('dashboard'),
    }
    return render_template('version_history.html',
                           article=article,
                           versions=versions,
                           urls=urls)
@app.route('/articles/mine')
def my_articles():
    user = get_current_user()
    articles = load_articles()
    filter_status = request.args.get('filter-article-status', '').strip().lower()
    user_articles = [a for a in articles.values() if a['author'] == user]
    if filter_status:
        user_articles = [a for a in user_articles if a['status'].lower() == filter_status]
    urls = {
        'create_article': url_for('create_article'),
        'dashboard': url_for('dashboard'),
    }
    return render_template('my_articles.html',
                           articles=user_articles,
                           filter_status=filter_status,
                           urls=urls)
@app.route('/articles/published')
def published_articles():
    articles = load_articles()
    filter_category = request.args.get('filter-published-category', '').strip().lower()
    sort_order = request.args.get('sort-published', '').strip().lower()
    published_articles = [a for a in articles.values() if a['status'] == 'published']
    if filter_category:
        published_articles = [a for a in published_articles if a['category'].lower() == filter_category]
    if sort_order == 'date_asc':
        published_articles.sort(key=lambda a: a['publish_date'] or '')
    elif sort_order == 'date_desc':
        published_articles.sort(key=lambda a: a['publish_date'] or '', reverse=True)
    urls = {
        'dashboard': url_for('dashboard'),
    }
    return render_template('published_articles.html',
                           articles=published_articles,
                           filter_category=filter_category,
                           sort_order=sort_order,
                           urls=urls)
@app.route('/content_calendar')
def content_calendar():
    articles = load_articles()
    calendar_view = request.args.get('calendar-view', 'month')
    # Filter articles with publish_date for calendar display
    scheduled_articles = [a for a in articles.values() if a['publish_date']]
    urls = {
        'dashboard': url_for('dashboard'),
    }
    return render_template('content_calendar.html',
                           articles=scheduled_articles,
                           calendar_view=calendar_view,
                           urls=urls)
@app.route('/article/<article_id>/analytics')
def article_analytics(article_id):
    articles = load_articles()
    analytics = load_analytics()
    article = articles.get(article_id)
    if not article:
        flash('Article not found.', 'error')
        return redirect(url_for('dashboard'))
    article_analytics = [a for a in analytics if a['article_id'] == article_id]
    total_views = sum(a['views'] for a in article_analytics)
    unique_visitors = sum(a['unique_visitors'] for a in article_analytics)
    avg_time_seconds = int(sum(a['avg_time_seconds'] for a in article_analytics) / len(article_analytics)) if article_analytics else 0
    shares = sum(a['shares'] for a in article_analytics)
    urls = {
        'edit_article': url_for('edit_article', article_id=article_id),
        'dashboard': url_for('dashboard'),
    }
    return render_template('article_analytics.html',
                           article=article,
                           total_views=total_views,
                           unique_visitors=unique_visitors,
                           avg_time_seconds=avg_time_seconds,
                           shares=shares,
                           urls=urls)
# --- Run app ---
if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(port=5000, debug=True)