from flask import Flask, request, redirect, url_for, render_template, session, jsonify, abort, flash
from functools import wraps
import os
import threading
import datetime
import difflib
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DATA_DIR = 'data'
LOCK = threading.Lock()

# File paths
ARTICLES_FILE = os.path.join(DATA_DIR, 'articles.txt')
ARTICLE_VERSIONS_FILE = os.path.join(DATA_DIR, 'article_versions.txt')
APPROVALS_FILE = os.path.join(DATA_DIR, 'approvals.txt')
COMMENTS_FILE = os.path.join(DATA_DIR, 'comments.txt')
ANALYTICS_FILE = os.path.join(DATA_DIR, 'analytics.txt')
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
WORKFLOW_STAGES_FILE = os.path.join(DATA_DIR, 'workflow_stages.txt')
CALENDAR_FILE = os.path.join(DATA_DIR, 'calendar_data.txt')

# Helper functions for file read/write with locking

def read_pipe_delimited_file(filepath, fieldnames):
    records = []
    if not os.path.exists(filepath):
        return records
    with LOCK:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != len(fieldnames):
                    continue  # skip malformed line
                record = dict(zip(fieldnames, parts))
                records.append(record)
    return records


def write_pipe_delimited_file(filepath, records, fieldnames):
    with LOCK:
        with open(filepath, 'w', encoding='utf-8') as f:
            for record in records:
                row = '|'.join(record.get(field, '') for field in fieldnames)
                f.write(row + '\n')


def append_pipe_delimited_file(filepath, record, fieldnames):
    # append a single record line
    with LOCK:
        with open(filepath, 'a', encoding='utf-8') as f:
            row = '|'.join(record.get(field, '') for field in fieldnames)
            f.write(row + '\n')


def generate_new_id(existing_ids, prefix):
    # Generates next numeric id with prefix
    max_num = 0
    for eid in existing_ids:
        if eid.startswith(prefix):
            try:
                num = int(eid[len(prefix):])
                if num > max_num:
                    max_num = num
            except:
                continue
    return f'{prefix}{max_num + 1}'


def get_current_user():
    # For this demo, simple session-based username
    username = session.get('username')
    if not username:
        return None
    users = get_all_users()
    for user in users:
        if user['username'] == username:
            return user
    return None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not get_current_user():
            flash('Please log in to access this page.')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# --- Data Models ---

# Fields definitions per file
ARTICLE_FIELDS = ['article_id','title','author','category','status','tags','featured_image','meta_description','created_date','publish_date']
ARTICLE_VERSION_FIELDS = ['version_id','article_id','version_number','content','author','created_date','change_summary']
APPROVAL_FIELDS = ['approval_id','version_id','approver','status','comments','timestamp']
COMMENT_FIELDS = ['comment_id','version_id','commenter','comment_text','timestamp']
ANALYTIC_FIELDS = ['article_id','views','unique_visitors','avg_time_seconds','shares']
USER_FIELDS = ['user_id','username','role']
WORKFLOW_STAGE_FIELDS = ['stage_id','category','stage_name','stage_order','is_required']
CALENDAR_FIELDS = ['article_id','scheduled_date','notes']


def get_all_users():
    return read_pipe_delimited_file(USERS_FILE, USER_FIELDS)


def get_user_by_username(username):
    users = get_all_users()
    for user in users:
        if user['username'] == username:
            return user
    return None

# Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        # For simplicity, no password used
        user = get_user_by_username(username)
        if user:
            session['username'] = username
            flash('Logged in successfully.')
            next_url = request.args.get('next')
            return redirect(next_url or url_for('dashboard'))
        else:
            flash('Invalid username')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out.')
    return redirect(url_for('login'))


# --- Data Access Functions ---

# Articles

def get_all_articles():
    return read_pipe_delimited_file(ARTICLES_FILE, ARTICLE_FIELDS)

def get_article(article_id):
    articles = get_all_articles()
    for article in articles:
        if article['article_id'] == article_id:
            return article
    return None



def save_articles(articles):
    write_pipe_delimited_file(ARTICLES_FILE, articles, ARTICLE_FIELDS)


def append_article(article):
    append_pipe_delimited_file(ARTICLES_FILE, article, ARTICLE_FIELDS)


# Article Versions

def get_all_versions():
    return read_pipe_delimited_file(ARTICLE_VERSIONS_FILE, ARTICLE_VERSION_FIELDS)


def get_versions_for_article(article_id):
    return [v for v in get_all_versions() if v['article_id'] == article_id]


