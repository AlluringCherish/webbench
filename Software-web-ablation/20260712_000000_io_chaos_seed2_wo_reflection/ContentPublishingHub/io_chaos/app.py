from flask import Flask, request, redirect, url_for, render_template, session, abort
import os
import threading
import datetime
import time

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_here'  # For session management

# Base data directory
DATA_DIR = 'data'

# File paths
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
ARTICLES_FILE = os.path.join(DATA_DIR, 'articles.txt')
ARTICLE_VERSIONS_FILE = os.path.join(DATA_DIR, 'article_versions.txt')
APPROVALS_FILE = os.path.join(DATA_DIR, 'approvals.txt')
COMMENTS_FILE = os.path.join(DATA_DIR, 'comments.txt')
WORKFLOW_STAGES_FILE = os.path.join(DATA_DIR, 'workflow_stages.txt')
ANALYTICS_FILE = os.path.join(DATA_DIR, 'analytics.txt')

# ----------------------------------------------------------------------------
# Utilities for Data File Handling (pipe-delimited files)
# ----------------------------------------------------------------------------

def read_pipe_delimited_file(filepath, field_names):
    """Read a pipe-delimited text file into list of dicts with keys field_names."""
    data = []
    if not os.path.exists(filepath):
        return data
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('|')
            if len(parts) != len(field_names):
                continue  # skip malformed lines
            item = dict(zip(field_names, parts))
            data.append(item)
    return data


def write_pipe_delimited_file(filepath, data, field_names):
    """Write list of dicts to pipe-delimited file atomically."""
    temp_filepath = filepath + '.tmp'
    with open(temp_filepath, 'w', encoding='utf-8') as f:
        for item in data:
            line = '|'.join(item.get(field, '') for field in field_names)
            f.write(line + '\n')
    os.replace(temp_filepath, filepath)

# Concurrency lock for writes
write_lock = threading.Lock()

# ----------------------------------------------------------------------------
# Models
# ----------------------------------------------------------------------------

class UserModel:
    FIELD_NAMES = ['user_id', 'username', 'fullname', 'email', 'role']

    @staticmethod
    def get_all_users():
        return read_pipe_delimited_file(USERS_FILE, UserModel.FIELD_NAMES)

    @staticmethod
    def get_user_by_username(username):
        users = UserModel.get_all_users()
        for u in users:
            if u['username'] == username:
                return u
        return None


class ArticleModel:
    FIELD_NAMES = ['article_id', 'owner_username', 'title', 'category', 'status']

    @staticmethod
    def get_all_articles():
        return read_pipe_delimited_file(ARTICLES_FILE, ArticleModel.FIELD_NAMES)

    @staticmethod
    def save_all_articles(articles):
        with write_lock:
            write_pipe_delimited_file(ARTICLES_FILE, articles, ArticleModel.FIELD_NAMES)

    @staticmethod
    def get_article_by_id(article_id):
        articles = ArticleModel.get_all_articles()
        for art in articles:
            if art['article_id'] == str(article_id):
                return art
        return None

    @staticmethod
    def add_article(article_dict):
        articles = ArticleModel.get_all_articles()
        articles.append(article_dict)
        ArticleModel.save_all_articles(articles)

    @staticmethod
    def update_article(article_id, updates):
        articles = ArticleModel.get_all_articles()
        updated = False
        for art in articles:
            if art['article_id'] == str(article_id):
                art.update(updates)
                updated = True
                break
        if updated:
            ArticleModel.save_all_articles(articles)
        return updated


