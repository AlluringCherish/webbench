'''
Flask backend implementation for ContentPublishingHub application.
Supports all specified routes and functionalities:
- Dashboard overview with user welcome, quick stats, recent activity
- Article creation, editing with version control
- Article version history viewing and restoring
- User's articles listing with filtering
- Published articles listing with filtering and sorting
- Content calendar for scheduled publications
- Article analytics display
Data is stored and retrieved from plain text files in 'data' directory.
'''
import os
from flask import Flask, render_template, request, redirect, url_for, abort, flash
from datetime import datetime
from collections import defaultdict
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages
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
def parse_users():
    users = {}
    for line in read_file_lines('users.txt'):
        parts = line.split('|')
        if len(parts) == 4:
            username, email, fullname, created_date = parts
            users[username] = {
                'username': username,
                'email': email,
                'fullname': fullname,
                'created_date': created_date
            }
    return users
def parse_articles():
    articles = {}
    for line in read_file_lines('articles.txt'):
        parts = line.split('|')
        if len(parts) == 10:
            (article_id, title, author, category, status, tags,
             featured_image, meta_description, created_date, publish_date) = parts
            articles[article_id] = {
                'article_id': article_id,
                'title': title,
                'author': author,
                'category': category,
                'status': status,
                'tags': tags.split(',') if tags else [],
                'featured_image': featured_image,
                'meta_description': meta_description,
                'created_date': created_date,
                'publish_date': publish_date
            }
    return articles
def write_articles(articles):
    lines = []
    for a in articles.values():
        tags_str = ','.join(a['tags']) if a['tags'] else ''
        line = '|'.join([
            a['article_id'], a['title'], a['author'], a['category'], a['status'],
            tags_str, a['featured_image'], a['meta_description'], a['created_date'], a['publish_date']
        ])
        lines.append(line)
    write_file_lines('articles.txt', lines)
def parse_article_versions():
    versions = defaultdict(list)  # article_id -> list of versions sorted by version_number
    for line in read_file_lines('article_versions.txt'):
        parts = line.split('|', 7)
        if len(parts) == 7:
            version_id, article_id, version_number, content, author, created_date, change_summary = parts
            version = {
                'version_id': version_id,
                'article_id': article_id,
                'version_number': int(version_number),
                'content': content,
                'author': author,
                'created_date': created_date,
                'change_summary': change_summary
            }
            versions[article_id].append(version)
    # Sort versions by version_number ascending
    for article_id in versions:
        versions[article_id].sort(key=lambda v: v['version_number'])
    return versions
def write_article_versions(versions):
    lines = []
    for version_list in versions.values():
        for v in version_list:
            line = '|'.join([
                v['version_id'], v['article_id'], str(v['version_number']),
                v['content'], v['author'], v['created_date'], v['change_summary']
            ])
            lines.append(line)
    write_file_lines('article_versions.txt', lines)
def parse_approvals():
    approvals = []
    for line in read_file_lines('approvals.txt'):
        parts = line.split('|', 7)
        if len(parts) == 7:
            approval_id, article_id, version_id, approver, status, comments, timestamp = parts
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
def parse_workflow_stages():
    stages = []
    for line in read_file_lines('workflow_stages.txt'):
        parts = line.split('|')
        if len(parts) == 5:
            stage_id, category, stage_name, stage_order, is_required = parts
            stages.append({
                'stage_id': stage_id,
                'category': category,
                'stage_name': stage_name,
                'stage_order': int(stage_order),
                'is_required': is_required.lower() == 'yes'
            })
    return stages
def parse_comments():
    comments = []
    for line in read_file_lines('comments.txt'):
        parts = line.split('|', 6)
        if len(parts) == 6:
            comment_id, article_id, version_id, user, comment_text, timestamp = parts
            comments.append({
                'comment_id': comment_id,
                'article_id': article_id,
                'version_id': version_id,
                'user': user,
                'comment_text': comment_text,
                'timestamp': timestamp
            })
    return comments
def parse_analytics():
    analytics = []
    for line in read_file_lines('analytics.txt'):
        parts = line.split('|')
        if len(parts) == 7:
            analytics_id, article_id, date, views, unique_visitors, avg_time_seconds, shares = parts
            analytics.append({
                'analytics_id': analytics_id,
                'article_id': article_id,
                'date': date,
                'views': int(views),
                'unique_visitors': int(unique_visitors),
                'avg_time_seconds': int(avg_time_seconds),
                'shares': int(shares)
            })
    return analytics
def get_next_id(filename):
    lines = read_file_lines(filename)
    max_id = 0
    for line in lines:
        parts = line.split('|')
        if parts and parts[0].isdigit():
            max_id = max(max_id, int(parts[0]))
    return str(max_id + 1)
# For simplicity, assume logged-in user is 'john' for all routes
# In real app, implement authentication and session management
LOGGED_IN_USER = 'john'
@app.route('/')
def index():
    return redirect(url_for('dashboard'))
