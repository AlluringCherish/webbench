from flask import Flask, request, render_template, redirect, url_for, session
from services.article_service import ArticleService
from services.approval_service import ApprovalService
from services.analytics_service import AnalyticsService
from data_access.data_access import DataAccess
import version_control.version_manager as VersionManager

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # For session handling

# Initialize services
article_service = ArticleService()
approval_service = ApprovalService()
analytics_service = AnalyticsService()
data_access = DataAccess()

# Helper function for user login simulation
@app.before_request
def load_user():
    # For example, let\'s say user_id is stored in session
    session['user_id'] = session.get('user_id', None)


@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id') or 'anonymous'
    username = user_id  # Simplified for demo; adjust as needed
    recent_articles = article_service.get_recent_articles(user_id)
    return render_template('dashboard.html', username=username, recent_articles=recent_articles)


@app.route('/article/new', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        data = request.form
        user_id = session.get('user_id') or 'anonymous'
        title = data.get('title')
        content = data.get('content')
        if not title or not content:
            return render_template('create_article.html', error='Title and content are required.')
        article_id = article_service.create_article(title=title, content=content, author=user_id)
        return redirect(url_for('view_article', article_id=article_id))
    return render_template('create_article.html')


@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    user_id = session.get('user_id') or 'anonymous'
    article = article_service.get_article(article_id)
    if not article:
        return 'Article not found', 404

    if request.method == 'POST':
        data = request.form
        new_content = data.get('content')
        summary = data.get('summary')  # summary expected in POST
        if not new_content or not summary:
            return render_template('edit_article.html', article=article, error='Content and summary required.')
        version_id = article_service.add_version(article_id, content=new_content, summary=summary, author=user_id)
        return redirect(url_for('view_article', article_id=article_id))

    return render_template('edit_article.html', article=article)


@app.route('/article/<int:article_id>/versions', methods=['GET'])
def article_versions(article_id):
    versions = article_service.get_versions(article_id)
    article = article_service.get_article(article_id)
    if not article:
        return 'Article not found', 404
    return render_template('versions.html', versions=versions, article=article)


@app.route('/article/<int:article_id>/versions/<int:version_id>/approve', methods=['POST'])
def approve_version(article_id, version_id):
    user_id = session.get('user_id') or 'anonymous'
    approval_status = request.form.get('status')
    comment = request.form.get('comment')
    if approval_status not in ['approved', 'rejected']:
        return 'Invalid approval status', 400
    approval_service.record_approval(article_id, version_id, approver=user_id, status=approval_status, comment=comment)
    return redirect(url_for('article_versions', article_id=article_id))


@app.route('/articles/mine', methods=['GET'])
def my_articles():
    user_id = session.get('user_id') or 'anonymous'
    articles = article_service.get_articles_by_author(user_id)
    return render_template('articles.html', articles=articles, categories=[], selected_category=None, sort=None)


@app.route('/articles/published', methods=['GET'])
def published_articles():
    articles = article_service.get_published_articles()
    return render_template('articles.html', articles=articles, categories=[], selected_category=None, sort=None)


@app.route('/calendar', methods=['GET'])
def calendar_view():
    events = article_service.get_calendar_events()
    return render_template('calendar.html', events=events)


@app.route('/article/<int:article_id>/analytics', methods=['GET'])
def article_analytics(article_id):
    analytics_data = analytics_service.get_analytics(article_id)
    article = article_service.get_article(article_id)
    if not article:
        return 'Article not found', 404
    return render_template('analytics.html', analytics_data=analytics_data, article=article)


@app.route('/article/<int:article_id>', methods=['GET'])
def view_article(article_id):
    article = article_service.get_article(article_id)
    if not article:
        return 'Article not found', 404
    return render_template('view_article.html', article=article)


if __name__ == '__main__':
    app.run(debug=True)
