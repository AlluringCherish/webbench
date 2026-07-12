from flask import Flask, request, render_template, redirect, url_for, session, abort
import os
import datetime
import threading
from functools import wraps
import calendar

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with config or environment variable

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# Ensure data directory and basic files exist
if not os.path.exists(data_dir):
    os.makedirs(data_dir, exist_ok=True)

# Ensure empty data files exist to prevent FileNotFoundError
required_data_files = [
    'users.txt', 'articles.txt', 'article_versions.txt',
    'approvals.txt', 'comments.txt', 'workflow_stages.txt', 'analytics.txt'
]
for filename in required_data_files:
    path = os.path.join(data_dir, filename)
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            pass  # create empty file

# Locks for concurrency safe writing
# lock keyed by filename prefix

data_locks = {
    'users': threading.Lock(),
    'articles': threading.Lock(),
    'article_versions': threading.Lock(),
    'approvals': threading.Lock(),
    'comments': threading.Lock(),
    'workflow_stages': threading.Lock(),
    'analytics': threading.Lock(),
}

# Helper functions for file path resolution

def data_path(filename):
    return os.path.join(data_dir, filename)

# =================================================================================
# Utils: file read/write helpers
# =================================================================================

def read_pipe_delimited_file(filename, keys):
    path = data_path(filename)
    data = []
    if not os.path.exists(path):
        return data
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != len(keys):
                continue  # discard malformed
            record = dict(zip(keys, parts))
            data.append(record)
    return data


def append_pipe_delimited_file(filename, keys, record_dict):
    # write one record as pipe delimited line
    path = data_path(filename)
    line = '|'.join(str(record_dict.get(k, '')).replace('\n',' ').replace('|',' ')
                    for k in keys)
    line += '\n'
    lock_name = filename.split('.')[0]
    lock = data_locks.get(lock_name)
    if lock:
        lock.acquire()
    try:
        with open(path, 'a', encoding='utf-8') as f:
            f.write(line)
    finally:
        if lock:
            lock.release()


def overwrite_pipe_delimited_file(filename, keys, records):
    # records: list of dict
    path = data_path(filename)
    lock_name = filename.split('.')[0]
    lock = data_locks.get(lock_name)
    if lock:
        lock.acquire()
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for rec in records:
                line = '|'.join(str(rec.get(k, '')).replace('\n',' ').replace('|',' ') for k in keys)
                f.write(line + '\n')
    finally:
        if lock:
            lock.release()

# =================================================================================
# Data Model Access Helpers
# =================================================================================

##### Users
# users.txt fields: username|fullname|email|role
user_keys = ['username','fullname','email','role']

def get_all_users():
    return read_pipe_delimited_file('users.txt', user_keys)

def get_user(username):
    users = get_all_users()
    for u in users:
        if u['username'] == username:
            return u
    return None

##### Articles
# articles.txt fields: article_id|author|title|category|status|created_date|updated_date
article_keys = ['article_id','author','title','category','status','created_date','updated_date']

def get_all_articles():
    return read_pipe_delimited_file('articles.txt', article_keys)

def get_article(article_id):
    articles = get_all_articles()
    for art in articles:
        if art['article_id'] == str(article_id):
            return art
    return None

# Save or update an article (overwrite full file)
def save_articles(articles):
    overwrite_pipe_delimited_file('articles.txt', article_keys, articles)

# Add a new article and return article_id (int) assigned
def add_article(author, title, category, status):
    articles = get_all_articles()
    # New article_id: max existing +1 or 1
    max_id = 0
    for a in articles:
        try:
            aid = int(a['article_id'])
            if aid > max_id:
                max_id = aid
        except:
            pass
    new_id = max_id + 1
    now = datetime.datetime.utcnow().isoformat()
    new_article = {
        'article_id': str(new_id),
        'author': author,
        'title': title,
        'category': category,
        'status': status,
        'created_date': now,
        'updated_date': now
    }
    articles.append(new_article)
    save_articles(articles)
    return new_id

# Update article fields and save
# Should be used to update status, title, category, updated_date
# article_id must exist
# Return True on success, False otherwise
# Note: article is modified in place

