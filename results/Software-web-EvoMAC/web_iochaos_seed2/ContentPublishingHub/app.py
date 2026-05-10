'''
ContentPublishingHub Web Application
Implements content management with version control,
content scheduling, analytics, and collaborative content creation.
'''
import os
from collections import defaultdict
from datetime import datetime
from flask import Flask, request, redirect, url_for, flash, render_template
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flash messages
DATA_DIR = 'data'
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
        f.write('\n'.join(lines) + '\n')
# Users
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
# Articles
def load_articles():
    articles = {}
    lines = read_file_lines('articles.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) < 9:
            continue
        article_id = parts[0]
        article = {
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
        articles[article_id] = article
    return articles
def save_articles(articles):
    lines = []
    for a in articles.values():
        tags_str = ','.join(a['tags']) if a['tags'] else ''
        publish_date = a.get('publish_date', '')
        line = '|'.join([
            a['article_id'], a['title'], a['author'], a['category'], a['status'],
            tags_str, a['featured_image'], a['meta_description'], a['created_date'], publish_date
        ])
        lines.append(line)
    write_file_lines('articles.txt', lines)
def get_next_article_id():
    articles = load_articles()
    if not articles:
        return '1'
    max_id = max(int(aid) for aid in articles.keys())
    return str(max_id + 1)
# Article Versions
def load_article_versions():
    versions = defaultdict(list)
    lines = read_file_lines('article_versions.txt')
    for line in lines:
        parts = line.split('|', 6)
        if len(parts) < 7:
            continue
        version_id, article_id, version_number, content, author, created_date, change_summary = parts
        versions[article_id].append({
            'version_id': version_id,
            'article_id': article_id,
            'version_number': int(version_number),
            'content': content,
            'author': author,
            'created_date': created_date,
            'change_summary': change_summary
        })
    # Sort versions by version_number ascending
    for article_id in versions:
        versions[article_id].sort(key=lambda v: v['version_number'])
    return versions
def save_article_versions(article_versions):
    lines = []
    for article_id, vers in article_versions.items():
        for v in vers:
            line = '|'.join([
                v['version_id'], v['article_id'], str(v['version_number']), v['content'],
                v['author'], v['created_date'], v['change_summary']
            ])
            lines.append(line)
    write_file_lines('article_versions.txt', lines)
def get_next_version_id():
    lines = read_file_lines('article_versions.txt')
    max_id = 0
    for line in lines:
        parts = line.split('|', 1)
        if not parts:
            continue
        try:
            vid = int(parts[0])
            if vid > max_id:
                max_id = vid
        except:
            continue
    return str(max_id + 1)
# Approvals
def load_approvals():
    approvals = []
    lines = read_file_lines('approvals.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) < 7:
            continue
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
# Workflow Stages
def load_workflow_stages():
    stages = defaultdict(list)
    lines = read_file_lines('workflow_stages.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) < 5:
            continue
        stage_id, category, stage_name, stage_order, is_required = parts
        stages[category].append({
            'stage_id': stage_id,
            'category': category,
            'stage_name': stage_name,
            'stage_order': int(stage_order),
            'is_required': is_required.lower() == 'yes'
        })
    # Sort stages by stage_order
    for category in stages:
        stages[category].sort(key=lambda s: s['stage_order'])
    return stages
# Comments
def load_comments():
    comments = defaultdict(list)
    lines = read_file_lines('comments.txt')
    for line in lines:
        parts = line.split('|', 5)
        if len(parts) < 6:
            continue
        comment_id, article_id, version_id, user, comment_text, timestamp = parts
        comments[article_id].append({
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
    for article_id, comment_list in comments.items():
        for c in comment_list:
            line = '|'.join([
                c['comment_id'], c['article_id'], c['version_id'], c['user'], c['comment_text'], c['timestamp']
            ])
            lines.append(line)
    write_file_lines('comments.txt', lines)
def get_next_comment_id():
    lines = read_file_lines('comments.txt')
    max_id = 0
    for line in lines:
        parts = line.split('|', 1)
        if not parts:
            continue
        try:
            cid = int(parts[0])
            if cid > max_id:
                max_id = cid
        except:
            continue
    return str(max_id + 1)
# Analytics
def load_analytics():
    analytics = defaultdict(list)
    lines = read_file_lines('analytics.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) < 7:
            continue
        analytics_id, article_id, date, views, unique_visitors, avg_time_seconds, shares = parts
        analytics[article_id].append({
            'analytics_id': analytics_id,
            'article_id': article_id,
            'date': date,
            'views': int(views),
            'unique_visitors': int(unique_visitors),
            'avg_time_seconds': int(avg_time_seconds),
            'shares': int(shares)
        })
    return analytics
def save_analytics(analytics):
    lines = []
    for article_id, analytics_list in analytics.items():
        for a in analytics_list:
            line = '|'.join([
                a['analytics_id'], a['article_id'], a['date'], str(a['views']),
                str(a['unique_visitors']), str(a['avg_time_seconds']), str(a['shares'])
            ])
            lines.append(line)
    write_file_lines('analytics.txt', lines)
def get_next_analytics_id():
    lines = read_file_lines('analytics.txt')
    max_id = 0
    for line in lines:
        parts = line.split('|', 1)
        if not parts:
            continue
        try:
            aid = int(parts[0])
            if aid > max_id:
                max_id = aid
        except:
            continue
    return str(max_id + 1)
# Helper: Get current user (demo fixed user)
def get_current_user():
    # For demo purposes, return a fixed user
    return 'john'
def get_current_user_fullname():
    users = load_users()
    user = get_current_user()
    if user in users:
        return users[user]['fullname']
    return user
def now_str():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# ROUTES
@app.route('/')
def index():
    return redirect(url_for('dashboard'))
@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    users = load_users()
    fullname = users.get(user, {}).get('fullname', user)
    articles = load_articles()
    article_versions = load_article_versions()
    comments = load_comments()
    # Quick stats
    total_articles = len(articles)
    published_articles = sum(1 for a in articles.values() if a['status'] == 'published')
    drafts = sum(1 for a in articles.values() if a['status'] == 'draft')
    pending_review = sum(1 for a in articles.values() if a['status'] == 'pending_review')
    quick_stats = {
        'total_articles': total_articles,
        'published_articles': published_articles,
        'drafts': drafts,
        'pending_review': pending_review
    }
    # Recent activity feed: combine recent versions and comments by user
    user_versions = []
    for vers_list in article_versions.values():
        for v in vers_list:
            if v['author'] == user:
                user_versions.append(v)
    user_comments = []
    for comment_list in comments.values():
        for c in comment_list:
            if c['user'] == user:
                user_comments.append(c)
    combined = []
    for v in user_versions:
        combined.append((v['created_date'], {
            'type': 'version',
            'version_number': v['version_number'],
            'article_id': v['article_id'],
            'change_summary': v['change_summary'],
            'created_date': v['created_date']
        }))
    for c in user_comments:
        combined.append((c['timestamp'], {
            'type': 'comment',
            'article_id': c['article_id'],
            'comment_text': c['comment_text'],
            'timestamp': c['timestamp']
        }))
    combined.sort(key=lambda x: x[0], reverse=True)
    recent_activities = [item[1] for item in combined[:5]]
    return render_template('dashboard.html',
                           fullname=fullname,
                           quick_stats=quick_stats,
                           recent_activities=recent_activities)
@app.route('/article/create', methods=['GET', 'POST'])
def create_article():
    user = get_current_user()
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if not title:
            flash('Title is required.', 'error')
            return render_template('create_article.html', title=title, content=content)
        article_id = get_next_article_id()
        created_date = now_str()
        article = {
            'article_id': article_id,
            'title': title,
            'author': user,
            'category': 'blog',  # default category, can be extended
            'status': 'draft',
            'tags': [],
            'featured_image': '',
            'meta_description': '',
            'created_date': created_date,
            'publish_date': ''
        }
        articles = load_articles()
        articles[article_id] = article
        save_articles(articles)
        # Create initial version
        article_versions = load_article_versions()
        version_id = get_next_version_id()
        version_number = 1
        created_date_time = now_str()
        change_summary = 'Initial draft'
        version = {
            'version_id': version_id,
            'article_id': article_id,
            'version_number': version_number,
            'content': content,
            'author': user,
            'created_date': created_date_time,
            'change_summary': change_summary
        }
        if article_id not in article_versions:
            article_versions[article_id] = []
        article_versions[article_id].append(version)
        save_article_versions(article_versions)
        flash('Article created successfully as draft.', 'success')
        return redirect(url_for('dashboard'))
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
    if article['author'] != user:
        flash('You do not have permission to edit this article.', 'error')
        return redirect(url_for('dashboard'))
    versions = article_versions.get(article_id, [])
    if not versions:
        flash('No versions found for this article.', 'error')
        return redirect(url_for('dashboard'))
    latest_version = versions[-1]
    if request.method == 'POST':
        title = request.form.get('edit-article-title', '').strip()
        content = request.form.get('edit-article-content', '').strip()
        change_summary = request.form.get('change_summary', '').strip()
        if not title:
            flash('Title is required.', 'error')
            return render_template('edit_article.html', article=article, content=latest_version['content'])
        if not content:
            flash('Content is required.', 'error')
            return render_template('edit_article.html', article=article, content=latest_version['content'])
        # Save new version
        version_id = get_next_version_id()
        version_number = latest_version['version_number'] + 1
        created_date_time = now_str()
        if not change_summary:
            change_summary = 'Updated content'
        new_version = {
            'version_id': version_id,
            'article_id': article_id,
            'version_number': version_number,
            'content': content,
            'author': user,
            'created_date': created_date_time,
            'change_summary': change_summary
        }
        article_versions[article_id].append(new_version)
        save_article_versions(article_versions)
        # Update article title if changed
        if title != article['title']:
            article['title'] = title
            articles[article_id] = article
            save_articles(articles)
        flash('Version saved successfully.', 'success')
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
    if article['author'] != user:
        flash('You do not have permission to view this article versions.', 'error')
        return redirect(url_for('dashboard'))
    versions = article_versions.get(article_id, [])
    if not versions:
        flash('No versions found for this article.', 'error')
        return redirect(url_for('dashboard'))
    version_comparison = None
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
        # Create new version as restoration
        version_id = get_next_version_id()
        version_number = versions[-1]['version_number'] + 1
        created_date_time = now_str()
        change_summary = f'Restored version {restore_version["version_number"]}'
        new_version = {
            'version_id': version_id,
            'article_id': article_id,
            'version_number': version_number,
            'content': restore_version['content'],
            'author': user,
            'created_date': created_date_time,
            'change_summary': change_summary
        }
        article_versions[article_id].append(new_version)
        save_article_versions(article_versions)
        flash(f'Version {restore_version["version_number"]} restored as new version.', 'success')
        return redirect(url_for('edit_article', article_id=article_id))
    # GET request: show versions and optionally compare
    selected_version_id = request.args.get('selected_version_id')
    latest_version = versions[-1]
    selected_version = None
    if selected_version_id:
        for v in versions:
            if v['version_id'] == selected_version_id:
                selected_version = v
                break
    if selected_version:
        version_comparison = {
            'latest': latest_version,
            'selected': selected_version
        }
    return render_template('version_history.html',
                           article=article,
                           versions=versions,
                           version_comparison=version_comparison)
@app.route('/articles/mine')
def my_articles():
    user = get_current_user()
    articles = load_articles()
    filter_status = request.args.get('status', '').lower()
    filtered_articles = []
    for a in articles.values():
        if a['author'] != user:
            continue
        if filter_status and a['status'].lower() != filter_status:
            continue
        filtered_articles.append(a)
    # Sort by created_date descending
    filtered_articles.sort(key=lambda x: x['created_date'], reverse=True)
    return render_template('my_articles.html',
                           articles=filtered_articles,
                           filter_status=filter_status)
@app.route('/articles/published')
def published_articles():
    articles = load_articles()
    filter_category = request.args.get('category', '').lower()
    sort_by = request.args.get('sort', 'publish_date')
    filtered_articles = []
    for a in articles.values():
        if a['status'] != 'published':
            continue
        if filter_category and a['category'].lower() != filter_category:
            continue
        filtered_articles.append(a)
    if sort_by == 'publish_date':
        filtered_articles.sort(key=lambda x: x['publish_date'] or '', reverse=True)
    elif sort_by == 'title':
        filtered_articles.sort(key=lambda x: x['title'])
    return render_template('published_articles.html',
                           articles=filtered_articles,
                           filter_category=filter_category,
                           sort_by=sort_by)
@app.route('/calendar', methods=['GET', 'POST'])
def content_calendar():
    user = get_current_user()
    articles = load_articles()
    calendar_view = request.args.get('view', 'month')
    if request.method == 'POST':
        article_id = request.form.get('article_id')
        publish_date = request.form.get('publish_date')
        if not article_id or not publish_date:
            flash('Article and publish date are required.', 'error')
            return redirect(url_for('content_calendar'))
        if article_id not in articles:
            flash('Article not found.', 'error')
            return redirect(url_for('content_calendar'))
        article = articles[article_id]
        if article['author'] != user:
            flash('You do not have permission to schedule this article.', 'error')
            return redirect(url_for('content_calendar'))
        article['publish_date'] = publish_date
        if article['status'] in ['draft', 'pending_review']:
            article['status'] = 'approved'
        articles[article_id] = article
        save_articles(articles)
        flash(f'Article "{article["title"]}" scheduled for publication on {publish_date}.', 'success')
        return redirect(url_for('content_calendar'))
    # GET: show calendar page
    return render_template('content_calendar.html', calendar_view=calendar_view, articles=articles)
@app.route('/article/<article_id>/analytics')
def article_analytics(article_id):
    user = get_current_user()
    articles = load_articles()
    analytics = load_analytics()
    article = articles.get(article_id)
    if not article:
        flash('Article not found.', 'error')
        return redirect(url_for('dashboard'))
    if article['author'] != user:
        flash('You do not have permission to view analytics for this article.', 'error')
        return redirect(url_for('dashboard'))
    article_analytics = analytics.get(article_id, [])
    total_views = sum(a['views'] for a in article_analytics)
    unique_visitors = sum(a['unique_visitors'] for a in article_analytics)
    shares = sum(a['shares'] for a in article_analytics)
    avg_time_seconds = 0
    if article_analytics:
        avg_time_seconds = int(sum(a['avg_time_seconds'] for a in article_analytics) / len(article_analytics))
    analytics_overview = {
        'total_views': total_views,
        'unique_visitors': unique_visitors,
        'avg_time_seconds': avg_time_seconds,
        'shares': shares
    }
    return render_template('article_analytics.html',
                           article=article,
                           analytics_overview=analytics_overview)
if __name__ == '__main__':
    app.run(port=5000, debug=True)