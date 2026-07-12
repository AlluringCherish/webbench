from flask import Flask, request, render_template, redirect, url_for, session, abort
import os
import datetime
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change to a secure key in production

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# --- Utility functions for file operations and parsing ---

def get_file_path(filename):
    return os.path.join(DATA_DIR, filename)


def parse_pipe_delimited_file(filename, fieldnames):
    """
    Parse a pipe-delimited file into list of dicts.
    """
    filepath = get_file_path(filename)
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                # Pad with empty strings if parts are fewer than fieldnames
                if len(parts) < len(fieldnames):
                    parts.extend([''] * (len(fieldnames) - len(parts)))
                record = dict(zip(fieldnames, parts))
                data.append(record)
    except FileNotFoundError:
        pass  # No data file yet
    return data


def write_pipe_delimited_file(filename, data, fieldnames):
    filepath = get_file_path(filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        for record in data:
            line = '|'.join(str(record.get(field, '')) for field in fieldnames)
            f.write(line + '\n')


def append_pipe_delimited_file(filename, record, fieldnames):
    filepath = get_file_path(filename)
    with open(filepath, 'a', encoding='utf-8') as f:
        line = '|'.join(str(record.get(field, '')) for field in fieldnames)
        f.write(line + '\n')


def get_next_id(records, id_field):
    max_id = 0
    for record in records:
        try:
            rid = int(record.get(id_field, '0'))
            if rid > max_id:
                max_id = rid
        except ValueError:
            continue
    return max_id + 1


def current_timestamp():
    return datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


# --- Data Models ---

# Schemas according to architecture.md for each data file
USERS_FIELDS = ['user_id', 'username', 'email', 'role']
ARTICLES_FIELDS = ['article_id', 'title', 'author', 'category', 'status', 'created_date', 'last_updated']
ARTICLE_VERSIONS_FIELDS = ['version_id', 'article_id', 'version_number', 'content', 'author', 'created_date', 'change_summary']
APPROVALS_FIELDS = ['approval_id', 'article_id', 'version_id', 'approver', 'status', 'comments', 'timestamp']
COMMENTS_FIELDS = ['comment_id', 'article_id', 'version_id', 'user', 'comment_text', 'timestamp']
WORKFLOW_STAGES_FIELDS = ['workflow_stage_id', 'category', 'stage_order', 'stage_name']
ANALYTICS_FIELDS = ['analytics_id', 'article_id', 'date', 'views', 'unique_visitors', 'avg_time_on_article', 'shares']


# Load data record lists
# These are raw loads for each operation; caching could be implemented if needed

def load_users():
    return parse_pipe_delimited_file('users.txt', USERS_FIELDS)


def load_articles():
    return parse_pipe_delimited_file('articles.txt', ARTICLES_FIELDS)


def load_article_versions():
    return parse_pipe_delimited_file('article_versions.txt', ARTICLE_VERSIONS_FIELDS)


def load_approvals():
    return parse_pipe_delimited_file('approvals.txt', APPROVALS_FIELDS)


def load_comments():
    return parse_pipe_delimited_file('comments.txt', COMMENTS_FIELDS)


def load_workflow_stages():
    return parse_pipe_delimited_file('workflow_stages.txt', WORKFLOW_STAGES_FIELDS)


def load_analytics():
    return parse_pipe_delimited_file('analytics.txt', ANALYTICS_FIELDS)


# Save entire datasets for updates

def save_articles(records):
    write_pipe_delimited_file('articles.txt', records, ARTICLES_FIELDS)


def save_article_versions(records):
    write_pipe_delimited_file('article_versions.txt', records, ARTICLE_VERSIONS_FIELDS)


def save_approvals(records):
    write_pipe_delimited_file('approvals.txt', records, APPROVALS_FIELDS)


def save_comments(records):
    write_pipe_delimited_file('comments.txt', records, COMMENTS_FIELDS)


# --- Service methods ---

def get_article_by_id(article_id):
    articles = load_articles()
    for article in articles:
        if str(article.get('article_id')) == str(article_id):
            return article
    return None


def get_article_versions(article_id):
    article_versions = load_article_versions()
    versions = [v for v in article_versions if v.get('article_id') == str(article_id)]
    # Sort by version_number ascending
    versions.sort(key=lambda x: int(x.get('version_number', '0')))
    return versions


def get_latest_version(article_id):
    versions = get_article_versions(article_id)
    if versions:
        return versions[-1]
    return None


def get_approvals_for_version(article_id, version_id):
    approvals = load_approvals()
    filtered = [a for a in approvals if a.get('article_id') == str(article_id) and a.get('version_id') == str(version_id)]
    return filtered


def get_comments_for_version(article_id, version_id):
    comments = load_comments()
    filtered = [c for c in comments if c.get('article_id') == str(article_id) and c.get('version_id') == str(version_id)]
    # Sort by timestamp ascending
    filtered.sort(key=lambda x: x.get('timestamp', ''))
    return filtered


def increment_version_number(article_id):
    versions = get_article_versions(article_id)
    if not versions:
        return 1
    max_version = max(int(v['version_number']) for v in versions)
    return max_version + 1


def create_article(title, content, author, category='General'):
    # Add new article
    articles = load_articles()
    article_id = get_next_id(articles, 'article_id')
    created_date = current_timestamp()
    new_article = {
        'article_id': str(article_id),
        'title': title,
        'author': author,
        'category': category,
        'status': 'draft',
        'created_date': created_date,
        'last_updated': created_date
    }
    articles.append(new_article)
    save_articles(articles)

    # Create first version
    article_versions = load_article_versions()
    version_id = get_next_id(article_versions, 'version_id')
    new_version = {
        'version_id': str(version_id),
        'article_id': str(article_id),
        'version_number': '1',
        'content': content,
        'author': author,
        'created_date': created_date,
        'change_summary': 'Initial version'
    }
    article_versions.append(new_version)
    save_article_versions(article_versions)
    return new_article


def update_article(article_id, title, content, author, change_summary='Updated content'):
    articles = load_articles()
    article_found = False
    for art in articles:
        if art.get('article_id') == str(article_id):
            art['title'] = title
            art['last_updated'] = current_timestamp()
            article_found = True
            break
    if not article_found:
        return None
    save_articles(articles)

    # Create new version
    article_versions = load_article_versions()
    version_id = get_next_id(article_versions, 'version_id')
    version_number = increment_version_number(article_id)
    new_version = {
        'version_id': str(version_id),
        'article_id': str(article_id),
        'version_number': str(version_number),
        'content': content,
        'author': author,
        'created_date': current_timestamp(),
        'change_summary': change_summary
    }
    article_versions.append(new_version)
    save_article_versions(article_versions)
    return True


def get_articles_by_author(username, filter_status=None):
    articles = load_articles()
    user_articles = [a for a in articles if a.get('author') == username]
    if filter_status:
        user_articles = [a for a in user_articles if a.get('status') == filter_status]
    return user_articles


def get_published_articles(filter_category=None, sort_order=None):
    articles = load_articles()
    published = [a for a in articles if a.get('status') == 'published']
    if filter_category:
        published = [a for a in published if a.get('category') == filter_category]

    # Sort order handling: expecting 'asc' or 'desc' for created_date
    if sort_order == 'title':
        published.sort(key=lambda x: x.get('title', '').lower())
    elif sort_order == 'author':
        published.sort(key=lambda x: x.get('author', '').lower())
    elif sort_order == 'asc':
        published.sort(key=lambda x: x.get('created_date', ''))
    elif sort_order == 'desc':
        published.sort(key=lambda x: x.get('created_date', ''), reverse=True)
    else:
        published.sort(key=lambda x: x.get('created_date', ''), reverse=True)

    return published


def get_scheduled_content():
    articles = load_articles()
    scheduled_items = [a for a in articles if a.get('status') == 'scheduled']
    for item in scheduled_items:
        item['date'] = item.get('last_updated', '')
        item['title'] = item.get('title', '')
    scheduled_items.sort(key=lambda x: x.get('last_updated',''))
    return scheduled_items


def aggregate_article_analytics(article_id):
    analytics = load_analytics()
    relevant = [a for a in analytics if a.get('article_id') == str(article_id)]
    overview = {
        'total_views': 0,
        'unique_visitors': 0,
        'average_time_on_article': 0.0,
        'shares': 0
    }
    if not relevant:
        return overview

    total_time = 0.0
    count = 0

    for record in relevant:
        try:
            overview['total_views'] += int(record.get('views', '0'))
            overview['unique_visitors'] += int(record.get('unique_visitors', '0'))
            total_time += float(record.get('avg_time_on_article', '0'))
            overview['shares'] += int(record.get('shares', '0'))
            count += 1
        except ValueError:
            continue

    if count > 0:
        overview['average_time_on_article'] = round(total_time / count, 2)

    return overview


# --- Route helpers for session and auth ---

def get_logged_in_username():
    return session.get('username')


def require_login():
    username = get_logged_in_username()
    if not username:
        abort(401)  # Unauthorized
    return username


# --- Flask Routes per architecture.md ---

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('root_redirect'))  # Note: root_redirect redirects to dashboard, potential infinite redirect if no login

    user_articles = get_articles_by_author(username)
    total_user_articles = len(user_articles)
    all_published = get_published_articles()
    total_published = len(all_published)

    recent_activity = sorted(user_articles, key=lambda x: x.get('last_updated',''), reverse=True)[:5]

    quick_stats = {
        'total_my_articles': total_user_articles,
        'total_published_articles': total_published
    }

    return render_template('dashboard.html', username=username, quick_stats=quick_stats, recent_activity=recent_activity)