def update_article(article_id, **kwargs):
    articles = get_all_articles()
    updated = False
    now = datetime.datetime.utcnow().isoformat()
    for art in articles:
        if art['article_id'] == str(article_id):
            for k,v in kwargs.items():
                if k in article_keys and v is not None:
                    art[k] = v
            art['updated_date'] = now
            updated = True
            break
    if updated:
        save_articles(articles)
    return updated

##### Article Versions
# article_versions.txt fields:
# version_id|article_id|version_number|content|author|created_date|change_summary
article_version_keys = ['version_id','article_id','version_number','content','author','created_date','change_summary']

def get_all_article_versions():
    return read_pipe_delimited_file('article_versions.txt', article_version_keys)

def get_versions_for_article(article_id):
    version_list = []
    versions = get_all_article_versions()
    for v in versions:
        if v['article_id'] == str(article_id):
            version_list.append(v)
    # Sort by version_number int ascending
    try:
        version_list.sort(key=lambda x: int(x['version_number']))
    except:
        pass
    return version_list

# Generate new version_id (int unique max+1) for article_versions

def next_version_id():
    versions = get_all_article_versions()
    max_id = 0
    for v in versions:
        try:
            vid = int(v['version_id'])
            if vid > max_id:
                max_id = vid
        except:
            pass
    return max_id + 1

# Get latest version_number for article
# returns int or 0 if no versions

def latest_version_number(article_id):
    versions = get_versions_for_article(article_id)
    max_version = 0
    for v in versions:
        try:
            ver_num = int(v['version_number'])
            if ver_num > max_version:
                max_version = ver_num
        except:
            pass
    return max_version

# Save new article version (appends)
def add_article_version(article_id, content, author, change_summary):
    new_version_id = next_version_id()
    new_version_number = latest_version_number(article_id) + 1
    now = datetime.datetime.utcnow().isoformat()
    record = {
        'version_id': str(new_version_id),
        'article_id': str(article_id),
        'version_number': str(new_version_number),
        'content': content,
        'author': author,
        'created_date': now,
        'change_summary': change_summary
    }
    append_pipe_delimited_file('article_versions.txt', article_version_keys, record)
    return record

# Get specific version by version_id or by article_id and version_number

def get_version_by_id(version_id):
    versions = get_all_article_versions()
    for v in versions:
        if v['version_id'] == str(version_id):
            return v
    return None


def get_version_by_article_and_number(article_id, version_number):
    versions = get_versions_for_article(article_id)
    for v in versions:
        if v['version_number'] == str(version_number):
            return v
    return None

##### Approvals
# approvals.txt fields:
# approval_id|article_id|version_id|approver|status|comments|timestamp
approval_keys = ['approval_id','article_id','version_id','approver','status','comments','timestamp']

def get_all_approvals():
    return read_pipe_delimited_file('approvals.txt', approval_keys)

def get_approvals_for_article_version(article_id, version_id):
    approvals = get_all_approvals()
    filtered = []
    for a in approvals:
        if a['article_id'] == str(article_id) and a['version_id'] == str(version_id):
            filtered.append(a)
    return filtered

# Generate next approval_id
def next_approval_id():
    approvals = get_all_approvals()
    max_id = 0
    for a in approvals:
        try:
            aid = int(a['approval_id'])
            if aid > max_id:
                max_id = aid
        except:
            pass
    return max_id + 1

# Add approval record
# returns approval record

def add_approval(article_id, version_id, approver, status, comments):
    new_approval_id = next_approval_id()
    now = datetime.datetime.utcnow().isoformat()
    record = {
        'approval_id': str(new_approval_id),
        'article_id': str(article_id),
        'version_id': str(version_id),
        'approver': approver,
        'status': status,
        'comments': comments,
        'timestamp': now
    }
    append_pipe_delimited_file('approvals.txt', approval_keys, record)
    return record

##### Comments
# comments.txt fields:
# comment_id|article_id|version_id|commenter|comment_text|timestamp
comment_keys = ['comment_id','article_id','version_id','commenter','comment_text','timestamp']

