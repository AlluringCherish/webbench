from flask import Flask, render_template, request, redirect, url_for, session, abort
from datetime import datetime
import os
import threading
import difflib

app = Flask(__name__)
app.secret_key = 'super_secret_key_change_me'  # Session secret key

DATA_DIR = 'data'
file_lock = threading.Lock()

# Utility functions for file operations

def read_pipe_delimited_file(filename, fields):
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path):
        return []
    records = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != len(fields):
                continue
            record = dict(zip(fields, parts))
            records.append(record)
    return records


def append_pipe_delimited_file(filename, fields, record):
    file_path = os.path.join(DATA_DIR, filename)
    with file_lock:
        with open(file_path, 'a', encoding='utf-8') as f:
            line = '|'.join(str(record.get(field, '')).replace('\n', ' ') for field in fields)
            f.write(line + '\n')


def overwrite_pipe_delimited_file(filename, fields, records):
    file_path = os.path.join(DATA_DIR, filename)
    with file_lock:
        with open(file_path, 'w', encoding='utf-8') as f:
            for record in records:
                line = '|'.join(str(record.get(field, '')).replace('\n', ' ') for field in fields)
                f.write(line + '\n')

# Data models and fields

USER_FIELDS = ['id', 'username', 'role']

ARTICLE_FIELDS = ['article_id', 'title', 'author', 'category', 'status', 'created_date', 'last_modified']

ARTICLE_VERSION_FIELDS = ['version_id', 'article_id', 'version_number', 'content', 'author', 'created_date', 'change_summary']

APPROVAL_FIELDS = ['approval_id', 'article_id', 'version_id', 'approver', 'status', 'comment', 'timestamp']

COMMENT_FIELDS = ['comment_id', 'article_id', 'version_id', 'author', 'comment_text', 'timestamp']

WORKFLOW_STAGE_FIELDS = ['stage_id', 'name', 'required_reviewers']

ANALYTICS_FIELDS = ['analytics_id', 'article_id', 'date', 'views', 'unique_visitors', 'average_time_spent', 'shares']


# Authentication

def get_logged_in_username():
    return session.get('username')


# User management

def get_all_users():
    return read_pipe_delimited_file('users.txt', USER_FIELDS)


def get_user_by_username(username):
    users = get_all_users()
    for user in users:
        if user['username'] == username:
            return user
    return None


# Article management

def get_all_articles():
    return read_pipe_delimited_file('articles.txt', ARTICLE_FIELDS)


def get_article_by_id(article_id):
    articles = get_all_articles()
    for article in articles:
        if article.get('article_id') == str(article_id):
            return article
    return None


def save_all_articles(articles):
    overwrite_pipe_delimited_file('articles.txt', ARTICLE_FIELDS, articles)


def create_article(title, author, category):
    articles = get_all_articles()
    max_id = max((int(a['article_id']) for a in articles), default=0)
    new_id = max_id + 1
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_article = {
        'article_id': str(new_id),
        'title': title,
        'author': author,
        'category': category if category else '',
        'status': 'draft',
        'created_date': now_str,
        'last_modified': now_str
    }
    articles.append(new_article)
    save_all_articles(articles)
    return new_article['article_id']


def update_article(article_id, title=None, status=None, last_modified=None):
    articles = get_all_articles()
    updated = False
    for article in articles:
        if article['article_id'] == str(article_id):
            if title is not None:
                article['title'] = title
            if status is not None:
                article['status'] = status
            if last_modified is not None:
                article['last_modified'] = last_modified
            updated = True
            break
    if updated:
        save_all_articles(articles)
    return updated


# Article versions

def get_all_article_versions():
    return read_pipe_delimited_file('article_versions.txt', ARTICLE_VERSION_FIELDS)


def get_versions_by_article_id(article_id):
    versions = get_all_article_versions()
    filtered = [v for v in versions if v['article_id'] == str(article_id)]
    filtered.sort(key=lambda v: int(v['version_number']))
    return filtered


def get_latest_version(article_id):
    versions = get_versions_by_article_id(article_id)
    if not versions:
        return None
    return max(versions, key=lambda v: int(v['version_number']))


def create_new_version(article_id, content, author, change_summary=''):
    versions = get_all_article_versions()
    max_version_num = 0
    for v in versions:
        if v['article_id'] == str(article_id):
            max_version_num = max(max_version_num, int(v['version_number']))
    new_version_num = max_version_num + 1
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_version = {
        'version_id': str(len(versions) + 1),
        'article_id': str(article_id),
        'version_number': str(new_version_num),
        'content': content,
        'author': author,
        'created_date': now_str,
        'change_summary': change_summary
    }
    append_pipe_delimited_file('article_versions.txt', ARTICLE_VERSION_FIELDS, new_version)
    return new_version


# Approvals

def get_all_approvals():
    return read_pipe_delimited_file('approvals.txt', APPROVAL_FIELDS)


def get_approvals_by_article_id(article_id):
    approvals = get_all_approvals()
    filtered = [a for a in approvals if a['article_id'] == str(article_id)]
    return filtered


