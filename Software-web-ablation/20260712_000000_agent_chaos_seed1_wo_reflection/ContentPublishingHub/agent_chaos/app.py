from flask import Flask, request, session, redirect, url_for, render_template, abort
from datetime import datetime
import os
import threading

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Secret key for sessions. Change in production.

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# Thread lock for file write operations to prevent race conditions
file_lock = threading.Lock()

# --- Data Access Layer Functions ---
# Helper to parse pipe delimited lines into dict based on provided fields

def parse_line(line, fields):
    parts = line.strip().split('|')
    if len(parts) != len(fields):
        return None
    return dict(zip(fields, parts))

# Helper to write all dict rows to file with pipe delimiter

def write_all_lines(filename, data_list, fields):
    path = os.path.join(DATA_DIR, filename)
    with file_lock:
        with open(path, 'w', encoding='utf-8') as f:
            for data in data_list:
                line = '|'.join(str(data.get(fld, '')) for fld in fields)
                f.write(line + '\n')

# Read all data lines from file and parse

def read_all(filename, fields):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    result = []
    for line in lines:
        if line.strip():
            parsed = parse_line(line, fields)
            if parsed:
                result.append(parsed)
    return result

# Append a single data dict as line to file

def append_line(filename, data, fields):
    path = os.path.join(DATA_DIR, filename)
    line = '|'.join(str(data.get(fld, '')) for fld in fields)
    with file_lock:
        with open(path, 'a', encoding='utf-8') as f:
            f.write(line + '\n')


# --- Data Models and Fields ---
# Based on architecture.md and implied data files

USER_FIELDS = ['user_id', 'username', 'fullname', 'email']
ARTICLE_FIELDS = ['article_id', 'author_id', 'title', 'status', 'created_at', 'updated_at']
ARTICLE_VERSION_FIELDS = ['version_id', 'article_id', 'version_number', 'content', 'created_at']
APPROVAL_FIELDS = ['approval_id', 'article_id', 'version_id', 'approver_id', 'status', 'comment', 'timestamp']
COMMENT_FIELDS = ['comment_id', 'article_id', 'version_id', 'user_id', 'comment_text', 'timestamp']
ANALYTICS_FIELDS = ['analytics_id', 'article_id', 'views', 'unique_visitors', 'avg_time_on_article', 'shares', 'date']
WORKFLOW_STAGE_FIELDS = ['stage_id', 'category', 'stage_order', 'stage_name']

# For ID generation, we'll use simple counters based on max existing IDs

def get_next_id(data_list, id_field):
    max_id = 0
    for data in data_list:
        try:
            val = int(data[id_field])
            if val > max_id:
                max_id = val
        except Exception:
            continue
    return max_id + 1


# --- User Session Helper ---

def get_current_user():
    username = session.get('username')
    if not username:
        return None
    # Load user info from users.txt
    users = read_all('users.txt', USER_FIELDS)
    for user in users:
        if user['username'] == username:
            return user
    return None


# --- Article Service Layer ---

def load_article(article_id):
    articles = read_all('articles.txt', ARTICLE_FIELDS)
    for article in articles:
        if article['article_id'] == str(article_id):
            return article
    return None


def load_article_versions(article_id):
    versions = read_all('article_versions.txt', ARTICLE_VERSION_FIELDS)
    article_versions = [v for v in versions if v['article_id'] == str(article_id)]
    # Sort by version_number ascending
    article_versions.sort(key=lambda v: int(v['version_number']))
    return article_versions


def create_article(author_id, title, content):
    articles = read_all('articles.txt', ARTICLE_FIELDS)
    article_id = get_next_id(articles, 'article_id')
    timestamp = datetime.utcnow().isoformat()
    new_article = {
        'article_id': str(article_id),
        'author_id': str(author_id),
        'title': title,
        'status': 'draft',
        'created_at': timestamp,
        'updated_at': timestamp
    }
    append_line('articles.txt', new_article, ARTICLE_FIELDS)
    # Also create first version
    versions = read_all('article_versions.txt', ARTICLE_VERSION_FIELDS)
    version_id = get_next_id(versions, 'version_id')
    first_version = {
        'version_id': str(version_id),
        'article_id': str(article_id),
        'version_number': '1',
        'content': content,
        'created_at': timestamp
    }
    append_line('article_versions.txt', first_version, ARTICLE_VERSION_FIELDS)
    return new_article


