from flask import Flask, request, render_template, session, redirect, url_for, abort
from datetime import datetime
import os
import threading

app = Flask(__name__)
app.secret_key = 'replace_this_with_a_secret_key'

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# File paths
ARTICLE_FILE = os.path.join(DATA_DIR, 'articles.txt')
ARTICLE_VERSIONS_FILE = os.path.join(DATA_DIR, 'article_versions.txt')
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
APPROVALS_FILE = os.path.join(DATA_DIR, 'approvals.txt')
COMMENTS_FILE = os.path.join(DATA_DIR, 'comments.txt')
ANALYTICS_FILE = os.path.join(DATA_DIR, 'analytics.txt')
WORKFLOW_STAGES_FILE = os.path.join(DATA_DIR, 'workflow_stages.txt')

_file_lock = threading.Lock()

# --- Utility functions ---
def _atomic_write(filepath, lines):
    """Write lines to a file atomically."""
    temp_path = filepath + '.tmp'
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    os.replace(temp_path, filepath)


def parse_pipe_line(line, num_fields):
    parts = line.rstrip('\n').split('|')
    if len(parts) != num_fields:
        return None
    return parts


def load_file_lines(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.readlines()


def write_file_lines(filepath, lines):
    with _file_lock:
        _atomic_write(filepath, lines)


# --- Data Access Objects (DAO) ---

# Articles: article_id|title|author|status|category|created_timestamp|last_updated_timestamp


def read_all_articles():
    lines = load_file_lines(ARTICLE_FILE)
    articles = []
    for line in lines:
        parts = parse_pipe_line(line, 7)
        if parts:
            article = {
                'article_id': parts[0],
                'title': parts[1],
                'author': parts[2],
                'status': parts[3],
                'category': parts[4],
                'created_timestamp': parts[5],
                'last_updated_timestamp': parts[6]
            }
            articles.append(article)
    return articles


def write_articles(articles):
    lines = []
    for a in articles:
        line = '|'.join([
            a['article_id'], a['title'], a['author'], a['status'], a['category'],
            a['created_timestamp'], a['last_updated_timestamp']]) + '\n'
        lines.append(line)
    write_file_lines(ARTICLE_FILE, lines)


def find_article(article_id):
    articles = read_all_articles()
    for a in articles:
        if a['article_id'] == str(article_id):
            return a
    return None


def add_article(article):
    articles = read_all_articles()
    articles.append(article)
    write_articles(articles)


def update_article(article):
    articles = read_all_articles()
    for idx, a in enumerate(articles):
        if a['article_id'] == article['article_id']:
            articles[idx] = article
            write_articles(articles)
            return True
    return False


# Article Versions: version_id|article_id|version_number|content|author|timestamp|change_summary

def read_all_versions():
    lines = load_file_lines(ARTICLE_VERSIONS_FILE)
    versions = []
    for line in lines:
        parts = parse_pipe_line(line, 7)
        if parts:
            version = {
                'version_id': parts[0],
                'article_id': parts[1],
                'version_number': int(parts[2]),
                'content': parts[3],
                'author': parts[4],
                'timestamp': parts[5],
                'change_summary': parts[6]
            }
            versions.append(version)
    return versions


def write_versions(versions):
    lines = []
    for v in versions:
        line = '|'.join([
            v['version_id'], v['article_id'], str(v['version_number']), v['content'], v['author'], v['timestamp'], v['change_summary']
        ]) + '\n'
        lines.append(line)
    write_file_lines(ARTICLE_VERSIONS_FILE, lines)


def find_versions_by_article(article_id):
    versions = read_all_versions()
    return [v for v in versions if v['article_id'] == str(article_id)]


def find_latest_version(article_id):
    versions = find_versions_by_article(article_id)
    if not versions:
        return None
    return max(versions, key=lambda v: v['version_number'])


def add_version(version):
    versions = read_all_versions()
    versions.append(version)
    write_versions(versions)


# Approvals: approval_id|article_id|version_id|approver_username|status|comments|timestamp

def read_all_approvals():
    lines = load_file_lines(APPROVALS_FILE)
    approvals = []
    for line in lines:
        parts = parse_pipe_line(line, 7)
        if parts:
            approval = {
                'approval_id': parts[0],
                'article_id': parts[1],
                'version_id': parts[2],
                'approver_username': parts[3],
                'status': parts[4],
                'comments': parts[5],
                'timestamp': parts[6]
            }
            approvals.append(approval)
    return approvals


def write_approvals(approvals):
    lines = []
    for a in approvals:
        line = '|'.join([
            a['approval_id'], a['article_id'], a['version_id'], a['approver_username'],
            a['status'], a['comments'], a['timestamp']]) + '\n'
        lines.append(line)
    write_file_lines(APPROVALS_FILE, lines)


def find_approvals_by_article_version(article_id, version_id):
    approvals = read_all_approvals()
    return [a for a in approvals if a['article_id'] == str(article_id) and a['version_id'] == str(version_id)]


def add_approval(approval):
    approvals = read_all_approvals()
    approvals.append(approval)
    write_approvals(approvals)


# Comments: comment_id|article_id|version_id|commenter_username|comment_text|timestamp

def read_all_comments():
    lines = load_file_lines(COMMENTS_FILE)
    comments = []
    for line in lines:
        parts = parse_pipe_line(line, 6)
        if parts:
            comment = {
                'comment_id': parts[0],
                'article_id': parts[1],
                'version_id': parts[2],
                'commenter_username': parts[3],
                'comment_text': parts[4],
                'timestamp': parts[5]
            }
            comments.append(comment)
    return comments


def write_comments(comments):
    lines = []
    for c in comments:
        line = '|'.join([
            c['comment_id'], c['article_id'], c['version_id'], c['commenter_username'],
            c['comment_text'], c['timestamp']]) + '\n'
        lines.append(line)
    write_file_lines(COMMENTS_FILE, lines)


def find_comments_by_article_version(article_id, version_id):
    comments = read_all_comments()
    return [c for c in comments if c['article_id'] == str(article_id) and c['version_id'] == str(version_id)]


def add_comment(comment):
    comments = read_all_comments()
    comments.append(comment)
    write_comments(comments)


# Analytics: analytics_id|article_id|views|unique_visitors|average_time_seconds|shares

def read_all_analytics():
    lines = load_file_lines(ANALYTICS_FILE)
    analytics = []
    for line in lines:
        parts = parse_pipe_line(line, 6)
        if parts:
            stat = {
                'analytics_id': parts[0],
                'article_id': parts[1],
                'views': int(parts[2]),
                'unique_visitors': int(parts[3]),
                'average_time_seconds': float(parts[4]),
                'shares': int(parts[5])
            }
            analytics.append(stat)
    return analytics


def find_analytics_by_article(article_id):
    analytics = read_all_analytics()
    return [a for a in analytics if a['article_id'] == str(article_id)]


def add_or_update_analytics(new_analytic):
    analytics = read_all_analytics()
    updated = False
    for idx, a in enumerate(analytics):
        if a['article_id'] == new_analytic['article_id']:
            # Aggregate by summing/updating
            analytics[idx]['views'] += new_analytic['views']
            analytics[idx]['unique_visitors'] += new_analytic['unique_visitors']
            # For average_time_seconds, average weighted by views
            total_views = analytics[idx]['views']
            existing_avg = analytics[idx]['average_time_seconds']
            new_avg = new_analytic['average_time_seconds']
            weighted_avg = ((existing_avg * (total_views - new_analytic['views'])) + (new_avg * new_analytic['views'])) / total_views if total_views > 0 else 0
            analytics[idx]['average_time_seconds'] = weighted_avg
            analytics[idx]['shares'] += new_analytic['shares']
            updated = True
            break
    if not updated:
        analytics.append(new_analytic)
    write_analytics(analytics)


def write_analytics(analytics):
    lines = []
    for a in analytics:
        line = '|'.join([
            a['analytics_id'], a['article_id'], str(a['views']), str(a['unique_visitors']),
            f'{a["average_time_seconds"]:.2f}', str(a['shares'])
        ]) + '\n'
        lines.append(line)
    write_file_lines(ANALYTICS_FILE, lines)


# Workflow Stages: stage_id|category|stage_name|sequence_order

def read_workflow_stages():
    lines = load_file_lines(WORKFLOW_STAGES_FILE)
    stages = []
    for line in lines:
        parts = parse_pipe_line(line, 4)
        if parts:
            stage = {
                'stage_id': parts[0],
                'category': parts[1],
                'stage_name': parts[2],
                'sequence_order': int(parts[3])
            }
            stages.append(stage)
    return stages


def find_stages_by_category(category):
    stages = read_workflow_stages()
    return sorted([s for s in stages if s['category'] == category], key=lambda s: s['sequence_order'])


# --- Helpers ---
import uuid

def generate_id():
    return str(uuid.uuid4())


def current_timestamp():
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


def login_required():
    if 'username' not in session:
        return False
    return True


def get_current_user():
    return session.get('username') if 'username' in session else None


# --- Route Handlers ---

@app.route('/')
def root():
    # Redirect to /dashboard
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = get_current_user()
    if not username:
        # Could redirect to login, but specs do not mention login route
        # So just show unauthorized
        return "Unauthorized - please login", 401
    return render_template('dashboard.html', username=username)


@app.route('/article/create', methods=['GET', 'POST'])
def create_article():
    username = get_current_user()
    if not username:
        return "Unauthorized - please login", 401

    if request.method == 'GET':
        return render_template('create_article.html')

    # POST to create a new article draft
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    category = request.form.get('category', '').strip()

    if not title or not content or not category:
        error = 'Title, content, and category are required.'
        return render_template('create_article.html', error=error)

    # Create new article with draft status
    new_article_id = generate_id()
    timestamp = current_timestamp()
    article = {
        'article_id': new_article_id,
        'title': title,
        'author': username,
        'status': 'draft',
        'category': category,
        'created_timestamp': timestamp,
        'last_updated_timestamp': timestamp
    }
    add_article(article)

    # Add first version
    version = {
        'version_id': generate_id(),
        'article_id': new_article_id,
        'version_number': 1,
        'content': content,
        'author': username,
        'timestamp': timestamp,
        'change_summary': 'Initial draft'
    }
    add_version(version)

    return redirect(url_for('edit_article', article_id=new_article_id))


@app.route('/article/<article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    username = get_current_user()
    if not username:
        return "Unauthorized - please login", 401

    article = find_article(article_id)
    if article is None:
        abort(404)

    if article['author'] != username:
        return "Forbidden - you are not the author of this article", 403

    if request.method == 'GET':
        # Fetch latest version content
        version = find_latest_version(article_id)
        content = version['content'] if version else ''
        return render_template('edit_article.html', article=article, content=content)

    # POST update: create a new version with updated content and change summary
    content = request.form.get('content', '').strip()
    change_summary = request.form.get('change_summary', '').strip()

    if not content or not change_summary:
        error = 'Content and change summary are required.'
        return render_template('edit_article.html', article=article, content=content, error=error)

    # Get next version number
    existing_versions = find_versions_by_article(article_id)
    next_version_num = max([v['version_number'] for v in existing_versions]) + 1 if existing_versions else 1

    version = {
        'version_id': generate_id(),
        'article_id': article_id,
        'version_number': next_version_num,
        'content': content,
        'author': username,
        'timestamp': current_timestamp(),
        'change_summary': change_summary
    }
    add_version(version)

    # Update article last updated timestamp
    article['last_updated_timestamp'] = version['timestamp']
    update_article(article)

    return redirect(url_for('edit_article', article_id=article_id))


@app.route('/article/<article_id>/versions')
def version_history(article_id):
    username = get_current_user()
    if not username:
        return "Unauthorized - please login", 401

    article = find_article(article_id)
    if article is None:
        abort(404)

    if article['author'] != username:
        return "Forbidden - you are not the author of this article", 403

    versions = find_versions_by_article(article_id)
    versions_sorted = sorted(versions, key=lambda v: v['version_number'], reverse=True)

    return render_template('version_history.html', article=article, versions=versions_sorted)


@app.route('/articles/mine')
def my_articles():
    username = get_current_user()
    if not username:
        return "Unauthorized - please login", 401

    articles = read_all_articles()
    user_articles = [a for a in articles if a['author'] == username]

    return render_template('my_articles.html', articles=user_articles)


@app.route('/articles/published')
def published_articles():
    # Show all articles with status 'approved'
    articles = read_all_articles()
    published = [a for a in articles if a['status'] == 'approved']
    return render_template('published_articles.html', articles=published)


@app.route('/calendar')
def content_calendar():
    # Fetch scheduled publication data
    # For simplicity assume status 'approved' articles have scheduled publication in created_timestamp
    articles = read_all_articles()
    scheduled = [a for a in articles if a['status'] == 'approved']
    return render_template('content_calendar.html', articles=scheduled)


@app.route('/article/<article_id>/analytics')
def article_analytics(article_id):
    article = find_article(article_id)
    if article is None:
        abort(404)

    analytics_list = find_analytics_by_article(article_id)

    # Aggregate simple metrics
    total_views = sum(a['views'] for a in analytics_list)
    total_unique_visitors = sum(a['unique_visitors'] for a in analytics_list)
    if total_views > 0:
        avg_time = sum(a['average_time_seconds'] * a['views'] for a in analytics_list) / total_views
    else:
        avg_time = 0.0
    total_shares = sum(a['shares'] for a in analytics_list)

    analytics_summary = {
        'total_views': total_views,
        'total_unique_visitors': total_unique_visitors,
        'average_time_seconds': avg_time,
        'total_shares': total_shares
    }

    return render_template('article_analytics.html', article=article, analytics=analytics_summary)


if __name__ == '__main__':
    app.run(debug=True)
