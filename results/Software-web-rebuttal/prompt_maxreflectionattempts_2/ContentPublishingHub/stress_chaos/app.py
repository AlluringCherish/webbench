from flask import Flask, request, render_template, redirect, url_for, session, flash
import os
import datetime
from collections import defaultdict

# Data file paths
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
ARTICLES_FILE = os.path.join(DATA_DIR, 'articles.txt')
ARTICLE_VERSIONS_FILE = os.path.join(DATA_DIR, 'article_versions.txt')
APPROVALS_FILE = os.path.join(DATA_DIR, 'approvals.txt')
WORKFLOW_STAGES_FILE = os.path.join(DATA_DIR, 'workflow_stages.txt')
COMMENTS_FILE = os.path.join(DATA_DIR, 'comments.txt')
ANALYTICS_FILE = os.path.join(DATA_DIR, 'analytics.txt')

from flask import abort

from threading import Lock

# Global in-memory locks (for basic concurrency control on file writes)
file_locks = {
    USERS_FILE: Lock(),
    ARTICLES_FILE: Lock(),
    ARTICLE_VERSIONS_FILE: Lock(),
    APPROVALS_FILE: Lock(),
    WORKFLOW_STAGES_FILE: Lock(),
    COMMENTS_FILE: Lock(),
    ANALYTICS_FILE: Lock()
}

# ---- Utility functions for file IO and parsing ----

def _atomic_write(filepath, lines):
    # Write to a temp file then rename to ensure atomic write
    temp_path = filepath + '.tmp'
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    os.replace(temp_path, filepath)


def read_pipe_delimited(filepath, fieldnames):
    """
    Reads a pipe delimited file into a list of dicts keyed by fieldnames
    """
    data = []
    if not os.path.exists(filepath):
        return data
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip('\n').rstrip('|').strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < len(fieldnames):
                # Fill missing parts with empty strings
                parts += [''] * (len(fieldnames) - len(parts))
            entry = dict(zip(fieldnames, parts))
            data.append(entry)
    return data


def write_pipe_delimited(filepath, records, fieldnames):
    lines = []
    for rec in records:
        line = '|'.join(rec.get(k, '') for k in fieldnames) + '\n'
        lines.append(line)
    _atomic_write(filepath, lines)


# ---- User session helper stub ----
def get_current_username():
    # Stub for getting current logged user from session
    # For now if no user in session, default to 'guest'
    return session.get('username', 'guest')


# ---- Data fieldnames for each file according to architecture specs ----
# users.txt fields: user_id|username|email|role
USER_FIELDS = ['user_id', 'username', 'email', 'role']

# articles.txt fields: article_id|title|category|author|status|created_date|last_modified_date
ARTICLE_FIELDS = ['article_id', 'title', 'category', 'author', 'status', 'created_date', 'last_modified_date']

# article_versions.txt fields: version_id|article_id|version_number|content|author|created_date|change_summary
ARTICLE_VERSION_FIELDS = ['version_id', 'article_id', 'version_number', 'content', 'author', 'created_date', 'change_summary']

# approvals.txt fields: approval_id|article_id|version_id|approver|status|comments|timestamp
APPROVAL_FIELDS = ['approval_id', 'article_id', 'version_id', 'approver', 'status', 'comments', 'timestamp']

# workflow_stages.txt fields: category|stage_order|stage_name|required
WORKFLOW_STAGE_FIELDS = ['category', 'stage_order', 'stage_name', 'required']

# comments.txt fields: comment_id|article_id|version_id|commenter|comment|timestamp
COMMENT_FIELDS = ['comment_id', 'article_id', 'version_id', 'commenter', 'comment', 'timestamp']

# analytics.txt fields: analytic_id|article_id|views|unique_visitors|avg_time_on_article|shares|date
ANALYTIC_FIELDS = ['analytic_id', 'article_id', 'views', 'unique_visitors', 'avg_time_on_article', 'shares', 'date']

# ---- Helper functions for loading/saving entities ----

def load_users():
    return read_pipe_delimited(USERS_FILE, USER_FIELDS)

def load_articles():
    return read_pipe_delimited(ARTICLES_FILE, ARTICLE_FIELDS)

def save_articles(articles):
    with file_locks[ARTICLES_FILE]:
        write_pipe_delimited(ARTICLES_FILE, articles, ARTICLE_FIELDS)


