import os
import threading
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, abort, flash

# File paths (relative to this file)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
ARTICLES_FILE = os.path.join(DATA_DIR, 'articles.txt')
ARTICLE_VERSIONS_FILE = os.path.join(DATA_DIR, 'article_versions.txt')
APPROVALS_FILE = os.path.join(DATA_DIR, 'approvals.txt')
WORKFLOW_STAGES_FILE = os.path.join(DATA_DIR, 'workflow_stages.txt')
COMMENTS_FILE = os.path.join(DATA_DIR, 'comments.txt')
ANALYTICS_FILE = os.path.join(DATA_DIR, 'analytics.txt')

# Flask app initialization
app = Flask(__name__)
app.secret_key = 'YOUR_SECRET_KEY_HERE_CHANGE_ME'

# --- Utility functions ---

# A lock for data file writes to avoid concurrency issues
write_lock = threading.Lock()

def read_pipe_delimited_file(filepath):
    data = []
    if not os.path.exists(filepath):
        return data
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            data.append(fields)
    return data

def append_pipe_delimited_file(filepath, fields):
    line = '|'.join(str(x) for x in fields) + '\n'
    # concurrency safe append with lock
    with write_lock:
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(line)

def write_pipe_delimited_file(filepath, lines):
    # lines = list of lists
    tmpfile = filepath + '.tmp'
    with write_lock:
        with open(tmpfile, 'w', encoding='utf-8') as f:
            for fields in lines:
                line = '|'.join(str(x) for x in fields) + '\n'
                f.write(line)
        os.replace(tmpfile, filepath)


def generate_new_id(existing_ids):
    # Assumes numeric IDs
    max_id = 0
    for id_ in existing_ids:
        try:
            max_id = max(max_id, int(id_))
        except Exception:
            pass
    return max_id + 1


def parse_datetime(dt_str):
    # Attempt isoformat parsing fallback
    try:
        return datetime.fromisoformat(dt_str)
    except Exception:
        try:
            return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        except Exception:
            return None

def serialize_datetime(dt):
    if not dt:
        return ''
    return dt.isoformat(sep=' ', timespec='seconds')

# --- Data Model classes ---

# Users have minimal usage here - username is primary key
# For demo, assume users.txt: user_id|username|full_name|email|role
class User:
    fields = ['user_id', 'username', 'full_name', 'email', 'role']

    @staticmethod
    def load_all():
        users = {}
        rows = read_pipe_delimited_file(USERS_FILE)
        for row in rows:
            if len(row) < 5:
                continue
            user = dict(zip(User.fields, row))
            users[user['username']] = user
        return users

    @staticmethod
    def get(username):
        return User.load_all().get(username)


# Articles: article_id|author|title|category|status|publication_date
# status: draft, pending_review, under_review, approved, rejected, published, etc.
class Article:
    fields = ['article_id', 'author', 'title', 'category', 'status', 'publication_date']

    @staticmethod
    def load_all():
        articles = {}
        rows = read_pipe_delimited_file(ARTICLES_FILE)
        for row in rows:
            if len(row) < 6:
                continue
            article = dict(zip(Article.fields, row))
            articles[int(article['article_id'])] = article
        return articles

    @staticmethod
    def save_all(articles_dict):
        # articles_dict keyed by article_id int
        lines = []
        for article_id in sorted(articles_dict.keys()):
            art = articles_dict[article_id]
            lines.append([art['article_id'], art['author'], art['title'], art['category'], art['status'], art['publication_date']])
        write_pipe_delimited_file(ARTICLES_FILE, lines)

    @staticmethod
    def get(article_id):
        return Article.load_all().get(article_id)

    @staticmethod
    def append(article_dict):
        append_pipe_delimited_file(ARTICLES_FILE, [article_dict['article_id'], article_dict['author'], article_dict['title'], article_dict['category'], article_dict['status'], article_dict['publication_date']])


