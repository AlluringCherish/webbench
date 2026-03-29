from flask import Flask, session, redirect, url_for, render_template, request, flash
from datetime import datetime
import os
import threading

# === Configuration Constants ===
DATA_DIR = "data"
ARTICLES_FILE = os.path.join(DATA_DIR, "articles.txt")
ARTICLE_VERSIONS_FILE = os.path.join(DATA_DIR, "article_versions.txt")
APPROVALS_FILE = os.path.join(DATA_DIR, "approvals.txt")
COMMENTS_FILE = os.path.join(DATA_DIR, "comments.txt")
ANALYTICS_FILE = os.path.join(DATA_DIR, "analytics.txt")
WORKFLOW_STAGES_FILE = os.path.join(DATA_DIR, "workflow_stages.txt")
USERS_FILE = os.path.join(DATA_DIR, "users.txt")

# Thread lock for file writing to prevent races
file_lock = threading.Lock()

# === Utility Functions for pipe-delimited file reading/writing ===

def read_pipe_delimited_file(filepath, fieldnames):
    """Read file, parse pipe-delimited lines into list of dicts with keys from fieldnames."""
    data = []
    if not os.path.exists(filepath):
        return data
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != len(fieldnames):
                continue  # Skip malformed lines
            entry = dict(zip(fieldnames, parts))
            data.append(entry)
    return data


def write_pipe_delimited_file(filepath, fieldnames, data_list):
    """Overwrite file with list of dicts written as pipe-delimited lines."""
    with file_lock:
        with open(filepath, "w", encoding="utf-8") as f:
            for entry in data_list:
                line = '|'.join(str(entry.get(k, '')) for k in fieldnames)
                f.write(line + "\n")


def append_pipe_delimited_file(filepath, fieldnames, entry):
    """Append a single dict entry to pipe-delimited file."""
    with file_lock:
        with open(filepath, "a", encoding="utf-8") as f:
            line = '|'.join(str(entry.get(k, '')) for k in fieldnames)
            f.write(line + "\n")


# === Data Access: Articles DAO ===
# articles.txt schema (example): article_id|title|author|category|status|created_at|updated_at
ARTICLE_FIELDS = ["article_id", "title", "author", "category", "status", "created_at", "updated_at"]

def load_articles():
    articles = read_pipe_delimited_file(ARTICLES_FILE, ARTICLE_FIELDS)
    # Convert some fields to ints or date if needed
    for a in articles:
        a['article_id'] = int(a['article_id'])
    return articles

def save_articles(articles):
    # articles: list of dicts
    # Convert all values to str
    write_pipe_delimited_file(ARTICLES_FILE, ARTICLE_FIELDS, articles)

def find_article(article_id):
    articles = load_articles()
    for a in articles:
        if a['article_id'] == article_id:
            return a
    return None

def generate_article_id():
    articles = load_articles()
    if not articles:
        return 1
    return max(a['article_id'] for a in articles) + 1

# === Data Access: Article Versions DAO ===
# article_versions.txt schema: article_id|version_number|content|author|timestamp|change_summary
ARTICLE_VERSION_FIELDS = ["article_id", "version_number", "content", "author", "timestamp", "change_summary"]

def load_article_versions(article_id=None):
    versions = read_pipe_delimited_file(ARTICLE_VERSIONS_FILE, ARTICLE_VERSION_FIELDS)
    # Convert fields
    result = []
    for v in versions:
        v['article_id'] = int(v['article_id'])
        v['version_number'] = int(v['version_number'])
        result.append(v)
    if article_id is not None:
        result = [v for v in result if v['article_id'] == article_id]
    # Sort by version_number ascending
    result.sort(key=lambda x: x['version_number'])
    return result

def append_article_version(version_entry):
    # version_entry: dict with keys in ARTICLE_VERSION_FIELDS
    append_pipe_delimited_file(ARTICLE_VERSIONS_FILE, ARTICLE_VERSION_FIELDS, version_entry)

def get_latest_version_number(article_id):
    versions = load_article_versions(article_id)
    if not versions:
        return 0
    return max(v['version_number'] for v in versions)

# === Data Access: Approvals DAO ===
# approvals.txt schema: article_id|version_number|approver|status|comment|timestamp
APPROVAL_FIELDS = ["article_id", "version_number", "approver", "status", "comment", "timestamp"]

def load_approvals(article_id=None, version_number=None):
    approvals = read_pipe_delimited_file(APPROVALS_FILE, APPROVAL_FIELDS)
    result = []
    for a in approvals:
        a['article_id'] = int(a['article_id'])
        a['version_number'] = int(a['version_number'])
        result.append(a)
    if article_id is not None:
        result = [a for a in result if a['article_id'] == article_id]
    if version_number is not None:
        result = [a for a in result if a['version_number'] == version_number]
    return result

