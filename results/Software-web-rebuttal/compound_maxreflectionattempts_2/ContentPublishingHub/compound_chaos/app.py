import os
import threading
import datetime
import functools
from flask import (
    Flask, render_template, request, redirect, url_for, session, abort, flash
)
import uuid

# Utility for concurrency-safe file IO
from utils.file_io import read_file_lines, write_file_lines_atomic

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'devsecret')

DATA_DIR = 'data'

# Thread lock for safe file read/write
file_lock = threading.Lock()

# ----------------------
# Helper functions
# ----------------------

def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated


def parse_pipe_line(line, fields_count):
    parts = line.strip().split('|')
    if len(parts) != fields_count:
        return None
    return [p.strip() for p in parts]


def iso_datetime_now():
    return datetime.datetime.utcnow().isoformat()


# ----------------------
# Models
# ----------------------

class UserModel:
    FILENAME = os.path.join(DATA_DIR, 'users.txt')
    FIELDS = 3  # username|password|other_fields...

    @staticmethod
    def get_all_users():
        with file_lock:
            lines = read_file_lines(UserModel.FILENAME)
        users = {}
        for line in lines:
            parts = parse_pipe_line(line, UserModel.FIELDS)
            if parts:
                username = parts[0]
                password = parts[1]
                users[username] = {'username': username, 'password': password}
        return users

    @staticmethod
    def validate_user(username, password):
        users = UserModel.get_all_users()
        if username in users and users[username]['password'] == password:
            return True
        return False


class ArticleModel:
    FILENAME = os.path.join(DATA_DIR, 'articles.txt')
    FIELDS = 7  # article_id|owner|title|category|status|created_at|updated_at

    @staticmethod
    def read_all():
        with file_lock:
            lines = read_file_lines(ArticleModel.FILENAME)
        articles = {}
        for line in lines:
            parts = parse_pipe_line(line, ArticleModel.FIELDS)
            if parts:
                article_id, owner, title, category, status, created_at, updated_at = parts
                articles[article_id] = {
                    'article_id': article_id,
                    'owner': owner,
                    'title': title,
                    'category': category,
                    'status': status,
                    'created_at': created_at,
                    'updated_at': updated_at
                }
        return articles

    @staticmethod
    def save_all(articles):
        lines = []
        for a in articles.values():
            line = '|'.join([
                a['article_id'], a['owner'], a['title'], a['category'], a['status'], a['created_at'], a['updated_at']
            ])
            lines.append(line)
        with file_lock:
            write_file_lines_atomic(ArticleModel.FILENAME, lines)

    @staticmethod
    def add_article(owner, title, category='Uncategorized'):
        article_id = str(uuid.uuid4())
        created_at = iso_datetime_now()
        new_article = {
            'article_id': article_id,
            'owner': owner,
            'title': title,
            'category': category,
            'status': 'draft',
            'created_at': created_at,
            'updated_at': created_at,
        }
        articles = ArticleModel.read_all()
        articles[article_id] = new_article
        ArticleModel.save_all(articles)
        return new_article

    @staticmethod
    def update_article(article_id, title=None, category=None, status=None):
        articles = ArticleModel.read_all()
        if article_id not in articles:
            return None
        article = articles[article_id]
        updated = False
        if title is not None:
            article['title'] = title
            updated = True
        if category is not None:
            article['category'] = category
            updated = True
        if status is not None:
            article['status'] = status
            updated = True
        if updated:
            article['updated_at'] = iso_datetime_now()
            articles[article_id] = article
            ArticleModel.save_all(articles)
        return article


class VersionModel:
    FILENAME = os.path.join(DATA_DIR, 'article_versions.txt')
    FIELDS = 6  # version_id|article_id|version_number|content|created_at|status

    @staticmethod
    def read_all():
        with file_lock:
            lines = read_file_lines(VersionModel.FILENAME)
        versions = {}
        by_article = {}
        for line in lines:
            parts = parse_pipe_line(line, VersionModel.FIELDS)
            if parts:
                version_id, article_id, version_number, content, created_at, status = parts
                version_number = int(version_number)
                v = {
                    'version_id': version_id,
                    'article_id': article_id,
                    'version_number': version_number,
                    'content': content,
                    'created_at': created_at,
                    'status': status
                }
                versions[version_id] = v
                by_article.setdefault(article_id, []).append(v)
        # sort versions by version_number for each article
        for art_id in by_article:
            by_article[art_id].sort(key=lambda x: x['version_number'])
        return versions, by_article

    @staticmethod
    def save_all(versions):
        # versions is dict by version_id
        lines = []
        for v in versions.values():
            line = '|'.join([
                v['version_id'], v['article_id'], str(v['version_number']), v['content'], v['created_at'], v['status']
            ])
            lines.append(line)
        with file_lock:
            write_file_lines_atomic(VersionModel.FILENAME, lines)

    @staticmethod
    def add_version(article_id, content, status='draft'):
        versions, by_article = VersionModel.read_all()
        existing_versions = by_article.get(article_id, [])
        new_version_number = existing_versions[-1]['version_number'] + 1 if existing_versions else 1
        version_id = f"{article_id}_v{new_version_number}"
        created_at = iso_datetime_now()
        version = {
            'version_id': version_id,
            'article_id': article_id,
            'version_number': new_version_number,
            'content': content,
            'created_at': created_at,
            'status': status
        }
        versions[version_id] = version
        VersionModel.save_all(versions)
        return version