class ArticleVersionModel:
    FIELD_NAMES = ['version_id', 'article_id', 'version_number', 'content', 'author', 'timestamp', 'change_summary']

    @staticmethod
    def get_all_versions():
        return read_pipe_delimited_file(ARTICLE_VERSIONS_FILE, ArticleVersionModel.FIELD_NAMES)

    @staticmethod
    def save_all_versions(versions):
        with write_lock:
            write_pipe_delimited_file(ARTICLE_VERSIONS_FILE, versions, ArticleVersionModel.FIELD_NAMES)

    @staticmethod
    def get_versions_by_article(article_id):
        versions = ArticleVersionModel.get_all_versions()
        filtered = [v for v in versions if v['article_id'] == str(article_id)]
        filtered.sort(key=lambda v: int(v['version_number']), reverse=False)  # ascending by version_number
        return filtered

    @staticmethod
    def get_latest_version_number(article_id):
        versions = ArticleVersionModel.get_versions_by_article(article_id)
        if not versions:
            return 0
        return max(int(v['version_number']) for v in versions)

    @staticmethod
    def add_version(version_dict):
        versions = ArticleVersionModel.get_all_versions()
        versions.append(version_dict)
        ArticleVersionModel.save_all_versions(versions)

    @staticmethod
    def get_version(article_id, version_number):
        versions = ArticleVersionModel.get_versions_by_article(article_id)
        for v in versions:
            if str(v['version_number']) == str(version_number):
                return v
        return None


class ApprovalModel:
    FIELD_NAMES = ['approval_id', 'article_id', 'version_id', 'approver', 'status', 'comments', 'timestamp']

    @staticmethod
    def get_all_approvals():
        return read_pipe_delimited_file(APPROVALS_FILE, ApprovalModel.FIELD_NAMES)

    @staticmethod
    def save_all_approvals(approvals):
        with write_lock:
            write_pipe_delimited_file(APPROVALS_FILE, approvals, ApprovalModel.FIELD_NAMES)

    @staticmethod
    def get_approvals_by_article_version(article_id, version_id):
        approvals = ApprovalModel.get_all_approvals()
        filtered = [a for a in approvals if a['article_id'] == str(article_id) and a['version_id'] == str(version_id)]
        filtered.sort(key=lambda a: a['timestamp'])
        return filtered

    @staticmethod
    def add_approval(approval_dict):
        approvals = ApprovalModel.get_all_approvals()
        approvals.append(approval_dict)
        ApprovalModel.save_all_approvals(approvals)


class CommentsModel:
    FIELD_NAMES = ['comment_id', 'article_id', 'version_id', 'commenter', 'comment', 'timestamp']

    @staticmethod
    def get_all_comments():
        return read_pipe_delimited_file(COMMENTS_FILE, CommentsModel.FIELD_NAMES)

    @staticmethod
    def save_all_comments(comments):
        with write_lock:
            write_pipe_delimited_file(COMMENTS_FILE, comments, CommentsModel.FIELD_NAMES)

    @staticmethod
    def get_comments_by_article_version(article_id, version_id):
        comments = CommentsModel.get_all_comments()
        filtered = [c for c in comments if c['article_id'] == str(article_id) and c['version_id'] == str(version_id)]
        filtered.sort(key=lambda c: c['timestamp'])
        return filtered

    @staticmethod
    def add_comment(comment_dict):
        comments = CommentsModel.get_all_comments()
        comments.append(comment_dict)
        CommentsModel.save_all_comments(comments)


class WorkflowModel:
    FIELD_NAMES = ['category', 'stage_number', 'stage_name']

    @staticmethod
    def get_all_stages():
        return read_pipe_delimited_file(WORKFLOW_STAGES_FILE, WorkflowModel.FIELD_NAMES)

    @staticmethod
    def get_stages_for_category(category):
        stages = WorkflowModel.get_all_stages()
        filtered = [s for s in stages if s['category'].lower() == category.lower()]
        filtered.sort(key=lambda s: int(s['stage_number']))
        return filtered


class AnalyticsModel:
    FIELD_NAMES = ['article_id', 'views', 'unique_visitors', 'average_time', 'shares']

    @staticmethod
    def get_all_analytics():
        return read_pipe_delimited_file(ANALYTICS_FILE, AnalyticsModel.FIELD_NAMES)

    @staticmethod
    def save_all_analytics(analytics_list):
        with write_lock:
            write_pipe_delimited_file(ANALYTICS_FILE, analytics_list, AnalyticsModel.FIELD_NAMES)

    @staticmethod
    def get_analytics_by_article(article_id):
        analytics = AnalyticsModel.get_all_analytics()
        for record in analytics:
            if record['article_id'] == str(article_id):
                return record
        return None