def append_approval(approval_entry):
    append_pipe_delimited_file(APPROVALS_FILE, APPROVAL_FIELDS, approval_entry)

# === Data Access: Comments DAO ===
# comments.txt schema: article_id|version_number|commenter|comment|timestamp
COMMENT_FIELDS = ["article_id", "version_number", "commenter", "comment", "timestamp"]

def load_comments(article_id=None, version_number=None):
    comments = read_pipe_delimited_file(COMMENTS_FILE, COMMENT_FIELDS)
    result = []
    for c in comments:
        c['article_id'] = int(c['article_id'])
        c['version_number'] = int(c['version_number'])
        result.append(c)
    if article_id is not None:
        result = [c for c in result if c['article_id'] == article_id]
    if version_number is not None:
        result = [c for c in result if c['version_number'] == version_number]
    return result

def append_comment(comment_entry):
    append_pipe_delimited_file(COMMENTS_FILE, COMMENT_FIELDS, comment_entry)

# === Data Access: Analytics DAO ===
# analytics.txt schema: article_id|date|views|unique_visitors|avg_time_seconds|shares
ANALYTICS_FIELDS = ["article_id", "date", "views", "unique_visitors", "avg_time_seconds", "shares"]

def load_analytics(article_id=None):
    data = read_pipe_delimited_file(ANALYTICS_FILE, ANALYTICS_FIELDS)
    result = []
    for d in data:
        d['article_id'] = int(d['article_id'])
        d['views'] = int(d['views'])
        d['unique_visitors'] = int(d['unique_visitors'])
        d['avg_time_seconds'] = float(d['avg_time_seconds'])
        d['shares'] = int(d['shares'])
        result.append(d)
    if article_id is not None:
        result = [r for r in result if r['article_id'] == article_id]
    return result

# === Data Access: Workflow Stages DAO ===
# workflow_stages.txt schema: category|stage_number|stage_name|required_flag
WORKFLOW_STAGE_FIELDS = ["category", "stage_number", "stage_name", "required_flag"]

def load_workflow_stages(category=None):
    stages = read_pipe_delimited_file(WORKFLOW_STAGES_FILE, WORKFLOW_STAGE_FIELDS)
    result = []
    for s in stages:
        s['stage_number'] = int(s['stage_number'])
        s['required_flag'] = s['required_flag'].lower() == 'true'
        result.append(s)
    if category is not None:
        result = [s for s in result if s['category'] == category]
    # Sort by stage_number
    result.sort(key=lambda x: x['stage_number'])
    return result

# === Data Access: Users DAO (for session auth and user info) ===
# users.txt schema: username|full_name|role
USER_FIELDS = ["username", "full_name", "role"]

def load_users():
    users = read_pipe_delimited_file(USERS_FILE, USER_FIELDS)
    return users

def find_user(username):
    users = load_users()
    for u in users:
        if u['username'] == username:
            return u
    return None


# === Business Logic / Services ===

def create_article(title, content, author, category="general"):
    # Create new article record
    article_id = generate_article_id()
    now_str = datetime.utcnow().isoformat()
    new_article = {
        "article_id": article_id,
        "title": title,
        "author": author,
        "category": category,
        "status": "draft",
        "created_at": now_str,
        "updated_at": now_str
    }
    articles = load_articles()
    articles.append(new_article)
    save_articles(articles)

    # Create initial version
    version_entry = {
        "article_id": article_id,
        "version_number": 1,
        "content": content,
        "author": author,
        "timestamp": now_str,
        "change_summary": "Initial version"
    }
    append_article_version(version_entry)
    return article_id


def update_article(article_id, title, content, author, change_summary):
    articles = load_articles()
    found = False
    for a in articles:
        if a['article_id'] == article_id:
            a['title'] = title
            a['updated_at'] = datetime.utcnow().isoformat()
            found = True
            break
    if not found:
        return False
    save_articles(articles)

    # Add new version
    latest_version_num = get_latest_version_number(article_id)
    new_version_num = latest_version_num + 1
    version_entry = {
        "article_id": article_id,
        "version_number": new_version_num,
        "content": content,
        "author": author,
        "timestamp": datetime.utcnow().isoformat(),
        "change_summary": change_summary if change_summary else "Updated content"
    }
    append_article_version(version_entry)
    return True


def get_article_version_history(article_id):
    return load_article_versions(article_id)


def get_article_with_latest_version(article_id):
    article = find_article(article_id)
    if not article:
        return None
    versions = load_article_versions(article_id)
    if not versions:
        return article
    latest_version = versions[-1]
    merged = article.copy()
    merged["latest_version"] = latest_version
    return merged

# Approval status checking

VALID_APPROVAL_STATUSES = ['approved', 'rejected', 'revision_requested']

