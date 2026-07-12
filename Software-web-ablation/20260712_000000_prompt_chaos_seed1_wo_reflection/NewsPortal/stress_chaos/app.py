from flask import Flask, render_template, redirect, url_for, request, abort
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load and save data

def load_articles():
    articles = []
    path = os.path.join(DATA_DIR, 'articles.txt')
    if not os.path.exists(path):
        return articles
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            try:
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
            except:
                continue
    return articles

def load_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    if not os.path.exists(path):
        return categories
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            try:
                category = {
                    'category_id': int(parts[0]),
                    'category_name': parts[1],
                    'description': parts[2]
                }
                categories.append(category)
            except:
                continue
    return categories


def load_bookmarks():
    bookmarks = []
    path = os.path.join(DATA_DIR, 'bookmarks.txt')
    if not os.path.exists(path):
        return bookmarks
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 4:
                continue
            try:
                bookmark = {
                    'bookmark_id': int(parts[0]),
                    'article_id': int(parts[1]),
                    'article_title': parts[2],
                    'bookmarked_date': parts[3]
                }
                bookmarks.append(bookmark)
            except:
                continue
    return bookmarks


def save_bookmarks(bookmarks):
    path = os.path.join(DATA_DIR, 'bookmarks.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in bookmarks:
            line = f"{b['bookmark_id']}|{b['article_id']}|{b['article_title']}|{b['bookmarked_date']}\n"
            f.write(line)

def load_comments():
    comments = []
    path = os.path.join(DATA_DIR, 'comments.txt')
    if not os.path.exists(path):
        return comments
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            try:
                comment = {
                    'comment_id': int(parts[0]),
                    'article_id': int(parts[1]),
                    'article_title': parts[2],
                    'commenter_name': parts[3],
                    'comment_text': parts[4],
                    'comment_date': parts[5]
                }
                comments.append(comment)
            except:
                continue
    return comments

def save_comments(comments):
    path = os.path.join(DATA_DIR, 'comments.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for c in comments:
            line = f"{c['comment_id']}|{c['article_id']}|{c['article_title']}|{c['commenter_name']}|{c['comment_text']}|{c['comment_date']}\n"
            f.write(line)


def load_trending():
    trending = []
    path = os.path.join(DATA_DIR, 'trending.txt')
    if not os.path.exists(path):
        return trending
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            try:
                item = {
                    'article_id': int(parts[0]),
                    'article_title': parts[1],
                    'category': parts[2],
                    'view_count': int(parts[3]),
                    'period': parts[4]
                }
                trending.append(item)
            except:
                continue
    return trending


# Route: /
def root_redirect():
    return redirect(url_for('dashboard'))

app.add_url_rule('/', 'root_redirect', root_redirect, methods=['GET'])


# Route: /dashboard
@app.route('/dashboard', methods=['GET'])
def dashboard():
    articles = load_articles()
    # featured_articles are article_id, title, author, date
    featured_articles = []
    # Let's assume featured are top 5 by views descending
    sorted_articles = sorted(articles, key=lambda a: a['views'], reverse=True)
    for a in sorted_articles[:5]:
        featured_articles.append({
            'article_id': a['article_id'],
            'title': a['title'],
            'author': a['author'],
            'date': a['date']
        })
    trending_articles_button_url = url_for('trending_articles')
    browse_articles_url = url_for('article_catalog')
    view_bookmarks_url = url_for('bookmarks')
    trending_articles_url = url_for('trending_articles')
    return render_template('dashboard.html', featured_articles=featured_articles, trending_articles_button_url=trending_articles_button_url, browse_articles_url=browse_articles_url, view_bookmarks_url=view_bookmarks_url, trending_articles_url=trending_articles_url)


# Route: /catalog
@app.route('/catalog', methods=['GET'])
def article_catalog():
    articles_raw = load_articles()
    categories = load_categories()
    # articles: article_id:int, title:str, author:str, date:str, category:str
    articles = []
    for a in articles_raw:
        articles.append({
            'article_id': a['article_id'],
            'title': a['title'],
            'author': a['author'],
            'date': a['date'],
            'category': a['category']
        })
    return render_template('catalog.html', articles=articles, categories=categories)


# Route: /article/<int:article_id>
@app.route('/article/<int:article_id>', methods=['GET'])
def article_details(article_id):
    articles = load_articles()
    article = None
    for a in articles:
        if a['article_id'] == article_id:
            article = a
            break
    if article is None:
        abort(404)
    return render_template('article_details.html', article=article)


# Route: /article/<int:article_id>/bookmark (POST)
@app.route('/article/<int:article_id>/bookmark', methods=['POST'])
def bookmark_article(article_id):
    articles = load_articles()
    article = None
    for a in articles:
        if a['article_id'] == article_id:
            article = a
            break
    if article is None:
        abort(404)

    bookmarks = load_bookmarks()
    # Check if already bookmarked
    for b in bookmarks:
        if b['article_id'] == article_id:
            # Already bookmarked
            return redirect(url_for('article_details', article_id=article_id))

    new_id = 1
    if bookmarks:
        new_id = max(b['bookmark_id'] for b in bookmarks) + 1
    bookmarked_date = datetime.now().strftime('%Y-%m-%d')
    new_bm = {
        'bookmark_id': new_id,
        'article_id': article['article_id'],
        'article_title': article['title'],
        'bookmarked_date': bookmarked_date
    }
    bookmarks.append(new_bm)
    save_bookmarks(bookmarks)
    return redirect(url_for('article_details', article_id=article_id))


# Route: /bookmarks
@app.route('/bookmarks', methods=['GET'])
def bookmarks():
    bookmarks = load_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)


# Route: /bookmarks/<int:bookmark_id>/remove (POST)
@app.route('/bookmarks/<int:bookmark_id>/remove', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = load_bookmarks()
    new_bookmarks = [b for b in bookmarks if b['bookmark_id'] != bookmark_id]
    if len(new_bookmarks) == len(bookmarks):
        # bookmark_id not found
        abort(404)
    save_bookmarks(new_bookmarks)
    return redirect(url_for('bookmarks'))


# Route: /comments
@app.route('/comments', methods=['GET'])
def comments_page():
    comments = load_comments()
    articles_raw = load_articles()
    # Prepare articles list with article_id, title
    articles = []
    for a in articles_raw:
        articles.append({'article_id': a['article_id'], 'title': a['title']})
    return render_template('comments.html', comments=comments, articles=articles)


# Route: /write-comment (GET)
@app.route('/write-comment', methods=['GET'])
def write_comment():
    articles_raw = load_articles()
    articles = []
    for a in articles_raw:
        articles.append({'article_id': a['article_id'], 'title': a['title']})
    return render_template('write_comment.html', articles=articles)


# Route: /write-comment (POST)
@app.route('/write-comment', methods=['POST'])
def submit_comment():
    try:
        selected_article_id = int(request.form.get('select_article', 0))
        commenter_name = request.form.get('commenter_name', '').strip()
        comment_text = request.form.get('comment_text', '').strip()
    except:
        return redirect(url_for('write_comment'))

    articles = load_articles()
    article_title = None
    for a in articles:
        if a['article_id'] == selected_article_id:
            article_title = a['title']
            break
    if article_title is None or not commenter_name or not comment_text:
        # Missing data or invalid article
        return redirect(url_for('write_comment'))

    comments = load_comments()
    new_id = 1
    if comments:
        new_id = max(c['comment_id'] for c in comments) + 1
    comment_date = datetime.now().strftime('%Y-%m-%d')
    new_comment = {
        'comment_id': new_id,
        'article_id': selected_article_id,
        'article_title': article_title,
        'commenter_name': commenter_name,
        'comment_text': comment_text,
        'comment_date': comment_date
    }
    comments.append(new_comment)
    save_comments(comments)
    return redirect(url_for('comments_page'))


# Route: /trending
@app.route('/trending', methods=['GET'])
def trending_articles():
    trending = load_trending()
    period = request.args.get('period', '')
    # Filter trending by period if provided
    filtered = []
    if period:
        for t in trending:
            if t['period'] == period:
                filtered.append(t)
    else:
        filtered = trending

    # Provide the period used in context
    time_period = period if period else 'All Time'
    return render_template('trending.html', trending_articles=filtered, time_period=time_period)


# Route: /category/<string:category_name>
@app.route('/category/<string:category_name>', methods=['GET'])
def category_articles(category_name):
    # Sorting param
    sort_by = request.args.get('sort', '')  # 'date' or 'popularity'
    articles = load_articles()
    filtered = []
    for a in articles:
        if a['category'].lower() == category_name.lower():
            filtered.append({
                'article_id': a['article_id'],
                'title': a['title'],
                'author': a['author'],
                'date': a['date'],
                'views': a['views']
            })

    # Sorting
    if sort_by == 'date':
        filtered.sort(key=lambda x: x['date'], reverse=True)
    elif sort_by == 'popularity':
        filtered.sort(key=lambda x: x['views'], reverse=True)

    return render_template('category.html', category_name=category_name, category_articles=filtered)


# Route: /search
@app.route('/search', methods=['GET'])
def search_results():
    q = request.args.get('q', '').strip()
    articles = load_articles()
    results = []
    if q:
        q_lower = q.lower()
        for a in articles:
            if q_lower in a['title'].lower() or q_lower in a['content'].lower():
                excerpt = a['content'][:150] + ('...' if len(a['content']) > 150 else '')
                results.append({
                    'article_id': a['article_id'],
                    'title': a['title'],
                    'excerpt': excerpt
                })
    return render_template('search_results.html', search_query=q, search_results=results)


if __name__ == '__main__':
    app.run(debug=True)
