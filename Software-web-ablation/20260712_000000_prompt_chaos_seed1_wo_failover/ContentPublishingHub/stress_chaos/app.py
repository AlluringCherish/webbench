from flask import Flask, request, session, redirect, url_for, render_template, jsonify, flash
import os
import datetime
import threading

app = Flask(__name__)
app.secret_key = 'supersecretkey123'

DATA_DIR = 'data'

ARTICLE_VERSIONS_FILE = os.path.join(DATA_DIR, 'article_versions.txt')
APPROVALS_FILE = os.path.join(DATA_DIR, 'approvals.txt')
COMMENTS_FILE = os.path.join(DATA_DIR, 'comments.txt')
WORKFLOW_STAGES_FILE = os.path.join(DATA_DIR, 'workflow_stages.txt')

# Thread lock for file access
file_lock = threading.Lock()

# Utility functions to safely read/write with locks

def safe_read_lines(filepath):
    with file_lock:
        if not os.path.exists(filepath):
            return []
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.readlines()

def safe_write_lines(filepath, lines):
    with file_lock:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)

##### Data Model Layers #####

def parse_article_versions():
    # Returns dict: article_id -> list of versions ({version, timestamp, summary, content}) ordered by version
    lines = safe_read_lines(ARTICLE_VERSIONS_FILE)
    articles = {}
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) < 5:
            continue
        article_id, version_str, timestamp, summary, content = parts
        try:
            version = int(version_str)
        except ValueError:
            continue
        articles.setdefault(article_id, []).append({
            'version': version,
            'timestamp': timestamp,
            'summary': summary,
            'content': content
        })
    # Sort versions by version number
    for article_id in articles:
        articles[article_id].sort(key=lambda v: v['version'])
    return articles

def save_article_versions(articles):
    lines = []
    for article_id, versions in articles.items():
        for v in versions:
            line = f"{article_id}|{v['version']}|{v['timestamp']}|{v['summary']}|{v['content']}\n"
            lines.append(line)
    safe_write_lines(ARTICLE_VERSIONS_FILE, lines)

def parse_approvals():
    # Returns dict (article_id, version) -> list of approvals ({approver, status, comments})
    lines = safe_read_lines(APPROVALS_FILE)
    approvals = {}
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) < 5:
            continue
        article_id, version_str, approver, status, comments = parts
        try:
            version = int(version_str)
        except ValueError:
            continue
        key = (article_id, version)
        approvals.setdefault(key, []).append({
            'approver': approver,
            'status': status,
            'comments': comments
        })
    return approvals

def save_approvals(approvals):
    lines = []
    for (article_id, version), records in approvals.items():
        for r in records:
            line = f"{article_id}|{version}|{r['approver']}|{r['status']}|{r['comments']}\n"
            lines.append(line)
    safe_write_lines(APPROVALS_FILE, lines)

def parse_comments():
    # Returns dict (article_id, version) -> list of comments ({commenter, timestamp, text})
    lines = safe_read_lines(COMMENTS_FILE)
    comments = {}
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) < 5:
            continue
        article_id, version_str, commenter, timestamp, comment_text = parts
        try:
            version = int(version_str)
        except ValueError:
            continue
        key = (article_id, version)
        comments.setdefault(key, []).append({
            'commenter': commenter,
            'timestamp': timestamp,
            'text': comment_text
        })
    return comments

def save_comments(comments):
    lines = []
    for (article_id, version), entries in comments.items():
        for c in entries:
            line = f"{article_id}|{version}|{c['commenter']}|{c['timestamp']}|{c['text']}\n"
            lines.append(line)
    safe_write_lines(COMMENTS_FILE, lines)

def parse_workflow_stages():
    # Returns dict: category -> list of required approval roles (ordered)
    lines = safe_read_lines(WORKFLOW_STAGES_FILE)
    stages = {}
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) < 2:
            continue
        category = parts[0]
        # roles separated by commas
        roles = parts[1].split(',')
        stages[category] = [r.strip() for r in roles if r.strip()]
    return stages

##### Business Logic / Service Layer #####

def get_current_user():
    # For demo, a simple user stored in session
    return session.get('username', 'guest')

def require_login():
    if 'username' not in session:
        flash('Login required')
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if username:
            session['username'] = username
            flash(f'Logged in as {username}')
            return redirect(url_for('dashboard'))
        else:
            flash('Username required')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out')
    return redirect(url_for('login'))

