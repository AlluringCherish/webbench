from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load data from files

def load_articles():
    articles = []
    path = os.path.join(DATA_DIR, 'articles.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    article = {
                        'article_id': int(parts[0]),
                        'title': parts[1],
                        'author': parts[2],
                        'category': parts[3],
                        'content': parts[4],
                        'date': parts[5],
                        'views': int(parts[6])
                    }
                    articles.append(article)
    except FileNotFoundError:
        pass
    return articles


def load_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    category = {
                        'category_id': int(parts[0]),
                        'category_name': parts[1],
                        'description': parts[2]
                    }
                    categories.append(category)
    except FileNotFoundError:
        pass
    return categories


def load_bookmarks():
    bookmarks = []
    path = os.path.join(DATA_DIR, 'bookmarks.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    bookmark = {
                        'bookmark_id': int(parts[0]),
                        'article_id': int(parts[1]),
                        'article_title': parts[2],
                        'bookmarked_date': parts[3]
                    }
                    bookmarks.append(bookmark)
    except FileNotFoundError:
        pass
    return bookmarks


def load_comments():
    comments = []
    path = os.path.join(DATA_DIR, 'comments.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    comment = {
                        'comment_id': int(parts[0]),
                        'article_id': int(parts[1]),
                        'article_title': parts[2],
                        'commenter_name': parts[3],
                        'comment_text': parts[4],
                        'comment_date': parts[5]
                    }
                    comments.append(comment)
    except FileNotFoundError:
        pass
    return comments


def load_trending():
    trending = []
    path = os.path.join(DATA_DIR, 'trending.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    t = {
                        'article_id': int(parts[0]),
                        'title': parts[1],
                        'category': parts[2],
                        'view_count': int(parts[3]),
                        'period': parts[4]
                    }
                    trending.append(t)
    except FileNotFoundError:
        pass
    return trending


# Helper to write data to files

def save_bookmarks(bookmarks):
    path = os.path.join(DATA_DIR, 'bookmarks.txt')
    lines = []
    for b in bookmarks:
        line = f"{b['bookmark_id']}|{b['article_id']}|{b['article_title']}|{b['bookmarked_date']}"
        lines.append(line)
    content = '\n'.join(lines)
    from functions import write_text_file
    write_text_file(filename=path, content=content)


def save_comments(comments):
    path = os.path.join(DATA_DIR, 'comments.txt')
    lines = []
    for c in comments:
        line = f"{c['comment_id']}|{c['article_id']}|{c['article_title']}|{c['commenter_name']}|{c['comment_text']}|{c['comment_date']}"
        lines.append(line)
    content = '\n'.join(lines)
    from functions import write_text_file
    write_text_file(filename=path, content=content)


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    articles = load_articles()
    trending = load_trending()

    # featured_articles: list of dicts (article_id:int, title:str, summary:str)
    # We will use summary as first 100 chars of content
    featured_articles = []
    for a in articles[:5]:
        featured_articles.append({
            'article_id': a['article_id'],
            'title': a['title'],
            'summary': a['content'][:100] + ('...' if len(a['content']) > 100 else '')
        })

    # trending_articles: list of dicts (article_id:int, title:str, category:str, view_count:int)
    trending_articles = []
    for t in trending[:5]:
        trending_articles.append({
            'article_id': t['article_id'],
            'title': t['title'],
            'category': t['category'],
            'view_count': t['view_count']
        })

    return render_template('dashboard.html', featured_articles=featured_articles, trending_articles=trending_articles)


@app.route('/catalog')
def article_catalog():
    articles_data = load_articles()
    categories_data = load_categories()

    articles = []
    for a in articles_data:
        articles.append({
            'article_id': a['article_id'],
            'title': a['title'],
            'author': a['author'],
            'category': a['category'],
            'date': a['date'],
        })

    categories = []
    for c in categories_data:
        categories.append({
            'category_id': c['category_id'],
            'category_name': c['category_name']
        })

    return render_template('catalog.html', articles=articles, categories=categories)


@app.route('/catalog/search', methods=['POST'])
def catalog_search_results():
    search_query = request.form.get('search_query', '').strip()
    results = []
    if search_query:
        articles = load_articles()
        lowered_query = search_query.lower()
        for a in articles:
            if lowered_query in a['title'].lower() or lowered_query in a['content'].lower():
                excerpt_limit = 100
                content_lower = a['content'].lower()
                pos = content_lower.find(lowered_query)
                if pos == -1:
                    pos = 0
                start = max(0, pos - 20)
                end = min(len(a['content']), pos + len(search_query) + 20)
                excerpt = a['content'][start:end]
                if start > 0:
                    excerpt = '...' + excerpt
                if end < len(a['content']):
                    excerpt = excerpt + '...'
                results.append({
                    'article_id': a['article_id'],
                    'title': a['title'],
                    'excerpt': excerpt
                })
    return render_template('search_results.html', query=search_query, results=results)


