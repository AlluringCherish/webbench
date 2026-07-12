import os
import csv
import threading
import datetime
import uuid
from flask import Flask, request, jsonify, redirect, url_for, session, render_template

app = Flask(__name__)
app.secret_key = 'supersecretkeyreplace'

DATA_DIR = 'data'
ARTICLES_FILE = os.path.join(DATA_DIR, 'articles.txt')
ARTICLE_VERSIONS_FILE = os.path.join(DATA_DIR, 'article_versions.txt')
APPROVALS_FILE = os.path.join(DATA_DIR, 'approvals.txt')
COMMENTS_FILE = os.path.join(DATA_DIR, 'comments.txt')
WORKFLOW_STAGES_FILE = os.path.join(DATA_DIR, 'workflow_stages.txt')

lock = threading.Lock()

# Utility functions

def safe_read_pipe_delimited(file_path):
    if not os.path.isfile(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f, delimiter='|')
        return list(reader)


def safe_write_pipe_delimited(file_path, data, fieldnames):
    with lock:
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='|')
            writer.writeheader()
            writer.writerows(data)


def safe_append_pipe_delimited(file_path, row, fieldnames):
    with lock:
        file_exists = os.path.isfile(file_path)
        with open(file_path, 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='|')
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)


def generate_uuid():
    return str(uuid.uuid4())


def get_timestamp():
    return datetime.datetime.utcnow().isoformat() + 'Z'


def get_current_username():
    return session.get('username', 'anonymous')


# Models
class ArticlesModel:
    FIELDS = ['article_id', 'title', 'author', 'category', 'status', 'last_modified']

    @staticmethod
    def list_all():
        return safe_read_pipe_delimited(ARTICLES_FILE)

    @staticmethod
    def find_by_id(article_id):
        articles = ArticlesModel.list_all()
        for a in articles:
            if a['article_id'] == str(article_id):
                return a
        return None

    @staticmethod
    def add(article):
        articles = ArticlesModel.list_all()
        articles.append(article)
        safe_write_pipe_delimited(ARTICLES_FILE, articles, ArticlesModel.FIELDS)

    @staticmethod
    def update(article_id, updated_data):
        articles = ArticlesModel.list_all()
        updated = False
        for i, art in enumerate(articles):
            if art['article_id'] == str(article_id):
                articles[i].update(updated_data)
                updated = True
                break
        if updated:
            safe_write_pipe_delimited(ARTICLES_FILE, articles, ArticlesModel.FIELDS)
        return updated


class ArticleVersionsModel:
    FIELDS = ['version_id', 'article_id', 'version_number', 'content', 'author', 'created_date', 'change_summary']

    @staticmethod
    def list_all():
        return safe_read_pipe_delimited(ARTICLE_VERSIONS_FILE)

    @staticmethod
    def find_by_article(article_id):
        versions = ArticleVersionsModel.list_all()
        return [v for v in versions if v['article_id'] == str(article_id)]

    @staticmethod
    def add(version):
        safe_append_pipe_delimited(ARTICLE_VERSIONS_FILE, version, ArticleVersionsModel.FIELDS)

    @staticmethod
    def max_version_number(article_id):
        versions = ArticleVersionsModel.find_by_article(article_id)
        if not versions:
            return 0
        return max(int(v['version_number']) for v in versions)


class ApprovalsModel:
    FIELDS = ['approval_id', 'article_id', 'version_id', 'approver', 'status', 'comments', 'timestamp']

    @staticmethod
    def list_all():
        return safe_read_pipe_delimited(APPROVALS_FILE)

    @staticmethod
    def find_by_article(article_id):
        approvals = ApprovalsModel.list_all()
        return [a for a in approvals if a['article_id'] == str(article_id)]

    @staticmethod
    def add(approval):
        safe_append_pipe_delimited(APPROVALS_FILE, approval, ApprovalsModel.FIELDS)


