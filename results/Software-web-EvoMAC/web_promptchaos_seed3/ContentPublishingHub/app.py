'''
Main Flask application for ContentPublishingHub.
Implements backend routes, data file operations, version control,
content scheduling, analytics, and collaborative content creation.
'''
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from collections import defaultdict
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For flash messages
DATA_DIR = 'data'
# Utility functions for file operations and parsing
def read_file_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines
def write_file_lines(filename, lines):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')
# Users
def load_users():
    users = {}
    lines = read_file_lines('users.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) < 4:
            continue
        username, email, fullname, created_date = parts[:4]
        users[username] = {
            'username': username,
            'email': email,
            'fullname': fullname,
            'created_date': created_date
        }
    return users
# Articles
def load_articles():
    articles = {}
    lines = read_file_lines('articles.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) < 10:
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
        publish_date = a.get('publish_date', '')
        line = '|'.join([
            str(a['article_id']),
            a['title'],
            a['author'],
            a['category'],
            a['status'],
            tags_str,
            a['featured_image'] if a['featured_image'] else '',
            a['meta_description'],
            a['created_date'],
            publish_date
        ])
        lines.append(line)
    write_file_lines('articles.txt', lines)
# Article Versions
def load_article_versions():
    versions = defaultdict(list)
    lines = read_file_lines('article_versions.txt')
    for line in lines:
        parts = line.split('|', 6)
        if len(parts) < 7:
            continue
        version_id = parts[0]
        article_id = parts[1]
        try:
            version_number = int(parts[2])
        except ValueError:
            continue
        content = parts[3]
        author = parts[4]
        created_date = parts[5]
        change_summary = parts[6]
        versions[article_id].append({
            'version_id': version_id,
            'article_id': article_id,
            'version_number': version_number,
            'content': content,
            'author': author,
            'created_date': created_date,
            'change_summary': change_summary
        })
    # Sort versions by version_number ascending for each article
    for article_id in versions:
        versions[article_id].sort(key=lambda v: v['version_number'])
    return versions
def save_article_versions(versions):
    lines = []
    for article_id, vers in versions.items():
        for v in vers:
            line = '|'.join([
                str(v['version_id']),
                v['article_id'],
                str(v['version_number']),
                v['content'],
                v['author'],
                v['created_date'],
                v['change_summary']
            ])
            lines.append(line)
    write_file_lines('article_versions.txt', lines)
# Approvals
def load_approvals():
    approvals = []
    lines = read_file_lines('approvals.txt')
    for line in lines:
        parts = line.split('|', 6)
        if len(parts) < 7:
            continue
        approval_id = parts[0]
        article_id = parts[1]
        version_id = parts[2]
        approver = parts[3]
        status = parts[4]
        comments = parts[5]
        timestamp = parts[6]
        approvals.append({
            'approval_id': approval_id,
            'article_id': article_id,
            'version_id': version_id,
            'approver': approver,
            'status': status,
            'comments': comments,
            'timestamp': timestamp
        })
    return approvals
def save_approvals(approvals):
    lines = []
    for a in approvals:
        line = '|'.join([
            str(a['approval_id']),
            a['article_id'],
            a['version_id'],
            a['approver'],
            a['status'],
            a['comments'],
            a['timestamp']
        ])
        lines.append(line)
    write_file_lines('approvals.txt', lines)
# Workflow Stages
def load_workflow_stages():
    stages = []
    lines = read_file_lines('workflow_stages.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) < 5:
            continue
        stage_id = parts[0]
        category = parts[1]
        stage_name = parts[2]
        try:
            stage_order = int(parts[3])
        except ValueError:
            continue
        is_required = parts[4].lower() == 'yes'
        stages.append({
            'stage_id': stage_id,
            'category': category,
            'stage_name': stage_name,
            'stage_order': stage_order,
            'is_required': is_required
        })
    return stages
# Comments
def load_comments():
    comments = []
    lines = read_file_lines('comments.txt')
    for line in lines:
        parts = line.split('|', 5)
        if len(parts) < 6:
            continue
        comment_id = parts[0]
        article_id = parts[1]
        version_id = parts[2]
        user = parts[3]
        comment_text = parts[4]
        timestamp = parts[5]
        comments.append({
            'comment_id': comment_id,
            'article_id': article_id,
            'version_id': version_id,
            'user': user,
            'comment_text': comment_text,
            'timestamp': timestamp
        })
    return comments
def save_comments(comments):
    lines = []
    for c in comments:
        line = '|'.join([
            str(c['comment_id']),
            c['article_id'],
            c['version_id'],
            c['user'],
            c['comment_text'],
            c['timestamp']
        ])
        lines.append(line)
    write_file_lines('comments.txt', lines)
# Analytics
def load_analytics():
    analytics = []
    lines = read_file_lines('analytics.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) < 7:
            continue
        analytics_id = parts[0]
        article_id = parts[1]
        date = parts[2]
        try:
            views = int(parts[3])
            unique_visitors = int(parts[4])
            avg_time_seconds = int(parts[5])
            shares = int(parts[6])
        except ValueError:
            continue
        analytics.append({
            'analytics_id': analytics_id,
            'article_id': article_id,
            'date': date,
            'views': views,
            'unique_visitors': unique_visitors,
            'avg_time_seconds': avg_time_seconds,
            'shares': shares
        })
    return analytics
def save_analytics(analytics):
    lines = []
    for a in analytics:
        line = '|'.join([
            str(a['analytics_id']),
            a['article_id'],
            a['date'],
            str(a['views']),
            str(a['unique_visitors']),
            str(a['avg_time_seconds']),
            str(a['shares'])
        ])
        lines.append(line)
    write_file_lines('analytics.txt', lines)
# Helpers
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
def get_next_approval_id(approvals):
    max_id = 0
    for a in approvals:
        try:
            val = int(a['approval_id'])
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
def get_next_version_id(all_versions):
    max_id = 0
    for v in all_versions:
        try:
            val = int(v['version_id'])
            if val > max_id:
                max_id = val
        except Exception:
            continue
    return str(max_id + 1)
# For simplicity, simulate a logged-in user (in real app use sessions/auth)
def get_current_user():
    # For testing/demo, return 'john'
    return 'john'
# Routes
@app.route('/')
def index():
    # Redirect to dashboard as first page
    return redirect(url_for('dashboard'))
@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    users = load_users()
    articles = load_articles()
    article_versions = load_article_versions()
    approvals = load_approvals()
    comments = load_comments()
    analytics = load_analytics()
    # Welcome message
    fullname = users.get(user, {}).get('fullname', user)
    # Quick stats: count articles by status for current user
    user_articles = [a for a in articles.values() if a['author'] == user]
    status_counts = defaultdict(int)
    for a in user_articles:
        status_counts[a['status']] += 1
    # Recent activity feed: last 5 article versions by user or comments by user
    recent_activities = []
    # Article versions by user
    user_versions = []
    for vers_list in article_versions.values():
        for v in vers_list:
            if v['author'] == user:
                user_versions.append(v)
    user_versions.sort(key=lambda v: v['created_date'], reverse=True)
    # Comments by user
    user_comments = [c for c in comments if c['user'] == user]
    user_comments.sort(key=lambda c: c['timestamp'], reverse=True)
    # Merge and sort by date descending
    # We'll create a unified list with type and date
    activities = []
    for v in user_versions:
        activities.append({
            'type': 'version',
            'date': v['created_date'],
            'summary': f"Edited article ID {v['article_id']} (v{v['version_number']}): {v['change_summary']}"
        })
    for c in user_comments:
        activities.append({
            'type': 'comment',
            'date': c['timestamp'],
            'summary': f"Commented on article ID {c['article_id']} version {c['version_id']}: {c['comment_text']}"
        })
    activities.sort(key=lambda x: x['date'], reverse=True)
    recent_activities = activities[:5]
    return render_template('dashboard.html',
                           username=fullname,
                           quick_stats=status_counts,
                           recent_activity=recent_activities)
@app.route('/article/create', methods=['GET', 'POST'])
def create_article():
    user = get_current_user()
    if request.method == 'POST':
        title = request.form.get('article-title', '').strip()
        content = request.form.get('article-content', '').strip()
        if not title:
            flash('Article title is required.', 'error')
            return render_template('create_article.html')
        # Load articles and versions
        articles = load_articles()
        article_versions = load_article_versions()
        # Generate new article_id
        new_article_id = str(get_next_id(articles.values(), 'article_id'))
        created_date = datetime.now().strftime('%Y-%m-%d')
        # Default category, status, tags, featured_image, meta_description empty for now
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
        change_summary = 'Initial draft'
        version_entry = {
            'version_id': new_version_id,
            'article_id': new_article_id,
            'version_number': version_number,
            'content': content,
            'author': user,
            'created_date': created_date_time,
            'change_summary': change_summary
        }
        article_versions[new_article_id].append(version_entry)
        save_article_versions(article_versions)
        flash('Article created and saved as draft.', 'success')
        return redirect(url_for('edit_article', article_id=new_article_id))
    return render_template('create_article.html')
@app.route('/article/<article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    user = get_current_user()
    articles = load_articles()
    article_versions = load_article_versions()
    article = articles.get(article_id)
    if not article:
        flash('Article not found.', 'error')
        return redirect(url_for('dashboard'))
    # Load latest version content for editing
    versions = article_versions.get(article_id, [])
    if not versions:
        flash('No versions found for this article.', 'error')
        return redirect(url_for('dashboard'))
    latest_version = max(versions, key=lambda v: v['version_number'])
    if request.method == 'POST':
        title = request.form.get('edit-article-title', '').strip()
        content = request.form.get('edit-article-content', '').strip()
        if not title:
            flash('Article title is required.', 'error')
            return render_template('edit_article.html', article=article, content=latest_version['content'])
        # Update article title
        article['title'] = title
        articles[article_id] = article
        save_articles(articles)
        # Save new version only if content changed or title changed (optional)
        # For simplicity, always save new version on POST
        new_version_number = latest_version['version_number'] + 1
        all_versions_flat = [v for vers in article_versions.values() for v in vers]
        new_version_id = str(get_next_version_id(all_versions_flat))
        created_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        change_summary = f'Version {new_version_number} saved'
        new_version = {
            'version_id': new_version_id,
            'article_id': article_id,
            'version_number': new_version_number,
            'content': content,
            'author': user,
            'created_date': created_date_time,
            'change_summary': change_summary
        }
        article_versions[article_id].append(new_version)
        save_article_versions(article_versions)
        flash('New version saved successfully.', 'success')
        return redirect(url_for('edit_article', article_id=article_id))
    return render_template('edit_article.html', article=article, content=latest_version['content'])
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
    if not versions:
        flash('No versions found for this article.', 'error')
        return redirect(url_for('edit_article', article_id=article_id))
    # Sort versions ascending by version_number
    versions = sorted(versions, key=lambda v: v['version_number'])
    # Handle restore version POST
    if request.method == 'POST':
        restore_version_id = request.form.get('restore_version_id')
        if not restore_version_id:
            flash('No version selected to restore.', 'error')
            return redirect(url_for('version_history', article_id=article_id))
        # Find version to restore
        restore_version = None
        for v in versions:
            if v['version_id'] == restore_version_id:
                restore_version = v
                break
        if not restore_version:
            flash('Selected version not found.', 'error')
            return redirect(url_for('version_history', article_id=article_id))
        # Prevent restoring if content identical to latest version (optional)
        latest_version = versions[-1]
        if restore_version['content'] == latest_version['content']:
            flash('Selected version content is identical to the latest version. No new version created.', 'info')
            return redirect(url_for('edit_article', article_id=article_id))
        # Restore means create a new version identical to the selected version content
        new_version_number = versions[-1]['version_number'] + 1
        all_versions_flat = [v for vers in article_versions.values() for v in vers]
        new_version_id = str(get_next_version_id(all_versions_flat))
        created_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        change_summary = f'Restored version {restore_version["version_number"]}'
        new_version = {
            'version_id': new_version_id,
            'article_id': article_id,
            'version_number': new_version_number,
            'content': restore_version['content'],
            'author': user,
            'created_date': created_date_time,
            'change_summary': change_summary
        }
        article_versions[article_id].append(new_version)
        save_article_versions(article_versions)
        flash(f'Version {restore_version["version_number"]} restored as new version.', 'success')
        return redirect(url_for('edit_article', article_id=article_id))
    # For version comparison, if query params specify two versions, show diff
    # For simplicity, just show content side by side
    v1_id = request.args.get('v1')
    v2_id = request.args.get('v2')
    version1 = None
    version2 = None
    if v1_id and v2_id:
        for v in versions:
            if v['version_id'] == v1_id:
                version1 = v
            if v['version_id'] == v2_id:
                version2 = v
    return render_template('version_history.html',
                           article=article,
                           versions=versions,
                           version1=version1,
                           version2=version2)
@app.route('/articles/mine', methods=['GET', 'POST'])
def my_articles():
    user = get_current_user()
    articles = load_articles()
    # Filter by status
    filter_status = request.args.get('filter-article-status', '').strip().lower()
    user_articles = [a for a in articles.values() if a['author'] == user]
    if filter_status:
        user_articles = [a for a in user_articles if a['status'].lower() == filter_status]
    return render_template('my_articles.html',
                           articles=user_articles,
                           filter_status=filter_status)
@app.route('/articles/published')
def published_articles():
    articles = load_articles()
    # Filter by category and sort
    filter_category = request.args.get('filter-published-category', '').strip().lower()
    sort_by = request.args.get('sort-published', '').strip().lower()
    published_articles = [a for a in articles.values() if a['status'] == 'published']
    if filter_category:
        published_articles = [a for a in published_articles if a['category'].lower() == filter_category]
    if sort_by == 'date':
        published_articles.sort(key=lambda a: a['publish_date'] or '', reverse=True)
    elif sort_by == 'title':
        published_articles.sort(key=lambda a: a['title'].lower())
    return render_template('published_articles.html',
                           articles=published_articles,
                           filter_category=filter_category,
                           sort_by=sort_by)
@app.route('/calendar')
def content_calendar():
    articles = load_articles()
    # Show scheduled publications timeline
    # For simplicity, pass articles with publish_date set
    scheduled_articles = [a for a in articles.values() if a['publish_date']]
    # Calendar view selector (e.g. month, week) - default month
    calendar_view = request.args.get('calendar-view', 'month')
    return render_template('content_calendar.html',
                           articles=scheduled_articles,
                           calendar_view=calendar_view)
@app.route('/article/<article_id>/analytics')
def article_analytics(article_id):
    articles = load_articles()
    analytics = load_analytics()
    article = articles.get(article_id)
    if not article:
        flash('Article not found.', 'error')
        return redirect(url_for('dashboard'))
    # Filter analytics for this article
    article_analytics = [a for a in analytics if a['article_id'] == article_id]
    # Aggregate overview
    total_views = sum(a['views'] for a in article_analytics)
    unique_visitors = sum(a['unique_visitors'] for a in article_analytics)
    avg_time_seconds = 0
    shares = sum(a['shares'] for a in article_analytics)
    if article_analytics:
        avg_time_seconds = int(sum(a['avg_time_seconds'] for a in article_analytics) / len(article_analytics))
    return render_template('article_analytics.html',
                           article=article,
                           analytics=article_analytics,
                           total_views=total_views,
                           unique_visitors=unique_visitors,
                           avg_time_seconds=avg_time_seconds,
                           shares=shares)
# Run the app
if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)