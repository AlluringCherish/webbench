from flask import Flask, request, jsonify, render_template, session, redirect, url_for, abort
from threading import Lock
import os
import csv

app = Flask(__name__)
app.secret_key = 'change_this_secret'

# File paths
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
ARTICLES_FILE = os.path.join(DATA_DIR, 'articles.txt')
ARTICLE_VERSIONS_FILE = os.path.join(DATA_DIR, 'article_versions.txt')
APPROVALS_FILE = os.path.join(DATA_DIR, 'approvals.txt')
WORKFLOW_STAGES_FILE = os.path.join(DATA_DIR, 'workflow_stages.txt')
COMMENTS_FILE = os.path.join(DATA_DIR, 'comments.txt')
ANALYTICS_FILE = os.path.join(DATA_DIR, 'analytics.txt')

# Locks for thread-safe file write
users_lock = Lock()
articles_lock = Lock()
versions_lock = Lock()
approvals_lock = Lock()
comments_lock = Lock()
analytics_lock = Lock()

# Field names as per schema
users_fields = ['user_id', 'username', 'email', 'role']
articles_fields = ['article_id', 'title', 'author', 'category', 'status', 'published_date']
article_versions_fields = ['version_id', 'article_id', 'version_number', 'content', 'created_at']
approvals_fields = ['approval_id', 'version_id', 'approver', 'status', 'comment', 'timestamp']
workflow_stages_fields = ['stage_id', 'category', 'step_order', 'step_name', 'required_approver']
comments_fields = ['comment_id', 'version_id', 'commenter', 'comment_text', 'timestamp']
analytics_fields = ['analytics_id', 'article_id', 'date', 'views', 'unique_visitors', 'time_spent', 'shares']


# Helper functions for file reading and writing

def read_data_file(filepath, fieldnames):
    data = []
    if not os.path.exists(filepath):
        return data
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='|', fieldnames=fieldnames)
        for row in reader:
            data.append(row)
    return data


def write_data_file(filepath, fieldnames, data):
    temp_file = filepath + '.tmp'
    with open(temp_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, delimiter='|', fieldnames=fieldnames)
        for row in data:
            writer.writerow(row)
    os.replace(temp_file, filepath)


def append_data_file(filepath, fieldnames, row_dict, lock):
    with lock:
        file_exists = os.path.exists(filepath)
        with open(filepath, 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, delimiter='|', fieldnames=fieldnames)
            if not file_exists:
                # write header
                pass  # headers not needed per schema
            writer.writerow(row_dict)


# Read initial data into memory on start

def load_users():
    users = read_data_file(USERS_FILE, users_fields)
    users_map = {u['user_id']: u for u in users}
    return users_map

def load_articles():
    articles = read_data_file(ARTICLES_FILE, articles_fields)
    articles_map = {a['article_id']: a for a in articles}
    return articles_map

def load_article_versions():
    versions = read_data_file(ARTICLE_VERSIONS_FILE, article_versions_fields)
    versions_map = {}
    for v in versions:
        a_id = v['article_id']
        versions_map.setdefault(a_id, []).append(v)
    # Optional sort by version_number ascending
    for vlist in versions_map.values():
        vlist.sort(key=lambda x: int(x['version_number']))
    return versions_map

def load_approvals():
    approvals = read_data_file(APPROVALS_FILE, approvals_fields)
    approvals_map = {}
    for a in approvals:
        v_id = a['version_id']
        approvals_map.setdefault(v_id, []).append(a)
    return approvals_map

def load_workflow_stages():
    stages = read_data_file(WORKFLOW_STAGES_FILE, workflow_stages_fields)
    stages_map = {}
    for s in stages:
        cat = s['category']
        stages_map.setdefault(cat, []).append(s)
    # sort steps by step_order
    for steps in stages_map.values():
        steps.sort(key=lambda x: int(x['step_order']))
    return stages_map

def load_comments():
    comments = read_data_file(COMMENTS_FILE, comments_fields)
    comments_map = {}
    for c in comments:
        v_id = c['version_id']
        comments_map.setdefault(v_id, []).append(c)
    return comments_map

def load_analytics():
    analytics = read_data_file(ANALYTICS_FILE, analytics_fields)
    analytics_map = {}
    for a in analytics:
        art_id = a['article_id']
        analytics_map.setdefault(art_id, []).append(a)
    return analytics_map


# Global cached data - to simplify demonstration
users_cache = load_users()
articles_cache = load_articles()
versions_cache = load_article_versions()
approvals_cache = load_approvals()
stages_cache = load_workflow_stages()
comments_cache = load_comments()
analytics_cache = load_analytics()


# Utility ID increment functions

def next_id(data_map):
    if not data_map:
        return '1'
    max_id = max(int(k) for k in data_map.keys() if k.isdigit())
    return str(max_id + 1)

def next_id_from_list(data_list):
    if not data_list:
        return '1'
    max_id = max(int(item[next(iter(item))]) for item in data_list if item[next(iter(item))].isdigit())
    return str(max_id + 1)

def next_article_id():
    return next_id(articles_cache)

def next_version_id():
    # versions_cache maps article_id to list of versions
    all_ids = []
    for vers in versions_cache.values():
        all_ids.extend([int(v['version_id']) for v in vers if v['version_id'].isdigit()])
    if not all_ids:
        return '1'
    return str(max(all_ids) + 1)


def auth_required():
    if 'username' not in session:
        abort(401)  # Unauthorized


def get_user_by_username(username):
    for user in users_cache.values():
        if user['username'] == username:
            return user
    return None


# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    auth_required()
    username = session['username']
    user = get_user_by_username(username)
    # Prepare quick stats
    total_articles = len(articles_cache)
    total_versions = sum(len(v) for v in versions_cache.values())
    recent_activity = []  # Placeholder for demo
    quick_stats = {
        'total_articles': total_articles,
        'total_versions': total_versions,
    }
    return render_template('dashboard.html', username=username, quick_stats=quick_stats, recent_activity=recent_activity)


@app.route('/article/create', methods=['GET', 'POST'])
def create_article():
    auth_required()
    if request.method == 'GET':
        return render_template('create_article.html')
    # POST
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    category = request.form.get('category', '').strip()
    if not title or not content or not category:
        return render_template('create_article.html', error='Missing required fields')
    # Add new article
    article_id = next_article_id()
    author_user = get_user_by_username(session['username'])
    # status default draft
    article_rec = {
        'article_id': article_id,
        'title': title,
        'author': author_user['username'],
        'category': category,
        'status': 'draft',
        'published_date': ''
    }
    with articles_lock:
        articles_cache[article_id] = article_rec
        write_data_file(ARTICLES_FILE, articles_fields, articles_cache.values())
    # Create initial version record
    version_id = next_version_id()
    version_rec = {
        'version_id': version_id,
        'article_id': article_id,
        'version_number': '1',
        'content': content,
        'created_at': '',
    }
    with versions_lock:
        versions_cache.setdefault(article_id, []).append(version_rec)
        all_versions = []
        for vers_list in versions_cache.values():
            all_versions.extend(vers_list)
        write_data_file(ARTICLE_VERSIONS_FILE, article_versions_fields, all_versions)
    return redirect(url_for('edit_article', article_id=article_id))


@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    auth_required()
    article_id_str = str(article_id)
    article = articles_cache.get(article_id_str)
    if not article:
        abort(404)
    if request.method == 'GET':
        # Return current article and versions
        article_versions = versions_cache.get(article_id_str, [])
        # load approvals and comments per version
        for v in article_versions:
            v_id = v['version_id']
            v['approvals'] = approvals_cache.get(v_id, [])
            v['comments'] = comments_cache.get(v_id, [])
        return render_template('edit_article.html', article=article, versions=article_versions)
    # POST to save new version
    content = request.form.get('content', '').strip()
    if not content:
        return render_template('edit_article.html', article=article, versions=versions_cache.get(article_id_str, []), error='Content cannot be empty')
    # Determine version_number
    current_versions = versions_cache.get(article_id_str, [])
    new_version_number = str(len(current_versions) + 1)
    new_version_id = next_version_id()
    version_rec = {
        'version_id': new_version_id,
        'article_id': article_id_str,
        'version_number': new_version_number,
        'content': content,
        'created_at': '',
    }
    with versions_lock:
        current_versions.append(version_rec)
        # write back all versions
        all_versions = []
        for vers_list in versions_cache.values():
            all_versions.extend(vers_list)
        write_data_file(ARTICLE_VERSIONS_FILE, article_versions_fields, all_versions)
    return redirect(url_for('edit_article', article_id=article_id))


@app.route('/article/<int:article_id>/versions')
def article_version_history(article_id):
    auth_required()
    article_id_str = str(article_id)
    article = articles_cache.get(article_id_str)
    if not article:
        abort(404)
    article_versions = versions_cache.get(article_id_str, [])
    for v in article_versions:
        v_id = v['version_id']
        v['approvals'] = approvals_cache.get(v_id, [])
        v['comments'] = comments_cache.get(v_id, [])
    return render_template('version_history.html', article=article, versions=article_versions)


@app.route('/articles/mine')
def my_articles():
    auth_required()
    username = session['username']
    my_articles = [a for a in articles_cache.values() if a['author'] == username]
    return render_template('my_articles.html', articles=my_articles)


@app.route('/articles/published')
def published_articles():
    auth_required()
    filter_title = request.args.get('filter', '').strip().lower()
    filtered_articles = [a for a in articles_cache.values() if a['status'] == 'published']
    if filter_title:
        filtered_articles = [a for a in filtered_articles if filter_title in a['title'].lower()]
    return render_template('published_articles.html', articles=filtered_articles)


@app.route('/calendar')
def content_calendar():
    auth_required()
    # For demo, empty events list
    events = []
    return render_template('content_calendar.html', events=events)


@app.route('/article/<int:article_id>/analytics')
def article_analytics(article_id):
    auth_required()
    article_id_str = str(article_id)
    article = articles_cache.get(article_id_str)
    if not article:
        abort(404)
    # Aggregate analytics from analytics_cache
    analytics_list = analytics_cache.get(article_id_str, [])
    total_views = sum(int(a['views']) for a in analytics_list if a['views'].isdigit())
    unique_visitors = sum(int(a['unique_visitors']) for a in analytics_list if a['unique_visitors'].isdigit())
    avg_time_spent = 0
    if analytics_list:
        total_time = sum(float(a['time_spent']) for a in analytics_list if a['time_spent'])
        avg_time_spent = total_time / len(analytics_list)
    total_shares = sum(int(a['shares']) for a in analytics_list if a['shares'].isdigit())
    # Bounce rate is unavailable, so default to 0
    bounce_rate = 0
    analytics_summary = {
        'total_views': total_views,
        'unique_visitors': unique_visitors,
        'avg_time_spent': avg_time_spent,
        'total_shares': total_shares,
        'bounce_rate': bounce_rate
    }
    return render_template('article_analytics.html', article=article, analytics=analytics_summary)


if __name__ == '__main__':
    app.run(debug=True)