@app.route('/article/create', methods=['GET', 'POST'])
def create_article_route():
    username = require_login()
    if request.method == 'GET':
        return render_template('create_article.html')

    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    category = request.form.get('category', 'General').strip() or 'General'

    errors = {}
    if not title:
        errors['title'] = 'Title is required.'
    if not content:
        errors['content'] = 'Content is required.'

    if errors:
        return render_template('create_article.html', errors=errors, title=title, content=content, category=category)

    new_article = create_article(title, content, username, category)
    if not new_article:
        errors['general'] = 'Failed to create article.'
        return render_template('create_article.html', errors=errors, title=title, content=content, category=category)

    return redirect(url_for('edit_article', article_id=new_article['article_id']))


@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    username = require_login()
    article = get_article_by_id(article_id)
    if not article:
        abort(404, description='Article not found')

    if article.get('author') != username:
        abort(403, description='Forbidden: You are not the author')

    if request.method == 'GET':
        latest_version = get_latest_version(article_id)
        content = latest_version.get('content') if latest_version else ''
        return render_template('edit_article.html', article=article, content=content, article_id=article_id)

    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()

    errors = {}
    if not title:
        errors['title'] = 'Title is required.'
    if not content:
        errors['content'] = 'Content is required.'

    if errors:
        return render_template('edit_article.html', article=article, content=content, errors=errors, article_id=article_id)

    update_success = update_article(article_id, title, content, username)
    if not update_success:
        errors['general'] = 'Failed to update article.'
        return render_template('edit_article.html', article=article, content=content, errors=errors, article_id=article_id)

    return redirect(url_for('edit_article', article_id=article_id))