def update_article_timestamp(article_id):
    # Updates updated_at field of article to now
    articles = read_all('articles.txt', ARTICLE_FIELDS)
    updated = False
    timestamp = datetime.utcnow().isoformat()
    for article in articles:
        if article['article_id'] == str(article_id):
            article['updated_at'] = timestamp
            updated = True
            break
    if updated:
        write_all_lines('articles.txt', articles, ARTICLE_FIELDS)


def create_new_version(article_id, content):
    versions = read_all('article_versions.txt', ARTICLE_VERSION_FIELDS)
    article_versions = [v for v in versions if v['article_id'] == str(article_id)]
    if article_versions:
        max_version_num = max(int(v['version_number']) for v in article_versions)
        version_number = max_version_num + 1
    else:
        version_number = 1
    version_id = get_next_id(versions, 'version_id')
    timestamp = datetime.utcnow().isoformat()
    new_version = {
        'version_id': str(version_id),
        'article_id': str(article_id),
        'version_number': str(version_number),
        'content': content,
        'created_at': timestamp
    }
    append_line('article_versions.txt', new_version, ARTICLE_VERSION_FIELDS)
    update_article_timestamp(article_id)
    return new_version


# --- Approval Services ---

def load_approvals(article_id, version_id):
    approvals = read_all('approvals.txt', APPROVAL_FIELDS)
    return [apr for apr in approvals if apr['article_id'] == str(article_id) and apr['version_id'] == str(version_id)]


def add_approval(article_id, version_id, approver_id, status, comment):
    approvals = read_all('approvals.txt', APPROVAL_FIELDS)
    approval_id = get_next_id(approvals, 'approval_id')
    timestamp = datetime.utcnow().isoformat()
    approval = {
        'approval_id': str(approval_id),
        'article_id': str(article_id),
        'version_id': str(version_id),
        'approver_id': str(approver_id),
        'status': status,
        'comment': comment,
        'timestamp': timestamp
    }
    append_line('approvals.txt', approval, APPROVAL_FIELDS)
    return approval


# --- Comment Services ---

def load_comments(article_id, version_id):
    comments = read_all('comments.txt', COMMENT_FIELDS)
    return [c for c in comments if c['article_id'] == str(article_id) and c['version_id'] == str(version_id)]


def add_comment(article_id, version_id, user_id, comment_text):
    comments = read_all('comments.txt', COMMENT_FIELDS)
    comment_id = get_next_id(comments, 'comment_id')
    timestamp = datetime.utcnow().isoformat()
    comment = {
        'comment_id': str(comment_id),
        'article_id': str(article_id),
        'version_id': str(version_id),
        'user_id': str(user_id),
        'comment_text': comment_text,
        'timestamp': timestamp
    }
    append_line('comments.txt', comment, COMMENT_FIELDS)
    return comment


# --- Analytics Services ---

def load_analytics(article_id):
    analytics = read_all('analytics.txt', ANALYTICS_FIELDS)
    article_analytics = [a for a in analytics if a['article_id'] == str(article_id)]
    # Aggregate metrics
    total_views = 0
    total_unique_visitors = 0
    total_time = 0.0
    total_shares = 0
    count = 0
    for entry in article_analytics:
        try:
            total_views += int(entry['views'])
            total_unique_visitors += int(entry['unique_visitors'])
            total_time += float(entry['avg_time_on_article'])
            total_shares += int(entry['shares'])
            count += 1
        except Exception:
            pass
    avg_time = (total_time / count) if count > 0 else 0
    analytics_summary = {
        'total_views': total_views,
        'total_unique_visitors': total_unique_visitors,
        'average_time_on_article': avg_time,
        'total_shares': total_shares,
        'data_points': count
    }
    return analytics_summary