def get_version(version_id):
    versions = get_all_versions()
    for v in versions:
        if v['version_id'] == version_id:
            return v
    return None


def save_versions(versions):
    write_pipe_delimited_file(ARTICLE_VERSIONS_FILE, versions, ARTICLE_VERSION_FIELDS)


def append_version(version):
    append_pipe_delimited_file(ARTICLE_VERSIONS_FILE, version, ARTICLE_VERSION_FIELDS)


def get_next_version_number(article_id):
    versions = get_versions_for_article(article_id)
    max_version = 0
    for v in versions:
        try:
            vn = int(v['version_number'])
            if vn > max_version:
                max_version = vn
        except:
            pass
    return max_version + 1


# Approvals

def get_all_approvals():
    return read_pipe_delimited_file(APPROVALS_FILE, APPROVAL_FIELDS)

def get_approvals_for_version(version_id):
    return [a for a in get_all_approvals() if a['version_id'] == version_id]

def append_approval(approval):
    append_pipe_delimited_file(APPROVALS_FILE, approval, APPROVAL_FIELDS)


def get_latest_approval_for_version(version_id):
    approvals = get_approvals_for_version(version_id)
    if not approvals:
        return None
    # Return latest by timestamp
    approvals.sort(key=lambda x: x['timestamp'], reverse=True)
    return approvals[0]


# Comments

def get_all_comments():
    return read_pipe_delimited_file(COMMENTS_FILE, COMMENT_FIELDS)

def get_comments_for_version(version_id):
    return [c for c in get_all_comments() if c['version_id'] == version_id]

def append_comment(comment):
    append_pipe_delimited_file(COMMENTS_FILE, comment, COMMENT_FIELDS)


# Analytics

def get_all_analytics():
    return read_pipe_delimited_file(ANALYTICS_FILE, ANALYTIC_FIELDS)

def get_analytics_for_article(article_id):
    analytics = get_all_analytics()
    for a in analytics:
        if a['article_id'] == article_id:
            # Convert metrics
            try:
                a['views'] = int(a['views'])
                a['unique_visitors'] = int(a['unique_visitors'])
                a['avg_time_seconds'] = float(a['avg_time_seconds'])
                a['shares'] = int(a['shares'])
            except:
                a['views'] = 0
                a['unique_visitors'] = 0
                a['avg_time_seconds'] = 0.0
                a['shares'] = 0
            return a
    return {'article_id': article_id, 'views': 0, 'unique_visitors': 0, 'avg_time_seconds': 0.0, 'shares': 0}


# Workflow

def get_workflow_stages():
    stages = read_pipe_delimited_file(WORKFLOW_STAGES_FILE, WORKFLOW_STAGE_FIELDS)
    # Sort by stage_order
    try:
        stages.sort(key=lambda s: int(s['stage_order']))
    except:
        pass
    return stages


def get_stage_by_category_and_order(category, stage_order):
    stages = get_workflow_stages()
    for stage in stages:
        try:
            if stage['category'] == category and int(stage['stage_order']) == int(stage_order):
                return stage
        except:
            continue
    return None

# Calendar

def get_all_calendar_entries():
    return read_pipe_delimited_file(CALENDAR_FILE, CALENDAR_FIELDS)

def save_calendar_entries(entries):
    write_pipe_delimited_file(CALENDAR_FILE, entries, CALENDAR_FIELDS)


def append_calendar_entry(entry):
    append_pipe_delimited_file(CALENDAR_FILE, entry, CALENDAR_FIELDS)


# --- Routes ---

@app.route('/')
def index():
    return redirect(url_for('dashboard'))


# Dashboard - GET
@app.route('/dashboard')
@login_required
def dashboard():
    user = get_current_user()
    articles = get_all_articles()

    # Simple stats
    total_articles = len(articles)
    published_articles = len([a for a in articles if a['status'].lower() == 'published'])
    pending_approval = len([a for a in articles if a['status'].lower() == 'pending approval'])
    drafts = len([a for a in articles if a['status'].lower() == 'draft'])
    my_articles = len([a for a in articles if a['author'] == user['username']])

    return render_template('dashboard.html', user=user, total_articles=total_articles,
                           published_articles=published_articles, my_articles=my_articles,
                           pending_approval=pending_approval, drafts=drafts)


# List articles owned by current user
@app.route('/articles/mine')
@login_required
def articles_mine():
    user = get_current_user()
    articles = get_all_articles()
    my_articles = [a for a in articles if a['author'] == user['username']]
    return render_template('my_articles.html', articles=my_articles)