def load_article_versions():
    return read_pipe_delimited(ARTICLE_VERSIONS_FILE, ARTICLE_VERSION_FIELDS)

def save_article_versions(versions):
    with file_locks[ARTICLE_VERSIONS_FILE]:
        write_pipe_delimited(ARTICLE_VERSIONS_FILE, versions, ARTICLE_VERSION_FIELDS)


def load_approvals():
    return read_pipe_delimited(APPROVALS_FILE, APPROVAL_FIELDS)

def save_approvals(approvals):
    with file_locks[APPROVALS_FILE]:
        write_pipe_delimited(APPROVALS_FILE, approvals, APPROVAL_FIELDS)


def load_workflow_stages():
    return read_pipe_delimited(WORKFLOW_STAGES_FILE, WORKFLOW_STAGE_FIELDS)

def load_comments():
    return read_pipe_delimited(COMMENTS_FILE, COMMENT_FIELDS)

def save_comments(comments):
    with file_locks[COMMENTS_FILE]:
        write_pipe_delimited(COMMENTS_FILE, comments, COMMENT_FIELDS)


def load_analytics():
    return read_pipe_delimited(ANALYTICS_FILE, ANALYTIC_FIELDS)

def save_analytics(analytics):
    with file_locks[ANALYTICS_FILE]:
        write_pipe_delimited(ANALYTICS_FILE, analytics, ANALYTIC_FIELDS)


# ---- Version control and approval logic ----

def generate_new_article_id(articles):
    max_id = 0
    for a in articles:
        try:
            aid = int(a['article_id'])
            if aid > max_id:
                max_id = aid
        except ValueError:
            pass
    return str(max_id + 1)



def generate_new_version_id(versions):
    max_id = 0
    for v in versions:
        try:
            vid = int(v['version_id'])
            if vid > max_id:
                max_id = vid
        except ValueError:
            pass
    return str(max_id + 1)

def generate_new_approval_id(approvals):
    max_id = 0
    for ap in approvals:
        try:
            aid = int(ap['approval_id'])
            if aid > max_id:
                max_id = aid
        except ValueError:
            pass
    return str(max_id + 1)

def generate_new_comment_id(comments):
    max_id = 0
    for cm in comments:
        try:
            cid = int(cm['comment_id'])
            if cid > max_id:
                max_id = cid
        except ValueError:
            pass
    return str(max_id + 1)

def generate_new_analytic_id(analytics):
    max_id = 0
    for an in analytics:
        try:
            aid = int(an['analytic_id'])
            if aid > max_id:
                max_id = aid
        except ValueError:
            pass
    return str(max_id + 1)



def get_next_version_number(article_id, versions):
    max_version = 0
    for v in versions:
        if v['article_id'] == article_id:
            try:
                vn = int(v['version_number'])
                if vn > max_version:
                    max_version = vn
            except ValueError:
                pass
    return str(max_version + 1)


# Check approval stages completion for a category and article version
# Returns True if all required stages approved, False otherwise

def is_version_fully_approved(category, article_id, version_id):
    workflow_stages = load_workflow_stages()
    approvals = load_approvals()

    # Get required stages for category
    required_stages = [w['stage_name'] for w in workflow_stages if w['category'] == category and w['required'].lower() == 'true']

    # For each required stage, check if there's at least one approval with status 'approved'
    for stage in required_stages:
        approved = False
        for ap in approvals:
            if ap['article_id'] == article_id and ap['version_id'] == version_id:
                if ap['approver'] == stage and ap['status'].lower() == 'approved':
                    approved = True
                    break
        if not approved:
            return False
    return True


def update_article_status_based_on_approval(article, category, article_id, version_id):
    # If fully approved, mark article status to 'published', else 'in_review' if any approval exists else 'draft'
    fully_approved = is_version_fully_approved(category, article_id, version_id)
    if fully_approved:
        article['status'] = 'published'
    else:
        # Check if any approval record exists for this article/version
        approvals = load_approvals()
        any_approval = any((ap['article_id'] == article_id and ap['version_id'] == version_id) for ap in approvals)
        if any_approval:
            article['status'] = 'in_review'
        else:
            article['status'] = 'draft'