class ApprovalModel:
    FILENAME = os.path.join(DATA_DIR, 'approvals.txt')
    FIELDS = 5  # approval_id|version_id|approver|status|timestamp

    @staticmethod
    def read_all():
        with file_lock:
            lines = read_file_lines(ApprovalModel.FILENAME)
        approvals = {}
        for line in lines:
            parts = parse_pipe_line(line, ApprovalModel.FIELDS)
            if parts:
                approval_id, version_id, approver, status, timestamp = parts
                approvals[approval_id] = {
                    'approval_id': approval_id,
                    'version_id': version_id,
                    'approver': approver,
                    'status': status,
                    'timestamp': timestamp
                }
        return approvals

    @staticmethod
    def save_all(approvals):
        lines = []
        for a in approvals.values():
            line = '|'.join([
                a['approval_id'], a['version_id'], a['approver'], a['status'], a['timestamp']
            ])
            lines.append(line)
        with file_lock:
            write_file_lines_atomic(ApprovalModel.FILENAME, lines)

    @staticmethod
    def add_approval(version_id, approver, status):
        approvals = ApprovalModel.read_all()
        approval_id = f"{version_id}_{approver}"
        timestamp = iso_datetime_now()
        approvals[approval_id] = {
            'approval_id': approval_id,
            'version_id': version_id,
            'approver': approver,
            'status': status,
            'timestamp': timestamp
        }
        ApprovalModel.save_all(approvals)
        return approvals[approval_id]

class CommentModel:
    FILENAME = os.path.join(DATA_DIR, 'comments.txt')
    FIELDS = 6  # comment_id|article_id|version_id|username|content|created_at

    @staticmethod
    def read_all():
        with file_lock:
            lines = read_file_lines(CommentModel.FILENAME)
        comments = {}
        for line in lines:
            parts = parse_pipe_line(line, CommentModel.FIELDS)
            if parts:
                comment_id, article_id, version_id, username, content, created_at = parts
                comments[comment_id] = {
                    'comment_id': comment_id,
                    'article_id': article_id,
                    'version_id': version_id,
                    'username': username,
                    'content': content,
                    'created_at': created_at
                }
        return comments

    @staticmethod
    def save_all(comments):
        lines = []
        for c in comments.values():
            line = '|'.join([
                c['comment_id'], c['article_id'], c['version_id'], c['username'], c['content'], c['created_at']
            ])
            lines.append(line)
        with file_lock:
            write_file_lines_atomic(CommentModel.FILENAME, lines)

    @staticmethod
    def add_comment(article_id, version_id, username, content):
        comments = CommentModel.read_all()
        comment_id = str(uuid.uuid4())
        created_at = iso_datetime_now()
        comment = {
            'comment_id': comment_id,
            'article_id': article_id,
            'version_id': version_id,
            'username': username,
            'content': content,
            'created_at': created_at
        }
        comments[comment_id] = comment
        CommentModel.save_all(comments)
        return comment

class WorkflowModel:
    FILENAME = os.path.join(DATA_DIR, 'workflow_stages.txt')
    FIELDS = 2  # category|stages (comma separated)

    @staticmethod
    def read_all():
        with file_lock:
            lines = read_file_lines(WorkflowModel.FILENAME)
        workflows = {}
        for line in lines:
            parts = parse_pipe_line(line, WorkflowModel.FIELDS)
            if parts:
                category, stages_str = parts
                stages = [s.strip() for s in stages_str.split(',') if s.strip()]
                workflows[category] = stages
        return workflows