# List published articles with optional filtering
@app.route('/articles/published')
@login_required
def articles_published():
    articles = get_all_articles()
    published = [a for a in articles if a['status'].lower() == 'published']

    # Filters from query
    category_filter = request.args.get('category')
    if category_filter:
        published = [a for a in published if a['category'] == category_filter]

    # Gather distinct categories for filter dropdown
    categories = sorted(set(a['category'] for a in articles if a['category']))
    selected_category = category_filter or ''

    return render_template('published_articles.html', articles=published, categories=categories, selected_category=selected_category)


# Article Creation GET/POST
@app.route('/article/create', methods=['GET', 'POST'])
@login_required
def article_create():
    user = get_current_user()
    if request.method == 'POST':
        # Get data
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        tags = request.form.get('tags', '').strip()
        featured_image = request.form.get('featured_image', '').strip()
        meta_description = request.form.get('meta_description', '').strip()

        if not title:
            flash('Title is required.')
            return render_template('create_article.html')

        articles = get_all_articles()
        article_ids = [a['article_id'] for a in articles]
        new_article_id = generate_new_id(article_ids, 'A')

        created_date = datetime.datetime.now().strftime('%Y-%m-%d')

        new_article = {
            'article_id': new_article_id,
            'title': title,
            'author': user['username'],
            'category': category,
            'status': 'draft',
            'tags': tags,
            'featured_image': featured_image,
            'meta_description': meta_description,
            'created_date': created_date,
            'publish_date': ''
        }

        append_article(new_article)

        # Also create initial version
        version_ids = [v['version_id'] for v in get_all_versions()]
        new_version_id = generate_new_id(version_ids, 'V')
        version_number = 1
        content = request.form.get('content', '').strip() or ''
        change_summary = 'Initial version'
        created_date_time = datetime.datetime.now().isoformat()
        new_version = {
            'version_id': new_version_id,
            'article_id': new_article_id,
            'version_number': str(version_number),
            'content': content,
            'author': user['username'],
            'created_date': created_date_time,
            'change_summary': change_summary,
        }
        append_version(new_version)

        flash('Article created successfully.')
        return redirect(url_for('article_edit', article_id=new_article_id))

    return render_template('create_article.html')


# Edit article GET/POST & version creation
@app.route('/article/<article_id>/edit', methods=['GET', 'POST'])
@login_required
def article_edit(article_id):
    user = get_current_user()
    article = get_article(article_id)
    if not article:
        abort(404, description='Article not found')

    # Authorization: Authors can only edit their own articles, others editors/admins can edit all
    if user['role'].lower() == 'author' and article['author'] != user['username']:
        abort(403)

    if request.method == 'POST':
        # Update article metadata
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        tags = request.form.get('tags', '').strip()
        featured_image = request.form.get('featured_image', '').strip()
        meta_description = request.form.get('meta_description', '').strip()

        if not title:
            flash('Title cannot be empty.')
            return render_template('edit_article.html', article=article)

        article['title'] = title
        article['category'] = category
        article['tags'] = tags
        article['featured_image'] = featured_image
        article['meta_description'] = meta_description

        articles = get_all_articles()
        # Update in articles list
        for idx, a in enumerate(articles):
            if a['article_id'] == article_id:
                articles[idx] = article
                break
        save_articles(articles)

        # Save new version
        content = request.form.get('content', '').strip() or ''
        change_summary = request.form.get('change_summary', '').strip() or 'Updated content'

        version_ids = [v['version_id'] for v in get_all_versions()]
        new_version_id = generate_new_id(version_ids, 'V')
        version_number = get_next_version_number(article_id)
        created_date_time = datetime.datetime.now().isoformat()

        new_version = {
            'version_id': new_version_id,
            'article_id': article_id,
            'version_number': str(version_number),
            'content': content,
            'author': user['username'],
            'created_date': created_date_time,
            'change_summary': change_summary,
        }
        append_version(new_version)

        flash('Article updated and new version saved.')
        return redirect(url_for('article_edit', article_id=article_id))

    # GET: show latest version content
    versions = get_versions_for_article(article_id)
    if versions:
        # Latest by version_number
        try:
            versions.sort(key=lambda v: int(v['version_number']), reverse=True)
        except:
            pass
        latest_version = versions[0]
    else:
        latest_version = None

    return render_template('edit_article.html', article=article, version=latest_version)


