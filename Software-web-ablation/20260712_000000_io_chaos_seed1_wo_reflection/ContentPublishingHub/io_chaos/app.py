from flask import Flask, request, session, redirect, url_for, render_template, flash, abort
import os
from datetime import datetime
from functools import wraps
import threading

app = Flask(__name__)
app.secret_key = 'supersecretkeyhere'  # Should be replaced with a real secure key and environment variable in production

# Data folder path
DATA_FOLDER = 'data'
LOCK = threading.Lock()

# Utility functions for file I/O with locking

def read_file_lines(filename):
    path = os.path.join(DATA_FOLDER, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines


def write_file_lines(filename, lines):
    path = os.path.join(DATA_FOLDER, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n' if lines else '')


def atomic_write_file_lines(filename, lines):
    # To safely write file with lock
    with LOCK:
        write_file_lines(filename, lines)


# ------------------------- Models ------------------------------


# users.txt schema: user_id|username|role
# role: string (e.g., author, editor, admin)
class UserModel:
    FILENAME = 'users.txt'

    @staticmethod
    def all_users():
        users = []
        lines = read_file_lines(UserModel.FILENAME)
        for line in lines:
            parts = line.split('|')
            if len(parts) != 3:
                continue
            user_id, username, role = parts
            users.append({
                'user_id': int(user_id), 'username': username, 'role': role
            })
        return users

    @staticmethod
    def find_by_username(username):
        for user in UserModel.all_users():
            if user['username'] == username:
                return user
        return None

    @staticmethod
    def find_by_id(user_id):
        for user in UserModel.all_users():
            if user['user_id'] == user_id:
                return user
        return None


# articles.txt schema: article_id|author_id|title|category|status|created_at|updated_at
# status: draft, published, archived
class ArticleModel:
    FILENAME = 'articles.txt'

    @staticmethod
    def all_articles():
        articles = []
        lines = read_file_lines(ArticleModel.FILENAME)
        for line in lines:
            parts = line.split('|')
            if len(parts) != 7:
                continue
            article_id, author_id, title, category, status, created_at, updated_at = parts
            articles.append({
                'article_id': int(article_id),
                'author_id': int(author_id),
                'title': title,
                'category': category,
                'status': status,
                'created_at': created_at,
                'updated_at': updated_at
            })
        return articles

    @staticmethod
    def find_article(article_id):
        for art in ArticleModel.all_articles():
            if art['article_id'] == article_id:
                return art
        return None

    @staticmethod
    def save_article(article):
        articles = ArticleModel.all_articles()
        updated = False
        for idx, art in enumerate(articles):
            if art['article_id'] == article['article_id']:
                articles[idx] = article
                updated = True
                break
        if not updated:
            articles.append(article)
        lines = [f"{a['article_id']}|{a['author_id']}|{a['title']}|{a['category']}|{a['status']}|{a['created_at']}|{a['updated_at']}" for a in articles]
        atomic_write_file_lines(ArticleModel.FILENAME, lines)

    @staticmethod
    def next_id():
        arts = ArticleModel.all_articles()
        if not arts:
            return 1
        return max(a['article_id'] for a in arts) + 1


# article_versions.txt schema: version_id|article_id|version_number|content|created_at
class VersionModel:
    FILENAME = 'article_versions.txt'

    @staticmethod
    def all_versions():
        versions = []
        lines = read_file_lines(VersionModel.FILENAME)
        for line in lines:
            parts = line.split('|', 4)  # content may contain pipes, we allow max 5 splits
            if len(parts) != 5:
                continue
            version_id, article_id, version_number, content, created_at = parts
            versions.append({
                'version_id': int(version_id),
                'article_id': int(article_id),
                'version_number': int(version_number),
                'content': content,
                'created_at': created_at
            })
        return versions

    @staticmethod
    def find_versions_by_article(article_id):
        return [v for v in VersionModel.all_versions() if v['article_id'] == article_id]

    @staticmethod
    def find_version(version_id):
        for v in VersionModel.all_versions():
            if v['version_id'] == version_id:
                return v
        return None

    @staticmethod
    def next_version_id():
        versions = VersionModel.all_versions()
        if not versions:
            return 1
        return max(v['version_id'] for v in versions) + 1

    @staticmethod
    def max_version_number(article_id):
        versions = VersionModel.find_versions_by_article(article_id)
        if not versions:
            return 0
        return max(v['version_number'] for v in versions)

    @staticmethod
    def save_version(version):
        versions = VersionModel.all_versions()
        updated = False
        for idx, v in enumerate(versions):
            if v['version_id'] == version['version_id']:
                versions[idx] = version
                updated = True
                break
        if not updated:
            versions.append(version)
        lines = [f"{v['version_id']}|{v['article_id']}|{v['version_number']}|{v['content']}|{v['created_at']}" for v in versions]
        atomic_write_file_lines(VersionModel.FILENAME, lines)


# approvals.txt schema: approval_id|version_id|article_id|approver_id|status|comment|created_at
# status: approved, rejected, revision_requested
class ApprovalModel:
    FILENAME = 'approvals.txt'

    @staticmethod
    def all_approvals():
        approvals = []
        lines = read_file_lines(ApprovalModel.FILENAME)
        for line in lines:
            parts = line.split('|', 6)
            if len(parts) != 7:
                continue
            approval_id, version_id, article_id, approver_id, status, comment, created_at = parts
            approvals.append({
                'approval_id': int(approval_id),
                'version_id': int(version_id),
                'article_id': int(article_id),
                'approver_id': int(approver_id),
                'status': status,
                'comment': comment,
                'created_at': created_at
            })
        return approvals

    @staticmethod
    def find_by_version(version_id):
        return [a for a in ApprovalModel.all_approvals() if a['version_id'] == version_id]

    @staticmethod
    def save_approval(approval):
        approvals = ApprovalModel.all_approvals()
        updated = False
        for idx, a in enumerate(approvals):
            if a['approval_id'] == approval['approval_id']:
                approvals[idx] = approval
                updated = True
                break
        if not updated:
            approvals.append(approval)
        lines = [f"{a['approval_id']}|{a['version_id']}|{a['article_id']}|{a['approver_id']}|{a['status']}|{a['comment']}|{a['created_at']}" for a in approvals]
        atomic_write_file_lines(ApprovalModel.FILENAME, lines)

    @staticmethod
    def next_approval_id():
        approvals = ApprovalModel.all_approvals()
        if not approvals:
            return 1
        return max(a['approval_id'] for a in approvals) + 1


# comments.txt schema: comment_id|article_id|version_id|user_id|comment_text|created_at
class CommentModel:
    FILENAME = 'comments.txt'

    @staticmethod
    def all_comments():
        comments = []
        lines = read_file_lines(CommentModel.FILENAME)
        for line in lines:
            parts = line.split('|', 5)
            if len(parts) != 6:
                continue
            comment_id, article_id, version_id, user_id, comment_text, created_at = parts
            comments.append({
                'comment_id': int(comment_id),
                'article_id': int(article_id),
                'version_id': int(version_id),
                'user_id': int(user_id),
                'comment_text': comment_text,
                'created_at': created_at
            })
        return comments

    @staticmethod
    def find_comments(article_id, version_id):
        return [c for c in CommentModel.all_comments() if c['article_id'] == article_id and c['version_id'] == version_id]

    @staticmethod
    def save_comment(comment):
        comments = CommentModel.all_comments()
        updated = False
        for idx, c in enumerate(comments):
            if c['comment_id'] == comment['comment_id']:
                comments[idx] = comment
                updated = True
                break
        if not updated:
            comments.append(comment)
        lines = [f"{c['comment_id']}|{c['article_id']}|{c['version_id']}|{c['user_id']}|{c['comment_text']}|{c['created_at']}" for c in comments]
        atomic_write_file_lines(CommentModel.FILENAME, lines)

    @staticmethod
    def next_comment_id():
        comments = CommentModel.all_comments()
        if not comments:
            return 1
        return max(c['comment_id'] for c in comments) + 1


# workflow_stages.txt schema: workflow_id|category|stage_order|stage_name|required
class WorkflowModel:
    FILENAME = 'workflow_stages.txt'

    @staticmethod
    def all_stages():
        stages = []
        lines = read_file_lines(WorkflowModel.FILENAME)
        for line in lines:
            parts = line.split('|')
            if len(parts) != 5:
                continue
            workflow_id, category, stage_order, stage_name, required = parts
            stages.append({
                'workflow_id': int(workflow_id),
                'category': category,
                'stage_order': int(stage_order),
                'stage_name': stage_name,
                'required': required.lower() == 'true'
            })
        return stages

    @staticmethod
    def stages_by_category(category):
        return sorted([s for s in WorkflowModel.all_stages() if s['category'] == category], key=lambda x: x['stage_order'])


# analytics.txt schema: analytics_id|article_id|views|unique_visitors|average_time_seconds|shares
class AnalyticsModel:
    FILENAME = 'analytics.txt'

    @staticmethod
    def all_analytics():
        analytics = []
        lines = read_file_lines(AnalyticsModel.FILENAME)
        for line in lines:
            parts = line.split('|')
            if len(parts) != 6:
                continue
            analytics_id, article_id, views, unique_visitors, average_time_seconds, shares = parts
            analytics.append({
                'analytics_id': int(analytics_id),
                'article_id': int(article_id),
                'views': int(views),
                'unique_visitors': int(unique_visitors),
                'average_time_seconds': float(average_time_seconds),
                'shares': int(shares)
            })
        return analytics

    @staticmethod
    def find_by_article(article_id):
        for a in AnalyticsModel.all_analytics():
            if a['article_id'] == article_id:
                return a
        return None


# ------------------------- Services ------------------------------


class ArticleService:
    @staticmethod
    def create_article(author_id, title, content, category='General'):
        article_id = ArticleModel.next_id()
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        article = {
            'article_id': article_id,
            'author_id': author_id,
            'title': title,
            'category': category,
            'status': 'draft',
            'created_at': now,
            'updated_at': now
        }
        ArticleModel.save_article(article)

        # Create first version
        version_id = VersionModel.next_version_id()
        version = {
            'version_id': version_id,
            'article_id': article_id,
            'version_number': 1,
            'content': content,
            'created_at': now
        }
        VersionModel.save_version(version)

        return article

    @staticmethod
    def update_article_version(article_id, new_content):
        article = ArticleModel.find_article(article_id)
        if not article:
            return None

        # Get next version number
        next_version_num = VersionModel.max_version_number(article_id) + 1
        version_id = VersionModel.next_version_id()
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        version = {
            'version_id': version_id,
            'article_id': article_id,
            'version_number': next_version_num,
            'content': new_content,
            'created_at': now
        }
        VersionModel.save_version(version)

        # Update article updated_at
        article['updated_at'] = now
        ArticleModel.save_article(article)

        return version

    @staticmethod
    def get_article_versions(article_id):
        return sorted(VersionModel.find_versions_by_article(article_id), key=lambda v: v['version_number'])

    @staticmethod
    def get_articles_by_author(author_id, status_filter=None):
        arts = [a for a in ArticleModel.all_articles() if a['author_id'] == author_id]
        if status_filter:
            arts = [a for a in arts if a['status'] == status_filter]
        return arts

    @staticmethod
    def get_published_articles(filter_category=None, sort_by=None):
        arts = [a for a in ArticleModel.all_articles() if a['status'] == 'published']
        if filter_category:
            arts = [a for a in arts if a['category'] == filter_category]
        if sort_by:
            if sort_by == 'title':
                arts = sorted(arts, key=lambda a: a['title'].lower())
            elif sort_by == 'created_at':
                arts = sorted(arts, key=lambda a: a['created_at'], reverse=True)
        return arts


class ApprovalService:
    @staticmethod
    def approve_version(version_id, approver_id, status, comment):
        approvals = ApprovalModel.find_by_version(version_id)
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        # Check if approver already approved this version
        for appr in approvals:
            if appr['approver_id'] == approver_id:
                # Update existing approval
                appr['status'] = status
                appr['comment'] = comment
                appr['created_at'] = now
                ApprovalModel.save_approval(appr)
                return appr

        # New approval
        approval_id = ApprovalModel.next_approval_id()
        version = VersionModel.find_version(version_id)
        if not version:
            return None

        approval = {
            'approval_id': approval_id,
            'version_id': version_id,
            'article_id': version['article_id'],
            'approver_id': approver_id,
            'status': status,
            'comment': comment,
            'created_at': now
        }
        ApprovalModel.save_approval(approval)
        return approval

    @staticmethod
    def get_approvals_for_version(version_id):
        return ApprovalModel.find_by_version(version_id)


class CommentService:
    @staticmethod
    def add_comment(article_id, version_id, user_id, comment_text):
        comment_id = CommentModel.next_comment_id()
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        comment = {
            'comment_id': comment_id,
            'article_id': article_id,
            'version_id': version_id,
            'user_id': user_id,
            'comment_text': comment_text,
            'created_at': now
        }
        CommentModel.save_comment(comment)
        return comment

    @staticmethod
    def get_comments(article_id, version_id):
        return CommentModel.find_comments(article_id, version_id)


class AnalyticsService:
    @staticmethod
    def get_analytics_for_article(article_id):
        analytics = AnalyticsModel.find_by_article(article_id)
        if not analytics:
            return {
                'views': 0,
                'unique_visitors': 0,
                'average_time_seconds': 0.0,
                'shares': 0
            }
        return analytics


# ------------------------- Authentication & Helpers ------------------------------

# Dummy auth, assume session['username'] is set when logged in
# In real app, implement proper login, logout and session management

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You need to login to access this page.')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def current_user():
    if 'username' in session:
        return UserModel.find_by_username(session['username'])
    return None


# ------------------------- Routes ------------------------------

@app.route('/')
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user()
    username = user['username'] if user else 'Guest'

    # Quick stats example: counts of user's articles by status
    articles = ArticleModel.all_articles()
    user_articles = [a for a in articles if a['author_id'] == user['user_id']]
    quick_stats = {
        'drafts': sum(1 for a in user_articles if a['status'] == 'draft'),
        'published': sum(1 for a in user_articles if a['status'] == 'published'),
        'archived': sum(1 for a in user_articles if a['status'] == 'archived')
    }

    # Recent activity example: Latest articles updated by user
    recent_activity = sorted(user_articles, key=lambda x: x['updated_at'], reverse=True)[:5]

    return render_template('dashboard.html', username=username, quick_stats=quick_stats, recent_activity=recent_activity)


@app.route('/article/create', methods=['GET', 'POST'])
@login_required
def create_article():
    user = current_user()
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', 'General').strip()

        errors = []
        if not title:
            errors.append('Title is required.')
        if not content:
            errors.append('Content is required.')

        if errors:
            for e in errors:
                flash(e)
            return render_template('create_article.html', title=title, content=content, category=category)

        article = ArticleService.create_article(user['user_id'], title, content, category)
        flash('Article created successfully.')
        return redirect(url_for('edit_article', article_id=article['article_id']))

    # GET request
    return render_template('create_article.html')


@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    user = current_user()
    article = ArticleModel.find_article(article_id)
    if not article:
        abort(404, description='Article not found')

    if article['author_id'] != user['user_id']:
        abort(403, description='Unauthorized to edit this article')

    if request.method == 'POST':
        new_content = request.form.get('content', '').strip()
        if not new_content:
            flash('Content is required.')
            # Provide current latest version content if any
            versions = ArticleService.get_article_versions(article_id)
            latest_version = versions[-1] if versions else None
            return render_template('edit_article.html', article_id=article_id, article_title=article['title'], article_content=latest_version['content'] if latest_version else '')

        new_version = ArticleService.update_article_version(article_id, new_content)
        if not new_version:
            flash('Failed to save new version.')
            return redirect(url_for('edit_article', article_id=article_id))

        flash('Article updated with new version.')
        return redirect(url_for('edit_article', article_id=article_id))

    # GET request
    versions = ArticleService.get_article_versions(article_id)
    latest_version = versions[-1] if versions else None
    article_content = latest_version['content'] if latest_version else ''
    return render_template('edit_article.html', article_id=article_id, article_title=article['title'], article_content=article_content)


@app.route('/article/<int:article_id>/versions')
@login_required
def article_version_history(article_id):
    user = current_user()
    article = ArticleModel.find_article(article_id)
    if not article:
        abort(404, description='Article not found')

    if article['author_id'] != user['user_id'] and user['role'] != 'editor':
        abort(403, description='Unauthorized to view versions')

    versions_list = ArticleService.get_article_versions(article_id)

    # Add comments and approvals on versions
    for version in versions_list:
        version_comments = CommentService.get_comments(article_id, version['version_number'])
        version['comments'] = [c['comment_text'] for c in CommentService.get_comments(article_id, version['version_number'])]
        approvals = ApprovalService.get_approvals_for_version(version['version_id'])
        if approvals:
            # We can pick the status of the latest approval for display
            version['status'] = approvals[-1]['status']
        else:
            version['status'] = 'No approval'

    # Optional comparison_data: For simplicity, omitted detailed diff logic
    comparison_data = None

    return render_template('version_history.html', versions_list=versions_list, comparison_data=comparison_data)


@app.route('/articles/mine')
@login_required
def my_articles():
    user = current_user()
    status_filter = request.args.get('status', None)
    articles = ArticleService.get_articles_by_author(user['user_id'], status_filter)

    # Add last_updated attribute to articles for display
    for a in articles:
        a['last_updated'] = a['updated_at']
        a['id'] = a['article_id']

    return render_template('my_articles.html', articles=articles, filter_status=status_filter)


@app.route('/articles/published')
def published_articles():
    filter_category = request.args.get('category', None)
    sort_by = request.args.get('sort_by', 'date')  # default to date

    articles = ArticleService.get_published_articles(filter_category, None)

    # Add published_date and popularity with dummy values for UI
    for a in articles:
        a['published_date'] = a['created_at']
        a['popularity'] = 0  # Placeholder value
        a['id'] = a['article_id']

    categories = list(set(a['category'] for a in articles))

    # Implement sorting
    if sort_by == 'date':
        articles.sort(key=lambda x: x['created_at'], reverse=True)
    elif sort_by == 'popularity':
        articles.sort(key=lambda x: x.get('popularity', 0), reverse=True)

    return render_template('published_articles.html', articles=articles, filter_category=filter_category, sort_by=sort_by, categories=categories)


@app.route('/calendar')
@login_required
def content_calendar():
    calendar_view = request.args.get('calendar_view', 'month')  # month, week, day
    # For simplicity, we provide all articles with created dates, and frontend can filter by view
    all_articles = ArticleModel.all_articles()
    scheduled_articles = [a for a in all_articles if a['status'] != 'archived']

    # Fix for scheduled_date display: Add dummy scheduled_date if not present
    for a in scheduled_articles:
        if 'scheduled_date' not in a or not a['scheduled_date']:
            a['scheduled_date'] = a['created_at']  # fallback

    return render_template('content_calendar.html', calendar_view=calendar_view, scheduled_articles=scheduled_articles)


@app.route('/article/<int:article_id>/analytics')
@login_required
def article_analytics(article_id):
    user = current_user()
    article = ArticleModel.find_article(article_id)
    if not article:
        abort(404, description='Article not found')

    if article['author_id'] != user['user_id'] and user['role'] != 'editor':
        abort(403, description='Unauthorized to view analytics')

    analytics_overview = AnalyticsService.get_analytics_for_article(article_id)

    return render_template('article_analytics.html', analytics_overview=analytics_overview, article=article)


# Run app if main
if __name__ == '__main__':
    app.run(debug=True)
