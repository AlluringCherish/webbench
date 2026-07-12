from flask import Flask, render_template, request, redirect, url_for, abort
from datetime import datetime

app = Flask(__name__)

# Data structures to simulate database
articles = {}
article_versions = {}
article_analytics_data = {}

# Auto-increment IDs
next_article_id = 1

# Predefined statuses and categories
STATUSES = ['draft', 'under_review', 'approved', 'rejected', 'published', 'archived']
CATEGORIES = ['Technology', 'Science', 'Lifestyle', 'Health', 'Finance', 'Uncategorized']

@app.route('/')
def root():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/create_article', methods=['GET', 'POST'])
def create_article():
    global next_article_id
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if not title or not content:
            abort(400, "Title and content are required.")
        article_id = next_article_id
        next_article_id += 1
        articles[article_id] = {
            'id': article_id,
            'title': title,
            'content': content,
            'status': 'draft',
            'category': 'Uncategorized',
            'last_modified': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'author': 'Current User',
            'published_date': None
        }
        article_versions[article_id] = [{
            'id': 1,
            'version_number': 1,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'stage': 'draft',
            'title': title,
            'content': content
        }]
        article_analytics_data[article_id] = {
            'views': 0,
            'unique_visitors': 0,
            'average_read_time': 0
        }
        return redirect(url_for('my_articles'))

    return render_template('create_article.html')

@app.route('/my_articles')
def my_articles():
    filter_status = request.args.get('filter_status', 'all')
    filter_category = request.args.get('filter_category', 'all')

    filtered = list(articles.values())
    if filter_status != 'all':
        filtered = [a for a in filtered if a['status'] == filter_status]
    if filter_category != 'all':
        filtered = [a for a in filtered if a['category'] == filter_category]

    return render_template('my_articles.html', articles=filtered, categories=CATEGORIES)

@app.route('/published_articles')
def published_articles():
    filter_status = request.args.get('filter_status', 'published')
    filter_category = request.args.get('filter_category', 'all')

    filtered = [a for a in articles.values() if a['status'] in ['published', 'archived']]
    if filter_status != 'all':
        filtered = [a for a in filtered if a['status'] == filter_status]
    if filter_category != 'all':
        filtered = [a for a in filtered if a['category'] == filter_category]

    return render_template('published_articles.html', articles=filtered, categories=CATEGORIES)

@app.route('/content_calendar')
def content_calendar():
    return render_template('content_calendar.html')

@app.route('/edit_article/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    article = articles.get(article_id)
    if not article:
        abort(404)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if not title or not content:
            abort(400, "Title and content are required.")
        article['title'] = title
        article['content'] = content
        article['last_modified'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        versions = article_versions.setdefault(article_id, [])
        version_num = len(versions) + 1
        versions.append({
            'id': version_num,
            'version_number': version_num,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'stage': article['status'],
            'title': title,
            'content': content
        })
        article_versions[article_id] = versions

        return redirect(url_for('my_articles'))

    return render_template('edit_article.html', article=article)

@app.route('/version_history/<int:article_id>')
def version_history(article_id):
    article = articles.get(article_id)
    if not article:
        abort(404)
    versions = article_versions.get(article_id, [])
    return render_template('version_history.html', article=article, versions=versions)

@app.route('/restore_version/<int:article_id>/<int:version_id>', methods=['POST'])
def restore_version(article_id, version_id):
    article = articles.get(article_id)
    if not article:
        abort(404)
    versions = article_versions.get(article_id, [])
    version_to_restore = None
    for v in versions:
        if v['id'] == version_id:
            version_to_restore = v
            break
    if not version_to_restore:
        abort(404)

    article['title'] = version_to_restore['title']
    article['content'] = version_to_restore['content']
    article['last_modified'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    version_num = len(versions) + 1
    versions.append({
        'id': version_num,
        'version_number': version_num,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'stage': article['status'],
        'title': article['title'],
        'content': article['content']
    })
    article_versions[article_id] = versions

    return redirect(url_for('edit_article', article_id=article_id))

@app.route('/article_analytics/<int:article_id>')
def article_analytics(article_id):
    article = articles.get(article_id)
    if not article:
        abort(404)

    analytics = article_analytics_data.get(article_id, {
        'views': 0,
        'unique_visitors': 0,
        'average_read_time': 0
    })

    return render_template('article_analytics.html', article=article, analytics=analytics)

if __name__ == '__main__':
    app.run(debug=True)