# ----- Flask app setup -----

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Should be a config item


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = get_current_username()

    # Quick stats: count articles (total, by status), recent activity (last 5 edits)
    articles = load_articles()
    versions = load_article_versions()

    total_articles = len(articles)
    status_counts = defaultdict(int)
    for a in articles:
        status_counts[a['status']] += 1

    # Recent activity: list last 5 versions by created_date descending
    versions_sorted = sorted(versions, key=lambda v: v['created_date'], reverse=True)
    recent_activity = versions_sorted[:5]

    quick_stats = {
        'total_articles': total_articles,
        'status_counts': dict(status_counts)
    }

    return render_template('dashboard.html', username=username, quick_stats=quick_stats, recent_activity=recent_activity)


@app.route('/article/create', methods=['GET', 'POST'])
def create_article():
    username = get_current_username()

    if request.method == 'GET':
        return render_template('create_article.html', username=username)

    # POST
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    category = request.form.get('category', '').strip()

    errors = []
    if not title:
        errors.append('Title is required.')
    if not content:
        errors.append('Content is required.')
    if not category:
        errors.append('Category is required.')

    if errors:
        return render_template('create_article.html', username=username, validation_errors=errors)

    articles = load_articles()
    article_versions = load_article_versions()

    new_article_id = generate_new_article_id(articles)
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    new_article = {
        'article_id': new_article_id,
        'title': title,
        'category': category,
        'author': username,
        'status': 'draft',
        'created_date': today,
        'last_modified_date': today
    }
    articles.append(new_article)

    # Create initial version
    new_version_id = generate_new_version_id(article_versions)
    new_version = {
        'version_id': new_version_id,
        'article_id': new_article_id,
        'version_number': '1',
        'content': content,
        'author': username,
        'created_date': today,
        'change_summary': 'Initial version'
    }
    article_versions.append(new_version)

    # Save both files
    save_articles(articles)
    save_article_versions(article_versions)

    flash('Article created successfully!')
    return redirect(url_for('edit_article', article_id=new_article_id))


@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    username = get_current_username()
    articles = load_articles()
    article = None
    for a in articles:
        if int(a['article_id']) == article_id:
            article = a
            break
    if article is None:
        abort(404, description='Article not found')

    article_versions = load_article_versions()

    if request.method == 'GET':
        # Show latest version content
        current_versions = [v for v in article_versions if v['article_id'] == article['article_id']]
        if not current_versions:
            # No versions found (inconsistent state)
            content = ''
            version_number = 'N/A'
        else:
            latest_version = max(current_versions, key=lambda v: int(v['version_number']))
            content = latest_version['content']
            version_number = latest_version['version_number']

        return render_template('edit_article.html', article=article, content=content, version_number=version_number, username=username)

    # POST: save new version
    content = request.form.get('content', '').strip()
    change_summary = request.form.get('change_summary', '').strip() or 'Edit'

    errors = []
    if not content:
        errors.append('Content cannot be empty.')

    if errors:
        # re-render with errors and the attempted content
        return render_template('edit_article.html', article=article, content=content, errors=errors, username=username)

    # Create new version
    new_version_id = generate_new_version_id(article_versions)
    version_number = get_next_version_number(article['article_id'], article_versions)
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    new_version = {
        'version_id': new_version_id,
        'article_id': article['article_id'],
        'version_number': version_number,
        'content': content,
        'author': username,
        'created_date': today,
        'change_summary': change_summary
    }
    article_versions.append(new_version)
    save_article_versions(article_versions)

    # Update article last modified date
    article['last_modified_date'] = today

    # After new version is saved, reset article status to draft until approvals
    article['status'] = 'draft'

    save_articles(articles)

    flash('Article updated with new version saved.')
    return redirect(url_for('edit_article', article_id=article_id))


@app.route('/article/<int:article_id>/versions')
def article_version_history(article_id):
    username = get_current_username()

    articles = load_articles()
    article = next((a for a in articles if int(a['article_id']) == article_id), None)
    if article is None:
        abort(404, description='Article not found')

    article_versions = load_article_versions()
    approvals = load_approvals()
    comments = load_comments()

    versions = [v for v in article_versions if v['article_id'] == article['article_id']]
    versions_sorted = sorted(versions, key=lambda v: int(v['version_number']), reverse=True)

    # enrich with approvals and comments count
    for v in versions_sorted:
        v_approvals = [ap for ap in approvals if ap['article_id'] == article['article_id'] and ap['version_id'] == v['version_id']]
        v_comments = [cm for cm in comments if cm['article_id'] == article['article_id'] and cm['version_id'] == v['version_id']]
        v['approvals_count'] = str(len(v_approvals))
        v['comments_count'] = str(len(v_comments))

    return render_template('article_version_history.html', article=article, versions=versions_sorted, username=username, article_id=article['article_id'])


