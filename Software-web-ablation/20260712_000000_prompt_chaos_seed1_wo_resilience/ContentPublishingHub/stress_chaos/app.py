from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

# In-memory data stores
articles = {}
article_versions = {}
article_id_counter = 1

calendar_events = []  # Each event {'id': int, 'title': str, 'date': str}

user_analytics = {
    'views': 0,
    'edits': 0,
    'publish_count': 0
}

# Dashboard data (for simplicity)
def get_dashboard_data():
    return {
        'total_articles': len(articles),
        'published_articles': len([a for a in articles.values() if a.get('published', False)]),
        'scheduled_events': len(calendar_events),
        'user_analytics': user_analytics
    }

@app.route('/')
@app.route('/dashboard')
def dashboard():
    data = get_dashboard_data()
    return render_template('dashboard.html', data=data)

@app.route('/content_calendar')
def content_calendar():
    return render_template('content_calendar.html', calendar_events=calendar_events)

@app.route('/create_article', methods=['GET', 'POST'])
def create_article():
    global article_id_counter
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if not title or not content:
            # Ideally flash message or error handling here
            return render_template('create_article.html', error='Title and content are required')
        article_id = article_id_counter
        article_id_counter += 1
        articles[article_id] = {
            'id': article_id,
            'title': title,
            'content': content,
            'summary': content[:100] + '...' if len(content) > 100 else content,
            'published': False,
            'versions': []
        }
        # Save initial version
        articles[article_id]['versions'].append({'title': title, 'content': content})
        return redirect(url_for('published_articles'))
    return render_template('create_article.html')

@app.route('/edit_article/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    article = articles.get(article_id)
    if not article:
        abort(404)
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if not title or not content:
            return render_template('edit_article.html', article=article, error='Title and content are required')
        article['title'] = title
        article['content'] = content
        article['summary'] = content[:100] + '...' if len(content) > 100 else content
        # Add version
        article['versions'].append({'title': title, 'content': content})
        user_analytics['edits'] += 1
        return redirect(url_for('published_articles'))
    return render_template('edit_article.html', article=article)

@app.route('/published_articles')
def published_articles():
    # Filter to only published articles
    published = [a for a in articles.values() if a.get('published', False)]
    return render_template('published_articles.html', articles=published)

@app.route('/view_article/<int:article_id>')
def view_article(article_id):
    article = articles.get(article_id)
    if not article:
        abort(404)
    user_analytics['views'] += 1
    return render_template('view_article.html', article=article)

# Additional route to publish an article (for simplicity)
@app.route('/publish_article/<int:article_id>', methods=['POST'])
def publish_article(article_id):
    article = articles.get(article_id)
    if not article:
        abort(404)
    article['published'] = True
    user_analytics['publish_count'] += 1
    # Add calendar event for publish date (simulated here as today's date string)
    from datetime import datetime
    publish_date = datetime.now().strftime('%Y-%m-%d')
    calendar_events.append({'id': len(calendar_events) + 1, 'title': article['title'], 'date': publish_date})
    return redirect(url_for('published_articles'))

# User analytics page
@app.route('/user_analytics')
def user_analytics_view():
    return render_template('user_analytics.html', analytics=user_analytics)

if __name__ == '__main__':
    app.run(debug=True)
