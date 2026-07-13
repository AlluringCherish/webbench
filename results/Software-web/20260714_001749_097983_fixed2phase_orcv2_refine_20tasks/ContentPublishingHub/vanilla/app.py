from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Data files
USERS_FILE = 'users.txt'
ARTICLES_FILE = 'articles.txt'
VERSIONS_FILE = 'article_versions.txt'
APPROVALS_FILE = 'approvals.txt'
WORKFLOW_FILE = 'workflow_stages.txt'
COMMENTS_FILE = 'comments.txt'
ANALYTICS_FILE = 'analytics.txt'

# Helper functions for reading and writing data

def read_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                username, email, fullname, created_date = line.split('|')
                users[username] = {
                    'username': username,
                    'email': email,
                    'fullname': fullname,
                    'created_date': created_date
                }
    return users

def read_articles():
    articles = {}
    if os.path.exists(ARTICLES_FILE):
        with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                # article_id|title|author|category|status|tags|featured_image|meta_description|created_date|publish_date
                if len(parts) < 10:
                    continue
                article_id = int(parts[0])
                articles[article_id] = {
                    'article_id': article_id,
                    'title': parts[1],
                    'author': parts[2],
                    'category': parts[3],
                    'status': parts[4],
                    'tags': parts[5],
                    'featured_image': parts[6],
                    'meta_description': parts[7],
                    'created_date': parts[8],
                    'publish_date': parts[9]
                }
    return articles

def write_articles(articles):
    lines = []
    for a in articles.values():
        line = '|'.join([
            str(a['article_id']), a['title'], a['author'], a['category'], a['status'],
            a['tags'], a['featured_image'], a['meta_description'], a['created_date'], a['publish_date']
        ])
        lines.append(line)
    with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# Versions