class AnalyticsModel:
    FILENAME = os.path.join(DATA_DIR, 'analytics.txt')
    FIELDS = 6  # article_id|version_id|views|unique_visitors|avg_read_time_seconds|shares

    @staticmethod
    def read_all():
        with file_lock:
            lines = read_file_lines(AnalyticsModel.FILENAME)
        analytics = {}
        for line in lines:
            parts = parse_pipe_line(line, AnalyticsModel.FIELDS)
            if parts:
                article_id, version_id, views, uv, art, shares = parts
                analytics_key = (article_id, version_id)
                analytics[analytics_key] = {
                    'views': int(views),
                    'unique_visitors': int(uv),
                    'avg_read_time_seconds': float(art),
                    'shares': int(shares)
                }
        return analytics

# ----------------------
# Services
# ----------------------

from approval_service import ApprovalService
from analytics_service import AnalyticsService
from article_service import ArticleService

# ----------------------
# Routes
# ----------------------

@app.route('/')
def root():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username','').strip()
    password = request.form.get('password','').strip()
    if not username or not password:
        flash('Username and password required','error')
        return redirect(url_for('login'))
    if UserModel.validate_user(username, password):
        session['username'] = username
        next_url = request.args.get('next') or url_for('dashboard')
        return redirect(next_url)
    flash('Invalid username or password','error')
    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    flash('Logged out successfully','info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    username = session['username']
    quick_stats = ArticleService.get_quick_stats(username)
    recent_activity = ArticleService.get_recent_activity(username)
    return render_template('dashboard.html', username=username, quick_stats=quick_stats, recent_activity=recent_activity)

@app.route('/article/create', methods=['GET','POST'])
@login_required
def create_article():
    if request.method == 'GET':
        categories = ArticleService.get_all_categories()
        return render_template('create_article.html', categories=categories)
    # POST
    title = request.form.get('title','').strip()
    content = request.form.get('content','').strip()
    category = request.form.get('category','Uncategorized').strip()
    if not title or not content:
        flash('Title and Content are required','error')
        return redirect(url_for('create_article'))
    username = session['username']
    article = ArticleService.create_article(username, title, content, category)
    flash('Article created successfully','success')
    return redirect(url_for('edit_article', article_id=article['article_id']))

@app.route('/article/<article_id>/edit', methods=['GET','POST'])
@login_required
def edit_article(article_id):
    username = session['username']
    article = ArticleModel.read_all().get(article_id)
    if article is None:
        abort(404)
    if article['owner'] != username:
        abort(403)

    if request.method == 'GET':
        versions = VersionModel.read_all()[1].get(article_id, [])
        latest_version = versions[-1] if versions else None
        return render_template('edit_article.html', article=article, versions=versions, latest_version=latest_version)

    # POST
    title = request.form.get('title','').strip()
    content = request.form.get('content','').strip()
    if not title or not content:
        flash('Title and Content are required','error')
        return redirect(url_for('edit_article', article_id=article_id))

    # Update article with new title if changed
    ArticleModel.update_article(article_id, title=title)

    # Save new version
    ArticleService.create_version(article_id, content)

    flash('Article updated with new version','success')
    return redirect(url_for('edit_article', article_id=article_id))

@app.route('/article/<article_id>/versions', methods=['GET'])
@login_required
def article_version_history(article_id):
    article = ArticleModel.read_all().get(article_id)
    if article is None:
        abort(404)
    versions = VersionModel.read_all()[1].get(article_id, [])
    current_version_num = versions[-1]['version_number'] if versions else 0

    # For comparison, demo pass two latest versions
    compare_versions = versions[-2:] if len(versions) > 1 else versions

    # Create a comparison dict for template
    comparison = None
    if len(compare_versions) == 2:
        old_version = compare_versions[0]
        new_version = compare_versions[1]
        import difflib
        diff = difflib.unified_diff(
            old_version['content'].splitlines(),
            new_version['content'].splitlines(),
            fromfile=f"Version {old_version['version_number']}",
            tofile=f"Version {new_version['version_number']}",
            lineterm=''
        )
        diff_text = '\n'.join(diff)
        comparison = {
            'old_version': old_version,
            'new_version': new_version,
            'diff': diff_text
        }

    return render_template('version_history.html', article=article, versions=versions, comparison=comparison)

@app.route('/articles/mine', methods=['GET'])
@login_required
def my_articles():
    username = session['username']
    status_filter = request.args.get('status', None)
    all_articles = ArticleModel.read_all()
    filtered = [a for a in all_articles.values() if a['owner'] == username]
    if status_filter:
        filtered = [a for a in filtered if a['status'] == status_filter]

    # Provide filter options for statuses
    statuses = sorted(set(a['status'] for a in all_articles.values() if a['owner'] == username))

    return render_template('my_articles.html', articles=filtered, filter_options=statuses, selected_filter=status_filter)

@app.route('/articles/published', methods=['GET'])
def published_articles():
    category_filter = request.args.get('category', None)
    sort_option = request.args.get('sort', 'created_desc')
    all_articles = ArticleModel.read_all()
    published = [a for a in all_articles.values() if a['status'] == 'published']
    if category_filter:
        published = [a for a in published if a['category'] == category_filter]

    # Sorting demo by created_at descending or ascending
    reverse = True if sort_option.endswith('_desc') else False
    key = None
    if 'created' in sort_option:
        key = lambda x: x['created_at']
    elif 'title' in sort_option:
        key = lambda x: x['title'].lower()
    if key:
        published.sort(key=key, reverse=reverse)

    # Extract categories for filter dropdown
    categories = sorted(set(a['category'] for a in all_articles.values()))
    # Define sort options list to provide to template
    sort_options = ['created_asc', 'created_desc', 'title_asc', 'title_desc']

    return render_template('published_articles.html', articles=published, categories=categories, selected_category=category_filter, sort_option=sort_option, sort_options=sort_options, selected_sort=sort_option)

@app.route('/calendar', methods=['GET'])
def content_calendar():
    view_mode = request.args.get('view', 'month')
    # For demo, gather publish dates and events
    all_articles = ArticleModel.read_all()
    versions_by_article = VersionModel.read_all()[1]
    scheduled_events = []
    for article in all_articles.values():
        article_id = article['article_id']
        versions = versions_by_article.get(article_id, [])
        # Use latest approved or published version publish date or similar
        for v in reversed(versions):
            if v['status'] in ('approved','published'):
                # Placeholder: assume publish date stored in content (not defined), use created_at
                scheduled_events.append({
                    'article_id': article_id,
                    'title': article['title'],
                    'date': v['created_at']
                })
                break
    return render_template('content_calendar.html', view_mode=view_mode, scheduled_events=scheduled_events)

@app.route('/article/<article_id>/analytics', methods=['GET'])
@login_required
def article_analytics(article_id):
    article = ArticleModel.read_all().get(article_id)
    if article is None:
        abort(404)
    versions = VersionModel.read_all()[1].get(article_id, [])
    analytics_all = AnalyticsModel.read_all()

    # Aggregate analytics by summing across versions
    aggregated = {
        'views': 0,
        'unique_visitors': 0,
        'avg_read_time_seconds': 0.0,
        'shares': 0
    }
    count_versions = 0
    for v in versions:
        key = (article_id, v['version_id'])
        a = analytics_all.get(key)
        if a:
            aggregated['views'] += a['views']
            aggregated['unique_visitors'] += a['unique_visitors']
            aggregated['avg_read_time_seconds'] += a['avg_read_time_seconds']
            aggregated['shares'] += a['shares']
            count_versions += 1
    if count_versions > 0:
        aggregated['avg_read_time_seconds'] /= count_versions

    # Add empty traffic_by_date for template to avoid errors
    aggregated['traffic_by_date'] = []

    return render_template('article_analytics.html', article=article, analytics_overview=aggregated)

# Approval submit
@app.route('/article/<article_id>/approve', methods=['POST'])
@login_required
def article_approve(article_id):
    username = session['username']
    article = ArticleModel.read_all().get(article_id)
    if article is None:
        abort(404)
    status = request.form.get('status','').strip()
    if status not in ('approved', 'rejected', 'revision_requested'):
        flash('Invalid approval status','error')
        return redirect(url_for('edit_article', article_id=article_id))

    versions = VersionModel.read_all()[1].get(article_id, [])
    if not versions:
        flash('No versions found to approve','error')
        return redirect(url_for('edit_article', article_id=article_id))
    latest_version = versions[-1]
    version_id = latest_version['version_id']

    ApprovalModel.add_approval(version_id, username, status)

    # Evaluate aggregate approval status
    ApprovalService.update_version_status(article_id, version_id)

    flash('Approval status updated','success')
    return redirect(url_for('article_version_history', article_id=article_id))

# Add comment
@app.route('/article/<article_id>/comment', methods=['POST'])
@login_required
def article_comment(article_id):
    username = session['username']
    article = ArticleModel.read_all().get(article_id)
    if article is None:
        abort(404)
    content = request.form.get('content','').strip()
    version_id = request.form.get('version_id','').strip()
    if not content or not version_id:
        flash('Comment content and version required','error')
        return redirect(url_for('article_version_history', article_id=article_id))

    CommentModel.add_comment(article_id, version_id, username, content)

    flash('Comment added','success')
    return redirect(url_for('article_version_history', article_id=article_id))


if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(debug=True)
