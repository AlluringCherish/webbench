from flask import Flask, request, render_template, redirect, url_for, session, abort, flash
from services.article_service import ArticleService
from services.user_service import UserService
from services.analytics_service import AnalyticsService
from services.approval_service import ApprovalService
from services.comment_service import CommentService

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Initialize service instances for separation of concerns and business logic
article_service = ArticleService()
user_service = UserService()
analytics_service = AnalyticsService()
approval_service = ApprovalService()
comment_service = CommentService()

# Decorator enforcing user session authentication
def login_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper

# Route: GET /dashboard - shows user dashboard with quick stats and recent activity
@app.route('/dashboard')
@login_required
def dashboard():
    current_user = session['user']
    quick_stats = article_service.get_quick_stats(current_user)
    recent_activity = article_service.get_recent_activity(current_user)
    return render_template('dashboard.html',
                           username=current_user,
                           quick_stats=quick_stats,
                           recent_activity=recent_activity)

# Route: GET, POST /article/create - create new article, with validation and success/errors context
@app.route('/article/create', methods=['GET', 'POST'])
@login_required
def create_article():
    current_user = session['user']
    errors = {}
    success_flag = False
    if request.method == 'POST':
        form_data = request.form.to_dict()
        # Additional backend validation for empty title
        if not form_data.get('title') or not form_data.get('title').strip():
            errors['title'] = 'Title cannot be empty.'
        else:
            success_flag, errors = article_service.create_article(current_user, form_data)
        if success_flag:
            flash('Article created successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Error creating article.', 'error')
    return render_template('create_article.html',
                           errors=errors,
                           success_flag=success_flag)

# Route: GET, POST /article/<article_id>/edit - edit existing article; passes article, errors, current_version
@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    current_user = session['user']
    article, errors, current_version = article_service.get_article_and_version(article_id, current_user)
    if article is None:
        abort(404)
    if request.method == 'POST':
        form_data = request.form.to_dict()
        success, form_errors = article_service.update_article(article_id, current_user, form_data)
        # Replace errors dictionary to show form errors on frontend
        if not errors:
            errors = {}
        errors.update(form_errors)
        if success:
            flash('Article updated successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Error updating article.', 'error')
    return render_template('edit_article.html',
                           article=article,
                           errors=errors,
                           current_version=current_version)

# Route: GET /article/<article_id>/versions - fetch all versions for comparison/history display
@app.route('/article/<int:article_id>/versions')
@login_required
def article_version_history(article_id):
    current_user = session['user']
    versions = article_service.get_versions(article_id, current_user)
    if versions is None:
        abort(404)
    comparison_data = article_service.get_comparison_data(article_id, current_user)
    return render_template('article_versions.html',
                           article_id=article_id,
                           versions=versions,
                           comparison_data=comparison_data)

# Route: GET /articles/mine - user\u001as articles with optional status filter
@app.route('/articles/mine')
@login_required
def my_articles():
    current_user = session['user']
    filter_status = request.args.get('status')
    articles = article_service.get_user_articles(current_user, filter_status)
    filter_status_options = article_service.get_filter_status_options()
    return render_template('my_articles.html',
                           articles=articles,
                           filter_status_options=filter_status_options)

# Route: GET /articles/published - published articles listing with category and sort options
@app.route('/articles/published')
def published_articles():
    category = request.args.get('category')
    sort = request.args.get('sort')
    published_articles = article_service.list_published_articles(category, sort)
    category_options = article_service.get_all_categories()
    sort_options = article_service.get_sort_options()
    return render_template('published_articles.html',
                           published_articles=published_articles,
                           category_options=category_options,
                           sort_options=sort_options)

# Route: GET /calendar - content calendar display with calendar data and view options
@app.route('/calendar')
@login_required
def content_calendar():
    current_user = session['user']
    calendar_data, view_options = article_service.get_content_calendar(current_user)
    return render_template('content_calendar.html',
                           calendar_data=calendar_data,
                           view_options=view_options)

# Route: GET /article/<article_id>/analytics - article performance analytics overview
@app.route('/article/<int:article_id>/analytics')
@login_required
def article_analytics(article_id):
    current_user = session['user']
    if not approval_service.can_view_article(current_user, article_id):
        abort(403)
    analytics_overview = analytics_service.get_overview(article_id)
    total_views = analytics_service.get_total_views(article_id)
    unique_visitors = analytics_service.get_unique_visitors(article_id)
    return render_template('article_analytics.html',
                           analytics_overview=analytics_overview,
                           total_views=total_views,
                           unique_visitors=unique_visitors)

# Route: GET, POST /article/<article_id>/versions/<version_id>/comments - manage comments on article versions
@app.route('/article/<int:article_id>/versions/<int:version_id>/comments', methods=['GET', 'POST'])
@login_required
def comments_manage(article_id, version_id):
    current_user = session['user']
    if request.method == 'POST':
        comment_text = request.form.get('comment')
        if comment_text:
            comment_service.add_comment(article_id, version_id, current_user, comment_text)
            flash('Comment added.', 'success')
        else:
            flash('Comment text is required.', 'error')
    comments = comment_service.get_comments(article_id, version_id)
    return render_template('comments.html',
                           article_id=article_id,
                           version_id=version_id,
                           comments=comments)

# Route: POST /article/<article_id>/approve - handles the approval workflow for article versions
@app.route('/article/<int:article_id>/approve', methods=['POST'])
@login_required
def approve_article(article_id):
    current_user = session['user']
    version_id = request.form.get('version_id')
    if not version_id:
        abort(400)
    success, message = approval_service.process_approval(article_id, int(version_id), current_user)
    if success:
        flash('Approval recorded.', 'success')
    else:
        flash(f'Approval failed: {message}', 'error')
    return redirect(url_for('article_version_history', article_id=article_id))

# Route: GET / - Redirects root to dashboard
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

# Route: GET, POST /login - user login management for session
@app.route('/login', methods=['GET', 'POST'])
def login():
    errors = {}
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if user_service.authenticate(username, password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            errors['login'] = 'Invalid username or password'
    return render_template('login.html', errors=errors)

# Route: GET /logout - clears session and logs out user
@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))

# HTTP error handlers to render appropriate error templates
@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
