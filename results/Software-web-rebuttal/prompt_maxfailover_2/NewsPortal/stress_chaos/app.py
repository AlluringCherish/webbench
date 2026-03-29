from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'


# Helper functions to load and save data

def load_articles():
    path = os.path.join(DATA_DIR, 'articles.txt')
    articles = []
    try:
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
                except ValueError:
                    continue
    except (FileNotFoundError, IOError):
        pass
    return articles


def load_categories():
    path = os.path.join(DATA_DIR, 'categories.txt')
    categories = []
    try:
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
                except ValueError:
                    continue
    except (FileNotFoundError, IOError):
        pass
    return categories


def load_bookmarks():
    path = os.path.join(DATA_DIR, 'bookmarks.txt')
    bookmarks = []
    try:
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
                except ValueError:
                    continue
    except (FileNotFoundError, IOError):
        pass
    return bookmarks


def save_bookmarks(bookmarks):
    path = os.path.join(DATA_DIR, 'bookmarks.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for bm in bookmarks:
                line = f"{bm['bookmark_id']}|{bm['article_id']}|{bm['article_title']}|{bm['bookmarked_date']}\n"
                f.write(line)
    except (IOError, FileNotFoundError):
        pass


def load_comments():
    path = os.path.join(DATA_DIR, 'comments.txt')
    comments = []
    try:
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
                except ValueError:
                    continue
    except (FileNotFoundError, IOError):
        pass
    return comments


def save_comments(comments):
    path = os.path.join(DATA_DIR, 'comments.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for c in comments:
                line = f"{c['comment_id']}|{c['article_id']}|{c['article_title']}|{c['commenter_name']}|{c['comment_text']}|{c['comment_date']}\n"
                f.write(line)
    except (IOError, FileNotFoundError):
        pass


def load_trending():
    path = os.path.join(DATA_DIR, 'trending.txt')
    trending_articles = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                try:
                    ta = {
                        'article_id': int(parts[0]),
                        'title': parts[1],
                        'category': parts[2],
                        'view_count': int(parts[3]),
                        'period': parts[4]
                    }
                    trending_articles.append(ta)
                except ValueError:
                    continue
    except (FileNotFoundError, IOError):
        pass
    return trending_articles


def get_next_comment_id(comments):
    if not comments:
        return 1
    return max(c['comment_id'] for c in comments) + 1

def get_next_bookmark_id(bookmarks):
    if not bookmarks:
        return 1
    return max(bm['bookmark_id'] for bm in bookmarks) + 1


# Flask Routes Implementations

@app.route('/')
def dashboard():
    articles = load_articles()
    categories = load_categories()
    bookmarks = load_bookmarks()
    trending_articles = load_trending()

    category_filter = None
    sort = None
    page_title = 'News Portal'

    return render_template('dashboard.html',
                           articles=articles,
                           categories=categories,
                           bookmarks=bookmarks,
                           trending_articles=trending_articles,
                           category_filter=category_filter,
                           sort=sort,
                           page_title=page_title)


@app.route('/catalog')
def catalog_page():
    articles = load_articles()
    categories = load_categories()
    search_query = request.args.get('search_query')
    if search_query:
        search_query = search_query.strip()
    else:
        search_query = None

    category_filter = request.args.get('category_filter')
    if category_filter:
        category_filter = category_filter.strip()
    else:
        category_filter = None

    filtered_articles = articles

    if search_query:
        filtered_articles = [a for a in filtered_articles if search_query.lower() in a['title'].lower() or search_query.lower() in a['content'].lower()]
    if category_filter:
        filtered_articles = [a for a in filtered_articles if a['category'] == category_filter]

    page_title = 'Article Catalog'

    return render_template('catalog.html',
                           articles=filtered_articles,
                           categories=categories,
                           search_query=search_query,
                           category_filter=category_filter,
                           page_title=page_title)


@app.route('/articles/<int:article_id>', methods=['GET', 'POST'])
def article_details(article_id):
    articles = load_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        # Article not found, show 404
        return "Article not found", 404

    comments = load_comments()
    article_comments = [c for c in comments if c['article_id'] == article_id]

    bookmarks = load_bookmarks()

    is_bookmarked = any(bm['article_id'] == article_id for bm in bookmarks)

    if request.method == 'POST':
        commenter_name = request.form.get('commenter_name', '').strip()
        comment_text = request.form.get('comment_text', '').strip()
        if commenter_name and comment_text:
            # Add new comment
            comment_id = get_next_comment_id(comments)
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
            # Refresh comments list
            article_comments.append(new_comment)

    page_title = 'Article Details'

    return render_template('article_details.html',
                           article=article,
                           comments=article_comments,
                           is_bookmarked=is_bookmarked,
                           page_title=page_title)


@app.route('/bookmarks')
def bookmarks_page():
    bookmarks = load_bookmarks()
    page_title = 'My Bookmarks'
    return render_template('bookmarks.html',
                           bookmarks=bookmarks,
                           page_title=page_title)


@app.route('/bookmarks/remove/<int:bookmark_id>', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = load_bookmarks()
    bookmarks = [bm for bm in bookmarks if bm['bookmark_id'] != bookmark_id]
    save_bookmarks(bookmarks)
    return redirect(url_for('bookmarks_page'))


@app.route('/comments')
def comments_page():
    comments = load_comments()
    articles = load_articles()
    selected_article_id = request.args.get('selected_article_id')
    if selected_article_id:
        try:
            selected_article_id = int(selected_article_id)
            comments = [c for c in comments if c['article_id'] == selected_article_id]
        except ValueError:
            selected_article_id = None
    else:
        selected_article_id = None

    page_title = 'Article Comments'
    return render_template('comments.html',
                           comments=comments,
                           articles=articles,
                           selected_article_id=selected_article_id,
                           page_title=page_title)


@app.route('/write-comment', methods=['GET', 'POST'])
def write_comment_page():
    articles = load_articles()
    if request.method == 'POST':
        commenter_name = request.form.get('commenter_name', '').strip()
        comment_text = request.form.get('comment_text', '').strip()
        article_id_str = request.form.get('article_id')
        if article_id_str and article_id_str.isdigit():
            article_id = int(article_id_str)
        else:
            article_id = None

        if commenter_name and comment_text and article_id is not None:
            # Validate if article exists
            article = next((a for a in articles if a['article_id'] == article_id), None)
            if article:
                comments = load_comments()
                comment_id = get_next_comment_id(comments)
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

    page_title = 'Write a Comment'
    return render_template('write_comment.html',
                           articles=articles,
                           page_title=page_title)


@app.route('/trending')
def trending_page():
    trending_articles = load_trending()
    time_period_filter = request.args.get('time_period_filter')
    if time_period_filter:
        time_period_filter = time_period_filter.strip()
    else:
        time_period_filter = None

    filtered_trending = trending_articles
    if time_period_filter:
        filtered_trending = [t for t in trending_articles if t['period'] == time_period_filter]

    page_title = 'Trending Articles'
    return render_template('trending.html',
                           trending_articles=filtered_trending,
                           time_period_filter=time_period_filter,
                           page_title=page_title)


@app.route('/category/<string:category_name>')
def category_page(category_name):
    articles = load_articles()
    filtered_articles = [a for a in articles if a['category'] == category_name]

    sort_order = request.args.get('sort_order')
    if sort_order not in ('date', 'popularity'):
        sort_order = None

    if sort_order == 'date':
        filtered_articles.sort(key=lambda x: x['date'], reverse=True)  # latest first
    elif sort_order == 'popularity':
        filtered_articles.sort(key=lambda x: x['views'], reverse=True)

    page_title = 'Category Articles'

    return render_template('category.html',
                           category_name=category_name,
                           articles=filtered_articles,
                           page_title=page_title,
                           sort_order=sort_order)


@app.route('/search')
def search_results_page():
    query = request.args.get('query')
    if query:
        query = query.strip()
    else:
        query = None

    category = request.args.get('category')
    if category:
        category = category.strip()
    else:
        category = None

    articles = load_articles()
    filtered_articles = articles

    if query:
        filtered_articles = [a for a in filtered_articles if query.lower() in a['title'].lower() or query.lower() in a['content'].lower()]

    if category:
        filtered_articles = [a for a in filtered_articles if a['category'] == category]

    page_title = 'Search Results'

    return render_template('search_results.html',
                           articles=filtered_articles,
                           query=query,
                           page_title=page_title)


if __name__ == '__main__':
    app.run(debug=True)