@app.route('/dashboard')
def dashboard():
    users = parse_users()
    articles = parse_articles()
    versions = parse_article_versions()
    approvals = parse_approvals()
    comments = parse_comments()
    username = LOGGED_IN_USER
    user = users.get(username, {'fullname': username})
    # Quick stats: count articles by status for this user
    user_articles = [a for a in articles.values() if a['author'] == username]
    status_counts = defaultdict(int)
    for a in user_articles:
        status_counts[a['status']] += 1
    # Recent activity feed: last 5 comments and approvals on user's articles
    recent_activities = []
    # Comments on user's articles
    user_article_ids = set(a['article_id'] for a in user_articles)
    user_comments = [c for c in comments if c['article_id'] in user_article_ids]
    user_approvals = [ap for ap in approvals if ap['article_id'] in user_article_ids]
    # Combine and sort by timestamp descending
    combined = []
    for c in user_comments:
        combined.append({
            'type': 'comment',
            'user': c['user'],
            'article_id': c['article_id'],
            'version_id': c['version_id'],
            'text': c['comment_text'],
            'timestamp': c['timestamp']
        })
    for ap in user_approvals:
        combined.append({
            'type': 'approval',
            'user': ap['approver'],
            'article_id': ap['article_id'],
            'version_id': ap['version_id'],
            'text': f"Status: {ap['status']}. Comments: {ap['comments']}",
            'timestamp': ap['timestamp']
        })
    combined.sort(key=lambda x: x['timestamp'], reverse=True)
    recent_activities = combined[:5]
    return render_template('dashboard.html',
                           username=username,
                           fullname=user.get('fullname', username),
                           quick_stats=status_counts,
                           recent_activity=recent_activities)
