from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load and save data

def load_articles():
    articles = []
    path = os.path.join(DATA_DIR, 'articles.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                article_id, title, author, category, content, date, views = parts
                articles.append({
                    'article_id': int(article_id),
                    'title': title,
                    'author': author,
                    'category': category,
                    'content': content,
                    'date': date,
                    'views': int(views)
                })
    except FileNotFoundError:
        pass
    return articles


def load_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                category_id, category_name, description = parts
                categories.append(category_name)
    except FileNotFoundError:
        pass
    return categories


def load_bookmarks():
    bookmarks = []
    path = os.path.join(DATA_DIR, 'bookmarks.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 4:
                    continue
                bookmark_id, article_id, article_title, bookmarked_date = parts
                bookmarks.append({
                    'bookmark_id': int(bookmark_id),
                    'article_id': int(article_id),
                    'article_title': article_title,
                    'bookmarked_date': bookmarked_date
                })
    except FileNotFoundError:
        pass
    return bookmarks


def save_bookmarks(bookmarks):
    path = os.path.join(DATA_DIR, 'bookmarks.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for bm in bookmarks:
            line = f"{bm['bookmark_id']}|{bm['article_id']}|{bm['article_title']}|{bm['bookmarked_date']}"
            f.write(line + '\n')


def load_comments():
    comments = []
    path = os.path.join(DATA_DIR, 'comments.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                comment_id, article_id, article_title, commenter_name, comment_text, comment_date = parts
                comments.append({
                    'comment_id': int(comment_id),
                    'article_id': int(article_id),
                    'article_title': article_title,
                    'commenter_name': commenter_name,
                    'comment_text': comment_text,
                    'comment_date': comment_date
                })
    except FileNotFoundError:
        pass
    return comments


def save_comments(comments):
    path = os.path.join(DATA_DIR, 'comments.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for cm in comments:
            line = f"{cm['comment_id']}|{cm['article_id']}|{cm['article_title']}|{cm['commenter_name']}|{cm['comment_text']}|{cm['comment_date']}"
            f.write(line + '\n')


def load_trending():
    trending = []
    path = os.path.join(DATA_DIR, 'trending.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                article_id, article_title, category, view_count, period = parts
                trending.append({
                    'article_id': int(article_id),
                    'article_title': article_title,
                    'category': category,
                    'view_count': int(view_count),
                    'period': period
                })
    except FileNotFoundError:
        pass
    return trending


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    articles = load_articles()
    # featured_articles: list of dict with keys: article_id, title, author, date
    featured_articles = [
        {'article_id': a['article_id'], 'title': a['title'], 'author': a['author'], 'date': a['date']}
        for a in articles
    ]
    return render_template('dashboard.html', featured_articles=featured_articles)


@app.route('/catalog', methods=['GET', 'POST'])
def article_catalog():
    articles = load_articles()
    categories = load_categories()

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip().lower()
        category_filter = request.form.get('category_filter', '').strip()

        filtered_articles = articles

        if search_query:
            filtered_articles = [a for a in filtered_articles if
                                 search_query in a['title'].lower() or
                                 search_query in a['author'].lower() or
                                 search_query in a['content'].lower()]
        if category_filter:
            filtered_articles = [a for a in filtered_articles if a['category'] == category_filter]

        context = {
            'articles': [
                {'article_id': a['article_id'], 'title': a['title'], 'author': a['author'], 'category': a['category'], 'date': a['date']}
                for a in filtered_articles
            ],
            'categories': categories,
            'search_query': search_query,
            'category_filter': category_filter
        }

        return render_template('article_catalog.html', **context)

    else:
        # GET request
        context = {
            'articles': [
                {'article_id': a['article_id'], 'title': a['title'], 'author': a['author'], 'category': a['category'], 'date': a['date']}
                for a in articles
            ],
            'categories': categories
        }
        return render_template('article_catalog.html', **context)


@app.route('/article/<int:article_id>')
def article_details(article_id):
    articles = load_articles()
    bookmarks = load_bookmarks()

    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404

    is_bookmarked = any(b['article_id'] == article_id for b in bookmarks)

    context = {
        'article': {
            'article_id': article['article_id'],
            'title': article['title'],
            'author': article['author'],
            'date': article['date'],
            'content': article['content']
        },
        'is_bookmarked': is_bookmarked
    }

    return render_template('article_details.html', **context)


@app.route('/bookmark', methods=['POST'])
def add_bookmark():
    article_id = request.form.get('article_id', type=int)
    if article_id is None:
        return redirect(url_for('bookmarks'))

    articles = load_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return redirect(url_for('bookmarks'))

    bookmarks = load_bookmarks()
    # Prevent duplicate bookmark for same article
    if any(b['article_id'] == article_id for b in bookmarks):
        return redirect(url_for('bookmarks'))

    new_id = max([b['bookmark_id'] for b in bookmarks], default=0) + 1
    bookmarked_date = datetime.now().strftime('%Y-%m-%d')

    bookmarks.append({
        'bookmark_id': new_id,
        'article_id': article_id,
        'article_title': article['title'],
        'bookmarked_date': bookmarked_date
    })

    save_bookmarks(bookmarks)

    return redirect(url_for('bookmarks'))


@app.route('/bookmarks')
def bookmarks():
    bookmarks = load_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)


@app.route('/bookmark/remove/<int:id>', methods=['POST'])
def remove_bookmark(id):
    bookmark_id = id
    bookmarks = load_bookmarks()
    bookmarks = [b for b in bookmarks if b['bookmark_id'] != bookmark_id]
    save_bookmarks(bookmarks)
    return redirect(url_for('bookmarks'))


@app.route('/comments')
def comments():
    comments = load_comments()
    articles = load_articles()
    articles_simple = [{'article_id': a['article_id'], 'title': a['title']} for a in articles]
    return render_template('comments.html', comments=comments, articles=articles_simple)


@app.route('/comment/write', methods=['GET'])
def write_comment():
    articles = load_articles()
    articles_simple = [{'article_id': a['article_id'], 'title': a['title']} for a in articles]
    return render_template('write_comment.html', articles=articles_simple)


@app.route('/comment/write', methods=['POST'])
def submit_comment():
    article_id = request.form.get('article_id', type=int)
    commenter_name = request.form.get('commenter_name', '').strip()
    comment_text = request.form.get('comment_text', '').strip()

    if not article_id or not commenter_name or not comment_text:
        return redirect(url_for('write_comment'))

    articles = load_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return redirect(url_for('write_comment'))

    comments = load_comments()
    new_id = max([c['comment_id'] for c in comments], default=0) + 1
    comment_date = datetime.now().strftime('%Y-%m-%d')

    comments.append({
        'comment_id': new_id,
        'article_id': article_id,
        'article_title': article['title'],
        'commenter_name': commenter_name,
        'comment_text': comment_text,
        'comment_date': comment_date
    })

    save_comments(comments)

    return redirect(url_for('comments'))


@app.route('/trending')
def trending_articles():
    trending = load_trending()
    return render_template('trending.html', trending_articles=trending)


@app.route('/category/<category_name>', methods=['GET', 'POST'])
def category_articles(category_name):
    articles = load_articles()
    filtered = [
        {'article_id': a['article_id'], 'title': a['title'], 'date': a['date'], 'popularity': a['views']}
        for a in articles if a['category'] == category_name
    ]

    if request.method == 'POST':
        sort_by = request.form.get('sort_by', '')
        if sort_by == 'date':
            filtered.sort(key=lambda x: x['date'], reverse=True)
        elif sort_by == 'popularity':
            filtered.sort(key=lambda x: x['popularity'], reverse=True)

    return render_template('category.html', category_name=category_name, articles=filtered)


@app.route('/search', methods=['GET', 'POST'])
def search_results():
    articles = load_articles()
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        query = search_query
    else:
        query = request.args.get('query', '').strip()

    results = []
    if query:
        qlower = query.lower()
        for a in articles:
            # Fix: search in title and content case-insensitive (already lowered)
            # Also search in author to be consistent with catalog search
            if (qlower in a['title'].lower() or qlower in a['content'].lower() or qlower in a['author'].lower()):
                excerpt = a['content'][:150] + ('...' if len(a['content']) > 150 else '')
                results.append({
                    'article_id': a['article_id'],
                    'title': a['title'],
                    'excerpt': excerpt
                })

    return render_template('search_results.html', query=query, results=results)


if __name__ == '__main__':
    app.run(debug=True)
