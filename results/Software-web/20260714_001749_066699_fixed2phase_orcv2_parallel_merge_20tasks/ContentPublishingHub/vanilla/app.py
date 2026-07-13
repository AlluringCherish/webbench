from flask import Flask, render_template, request, redirect, url_for, session, abort
from datetime import datetime
import os
from threading import Lock

app = Flask(__name__)
app.secret_key = 'supersecretkey'

data_dir = 'data'

# Mutex lock for concurrency safety on file operations
file_lock = Lock()

# Helper functions for data file reading/writing/parsing

def read_users():
    path = os.path.join(data_dir, 'users.txt')
    users = []
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                username, email, fullname, created_date = line.split('|')
                users.append({
                    'username': username,
                    'email': email,
                    'fullname': fullname,
                    'created_date': created_date
                })
    return users


def find_user(username):
    users = read_users()
    for u in users:
        if u['username'] == username:
            return u
    return None


def read_articles():
    path = os.path.join(data_dir, 'articles.txt')
    articles = []
    if not os.path.exists(path):
        return articles
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) != 10:
                    continue
                article_id = int(parts[0])
                articles.append({
                    'article_id': article_id,
                    'title': parts[1],
                    'author': parts[2],
                    'category': parts[3],
                    'status': parts[4],
                    'tags': parts[5].split(',') if parts[5] else [],
                    'featured_image': parts[6],
                    'meta_description': parts[7],
                    'created_date': parts[8],
                    'publish_date': parts[9]
                })
    return articles


def write_articles(articles):
    path = os.path.join(data_dir, 'articles.txt')
    lines = []
    for art in articles:
        line = '|'.join([
            str(art['article_id']),
            art['title'],
            art['author'],
            art['category'],
            art['status'],
            ','.join(art['tags']),
            art['featured_image'],
            art['meta_description'],
            art['created_date'],
            art['publish_date']
        ])
        lines.append(line)
    with file_lock:
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))


def read_article_versions():
    path = os.path.join(data_dir, 'article_versions.txt')
    versions = []
    if not os.path.exists(path):
        return versions
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|', 6)
                if len(parts) != 7:
                    continue
                version_id = int(parts[0])
                article_id = int(parts[1])
                version_number = int(parts[2])
                content = parts[3]
                author = parts[4]
                created_date = parts[5]
                change_summary = parts[6]
                versions.append({
                    'version_id': version_id,
                    'article_id': article_id,
                    'version_number': version_number,
                    'content': content,
                    'author': author,
                    'created_date': created_date,
                    'change_summary': change_summary
                })
    return versions


def write_article_versions(versions):
    path = os.path.join(data_dir, 'article_versions.txt')
    lines = []
    for v in versions:
        # Escape content and change_summary? But spec doesn't define escaping - trust no pipes in text?
        line = '|'.join([
            str(v['version_id']),
            str(v['article_id']),
            str(v['version_number']),
            v['content'],
            v['author'],
            v['created_date'],
            v['change_summary']
        ])
        lines.append(line)
    with file_lock:
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))


def read_approvals():
    path = os.path.join(data_dir, 'approvals.txt')
    approvals = []
    if not os.path.exists(path):
        return approvals
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|', 6)
                if len(parts) != 7:
                    continue
                approval_id = int(parts[0])
                article_id = int(parts[1])
                version_id = int(parts[2])
                approver = parts[3]
                status = parts[4]
                comments = parts[5]
                timestamp = parts[6]
                approvals.append({
                    'approval_id': approval_id,
                    'article_id': article_id,
                    'version_id': version_id,
                    'approver': approver,
                    'status': status,
                    'comments': comments,
                    'timestamp': timestamp
                })
    return approvals


def write_approvals(approvals):
    path = os.path.join(data_dir, 'approvals.txt')
    lines = []
    for a in approvals:
        line = '|'.join([
            str(a['approval_id']),
            str(a['article_id']),
            str(a['version_id']),
            a['approver'],
            a['status'],
            a['comments'],
            a['timestamp']
        ])
        lines.append(line)
    with file_lock:
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))


