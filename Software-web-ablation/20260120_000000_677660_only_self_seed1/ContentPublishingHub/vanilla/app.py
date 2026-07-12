from flask import Flask, request, session, g, redirect, url_for, render_template, abort
import os
from datetime import datetime

# Data directory and filenames
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
ARTICLES_FILE = os.path.join(DATA_DIR, 'articles.txt')
ARTICLE_VERSIONS_FILE = os.path.join(DATA_DIR, 'article_versions.txt')
APPROVALS_FILE = os.path.join(DATA_DIR, 'approvals.txt')
COMMENTS_FILE = os.path.join(DATA_DIR, 'comments.txt')
ANALYTICS_FILE = os.path.join(DATA_DIR, 'analytics.txt')
WORKFLOW_STAGES_FILE = os.path.join(DATA_DIR, 'workflow_stages.txt')
CALENDAR_FILE = os.path.join(DATA_DIR, 'calendar.txt')

# Utility functions for file I/O and data parsing

def read_pipe_delimited_file(filename, fieldnames):
    records = []
    if not os.path.exists(filename):
        return records
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip('\n\r ')
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != len(fieldnames):
                # skip malformed line
                continue
            record = dict(zip(fieldnames, parts))
            records.append(record)
    return records


def append_pipe_delimited_file(filename, fieldnames, record_dict):
    values = []
    for field in fieldnames:
        val = record_dict.get(field, '')
        if val is None:
            val = ''
        if isinstance(val, str):
            val = val.replace('\n', ' ').replace('|', ' ')
        values.append(str(val))
    with open(filename, 'a', encoding='utf-8') as f:
        f.write('|'.join(values)+'\n')


def overwrite_pipe_delimited_file(filename, fieldnames, records):
    with open(filename, 'w', encoding='utf-8') as f:
        for rec in records:
            values = []
            for field in fieldnames:
                val = rec.get(field, '')
                if val is None:
                    val = ''
                if isinstance(val, str):
                    val = val.replace('\n', ' ').replace('|', ' ')
                values.append(str(val))
            f.write('|'.join(values)+'\n')


# Models

# User model
class User:
    FIELDS = ['username', 'fullname', 'email']

    def __init__(self, username, fullname, email):
        self.username = username
        self.fullname = fullname
        self.email = email

    @classmethod
    def load_all(cls):
        users = read_pipe_delimited_file(USERS_FILE, cls.FIELDS)
        return [cls(**u) for u in users]

    @classmethod
    def find_by_username(cls, username):
        all_users = cls.load_all()
        for user in all_users:
            if user.username == username:
                return user
        return None