def create_approval(article_id, version_id, approver, status, comment=''):
    approvals = get_all_approvals()
    max_id = max((int(a['approval_id']) for a in approvals), default=0)
    new_id = max_id + 1
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    approval_record = {
        'approval_id': str(new_id),
        'article_id': str(article_id),
        'version_id': str(version_id),
        'approver': approver,
        'status': status,
        'comment': comment,
        'timestamp': now_str
    }
    append_pipe_delimited_file('approvals.txt', APPROVAL_FIELDS, approval_record)
    return approval_record


# Comments

def get_all_comments():
    return read_pipe_delimited_file('comments.txt', COMMENT_FIELDS)


def get_comments_by_article_and_version(article_id, version_id):
    comments = get_all_comments()
    filtered = [c for c in comments if c['article_id'] == str(article_id) and c['version_id'] == str(version_id)]
    filtered.sort(key=lambda c: c['timestamp'])
    return filtered


def create_comment(article_id, version_id, author, comment_text):
    comments = get_all_comments()
    max_id = max((int(c['comment_id']) for c in comments), default=0)
    new_id = max_id + 1
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    comment_record = {
        'comment_id': str(new_id),
        'article_id': str(article_id),
        'version_id': str(version_id),
        'author': author,
        'comment_text': comment_text,
        'timestamp': now_str
    }
    append_pipe_delimited_file('comments.txt', COMMENT_FIELDS, comment_record)
    return comment_record


# Workflow stages

def get_workflow_stages():
    return read_pipe_delimited_file('workflow_stages.txt', WORKFLOW_STAGE_FIELDS)


# Analytics

def get_all_analytics():
    return read_pipe_delimited_file('analytics.txt', ANALYTICS_FIELDS)


def aggregate_analytics(article_id):
    analytics = get_all_analytics()
    filtered = [a for a in analytics if a['article_id'] == str(article_id)]
    total_views = 0
    unique_dates = set()
    total_time = 0.0
    total_shares = 0
    for rec in filtered:
        try:
            total_views += int(rec.get('views', 0))
        except:
            pass
        unique_dates.add(rec.get('date', ''))
        try:
            total_time += float(rec.get('average_time_spent', 0))
        except:
            pass
        try:
            total_shares += int(rec.get('shares', 0))
        except:
            pass
    avg_time = 0
    if filtered:
        avg_time = total_time / len(filtered)
    analytics_summary = {
        'Total Views': total_views,
        'Unique Visit Days': len(unique_dates),
        'Average Time on Article (s)': round(avg_time, 2),
        'Total Shares': total_shares
    }
    return analytics_summary


# Diff helper for version comparison

def generate_diff_summary(old_content, new_content):
    diff = difflib.unified_diff(
        old_content.splitlines(),
        new_content.splitlines(),
        fromfile='Old Version',
        tofile='New Version',
        lineterm=''
    )
    return '\n'.join(diff)


# Routes

@app.route('/')
def index():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('index'))

    all_articles = get_all_articles()
    user_articles = [a for a in all_articles if a['author'] == username]
    published_count = sum(1 for a in user_articles if a['status'] == 'published')
    approval_count = sum(1 for a in user_articles if a['status'] == 'pending_review')

    quick_stats = {
        'Total Articles': len(user_articles),
        'Published Articles': published_count,
        'Articles Pending Approval': approval_count
    }

    recent_activity_raw = sorted(
        user_articles, key=lambda a: a['last_modified'], reverse=True)[:5]

    recent_activity = []
    for art in recent_activity_raw:
        recent_activity.append({
            'title': art['title'],
            'description': f'Status: {art["status"]}',
            'date': art['last_modified']
        })

    return render_template('dashboard.html', username=username, quick_stats=quick_stats, recent_activity=recent_activity)


@app.route('/article/create', methods=['GET', 'POST'])
def create_article():
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form.get('article_title', '').strip()
        content = request.form.get('article_content', '').strip()

        errors = []
        if not title:
            errors.append('Title is required.')
        if not content:
            errors.append('Content is required.')

        if errors:
            return render_template('create_article.html', error_message=' '.join(errors))

        # Create article
        new_article_id = create_article(title, username, '')
        create_new_version(new_article_id, content, username, change_summary='Initial version')

        success_message = 'Article created successfully.'
        return render_template('create_article.html', success_message=success_message)

    return render_template('create_article.html')


@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('index'))

    article = get_article_by_id(article_id)
    if not article:
        abort(404, description='Article not found')
    if article['author'] != username:
        abort(403, description='Permission denied: can only edit own articles')

    latest_version = get_latest_version(article_id)
    title = article['title']
    content = latest_version['content'] if latest_version else ''

    if request.method == 'POST':
        new_title = request.form.get('article_title', '').strip()
        new_content = request.form.get('article_content', '').strip()
        change_summary = request.form.get('change_summary', '').strip()

        errors = []
        if not new_title:
            errors.append('Title is required.')
        if not new_content:
            errors.append('Content is required.')

        if errors:
            return render_template('edit_article.html', article_id=article_id, title=new_title, content=new_content, error_message=' '.join(errors))

        create_new_version(article_id, new_content, username, change_summary)
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        update_article(article_id, title=new_title, last_modified=now_str)

        success_message = 'Article updated and saved successfully.'
        return render_template('edit_article.html', article_id=article_id, title=new_title, content=new_content, success_message=success_message)

    return render_template('edit_article.html', article_id=article_id, title=title, content=content)