def read_workflow_stages():
    path = os.path.join(data_dir, 'workflow_stages.txt')
    stages = []
    if not os.path.exists(path):
        return stages
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                stage_id = int(parts[0])
                category = parts[1]
                stage_name = parts[2]
                stage_order = int(parts[3])
                is_required = parts[4]
                stages.append({
                    'stage_id': stage_id,
                    'category': category,
                    'stage_name': stage_name,
                    'stage_order': stage_order,
                    'is_required': is_required
                })
    return stages


def read_comments():
    path = os.path.join(data_dir, 'comments.txt')
    comments = []
    if not os.path.exists(path):
        return comments
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|', 5)
                if len(parts) != 6:
                    continue
                comment_id = int(parts[0])
                article_id = int(parts[1])
                version_id = int(parts[2])
                user = parts[3]
                comment_text = parts[4]
                timestamp = parts[5]
                comments.append({
                    'comment_id': comment_id,
                    'article_id': article_id,
                    'version_id': version_id,
                    'user': user,
                    'comment_text': comment_text,
                    'timestamp': timestamp
                })
    return comments


def write_comments(comments):
    path = os.path.join(data_dir, 'comments.txt')
    lines = []
    for c in comments:
        line = '|'.join([
            str(c['comment_id']),
            str(c['article_id']),
            str(c['version_id']),
            c['user'],
            c['comment_text'],
            c['timestamp']
        ])
        lines.append(line)
    with file_lock:
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))


def read_analytics():
    path = os.path.join(data_dir, 'analytics.txt')
    analytics = []
    if not os.path.exists(path):
        return analytics
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                analytics_id = int(parts[0])
                article_id = int(parts[1])
                date = parts[2]
                views = int(parts[3])
                unique_visitors = int(parts[4])
                avg_time_seconds = int(parts[5])
                shares = int(parts[6])
                analytics.append({
                    'analytics_id': analytics_id,
                    'article_id': article_id,
                    'date': date,
                    'views': views,
                    'unique_visitors': unique_visitors,
                    'avg_time_seconds': avg_time_seconds,
                    'shares': shares
                })
    return analytics


def write_analytics(analytics):
    path = os.path.join(data_dir, 'analytics.txt')
    lines = []
    for a in analytics:
        line = '|'.join([
            str(a['analytics_id']),
            str(a['article_id']),
            a['date'],
            str(a['views']),
            str(a['unique_visitors']),
            str(a['avg_time_seconds']),
            str(a['shares'])
        ])
        lines.append(line)
    with file_lock:
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

# Helpers for ID generation

def get_next_article_id():
    arts = read_articles()
    max_id = max([a['article_id'] for a in arts], default=0)
    return max_id + 1


def get_next_version_id():
    vers = read_article_versions()
    max_id = max([v['version_id'] for v in vers], default=0)
    return max_id + 1


def get_next_approval_id():
    apps = read_approvals()
    max_id = max([a['approval_id'] for a in apps], default=0)
    return max_id + 1


def get_next_comment_id():
    comments = read_comments()
    max_id = max([c['comment_id'] for c in comments], default=0)
    return max_id + 1


def get_next_analytics_id():
    analytics = read_analytics()
    max_id = max([a['analytics_id'] for a in analytics], default=0)
    return max_id + 1

# Authentication and session helpers

def get_current_user():
    # In real app, use flask-login or similar
    # For now, assume session['username'] is set if logged in
    username = session.get('username')
    if username:
        user = find_user(username)
        return user
    return None


def login_required(f):
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not get_current_user():
            return abort(401)  # Unauthorized
        return f(*args, **kwargs)
    return decorated_function

# Business Logic Helpers

def get_article_by_id(article_id):
    articles = read_articles()
    for a in articles:
        if a['article_id'] == article_id:
            return a
    return None


def get_versions_for_article(article_id):
    versions = read_article_versions()
    return [v for v in versions if v['article_id'] == article_id]