def get_all_comments():
    return read_pipe_delimited_file('comments.txt', comment_keys)

def get_comments_for_article_version(article_id, version_id):
    comments = get_all_comments()
    filtered = []
    for c in comments:
        if c['article_id'] == str(article_id) and c['version_id'] == str(version_id):
            filtered.append(c)
    # sort by timestamp ascending
    filtered.sort(key=lambda x: x['timestamp'])
    return filtered

# Generate next comment_id
def next_comment_id():
    comments = get_all_comments()
    max_id = 0
    for c in comments:
        try:
            cid = int(c['comment_id'])
            if cid > max_id:
                max_id = cid
        except:
            pass
    return max_id + 1

# Add comment
# returns comment record

def add_comment(article_id, version_id, commenter, comment_text):
    new_comment_id = next_comment_id()
    now = datetime.datetime.utcnow().isoformat()
    record = {
        'comment_id': str(new_comment_id),
        'article_id': str(article_id),
        'version_id': str(version_id),
        'commenter': commenter,
        'comment_text': comment_text,
        'timestamp': now
    }
    append_pipe_delimited_file('comments.txt', comment_keys, record)
    return record

##### Workflow Stages
# workflow_stages.txt fields:
# category|stage_number|stage_name
workflow_stage_keys = ['category','stage_number','stage_name']

def get_workflow_stages():
    stages = read_pipe_delimited_file('workflow_stages.txt', workflow_stage_keys)
    # convert stage_number to int
    for s in stages:
        try:
            s['stage_number'] = int(s['stage_number'])
        except:
            s['stage_number'] = 0
    return stages

def get_stages_for_category(category):
    stages = get_workflow_stages()
    filtered = [s for s in stages if s['category'] == category]
    filtered.sort(key=lambda x:x['stage_number'])
    return filtered

##### Analytics
# analytics.txt fields:
# article_id|date|views|unique_visitors|avg_time_on_article|shares
analytics_keys = ['article_id','date','views','unique_visitors','avg_time_on_article','shares']

def get_all_analytics():
    return read_pipe_delimited_file('analytics.txt', analytics_keys)

def get_analytics_for_article(article_id):
    all_analytics = get_all_analytics()
    filtered = []
    for a in all_analytics:
        if a['article_id'] == str(article_id):
            filtered.append(a)
    return filtered

# =================================================================================
# Authentication & Authorization Helpers
# =================================================================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# =================================================================================
# Business Logic / Services
# =================================================================================

def user_owns_article(username, article):
    return article and article.get('author') == username

# =================================================================================
# Routes
# =================================================================================

@app.route('/')
def root():
    # Redirect to /dashboard
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    username = session.get('username')
    # quick_stats: number of articles authored by user, number published, pending approval
    articles = get_all_articles()
    user_articles = [a for a in articles if a['author'] == username]
    num_authored = len(user_articles)
    num_published = sum(1 for a in user_articles if a['status'] == 'published')
    # pending approval: any article with status 'pending'
    num_pending = sum(1 for a in user_articles if a['status'] == 'pending')
    quick_stats = {
        'Authored': num_authored,
        'Published': num_published,
        'Pending': num_pending
    }

    # recent_activity: last 5 article_versions by user
    all_versions = get_all_article_versions()
    user_versions = [v for v in all_versions if v['author'] == username]
    user_versions.sort(key=lambda x: x['created_date'], reverse=True)
    recent_activity = user_versions[:5]

    return render_template('dashboard.html', username=username, quick_stats=quick_stats, recent_activity=recent_activity)