@app.route('/article/create', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        title = request.form.get('article-title', '').strip()
        content = request.form.get('article-content', '').strip()
        category = request.form.get('article-category', 'blog').strip()
        if category not in ['news', 'blog', 'tutorial', 'announcement', 'press_release']:
            category = 'blog'  # fallback to default
        if not title:
            flash('Article title is required.', 'error')
            return render_template('create_article.html')
        # Create new article_id
        articles = parse_articles()
        article_versions = parse_article_versions()
        new_article_id = str(max([int(aid) for aid in articles.keys()] + [0]) + 1)
        created_date = datetime.now().strftime('%Y-%m-%d')
        # Default values for new article
        new_article = {
            'article_id': new_article_id,
            'title': title,
            'author': LOGGED_IN_USER,
            'category': category,
            'status': 'draft',
            'tags': [],
            'featured_image': '',
            'meta_description': '',
            'created_date': created_date,
            'publish_date': ''
        }
        articles[new_article_id] = new_article
        write_articles(articles)
        # Add initial version
        new_version_id = get_next_id('article_versions.txt')
        version = {
            'version_id': new_version_id,
            'article_id': new_article_id,
            'version_number': 1,
            'content': content,
            'author': LOGGED_IN_USER,
            'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'change_summary': 'Initial draft'
        }
        article_versions[new_article_id].append(version)
        write_article_versions(article_versions)
        flash('Article created and saved as draft.', 'success')
        return redirect(url_for('edit_article', article_id=new_article_id))
    return render_template('create_article.html')
@app.route('/article/<article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    articles = parse_articles()
    article_versions = parse_article_versions()
    article = articles.get(article_id)
    if not article:
        abort(404, description="Article not found")
    # Only author can edit
    if article['author'] != LOGGED_IN_USER:
        abort(403, description="Unauthorized to edit this article")
    if request.method == 'POST':
        title = request.form.get('edit-article-title', '').strip()
        content = request.form.get('edit-article-content', '').strip()
        if not title:
            flash('Article title is required.', 'error')
            return render_template('edit_article.html', article=article, content=content)
        # Update article title
        article['title'] = title
        articles[article_id] = article
        write_articles(articles)
        # Add new version
        versions = article_versions.get(article_id, [])
        new_version_number = max([v['version_number'] for v in versions], default=0) + 1
        new_version_id = get_next_id('article_versions.txt')
        change_summary = f'Version {new_version_number} saved'
        new_version = {
            'version_id': new_version_id,
            'article_id': article_id,
            'version_number': new_version_number,
            'content': content,
            'author': LOGGED_IN_USER,
            'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'change_summary': change_summary
        }
        article_versions[article_id].append(new_version)
        write_article_versions(article_versions)
        flash('New version saved successfully.', 'success')
        return redirect(url_for('edit_article', article_id=article_id))
    # GET request: show latest version content
    versions = article_versions.get(article_id, [])
    if versions:
        latest_version = max(versions, key=lambda v: v['version_number'])
        content = latest_version['content']
    else:
        content = ''
    return render_template('edit_article.html', article=article, content=content)
@app.route('/article/<article_id>/versions', methods=['GET', 'POST'])
def version_history(article_id):
    articles = parse_articles()
    article_versions = parse_article_versions()
    article = articles.get(article_id)
    if not article:
        abort(404, description="Article not found")
    # Only author can view version history
    if article['author'] != LOGGED_IN_USER:
        abort(403, description="Unauthorized to view this article's versions")
    versions = article_versions.get(article_id, [])
    versions_sorted = sorted(versions, key=lambda v: v['version_number'], reverse=True)
    if request.method == 'POST':
        # Restore a version
        restore_version_id = request.form.get('restore_version_id')
        if not restore_version_id:
            flash('No version selected to restore.', 'error')
            return redirect(url_for('version_history', article_id=article_id))
        # Find version to restore
        version_to_restore = None
        for v in versions:
            if v['version_id'] == restore_version_id:
                version_to_restore = v
                break
        if not version_to_restore:
            flash('Selected version not found.', 'error')
            return redirect(url_for('version_history', article_id=article_id))
        # Add a new version identical to the restored one but with new version number and timestamp
        new_version_number = max([v['version_number'] for v in versions], default=0) + 1
        new_version_id = get_next_id('article_versions.txt')
        new_version = {
            'version_id': new_version_id,
            'article_id': article_id,
            'version_number': new_version_number,
            'content': version_to_restore['content'],
            'author': LOGGED_IN_USER,
            'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'change_summary': f'Restored version {version_to_restore["version_number"]}'
        }
        article_versions[article_id].append(new_version)
        write_article_versions(article_versions)
        flash(f'Version {version_to_restore["version_number"]} restored as new version.', 'success')
        return redirect(url_for('edit_article', article_id=article_id))
    # For version comparison, show content of first two versions if available
    version1 = versions_sorted[0] if len(versions_sorted) > 0 else None
    version2 = versions_sorted[1] if len(versions_sorted) > 1 else None
    return render_template('version_history.html',
                           article=article,
                           versions=versions_sorted,
                           version1=version1,
                           version2=version2)
@app.route('/articles/mine')
def my_articles():
    articles = parse_articles()
    username = LOGGED_IN_USER
    # Filter by status if provided
    filter_status = request.args.get('status', '').strip().lower()
    user_articles = [a for a in articles.values() if a['author'] == username]
    if filter_status:
        user_articles = [a for a in user_articles if a['status'].lower() == filter_status]
    # Sort by created_date descending
    user_articles.sort(key=lambda a: a['created_date'], reverse=True)
    return render_template('my_articles.html',
                           articles=user_articles,
                           filter_status=filter_status)
@app.route('/articles/published')
def published_articles():
    articles = parse_articles()
    # Filter by category if provided
    filter_category = request.args.get('category', '').strip().lower()
    sort_by = request.args.get('sort', 'publish_date').strip()
    published_articles = [a for a in articles.values() if a['status'] == 'published']
    if filter_category:
        published_articles = [a for a in published_articles if a['category'].lower() == filter_category]
    # Sorting
    if sort_by == 'title':
        published_articles.sort(key=lambda a: a['title'].lower())
    elif sort_by == 'publish_date':
        # Sort descending by publish_date
        def parse_date(d):
            try:
                return datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
            except Exception:
                return datetime.min
        published_articles.sort(key=lambda a: parse_date(a['publish_date']), reverse=True)
    else:
        # Default fallback
        published_articles.sort(key=lambda a: a['title'].lower())
    return render_template('published_articles.html',
                           articles=published_articles,
                           filter_category=filter_category,
                           sort_by=sort_by)
@app.route('/calendar')
def content_calendar():
    articles = parse_articles()
    # Show scheduled publications (status approved or published) with publish_date
    scheduled_articles = [a for a in articles.values() if a['publish_date'] and a['status'] in ('approved', 'published')]
    # Calendar view selector (e.g. month, week) - for simplicity, just pass param
    calendar_view = request.args.get('view', 'month')
    return render_template('content_calendar.html',
                           articles=scheduled_articles,
                           calendar_view=calendar_view)
@app.route('/article/<article_id>/analytics')
def article_analytics(article_id):
    articles = parse_articles()
    analytics = parse_analytics()
    article = articles.get(article_id)
    if not article:
        abort(404, description="Article not found")
    # Only author can view analytics
    if article['author'] != LOGGED_IN_USER:
        abort(403, description="Unauthorized to view analytics for this article")
    # Aggregate analytics for this article
    article_analytics = [a for a in analytics if a['article_id'] == article_id]
    total_views = sum(a['views'] for a in article_analytics)
    unique_visitors = sum(a['unique_visitors'] for a in article_analytics)
    avg_time_seconds = 0
    shares = sum(a['shares'] for a in article_analytics)
    if article_analytics:
        avg_time_seconds = int(sum(a['avg_time_seconds'] for a in article_analytics) / len(article_analytics))
    return render_template('article_analytics.html',
                           article=article,
                           total_views=total_views,
                           unique_visitors=unique_visitors,
                           avg_time_seconds=avg_time_seconds,
                           shares=shares)
# Run the app on port 5000
if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)