def get_latest_version(article_id):
    versions = get_versions_for_article(article_id)
    if not versions:
        return None
    # Latest by version_number
    versions.sort(key=lambda x: x['version_number'], reverse=True)
    return versions[0]


def get_workflow_stages_for_category(category):
    stages = read_workflow_stages()
    cat_stages = [s for s in stages if s['category'] == category]
    cat_stages.sort(key=lambda x: x['stage_order'])
    return cat_stages


def all_required_approved(article_id, version_id, category):
    # Check for all workflow required stages if approvals exist and are approved
    stages = get_workflow_stages_for_category(category)
    approvals = read_approvals()
    for stage in stages:
        if stage['is_required'].lower() != 'yes':
            continue
        approver_approved = False
        # We consider an approval with approved status by any approver in the required stages
        # But spec does not define stage linkage to approver user or name, so just
        # we check if approval record exists with approved for article/version.
        # This is a simplification given design spec lack of stage-to-approver mapping
        for approval in approvals:
            if (
                approval['article_id'] == article_id and
                approval['version_id'] == version_id and
                approval['status'] == 'approved'
            ):
                approver_approved = True
                break
        if not approver_approved:
            return False
    return True


@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    user = get_current_user()
    articles = read_articles()
    username = user['username']

    quick_stats = {
        'total_articles': 0,
        'draft': 0,
        'pending_review': 0,
        'under_review': 0,
        'approved': 0,
        'published': 0,
        'rejected': 0,
        'archived': 0
    }
    recent_activities = []

    # Count articles by status
    for art in articles:
        if art['author'] == username:
            quick_stats['total_articles'] += 1
        if art['status'] in quick_stats:
            if art['author'] == username:
                quick_stats[art['status']] += 1

    # Recent activity feed: last 10 article_versions or approvals or comments linked to user articles
    # We'll gather recent actions from article_versions, approvals, comments in one list sorted by timestamp
    activities = []
    user_articles_ids = {a['article_id'] for a in articles if a['author'] == username}

    versions = read_article_versions()
    for v in versions:
        if v['article_id'] in user_articles_ids:
            activities.append({'type': 'version', 'description': f"Version {v['version_number']} saved", 'timestamp': v['created_date']})

    approvals = read_approvals()
    for a in approvals:
        if a['article_id'] in user_articles_ids:
            activities.append({'type': 'approval', 'description': f"Approval {a['status']} by {a['approver']}", 'timestamp': a['timestamp']})

    comments = read_comments()
    for c in comments:
        if c['article_id'] in user_articles_ids:
            activities.append({'type': 'comment', 'description': f"Comment by {c['user']}", 'timestamp': c['timestamp']})

    # Sort by timestamp desc
    activities.sort(key=lambda x: x['timestamp'], reverse=True)
    recent_activities = activities[:10]

    return render_template('dashboard.html', username=user['fullname'], quick_stats=quick_stats, recent_activities=recent_activities)


@app.route('/article/create', methods=['GET', 'POST'])
@login_required
def create_article():
    user = get_current_user()
    if request.method == 'GET':
        return render_template('create_article.html')

    # POST: Validate and create new article
    title = request.form.get('article_title', '').strip()
    content = request.form.get('article_content', '').strip()
    category = request.form.get('category', 'blog').strip()  # default blog if not present
    tags = request.form.get('tags', '').strip()  # comma separated optional
    tags_list = [t.strip() for t in tags.split(',')] if tags else []
    featured_image = request.form.get('featured_image', '').strip()  # optional
    meta_description = request.form.get('meta_description', '').strip()  # optional

    if not title or not content:
        # Incomplete form
        return render_template('create_article.html', error='Title and content required', article_title=title, article_content=content)

    article_id = get_next_article_id()
    created_date = datetime.now().strftime('%Y-%m-%d')

    new_article = {
        'article_id': article_id,
        'title': title,
        'author': user['username'],
        'category': category if category in ['news', 'blog', 'tutorial', 'announcement', 'press_release'] else 'blog',
        'status': 'draft',
        'tags': tags_list,
        'featured_image': featured_image,
        'meta_description': meta_description,
        'created_date': created_date,
        'publish_date': ''
    }

    articles = read_articles()
    articles.append(new_article)
    write_articles(articles)

    # Create initial version
    version_id = get_next_version_id()
    created_date_full = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    initial_version = {
        'version_id': version_id,
        'article_id': article_id,
        'version_number': 1,
        'content': content,
        'author': user['username'],
        'created_date': created_date_full,
        'change_summary': 'Initial draft'
    }
    versions = read_article_versions()
    versions.append(initial_version)
    write_article_versions(versions)

    # Redirect to own articles list
    return redirect(url_for('my_articles'))