@app.route('/article/<int:article_id>/versions')
def article_version_history(article_id):
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('index'))

    article = get_article_by_id(article_id)
    if not article:
        abort(404, description='Article not found')

    versions = get_versions_by_article_id(article_id)
    current_version_num = int(request.args.get('version', versions[-1]['version_number'] if versions else '0'))

    # Sort versions
    versions_sorted = sorted(versions, key=lambda v: int(v['version_number']))

    # Prepare comparison diff
    comparison = None
    current_version = None
    for v in versions:
        if int(v['version_number']) == current_version_num:
            current_version = v
            break

    if current_version_num > 1:
        old_version = None
        new_version = None
        for i, v in enumerate(versions_sorted):
            if int(v['version_number']) == current_version_num - 1:
                old_version = v
            if int(v['version_number']) == current_version_num:
                new_version = v
        if old_version and new_version:
            diff_text = generate_diff_summary(old_version['content'], new_version['content'])
            comparison = {'diff_text': diff_text}

    return render_template('version_history.html', article_id=article_id, versions=versions_sorted, comparison=comparison, current_version=current_version_num)


@app.route('/articles/mine')
def my_articles():
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('index'))

    filter_status = request.args.get('filter_status', '').lower()
    all_articles = get_all_articles()
    user_articles = [a for a in all_articles if a['author'] == username]
    if filter_status:
        user_articles = [a for a in user_articles if a['status'].lower() == filter_status]

    return render_template('my_articles.html', articles=user_articles, filter_status=filter_status)


@app.route('/articles/published')
def published_articles():
    sort_option = request.args.get('sort_option', 'date_desc')
    filter_category = request.args.get('filter_category', '').lower()

    all_articles = get_all_articles()
    published = [a for a in all_articles if a['status'].lower() == 'published']

    if filter_category:
        published = [a for a in published if a['category'].lower() == filter_category]

    if sort_option == 'date_asc':
        published.sort(key=lambda a: a['created_date'])
    elif sort_option == 'date_desc':
        published.sort(key=lambda a: a['created_date'], reverse=True)
    elif sort_option == 'title_asc':
        published.sort(key=lambda a: a['title'].lower())
    elif sort_option == 'title_desc':
        published.sort(key=lambda a: a['title'].lower(), reverse=True)

    return render_template('published_articles.html', articles=published, sort_option=sort_option, filter_category=filter_category)


@app.route('/content_calendar', methods=['GET', 'POST'])
def content_calendar():
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('index'))

    calendar_view = 'monthly'
    calendar_data = []

    if request.method == 'POST':
        calendar_view = request.form.get('calendar_view', 'monthly')

    # Stub for calendar data
    # In real app, load scheduled articles or events
    calendar_data = [
        {'title': 'Article 1', 'date': '2024-06-01', 'description': 'Scheduled Publish'},
        {'title': 'Article 2', 'date': '2024-06-15', 'description': 'Scheduled Review'},
    ]

    return render_template('content_calendar.html', calendar_view=calendar_view, calendar_data=calendar_data)


@app.route('/article/<int:article_id>/analytics')
def article_analytics(article_id):
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('index'))

    article = get_article_by_id(article_id)
    if not article:
        abort(404, description='Article not found')

    analytics_summary = aggregate_analytics(article_id)

    return render_template('article_analytics.html', article_id=article_id, analytics=analytics_summary)


@app.route('/article/<int:article_id>/version/<int:version_id>/comments', methods=['GET', 'POST'])
def article_version_comments(article_id, version_id):
    username = get_logged_in_username()
    if not username:
        return redirect(url_for('index'))

    if request.method == 'GET':
        comments = get_comments_by_article_and_version(article_id, version_id)
        return render_template('comments.html', article_id=article_id, version_id=version_id, comments=comments)

    if request.method == 'POST':
        comment_text = request.form.get('comment_text', '').strip()
        errors = []
        if not comment_text:
            errors.append('Comment text is required.')

        if errors:
            comments = get_comments_by_article_and_version(article_id, version_id)
            return render_template('comments.html', article_id=article_id, version_id=version_id, comments=comments, errors=errors)

        create_comment(article_id, version_id, username, comment_text)
        success_message = 'Comment added successfully.'
        comments = get_comments_by_article_and_version(article_id, version_id)
        return render_template('comments.html', article_id=article_id, version_id=version_id, comments=comments, success_message=success_message)


if __name__ == '__main__':
    app.run(debug=True)