@app.route('/articles/mine')
def my_articles():
    username = get_current_username()

    # Optional filter
    status_filter = request.args.get('status', '').lower()

    articles = load_articles()
    my_articles = [a for a in articles if a['author'] == username]
    if status_filter:
        my_articles = [a for a in my_articles if a['status'].lower() == status_filter]

    return render_template('my_articles.html', username=username, articles=my_articles, filter_status=status_filter)


@app.route('/articles/published')
def published_articles():
    category_filter = request.args.get('category', '').strip()
    sort_by = request.args.get('sort', '').strip()

    articles = load_articles()
    published = [a for a in articles if a['status'].lower() == 'published']

    if category_filter:
        published = [a for a in published if a['category'] == category_filter]

    if sort_by:
        if sort_by == 'date':
            published.sort(key=lambda x: x['created_date'], reverse=True)
        elif sort_by == 'title':
            published.sort(key=lambda x: x['title'])

    # Prepare unique categories for filter dropdown
    categories = sorted(set(a['category'] for a in load_articles() if a['status'].lower() == 'published'))

    # Provide user_roles for template (stub: only 'guest')
    user_roles = []
    users = load_users()
    username = get_current_username()
    for u in users:
        if u['username'] == username:
            user_roles.append(u['role'])
            break

    return render_template('published_articles.html', articles=published, filter_category=category_filter, sort_by=sort_by, categories=categories, user_roles=user_roles)


@app.route('/calendar', methods=['GET', 'POST'])
def content_calendar():
    username = get_current_username()
    articles = load_articles()

    message = None
    validation_errors = []

    if request.method == 'POST':
        # Expect form data for scheduling: article_id, new_date (scheduled_publish_date) - treating last_modified_date as scheduled
        article_id = request.form.get('article_id', '').strip()
        new_date = request.form.get('new_date', '').strip()  # Expecting YYYY-MM-DD

        if not article_id or not new_date:
            validation_errors.append('Article and date are required for scheduling.')
        else:
            # Validate date format
            try:
                datetime.datetime.strptime(new_date, '%Y-%m-%d')
            except ValueError:
                validation_errors.append('Invalid date format. Use YYYY-MM-DD.')

            # Find article
            article = None
            for a in articles:
                if a['article_id'] == article_id:
                    article = a
                    break
            if article is None:
                validation_errors.append('Article not found.')

            if not validation_errors:
                # Update the last_modified_date as scheduled publish date
                article['last_modified_date'] = new_date
                save_articles(articles)
                message = 'Scheduling updated successfully.'

    # Prepare calendar data: list of articles with their scheduled publish dates (using last_modified_date)
    calendar_data = []
    for a in articles:
        calendar_data.append({'article_id': a['article_id'], 'title': a['title'], 'scheduled_date': a['last_modified_date']})

    return render_template('content_calendar.html', calendar_view=True, calendar_data=calendar_data, status_message=message, validation_errors=validation_errors, username=username)


@app.route('/article/<int:article_id>/analytics')
def article_analytics(article_id):
    username = get_current_username()

    articles = load_articles()
    article = next((a for a in articles if int(a['article_id']) == article_id), None)
    if article is None:
        abort(404, description='Article not found')

    analytics = load_analytics()
    filtered_analytics = [a for a in analytics if int(a['article_id']) == article_id]

    # Aggregate analytics over time
    total_views = 0
    total_unique_visitors = 0
    total_avg_time = 0.0
    total_shares = 0
    count = 0

    for entry in filtered_analytics:
        try:
            total_views += int(entry['views'])
            total_unique_visitors += int(entry['unique_visitors'])
            total_avg_time += float(entry['avg_time_on_article'])
            total_shares += int(entry['shares'])
            count += 1
        except ValueError:
            pass

    if count > 0:
        avg_time = round(total_avg_time / count, 2)
    else:
        avg_time = 0.0

    analytics_summary = {
        'total_views': total_views,
        'total_unique_visitors': total_unique_visitors,
        'average_time_on_article': avg_time,
        'total_shares': total_shares
    }

    return render_template('article_analytics.html', article=article, analytics_summary=analytics_summary, username=username)

# Note: Comments and approval action APIs not detailed here due to spec focus on routes listed

if __name__ == '__main__':
    app.run(debug=True)