@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    user = get_current_user()
    article = get_article_by_id(article_id)
    if not article:
        abort(404)

    # Only author or admin allowed to edit (spec does not restrict, but common sense)
    if article['author'] != user['username'] and user['username'] != 'admin':
        abort(403)

    latest_version = get_latest_version(article_id)

    if request.method == 'GET':
        # Provide article data and latest version content
        return render_template('edit_article.html',
                               article_id=article_id,
                               article_title=article['title'],
                               article_content=latest_version['content'] if latest_version else '',
                               version_info=latest_version)

    # POST: Save new version
    content = request.form.get('edit-article-content', '').strip()
    title = request.form.get('edit-article-title', '').strip()
    change_summary = request.form.get('change-summary', '').strip()  # Optional

    if not content or not title:
        # Validation error
        return render_template('edit_article.html', article_id=article_id, article_title=title, article_content=content, error='Title and content required')

    versions = read_article_versions()
    new_version_number = 1
    filtered_versions = [v for v in versions if v['article_id'] == article_id]
    if filtered_versions:
        new_version_number = max(v['version_number'] for v in filtered_versions) + 1

    version_id = get_next_version_id()
    created_date_full = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    new_version = {
        'version_id': version_id,
        'article_id': article_id,
        'version_number': new_version_number,
        'content': content,
        'author': user['username'],
        'created_date': created_date_full,
        'change_summary': change_summary or 'Updated version'
    }

    versions.append(new_version)
    write_article_versions(versions)

    # Update article title if changed
    articles = read_articles()
    for art in articles:
        if art['article_id'] == article_id:
            art['title'] = title
            # If status draft, move to pending_review
            if art['status'] == 'draft':
                art['status'] = 'pending_review'
            break
    write_articles(articles)

    return redirect(url_for('edit_article', article_id=article_id))


@app.route('/article/<int:article_id>/versions', methods=['GET', 'POST'])
@login_required
def article_versions(article_id):
    user = get_current_user()
    article = get_article_by_id(article_id)
    if not article:
        abort(404)

    # Only author or admin allowed
    if article['author'] != user['username'] and user['username'] != 'admin':
        abort(403)

    versions = get_versions_for_article(article_id)
    versions = sorted(versions, key=lambda x: x['version_number'], reverse=True)

    if request.method == 'GET':
        # Show all versions with metadata
        # Optionally, if version_id parameter exists, show that content for comparison
        selected_version_id = request.args.get('selected_version_id', type=int)
        selected_version_content = ''
        if selected_version_id:
            for v in versions:
                if v['version_id'] == selected_version_id:
                    selected_version_content = v['content']
                    break
        return render_template('version_history.html',
                               article_id=article_id,
                               versions=versions,
                               selected_version_content_1=selected_version_content)

    # POST - restore action
    restore_version_id = request.form.get('restore_version_id', type=int)
    if not restore_version_id:
        return redirect(url_for('article_versions', article_id=article_id))

    versions = read_article_versions()
    restore_version = None
    for v in versions:
        if v['version_id'] == restore_version_id:
            restore_version = v
            break
    if not restore_version:
        abort(404)

    # Create new version entry copying restored version content
    new_version_id = get_next_version_id()
    new_version_number = max([v['version_number'] for v in versions if v['article_id'] == article_id], default=0) + 1
    created_date_full = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    new_version = {
        'version_id': new_version_id,
        'article_id': article_id,
        'version_number': new_version_number,
        'content': restore_version['content'],
        'author': user['username'],
        'created_date': created_date_full,
        'change_summary': f"Restored version {restore_version['version_number']}"
    }

    versions.append(new_version)
    write_article_versions(versions)

    return redirect(url_for('article_versions', article_id=article_id))


