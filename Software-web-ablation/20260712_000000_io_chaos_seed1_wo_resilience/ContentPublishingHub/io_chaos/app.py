from flask import Flask, request, session, redirect, url_for, render_template, abort
from datetime import datetime
import os
import threading

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# Lock for file writing to avoid concurrency issues.
write_lock = threading.Lock()

# File paths
ARTICLES_FILE = os.path.join(DATA_DIR, 'articles.txt')
ARTICLE_VERSIONS_FILE = os.path.join(DATA_DIR, 'article_versions.txt')
APPROVALS_FILE = os.path.join(DATA_DIR, 'approvals.txt')
COMMENTS_FILE = os.path.join(DATA_DIR, 'comments.txt')
WORKFLOW_STAGES_FILE = os.path.join(DATA_DIR, 'workflow_stages.txt')
ANALYTICS_FILE = os.path.join(DATA_DIR, 'analytics.txt')
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')


# ----------------------- Utility Functions -----------------------

def atomic_write(file_path, lines):
    # Write all lines atomically
    temp_path = file_path + '.tmp'
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    os.replace(temp_path, file_path)


def read_file_lines(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()


def parse_pipe_line(line, expected_fields):
    parts = line.rstrip('\n').split('|')
    if len(parts) != expected_fields:
        return None
    return parts


def parse_date(dt_str):
    try:
        return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    except Exception:
        return None


# ----------------------- Data Models -----------------------

# User Model
# users.txt assumed fields: user_id|username|full_name|email
# for session mapping we only use username and user_id here
class UserModel:
    @staticmethod
    def get_user_by_username(username):
        lines = read_file_lines(USERS_FILE)
        for line in lines:
            parts = parse_pipe_line(line, 4)
            if parts is None:
                continue
            user_id, uname, full_name, email = parts
            if uname == username:
                return {'user_id': int(user_id), 'username': uname, 'full_name': full_name, 'email': email}
        return None


# Article Model
# articles.txt assumed fields: article_id|title|author|category|status|created_at|updated_at
class ArticleModel:
    @staticmethod
    def get_all_articles():
        articles = []
        lines = read_file_lines(ARTICLES_FILE)
        for line in lines:
            parts = parse_pipe_line(line, 7)
            if parts is None:
                continue
            article_id, title, author, category, status, created_at, updated_at = parts
            articles.append({
                'article_id': int(article_id),
                'title': title,
                'author': author,
                'category': category,
                'status': status,
                'created_at': created_at,
                'updated_at': updated_at
            })
        return articles

    @staticmethod
    def get_article(article_id):
        articles = ArticleModel.get_all_articles()
        for article in articles:
            if article['article_id'] == article_id:
                return article
        return None

    @staticmethod
    def save_article(article):
        # article is dict with fields matching schema
        articles = ArticleModel.get_all_articles()
        updated = False
        for i, a in enumerate(articles):
            if a['article_id'] == article['article_id']:
                articles[i] = article
                updated = True
                break
        if not updated:
            articles.append(article)
        # Write back
        lines = [
            f"{a['article_id']}|{a['title']}|{a['author']}|{a['category']}|{a['status']}|{a['created_at']}|{a['updated_at']}\n"
            for a in articles
        ]
        with write_lock:
            atomic_write(ARTICLES_FILE, lines)

    @staticmethod
    def create_article(title, author, category):
        articles = ArticleModel.get_all_articles()
        max_id = max([a['article_id'] for a in articles], default=0)
        new_id = max_id + 1
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        article = {
            'article_id': new_id,
            'title': title,
            'author': author,
            'category': category,
            'status': 'draft',
            'created_at': now_str,
            'updated_at': now_str,
        }
        ArticleModel.save_article(article)
        return article


# Article Version Model
# article_versions.txt fields:
# version_id|article_id|version_number|author|content|timestamp|change_summary
class ArticleVersionModel:
    @staticmethod
    def get_versions_for_article(article_id):
        versions = []
        lines = read_file_lines(ARTICLE_VERSIONS_FILE)
        for line in lines:
            parts = parse_pipe_line(line, 7)
            if parts is None:
                continue
            version_id, art_id, version_num, author, content, timestamp, summary = parts
            if int(art_id) == article_id:
                versions.append({
                    'version_id': int(version_id),
                    'article_id': int(art_id),
                    'version_number': int(version_num),
                    'author': author,
                    'content': content,
                    'timestamp': timestamp,
                    'change_summary': summary
                })
        # sort by version_number ascending
        versions.sort(key=lambda v: v['version_number'])
        return versions

    @staticmethod
    def get_latest_version_number(article_id):
        versions = ArticleVersionModel.get_versions_for_article(article_id)
        if not versions:
            return 0
        return max(v['version_number'] for v in versions)

    @staticmethod
    def create_version(article_id, author, content, change_summary):
        versions = []
        lines = read_file_lines(ARTICLE_VERSIONS_FILE)
        for line in lines:
            parts = parse_pipe_line(line, 7)
            if parts is None:
                continue
            version_id = int(parts[0])
            versions.append(version_id)
        max_version_id = max(versions, default=0)
        new_version_id = max_version_id + 1
        version_number = ArticleVersionModel.get_latest_version_number(article_id) + 1
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line = f"{new_version_id}|{article_id}|{version_number}|{author}|{content}|{timestamp}|{change_summary}\n"
        with write_lock:
            with open(ARTICLE_VERSIONS_FILE, 'a', encoding='utf-8') as f:
                f.write(line)
        return {
            'version_id': new_version_id,
            'article_id': article_id,
            'version_number': version_number,
            'author': author,
            'content': content,
            'timestamp': timestamp,
            'change_summary': change_summary
        }


# Approval Model
# approvals.txt fields:
# approval_id|version_id|approver|status|comments|timestamp
class ApprovalModel:
    @staticmethod
    def get_approvals_for_version(version_id):
        approvals = []
        lines = read_file_lines(APPROVALS_FILE)
        for line in lines:
            parts = parse_pipe_line(line, 6)
            if parts is None:
                continue
            approval_id, v_id, approver, status, comments, timestamp = parts
            if int(v_id) == version_id:
                approvals.append({
                    'approval_id': int(approval_id),
                    'version_id': int(v_id),
                    'approver': approver,
                    'status': status,
                    'comments': comments,
                    'timestamp': timestamp
                })
        return approvals

    @staticmethod
    def add_or_update_approval(version_id, approver, status, comments):
        lines = read_file_lines(APPROVALS_FILE)
        approvals = []
        max_approval_id = 0
        found = False
        for line in lines:
            parts = parse_pipe_line(line, 6)
            if parts is None:
                continue
            approval_id, v_id, appr, stat, comm, ts = parts
            approval_id_i = int(approval_id)
            v_id_i = int(v_id)
            if approval_id_i > max_approval_id:
                max_approval_id = approval_id_i
            if v_id_i == version_id and appr == approver:
                # Update this approval
                new_line = f"{approval_id}|{version_id}|{approver}|{status}|{comments}|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                approvals.append(new_line)
                found = True
            else:
                approvals.append(line)
        if not found:
            # Add new approval
            new_approval_id = max_approval_id + 1
            new_line = f"{new_approval_id}|{version_id}|{approver}|{status}|{comments}|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            approvals.append(new_line)
        with write_lock:
            atomic_write(APPROVALS_FILE, approvals)


# Comments Model
# comments.txt fields:
# comment_id|version_id|commenter|comment|timestamp
class CommentModel:
    @staticmethod
    def get_comments_for_version(version_id):
        comments = []
        lines = read_file_lines(COMMENTS_FILE)
        for line in lines:
            parts = parse_pipe_line(line, 5)
            if parts is None:
                continue
            comment_id, v_id, commenter, comment, timestamp = parts
            if int(v_id) == version_id:
                comments.append({
                    'comment_id': int(comment_id),
                    'version_id': int(v_id),
                    'commenter': commenter,
                    'comment': comment,
                    'timestamp': timestamp
                })
        # Sort ascending by timestamp
        comments.sort(key=lambda c: c['timestamp'])
        return comments

    @staticmethod
    def add_comment(version_id, commenter, comment_text):
        lines = read_file_lines(COMMENTS_FILE)
        max_comment_id = 0
        for line in lines:
            parts = parse_pipe_line(line,5)
            if parts is None:
                continue
            comment_id = int(parts[0])
            if comment_id > max_comment_id:
                max_comment_id = comment_id
        new_id = max_comment_id + 1
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_line = f"{new_id}|{version_id}|{commenter}|{comment_text}|{timestamp}\n"
        with write_lock:
            with open(COMMENTS_FILE, 'a', encoding='utf-8') as f:
                f.write(new_line)


# Workflow Stage Model
# workflow_stages.txt fields:
# category|stage_number|stage_name|required_approver_role
class WorkflowStageModel:
    @staticmethod
    def get_stages():
        stages = []
        lines = read_file_lines(WORKFLOW_STAGES_FILE)
        for line in lines:
            parts = parse_pipe_line(line, 4)
            if parts is None:
                continue
            category, stage_num, stage_name, role = parts
            stages.append({
                'category': category,
                'stage_number': int(stage_num),
                'stage_name': stage_name,
                'required_approver_role': role
            })
        return stages

    @staticmethod
    def get_stages_for_category(category):
        return [s for s in WorkflowStageModel.get_stages() if s['category'] == category]


# Analytics Model
# analytics.txt fields:
# record_id|article_id|views|unique_visitors|avg_time_seconds|shares|date
class AnalyticsModel:
    @staticmethod
    def get_analytics_for_article(article_id):
        records = []
        lines = read_file_lines(ANALYTICS_FILE)
        for line in lines:
            parts = parse_pipe_line(line, 7)
            if parts is None:
                continue
            record_id, a_id, views, uv, avg_time, shares, date_str = parts
            if int(a_id) == article_id:
                records.append({
                    'record_id': int(record_id),
                    'article_id': int(a_id),
                    'views': int(views),
                    'unique_visitors': int(uv),
                    'avg_time_seconds': float(avg_time),
                    'shares': int(shares),
                    'date': date_str
                })
        return records


# ----------------------- Service Layer -----------------------

class ArticleService:
    @staticmethod
    def create_article(title, author, category):
        # Basic validation
        if not title or not author or not category:
            return None, 'Title, author, and category are required.'
        article = ArticleModel.create_article(title, author, category)
        # Also create initial version with empty content
        ArticleVersionModel.create_version(article['article_id'], author, '', 'Initial version')
        return article, None

    @staticmethod
    def update_article_version(article_id, author, content, change_summary):
        # Validate article exists
        article = ArticleModel.get_article(article_id)
        if not article:
            return None, 'Article not found.'
        # Create new version
        new_version = ArticleVersionModel.create_version(article_id, author, content, change_summary)
        # Update article updated_at
        article['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ArticleModel.save_article(article)
        return new_version, None

    @staticmethod
    def get_article_versions(article_id):
        return ArticleVersionModel.get_versions_for_article(article_id)

    @staticmethod
    def get_article_with_versions(article_id):
        article = ArticleModel.get_article(article_id)
        if not article:
            return None
        versions = ArticleVersionModel.get_versions_for_article(article_id)
        return article, versions

    @staticmethod
    def get_user_articles(username, filters=None):
        # Filters could include category, status, etc.
        articles = ArticleModel.get_all_articles()
        user_articles = [a for a in articles if a['author'] == username]
        if filters:
            for k, v in filters.items():
                if v:
                    user_articles = [a for a in user_articles if a.get(k) == v]
        return user_articles

    @staticmethod
    def get_published_articles(category=None, sort_by=None):
        articles = ArticleModel.get_all_articles()
        published = [a for a in articles if a['status'] == 'published']
        if category:
            published = [a for a in published if a['category'] == category]
        if sort_by == 'date_desc':
            published.sort(key=lambda x: x['created_at'], reverse=True)
        elif sort_by == 'date_asc':
            published.sort(key=lambda x: x['created_at'])
        return published


class WorkflowService:
    @staticmethod
    def get_stages_for_category(category):
        return WorkflowStageModel.get_stages_for_category(category)

    @staticmethod
    def check_approval_progress(article_id):
        # Example: check if all necessary approvals done for latest version
        article = ArticleModel.get_article(article_id)
        if not article:
            return False
        versions = ArticleVersionModel.get_versions_for_article(article_id)
        if not versions:
            return False
        latest_version = versions[-1]
        stages = WorkflowStageModel.get_stages_for_category(article['category'])
        approvals = ApprovalModel.get_approvals_for_version(latest_version['version_id'])

        required_roles = [stage['required_approver_role'] for stage in stages]
        approval_roles_done = [a['approver'] for a in approvals if a['status'].lower() == 'approved']
        # We do a simplified check matching approver as role name
        return all(role in approval_roles_done for role in required_roles)


class AnalyticsService:
    @staticmethod
    def aggregate_article_analytics(article_id):
        records = AnalyticsModel.get_analytics_for_article(article_id)
        if not records:
            return {'views': 0, 'unique_visitors': 0, 'avg_time_seconds': 0.0, 'shares': 0, 'likes': 0, 'comments': 0}
        total_views = sum(r['views'] for r in records)
        total_unique = sum(r['unique_visitors'] for r in records)
        # weighted avg time
        weighted_time_sum = sum(r['avg_time_seconds'] * r['views'] for r in records)
        avg_time = weighted_time_sum / total_views if total_views else 0.0
        total_shares = sum(r['shares'] for r in records)
        # Likes and comments not present in analytics.txt; mock 0
        return {
            'views': total_views,
            'unique_visitors': total_unique,
            'avg_time_seconds': avg_time,
            'shares': total_shares,
            'likes': 0,
            'comments': 0
        }


# ----------------------- Routes -----------------------

@app.route('/')
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    # Prepare quick stats and recent activities - mocked for example
    quick_stats = {
        'total_articles': len(ArticleModel.get_all_articles()),
        'published_articles': len(ArticleService.get_published_articles()),
        'pending_approvals': 0,
        'comments': 0
    }

    recent_activities = []
    # Could load recent edits, comments, approvals
    # For demo, just empty list

    return render_template('dashboard.html', username=username, quick_stats=quick_stats, recent_activities=recent_activities)


@app.route('/article/create', methods=['GET', 'POST'])
def create_article():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()

        article, error = ArticleService.create_article(title, username, category)
        if error:
            # Pass errors as list for template
            return render_template('create_article.html', errors=[error], form_data={'title': title, 'category': category})

        return redirect(url_for('edit_article', article_id=article['article_id']))

    return render_template('create_article.html', errors=None, form_data=None)


@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    article = ArticleModel.get_article(article_id)
    if not article:
        abort(404)

    # Authorization: only author can edit
    if article['author'] != username:
        abort(403)

    versions = ArticleVersionModel.get_versions_for_article(article_id)
    latest_version = versions[-1] if versions else None

    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        change_summary = request.form.get('change_summary', '').strip()

        if not content:
            error = 'Content cannot be empty.'
            return render_template('edit_article.html', article=article, latest_version=latest_version, error=error)

        if not change_summary:
            change_summary = 'Updated content'

        new_version, error = ArticleService.update_article_version(article_id, username, content, change_summary)
        if error:
            return render_template('edit_article.html', article=article, latest_version=latest_version, error=error)

        return redirect(url_for('edit_article', article_id=article_id))

    return render_template('edit_article.html', article=article, latest_version=latest_version, error=None)


@app.route('/article/<int:article_id>/versions')
def article_version_history(article_id):
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    article = ArticleModel.get_article(article_id)
    if not article:
        abort(404)

    versions = ArticleVersionModel.get_versions_for_article(article_id)
    # Also get approvals and comments per version
    versions_details = []
    for v in versions:
        approvals = ApprovalModel.get_approvals_for_version(v['version_id'])
        comments = CommentModel.get_comments_for_version(v['version_id'])
        versions_details.append({'version': v, 'approvals': approvals, 'comments': comments})

    return render_template('version_history.html', article=article, versions_details=versions_details)


@app.route('/articles/mine')
def my_articles():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    # Filters from query params
    category = request.args.get('category')
    status = request.args.get('status')
    filters = {}
    if category:
        filters['category'] = category
    if status:
        filters['status'] = status

    articles = ArticleService.get_user_articles(username, filters)

    # Prepare article display info
    # Provide last_edited as updated_at for display
    for a in articles:
        a['last_edited'] = a.get('updated_at', '')
        # Provide id for template convenience
        a['id'] = a['article_id']

    return render_template('my_articles.html', articles=articles, username=username)


@app.route('/articles/published')
def published_articles():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    category = request.args.get('category')
    sort_by = request.args.get('sort')  # adjusted to 'sort' from template

    articles = ArticleService.get_published_articles(category=category, sort_by=sort_by)

    # Get categories from all published to list
    categories = list(set(a['category'] for a in ArticleModel.get_all_articles() if a['status']=='published'))

    # Prepare published_date for display
    for a in articles:
        a['published_date'] = a.get('updated_at', '')
        # Provide id for template convenience
        a['id'] = a['article_id']

    return render_template('published_articles.html', articles=articles, categories=categories, selected_category=category, sort_by=sort_by)


@app.route('/calendar')
def content_calendar():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    # Prepare scheduled publications, assuming articles with status "scheduled"
    articles = ArticleModel.get_all_articles()
    scheduled = [a for a in articles if a['status'] == 'scheduled']

    # Group by scheduled date if available; since no schedule date info, group by updated_at date (YYYY-MM-DD)
    scheduled_publications = {}
    for a in scheduled:
        # Here using updated_at date as proxy for schedule date
        date_key = a['updated_at'][:10] if a['updated_at'] else 'Unknown'
        if date_key not in scheduled_publications:
            scheduled_publications[date_key] = []
        scheduled_publications[date_key].append({'title': a['title'], 'id': a['article_id']})

    return render_template('content_calendar.html', scheduled_publications=scheduled_publications)


@app.route('/article/<int:article_id>/analytics')
def article_analytics(article_id):
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    article = ArticleModel.get_article(article_id)
    if not article:
        abort(404)

    analytics_data = AnalyticsService.aggregate_article_analytics(article_id)

    return render_template('article_analytics.html', article=article, analytics=analytics_data)


# Placeholder login route for completeness, not specified but to avoid redirect loops
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        # Simple login for demo: check user exists
        user = UserModel.get_user_by_username(username)
        if user:
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username')
    return render_template('login.html')


# Start the flask app on typical development port
if __name__ == '__main__':
    app.run(debug=True)
