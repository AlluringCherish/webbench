from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
ARTICLES_FILE = 'data/articles.txt'
CATEGORIES_FILE = 'data/categories.txt'
BOOKMARKS_FILE = 'data/bookmarks.txt'
COMMENTS_FILE = 'data/comments.txt'
TRENDING_FILE = 'data/trending.txt'

# Utility functions to read/write data

def read_articles():
    articles = []
    try:
        with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                article = {
                    'article_id': int(parts[0]),
                    'title': parts[1],
                    'author': parts[2],
                    'category': parts[3],
                    'content': parts[4],
                    'date': parts[5],
                    'views': int(parts[6]),
                }
                articles.append(article)
    except FileNotFoundError:
        pass
    return articles


def read_categories():
    categories = []
    try:
        with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 3:
                    continue
                cat = {
                    'category_id': int(parts[0]),
                    'category_name': parts[1],
                    'description': parts[2]
                }
                categories.append(cat)
    except FileNotFoundError:
        pass
    return categories


def read_bookmarks():
    bookmarks = []
    try:
        with open(BOOKMARKS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 4:
                    continue
                bm = {
                    'bookmark_id': int(parts[0]),
                    'article_id': int(parts[1]),
                    'article_title': parts[2],
                    'bookmarked_date': parts[3]
                }
                bookmarks.append(bm)
    except FileNotFoundError:
        pass
    return bookmarks


def write_bookmarks(bookmarks):
    try:
        with open(BOOKMARKS_FILE, 'w', encoding='utf-8') as f:
            for bm in bookmarks:
                f.write(f"{bm['bookmark_id']}|{bm['article_id']}|{bm['article_title']}|{bm['bookmarked_date']}\n")
    except Exception:
        pass


def read_comments():
    comments = []
    try:
        with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 6:
                    continue
                cm = {
                    'comment_id': int(parts[0]),
                    'article_id': int(parts[1]),
                    'article_title': parts[2],
                    'commenter_name': parts[3],
                    'comment_text': parts[4],
                    'comment_date': parts[5]
                }
                comments.append(cm)
    except FileNotFoundError:
        pass
    return comments


def write_comments(comments):
    try:
        with open(COMMENTS_FILE, 'w', encoding='utf-8') as f:
            for cm in comments:
                f.write(f"{cm['comment_id']}|{cm['article_id']}|{cm['article_title']}|{cm['commenter_name']}|{cm['comment_text']}|{cm['comment_date']}\n")
    except Exception:
        pass


def read_trending():
    trending = []
    try:
        with open(TRENDING_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 5:
                    continue
                tr = {
                    'article_id': int(parts[0]),
                    'title': parts[1],
                    'category': parts[2],
                    'view_count': int(parts[3]),
                    'period': parts[4],
                }
                trending.append(tr)
    except FileNotFoundError:
        pass
    return trending


def save_trending(trending):
    try:
        with open(TRENDING_FILE, 'w', encoding='utf-8') as f:
            for tr in trending:
                f.write(f"{tr['article_id']}|{tr['title']}|{tr['category']}|{tr['view_count']}|{tr['period']}\n")
    except Exception:
        pass


def build_article_excerpt(content, length=80):
    if len(content) <= length:
        return content
    # truncate and add ellipsis
    return content[:length].rsplit(' ',1)[0] + '...'


@app.route('/')
def redirect_to_dashboard():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # featured_articles: list of dict (article_id:int, title:str, author:str, date:str, excerpt:str)
    articles = read_articles()
    # Assuming featured means articles with highest views, pick top 5
    sorted_articles = sorted(articles, key=lambda x: x['views'], reverse=True)[:5]
    featured_articles = []
    for art in sorted_articles:
        featured_articles.append({
            'article_id': art['article_id'],
            'title': art['title'],
            'author': art['author'],
            'date': art['date'],
            'excerpt': build_article_excerpt(art['content']),
        })
    return render_template('dashboard.html', featured_articles=featured_articles)


@app.route('/catalog')
def article_catalog():
    articles = read_articles()
    categories = read_categories()
    # articles context: list of dict (article_id:int, title:str, author:str, date:str, category:str, thumbnail_url:str)
    # No thumbnail_url in data, so provide empty string or a placeholder value
    articles_context = []
    for art in articles:
        articles_context.append({
            'article_id': art['article_id'],
            'title': art['title'],
            'author': art['author'],
            'date': art['date'],
            'category': art['category'],
            'thumbnail_url': '',  # no data for thumbnail, empty
        })
    # categories context: list of dict (category_id:int, category_name:str)
    categories_context = [{'category_id': c['category_id'], 'category_name': c['category_name']} for c in categories]

    return render_template('article_catalog.html', articles=articles_context, categories=categories_context)


@app.route('/catalog/search', methods=['POST'])
def search_results():
    # Form data: search_query: str
    query = request.form.get('search_query', '').strip()
    articles = read_articles()
    results = []
    lower_query = query.lower()
    for art in articles:
        if lower_query in art['title'].lower() or lower_query in art['content'].lower():
            results.append({
                'article_id': art['article_id'],
                'title': art['title'],
                'excerpt': build_article_excerpt(art['content']),
            })
    return render_template('search_results.html', query=query, results=results)


@app.route('/article/<int:article_id>')
def article_details(article_id):
    articles = read_articles()
    bookmarks = read_bookmarks()

    article = None
    for art in articles:
        if art['article_id'] == article_id:
            article = {
                'article_id': art['article_id'],
                'title': art['title'],
                'author': art['author'],
                'date': art['date'],
                'content': art['content'],
            }
            break

    if not article:
        # Article not found, handle gracefully by redirecting to catalog
        return redirect(url_for('article_catalog'))

    # Check if bookmarked
    is_bookmarked = any(bm['article_id'] == article_id for bm in bookmarks)

    return render_template('article_details.html', article=article, is_bookmarked=is_bookmarked)


@app.route('/article/<int:article_id>/bookmark', methods=['POST'])
def bookmark_article(article_id):
    articles = read_articles()
    bookmarks = read_bookmarks()

    article = next((art for art in articles if art['article_id'] == article_id), None)
    if not article:
        # Article not found, redirect
        return redirect(url_for('article_details', article_id=article_id))

    # Check if already bookmarked
    if any(bm['article_id'] == article_id for bm in bookmarks):
        # Already bookmarked, redirect back
        return redirect(url_for('article_details', article_id=article_id))

    # Add bookmark
    max_id = max((bm['bookmark_id'] for bm in bookmarks), default=0)
    new_id = max_id + 1
    bookmarked_date = datetime.now().strftime('%Y-%m-%d')
    bookmarks.append({
        'bookmark_id': new_id,
        'article_id': article['article_id'],
        'article_title': article['title'],
        'bookmarked_date': bookmarked_date
    })

    write_bookmarks(bookmarks)

    return redirect(url_for('article_details', article_id=article_id))


@app.route('/bookmarks')
def bookmarks():
    bookmarks_list = read_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks_list)


@app.route('/bookmark/<int:bookmark_id>/remove', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks_list = read_bookmarks()
    bookmarks_list = [bm for bm in bookmarks_list if bm['bookmark_id'] != bookmark_id]
    write_bookmarks(bookmarks_list)
    return redirect(url_for('bookmarks'))


@app.route('/comment')
def comments():
    comments_list = read_comments()
    articles = read_articles()

    # Build article titles map
    article_map = {art['article_id']: art['title'] for art in articles}

    # Prepare comments with article titles
    comments_context = []
    for c in comments_list:
        title = article_map.get(c['article_id'], '')
        comments_context.append({
            'comment_id': c['comment_id'],
            'article_id': c['article_id'],
            'article_title': title,
            'commenter_name': c['commenter_name'],
            'comment_text': c['comment_text'],
            'comment_date': c['comment_date'],
        })

    # articles context: list of dict(article_id:int, title:str)
    articles_context = [{'article_id': art['article_id'], 'title': art['title']} for art in articles]

    return render_template('comments.html', comments=comments_context, articles=articles_context)


@app.route('/comment/write', methods=['GET'])
def write_comment():
    articles = read_articles()
    articles_context = [{'article_id': art['article_id'], 'title': art['title']} for art in articles]
    return render_template('write_comment.html', articles=articles_context)


@app.route('/comment/write', methods=['POST'])
def submit_comment():
    article_id = request.form.get('article_id')
    commenter_name = request.form.get('commenter_name', '').strip()
    comment_text = request.form.get('comment_text', '').strip()

    # Validate and convert article_id
    try:
        article_id = int(article_id)
    except (ValueError, TypeError):
        return redirect(url_for('write_comment'))

    if not commenter_name or not comment_text:
        return redirect(url_for('write_comment'))

    articles = read_articles()
    article = next((art for art in articles if art['article_id'] == article_id), None)
    if not article:
        return redirect(url_for('write_comment'))

    comments = read_comments()
    max_id = max((c['comment_id'] for c in comments), default=0)
    new_id = max_id + 1
    comment_date = datetime.now().strftime('%Y-%m-%d')

    new_comment = {
        'comment_id': new_id,
        'article_id': article_id,
        'article_title': article['title'],
        'commenter_name': commenter_name,
        'comment_text': comment_text,
        'comment_date': comment_date
    }

    comments.append(new_comment)
    write_comments(comments)

    return redirect(url_for('comments'))


@app.route('/trending')
def trending_articles():
    # Default time_period filter is 'This Week'
    time_period = 'This Week'
    trending_data = read_trending()
    filtered = [t for t in trending_data if t['period'] == time_period]

    # Sort by view_count descending
    filtered_sorted = sorted(filtered, key=lambda x: x['view_count'], reverse=True)

    trending_articles_list = []
    rank = 1
    for tr in filtered_sorted:
        trending_articles_list.append({
            'article_id': tr['article_id'],
            'title': tr['title'],
            'category': tr['category'],
            'view_count': tr['view_count'],
            'rank': rank
        })
        rank += 1

    return render_template('trending.html', trending_articles=trending_articles_list, time_period=time_period)


@app.route('/trending/filter', methods=['POST'])
def filter_trending():
    time_period = request.form.get('time_period', 'This Week')
    trending_data = read_trending()
    filtered = [t for t in trending_data if t['period'] == time_period]
    filtered_sorted = sorted(filtered, key=lambda x: x['view_count'], reverse=True)

    trending_articles_list = []
    rank = 1
    for tr in filtered_sorted:
        trending_articles_list.append({
            'article_id': tr['article_id'],
            'title': tr['title'],
            'category': tr['category'],
            'view_count': tr['view_count'],
            'rank': rank
        })
        rank += 1

    return render_template('trending.html', trending_articles=trending_articles_list, time_period=time_period)


@app.route('/category/<category_name>')
def category_articles(category_name):
    articles = read_articles()
    # Filter articles by category
    filtered = [a for a in articles if a['category'].lower() == category_name.lower()]
    # articles context: list of dict (article_id:int, title:str, date:str, popularity:int)
    # popularity from views
    articles_context = []
    for art in filtered:
        articles_context.append({
            'article_id': art['article_id'],
            'title': art['title'],
            'date': art['date'],
            'popularity': art['views'],
        })

    return render_template('category.html', category_name=category_name, articles=articles_context)


@app.route('/category/<category_name>/sort', methods=['POST'])
def sort_category_articles(category_name):
    sort_by = request.form.get('sort_by', 'date')
    articles = read_articles()
    filtered = [a for a in articles if a['category'].lower() == category_name.lower()]

    if sort_by == 'popularity':
        sorted_articles = sorted(filtered, key=lambda x: x['views'], reverse=True)
    else:
        # default or 'date'
        # dates expected format YYYY-MM-DD
        sorted_articles = sorted(filtered, key=lambda x: x['date'], reverse=True)

    articles_context = []
    for art in sorted_articles:
        articles_context.append({
            'article_id': art['article_id'],
            'title': art['title'],
            'date': art['date'],
            'popularity': art['views'],
        })

    return render_template('category.html', category_name=category_name, sort_by=sort_by, articles=articles_context)


if __name__ == '__main__':
    app.run(debug=True)
