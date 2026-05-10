'''
Main Flask application for ContentPublishingHub.
Provides routes and backend logic for content management system.
'''
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from collections import defaultdict
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For flash messages
DATA_DIR = 'data'
# Utility functions to read and write files
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
# Load users from users.txt
def load_users():
    users = {}
    lines = read_file_lines('users.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) < 4:
            continue
        username, email, fullname, created_date = parts
        users[username] = {
            'username': username,
            'email': email,
            'fullname': fullname,
            'created_date': created_date
        }
    return users
# Load articles from articles.txt
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
def get_next_article_id():
    articles = load_articles()
    if not articles:
        return '1'
    max_id = max(int(aid) for aid in articles.keys())
    return str(max_id + 1)
# Load article versions from article_versions.txt
def load_article_versions():
    versions = defaultdict(list)
    lines = read_file_lines('article_versions.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) < 7:
            continue
        version_id = parts[0]
        article_id = parts[1]
        version_number = int(parts[2])
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
    # Sort versions by version_number ascending
    for vlist in versions.values():
        vlist.sort(key=lambda v: v['version_number'])
    return versions
def save_article_versions(versions):
    lines = []
    for article_id, vers in versions.items():
        for v in vers:
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
def get_next_version_id():
    lines = read_file_lines('article_versions.txt')
    if not lines:
        return '1'
    max_id = 0
    for line in lines:
        parts = line.split('|')
        try:
            vid = int(parts[0])
            if vid > max_id:
                max_id = vid
        except:
            continue
    return str(max_id + 1)
# Load approvals from approvals.txt
def load_approvals():
    approvals = []
    lines = read_file_lines('approvals.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) < 7:
            continue
        approvals.append({
            'approval_id': parts[0],
            'article_id': parts[1],
            'version_id': parts[2],
            'approver': parts[3],
            'status': parts[4],
            'comments': parts[5],
            'timestamp': parts[6]
        })
    return approvals
def save_approvals(approvals):
    lines = []
    for a in approvals:
        line = '|'.join([
            a['approval_id'],
            a['article_id'],
            a['version_id'],
            a['approver'],
            a['status'],
            a['comments'],
            a['timestamp']
        ])
        lines.append(line)
    write_file_lines('approvals.txt', lines)
# Load workflow stages from workflow_stages.txt
def load_workflow_stages():
    stages = []
    lines = read_file_lines('workflow_stages.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) < 5:
            continue
        stages.append({
            'stage_id': parts[0],
            'category': parts[1],
            'stage_name': parts[2],
            'stage_order': int(parts[3]),
            'is_required': parts[4].lower() == 'yes'
        })
    return stages
# Load comments from comments.txt
def load_comments():
    comments = []
    lines = read_file_lines('comments.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) < 6:
            continue
        comments.append({
            'comment_id': parts[0],
            'article_id': parts[1],
            'version_id': parts[2],
            'user': parts[3],
            'comment_text': parts[4],
            'timestamp': parts[5]
        })
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
# Load analytics from analytics.txt
def load_analytics():
    analytics = []
    lines = read_file_lines('analytics.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) < 7:
            continue
        analytics.append({
            'analytics_id': parts[0],
            'article_id': parts[1],
            'date': parts[2],
            'views': int(parts[3]),
            'unique_visitors': int(parts[4]),
            'avg_time_seconds': int(parts[5]),
            'shares': int(parts[6])
        })
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
def get_next_analytics_id():
    lines = read_file_lines('analytics.txt')
    if not lines:
        return '1'
    max_id = 0
    for line in lines:
        parts = line.split('|')
        try:
            aid = int(parts[0])
            if aid > max_id:
                max_id = aid
        except:
            continue
    return str(max_id + 1)
# Format datetime string for display
def format_datetime(dt_str):
    try:
        dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%b %d, %Y %H:%M')
    except:
        return dt_str
# Simulate logged-in user (for testing)
def get_current_user():
    # For testing, default user is 'john'
    return 'john'
# Routes
@app.route('/')
def root():
    # Redirect root to dashboard as per regulation #2
    return redirect(url_for('dashboard'))
@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    users = load_users()
    articles = load_articles()
    comments = load_comments()
    approvals = load_approvals()
    analytics = load_analytics()
    article_versions = load_article_versions()
    # Filter articles by current user
    user_articles = [a for a in articles.values() if a['author'] == user]
    total_articles = len(user_articles)
    published_articles = len([a for a in user_articles if a['status'] == 'published'])
    drafts = len([a for a in user_articles if a['status'] == 'draft'])
    pending_review = len([a for a in user_articles if a['status'] == 'pending_review'])
    quick_stats = {
        'total_articles': total_articles,
        'published_articles': published_articles,
        'drafts': drafts,
        'pending_review': pending_review
    }
    # Prepare recent activity feed (last 5 items)
    recent_activity = []
    # Comments by user on their articles
    user_article_ids = set(a['article_id'] for a in user_articles)
    user_comments = [c for c in comments if c['article_id'] in user_article_ids]
    # Approvals on user's articles
    user_approvals = [a for a in approvals if a['article_id'] in user_article_ids]
    # Analytics on user's articles
    user_analytics = [a for a in analytics if a['article_id'] in user_article_ids]
    # Combine all activities with timestamps
    for c in user_comments:
        article_title = articles[c['article_id']]['title'] if c['article_id'] in articles else 'Unknown'
        recent_activity.append({
            'type': 'comment',
            'article_title': article_title,
            'user': c['user'],
            'timestamp': c['timestamp'],
            'comment_text': c['comment_text']
        })
    for a in user_approvals:
        article_title = articles[a['article_id']]['title'] if a['article_id'] in articles else 'Unknown'
        # Find version number from article_versions
        version_number = None
        versions = article_versions.get(a['article_id'], [])
        for v in versions:
            if v['version_id'] == a['version_id']:
                version_number = v['version_number']
                break
        recent_activity.append({
            'type': 'approval',
            'article_title': article_title,
            'version_number': version_number,
            'approver': a['approver'],
            'timestamp': a['timestamp'],
            'status': a['status'],
            'comments': a['comments']
        })
    for an in user_analytics:
        article_title = articles[an['article_id']]['title'] if an['article_id'] in articles else 'Unknown'
        recent_activity.append({
            'type': 'analytics',
            'article_title': article_title,
            'views': an['views'],
            'date': an['date']
        })
    # Sort combined activities by timestamp descending
    def activity_sort_key(item):
        # For comment and approval, timestamp field exists
        # For analytics, date field exists
        ts = item.get('timestamp') or item.get('date') or ''
        try:
            return datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
        except:
            try:
                return datetime.strptime(ts, '%Y-%m-%d')
            except:
                return datetime.min
    recent_activity.sort(key=activity_sort_key, reverse=True)
    recent_activity = recent_activity[:5]
    return render_template('dashboard.html',
                           username=users[user]['fullname'] if user in users else user,
                           quick_stats=quick_stats,
                           recent_activity=recent_activity,
                           user=user)
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
        new_article_id = get_next_article_id()
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
        new_version_id = get_next_version_id()
        version_number = 1
        created_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        change_summary = 'Initial draft'
        article_versions[new_article_id] = [{
            'version_id': new_version_id,
            'article_id': new_article_id,
            'version_number': version_number,
            'content': content,
            'author': user,
            'created_date': created_date_time,
            'change_summary': change_summary
        }]
        save_article_versions(article_versions)
        flash('Article created and saved as draft.', 'success')
        return redirect(url_for('edit_article', article_id=new_article_id))
    return render_template('create_article.html', create_article_page_id='create-article-page')
@app.route('/article/<article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    user = get_current_user()
    articles = load_articles()
    article_versions = load_article_versions()
    if article_id not in articles:
        flash('Article not found.', 'error')
        return redirect(url_for('dashboard'))
    article = articles[article_id]
    if article['author'] != user:
        flash('You are not authorized to edit this article.', 'error')
        return redirect(url_for('dashboard'))
    versions = article_versions.get(article_id, [])
    if not versions:
        flash('No versions found for this article.', 'error')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        title = request.form.get('edit-article-title', '').strip()
        content = request.form.get('edit-article-content', '').strip()
        if not title:
            flash('Article title is required.', 'error')
            return redirect(url_for('edit_article', article_id=article_id))
        # Update article title if changed
        if title != article['title']:
            article['title'] = title
            articles[article_id] = article
            save_articles(articles)
        # Create new version
        new_version_id = get_next_version_id()
        new_version_number = versions[-1]['version_number'] + 1
        created_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        change_summary = 'Updated content'
        article_versions[article_id].append({
            'version_id': new_version_id,
            'article_id': article_id,
            'version_number': new_version_number,
            'content': content,
            'author': user,
            'created_date': created_date_time,
            'change_summary': change_summary
        })
        save_article_versions(article_versions)
        flash('New version saved successfully.', 'success')
        return redirect(url_for('edit_article', article_id=article_id))
    # Show latest version content for editing
    latest_version = versions[-1]
    return render_template('edit_article.html',
                           edit_article_page_id='edit-article-page',
                           article=article,
                           version=latest_version)
@app.route('/article/<article_id>/versions', methods=['GET', 'POST'])
def version_history(article_id):
    user = get_current_user()
    articles = load_articles()
    article_versions = load_article_versions()
    if article_id not in articles:
        flash('Article not found.', 'error')
        return redirect(url_for('dashboard'))
    article = articles[article_id]
    if article['author'] != user:
        flash('You do not have permission to view this article versions.', 'error')
        return redirect(url_for('dashboard'))
    versions = article_versions.get(article_id, [])
    if not versions:
        flash('No versions found for this article.', 'error')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        restore_version_id = request.form.get('restore_version_id')
        if not restore_version_id:
            flash('No version selected to restore.', 'error')
            return redirect(url_for('version_history', article_id=article_id))
        restore_version = None
        for v in versions:
            if v['version_id'] == restore_version_id:
                restore_version = v
                break
        if not restore_version:
            flash('Selected version not found.', 'error')
            return redirect(url_for('version_history', article_id=article_id))
        # Create new version identical to restored version but with incremented version number
        new_version_id = get_next_version_id()
        new_version_number = versions[-1]['version_number'] + 1
        created_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        change_summary = f"Restored version {restore_version['version_number']}"
        article_versions[article_id].append({
            'version_id': new_version_id,
            'article_id': article_id,
            'version_number': new_version_number,
            'content': restore_version['content'],
            'author': user,
            'created_date': created_date_time,
            'change_summary': change_summary
        })
        save_article_versions(article_versions)
        flash(f"Version {restore_version['version_number']} restored as new version.", 'success')
        return redirect(url_for('version_history', article_id=article_id))
    # Prepare version comparison data (show first and latest versions)
    first_version = versions[0]
    latest_version = versions[-1]
    return render_template('version_history.html',
                           version_history_page_id='version-history-page',
                           article=article,
                           versions=versions,
                           first_version=first_version,
                           latest_version=latest_version)
@app.route('/articles/mine')
def my_articles():
    user = get_current_user()
    articles = load_articles()
    filter_status = request.args.get('filter-article-status', None)
    user_articles = [a for a in articles.values() if a['author'] == user]
    if filter_status:
        user_articles = [a for a in user_articles if a['status'] == filter_status]
    # Sort by created_date descending
    user_articles.sort(key=lambda x: x['created_date'], reverse=True)
    return render_template('my_articles.html',
                           my_articles_page_id='my-articles-page',
                           articles=user_articles,
                           filter_status=filter_status)
@app.route('/articles/published')
def published_articles():
    articles = load_articles()
    filter_category = request.args.get('filter-published-category', None)
    sort_by = request.args.get('sort-published', 'publish_date')
    published_articles = [a for a in articles.values() if a['status'] == 'published']
    if filter_category:
        published_articles = [a for a in published_articles if a['category'] == filter_category]
    if sort_by == 'publish_date':
        published_articles.sort(key=lambda x: x['publish_date'] or '', reverse=True)
    elif sort_by == 'title':
        published_articles.sort(key=lambda x: x['title'])
    return render_template('published_articles.html',
                           published_articles_page_id='published-articles-page',
                           articles=published_articles,
                           filter_category=filter_category,
                           sort_by=sort_by)
@app.route('/calendar')
def content_calendar():
    articles = load_articles()
    # Only approved or published articles for calendar
    scheduled_articles = [a for a in articles.values() if a['status'] in ('approved', 'published')]
    calendar_view = request.args.get('calendar-view', 'month')
    return render_template('content_calendar.html',
                           calendar_page_id='calendar-page',
                           articles=scheduled_articles,
                           calendar_view=calendar_view)
@app.route('/article/<article_id>/analytics')
def article_analytics(article_id):
    user = get_current_user()
    articles = load_articles()
    analytics = load_analytics()
    if article_id not in articles:
        flash('Article not found.', 'error')
        return redirect(url_for('dashboard'))
    article = articles[article_id]
    # Filter analytics for this article
    article_analytics = [a for a in analytics if a['article_id'] == article_id]
    total_views = sum(a['views'] for a in article_analytics)
    unique_visitors = sum(a['unique_visitors'] for a in article_analytics)
    avg_time_seconds = 0
    shares = sum(a['shares'] for a in article_analytics)
    if article_analytics:
        avg_time_seconds = int(sum(a['avg_time_seconds'] for a in article_analytics) / len(article_analytics))
    analytics_overview = {
        'total_views': total_views,
        'unique_visitors': unique_visitors,
        'avg_time_seconds': avg_time_seconds,
        'shares': shares
    }
    return render_template('article_analytics.html',
                           analytics_page_id='analytics-page',
                           article=article,
                           analytics_overview=analytics_overview)
if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)