def read_versions(article_id=None):
    versions = []
    if os.path.exists(VERSIONS_FILE):
        with open(VERSIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                v_article_id = int(parts[1])
                if article_id is not None and v_article_id != article_id:
                    continue
                version = {
                    'version_id': int(parts[0]),
                    'article_id': v_article_id,
                    'version_number': int(parts[2]),
                    'content': parts[3],
                    'author': parts[4],
                    'created_date': parts[5],
                    'change_summary': parts[6]
                }
                versions.append(version)
    return versions

def write_versions(versions):
    lines = []
    for v in versions:
        line = '|'.join([
            str(v['version_id']), str(v['article_id']), str(v['version_number']), v['content'],
            v['author'], v['created_date'], v['change_summary']
        ])
        lines.append(line)
    with open(VERSIONS_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# Approvals

def read_approvals(article_id=None):
    approvals = []
    if os.path.exists(APPROVALS_FILE):
        with open(APPROVALS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                a_article_id = int(parts[1])
                if article_id is not None and a_article_id != article_id:
                    continue
                approval = {
                    'approval_id': int(parts[0]),
                    'article_id': a_article_id,
                    'version_id': int(parts[2]),
                    'approver': parts[3],
                    'status': parts[4],
                    'comments': parts[5],
                    'timestamp': parts[6]
                }
                approvals.append(approval)
    return approvals

# Workflow stages

def read_workflow():
    workflow = []
    if os.path.exists(WORKFLOW_FILE):
        with open(WORKFLOW_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 5:
                    continue
                stage = {
                    'stage_id': int(parts[0]),
                    'category': parts[1],
                    'stage_name': parts[2],
                    'stage_order': int(parts[3]),
                    'is_required': parts[4]
                }
                workflow.append(stage)
    return workflow

# Comments

def read_comments(article_id=None):
    comments = []
    if os.path.exists(COMMENTS_FILE):
        with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 6:
                    continue
                c_article_id = int(parts[1])
                if article_id is not None and c_article_id != article_id:
                    continue
                comment = {
                    'comment_id': int(parts[0]),
                    'article_id': c_article_id,
                    'version_id': int(parts[2]),
                    'user': parts[3],
                    'comment_text': parts[4],
                    'timestamp': parts[5]
                }
                comments.append(comment)
    return comments

# Analytics

def read_analytics(article_id=None):
    analytics = []
    if os.path.exists(ANALYTICS_FILE):
        with open(ANALYTICS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                a_article_id = int(parts[1])
                if article_id is not None and a_article_id != article_id:
                    continue
                data = {
                    'analytics_id': int(parts[0]),
                    'article_id': a_article_id,
                    'date': parts[2],
                    'views': int(parts[3]),
                    'unique_visitors': int(parts[4]),
                    'avg_time_seconds': int(parts[5]),
                    'shares': int(parts[6])
                }
                analytics.append(data)
    return analytics

# Utilities

def get_next_id(items, key):
    if not items:
        return 1
    return max(item[key] for item in items) + 1

# For simplicity we simulate a logged in user
LOGGED_IN_USER = 'john'

@app.route('/dashboard')
def dashboard():
    users = read_users()
    articles = read_articles()
    approvals = read_approvals()

    user = users.get(LOGGED_IN_USER, {'fullname': LOGGED_IN_USER})

    # Quick stats example
    user_articles = [a for a in articles.values() if a['author'] == LOGGED_IN_USER]
    total_articles = len(user_articles)
    approved_articles = len([a for a in user_articles if a['status'] == 'approved'])

    recent_approvals = [ap for ap in approvals if ap['approver'] == LOGGED_IN_USER]
    recent_approvals = sorted(recent_approvals, key=lambda x: x['timestamp'], reverse=True)[:5]

    recent_activity = []
    # Just sample recent activity from user's articles and approvals
    for a in sorted(user_articles, key=lambda x: x['created_date'], reverse=True)[:5]:
        recent_activity.append(f"Article '{a['title']}' status changed to {a['status']}")
    for ap in recent_approvals:
        recent_activity.append(f"You {ap['status']} version {ap['version_id']} of article ID {ap['article_id']} on {ap['timestamp']}")

    return render_template('dashboard.html',
                           user=user,
                           total_articles=total_articles,
                           approved_articles=approved_articles,
                           recent_approvals=recent_approvals,
                           recent_activity=recent_activity)

@app.route('/article/create', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        title = request.form.get('article-title', '').strip()
        content = request.form.get('article-content', '').strip()
        if not title:
            flash('Article title is required.', 'error')
            return redirect(url_for('create_article'))

        articles = read_articles()
        next_id = get_next_id(articles.values(), 'article_id')
        created_date = datetime.now().strftime('%Y-%m-%d')
        new_article = {
            'article_id': next_id,
            'title': title,
            'author': LOGGED_IN_USER,
            'category': 'blog',  # default for new
            'status': 'draft',
            'tags': '',
            'featured_image': '',
            'meta_description': '',
            'created_date': created_date,
            'publish_date': ''
        }
        articles[next_id] = new_article
        write_articles(articles)

        # Create first version
        versions = read_versions()
        next_version_id = get_next_id(versions, 'version_id')
        version = {
            'version_id': next_version_id,
            'article_id': next_id,
            'version_number': 1,
            'content': content,
            'author': LOGGED_IN_USER,
            'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'change_summary': 'Initial draft'
        }
        versions.append(version)
        write_versions(versions)

        flash('Article draft created.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('create_article.html')

@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    articles = read_articles()
    article = articles.get(article_id)
    if not article or article['author'] != LOGGED_IN_USER:
        flash('Article not found or access denied.', 'error')
        return redirect(url_for('dashboard'))

    versions = read_versions(article_id)
    latest_version = max(versions, key=lambda v: v['version_number']) if versions else None

    if request.method == 'POST':
        title = request.form.get('edit-article-title', '').strip()
        content = request.form.get('edit-article-content', '').strip()
        if not title:
            flash('Article title is required.', 'error')
            return redirect(url_for('edit_article', article_id=article_id))

        # Update article title
        article['title'] = title
        articles[article_id] = article
        write_articles(articles)

        # Save new version
        next_version_id = get_next_id(versions, 'version_id')
        next_version_number = (latest_version['version_number'] + 1) if latest_version else 1
        version = {
            'version_id': next_version_id,
            'article_id': article_id,
            'version_number': next_version_number,
            'content': content,
            'author': LOGGED_IN_USER,
            'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'change_summary': 'Updated content'
        }
        versions.append(version)
        write_versions(versions)

        flash('New version saved.', 'success')
        return redirect(url_for('edit_article', article_id=article_id))

    # Load latest content if GET
    content = latest_version['content'] if latest_version else ''

    return render_template('edit_article.html', article=article, content=content)

@app.route('/article/<int:article_id>/versions')
def version_history(article_id):
    articles = read_articles()
    article = articles.get(article_id)
    if not article or article['author'] != LOGGED_IN_USER:
        flash('Article not found or access denied.', 'error')
        return redirect(url_for('dashboard'))

    versions = read_versions(article_id)
    versions = sorted(versions, key=lambda v: v['version_number'], reverse=True)

    # Just display versions list, no complex diff view for simplicity
    return render_template('version_history.html', article=article, versions=versions)

@app.route('/article/<int:article_id>/versions/restore/<int:version_number>', methods=['POST'])
def restore_version(article_id, version_number):
    articles = read_articles()
    article = articles.get(article_id)
    if not article or article['author'] != LOGGED_IN_USER:
        flash('Article not found or access denied.', 'error')
        return redirect(url_for('dashboard'))

    versions = read_versions(article_id)
    target_version = None
    for v in versions:
        if v['version_number'] == version_number:
            target_version = v
            break
    if not target_version:
        flash('Version not found.', 'error')
        return redirect(url_for('version_history', article_id=article_id))

    # Save restored version as new version
    next_version_id = get_next_id(versions, 'version_id')
    max_version_number = max(v['version_number'] for v in versions) if versions else 0
    new_version_number = max_version_number + 1
    new_version = {
        'version_id': next_version_id,
        'article_id': article_id,
        'version_number': new_version_number,
        'content': target_version['content'],
        'author': LOGGED_IN_USER,
        'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'change_summary': f'Restored to version {version_number}'
    }
    versions.append(new_version)
    write_versions(versions)

    flash(f'Version {version_number} restored as new version.', 'success')
    return redirect(url_for('version_history', article_id=article_id))

@app.route('/articles/mine')
def my_articles():
    articles = read_articles()
    filter_status = request.args.get('filter-status', None)
    user_articles = [a for a in articles.values() if a['author'] == LOGGED_IN_USER]
    if filter_status:
        user_articles = [a for a in user_articles if a['status'] == filter_status]
    return render_template('my_articles.html', articles=user_articles, filter_status=filter_status)

@app.route('/articles/published')
def published_articles():
    articles = read_articles()
    filter_category = request.args.get('filter-category', None)
    sort_by = request.args.get('sort-by', None)
    published = [a for a in articles.values() if a['status'] == 'published']
    if filter_category:
        published = [a for a in published if a['category'] == filter_category]
    if sort_by == 'date':
        published = sorted(published, key=lambda x: x['publish_date'], reverse=True)
    elif sort_by == 'title':
        published = sorted(published, key=lambda x: x['title'].lower())
    return render_template('published_articles.html', articles=published, filter_category=filter_category, sort_by=sort_by)

@app.route('/calendar')
def content_calendar():
    articles = read_articles()
    # We show only articles with publish_date set
    scheduled = [a for a in articles.values() if a['publish_date']]
    return render_template('content_calendar.html', scheduled_articles=scheduled)

@app.route('/article/<int:article_id>/analytics')
def article_analytics(article_id):
    articles = read_articles()
    analytics_data = read_analytics(article_id)
    article = articles.get(article_id)
    if not article:
        flash('Article not found.', 'error')
        return redirect(url_for('dashboard'))

    total_views = sum(d['views'] for d in analytics_data)
    unique_visitors = sum(d['unique_visitors'] for d in analytics_data)

    return render_template('article_analytics.html', article=article, total_views=total_views, unique_visitors=unique_visitors)

if __name__ == '__main__':
    app.run(debug=True)