# Article model
class Article:
    # Fields as per articles.txt
    # article_id|title|category|author|status|created_at|updated_at
    FIELDS = ['article_id','title','category','author','status','created_at','updated_at']

    def __init__(self, article_id, title, category, author, status, created_at, updated_at):
        self.article_id = int(article_id)
        self.title = title
        self.category = category
        self.author = author
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def load_all(cls):
        articles = read_pipe_delimited_file(ARTICLES_FILE, cls.FIELDS)
        result = []
        for a in articles:
            try:
                result.append(Article(**a))
            except Exception:
                # malformed line
                continue
        return result

    @classmethod
    def find_by_id(cls, article_id):
        if not isinstance(article_id, int):
            try:
                article_id = int(article_id)
            except:
                return None
        for a in cls.load_all():
            if a.article_id == article_id:
                return a
        return None

    @classmethod
    def find_by_author(cls, author):
        return [a for a in cls.load_all() if a.author == author]

    @classmethod
    def find_published(cls, category_filter=None, sort_key=None):
        articles = [a for a in cls.load_all() if a.status == 'published']
        if category_filter:
            articles = [a for a in articles if a.category == category_filter]
        if sort_key == 'created_at' or sort_key == 'date':
            articles.sort(key=lambda x:x.created_at, reverse=True)
        elif sort_key == 'title':
            articles.sort(key=lambda x:x.title)
        return articles

    @classmethod
    def next_article_id(cls):
        articles = cls.load_all()
        if not articles:
            return 1
        max_id = max(a.article_id for a in articles)
        return max_id + 1

    def to_dict(self):
        return {
            'article_id': self.article_id,
            'title': self.title,
            'category': self.category,
            'author': self.author,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def save(self):
        all_articles = Article.load_all()
        updated = False
        for i,a in enumerate(all_articles):
            if a.article_id == self.article_id:
                all_articles[i] = self
                updated = True
                break
        if not updated:
            all_articles.append(self)
        # Write back
        records = [a.to_dict() for a in all_articles]
        overwrite_pipe_delimited_file(ARTICLES_FILE, Article.FIELDS, records)


# ArticleVersion model
class ArticleVersion:
    # article_versions.txt fields:
    # version_id|article_id|version_number|content|author|timestamp|change_summary
    FIELDS = ['version_id','article_id','version_number','content','author','timestamp','change_summary']

    def __init__(self, version_id, article_id, version_number, content, author, timestamp, change_summary):
        self.version_id = int(version_id)
        self.article_id = int(article_id)
        self.version_number = int(version_number)
        self.content = content
        self.author = author
        self.timestamp = timestamp
        self.change_summary = change_summary

    @classmethod
    def load_all(cls):
        records = read_pipe_delimited_file(ARTICLE_VERSIONS_FILE, cls.FIELDS)
        result = []
        for rec in records:
            try:
                result.append(ArticleVersion(**rec))
            except Exception:
                continue
        return result

    @classmethod
    def find_by_article(cls, article_id):
        return [v for v in cls.load_all() if v.article_id == int(article_id)]

    @classmethod
    def find_latest_version_number(cls, article_id):
        versions = cls.find_by_article(article_id)
        if not versions:
            return 0
        return max(v.version_number for v in versions)

    @classmethod
    def find_by_version_id(cls, version_id):
        for v in cls.load_all():
            if v.version_id == int(version_id):
                return v
        return None

    @classmethod
    def next_version_id(cls):
        versions = cls.load_all()
        if not versions:
            return 1
        return max(v.version_id for v in versions) + 1

    def to_dict(self):
        return {
            'version_id': self.version_id,
            'article_id': self.article_id,
            'version_number': self.version_number,
            'content': self.content,
            'author': self.author,
            'timestamp': self.timestamp,
            'change_summary': self.change_summary
        }

    def save(self):
        versions = ArticleVersion.load_all()
        updated = False
        for i,v in enumerate(versions):
            if v.version_id == self.version_id:
                versions[i] = self
                updated = True
                break
        if not updated:
            versions.append(self)
        records = [v.to_dict() for v in versions]
        overwrite_pipe_delimited_file(ARTICLE_VERSIONS_FILE, ArticleVersion.FIELDS, records)


# Approval model
class Approval:
    # approvals.txt fields:
    # approval_id|article_id|version_id|approver|status|comments|timestamp
    FIELDS = ['approval_id','article_id','version_id','approver','status','comments','timestamp']

    def __init__(self, approval_id, article_id, version_id, approver, status, comments, timestamp):
        self.approval_id = int(approval_id)
        self.article_id = int(article_id)
        self.version_id = int(version_id)
        self.approver = approver
        self.status = status
        self.comments = comments
        self.timestamp = timestamp

    @classmethod
    def load_all(cls):
        records = read_pipe_delimited_file(APPROVALS_FILE, cls.FIELDS)
        result = []
        for rec in records:
            try:
                result.append(Approval(**rec))
            except Exception:
                continue
        return result

    @classmethod
    def find_by_article_and_version(cls, article_id, version_id):
        return [a for a in cls.load_all() if a.article_id == int(article_id) and a.version_id == int(version_id)]

    @classmethod
    def next_approval_id(cls):
        approvals = cls.load_all()
        if not approvals:
            return 1
        return max(a.approval_id for a in approvals) + 1

    def to_dict(self):
        return {
            'approval_id': self.approval_id,
            'article_id': self.article_id,
            'version_id': self.version_id,
            'approver': self.approver,
            'status': self.status,
            'comments': self.comments,
            'timestamp': self.timestamp
        }

    def save(self):
        approvals = Approval.load_all()
        updated = False
        for i,a in enumerate(approvals):
            if a.approval_id == self.approval_id:
                approvals[i] = self
                updated = True
                break
        if not updated:
            approvals.append(self)
        records = [a.to_dict() for a in approvals]
        overwrite_pipe_delimited_file(APPROVALS_FILE, Approval.FIELDS, records)


# Comment model
class Comment:
    # comments.txt fields:
    # comment_id|article_id|version_id|commenter|comment_text|timestamp
    FIELDS = ['comment_id','article_id','version_id','commenter','comment_text','timestamp']

    def __init__(self, comment_id, article_id, version_id, commenter, comment_text, timestamp):
        self.comment_id = int(comment_id)
        self.article_id = int(article_id)
        self.version_id = int(version_id)
        self.commenter = commenter
        self.comment_text = comment_text
        self.timestamp = timestamp

    @classmethod
    def load_all(cls):
        records = read_pipe_delimited_file(COMMENTS_FILE, cls.FIELDS)
        result = []
        for rec in records:
            try:
                result.append(Comment(**rec))
            except Exception:
                continue
        return result

    @classmethod
    def find_by_article_and_version(cls, article_id, version_id):
        return [c for c in cls.load_all() if c.article_id == int(article_id) and c.version_id == int(version_id)]

    @classmethod
    def next_comment_id(cls):
        comments = cls.load_all()
        if not comments:
            return 1
        return max(c.comment_id for c in comments) + 1

    def to_dict(self):
        return {
            'comment_id': self.comment_id,
            'article_id': self.article_id,
            'version_id': self.version_id,
            'commenter': self.commenter,
            'comment_text': self.comment_text,
            'timestamp': self.timestamp
        }

    def save(self):
        comments = Comment.load_all()
        updated = False
        for i,c in enumerate(comments):
            if c.comment_id == self.comment_id:
                comments[i] = self
                updated = True
                break
        if not updated:
            comments.append(self)
        records = [c.to_dict() for c in comments]
        overwrite_pipe_delimited_file(COMMENTS_FILE, Comment.FIELDS, records)


# Analytics model
class AnalyticsEntry:
    # analytics.txt fields:
    # entry_id|article_id|date|views|unique_visitors|avg_time_seconds|shares
    FIELDS = ['entry_id','article_id','date','views','unique_visitors','avg_time_seconds','shares']

    def __init__(self, entry_id, article_id, date, views, unique_visitors, avg_time_seconds, shares):
        self.entry_id = int(entry_id)
        self.article_id = int(article_id)
        self.date = date
        self.views = int(views)
        self.unique_visitors = int(unique_visitors)
        self.avg_time_seconds = float(avg_time_seconds)
        self.shares = int(shares)

    @classmethod
    def load_all(cls):
        records = read_pipe_delimited_file(ANALYTICS_FILE, cls.FIELDS)
        result = []
        for rec in records:
            try:
                result.append(AnalyticsEntry(**rec))
            except Exception:
                continue
        return result

    @classmethod
    def find_by_article(cls, article_id):
        return [e for e in cls.load_all() if e.article_id == int(article_id)]


# WorkflowStage model (not explicitly used in routes, but available)
class WorkflowStage:
    # workflow_stages.txt fields:
    # stage_id|category|stage_order|description
    FIELDS = ['stage_id','category','stage_order','description']

    def __init__(self, stage_id, category, stage_order, description):
        self.stage_id = int(stage_id)
        self.category = category
        self.stage_order = int(stage_order)
        self.description = description

    @classmethod
    def load_all(cls):
        records = read_pipe_delimited_file(WORKFLOW_STAGES_FILE, cls.FIELDS)
        result = []
        for rec in records:
            try:
                result.append(WorkflowStage(**rec))
            except:
                continue
        return result


# Business logic services


class ArticleService:
    @staticmethod
    def create_article(title, category, author):
        new_id = Article.next_article_id()
        now = datetime.utcnow().isoformat()
        article = Article(
            article_id=new_id,
            title=title,
            category=category,
            author=author,
            status='draft',
            created_at=now,
            updated_at=now
        )
        article.save()
        # Create initial version empty with version_number 1
        version = ArticleVersion(
            version_id=ArticleVersion.next_version_id(),
            article_id=new_id,
            version_number=1,
            content='',
            author=author,
            timestamp=now,
            change_summary="Initial version"
        )
        version.save()
        return article

    @staticmethod
    def update_article(article_id, title, category):
        article = Article.find_by_id(article_id)
        if not article:
            return None
        article.title = title
        article.category = category
        article.updated_at = datetime.utcnow().isoformat()
        article.save()
        return article


class VersionService:
    @staticmethod
    def create_version(article_id, content, author, change_summary):
        article = Article.find_by_id(article_id)
        if not article:
            return None
        next_version_num = ArticleVersion.find_latest_version_number(article_id) + 1
        version = ArticleVersion(
            version_id=ArticleVersion.next_version_id(),
            article_id=article_id,
            version_number=next_version_num,
            content=content,
            author=author,
            timestamp=datetime.utcnow().isoformat(),
            change_summary=change_summary
        )
        version.save()
        # Update article updated_at
        article.updated_at = datetime.utcnow().isoformat()
        article.save()
        return version

    @staticmethod
    def get_versions(article_id):
        return sorted(ArticleVersion.find_by_article(article_id), key=lambda v: v.version_number)


class ApprovalService:
    @staticmethod
    def add_approval(article_id, version_id, approver, status, comments):
        approval_id = Approval.next_approval_id()
        approval = Approval(
            approval_id=approval_id,
            article_id=article_id,
            version_id=version_id,
            approver=approver,
            status=status,
            comments=comments,
            timestamp=datetime.utcnow().isoformat()
        )
        approval.save()
        return approval

    @staticmethod
    def get_approvals(article_id, version_id):
        return Approval.find_by_article_and_version(article_id, version_id)


class CommentService:
    @staticmethod
    def add_comment(article_id, version_id, commenter, comment_text):
        comment_id = Comment.next_comment_id()
        comment = Comment(
            comment_id=comment_id,
            article_id=article_id,
            version_id=version_id,
            commenter=commenter,
            comment_text=comment_text,
            timestamp=datetime.utcnow().isoformat()
        )
        comment.save()
        return comment

    @staticmethod
    def get_comments(article_id, version_id):
        return Comment.find_by_article_and_version(article_id, version_id)


class AnalyticsService:
    @staticmethod
    def get_analytics_for_article(article_id):
        analytics_entries = AnalyticsEntry.find_by_article(article_id)
        # Aggregate overall data
        total_views = sum(entry.views for entry in analytics_entries)
        total_unique = sum(entry.unique_visitors for entry in analytics_entries)
        average_time = 0
        if analytics_entries:
            average_time = sum(entry.avg_time_seconds * entry.views for entry in analytics_entries) / max(total_views,1)
        total_shares = sum(entry.shares for entry in analytics_entries)

        # Calculate comments and approvals counts per date
        comments = Comment.load_all()
        approvals = Approval.load_all()

        comment_counts = {}
        approval_counts = {}

        for c in comments:
            if c.article_id == int(article_id):
                date_only = c.timestamp.split('T')[0]
                comment_counts[date_only] = comment_counts.get(date_only, 0) + 1

        for a in approvals:
            if a.article_id == int(article_id):
                date_only = a.timestamp.split('T')[0]
                approval_counts[date_only] = approval_counts.get(date_only, 0) + 1

        daily_data = []
        for entry in sorted(analytics_entries, key=lambda e: e.date):
            date = entry.date
            daily_data.append({
                'date': date,
                'views': entry.views,
                'comments': comment_counts.get(date, 0),
                'approvals': approval_counts.get(date, 0)
            })

        return {
            'total_views': total_views,
            'total_unique_visitors': total_unique,
            'average_time_seconds': round(average_time, 2),
            'total_shares': total_shares,
            'daily_data': daily_data
        }


# Simple input validation (only very basic validations)

def validate_article_form(form):
    errors = {}
    title = form.get('title','').strip()
    category = form.get('category','').strip()
    if not title:
        errors['title'] = "Title cannot be empty."
    if not category:
        errors['category'] = "Category cannot be empty."
    return errors


def validate_schedule_form(form):
    errors = {}
    scheduled_date = form.get('scheduled_date','').strip()
    article_id = form.get('article_id','').strip()
    if not scheduled_date:
        errors['scheduled_date'] = "Scheduled date is required."
    if not article_id:
        errors['article_id'] = "Article ID is required."
    else:
        try:
            int(article_id)
        except:
            errors['article_id'] = "Article ID must be a number."
    return errors


# Flask app factory
app = Flask(__name__)
app.secret_key = 'supersecretkey'


# Before request - set user in g from session
@app.before_request
def load_logged_in_user():
    g.user = None
    username = session.get('username')
    if username:
        user = User.find_by_username(username)
        if user:
            g.user = user


# Ensure DATA_DIR and necessary files exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

required_files = [USERS_FILE, ARTICLES_FILE, ARTICLE_VERSIONS_FILE, APPROVALS_FILE, COMMENTS_FILE, ANALYTICS_FILE, WORKFLOW_STAGES_FILE, CALENDAR_FILE]
for filepath in required_files:
    if not os.path.exists(filepath):
        open(filepath, 'a').close()


# Root redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


# Route: /dashboard
@app.route('/dashboard')
def dashboard():
    if not g.user:
        return redirect(url_for('root_redirect'))

    # Provide an article ID for analytics link - choose first user's article or None
    user_articles = Article.find_by_author(g.user.username)
    analytics_article_id = user_articles[0].article_id if user_articles else None

    return render_template('dashboard.html', username=g.user.username, analytics_article_id=analytics_article_id)


# Route: /article/create (GET, POST)
@app.route('/article/create', methods=['GET','POST'])
def create_article():
    if not g.user:
        return redirect(url_for('root_redirect'))
    if request.method == 'POST':
        form = request.form
        errors = validate_article_form(form)
        if errors:
            # Pass form data as 'article' to match template
            return render_template('create_article.html', validation_errors=errors, article=form)
        title = form.get('title','').strip()
        category = form.get('category','').strip()
        author = g.user.username
        article = ArticleService.create_article(title, category, author)
        return redirect(url_for('edit_article', article_id=article.article_id))
    else:
        return render_template('create_article.html')


# Route: /article/<int:article_id>/edit (GET, POST)
@app.route('/article/<int:article_id>/edit', methods=['GET','POST'])
def edit_article(article_id):
    if not g.user:
        return redirect(url_for('root_redirect'))
    article = Article.find_by_id(article_id)
    if not article:
        abort(404)
    if request.method == 'POST':
        form = request.form
        errors = validate_article_form(form)
        if errors:
            # Provide form and article to template
            return render_template('edit_article.html', validation_errors=errors, article=article, form=form)

        # update article main info
        updated_article = ArticleService.update_article(article_id, form.get('title','').strip(), form.get('category','').strip())

        # Create new version if content or change_summary provided
        content = form.get('content','').strip()
        change_summary = form.get('change_summary','').strip()

        if content or change_summary:
            if not change_summary:
                change_summary = "Updated content"
            VersionService.create_version(article_id, content, g.user.username, change_summary)

        return redirect(url_for('edit_article', article_id=article_id))

    else:
        versions = VersionService.get_versions(article_id)
        latest_version = versions[-1] if versions else None
        content_value = latest_version.content if latest_version else ''
        return render_template('edit_article.html', article=article, current_version=latest_version, content=content_value)


# Route: /article/<int:article_id>/versions (GET)
@app.route('/article/<int:article_id>/versions')
def article_version_history(article_id):
    if not g.user:
        return redirect(url_for('root_redirect'))
    article = Article.find_by_id(article_id)
    if not article:
        abort(404)
    versions = VersionService.get_versions(article_id)
    return render_template('version_history.html', article=article, versions=versions)


# Route: /articles/mine (GET)
@app.route('/articles/mine')
def my_articles():
    if not g.user:
        return redirect(url_for('root_redirect'))
    articles_raw = Article.find_by_author(g.user.username)
    articles = []
    for art in articles_raw:
        articles.append({
            'id': art.article_id,
            'title': art.title,
            'status': art.status,
            'last_modified': art.updated_at
        })
    return render_template('my_articles.html', articles=articles)


# Route: /articles/published (GET)
@app.route('/articles/published')
def published_articles():
    category = request.args.get('category', None)
    sort = request.args.get('sort', None)
    articles_raw = Article.find_published(category_filter=category, sort_key=sort)
    all_categories = set(a.category for a in Article.load_all() if a.status == 'published')
    categories = sorted(all_categories)
    articles = []
    for art in articles_raw:
        articles.append({
            'id': art.article_id,
            'title': art.title,
            'author': art.author,
            'category': art.category,
            'publish_date': art.updated_at
        })
    return render_template('published_articles.html', articles=articles, categories=categories, selected_category=category, selected_sort=sort)


# Calendar scheduling
CALENDAR_FILE = os.path.join(DATA_DIR, 'calendar.txt')
CALENDAR_FIELDS = ['calendar_id','article_id','scheduled_date','notes']


class CalendarEntry:
    def __init__(self, calendar_id, article_id, scheduled_date, notes):
        self.calendar_id = int(calendar_id)
        self.article_id = int(article_id)
        self.scheduled_date = scheduled_date
        self.notes = notes

    @classmethod
    def load_all(cls):
        records = read_pipe_delimited_file(CALENDAR_FILE, CALENDAR_FIELDS)
        result = []
        for rec in records:
            try:
                result.append(CalendarEntry(**rec))
            except Exception:
                continue
        return result

    @classmethod
    def next_calendar_id(cls):
        entries = cls.load_all()
        if not entries:
            return 1
        return max(e.calendar_id for e in entries) + 1

    def to_dict(self):
        return {
            'calendar_id': self.calendar_id,
            'article_id': self.article_id,
            'scheduled_date': self.scheduled_date,
            'notes': self.notes
        }

    def save(self):
        entries = CalendarEntry.load_all()
        updated = False
        for i,e in enumerate(entries):
            if e.calendar_id == self.calendar_id:
                entries[i] = self
                updated = True
                break
        if not updated:
            entries.append(self)
        records = [e.to_dict() for e in entries]
        overwrite_pipe_delimited_file(CALENDAR_FILE, CALENDAR_FIELDS, records)


@app.route('/calendar', methods=['GET','POST'])
def content_calendar():
    if not g.user:
        return redirect(url_for('root_redirect'))
    if request.method == 'POST':
        form = request.form
        errors = validate_schedule_form(form)
        if errors:
            scheduled_items = CalendarEntry.load_all()
            articles_map = {a.article_id:a.title for a in Article.load_all()}
            scheduled_items_display = []
            for item in scheduled_items:
                scheduled_items_display.append({
                    'id': item.calendar_id,
                    'article_title': articles_map.get(item.article_id, 'Unknown'),
                    'schedule_date': item.scheduled_date
                })
            return render_template('content_calendar.html', validation_errors=errors, scheduled_items=scheduled_items_display, unscheduled_articles=[])

        article_id = int(form.get('article_id').strip())
        scheduled_date = form.get('scheduled_date').strip()
        notes = form.get('notes','').strip()
        calendar_id = CalendarEntry.next_calendar_id()
        calendar_entry = CalendarEntry(calendar_id, article_id, scheduled_date, notes)
        calendar_entry.save()
        return redirect(url_for('content_calendar'))
    else:
        scheduled_items = CalendarEntry.load_all()
        articles_map = {a.article_id:a.title for a in Article.load_all()}
        scheduled_items_display = []
        for item in scheduled_items:
            scheduled_items_display.append({
                'id': item.calendar_id,
                'article_title': articles_map.get(item.article_id, 'Unknown'),
                'schedule_date': item.scheduled_date
            })

        scheduled_article_ids = set(item.article_id for item in scheduled_items)
        unscheduled_articles_raw = [a for a in Article.find_published() if a.article_id not in scheduled_article_ids]
        unscheduled_articles = []
        for art in unscheduled_articles_raw:
            unscheduled_articles.append({'id': art.article_id, 'title': art.title})

        return render_template('content_calendar.html', scheduled_items=scheduled_items_display, unscheduled_articles=unscheduled_articles)


# Route: /article/<int:article_id>/analytics (GET)
@app.route('/article/<int:article_id>/analytics')
def article_analytics(article_id):
    if not g.user:
        return redirect(url_for('root_redirect'))
    article = Article.find_by_id(article_id)
    if not article:
        abort(404)
    analytics_data = AnalyticsService.get_analytics_for_article(article_id)
    return render_template('article_analytics.html', article=article, analytics=analytics_data)


# Run the app if executed directly
if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(CALENDAR_FILE):
        with open(CALENDAR_FILE, 'a') as f:
            pass
    app.run(debug=True)