# ----------------------------------------------------------------------------
# Business Logic Services
# ----------------------------------------------------------------------------

from uuid import uuid4

def generate_id(prefix=''):
    return prefix + str(uuid4().hex)

class ArticleService:
    @staticmethod
    def create_article(owner_username, title, category, status='draft'):
        # Generate new article_id
        articles = ArticleModel.get_all_articles()
        existing_ids = {int(a['article_id']) for a in articles if a['article_id'].isdigit()}
        new_id = max(existing_ids) + 1 if existing_ids else 1

        article_dict = {
            'article_id': str(new_id),
            'owner_username': owner_username,
            'title': title,
            'category': category,
            'status': status
        }
        ArticleModel.add_article(article_dict)

        # Create initial version
        ArticleService.create_version(str(new_id), title_content=title, author=owner_username, change_summary='Initial version')
        return article_dict

    @staticmethod
    def create_version(article_id, title_content, author, change_summary):
        # Generate version_id
        version_id = generate_id('v_')
        # Determine next version number
        last_version_num = ArticleVersionModel.get_latest_version_number(article_id)
        new_version_num = last_version_num + 1
        timestamp = datetime.datetime.utcnow().isoformat()
        version_dict = {
            'version_id': version_id,
            'article_id': str(article_id),
            'version_number': str(new_version_num),
            'content': title_content,
            'author': author,
            'timestamp': timestamp,
            'change_summary': change_summary
        }
        ArticleVersionModel.add_version(version_dict)
        return version_dict

    @staticmethod
    def get_versions(article_id):
        return ArticleVersionModel.get_versions_by_article(article_id)

    @staticmethod
    def get_article(article_id):
        return ArticleModel.get_article_by_id(article_id)

    @staticmethod
    def update_article_status(article_id, new_status):
        return ArticleModel.update_article(article_id, {'status': new_status})

    @staticmethod
    def user_owns_article(username, article_id):
        article = ArticleService.get_article(article_id)
        return article and article['owner_username'] == username

class ApprovalService:
    @staticmethod
    def get_approvals(article_id, version_id):
        return ApprovalModel.get_approvals_by_article_version(article_id, version_id)

    @staticmethod
    def add_approval(article_id, version_id, approver, status, comments):
        approval_id = generate_id('a_')
        timestamp = datetime.datetime.utcnow().isoformat()
        approval_dict = {
            'approval_id': approval_id,
            'article_id': str(article_id),
            'version_id': version_id,
            'approver': approver,
            'status': status,
            'comments': comments,
            'timestamp': timestamp
        }
        ApprovalModel.add_approval(approval_dict)
        return approval_dict

class CommentService:
    @staticmethod
    def get_comments(article_id, version_id):
        return CommentsModel.get_comments_by_article_version(article_id, version_id)

    @staticmethod
    def add_comment(article_id, version_id, commenter, comment):
        comment_id = generate_id('c_')
        timestamp = datetime.datetime.utcnow().isoformat()
        comment_dict = {
            'comment_id': comment_id,
            'article_id': str(article_id),
            'version_id': version_id,
            'commenter': commenter,
            'comment': comment,
            'timestamp': timestamp
        }
        CommentsModel.add_comment(comment_dict)
        return comment_dict

class AnalyticsService:
    @staticmethod
    def get_analytics(article_id):
        record = AnalyticsModel.get_analytics_by_article(article_id)
        if not record:
            # Return default zeros if no analytics found
            return {
                'views': 0,
                'unique_visitors': 0,
                'average_time': 0.0,
                'shares': 0
            }
        # Convert to proper types
        return {
            'views': int(record.get('views', 0)),
            'unique_visitors': int(record.get('unique_visitors', 0)),
            'average_time': float(record.get('average_time', 0.0)),
            'shares': int(record.get('shares', 0))
        }

# ----------------------------------------------------------------------------
# Session & Auth Utilities
# ----------------------------------------------------------------------------

# For this implementation, simulate a logged-in user via session
# In real app, implement login logic

def get_logged_in_username():
    return session.get('username')

