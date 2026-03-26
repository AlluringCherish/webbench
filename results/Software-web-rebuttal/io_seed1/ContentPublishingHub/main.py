'''
Flask backend for ContentPublishingHub application.
Defines routes for all specified pages and loads data from text files in 'data' directory.
Provides context data to templates for rendering.
'''
from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
def read_users():
    users = []
    path = os.path.join(DATA_DIR, 'users.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    username, email, fullname, created_date = line.split('|')
                    users.append({
                        'username': username,
                        'email': email,
                        'fullname': fullname,
                        'created_date': created_date
                    })
    return users
def read_articles():
    articles = []
    path = os.path.join(DATA_DIR, 'articles.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    # Ensure all fields present (10 fields)
                    while len(parts) < 10:
                        parts.append('')
                    article_id, title, author, category, status, tags, featured_image, meta_description, created_date, publish_date = parts
                    articles.append({
                        'article_id': article_id,
                        'title': title,
                        'author': author,
                        'category': category,
                        'status': status,
                        'tags': tags,
                        'featured_image': featured_image,
                        'meta_description': meta_description,
                        'created_date': created_date,
                        'publish_date': publish_date
                    })
    return articles
def write_articles(articles):
    path = os.path.join(DATA_DIR, 'articles.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for a in articles:
            line = '|'.join([
                a.get('article_id', ''),
                a.get('title', ''),
                a.get('author', ''),
                a.get('category', ''),
                a.get('status', ''),
                a.get('tags', ''),
                a.get('featured_image', ''),
                a.get('meta_description', ''),
                a.get('created_date', ''),
                a.get('publish_date', '')
            ])
            f.write(line + '\n')
def read_article_versions():
    versions = []
    path = os.path.join(DATA_DIR, 'article_versions.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    version_id, article_id, version_number, content, author, created_date, change_summary = line.split('|', 6)
                    versions.append({
                        'version_id': version_id,
                        'article_id': article_id,
                        'version_number': int(version_number),
                        'content': content,
                        'author': author,
                        'created_date': created_date,
                        'change_summary': change_summary
                    })
    return versions
def write_article_versions(versions):
    path = os.path.join(DATA_DIR, 'article_versions.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for v in versions:
            line = '|'.join([
                v.get('version_id', ''),
                v.get('article_id', ''),
                str(v.get('version_number', '')),
                v.get('content', ''),
                v.get('author', ''),
                v.get('created_date', ''),
                v.get('change_summary', '')
            ])
            f.write(line + '\n')
def read_approvals():
    approvals = []
    path = os.path.join(DATA_DIR, 'approvals.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    approval_id, article_id, version_id, approver, status, comments, timestamp = line.split('|', 6)
                    approvals.append({
                        'approval_id': approval_id,
                        'article_id': article_id,
                        'version_id': version_id,
                        'user': approver,
                        'status': status,
                        'comments': comments,
                        'timestamp': timestamp
                    })
    return approvals
def read_comments():
    comments = []
    path = os.path.join(DATA_DIR, 'comments.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    comment_id, article_id, version_id, user, comment_text, timestamp = line.split('|', 5)
                    comments.append({
                        'comment_id': comment_id,
                        'article_id': article_id,
                        'version_id': version_id,
                        'user': user,
                        'text': comment_text,
                        'timestamp': timestamp,
                        'type': 'comment'
                    })
    return comments
def read_analytics():
    analytics = []
    path = os.path.join(DATA_DIR, 'analytics.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    analytics_id, article_id, date, views, unique_visitors, avg_time_seconds, shares = line.split('|')
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
def get_next_article_id():
    articles = read_articles()
    if not articles:
        return '1'
    max_id = max(int(a['article_id']) for a in articles if a['article_id'].isdigit())
    return str(max_id + 1)
def get_next_version_id():
    versions = read_article_versions()
    if not versions:
        return '1'
    max_id = max(int(v['version_id']) for v in versions if v['version_id'].isdigit())
    return str(max_id + 1)
def get_next_comment_id():
    comments = read_comments()
    if not comments:
        return '1'
    max_id = max(int(c['comment_id']) for c in comments if c['comment_id'].isdigit())
    return str(max_id + 1)
@app.route('/')
def index():
    # Redirect to dashboard as first page accessible via '/'
    return redirect(url_for('dashboard'))
@app.route('/dashboard')
def dashboard():
    # For demonstration, assume logged in user is 'john'
    username = 'john'
    articles = read_articles()
    analytics = read_analytics()
    # Calculate quick stats
    total_articles = len([a for a in articles if a['author'] == username])
    published_articles = len([a for a in articles if a['author'] == username and a['status'] == 'published'])
    draft_articles = len([a for a in articles if a['author'] == username and a['status'] == 'draft'])
    total_views = sum(a['views'] for a in analytics if any(art['article_id'] == a['article_id'] and art['author'] == username for art in articles))
    quick_stats = {
        'total_articles': total_articles,
        'published_articles': published_articles,
        'draft_articles': draft_articles,
        'total_views': total_views
    }
    # Recent activity: combine comments and approvals, sorted by timestamp descending, limit 10
    comments = read_comments()
    approvals = read_approvals()
    # Normalize approvals to have 'type' key for template
    for a in approvals:
        a['type'] = 'approval'
    combined_activity = comments + approvals
    # Sort by timestamp descending
    def parse_ts(item):
        try:
            return datetime.strptime(item['timestamp'], '%Y-%m-%d %H:%M:%S')
        except Exception:
            return datetime.min
    combined_activity.sort(key=parse_ts, reverse=True)
    recent_activity = combined_activity[:10]
    return render_template('dashboard.html', username=username, quick_stats=quick_stats, recent_activity=recent_activity)
@app.route('/article/create', methods=['GET', 'POST'])
def create_article():
    # For demonstration, assume logged in user is 'john'
    username = 'john'
    if request.method == 'POST':
        title = request.form.get('article-title', '').strip()
        content = request.form.get('article-content', '').strip()
        if not title:
            # Could add flash message or error handling here
            return render_template('create_article.html', error="Title is required.")
        # Create new article with draft status
        articles = read_articles()
        article_id = get_next_article_id()
        created_date = datetime.now().strftime('%Y-%m-%d')
        new_article = {
            'article_id': article_id,
            'title': title,
            'author': username,
            'category': '',  # category not provided in form, can be extended
            'status': 'draft',
            'tags': '',
            'featured_image': '',
            'meta_description': '',
            'created_date': created_date,
            'publish_date': ''
        }
        articles.append(new_article)
        write_articles(articles)
        # Create initial version for the article
        versions = read_article_versions()
        version_id = get_next_version_id()
        created_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_version = {
            'version_id': version_id,
            'article_id': article_id,
            'version_number': 1,
            'content': content,
            'author': username,
            'created_date': created_date_time,
            'change_summary': 'Initial draft'
        }
        versions.append(new_version)
        write_article_versions(versions)
        return redirect(url_for('dashboard'))
    return render_template('create_article.html')
@app.route('/article/<article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    # For demonstration, assume logged in user is 'john'
    username = 'john'
    articles = read_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404
    if request.method == 'POST':
        title = request.form.get('edit-article-title', '').strip()
        content = request.form.get('edit-article-content', '').strip()
        change_summary = request.form.get('change-summary', '').strip()
        if not title:
            return render_template('edit_article.html', article=article, error="Title is required.")
        # Update article title
        article['title'] = title
        # Save new version
        versions = read_article_versions()
        # Find max version number for this article
        article_versions = [v for v in versions if v['article_id'] == article_id]
        max_version_number = max([v['version_number'] for v in article_versions], default=0)
        new_version_number = max_version_number + 1
        version_id = get_next_version_id()
        created_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if not change_summary:
            change_summary = f'Version {new_version_number} update'
        new_version = {
            'version_id': version_id,
            'article_id': article_id,
            'version_number': new_version_number,
            'content': content,
            'author': username,
            'created_date': created_date_time,
            'change_summary': change_summary
        }
        versions.append(new_version)
        write_article_versions(versions)
        # Update article title in articles.txt
        write_articles(articles)
        return redirect(url_for('dashboard'))
    # GET request: load latest version content for editing
    versions = read_article_versions()
    article_versions = [v for v in versions if v['article_id'] == article_id]
    if not article_versions:
        content = ''
    else:
        # Get latest version by version_number
        latest_version = max(article_versions, key=lambda v: v['version_number'])
        content = latest_version['content']
    article_data = {
        'article_id': article['article_id'],
        'title': article['title'],
        'content': content
    }
    return render_template('edit_article.html', article=article_data)
@app.route('/article/<article_id>/versions')
def version_history(article_id):
    versions = read_article_versions()
    article_versions = [v for v in versions if v['article_id'] == article_id]
    if not article_versions:
        return "No versions found for this article", 404
    # Sort versions by version_number ascending
    article_versions.sort(key=lambda v: v['version_number'])
    return render_template('version_history.html', article_id=article_id, versions=article_versions)
@app.route('/article/<article_id>/versions/restore/<version_id>', methods=['POST'])
def restore_version(article_id, version_id):
    # Restore a previous version as the latest version
    versions = read_article_versions()
    target_version = next((v for v in versions if v['version_id'] == version_id and v['article_id'] == article_id), None)
    if not target_version:
        return "Version not found", 404
    # For demonstration, assume logged in user is 'john'
    username = 'john'
    # Find max version number for this article
    article_versions = [v for v in versions if v['article_id'] == article_id]
    max_version_number = max([v['version_number'] for v in article_versions], default=0)
    new_version_number = max_version_number + 1
    new_version_id = get_next_version_id()
    created_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Create new version with content from target version
    new_version = {
        'version_id': new_version_id,
        'article_id': article_id,
        'version_number': new_version_number,
        'content': target_version['content'],
        'author': username,
        'created_date': created_date_time,
        'change_summary': f'Restored version {target_version["version_number"]}'
    }
    versions.append(new_version)
    write_article_versions(versions)
    return redirect(url_for('version_history', article_id=article_id))
@app.route('/articles/mine')
def my_articles():
    # For demonstration, assume logged in user is 'john'
    username = 'john'
    articles = read_articles()
    user_articles = [a for a in articles if a['author'] == username]
    # Optional: filter by status if query param provided
    status_filter = request.args.get('status', '').strip()
    if status_filter:
        user_articles = [a for a in user_articles if a['status'] == status_filter]
    return render_template('my_articles.html', articles=user_articles)
@app.route('/articles/published')
def published_articles():
    articles = read_articles()
    published = [a for a in articles if a['status'] == 'published']
    # Optional: filter by category
    category_filter = request.args.get('category', '').strip()
    if category_filter:
        published = [a for a in published if a['category'] == category_filter]
    # Optional: sort by field
    sort_by = request.args.get('sort', '').strip()
    if sort_by == 'date':
        published.sort(key=lambda a: a['publish_date'] or '', reverse=True)
    elif sort_by == 'title':
        published.sort(key=lambda a: a['title'].lower())
    return render_template('published_articles.html', articles=published)
@app.route('/calendar')
def content_calendar():
    # For simplicity, no calendar data loaded
    return render_template('content_calendar.html')
@app.route('/article/<article_id>/analytics')
def article_analytics(article_id):
    analytics = read_analytics()
    article_analytics = [a for a in analytics if a['article_id'] == article_id]
    if not article_analytics:
        return "No analytics data found for this article", 404
    # Aggregate totals
    total_views = sum(a['views'] for a in article_analytics)
    unique_visitors = sum(a['unique_visitors'] for a in article_analytics)
    return render_template('article_analytics.html',
                           article_id=article_id,
                           analytics_overview=article_analytics,
                           total_views=total_views,
                           unique_visitors=unique_visitors)
if __name__ == '__main__':
    app.run(debug=True)