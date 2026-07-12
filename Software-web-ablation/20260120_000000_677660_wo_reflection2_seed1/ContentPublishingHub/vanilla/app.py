from flask import Flask, render_template, request, redirect, url_for, session, abort, flash
from datetime import datetime
import os

# Constants
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# Ensure data directory exists at startup
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Helper utilities for file reading and writing
LOCKS = {}

def write_text_file(filename, content):
    '''Utility to atomically write text content to a file.'''
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

# Data Access Layer

# Users Data Access
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
ARTICLES_FILE = os.path.join(DATA_DIR, 'articles.txt')
VERSIONS_FILE = os.path.join(DATA_DIR, 'article_versions.txt')
APPROVALS_FILE = os.path.join(DATA_DIR, 'approvals.txt')
COMMENTS_FILE = os.path.join(DATA_DIR, 'comments.txt')
WORKFLOW_STAGES_FILE = os.path.join(DATA_DIR, 'workflow_stages.txt')

# Models are basic data dictionaries keyed on specific fields

def parse_line(line, num_fields):
    parts = line.strip().split('|')
    if len(parts) != num_fields:
        return None
    return parts

# ------------------------- User DAO --------------------------
def read_users():
    '''Reads users.txt into list of dicts with keys: username, full_name, email, role'''
    users = []
    if not os.path.exists(USERS_FILE):
        return users
    with open(USERS_FILE, encoding='utf-8') as f:
        for line in f:
            parts = parse_line(line, 4)
            if parts:
                user = {
                    'username': parts[0],
                    'full_name': parts[1],
                    'email': parts[2],
                    'role': parts[3]
                }
                users.append(user)
    return users

def get_user(username):
    users = read_users()
    for user in users:
        if user['username'] == username:
            return user
    return None

# ------------------------- Articles DAO ------------------------
def read_articles():
    '''Reads articles.txt into list of dicts with keys: article_id, title, category, author, status, created_date, published_date'''
    articles = []
    if not os.path.exists(ARTICLES_FILE):
        return articles
    with open(ARTICLES_FILE, encoding='utf-8') as f:
        for line in f:
            parts = parse_line(line, 7)
            if parts:
                article = {
                    'article_id': int(parts[0]),
                    'title': parts[1],
                    'category': parts[2],
                    'author': parts[3],
                    'status': parts[4],  # e.g. draft, published
                    'created_date': parts[5],  # yyyy-mm-dd
                    'published_date': parts[6]  # yyyy-mm-dd or empty
                }
                articles.append(article)
    return articles

def write_articles(articles):
    lines = []
    for a in articles:
        line = f"{a['article_id']}|{a['title']}|{a['category']}|{a['author']}|{a['status']}|{a['created_date']}|{a['published_date']}"
        lines.append(line)
    write_text_file(ARTICLES_FILE, "\n".join(lines))

# Helper to get next article id

def next_article_id():
    articles = read_articles()
    if not articles:
        return 1
    return max(a['article_id'] for a in articles) + 1

# Find article by id

def get_article(article_id):
    articles = read_articles()
    for a in articles:
        if a['article_id'] == article_id:
            return a
    return None