@app.before_request
def require_login():
    # For routes that modify data, check session for username
    # Except for static and GET routes that don't require auth
    if request.endpoint is None:
        return
    if request.endpoint in ['static']:
        return
    # Routes requiring login for write actions
    write_routes = ['create_article', 'edit_article']
    if request.method == 'POST' and request.endpoint in write_routes:
        username = get_logged_in_username()
        if not username:
            return redirect(url_for('login'))

# Dummy login route for testing (not in spec but needed for session)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        user = UserModel.get_user_by_username(username)
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "User not found", 403
    return "Login form placeholder"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# ----------------------------------------------------------------------------
# Routes Implementation
# ----------------------------------------------------------------------------

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    username = get_logged_in_username() or 'Guest'

    # Prepare quick stats
    all_articles = ArticleModel.get_all_articles()
    user_articles = [a for a in all_articles if a['owner_username'] == username]
    total_articles = len(user_articles)
    published_articles = len([a for a in user_articles if a['status'] == 'published'])

    # Recent activities: list recent versions by user
    all_versions = ArticleVersionModel.get_all_versions()
    user_versions = [v for v in all_versions if v['author'] == username]
    user_versions.sort(key=lambda v: v['timestamp'], reverse=True)
    recent_activities = user_versions[:5]

    quick_stats = {
        'total_articles': total_articles,
        'published_articles': published_articles,
    }

    context = {
        'username': username,
        'quick_stats': quick_stats,
        'recent_activities': recent_activities
    }
    return render_template('dashboard.html', **context)


@app.route('/article/create', methods=['GET', 'POST'])
def create_article():
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('login'))

    if request.method == 'GET':
        # Render empty form
        return render_template('create_article.html', username=username)

    # POST: create draft article
    title = request.form.get('title', '').strip()
    category = request.form.get('category', '').strip()
    if not title or not category:
        return render_template('create_article.html', username=username, error='Title and Category are required')

    article = ArticleService.create_article(username, title, category, status='draft')

    return redirect(url_for('edit_article', article_id=article['article_id']))


@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('login'))

    article = ArticleService.get_article(str(article_id))
    if not article:
        abort(404)

    # Verify ownership
    if not ArticleService.user_owns_article(username, str(article_id)):
        abort(403)

    if request.method == 'GET':
        # Load latest version content
        versions = ArticleService.get_versions(str(article_id))
        latest_version = versions[-1] if versions else None
        if latest_version:
            content = latest_version['content']
            title = article['title']
        else:
            content = ''
            title = article['title']
        return render_template('edit_article.html', username=username, article=article, article_id=article_id, content=content)

    # POST: save new version
    content = request.form.get('content', '').strip()
    change_summary = request.form.get('change_summary', '').strip()
    if not content:
        # Reload edit page with error
        versions = ArticleService.get_versions(str(article_id))
        latest_version = versions[-1] if versions else None
        error = 'Content cannot be empty'
        return render_template('edit_article.html', username=username, article=article, article_id=article_id, content=content, error=error)

    new_version = ArticleService.create_version(str(article_id), content, username, change_summary or 'Edited content saved')

    # Optionally update article status to pending_review if it's a draft
    if article['status'] == 'draft':
        ArticleService.update_article_status(str(article_id), 'pending_review')

    # Redirect back to edit page or version history
    return redirect(url_for('edit_article', article_id=article_id))


@app.route('/article/<int:article_id>/versions')
def article_version_history(article_id):
    username = get_logged_in_username() or 'Guest'
    article = ArticleService.get_article(str(article_id))
    if not article:
        abort(404)

    versions = ArticleService.get_versions(str(article_id))

    # For each version add approval history and comments
    detailed_versions = []
    for v in versions:
        approvals = ApprovalService.get_approvals(str(article_id), v['version_id'])
        comments = CommentService.get_comments(str(article_id), v['version_id'])
        detailed_versions.append({'version': v, 'approvals': approvals, 'comments': comments})

    context = {
        'username': username,
        'article': article,
        'versions': detailed_versions
    }

    return render_template('version_history.html', **context)