# --- Routes Implementation ---

@app.route('/')
def root():
    # Redirect root to /dashboard
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    if not user:
        # For demo, we redirect to login or just show message
        return redirect(url_for('login'))

    username = user['username']

    # Quick stats and recent activity can be synthesized from articles and analytics
    articles = read_all('articles.txt', ARTICLE_FIELDS)
    user_articles = [a for a in articles if a['author_id'] == user['user_id']]
    recent_activity = []
    # For brevity, recent activity is last 5 updated articles by user
    user_articles_sorted = sorted(user_articles, key=lambda a: a['updated_at'], reverse=True)
    for article in user_articles_sorted[:5]:
        recent_activity.append({
            'title': article['title'],
            'updated_at': article['updated_at']
        })

    quick_stats = {
        'total_articles': len(user_articles),
        'published_articles': sum(1 for a in user_articles if a['status'] == 'published'),
        'draft_articles': sum(1 for a in user_articles if a['status'] == 'draft')
    }

    return render_template('dashboard.html', username=username, quick_stats=quick_stats, recent_activity=recent_activity)


@app.route('/article/create', methods=['GET', 'POST'])
def create_article():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if not title or not content:
            error_message = 'Title and content are required.'
            return render_template('create_article.html', error=error_message)

        new_article = create_article(user['user_id'], title, content)
        return redirect(url_for('edit_article', article_id=new_article['article_id']))

    return render_template('create_article.html')


@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))

    article = load_article(article_id)
    if not article:
        abort(404)

    # Only author can edit
    if article['author_id'] != user['user_id']:
        abort(403)

    versions = load_article_versions(article_id)
    latest_version = versions[-1] if versions else None

    if request.method == 'POST':
        new_content = request.form.get('content', '').strip()
        if not new_content:
            error_message = 'Content must not be empty.'
            return render_template('edit_article.html', article=article, content=latest_version['content'] if latest_version else '', error=error_message)
        new_version = create_new_version(article_id, new_content)
        return redirect(url_for('edit_article', article_id=article_id))

    content = latest_version['content'] if latest_version else ''
    return render_template('edit_article.html', article=article, content=content)


@app.route('/article/<int:article_id>/versions', methods=['GET', 'POST'])
def version_history(article_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))

    article = load_article(article_id)
    if not article:
        abort(404)

    # Only author or approver logic - simplified as author only
    if article['author_id'] != user['user_id']:
        abort(403)

    versions = load_article_versions(article_id)

    comparison = None

    if request.method == 'POST':
        action = request.form.get('action')
        version_number = request.form.get('version_number')
        if action == 'restore':
            # To restore a version, create a new version copying chosen version content
            if not version_number:
                error_message = 'Version number to restore not specified.'
                return render_template('version_history.html', article=article, versions=versions, error=error_message)
            # Find the version
            version_to_restore = None
            for v in versions:
                if v['version_number'] == version_number:
                    version_to_restore = v
                    break
            if not version_to_restore:
                error_message = 'Version not found.'
                return render_template('version_history.html', article=article, versions=versions, error=error_message)
            create_new_version(article_id, version_to_restore['content'])
            return redirect(url_for('version_history', article_id=article_id))
        elif action == 'compare':
            v1_num = request.form.get('version1')
            v2_num = request.form.get('version2')
            # Note: Template uses 'version_number' radio, changed to single select for restore and compare now
            # For compare, require two versions selected (would need checkboxes or JS in UI, simplified here
            # For now, we just fallback to error message
            error_message = 'Comparing versions requires two selections, UI to support not implemented.'
            return render_template('version_history.html', article=article, versions=versions, error=error_message)

    return render_template('version_history.html', article=article, versions=versions, comparison=comparison)