@app.route('/article/create', methods=['GET', 'POST'])
@login_required
def create_article():
    username = session.get('username')
    categories = list(sorted(set(a['category'] for a in get_all_articles())))
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', '').strip()
        change_summary = request.form.get('change_summary', '').strip() or 'Initial draft'
        status = request.form.get('status', 'draft').strip()  # allow draft or published/pending

        # Validation
        errors = []
        if not title:
            errors.append('Title is required.')
        if not content:
            errors.append('Content is required.')
        if not category:
            errors.append('Category is required.')

        if errors:
            return render_template('create_article.html', errors=errors,
                                   form_data={'title': title, 'content': content, 'category': category, 'status': status, 'change_summary': change_summary},
                                   categories=categories)

        # Save article
        try:
            # Save article with status draft or whatever
            article_id = add_article(username, title, category, status)
            # Add version
            add_article_version(article_id, content, username, change_summary)
            return redirect(url_for('edit_article', article_id=article_id))
        except Exception as e:
            errors = [f'Failed to create article: {str(e)}']
            return render_template('create_article.html', errors=errors,
                                   form_data={'title': title, 'content': content, 'category': category, 'status': status, 'change_summary': change_summary},
                                   categories=categories)

    # GET
    return render_template('create_article.html', categories=categories)

@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    username = session.get('username')
    article = get_article(article_id)
    if not article:
        abort(404, description='Article not found')
    # Only author can edit
    if not user_owns_article(username, article):
        abort(403, description='Forbidden: you cannot edit this article')

    categories = list(sorted(set(a['category'] for a in get_all_articles())))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', '').strip()
        change_summary = request.form.get('change_summary', '').strip() or 'Updated content'
        status = request.form.get('status', article.get('status', 'draft')).strip()

        errors = []
        if not title:
            errors.append('Title is required.')
        if not content:
            errors.append('Content is required.')
        if not category:
            errors.append('Category is required.')

        if errors:
            form_data = {'title': title, 'content': content, 'category': category, 'status': status, 'change_summary': change_summary}
            return render_template('edit_article.html', article=article, errors=errors, form_data=form_data, categories=categories)

        try:
            # update article fields
            update_article(article_id, title=title, category=category, status=status)
            # add version
            add_article_version(article_id, content, username, change_summary)
            # reload article (updated_date changed)
            article = get_article(article_id)
            msg_success = 'Article updated successfully.'
            form_data = {'title': title, 'content': content, 'category': category, 'status': status, 'change_summary': ''}
            return render_template('edit_article.html', article=article, success=msg_success, form_data=form_data, categories=categories)
        except Exception as e:
            form_data = {'title': title, 'content': content, 'category': category, 'status': status, 'change_summary': change_summary}
            errors = [f'Error updating article: {str(e)}']
            return render_template('edit_article.html', article=article, errors=errors, form_data=form_data, categories=categories)

    # GET - load current latest version content for editing
    versions = get_versions_for_article(article_id)
    if versions:
        latest_version = versions[-1]  # last version latest
        initial_content = latest_version.get('content', '')
    else:
        initial_content = ''

    form_data = {
        'title': article.get('title', ''),
        'content': initial_content,
        'category': article.get('category', ''),
        'status': article.get('status', 'draft'),
        'change_summary': '',
    }

    return render_template('edit_article.html', article=article, form_data=form_data, categories=categories)

@app.route('/article/<int:article_id>/versions')
@login_required
def view_article_versions(article_id):
    article = get_article(article_id)
    if not article:
        abort(404, description='Article not found')

    versions = get_versions_for_article(article_id)
    # Attach approvals to each version
    for v in versions:
        approvals = get_approvals_for_article_version(article_id, v['version_id'])
        v['approvals'] = approvals

    return render_template('version_history.html', article=article, versions=versions)

@app.route('/articles/mine')
@login_required
def my_articles():
    username = session.get('username')
    articles = get_all_articles()
    user_articles = [a for a in articles if a['author'] == username]
    # Optional filter params
    status_filter = request.args.get('status', '')
    category_filter = request.args.get('category', '')

    filtered_articles = []
    for a in user_articles:
        if status_filter and a['status'].lower() != status_filter.lower():
            continue
        if category_filter and a['category'].lower() != category_filter.lower():
            continue
        filtered_articles.append(a)

    categories = list(sorted(set(a['category'] for a in user_articles)))
    statuses = list(sorted(set(a['status'] for a in user_articles)))

    return render_template('my_articles.html', articles=filtered_articles, categories=categories, status_options=statuses, selected_status=status_filter, selected_category=category_filter)