@app.route('/articles/mine', methods=['GET'])
@login_required
def my_articles():
    user = get_current_user()
    status_filter = request.args.get('status', None)
    articles = read_articles()
    user_articles = [a for a in articles if a['author'] == user['username']]
    if status_filter:
        user_articles = [a for a in user_articles if a['status'] == status_filter]

    status_options = ['draft', 'pending_review', 'under_review', 'approved', 'published', 'rejected', 'archived']

    return render_template('my_articles.html', user_articles=user_articles, status_options=status_options)


@app.route('/articles/published', methods=['GET'])
@login_required
def published_articles():
    category_filter = request.args.get('category', None)
    sort_option = request.args.get('sort', None)  # e.g. date, popularity
    articles = read_articles()
    published = [a for a in articles if a['status'] == 'published']

    if category_filter:
        published = [a for a in published if a['category'] == category_filter]

    if sort_option == 'date':
        # Sort by publish_date descending
        published.sort(key=lambda x: x['publish_date'] or '', reverse=True)
    # Popularity sort not defined with data, so ignore or later extend

    category_options = ['news', 'blog', 'tutorial', 'announcement', 'press_release']
    sort_options = ['date', 'popularity']

    return render_template('published_articles.html', published_articles=published, category_options=category_options, sort_options=sort_options)


@app.route('/calendar', methods=['GET', 'POST'])
@login_required
def content_calendar():
    if request.method == 'GET':
        # Show scheduled publication dates with articles
        calendar_view_options = ['day', 'week', 'month']
        articles = read_articles()
        scheduled_items = []
        for a in articles:
            if a['publish_date']:
                scheduled_items.append({
                    'article_id': a['article_id'],
                    'title': a['title'],
                    'publish_date': a['publish_date']
                })
        return render_template('content_calendar.html', calendar_view_options=calendar_view_options, scheduled_items=scheduled_items)

    # POST: Schedule or reschedule article publish date
    article_id = request.form.get('article_id', type=int)
    publish_date = request.form.get('publish_date', '').strip()  # Expected format: YYYY-MM-DD HH:MM:SS
    if not article_id or not publish_date:
        return redirect(url_for('content_calendar'))

    try:
        datetime.strptime(publish_date, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        # Invalid date format
        return redirect(url_for('content_calendar'))

    articles = read_articles()
    updated = False
    for a in articles:
        if a['article_id'] == article_id:
            a['publish_date'] = publish_date
            updated = True
            break
    if updated:
        write_articles(articles)

    return redirect(url_for('content_calendar'))


@app.route('/article/<int:article_id>/analytics', methods=['GET'])
@login_required
def article_analytics(article_id):
    article = get_article_by_id(article_id)
    if not article:
        abort(404)

    analytics = read_analytics()
    filtered = [a for a in analytics if a['article_id'] == article_id]

    if not filtered:
        analytics_summary = {
            'total_views': 0,
            'unique_visitors': 0,
            'avg_time_seconds': 0,
            'shares': 0
        }
    else:
        total_views = sum(a['views'] for a in filtered)
        total_unique_visitors = sum(a['unique_visitors'] for a in filtered)
        if total_unique_visitors > 0:
            avg_time = int(sum(a['avg_time_seconds'] * a['unique_visitors'] for a in filtered) / total_unique_visitors)
        else:
            avg_time = 0
        total_shares = sum(a['shares'] for a in filtered)

        analytics_summary = {
            'total_views': total_views,
            'unique_visitors': total_unique_visitors,
            'avg_time_seconds': avg_time,
            'shares': total_shares
        }

    return render_template('article_analytics.html', article_id=article_id, analytics_summary=analytics_summary)


if __name__ == '__main__':
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    app.run(debug=True)