# List versions for article
@app.route('/article/<article_id>/versions')
@login_required
def article_versions(article_id):
    article = get_article(article_id)
    if not article:
        abort(404, description='Article not found')

    versions = get_versions_for_article(article_id)
    try:
        versions.sort(key=lambda v: int(v['version_number']), reverse=True)
    except:
        pass
    return render_template('version_history.html', article=article, versions=versions)


# View specific version
@app.route('/article/<article_id>/versions/<version_id>')
@login_required
def article_version_view(article_id, version_id):
    article = get_article(article_id)
    if not article:
        abort(404, description='Article not found')
    version = get_version(version_id)
    if not version or version['article_id'] != article_id:
        abort(404, description='Version not found for this article')

    comments = get_comments_for_version(version_id)

    return render_template('version_detail.html', article=article, version=version, comments=comments)


# Compare two versions
@app.route('/article/<article_id>/versions/<version_id>/compare/<other_version_id>')
@login_required
def article_version_compare(article_id, version_id, other_version_id):
    article = get_article(article_id)
    if not article:
        abort(404, description='Article not found')
    version1 = get_version(version_id)
    version2 = get_version(other_version_id)
    if not version1 or not version2:
        abort(404, description='Version(s) not found')
    if version1['article_id'] != article_id or version2['article_id'] != article_id:
        abort(404, description='Version(s) do not belong to article')

    diff = difflib.unified_diff(
        version1['content'].splitlines(),
        version2['content'].splitlines(),
        fromfile=f'Version {version1["version_number"]}',
        tofile=f'Version {version2["version_number"]}',
        lineterm=''
    )
    diff_text = '\n'.join(diff)

    return render_template('version_compare.html', article=article, version1=version1, version2=version2, diff=diff_text)


# Restore an older version as new current version
@app.route('/article/<article_id>/versions/<version_id>/restore', methods=['POST'])
@login_required
def article_version_restore(article_id, version_id):
    user = get_current_user()
    article = get_article(article_id)
    if not article:
        abort(404, description='Article not found')

    version_to_restore = get_version(version_id)
    if not version_to_restore or version_to_restore['article_id'] != article_id:
        abort(404, description='Version not found for this article')

    # Authorization check
    if user['role'].lower() == 'author' and article['author'] != user['username']:
        abort(403)

    # Create new version copying content from version_to_restore
    version_ids = [v['version_id'] for v in get_all_versions()]
    new_version_id = generate_new_id(version_ids, 'V')
    version_number = get_next_version_number(article_id)
    change_summary = f'Restored version {version_to_restore["version_number"]}'
    created_date_time = datetime.datetime.now().isoformat()
    new_version = {
        'version_id': new_version_id,
        'article_id': article_id,
        'version_number': str(version_number),
        'content': version_to_restore['content'],
        'author': user['username'],
        'created_date': created_date_time,
        'change_summary': change_summary,
    }
    append_version(new_version)

    flash('Version restored and new version created.')
    return redirect(url_for('article_edit', article_id=article_id))


# Approval status and comments view
@app.route('/article/<article_id>/approval')
@login_required
def article_approval_status(article_id):
    article = get_article(article_id)
    if not article:
        abort(404, description='Article not found')

    # Get latest version
    versions = get_versions_for_article(article_id)
    if not versions:
        flash('No versions found for this article.')
        return redirect(url_for('article_edit', article_id=article_id))

    try:
        versions.sort(key=lambda v: int(v['version_number']), reverse=True)
    except:
        pass
    latest_version = versions[0]

    approvals = get_approvals_for_version(latest_version['version_id'])

    return render_template('approval_status.html', article=article, version=latest_version, approvals=approvals)


# Submit approval decision
@app.route('/article/<article_id>/approval/submit', methods=['POST'])
@login_required
def article_approval_submit(article_id):
    user = get_current_user()
    article = get_article(article_id)
    if not article:
        abort(404, description='Article not found')

    status = request.form.get('status')  # expected: approved, rejected, revision_requested
    comments = request.form.get('comments', '')

    if status not in ['approved', 'rejected', 'revision_requested']:
        flash('Invalid approval status.')
        return redirect(url_for('article_approval_status', article_id=article_id))

    # Get latest version
    versions = get_versions_for_article(article_id)
    if not versions:
        flash('No versions for article to approve.')
        return redirect(url_for('article_edit', article_id=article_id))

    try:
        versions.sort(key=lambda v: int(v['version_number']), reverse=True)
    except:
        pass
    latest_version = versions[0]

    # Create new approval
    approval_ids = [a['approval_id'] for a in get_all_approvals()]
    new_approval_id = generate_new_id(approval_ids, 'AP')
    timestamp = datetime.datetime.now().isoformat()

    new_approval = {
        'approval_id': new_approval_id,
        'version_id': latest_version['version_id'],
        'approver': user['username'],
        'status': status,
        'comments': comments,
        'timestamp': timestamp
    }
    append_approval(new_approval)

    flash(f'Approval status "{status}" submitted.')
    return redirect(url_for('article_approval_status', article_id=article_id))


