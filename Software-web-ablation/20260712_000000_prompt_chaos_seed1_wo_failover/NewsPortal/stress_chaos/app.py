from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load/save data from text files

def load_articles():
    articles = []
    path = os.path.join(DATA_DIR, 'articles.txt')
    if not os.path.exists(path):
        return articles
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
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
    return articles


def load_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    if not os.path.exists(path):
        return categories
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 3:
                    category = {
                        'category_id': int(parts[0]),
                        'category_name': parts[1],
                        'description': parts[2]
                    }
                    categories.append(category)
    return categories


def load_bookmarks():
    bookmarks = []
    path = os.path.join(DATA_DIR, 'bookmarks.txt')
    if not os.path.exists(path):
        return bookmarks
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 4:
                    bookmark = {
                        'bookmark_id': int(parts[0]),
                        'article_id': int(parts[1]),
                        'article_title': parts[2],
                        'bookmarked_date': parts[3]
                    }
                    bookmarks.append(bookmark)
    return bookmarks


def save_bookmarks(bookmarks):
    path = os.path.join(DATA_DIR, 'bookmarks.txt')
    lines = []
    for b in bookmarks:
        line = f"{b['bookmark_id']}|{b['article_id']}|{b['article_title']}|{b['bookmarked_date']}"
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def load_comments():
    comments = []
    path = os.path.join(DATA_DIR, 'comments.txt')
    if not os.path.exists(path):
        return comments
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
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
    return comments


def save_comments(comments):
    path = os.path.join(DATA_DIR, 'comments.txt')
    lines = []
    for c in comments:
        line = f"{c['comment_id']}|{c['article_id']}|{c['article_title']}|{c['commenter_name']}|{c['comment_text']}|{c['comment_date']}"
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def load_trending():
    trending = []
    path = os.path.join(DATA_DIR, 'trending.txt')
    if not os.path.exists(path):
        return trending
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 5:
                    entry = {
                        'article_id': int(parts[0]),
                        'article_title': parts[1],
                        'category': parts[2],
                        'view_count': int(parts[3]),
                        'period': parts[4]
                    }
                    trending.append(entry)
    return trending


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    articles = load_articles()
    trending = load_trending()

    # featured_articles: list of dict with keys [article_id:int, title:str, author:str, date:str]
    # select first 5 articles as featured (or less if fewer available)
    featured_articles = [{'article_id': a['article_id'], 'title': a['title'], 'author': a['author'], 'date': a['date']} 
                         for a in articles[:5]]

    # trending_articles: list of dict with keys [article_id:int, title:str, category:str, view_count:int]
    # choose trending articles from trending.txt ignoring period for this page
    trending_articles = [{'article_id': t['article_id'], 'title': t['article_title'], 'category': t['category'], 'view_count': t['view_count']} for t in trending]

    return render_template('dashboard.html', featured_articles=featured_articles, trending_articles=trending_articles)


@app.route('/catalog')
def article_catalog_page():
    articles = load_articles()
    categories = load_categories()

    # articles context keys: article_id, title, author, category, date
    article_list = [{'article_id': a['article_id'], 'title': a['title'], 'author': a['author'], 'category': a['category'], 'date': a['date']} for a in articles]

    # categories context keys: category_id, category_name
    category_list = [{'category_id': c['category_id'], 'category_name': c['category_name']} for c in categories]

    return render_template('catalog.html', articles=article_list, categories=category_list)


@app.route('/article/<int:article_id>')
def article_details_page(article_id):
    articles = load_articles()
    article = None
    for a in articles:
        if a['article_id'] == article_id:
            article = a
            break

    if article is None:
        # Could optionally return 404 or redirect elsewhere, but not specified
        return redirect(url_for('article_catalog_page'))

    return render_template('article_details.html', article=article)


@app.route('/article/<int:article_id>/bookmark', methods=['POST'])
def bookmark_article(article_id):
    articles = load_articles()
    bookmarks = load_bookmarks()

    # Find article to bookmark
    article = None
    for a in articles:
        if a['article_id'] == article_id:
            article = a
            break

    if article is None:
        # Article not found, redirect back to catalog
        return redirect(url_for('article_catalog_page'))

    # Check if already bookmarked to avoid duplicates (not specified but reasonable)
    for b in bookmarks:
        if b['article_id'] == article_id:
            return redirect(url_for('article_details_page', article_id=article_id))

    # Assign new bookmark_id
    bookmark_id = 1
    if bookmarks:
        bookmark_id = max(b['bookmark_id'] for b in bookmarks) + 1

    bookmarked_date = datetime.now().strftime('%Y-%m-%d')
    new_bookmark = {
        'bookmark_id': bookmark_id,
        'article_id': article_id,
        'article_title': article['title'],
        'bookmarked_date': bookmarked_date
    }

    bookmarks.append(new_bookmark)
    save_bookmarks(bookmarks)

    return redirect(url_for('article_details_page', article_id=article_id))