@app.route('/')
def home_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    # Show recent user activity (versions edited, approvals given)
    articles = parse_article_versions()
    approvals = parse_approvals()
    recent_activity = []
    # Activity: user is author (assumed author username equals article id for demo), or approver
    for article_id, versions in articles.items():
        for v in versions[-5:]:
            recent_activity.append({
                'type': 'version',
                'user': user,
                'article_id': article_id,
                'version': v['version'],
                'summary': v['summary'],
                'timestamp': v['timestamp']
            })
    # Include approvals by user
    for (article_id, version), recs in approvals.items():
        for rec in recs:
            if rec['approver'] == user:
                recent_activity.append({
                    'type': 'approval',
                    'article_id': article_id,
                    'version': version,
                    'status': rec['status'],
                    'comments': rec['comments'],
                })
    recent_activity = sorted(recent_activity, key=lambda x: x.get('timestamp', '') or '', reverse=True)
    return render_template('dashboard.html', user=user, recent_activity=recent_activity)

@app.route('/article/create', methods=['GET', 'POST'])
def article_create():
    user = get_current_user()
    if request.method == 'POST':
        article_id = request.form.get('article_id', '').strip()
        summary = request.form.get('summary', '').strip()
        content = request.form.get('content', '').strip()

        if not article_id or not content:
            flash('Article ID and content are required')
            return render_template('article_create.html')

        articles = parse_article_versions()
        if article_id in articles:
            flash('Article already exists, use edit')
            return render_template('article_create.html')

        timestamp = datetime.datetime.utcnow().isoformat()
        version = 1
        articles.setdefault(article_id, []).append({
            'version': version,
            'timestamp': timestamp,
            'summary': summary,
            'content': content
        })
        save_article_versions(articles)

        flash('Article created')
        return redirect(url_for('article_edit', article_id=article_id))

    return render_template('article_create.html')

@app.route('/article/<article_id>/edit', methods=['GET', 'POST'])
def article_edit(article_id):
    user = get_current_user()
    articles = parse_article_versions()
    if article_id not in articles:
        flash('Article not found')
        return redirect(url_for('article_create'))

    versions = articles[article_id]
    latest = versions[-1]

    if request.method == 'POST':
        summary = request.form.get('summary', '').strip()
        content = request.form.get('content', '').strip()
        if not content:
            flash('Content cannot be empty')
            return render_template('article_edit.html', article_id=article_id, version=latest['version'], summary=latest['summary'], content=latest['content'])

        new_version_num = latest['version'] + 1
        timestamp = datetime.datetime.utcnow().isoformat()
        new_version = {
            'version': new_version_num,
            'timestamp': timestamp,
            'summary': summary,
            'content': content
        }
        versions.append(new_version)
        save_article_versions(articles)
        flash('New version saved')
        return redirect(url_for('article_versions', article_id=article_id))

    return render_template('article_edit.html', article_id=article_id, version=latest['version'], summary=latest['summary'], content=latest['content'])

@app.route('/article/<article_id>/versions')
def article_versions(article_id):
    user = get_current_user()
    articles = parse_article_versions()
    if article_id not in articles:
        flash('Article not found')
        return redirect(url_for('dashboard'))

    versions = articles[article_id]
    approvals = parse_approvals()
    comments = parse_comments()

    # Attach approvals and comments per version
    version_data = []
    for v in versions:
        vnum = v['version']
        vappr = approvals.get((article_id, vnum), [])
        vcomm = comments.get((article_id, vnum), [])
        version_data.append({
            'version': vnum,
            'timestamp': v['timestamp'],
            'summary': v['summary'],
            'content': v['content'],
            'approvals': vappr,
            'comments': vcomm
        })

    return render_template('article_versions.html', article_id=article_id, versions=version_data)

@app.route('/article/<article_id>/approve', methods=['POST'])
def article_approve(article_id):
    user = get_current_user()

    version_str = request.form.get('version', '').strip()
    status = request.form.get('status', '').strip()
    comments = request.form.get('comments', '').strip()

    if not version_str.isdigit():
        flash('Invalid version')
        return redirect(url_for('article_versions', article_id=article_id))
    version = int(version_str)

    if not status:
        flash('Approval status required')
        return redirect(url_for('article_versions', article_id=article_id))

    approvals = parse_approvals()
    approvals.setdefault((article_id, version), []).append({
        'approver': user,
        'status': status,
        'comments': comments
    })
    save_approvals(approvals)
    flash(f'Approval recorded for version {version}')
    return redirect(url_for('article_versions', article_id=article_id))