class CommentsModel:
    FIELDS = ['comment_id', 'article_id', 'version_id', 'author', 'comment', 'timestamp']

    @staticmethod
    def list_all():
        return safe_read_pipe_delimited(COMMENTS_FILE)

    @staticmethod
    def find_by_version(version_id):
        comments = CommentsModel.list_all()
        return [c for c in comments if c['version_id'] == str(version_id)]

    @staticmethod
    def add(comment):
        safe_append_pipe_delimited(COMMENTS_FILE, comment, CommentsModel.FIELDS)


# Services
class ArticleService:
    @staticmethod
    def create_article(title, content, author, category=None):
        article_id = generate_uuid()
        now = get_timestamp()
        article = {
            'article_id': article_id,
            'title': title,
            'author': author,
            'category': category if category else '',
            'status': 'draft',
            'last_modified': now
        }
        ArticlesModel.add(article)

        version_id = generate_uuid()
        version_record = {
            'version_id': version_id,
            'article_id': article_id,
            'version_number': '1',
            'content': content,
            'author': author,
            'created_date': now,
            'change_summary': 'Initial version',
        }
        ArticleVersionsModel.add(version_record)
        return article_id, version_id

    @staticmethod
    def edit_article(article_id, content, change_summary, author):
        article = ArticlesModel.find_by_id(article_id)
        if not article:
            return None, 'Article not found.'
        max_version = ArticleVersionsModel.max_version_number(article_id)
        next_version_num = max_version + 1
        now = get_timestamp()

        version_id = generate_uuid()
        version_record = {
            'version_id': version_id,
            'article_id': article_id,
            'version_number': str(next_version_num),
            'content': content,
            'author': author,
            'created_date': now,
            'change_summary': change_summary,
        }
        ArticleVersionsModel.add(version_record)
        ArticlesModel.update(article_id, {'last_modified': now})
        return version_id, None

    @staticmethod
    def get_version_history(article_id):
        versions = ArticleVersionsModel.find_by_article(article_id)
        versions_sorted = sorted(versions, key=lambda v: int(v['version_number']))
        return versions_sorted


class ApprovalService:
    @staticmethod
    def approve_version(article_id, version_id, approver, status, comments):
        valid_statuses = {'approved', 'rejected', 'revision_requested'}
        if status not in valid_statuses:
            return 'Invalid status.'

        approval_id = generate_uuid()
        approval_record = {
            'approval_id': approval_id,
            'article_id': article_id,
            'version_id': version_id,
            'approver': approver,
            'status': status,
            'comments': comments,
            'timestamp': get_timestamp(),
        }
        ApprovalsModel.add(approval_record)
        # Update article status on approval
        if status == 'approved':
            ArticlesModel.update(article_id, {'status': 'published'})
        elif status == 'revision_requested':
            ArticlesModel.update(article_id, {'status': 'revision requested'})
        elif status == 'rejected':
            ArticlesModel.update(article_id, {'status': 'rejected'})
        return None

    @staticmethod
    def get_approvals(article_id):
        return ApprovalsModel.find_by_article(article_id)


class CommentService:
    @staticmethod
    def add_comment(article_id, version_id, author, comment):
        comment_id = generate_uuid()
        comment_record = {
            'comment_id': comment_id,
            'article_id': article_id,
            'version_id': version_id,
            'author': author,
            'comment': comment,
            'timestamp': get_timestamp(),
        }
        CommentsModel.add(comment_record)


# Routes
@app.route('/')
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = get_current_username()
    articles = ArticlesModel.list_all()
    user_articles = [a for a in articles if a.get('author') == username]

    summaries = []
    for art in user_articles:
        art_id = art['article_id']
        versions = ArticleVersionsModel.find_by_article(art_id)
        approvals = ApprovalsModel.find_by_article(art_id)
        approval_count = sum(1 for a in approvals if a['status'] == 'approved')
        summaries.append({
            'article_id': art_id,
            'title': art.get('title', ''),
            'versions_count': len(versions),
            'approved_count': approval_count,
        })

    return jsonify({'username': username, 'articles': summaries})