@app.route('/articles/mine')
def my_articles():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))

    articles = read_all('articles.txt', ARTICLE_FIELDS)
    user_articles = [a for a in articles if a['author_id'] == user['user_id']]

    # Filter options via query params - example: ?status=draft
    status_filter = request.args.get('status', 'all')
    if status_filter != 'all':
        user_articles = [a for a in user_articles if a['status'] == status_filter]

    return render_template('my_articles.html', articles=user_articles, filter_status=status_filter)


@app.route('/articles/published')
def published_articles():
    articles = read_all('articles.txt', ARTICLE_FIELDS)
    published = [a for a in articles if a['status'] == 'published']

    # We do not have categories stored in articles, so categories list empty
    categories = ['Technology', 'Business', 'Entertainment']  # Sample categories for UI
    filter_category = request.args.get('category', 'all')
    if filter_category != 'all':
        # Filtering by category in article data is not implemented; skipping
        pass

    sort_by = request.args.get('sort', 'title')
    sort_options = ['title', 'created_at', 'updated_at']
    if sort_by in sort_options:
        published.sort(key=lambda a: a.get(sort_by, ''))

    return render_template('published_articles.html', articles=published, categories=categories, filter_category=filter_category, sort_options=sort_options, sort_by=sort_by)


@app.route('/calendar')
def content_calendar():
    # For simplicity, we aggregate published articles by their created_at date
    articles = read_all('articles.txt', ARTICLE_FIELDS)
    published_articles = [a for a in articles if a['status'] == 'published']

    calendar_events = []
    for art in published_articles:
        calendar_events.append({
            'title': art['title'],
            'date': art['created_at']
        })
    return render_template('content_calendar.html', events=calendar_events)


@app.route('/article/<int:article_id>/analytics')
def article_analytics(article_id):
    article = load_article(article_id)
    if not article:
        abort(404)

    analytics_summary = load_analytics(article_id)

    return render_template('article_analytics.html', article=article, analytics=analytics_summary)


# --- Additional Routes for Comments and Approvals (placeholders) ---

@app.route('/article/<int:article_id>/comments', methods=['GET', 'POST'])
def article_comments(article_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))

    article = load_article(article_id)
    if not article:
        abort(404)

    versions = load_article_versions(article_id)
    latest_version = versions[-1] if versions else None

    if request.method == 'POST':
        comment_text = request.form.get('comment_text', '').strip()
        if not comment_text:
            error_message = 'Comment text cannot be empty.'
            return render_template('article_comments.html', article=article, comments=[], error=error_message)
        add_comment(article_id, latest_version['version_id'], user['user_id'], comment_text)
        return redirect(url_for('article_comments', article_id=article_id))

    comments = load_comments(article_id, latest_version['version_id']) if latest_version else []
    return render_template('article_comments.html', article=article, comments=comments)


@app.route('/article/<int:article_id>/approvals', methods=['GET', 'POST'])
def article_approvals(article_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))

    article = load_article(article_id)
    if not article:
        abort(404)

    versions = load_article_versions(article_id)
    latest_version = versions[-1] if versions else None

    if request.method == 'POST':
        status = request.form.get('status')
        comment = request.form.get('comment', '').strip()
        if status not in ['approved', 'rejected']:
            error_message = 'Invalid approval status.'
            return render_template('article_approvals.html', article=article, approvals=[], error=error_message)
        add_approval(article_id, latest_version['version_id'], user['user_id'], status, comment)
        return redirect(url_for('article_approvals', article_id=article_id))

    approvals = load_approvals(article_id, latest_version['version_id']) if latest_version else []
    return render_template('article_approvals.html', article=article, approvals=approvals)


# --- Login simulation for testing ---
# This route is not specified in architecture.md but needed to test session and user
# Remove or replace with real auth in actual deployment

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            return 'Username required', 400
        # Set session for demo
        session['username'] = username
        return redirect(url_for('dashboard'))
    return 'Login page placeholder. POST username to login.'


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