# Publish article if approved
@app.route('/article/<article_id>/publish', methods=['POST'])
@login_required
def article_publish(article_id):
    user = get_current_user()
    article = get_article(article_id)
    if not article:
        abort(404, description='Article not found')

    # Authorization: only Editors, Publisher, Admin can publish
    if user['role'].lower() not in ['editor', 'publisher', 'admin']:
        abort(403)

    # Check approvals for latest version
    versions = get_versions_for_article(article_id)
    if not versions:
        flash('No versions to publish.')
        return redirect(url_for('article_edit', article_id=article_id))

    try:
        versions.sort(key=lambda v: int(v['version_number']), reverse=True)
    except:
        pass
    latest_version = versions[0]

    approvals = get_approvals_for_version(latest_version['version_id'])
    if not approvals:
        flash('Cannot publish without approvals.')
        return redirect(url_for('article_edit', article_id=article_id))

    approved = any(a['status'] == 'approved' for a in approvals)
    if not approved:
        flash('Article has no approved status, cannot publish.')
        return redirect(url_for('article_edit', article_id=article_id))

    # Update article status and publish_date
    articles = get_all_articles()
    for idx, a in enumerate(articles):
        if a['article_id'] == article_id:
            a['status'] = 'published'
            a['publish_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
            articles[idx] = a
            break
    save_articles(articles)

    flash('Article published successfully.')
    return redirect(url_for('articles_published'))


# Submit article for approval workflow
@app.route('/article/<article_id>/submit', methods=['POST'])
@login_required
def article_submit_for_approval(article_id):
    user = get_current_user()
    article = get_article(article_id)
    if not article:
        abort(404, description='Article not found')

    # Only author or editor can submit
    if user['role'].lower() == 'author' and article['author'] != user['username']:
        abort(403)

    # Change status to 'pending approval'
    articles = get_all_articles()
    for idx, a in enumerate(articles):
        if a['article_id'] == article_id:
            a['status'] = 'pending approval'
            articles[idx] = a
            break
    save_articles(articles)

    flash('Article submitted for approval.')
    return redirect(url_for('article_edit', article_id=article_id))


# Article analytics summary
@app.route('/article/<article_id>/analytics')
@login_required
def article_analytics(article_id):
    article = get_article(article_id)
    if not article:
        abort(404, description='Article not found')

    analytics = get_analytics_for_article(article_id)

    return render_template('article_analytics.html', article=article, analytics=analytics)


# Provide analytics data as JSON
@app.route('/article/<article_id>/analytics/data')
@login_required
def article_analytics_data(article_id):
    analytics = get_analytics_for_article(article_id)
    return jsonify(analytics)


# Content calendar view
@app.route('/calendar')
@login_required
def calendar_view():
    entries = get_all_calendar_entries()
    return render_template('content_calendar.html', calendar_entries=entries)


# Provide calendar data as JSON
@app.route('/calendar/data')
@login_required
def calendar_data():
    entries = get_all_calendar_entries()
    return jsonify(entries)


# Save calendar scheduling changes
@app.route('/calendar/save', methods=['POST'])
@login_required
def calendar_save():
    # Expecting JSON data array [{article_id, scheduled_date, notes}, ...]
    data = request.get_json()
    if not data or not isinstance(data, list):
        return jsonify({'error': 'Invalid data format'}), 400

    # Validate and overwrite calendar data
    validated = []
    for entry in data:
        article_id = entry.get('article_id')
        scheduled_date = entry.get('scheduled_date')
        notes = entry.get('notes', '')
        if not article_id or not scheduled_date:
            continue
        validated.append({'article_id': article_id, 'scheduled_date': scheduled_date, 'notes': notes})

    save_calendar_entries(validated)
    return jsonify({'success': True})


# Run if executed as main
if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True, host='0.0.0.0', port=5000)