@app.route('/article/create', methods=['GET', 'POST'])
def create_article():
    if request.method == 'GET':
        return render_template('create_article.html')

    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    category = request.form.get('category', '').strip()
    username = get_current_username()

    errors = {}
    if not title:
        errors['title'] = 'Title is required.'
    if not content:
        errors['content'] = 'Content is required.'
    if errors:
        return render_template('create_article.html', errors=errors)

    article_id, version_id = ArticleService.create_article(title, content, username, category)

    return redirect(url_for('edit_article', article_id=article_id))


@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    article = ArticlesModel.find_by_id(article_id)
    if not article:
        return render_template('edit_article.html', error='Article not found.'), 404

    if request.method == 'GET':
        versions = ArticleService.get_version_history(article_id)
        # Get latest version content for editing
        if versions:
            latest_version = versions[-1]
            article_content = latest_version['content']
        else:
            article_content = ''
        # Prepare article dict with fields for template
        article_display = {
            'id': article['article_id'],
            'title': article.get('title', ''),
            'category': article.get('category', ''),
            'status': article.get('status', 'draft'),
            'content': article_content
        }
        return render_template('edit_article.html', article=article_display, version_history=versions)

    content = request.form.get('content', '').strip()
    change_summary = request.form.get('change_summary', '').strip()
    username = get_current_username()

    errors = {}
    if not content:
        errors['content'] = 'Content is required.'
    if not change_summary:
        errors['change_summary'] = 'Change summary is required.'
    if errors:
        versions = ArticleService.get_version_history(article_id)
        article_display = {
            'id': article['article_id'],
            'title': article.get('title', ''),
            'category': article.get('category', ''),
            'status': article.get('status', 'draft'),
            'content': content
        }
        return render_template('edit_article.html', errors=errors, article=article_display, version_history=versions), 400

    version_id, err = ArticleService.edit_article(article_id, content, change_summary, username)
    if err:
        return render_template('edit_article.html', error=err), 400

    return redirect(url_for('edit_article', article_id=article_id))


@app.route('/article/<int:article_id>/versions')
def version_history(article_id):
    article = ArticlesModel.find_by_id(article_id)
    if not article:
        return render_template('version_history.html', error='Article not found.'), 404

    versions = ArticleService.get_version_history(article_id)
    return render_template('version_history.html', article_id=article_id, versions=versions)


@app.route('/articles/mine')
def my_articles():
    username = get_current_username()
    articles = ArticlesModel.list_all()
    my_articles = [a for a in articles if a.get('author') == username]
    prepared_articles = []
    for art in my_articles:
        prepared_articles.append({
            'id': art.get('article_id'),
            'title': art.get('title', ''),
            'category': art.get('category', ''),
            'status': art.get('status', 'draft'),
            'last_modified': art.get('last_modified', ''),
        })
    return render_template('my_articles.html', articles=prepared_articles)


@app.route('/articles/published')
def published_articles():
    articles = ArticlesModel.list_all()
    versions = ArticleVersionsModel.list_all()
    approvals = ApprovalsModel.list_all()

    published_list = []
    categories_set = set()
    for art in articles:
        art_id = art['article_id']
        art_versions = [v for v in versions if v['article_id'] == art_id]
        if not art_versions:
            continue

        latest_version = max(art_versions, key=lambda v: int(v['version_number']))

        latest_approvals = [a for a in approvals if a['version_id'] == latest_version['version_id']]
        if any(a['status'] == 'approved' for a in latest_approvals):
            categories_set.add(art.get('category', ''))
            published_list.append({
                'id': art_id,
                'title': art.get('title', ''),
                'category': art.get('category', ''),
                'published_date': latest_version['created_date'],
                'version_number': latest_version['version_number'],
                'content': latest_version['content'],
            })

    selected_category = request.args.get('category', '')
    selected_sort = request.args.get('sort', 'date')

    if selected_category:
        published_list = [p for p in published_list if p.get('category') == selected_category]

    if selected_sort == 'title':
        published_list = sorted(published_list, key=lambda x: x['title'])
    else:
        published_list = sorted(published_list, key=lambda x: x['published_date'], reverse=True)

    categories = sorted(filter(None, categories_set))

    return render_template('published_articles.html', articles=published_list, categories=categories, selected_category=selected_category, selected_sort=selected_sort)