@app.route('/article/<int:article_id>/versions', methods=['GET'])
def article_version_history(article_id):
    article = get_article_by_id(article_id)
    if not article:
        abort(404, description='Article not found')

    versions = get_article_versions(article_id)

    return render_template('version_history.html', article_id=article_id, versions=versions)


@app.route('/articles/mine', methods=['GET'])
def my_articles():
    username = require_login()
    filter_status = request.args.get('filter_status', None)

    articles = get_articles_by_author(username, filter_status=filter_status)

    return render_template('my_articles.html', username=username, articles=articles, filter_status=filter_status)


@app.route('/articles/published', methods=['GET'])
def published_articles():
    filter_category = request.args.get('category', None)
    sort_order = request.args.get('sort', None)

    articles = get_published_articles(filter_category=filter_category, sort_order=sort_order)

    return render_template('published_articles.html', articles=articles, filter_category=filter_category, sort_order=sort_order)


@app.route('/calendar', methods=['GET'])
def content_calendar():
    calendar_view = request.args.get('calendar_view', 'monthly')
    scheduled_items = get_scheduled_content()

    return render_template('content_calendar.html', calendar_view=calendar_view, scheduled_items=scheduled_items)


@app.route('/article/<int:article_id>/analytics', methods=['GET'])
def article_analytics(article_id):
    article = get_article_by_id(article_id)
    if not article:
        abort(404, description='Article not found')

    analytics_overview = aggregate_article_analytics(article_id)

    return render_template('article_analytics.html', article_id=article_id, analytics_overview=analytics_overview)


# Run the Flask app if executed directly
if __name__ == '__main__':
    app.run(debug=True)