@app.route('/bookmarks')
def bookmarks_page():
    bookmarks = load_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)


@app.route('/bookmark/<int:bookmark_id>/remove', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = load_bookmarks()
    bookmarks = [b for b in bookmarks if b['bookmark_id'] != bookmark_id]
    save_bookmarks(bookmarks)
    return redirect(url_for('bookmarks_page'))


@app.route('/comments')
def comments_page():
    comments = load_comments()
    articles = load_articles()
    # Enhance comments with article_title from articles to guarantee correctness
    article_dict = {a['article_id']: a['title'] for a in articles}
    for c in comments:
        if c['article_id'] in article_dict:
            c['article_title'] = article_dict[c['article_id']]

    # comments keys: comment_id:int, article_id:int, article_title:str, commenter_name:str, comment_text:str, comment_date:str
    # articles keys for context: article_id, title
    articles_context = [{'article_id': a['article_id'], 'title': a['title']} for a in articles]
    return render_template('comments.html', comments=comments, articles=articles_context)


@app.route('/comments/write')
def write_comment_page():
    articles = load_articles()
    articles_context = [{'article_id': a['article_id'], 'title': a['title']} for a in articles]
    return render_template('write_comment.html', articles=articles_context)


@app.route('/comments/submit', methods=['POST'])
def submit_comment():
    commenter_name = request.form.get('commenter_name', '').strip()
    comment_text = request.form.get('comment_text', '').strip()
    article_id_str = request.form.get('article_id', '').strip()

    try:
        article_id = int(article_id_str)
    except ValueError:
        return redirect(url_for('comments_page'))

    if not commenter_name or not comment_text:
        return redirect(url_for('comments_page'))

    articles = load_articles()
    article = None
    for a in articles:
        if a['article_id'] == article_id:
            article = a
            break

    if article is None:
        return redirect(url_for('comments_page'))

    comments = load_comments()
    comment_id = 1
    if comments:
        comment_id = max(c['comment_id'] for c in comments) + 1

    comment_date = datetime.now().strftime('%Y-%m-%d')

    new_comment = {
        'comment_id': comment_id,
        'article_id': article_id,
        'article_title': article['title'],
        'commenter_name': commenter_name,
        'comment_text': comment_text,
        'comment_date': comment_date
    }

    comments.append(new_comment)
    save_comments(comments)

    return redirect(url_for('comments_page'))


@app.route('/trending')
def trending_articles_page():
    trending = load_trending()

    trending_articles = [{'article_id': t['article_id'], 'article_title': t['article_title'], 'category': t['category'], 'view_count': t['view_count'], 'period': t['period']} for t in trending]

    return render_template('trending.html', trending_articles=trending_articles)


@app.route('/category/<string:category_name>')
def category_articles_page(category_name):
    articles = load_articles()
    filtered_articles = [a for a in articles if a['category'].lower() == category_name.lower()]

    # context articles keys: article_id:int, title:str, author:str, date:str, views:int
    articles_context = [{'article_id': a['article_id'], 'title': a['title'], 'author': a['author'], 'date': a['date'], 'views': a['views']} for a in filtered_articles]

    return render_template('category.html', category=category_name, articles=articles_context)


@app.route('/search')
def search_results_page():
    query = request.args.get('query', '').strip()
    articles = load_articles()

    results = []
    if query:
        q_lower = query.lower()
        for a in articles:
            if q_lower in a['title'].lower() or q_lower in a['content'].lower():
                excerpt = a['content']
                if len(excerpt) > 100:
                    excerpt = excerpt[:100] + '...'
                result = {
                    'article_id': a['article_id'],
                    'title': a['title'],
                    'excerpt': excerpt
                }
                results.append(result)

    return render_template('search_results.html', query=query, results=results)


if __name__ == '__main__':
    app.run(debug=True)