# Article Versions: version_id|article_id|version_number|content|author|timestamp
class ArticleVersion:
    fields = ['version_id', 'article_id', 'version_number', 'content', 'author', 'timestamp']

    @staticmethod
    def load_all():
        versions = []
        rows = read_pipe_delimited_file(ARTICLE_VERSIONS_FILE)
        for row in rows:
            if len(row) < 6:
                continue
            v = dict(zip(ArticleVersion.fields, row))
            # Convert ints
            try:
                v['version_id'] = int(v['version_id'])
                v['article_id'] = int(v['article_id'])
                v['version_number'] = int(v['version_number'])
            except Exception:
                continue
            versions.append(v)
        return versions

    @staticmethod
    def save_new_version(article_id, content, author):
        versions = ArticleVersion.load_all()
        # filter versions by article_id
        filtered = [v for v in versions if v['article_id'] == article_id]
        max_version = max((v['version_number'] for v in filtered), default=0)
        new_version_number = max_version + 1
        existing_ids = [v['version_id'] for v in versions]
        new_version_id = generate_new_id(existing_ids)
        timestamp = serialize_datetime(datetime.utcnow())
        new_version = {
            'version_id': new_version_id,
            'article_id': article_id,
            'version_number': new_version_number,
            'content': content,
            'author': author,
            'timestamp': timestamp
        }
        append_pipe_delimited_file(ARTICLE_VERSIONS_FILE, [new_version['version_id'], new_version['article_id'], new_version['version_number'], new_version['content'], new_version['author'], new_version['timestamp']])
        return new_version

    @staticmethod
    def get_versions_by_article(article_id):
        versions = ArticleVersion.load_all()
        return sorted([v for v in versions if v['article_id'] == article_id], key=lambda x: x['version_number'])

    @staticmethod
    def get_latest_version(article_id):
        versions = ArticleVersion.load_all()
        filtered = [v for v in versions if v['article_id'] == article_id]
        if not filtered:
            return None
        latest = max(filtered, key=lambda x: x['version_number'])
        return latest

    @staticmethod
    def get_version_by_number(article_id, version_number):
        versions = ArticleVersion.load_all()
        for v in versions:
            if v['article_id'] == article_id and v['version_number'] == version_number:
                return v
        return None

# Approvals: approval_id|article_id|version_id|approver|status|comments|timestamp
class Approval:
    fields = ['approval_id', 'article_id', 'version_id', 'approver', 'status', 'comments', 'timestamp']

    @staticmethod
    def load_all():
        approvals = []
        rows = read_pipe_delimited_file(APPROVALS_FILE)
        for row in rows:
            if len(row) < 7:
                continue
            a = dict(zip(Approval.fields, row))
            try:
                a['approval_id'] = int(a['approval_id'])
                a['article_id'] = int(a['article_id'])
                a['version_id'] = int(a['version_id'])
            except Exception:
                continue
            approvals.append(a)
        return approvals

    @staticmethod
    def append_approval(article_id, version_id, approver, status, comments):
        approvals = Approval.load_all()
        existing_ids = [a['approval_id'] for a in approvals]
        new_approval_id = generate_new_id(existing_ids)
        timestamp = serialize_datetime(datetime.utcnow())
        approval_record = [new_approval_id, article_id, version_id, approver, status, comments, timestamp]
        append_pipe_delimited_file(APPROVALS_FILE, approval_record)
        return approval_record

    @staticmethod
    def get_approvals_by_article_version(article_id, version_id):
        approvals = Approval.load_all()
        return [a for a in approvals if a['article_id'] == article_id and a['version_id'] == version_id]

# Workflow Stages: category|stage_number|stage_name|required_approver_roles
# required_approver_roles: comma separated e.g., editor,reviewer
class WorkflowStage:
    fields = ['category', 'stage_number', 'stage_name', 'required_approver_roles']

    @staticmethod
    def load_all():
        stages = {}
        rows = read_pipe_delimited_file(WORKFLOW_STAGES_FILE)
        for row in rows:
            if len(row) < 4:
                continue
            cat, stage_num_str, stage_name, roles_str = row[:4]
            try:
                stage_num = int(stage_num_str)
            except Exception:
                continue
            roles = [r.strip() for r in roles_str.split(',')] if roles_str else []
            if cat not in stages:
                stages[cat] = []
            stages[cat].append({'stage_number': stage_num, 'stage_name': stage_name, 'required_approver_roles': roles})
        # sort stages by stage_number
        for cat in stages:
            stages[cat].sort(key=lambda s: s['stage_number'])
        return stages