@app.route('/calendar', methods=['GET', 'POST'])
def content_calendar():
    if request.method == 'GET':
        approvals = ApprovalsModel.list_all()
        articles = ArticlesModel.list_all()

        schedule = []
        for a in approvals:
            article = next((art for art in articles if art['article_id'] == a['article_id']), None)
            if not article:
                continue
            schedule.append({
                'date': a.get('timestamp', ''),
                'title': article.get('title', ''),
                'category': article.get('category', ''),
                'status': a.get('status', ''),
            })

        view = request.args.get('view', 'month')
        return render_template('content_calendar.html', schedule=schedule, view=view)

    article_id = request.form.get('article_id')
    version_id = request.form.get('version_id')
    publish_date = request.form.get('publish_date')
    username = get_current_username()
    errors = {}

    if not article_id:
        errors['article_id'] = 'Article ID is required.'
    if not version_id:
        errors['version_id'] = 'Version ID is required.'
    if not publish_date:
        errors['publish_date'] = 'Publish date is required.'

    if errors:
        return render_template('content_calendar.html', errors=errors)

    approval_id = generate_uuid()
    approval_record = {
        'approval_id': approval_id,
        'article_id': article_id,
        'version_id': version_id,
        'approver': username,
        'status': 'scheduled',
        'comments': f'Scheduled for publication on {publish_date}',
        'timestamp': get_timestamp(),
    }
    ApprovalsModel.add(approval_record)
    return redirect(url_for('content_calendar'))


@app.route('/article/<int:article_id>/analytics')
def article_analytics(article_id):
    article = ArticlesModel.find_by_id(article_id)
    if not article:
        return render_template('article_analytics.html', error='Article not found.', article_id=article_id, analytics=None), 404

    versions = ArticleVersionsModel.find_by_article(article_id)
    approvals = ApprovalsModel.find_by_article(article_id)
    comments = CommentsModel.list_all()

    version_count = len(versions)
    approval_count = sum(1 for a in approvals if a['status'] == 'approved')
    comment_count = sum(1 for c in comments if c['article_id'] == str(article_id))

    analytics = [
        {'metric': 'Version Count', 'value': version_count},
        {'metric': 'Approval Count', 'value': approval_count},
        {'metric': 'Comment Count', 'value': comment_count},
    ]

    return render_template('article_analytics.html', article_id=article_id, analytics=analytics)


@app.route('/article/<int:article_id>/approve', methods=['POST'])
def approve_version(article_id):
    data = request.form
    version_id = data.get('version_id')
    status = data.get('status')
    comments = data.get('comments', '')
    username = get_current_username()

    if not version_id:
        return jsonify({'error': 'version_id is required'}), 400
    if not status or status not in {'approved', 'rejected', 'revision_requested'}:
        return jsonify({'error': 'Valid status is required (approved, rejected, revision_requested)'}), 400

    error = ApprovalService.approve_version(article_id, version_id, username, status, comments)
    if error:
        return jsonify({'error': error}), 400

    return jsonify({'message': f'Version {version_id} approval recorded.'})


@app.route('/article/<int:article_id>/comments', methods=['POST'])
def add_comment(article_id):
    data = request.form
    version_id = data.get('version_id')
    comment_text = data.get('comment')
    username = get_current_username()

    if not version_id:
        return jsonify({'error': 'version_id is required'}), 400
    if not comment_text:
        return jsonify({'error': 'comment text is required'}), 400

    CommentService.add_comment(article_id, version_id, username, comment_text)
    return jsonify({'message': 'Comment added successfully.'})


if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(debug=True)