@app.route('/article/<article_id>/comment', methods=['POST'])
def article_comment(article_id):
    user = get_current_user()
    version_str = request.form.get('version', '').strip()
    comment = request.form.get('comment', '').strip()
    if not version_str.isdigit() or not comment:
        flash('Invalid comment or version')
        return redirect(url_for('article_versions', article_id=article_id))
    version = int(version_str)

    comments = parse_comments()
    timestamp = datetime.datetime.utcnow().isoformat()
    comments.setdefault((article_id, version), []).append({
        'commenter': user,
        'timestamp': timestamp,
        'text': comment
    })
    save_comments(comments)
    flash('Comment added')
    return redirect(url_for('article_versions', article_id=article_id))

@app.route('/articles/mine')
def my_articles():
    user = get_current_user()
    articles = parse_article_versions()
    # Filter articles where user is author (for demo we assume author is article_id)
    user_articles = {aid: v for aid, v in articles.items() if aid == user}
    # Convert to list of dicts with id, title, status
    articles_list = []
    for aid, versions in user_articles.items():
        latest_ver = versions[-1]
        articles_list.append({
            'id': aid,
            'title': latest_ver['summary'],
            'status': 'Draft'
        })
    return render_template('my_articles.html', user=user, articles=articles_list)

@app.route('/articles/published')
def articles_published():
    # Show all articles where latest version is approved
    articles = parse_article_versions()
    approvals = parse_approvals()
    published_articles = []
    for aid, versions in articles.items():
        latest_version = versions[-1]['version']
        # Check if latest version approved with status 'Approved'
        approved = False
        key = (aid, latest_version)
        for appr in approvals.get(key, []):
            if appr['status'].lower() == 'approved':
                approved = True
                break
        if approved:
            latest_ver = versions[-1]
            published_articles.append({
                'id': aid,
                'title': latest_ver['summary'],
                'published_date': latest_ver['timestamp']
            })
    return render_template('published_articles.html', published_articles=published_articles)

@app.route('/calendar')
def calendar():
    # Show calendar view of all article versions by date
    articles = parse_article_versions()
    calendar_items = []
    for article_id, versions in articles.items():
        for v in versions:
            timestamp = v['timestamp']
            try:
                dt = datetime.datetime.fromisoformat(timestamp)
            except Exception:
                dt = None
            calendar_items.append({
                'article_title': v['summary'],
                'date': dt.date().isoformat() if dt else ''
            })
    return render_template('content_calendar.html', calendar_items=calendar_items)

@app.route('/article/<article_id>/analytics')
def article_analytics(article_id):
    articles = parse_article_versions()
    approvals = parse_approvals()
    comments = parse_comments()
    if article_id not in articles:
        flash('Article not found')
        return redirect(url_for('dashboard'))

    versions = articles[article_id]

    total_versions = len(versions)
    total_approvals = 0
    approval_counts = {}
    approvers_set = set()
    total_comments = 0

    for v in versions:
        vnum = v['version']
        key = (article_id, vnum)
        approval_list = approvals.get(key, [])
        total_approvals += len(approval_list)
        for a in approval_list:
            approvers_set.add(a['approver'])
            approval_counts[a['status']] = approval_counts.get(a['status'], 0) + 1

        comment_list = comments.get(key, [])
        total_comments += len(comment_list)

    analytics = {
        'article_id': article_id,
        'total_versions': total_versions,
        'total_approvals': total_approvals,
        'approval_counts': approval_counts,
        'unique_approvers_count': len(approvers_set),
        'total_comments': total_comments
    }

    # Adjusted to provide data structure for template
    analytics_summary = f"Analytics for article {article_id}"
    analytics_entries = [
        {'metric': 'Total Versions', 'value': total_versions},
        {'metric': 'Total Approvals', 'value': total_approvals},
        {'metric': 'Unique Approvers', 'value': len(approvers_set)},
        {'metric': 'Total Comments', 'value': total_comments}
    ]

    # Include individual status counts
    for status, count in approval_counts.items():
        analytics_entries.append({'metric': f"Approvals with status '{status}'", 'value': count})

    return render_template('article_analytics.html', analytics_summary=analytics_summary, analytics_entries=analytics_entries)

if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(debug=True)