def approve_article_version(article_id, version_number, approver, status, comment):
    if status not in VALID_APPROVAL_STATUSES:
        return False
    approval_entry = {
        "article_id": article_id,
        "version_number": version_number,
        "approver": approver,
        "status": status,
        "comment": comment or "",
        "timestamp": datetime.utcnow().isoformat()
    }
    append_approval(approval_entry)
    return True


def get_approvals_for_version(article_id, version_number):
    return load_approvals(article_id, version_number)


def add_comment(article_id, version_number, commenter, comment):
    comment_entry = {
        "article_id": article_id,
        "version_number": version_number,
        "commenter": commenter,
        "comment": comment,
        "timestamp": datetime.utcnow().isoformat()
    }
    append_comment(comment_entry)
    return True


def get_comments_for_version(article_id, version_number):
    return load_comments(article_id, version_number)

# Publication checking - confirm all required workflow stages approved

def get_workflow_for_category(category):
    return load_workflow_stages(category)


def is_article_version_fully_approved(article_id, version_number, category):
    workflow = get_workflow_for_category(category)
    approvals = get_approvals_for_version(article_id, version_number)
    # Build map: stage_name -> required flag
    required_stages = {stage['stage_name']: stage['required_flag'] for stage in workflow}
    # Build map: approver -> status
    status_map = {a['approver']: a['status'] for a in approvals}

    # Business logic: Must have approval with status 'approved' from each required stage
    # We assume approver names align to stages or we just check all required stages have at least one approval 'approved'
    # For simplicity, check if number of approvals with 'approved' for required stages equals required stages count

    # Note: Because we don't have approver-role->stage mapping, assume all required stages have at least one approval 'approved'
    # This is a simplification due to missing details.

    approved_count = sum(1 for a in approvals if a["status"] == 'approved')
    required_count = sum(1 for r in required_stages.values() if r)

    return approved_count >= required_count


# === Analytics Aggregation ===
def aggregate_article_analytics(article_id):
    data = load_analytics(article_id)
    if not data:
        return {
            "total_views": 0,
            "total_unique_visitors": 0,
            "average_time_seconds": 0.0,
            "total_shares": 0
        }
    total_views = sum(d['views'] for d in data)
    total_unique = sum(d['unique_visitors'] for d in data)
    avg_time = sum(d['avg_time_seconds'] * d['views'] for d in data)/total_views if total_views else 0
    total_shares = sum(d['shares'] for d in data)
    # Define additional fields to match template expected keys
    read_completion_rate = None  # no raw data to compute
    traffic_sources = {}  # no data available in backend
    return {
        "total_views": total_views,
        "total_unique_visitors": total_unique,
        "average_time_seconds": round(avg_time, 2),
        "total_shares": total_shares,
        "read_completion_rate": read_completion_rate,
        "traffic_sources": traffic_sources
    }

# === Dashboard Data Preparation ===
def get_user_quick_stats(username):
    # For demo, count user's articles in different statuses
    articles = load_articles()
    user_articles = [a for a in articles if a['author'] == username]
    count_draft = sum(1 for a in user_articles if a['status'] == 'draft')
    count_published = sum(1 for a in user_articles if a['status'] == 'published')
    count_review = sum(1 for a in user_articles if a['status'] == 'in_review')
    return {
        "draft": count_draft,
        "published": count_published,
        "in_review": count_review
    }

def get_user_recent_activity(username, max_items=5):
    # Recent activity from article versions authored by user, sorted desc
    versions = load_article_versions()
    user_versions = [v for v in versions if v['author'] == username]
    user_versions.sort(key=lambda x: x['timestamp'], reverse=True)
    return user_versions[:max_items]