# Comments: comment_id|version_id|user|timestamp|comment_text
class Comment:
    fields = ['comment_id', 'version_id', 'user', 'timestamp', 'comment_text']

    @staticmethod
    def load_all():
        comments = []
        rows = read_pipe_delimited_file(COMMENTS_FILE)
        for row in rows:
            if len(row) < 5:
                continue
            c = dict(zip(Comment.fields, row))
            try:
                c['comment_id'] = int(c['comment_id'])
                c['version_id'] = int(c['version_id'])
            except Exception:
                continue
            comments.append(c)
        return comments

    @staticmethod
    def append_comment(version_id, user, comment_text):
        comments = Comment.load_all()
        existing_ids = [c['comment_id'] for c in comments]
        new_comment_id = generate_new_id(existing_ids)
        timestamp = serialize_datetime(datetime.utcnow())
        comment_record = [new_comment_id, version_id, user, timestamp, comment_text]
        append_pipe_delimited_file(COMMENTS_FILE, comment_record)
        return comment_record

    @staticmethod
    def get_comments_by_version(version_id):
        comments = Comment.load_all()
        return [c for c in comments if c['version_id'] == version_id]

# Analytics: analytic_id|article_id|views|unique_visitors|avg_time_sec|shares|timestamp
class Analytics:
    fields = ['analytic_id', 'article_id', 'views', 'unique_visitors', 'avg_time_sec', 'shares', 'timestamp']

    @staticmethod
    def load_all():
        analytics = []
        rows = read_pipe_delimited_file(ANALYTICS_FILE)
        for row in rows:
            if len(row) < 7:
                continue
            a = dict(zip(Analytics.fields, row))
            try:
                a['analytic_id'] = int(a['analytic_id'])
                a['article_id'] = int(a['article_id'])
                a['views'] = int(a['views'])
                a['unique_visitors'] = int(a['unique_visitors'])
                a['avg_time_sec'] = float(a['avg_time_sec'])
                a['shares'] = int(a['shares'])
                a['timestamp'] = a['timestamp']
            except Exception:
                continue
            analytics.append(a)
        return analytics

    @staticmethod
    def get_analytics_by_article(article_id):
        analytics = Analytics.load_all()
        filtered = [a for a in analytics if a['article_id'] == article_id]
        return filtered

# --- Version control utilities ---

def generate_diff(content_a, content_b):
    # Simple line diff representation
    import difflib
    lines_a = content_a.splitlines()
    lines_b = content_b.splitlines()
    diff = difflib.unified_diff(lines_a, lines_b, lineterm='', fromfile='Version A', tofile='Version B')
    return '\n'.join(diff)

# --- Authentication Helpers (very minimal for demonstration) ---