@app.route('/catalog/category/<string:category_name>')
def category_page(category_name):
    articles = load_articles()
    category_articles = []
    for a in articles:
        if a['category'].lower() == category_name.lower():
            category_articles.append({
                'article_id': a['article_id'],
                'title': a['title'],
                'date': a['date'],
                'popularity': a['views']
            })

    return render_template('category.html', category_name=category_name, category_articles=category_articles)


@app.route('/article/<int:article_id>')
def article_details(article_id):
    articles = load_articles()
    article = None
    for a in articles:
        if a['article_id'] == article_id:
            article = {  # Matches context variables exactly
                'article_id': a['article_id'],
                'title': a['title'],
                'author': a['author'],
                'date': a['date'],
                'content': a['content'],
            }
            break
    return render_template('article_details.html', article=article)


@app.route('/article/<int:article_id>/bookmark', methods=['POST'])
def bookmark_article(article_id):
    articles = load_articles()
    article = None
    for a in articles:
        if a['article_id'] == article_id:
            article = a
            break
    if article is None:
        # Article not found, redirect back to article details
        return redirect(url_for('article_details', article_id=article_id))

    bookmarks = load_bookmarks()
    # Check if article already bookmarked
    for bm in bookmarks:
        if bm['article_id'] == article_id:
            return redirect(url_for('article_details', article_id=article_id))

    # Generate new bookmark id
    max_id = max([bm['bookmark_id'] for bm in bookmarks], default=0)
    new_id = max_id + 1
    today_str = datetime.today().strftime('%Y-%m-%d')
    new_bm = {
        'bookmark_id': new_id,
        'article_id': article_id,
        'article_title': article['title'],
        'bookmarked_date': today_str
    }
    bookmarks.append(new_bm)

    # Save bookmarks
    save_bookmarks(bookmarks)

    return redirect(url_for('article_details', article_id=article_id))


@app.route('/bookmarks')
def bookmarks_page():
    bookmarks = load_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)


@app.route('/bookmarks/remove/<int:bookmark_id>', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = load_bookmarks()
    bookmarks = [b for b in bookmarks if b['bookmark_id'] != bookmark_id]
    save_bookmarks(bookmarks)
    return redirect(url_for('bookmarks_page'))


@app.route('/comments')
def comments_page():
    comments = load_comments()
    articles_raw = load_articles()
    articles = []
    for a in articles_raw:
        articles.append({'article_id': a['article_id'], 'title': a['title']})

    return render_template('comments.html', comments=comments, articles=articles)


@app.route('/comments/write')
def write_comment_page():
    articles_raw = load_articles()
    articles = []
    for a in articles_raw:
        articles.append({'article_id': a['article_id'], 'title': a['title']})
    return render_template('write_comment.html', articles=articles)


@app.route('/comments/submit', methods=['POST'])
def submit_comment():
    article_id = request.form.get('article_id', type=int)
    commenter_name = request.form.get('commenter_name', '').strip()
    comment_text = request.form.get('comment_text', '').strip()

    if not article_id or not commenter_name or not comment_text:
        # Invalid data, redirect to write comment page
        return redirect(url_for('write_comment_page'))

    articles = load_articles()
    article_title = None
    for a in articles:
        if a['article_id'] == article_id:
            article_title = a['title']
            break

    if article_title is None:
        return redirect(url_for('write_comment_page'))

    comments = load_comments()
    max_id = max([c['comment_id'] for c in comments], default=0)
    new_id = max_id + 1
    today_str = datetime.today().strftime('%Y-%m-%d')
    new_comment = {
        'comment_id': new_id,
        'article_id': article_id,
        'article_title': article_title,
        'commenter_name': commenter_name,
        'comment_text': comment_text,
        'comment_date': today_str
    }
    comments.append(new_comment)
    save_comments(comments)

    return redirect(url_for('comments_page'))


@app.route('/trending')
def trending_articles_page():
    trending = load_trending()
    return render_template('trending.html', trending=trending)


@app.route('/trending/filter', methods=['POST'])
def filter_trending_by_period():
    time_period = request.form.get('time_period', '')
    trending = load_trending()
    trending_filtered = [t for t in trending if t['period'] == time_period]
    return render_template('trending.html', trending_filtered=trending_filtered)


@app.route('/search')
def search_results_page():
    query = request.args.get('query', '').strip()
    results = []
    if query:
        articles = load_articles()
        lowered_query = query.lower()
        for a in articles:
            if lowered_query in a['title'].lower() or lowered_query in a['content'].lower():
                excerpt_limit = 100
                content_lower = a['content'].lower()
                pos = content_lower.find(lowered_query)
                if pos == -1:
                    pos = 0
                start = max(0, pos - 20)
                end = min(len(a['content']), pos + len(query) + 20)
                excerpt = a['content'][start:end]
                if start > 0:
                    excerpt = '...' + excerpt
                if end < len(a['content']):
                    excerpt = excerpt + '...'
                results.append({
                    'article_id': a['article_id'],
                    'title': a['title'],
                    'excerpt': excerpt
                })

    return render_template('search_results.html', query=query, results=results)


if __name__ == '__main__':
    app.run(debug=True)