# === Flask App Factory ===
def create_app():
    app = Flask(__name__)
    app.secret_key = 'super-secret-key-for-dev'  # In production use environment var

    # Helper: simulate session login for demo (normally handled by auth)
    @app.before_request
    def simulate_login():
        # For demo, we forcibly set user session to demo user
        if 'username' not in session:
            session['username'] = 'demo_user'

    # === Routes ===
    
    @app.route('/')
    def root_redirect():
        return redirect(url_for('dashboard'))

    @app.route('/dashboard')
    def dashboard():
        username = session.get('username')
        if not username:
            flash("User not logged in.")
            return redirect(url_for('root_redirect'))
        quick_stats = get_user_quick_stats(username)
        recent_activity = get_user_recent_activity(username)
        return render_template('dashboard.html', username=username, quick_stats=quick_stats, recent_activity=recent_activity)

    @app.route('/article/create', methods=['GET', 'POST'])
    def create_article_route():
        username = session.get('username')
        if not username:
            flash("User not logged in.")
            return redirect(url_for('root_redirect'))

        if request.method == 'GET':
            # Render empty form
            return render_template('create_article.html', errors=None, form_data={})

        # POST - process form data
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', 'general').strip() or 'general'

        errors = {}
        if not title:
            errors['title'] = 'Title is required.'
        if not content:
            errors['content'] = 'Content is required.'

        if errors:
            return render_template('create_article.html', errors=errors, form_data=request.form)

        article_id = create_article(title, content, username, category)
        flash(f"Article created with ID {article_id}.")
        return redirect(url_for('edit_article', article_id=article_id))

    @app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
    def edit_article(article_id):
        username = session.get('username')
        if not username:
            flash("User not logged in.")
            return redirect(url_for('root_redirect'))

        article = find_article(article_id)
        if not article:
            flash("Article not found.")
            return redirect(url_for('dashboard'))

        # On GET: render form with latest version content
        if request.method == 'GET':
            versions = get_article_version_history(article_id)
            latest_version = versions[-1] if versions else None
            form_data = {
                'title': article['title'],
                'content': latest_version['content'] if latest_version else '',
                'change_summary': ''
            }
            return render_template('edit_article.html', article=article, form_data=form_data, errors=None)

        # POST: update article with new version
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        change_summary = request.form.get('change_summary', '').strip()

        errors = {}
        if not title:
            errors['title'] = 'Title is required.'
        if not content:
            errors['content'] = 'Content is required.'

        if errors:
            form_data = {
                'title': title,
                'content': content,
                'change_summary': change_summary
            }
            return render_template('edit_article.html', article=article, form_data=form_data, errors=errors)

        success = update_article(article_id, title, content, username, change_summary)
        if success:
            flash("Article updated successfully.")
        else:
            flash("Failed to update the article.")
        return redirect(url_for('edit_article', article_id=article_id))

    @app.route('/article/<int:article_id>/versions')
    def version_history(article_id):
        article = find_article(article_id)
        if not article:
            flash("Article not found.")
            return redirect(url_for('dashboard'))
        versions = get_article_version_history(article_id)
        current_version_id = versions[-1]['version_number'] if versions else None
        return render_template('version_history.html', article=article, article_id=article_id, versions=versions, current_version_id=current_version_id)

    @app.route('/articles/mine')
    def my_articles():
        username = session.get('username')
        if not username:
            flash("User not logged in.")
            return redirect(url_for('root_redirect'))
        status_filter = request.args.get('status')
        articles = load_articles()
        user_articles = [a for a in articles if a['author'] == username]
        if status_filter:
            user_articles = [a for a in user_articles if a['status'] == status_filter]
        return render_template('my_articles.html', articles=user_articles, filter_status=status_filter)

    @app.route('/articles/published')
    def published_articles():
        category_filter = request.args.get('category')
        sort_by = request.args.get('sort', 'date')
        articles = load_articles()
        published_articles = [a for a in articles if a['status'] == 'published']
        if category_filter:
            published_articles = [a for a in published_articles if a['category'] == category_filter]
        # Extract list of categories available
        categories = sorted(set(a['category'] for a in articles if a['status'] == 'published'))
        # Sorting
        reverse = True  # descending by default
        if sort_by == 'title':
            published_articles.sort(key=lambda x: x.get('title', '').lower(), reverse=reverse)
        elif sort_by == 'author':
            published_articles.sort(key=lambda x: x.get('author', '').lower(), reverse=reverse)
        elif sort_by == 'date':
            # Sort by created_at descending
            published_articles.sort(key=lambda x: x.get('created_at', ''), reverse=reverse)
        else:
            # Default fallback sort by created_at
            published_articles.sort(key=lambda x: x.get('created_at', ''), reverse=reverse)

        return render_template('published_articles.html', articles=published_articles, categories=categories, filter_category=category_filter, sort_by=sort_by)

    @app.route('/calendar')
    def content_calendar():
        # For demo, calendar view selection could come from query
        view = request.args.get('view', 'month')
        articles = load_articles()
        scheduled_articles_list = [a for a in articles if a['status'] in ('published', 'scheduled')]
        # Aggregate articles by date (use created_at date for scheduling)
        agg = {}
        for art in scheduled_articles_list:
            date_key = art['created_at'][:10]  # Extract date part
            if date_key not in agg:
                agg[date_key] = []
            agg[date_key].append(art)
        return render_template('content_calendar.html', calendar_view=view, scheduled_articles=agg)

    @app.route('/article/<int:article_id>/analytics')
    def article_analytics(article_id):
        article = find_article(article_id)
        if not article:
            flash("Article not found.")
            return redirect(url_for('dashboard'))
        analytics_data = aggregate_article_analytics(article_id)
        return render_template('article_analytics.html', article=article, analytics_data=analytics_data)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