def login_required(f):
    from functools import wraps
    def wrapped(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return wraps(f)(wrapped)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        users = User.load_all()
        if username in users:
            session['username'] = username
            next_url = request.args.get('next') or url_for('dashboard')
            return redirect(next_url)
        else:
            flash('Invalid username')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- Routes implementation ---

@app.route('/')
def root():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    username = session['username']
    return render_template('dashboard.html', username=username)


@app.route('/article/create', methods=['GET', 'POST'])
@login_required
def create_article():
    username = session['username']
    errors = {}
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', '').strip()
        if not title:
            errors['title'] = 'Title is required.'
        if not content:
            errors['content'] = 'Content is required.'
        if not category:
            errors['category'] = 'Category is required.'
        if errors:
            return render_template('article_create.html', errors=errors, form_data=request.form)

        # Create new article
        articles = Article.load_all()
        existing_ids = list(articles.keys())
        new_article_id = generate_new_id(existing_ids)
        article_dict = {
            'article_id': str(new_article_id),
            'author': username,
            'title': title,
            'category': category,
            'status': 'draft',
            'publication_date': ''
        }
        # Append to articles.txt
        Article.append(article_dict)
        # Create initial version
        ArticleVersion.save_new_version(new_article_id, content, username)
        flash('Article created successfully.')
        return redirect(url_for('edit_article', article_id=new_article_id))
    return render_template('article_create.html')


@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    username = session['username']
    article = Article.get(article_id)
    if not article:
        abort(404)
    if article['author'] != username:
        abort(403)  # authors only edit own articles

    errors = {}
    current_version = ArticleVersion.get_latest_version(article_id)
    if request.method == 'POST':
        # Accept new content and update version
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', '').strip()
        status = request.form.get('status', article['status'])

        if not title:
            errors['title'] = 'Title is required.'
        if not content:
            errors['content'] = 'Content is required.'
        if not category:
            errors['category'] = 'Category is required.'

        if errors:
            return render_template('article_edit.html', article_id=article_id, article=article, current_version=current_version, errors=errors, form_data=request.form)
        # Update article metadata
        articles = Article.load_all()
        art = articles.get(article_id)
        art['title'] = title
        art['category'] = category
        art['status'] = status
        # Update publication_date if status=published
        if status == 'published' and not art['publication_date']:
            art['publication_date'] = serialize_datetime(datetime.utcnow())
        Article.save_all(articles)

        # Save new version
        new_version = ArticleVersion.save_new_version(article_id, content, username)

        flash('Article updated successfully.')
        return redirect(url_for('edit_article', article_id=article_id))

    # GET
    return render_template('article_edit.html', article_id=article_id, article=article, current_version=current_version)


@app.route('/article/<int:article_id>/versions', methods=['GET'])
@login_required
def version_history(article_id):
    username = session['username']
    article = Article.get(article_id)
    if not article:
        abort(404)
    # Authorization: authors see their articles, others depending status?
    # For simplicity, let's allow only authors and users with approval roles (in session) to view
    # We check if user is author or in approval roles for article category
    user = User.get(username)
    if not user:
        abort(403)

    if article['author'] != username:
        # Check if user role in approval roles
        stages = WorkflowStage.load_all()
        cat_stages = stages.get(article['category'], [])
        needed_roles = set()
        for stage in cat_stages:
            needed_roles.update(stage['required_approver_roles'])
        if user['role'] not in needed_roles:
            abort(403)

    versions = ArticleVersion.get_versions_by_article(article_id)

    # Optional query params: selected_version, compare_version
    selected_version_num = request.args.get('selected_version', type=int)
    compare_version_num = request.args.get('compare_version', type=int)

    selected_version = None
    comparison_result = None

    if selected_version_num:
        selected_version = ArticleVersion.get_version_by_number(article_id, selected_version_num)

    if selected_version_num and compare_version_num:
        version_a = ArticleVersion.get_version_by_number(article_id, selected_version_num)
        version_b = ArticleVersion.get_version_by_number(article_id, compare_version_num)
        if version_a and version_b:
            comparison_result = generate_diff(version_a['content'], version_b['content'])

    return render_template('article_versions.html', article_id=article_id, versions=versions, selected_version=selected_version, comparison_result=comparison_result)


@app.route('/articles/mine', methods=['GET'])
@login_required
def my_articles():
    username = session['username']
    status_filter = request.args.get('status', '').strip().lower()
    articles = Article.load_all()
    filtered = [a for a in articles.values() if a['author'] == username]
    if status_filter:
        filtered = [a for a in filtered if a['status'].lower() == status_filter]
    # sort by article_id descending
    filtered = sorted(filtered, key=lambda x: int(x['article_id']), reverse=True)

    # Add last_modified field by deriving from latest version timestamp
    versions = ArticleVersion.load_all()
    latest_versions = {}
    for v in versions:
        aid = v['article_id']
        if aid not in latest_versions or v['version_number'] > latest_versions[aid]['version_number']:
            latest_versions[aid] = v
    for art in filtered:
        v = latest_versions.get(int(art['article_id']))
        art['last_modified'] = v['timestamp'] if v else ''

    return render_template('my_articles.html', username=username, articles=filtered, status_filter=status_filter)


@app.route('/articles/published', methods=['GET'])
def published_articles():
    category_filter = request.args.get('category', '').strip()
    sort_option = request.args.get('sort', '').strip()
    articles = Article.load_all()
    # Filter published only
    published = [a for a in articles.values() if a['status'] == 'published']
    if category_filter:
        published = [a for a in published if a['category'] == category_filter]

    # Load analytics for views sorting
    analytics = Analytics.load_all()
    analytics_by_article = {}
    for a in analytics:
        analytics_by_article.setdefault(a['article_id'], []).append(a)

    def total_views(art):
        recs = analytics_by_article.get(int(art['article_id']), [])
        return sum(r['views'] for r in recs)

    # Sorting: by publication_date desc (date), total views desc (popularity), or default by article_id
    if sort_option == 'date':
        published.sort(key=lambda x: x['publication_date'] or '', reverse=True)
    elif sort_option == 'popularity':
        published.sort(key=total_views, reverse=True)
    else:
        published.sort(key=lambda x: int(x['article_id']), reverse=True)

    # Add published_date and views fields for template
    for art in published:
        art['published_date'] = art['publication_date']
        art['views'] = total_views(art)

    return render_template('published_articles.html', articles=published, category_filter=category_filter, sort_option=sort_option)


@app.route('/calendar', methods=['GET', 'POST'])
@login_required
def content_calendar():
    username = session['username']
    scheduled_articles = []
    calendar_view = request.args.get('view', 'month')
    if request.method == 'POST':
        # For scheduling articles: expecting form data article_id and publication_date
        article_id_str = request.form.get('article_id', '').strip()
        pub_date_str = request.form.get('publication_date', '').strip()
        try:
            article_id = int(article_id_str)
        except Exception:
            flash('Invalid article ID.')
            return redirect(url_for('content_calendar'))
        # Validate pub_date - expects ISO
        try:
            pub_date = datetime.strptime(pub_date_str, '%Y-%m-%d')
        except Exception:
            flash('Invalid publication date format. Use YYYY-MM-DD.')
            return redirect(url_for('content_calendar'))

        articles = Article.load_all()
        art = articles.get(article_id)
        if not art:
            flash('Article not found.')
            return redirect(url_for('content_calendar'))
        if art['author'] != username:
            flash('You are not the author of this article.')
            return redirect(url_for('content_calendar'))
        # Update article publication_date
        art['publication_date'] = pub_date_str
        # If changing status to published, do it here? We'll keep status same, maybe set to published
        if art['status'] != 'published':
            art['status'] = 'published'
        Article.save_all(articles)
        flash('Article scheduled successfully.')
        return redirect(url_for('content_calendar'))

    # GET: list scheduled articles for user
    articles = Article.load_all()
    scheduled_articles = [a for a in articles.values() if a['author'] == username and a['publication_date']]
    scheduled_articles.sort(key=lambda x: x['publication_date'])
    return render_template('content_calendar.html', scheduled_articles=scheduled_articles, calendar_view=calendar_view)


@app.route('/article/<int:article_id>/analytics', methods=['GET'])
@login_required
def article_analytics(article_id):
    username = session['username']
    article = Article.get(article_id)
    if not article:
        abort(404)

    # Only author and approvers can view analytics
    if article['author'] != username:
        user = User.get(username)
        if not user:
            abort(403)
        # Check role against workflow required roles
        stages = WorkflowStage.load_all()
        cat_stages = stages.get(article['category'], [])
        needed_roles = set()
        for stage in cat_stages:
            needed_roles.update(stage['required_approver_roles'])
        if user['role'] not in needed_roles:
            abort(403)

    analytics_records = Analytics.get_analytics_by_article(article_id)
    # Aggregate analytics
    total_views = sum(a['views'] for a in analytics_records)
    total_unique_visitors = sum(a['unique_visitors'] for a in analytics_records)
    if analytics_records:
        avg_time = sum(a['avg_time_sec'] for a in analytics_records) / len(analytics_records)
    else:
        avg_time = 0.0
    total_shares = sum(a['shares'] for a in analytics_records)

    analytics = {
        'total_views': total_views,
        'total_unique_visitors': total_unique_visitors,
        'average_time_seconds': round(avg_time, 2),
        'total_shares': total_shares,
        'demographics': {},
        'traffic_sources': {},
        'avg_time_on_page': f"{round(avg_time, 2)} seconds"
    }

    return render_template('article_analytics.html', article_id=article_id, analytics=analytics)


# Run app if executed directly
if __name__ == '__main__':
    app.run(debug=True)