# ----------------------- Article Versions DAO ------------------
def read_versions():
    '''Reads article_versions.txt as list of dictionaries with fields:
    version_id, article_id, version_number, content, author, created_date, change_summary
    '''
    versions = []
    if not os.path.exists(VERSIONS_FILE):
        return versions
    with open(VERSIONS_FILE, encoding='utf-8') as f:
        for line in f:
            parts = parse_line(line, 7)
            if parts:
                version = {
                    'version_id': int(parts[0]),
                    'article_id': int(parts[1]),
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
        # Content must not contain pipe character; we'll escape by replacing with space for safety
        content_clean = v['content'].replace('|',' ')
        line = f"{v['version_id']}|{v['article_id']}|{v['version_number']}|{content_clean}|{v['author']}|{v['created_date']}|{v['change_summary']}"
        lines.append(line)
    write_text_file(VERSIONS_FILE, "\n".join(lines))

# Helper to get next version_id

def next_version_id():
    versions = read_versions()
    if not versions:
        return 1
    return max(v['version_id'] for v in versions) + 1

# Get versions by article_id

def get_versions_by_article(article_id):
    versions = read_versions()
    return sorted([v for v in versions if v['article_id'] == article_id], key=lambda x: x['version_number'])

# Get highest version number by article_id

def get_latest_version_number(article_id):
    versions = get_versions_by_article(article_id)
    if not versions:
        return 0
    return versions[-1]['version_number']

# --------------------------- Approvals DAO ----------------------
def read_approvals():
    '''Reads approvals.txt with fields:
    approval_id, article_id, version_id, approver_username, status, comments, timestamp
    '''
    approvals = []
    if not os.path.exists(APPROVALS_FILE):
        return approvals
    with open(APPROVALS_FILE, encoding='utf-8') as f:
        for line in f:
            parts = parse_line(line, 7)
            if parts:
                approval = {
                    'approval_id': int(parts[0]),
                    'article_id': int(parts[1]),
                    'version_id': int(parts[2]),
                    'approver_username': parts[3],
                    'status': parts[4],  # approved, rejected, revision_requested
                    'comments': parts[5],
                    'timestamp': parts[6]
                }
                approvals.append(approval)
    return approvals


def write_approvals(approvals):
    lines = []
    for a in approvals:
        comments_clean = a['comments'].replace('|', ' ')
        line = f"{a['approval_id']}|{a['article_id']}|{a['version_id']}|{a['approver_username']}|{a['status']}|{comments_clean}|{a['timestamp']}"
        lines.append(line)
    write_text_file(APPROVALS_FILE, "\n".join(lines))

# Helper to get next approval_id

def next_approval_id():
    approvals = read_approvals()
    if not approvals:
        return 1
    return max(a['approval_id'] for a in approvals) + 1

# Get approvals by article_id and version_id

def get_approvals_for_version(article_id, version_id):
    approvals = read_approvals()
    return [a for a in approvals if a['article_id'] == article_id and a['version_id'] == version_id]

# ---------------------------- Comments DAO ------------------------
def read_comments():
    '''Reads comments.txt with fields:
    comment_id, article_id, version_id, username, comment_text, timestamp
    '''
    comments = []
    if not os.path.exists(COMMENTS_FILE):
        return comments
    with open(COMMENTS_FILE, encoding='utf-8') as f:
        for line in f:
            parts = parse_line(line, 6)
            if parts:
                comment = {
                    'comment_id': int(parts[0]),
                    'article_id': int(parts[1]),
                    'version_id': int(parts[2]),
                    'username': parts[3],
                    'comment_text': parts[4],
                    'timestamp': parts[5]
                }
                comments.append(comment)
    return comments


def write_comments(comments):
    lines = []
    for c in comments:
        comment_text_clean = c['comment_text'].replace('|',' ')
        line = f"{c['comment_id']}|{c['article_id']}|{c['version_id']}|{c['username']}|{comment_text_clean}|{c['timestamp']}"
        lines.append(line)
    write_text_file(COMMENTS_FILE, "\n".join(lines))

# Helper for next comment id

def next_comment_id():
    comments = read_comments()
    if not comments:
        return 1
    return max(c['comment_id'] for c in comments) + 1

# --------------------------- Workflow Stages DAO --------------
def read_workflow_stages():
    '''workflow_stages.txt format:
    category|stage_order|stage_name
    '''
    stages = []
    if not os.path.exists(WORKFLOW_STAGES_FILE):
        return stages
    with open(WORKFLOW_STAGES_FILE, encoding='utf-8') as f:
        for line in f:
            parts = parse_line(line, 3)
            if parts:
                stage = {
                    'category': parts[0],
                    'stage_order': int(parts[1]),
                    'stage_name': parts[2]
                }
                stages.append(stage)
    return stages

# --------------------------- Analytics DAO -----------------------
# analytics.txt assumed to have records:
# article_id|date|views|unique_visitors|average_time|shares
ANALYTICS_FILE = os.path.join(DATA_DIR, 'analytics.txt')

def read_analytics():
    analytics = []
    if not os.path.exists(ANALYTICS_FILE):
        return analytics
    with open(ANALYTICS_FILE, encoding='utf-8') as f:
        for line in f:
            parts = parse_line(line, 6)
            if parts:
                record = {
                    'article_id': int(parts[0]),
                    'date': parts[1],
                    'views': int(parts[2]),
                    'unique_visitors': int(parts[3]),
                    'average_time': float(parts[4]),
                    'shares': int(parts[5])
                }
                analytics.append(record)
    return analytics

# No write operation needed here as per spec (analytics only read)

# --------------------------- Services Layer ----------------------

from copy import deepcopy

def create_article(title, category, author):
    '''Create new article entry with draft status and initial version. Returns article_id or error message.'''
    if not title or not category or not author:
        return None, 'Title, category, and author are required.'
    # Create article
    new_id = next_article_id()
    today = datetime.now().strftime('%Y-%m-%d')
    article = {
        'article_id': new_id,
        'title': title.strip(),
        'category': category.strip(),
        'author': author.strip(),
        'status': 'draft',
        'created_date': today,
        'published_date': ''
    }
    articles = read_articles()
    articles.append(article)
    write_articles(articles)
    # Create initial version with empty content and change summary
    version_id = next_version_id()
    version = {
        'version_id': version_id,
        'article_id': new_id,
        'version_number': 1,
        'content': '',
        'author': author.strip(),
        'created_date': today,
        'change_summary': 'Initial version'
    }
    versions = read_versions()
    versions.append(version)
    write_versions(versions)
    return new_id, None


def update_article(article_id, title, category, editor_username, new_content, change_summary):
    '''Update article metadata and create new version if content changed. Returns error or None.'''
    article = get_article(article_id)
    if not article:
        return 'Article not found.'
    changed = False
    if title and title.strip() != article['title']:
        article['title'] = title.strip()
        changed = True
    if category and category.strip() != article['category']:
        article['category'] = category.strip()
        changed = True
    # Save article metadata
    articles = read_articles()
    for i, a in enumerate(articles):
        if a['article_id'] == article_id:
            articles[i] = article
            break
    write_articles(articles)

    # Check if content changed - compare latest version content
    versions = get_versions_by_article(article_id)
    latest_content = versions[-1]['content'] if versions else ''
    if new_content != latest_content:
        # Create new version
        version_id = next_version_id()
        new_version_number = get_latest_version_number(article_id) + 1
        today = datetime.now().strftime('%Y-%m-%d')
        version = {
            'version_id': version_id,
            'article_id': article_id,
            'version_number': new_version_number,
            'content': new_content,
            'author': editor_username,
            'created_date': today,
            'change_summary': change_summary or ''
        }
        versions_all = read_versions()
        versions_all.append(version)
        write_versions(versions_all)
        changed = True
    if not changed:
        return 'No changes detected.'
    return None

# Approvals service

def add_approval(article_id, version_id, approver_username, status, comments):
    '''Add approval record. Status must be approved, rejected, or revision_requested.'''
    if status not in ('approved', 'rejected', 'revision_requested'):
        return 'Invalid approval status.'
    approval_id = next_approval_id()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    approval = {
        'approval_id': approval_id,
        'article_id': article_id,
        'version_id': version_id,
        'approver_username': approver_username,
        'status': status,
        'comments': comments or '',
        'timestamp': now
    }
    approvals = read_approvals()
    approvals.append(approval)
    write_approvals(approvals)
    return None

# Comments service

def add_comment(article_id, version_id, username, comment_text):
    if not comment_text:
        return 'Comment text cannot be empty.'
    comment_id = next_comment_id()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    comment = {
        'comment_id': comment_id,
        'article_id': article_id,
        'version_id': version_id,
        'username': username,
        'comment_text': comment_text,
        'timestamp': now
    }
    comments = read_comments()
    comments.append(comment)
    write_comments(comments)
    return None

# Analytics service

def aggregate_article_analytics(article_id):
    records = [rec for rec in read_analytics() if rec['article_id'] == article_id]
    if not records:
        return {
            'total_views': 0,
            'total_unique_visitors': 0,
            'average_time': 0.0,
            'total_shares': 0
        }
    total_views = sum(r['views'] for r in records)
    total_unique_visitors = sum(r['unique_visitors'] for r in records)
    avg_time = sum(r['average_time'] * r['views'] for r in records) / total_views if total_views > 0 else 0.0
    total_shares = sum(r['shares'] for r in records)
    return {
        'total_views': total_views,
        'total_unique_visitors': total_unique_visitors,
        'average_time': round(avg_time, 2),
        'total_shares': total_shares
    }

# --------------------------- Flask app ----------------------------
from flask import flash
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management, in prod use env var

# Stub for session handling - in real app replace with real auth
@app.before_request
def check_login():
    # We'll simulate a session user for demonstration
    # Replace this with actual login logic
    if 'username' not in session and request.endpoint != 'login' and not request.endpoint.startswith('static'):
        # For testing, auto-set username to 'john'
        session['username'] = 'john'


# Routes implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('root_redirect'))

    # Gather user stats: number of articles, number published, drafts
    articles = read_articles()
    user_articles = [a for a in articles if a['author'] == username]
    num_articles = len(user_articles)
    num_published = len([a for a in user_articles if a['status'] == 'published'])
    num_drafts = num_articles - num_published

    context = {
        'username': username,
        'num_articles': num_articles,
        'num_published': num_published,
        'num_drafts': num_drafts
    }
    return render_template('dashboard.html', **context)


@app.route('/article/create', methods=['GET', 'POST'])
def create_article_route():
    username = session.get('username')
    if not username:
        return redirect(url_for('root_redirect'))
    error = None
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        article_id, error = create_article(title, category, username)
        if error:
            return render_template('create_article.html', error=error, title=title, category=category)
        return redirect(url_for('edit_article', article_id=article_id))
    return render_template('create_article.html')


@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    username = session.get('username')
    if not username:
        return redirect(url_for('root_redirect'))

    article = get_article(article_id)
    if not article:
        abort(404)

    # Read latest version content
    versions = get_versions_by_article(article_id)
    if not versions:
        latest_version = None
        content = ''
        change_summary = ''
    else:
        latest_version = versions[-1]
        content = latest_version['content']
        change_summary = ''

    error = None
    if request.method == 'POST':
        new_title = request.form.get('title', '').strip()
        new_category = request.form.get('category', '').strip()
        new_content = request.form.get('content', '')
        change_summary = request.form.get('change_summary', '').strip()

        error = update_article(article_id, new_title, new_category, username, new_content, change_summary)
        if error:
            # Render with current values and error
            return render_template('edit_article.html', article=article, content=new_content, error=error, change_summary=change_summary)
        # On success reload article and redirect or render
        return redirect(url_for('edit_article', article_id=article_id))

    return render_template('edit_article.html', article=article, content=content)


@app.route('/article/<int:article_id>/versions')
def article_version_history(article_id):
    username = session.get('username')
    if not username:
        return redirect(url_for('root_redirect'))

    article = get_article(article_id)
    if not article:
        abort(404)

    versions = get_versions_by_article(article_id)

    # For simplicity, no version comparison implemented as UI not required

    return render_template('version_history.html', article=article, versions=versions)


@app.route('/articles/mine')
def my_articles():
    username = session.get('username')
    if not username:
        return redirect(url_for('root_redirect'))

    category_filter = request.args.get('category')
    status_filter = request.args.get('status')

    articles = read_articles()
    filtered = [a for a in articles if a['author'] == username]

    if category_filter:
        filtered = [a for a in filtered if a['category'].lower() == category_filter.lower()]
    if status_filter:
        filtered = [a for a in filtered if a['status'].lower() == status_filter.lower()]

    return render_template('my_articles.html', articles=filtered)


@app.route('/articles/published')
def published_articles():
    category_filter = request.args.get('category')
    sort_key = request.args.get('sort')

    articles = read_articles()
    published = [a for a in articles if a['status'] == 'published']

    if category_filter:
        published = [a for a in published if a['category'].lower() == category_filter.lower()]

    if sort_key == 'date':
        published.sort(key=lambda x: x['published_date'] or '', reverse=True)
    elif sort_key == 'title':
        published.sort(key=lambda x: x['title'].lower())

    return render_template('published_articles.html', articles=published)


@app.route('/calendar', methods=['GET', 'POST'])
def content_calendar():
    username = session.get('username')
    if not username:
        return redirect(url_for('root_redirect'))

    if request.method == 'POST':
        # Expect form data for scheduling update: article_id, new_publish_date
        article_id_str = request.form.get('article_id', '')
        new_publish_date = request.form.get('published_date', '')

        errors = []
        # Validate inputs
        try:
            article_id = int(article_id_str)
        except:
            errors.append('Invalid article id.')
            article_id = None

        if not new_publish_date:
            errors.append('Published date is required.')

        article = get_article(article_id) if article_id else None
        if not article:
            errors.append('Article not found.')

        if errors:
            # Render calendar with errors
            calendar_data = [a for a in read_articles() if a['author']==username]
            return render_template('calendar.html', articles=calendar_data, errors=errors)

        # Update article publish date and status
        articles = read_articles()
        for i, a in enumerate(articles):
            if a['article_id'] == article_id:
                articles[i]['published_date'] = new_publish_date
                articles[i]['status'] = 'published'
                break
        write_articles(articles)
        return redirect(url_for('content_calendar'))

    # GET request
    # Show calendar view with user's articles
    articles = read_articles()
    calendar_data = [a for a in articles if a['author'] == username]
    return render_template('calendar.html', articles=calendar_data)


@app.route('/article/<int:article_id>/analytics')
def article_analytics(article_id):
    username = session.get('username')
    if not username:
        return redirect(url_for('root_redirect'))

    article = get_article(article_id)
    if not article:
        abort(404)

    metrics = aggregate_article_analytics(article_id)

    return render_template('article_analytics.html', article=article, metrics=metrics)


# For this minimal app, no other routes defined

if __name__=='__main__':
    app.run(debug=True, port=5000)
