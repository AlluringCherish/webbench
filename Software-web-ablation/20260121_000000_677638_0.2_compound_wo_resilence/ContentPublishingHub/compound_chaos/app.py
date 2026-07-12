from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory data storage for demonstration purposes
articles = {}
# Example structure:
# articles = {
#     'article_id': {
#         'title': 'Title',
#         'content': 'Content',
#         'versions': [{'version_id': 'v1', 'content': 'Content v1', 'created_at': datetime}, ...],
#         'status': 'draft'/'approved'/'published',
#         'scheduled_time': None or datetime,
#         'created_at': datetime,
#         'updated_at': datetime
#     },
#     ...
# }

@app.route('/dashboard')
def dashboard():
    # Show summary overview
    total_articles = len(articles)
    drafts = sum(1 for a in articles.values() if a['status'] == 'draft')
    approved = sum(1 for a in articles.values() if a['status'] == 'approved')
    published = sum(1 for a in articles.values() if a['status'] == 'published')
    return render_template('dashboard.html', total=total_articles, drafts=drafts, approved=approved, published=published)

@app.route('/articles')
def list_articles():
    # List all articles
    return render_template('articles.html', articles=articles)

@app.route('/articles/new', methods=['GET', 'POST'])
def new_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if not title or not content:
            return render_template('new_article.html', error='Title and content are required.')
        article_id = str(uuid.uuid4())
        now = datetime.utcnow()
        articles[article_id] = {
            'title': title,
            'content': content,
            'versions': [{'version_id': 'v1', 'content': content, 'created_at': now}],
            'status': 'draft',
            'scheduled_time': None,
            'created_at': now,
            'updated_at': now
        }
        return redirect(url_for('list_articles'))
    return render_template('new_article.html')

@app.route('/articles/<article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    article = articles.get(article_id)
    if not article:
        return 'Article not found', 404
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if not title or not content:
            return render_template('edit_article.html', article=article, article_id=article_id, error='Title and content are required.')
        article['title'] = title
        article['content'] = content
        # Add new version
        version_id = 'v' + str(len(article['versions']) + 1)
        article['versions'].append({'version_id': version_id, 'content': content, 'created_at': datetime.utcnow()})
        article['updated_at'] = datetime.utcnow()
        return redirect(url_for('list_articles'))
    return render_template('edit_article.html', article=article, article_id=article_id)

@app.route('/articles/<article_id>/approve', methods=['POST'])
def approve_article(article_id):
    article = articles.get(article_id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404
    article['status'] = 'approved'
    article['updated_at'] = datetime.utcnow()
    return jsonify({'status': 'approved'})

@app.route('/articles/<article_id>/publish', methods=['POST'])
def publish_article(article_id):
    article = articles.get(article_id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404
    if article['status'] != 'approved':
        return jsonify({'error': 'Article not approved'}), 400
    article['status'] = 'published'
    article['updated_at'] = datetime.utcnow()
    article['scheduled_time'] = None
    return jsonify({'status': 'published'})

@app.route('/articles/<article_id>/schedule', methods=['POST'])
def schedule_article(article_id):
    article = articles.get(article_id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404
    scheduled_time_str = request.form.get('scheduled_time')
    if not scheduled_time_str:
        return jsonify({'error': 'Scheduled time required'}), 400
    try:
        scheduled_time = datetime.strptime(scheduled_time_str, '%Y-%m-%dT%H:%M')
    except ValueError:
        return jsonify({'error': 'Invalid datetime format'}), 400
    article['scheduled_time'] = scheduled_time
    article['status'] = 'approved'
    article['updated_at'] = datetime.utcnow()
    return jsonify({'status': 'scheduled', 'scheduled_time': scheduled_time_str})

@app.route('/analytics')
def analytics():
    # Aggregate some statistics
    published_count = sum(1 for a in articles.values() if a['status'] == 'published')
    approved_count = sum(1 for a in articles.values() if a['status'] == 'approved')
    drafts_count = sum(1 for a in articles.values() if a['status'] == 'draft')
    return render_template('analytics.html', published=published_count, approved=approved_count, drafts=drafts_count)

if __name__ == '__main__':
    app.run(debug=True)