@app.route('/articles/mine')
def my_articles():
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('login'))

    all_articles = ArticleModel.get_all_articles()
    user_articles = [a for a in all_articles if a['owner_username'] == username]

    # Filtering by query parameters
    filter_status = request.args.get('status', '')
    filter_category = request.args.get('category', '')

    if filter_status:
        user_articles = [a for a in user_articles if a['status'] == filter_status]
    if filter_category:
        user_articles = [a for a in user_articles if a['category'] == filter_category]

    # Prepare articles with last_modified date
    articles_with_details = []
    for art in user_articles:
        # Get last version
        versions = ArticleService.get_versions(art['article_id'])
        last_modified = versions[-1]['timestamp'] if versions else 'N/A'
        articles_with_details.append({
            'id': art['article_id'],
            'title': art['title'],
            'status': art['status'],
            'category': art['category'],
            'last_modified': last_modified
        })

    # Get status and category options for filters
    all_articles = ArticleModel.get_all_articles()
    status_options = list({a['status'] for a in all_articles})
    category_options = list({a['category'] for a in all_articles})

    context = {
        'username': username,
        'articles': articles_with_details,
        'filter_status': filter_status,
        'filter_category': filter_category,
        'status_options': status_options,
        'category_options': category_options
    }
    return render_template('my_articles.html', **context)


@app.route('/articles/published')
def published_articles():
    username = get_logged_in_username() or 'Guest'
    all_articles = ArticleModel.get_all_articles()
    published = [a for a in all_articles if a['status'].lower() == 'published']

    # Filtering by category and publication date (date filtering omitted since no publication date in model)
    filter_category = request.args.get('category', '')
    filter_date = request.args.get('publication_date', '')

    if filter_category:
        published = [a for a in published if a['category'] == filter_category]

    # Prepare articles for display
    articles_with_details = []
    for art in published:
        # Publication date not available in model, set to N/A
        articles_with_details.append({
            'id': art['article_id'],
            'title': art['title'],
            'category': art['category'],
            'publication_date': 'N/A',
            'author': art['owner_username']
        })

    # Get category options
    all_articles = ArticleModel.get_all_articles()
    category_options = list({a['category'] for a in all_articles})

    context = {
        'username': username,
        'articles': articles_with_details,
        'filter_category': filter_category,
        'filter_date': filter_date,
        'category_options': category_options
    }
    return render_template('published_articles.html', **context)


@app.route('/calendar')
def content_calendar():
    username = get_logged_in_username() or 'Guest'

    view_option = request.args.get('view_option', 'monthly')

    # Simulate calendar data per view_option
    # Dummy headers and rows for simplicity
    calendar_data = None
    if view_option == 'monthly':
        calendar_data = {
            'headers': ['Week', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'rows': [
                ['1', '', '', 'Article A', '', '', '', ''],
                ['2', '', 'Article B', '', '', 'Article C', '', ''],
            ]
        }
    elif view_option == 'weekly':
        calendar_data = {
            'headers': ['Day', 'Content'],
            'rows': [
                ['Monday', 'Article A'],
                ['Tuesday', 'Article B'],
                ['Wednesday', 'Article C'],
            ]
        }
    elif view_option == 'daily':
        calendar_data = {
            'headers': ['Date', 'Content'],
            'rows': [
                ['2024-01-01', 'Article A'],
                ['2024-01-02', 'Article B'],
                ['2024-01-03', 'Article C'],
            ]
        }

    context = {
        'username': username,
        'view_option': view_option,
        'calendar_data': calendar_data
    }
    return render_template('content_calendar.html', **context)


@app.route('/article/<int:article_id>/analytics')
def article_analytics(article_id):
    username = get_logged_in_username() or 'Guest'
    article = ArticleService.get_article(str(article_id))
    if not article:
        abort(404)

    analytics = AnalyticsService.get_analytics(str(article_id))

    # Map analytics keys to readable names for template
    analytics_metrics = {
        'views': analytics['views'],
        'unique_visitors': analytics['unique_visitors'],
        'average_time_spent': analytics['average_time'],
        'shares': analytics['shares']
    }

    context = {
        'username': username,
        'article': article,
        'analytics_metrics': analytics_metrics
    }
    return render_template('article_analytics.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