@app.route('/articles/published')
@login_required
def published_articles():
    articles = get_all_articles()
    published = [a for a in articles if a['status'].lower() == 'published']

    category_filter = request.args.get('category', '')
    sort_by = request.args.get('sort', 'created_date')  # default sort

    if category_filter:
        published = [a for a in published if a['category'].lower() == category_filter.lower()]

    # Sort by field desc except created_date asc
    if sort_by in ['created_date', 'updated_date', 'title', 'author', 'category']:
        reverse = False
        if sort_by != 'created_date':
            reverse = True
        try:
            published.sort(key=lambda x: x.get(sort_by, ''), reverse=reverse)
        except Exception:
            pass

    categories = list(sorted(set(a['category'] for a in get_all_articles() if a['status'].lower() == 'published')))
    sort_options = ['created_date', 'updated_date', 'title', 'author', 'category']

    return render_template('published_articles.html', articles=published, categories=categories, sort_options=sort_options, selected_category=category_filter, selected_sort=sort_by)

@app.route('/calendar')
@login_required
def content_calendar():
    # Enhanced calendar navigation and data
    # Get current month and year from query params or default to today
    try:
        month = int(request.args.get('month', 0))
        year = int(request.args.get('year', 0))
        if month < 1 or month > 12:
            month = 0
        if year < 1:
            year = 0
    except:
        month = 0
        year = 0

    now = datetime.datetime.utcnow()
    if month == 0 or year == 0:
        month = now.month
        year = now.year

    # Calculate prev/next month and year
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    # Prepare calendar weeks data structure
    cal = calendar.Calendar(calendar.SUNDAY)
    month_days = cal.monthdatescalendar(year, month)

    # Prepare events mapping by date for quick lookup
    articles = get_all_articles()
    events_by_date = {}

    for a in articles:
        try:
            # parse created_date to datetime
            dt = datetime.datetime.fromisoformat(a['created_date'])
            if dt.year == year and dt.month == month:
                day_key = dt.date()
                if day_key not in events_by_date:
                    events_by_date[day_key] = []
                events_by_date[day_key].append({
                    'id': a['article_id'],
                    'title': a['title']
                })
        except Exception:
            continue

    calendar_weeks = []
    for week in month_days:
        week_data = []
        for day in week:
            if day.month != month:
                week_data.append(None)
            else:
                week_data.append({
                    'date': day.isoformat(),
                    'day': day.day,
                    'events': events_by_date.get(day, [])
                })
        calendar_weeks.append(week_data)

    current_month_name = datetime.date(year, month, 1).strftime('%B')

    return render_template('content_calendar.html',
                           prev_month=prev_month, prev_year=prev_year,
                           next_month=next_month, next_year=next_year,
                           current_month=current_month_name, current_year=year,
                           calendar_weeks=calendar_weeks)

@app.route('/article/<int:article_id>/analytics')
@login_required
def article_analytics(article_id):
    article = get_article(article_id)
    if not article:
        abort(404, description='Article not found')

    analytics_records = get_analytics_for_article(article_id)

    # Aggregate analytics data
    total_views = 0
    total_unique = 0
    total_time = 0.0
    total_shares = 0
    count = 0

    for rec in analytics_records:
        try:
            total_views += int(rec.get('views', 0))
            total_unique += int(rec.get('unique_visitors', 0))
            total_time += float(rec.get('avg_time_on_article', 0.0))
            total_shares += int(rec.get('shares', 0))
            count += 1
        except:
            pass

    avg_time = (total_time / count) if count > 0 else 0.0

    analytics_summary = {
        'views': total_views,
        'unique_visitors': total_unique,
        'avg_time_spent': round(avg_time,2),
        'shares': total_shares,
        'comments': 0  # Placeholder, comments count not implemented
    }

    return render_template('article_analytics.html', article=article, analytics=analytics_summary)

# For this minimal implementation, we omit explicit login/logout handlers.
# Assume session['username'] is set externally for authenticated user.

if __name__ == '__main__':
    app.run(debug=True)
