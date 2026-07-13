from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

# File paths
ARTICLES_FILE = 'data/articles.txt'
CATEGORIES_FILE = 'data/categories.txt'
BOOKMARKS_FILE = 'data/bookmarks.txt'
COMMENTS_FILE = 'data/comments.txt'
TRENDING_FILE = 'data/trending.txt'


# Helper functions for file read/write

def read_articles():
    articles = []
    if not os.path.isfile(ARTICLES_FILE):
        return articles
    with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
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


def write_articles(articles):
    with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
        for a in articles:
            line = f"{a['article_id']}|{a['title']}|{a['author']}|{a['category']}|{a['content']}|{a['date']}|{a['views']}"
            f.write(line + '\n')


def read_categories():
    categories = []
    if not os.path.isfile(CATEGORIES_FILE):
        return categories
    with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            category = {
                'category_id': int(parts[0]),
                'category_name': parts[1],
                'description': parts[2]
            }
            categories.append(category)
    return categories


def read_bookmarks():
    bookmarks = []
    if not os.path.isfile(BOOKMARKS_FILE):
        return bookmarks
    with open(BOOKMARKS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 4:
                continue
            bookmark = {
                'bookmark_id': int(parts[0]),
                'article_id': int(parts[1]),
                'article_title': parts[2],
                'bookmarked_date': parts[3]
            }
            bookmarks.append(bookmark)
    return bookmarks


def write_bookmarks(bookmarks):
    with open(BOOKMARKS_FILE, 'w', encoding='utf-8') as f:
        for b in bookmarks:
            line = f"{b['bookmark_id']}|{b['article_id']}|{b['article_title']}|{b['bookmarked_date']}"
            f.write(line + '\n')


def read_comments():
    comments = []
    if not os.path.isfile(COMMENTS_FILE):
        return comments
    with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
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


def write_comments(comments):
    with open(COMMENTS_FILE, 'w', encoding='utf-8') as f:
        for c in comments:
            line = f"{c['comment_id']}|{c['article_id']}|{c['article_title']}|{c['commenter_name']}|{c['comment_text']}|{c['comment_date']}"
            f.write(line + '\n')


def read_trending():
    trending = []
    if not os.path.isfile(TRENDING_FILE):
        return trending
    with open(TRENDING_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            trend = {
                'article_id': int(parts[0]),
                'article_title': parts[1],
                'category': parts[2],
                'view_count': int(parts[3]),
                'period': parts[4]
            }
            trending.append(trend)
    return trending


# Route 1: Dashboard Page
@app.route('/', methods=['GET'])
def dashboard():
    '''Dashboard showing featured and trending articles'''
    articles = read_articles()
    trending = read_trending()

    # For featured articles, let's assume they are the most viewed top 5 articles as a simple metric
    featured_articles = sorted(articles, key=lambda x: x['views'], reverse=True)[:5]

    # Trending only first 5 for brief display
    trending_articles = trending[:5]

    return render_template('dashboard.html', featured_articles=featured_articles, trending_articles=trending_articles)


# Route 2: Article Catalog Page
@app.route('/articles', methods=['GET'])
def article_catalog():
    '''Articles catalog with optional search and category filter'''
    search_query = request.args.get('search', '').strip().lower()
    category_filter = request.args.get('category', '').strip().lower()
    articles = read_articles()

    categories = read_categories()  # Added categories list for template dropdown

    def matches_search(article):
        if not search_query:
            return True
        if (search_query in article['title'].lower() or
            search_query in article['author'].lower() or
            search_query in article['content'].lower()):
            return True
        return False

    def matches_category(article):
        if not category_filter:
            return True
        return article['category'].lower() == category_filter

    filtered_articles = [a for a in articles if matches_search(a) and matches_category(a)]

    return render_template('article_catalog.html', articles=filtered_articles, search=search_query, category=category_filter, categories=categories)


# Route 3: Article Details Page
@app.route('/article/<int:article_id>', methods=['GET'])
def article_details(article_id):
    '''Show full article details and increment view count'''
    articles = read_articles()
    found = None
    for article in articles:
        if article['article_id'] == article_id:
            found = article
            break
    if not found:
        return "Article Not Found", 404

    # Increment views and save
    found['views'] += 1
    write_articles(articles)

    return render_template('article_details.html', article=found)


# Route 4: Bookmark an Article
@app.route('/bookmark', methods=['POST'])
def add_bookmark():
    '''Add a bookmark for an article'''
    article_id = None
    if request.json:
        article_id = request.json.get('article_id')
    else:
        article_id = request.form.get('article_id')

    if not article_id:
        return jsonify({'success': False, 'message': 'Missing article_id'}), 400

    try:
        article_id = int(article_id)
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid article_id'}), 400

    articles = read_articles()
    article_title = None
    for article in articles:
        if article['article_id'] == article_id:
            article_title = article['title']
            break
    if not article_title:
        return jsonify({'success': False, 'message': 'Article not found'}), 404

    bookmarks = read_bookmarks()

    # Check if bookmark already exists
    for b in bookmarks:
        if b['article_id'] == article_id:
            return jsonify({'success': False, 'message': 'Bookmark already exists'}), 400

    # New bookmark ID
    bookmark_id = 1
    if bookmarks:
        bookmark_id = max(b['bookmark_id'] for b in bookmarks) + 1

    bookmarked_date = datetime.now().strftime('%Y-%m-%d')
    new_bookmark = {
        'bookmark_id': bookmark_id,
        'article_id': article_id,
        'article_title': article_title,
        'bookmarked_date': bookmarked_date
    }
    bookmarks.append(new_bookmark)
    write_bookmarks(bookmarks)

    return jsonify({'success': True, 'bookmark': new_bookmark}), 201


# Route 5: Remove Bookmark
@app.route('/bookmark/<int:bookmark_id>', methods=['DELETE'])
def remove_bookmark(bookmark_id):
    '''Remove a bookmark by bookmark_id'''
    bookmarks = read_bookmarks()
    new_bookmarks = [b for b in bookmarks if b['bookmark_id'] != bookmark_id]
    if len(new_bookmarks) == len(bookmarks):
        return jsonify({'success': False, 'message': 'Bookmark not found'}), 404

    write_bookmarks(new_bookmarks)
    return jsonify({'success': True})


# Route 6: Bookmarks Page
@app.route('/bookmarks', methods=['GET'])
def view_bookmarks():
    '''View all bookmarks'''
    bookmarks = read_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)


# Route 7: Comments Page
@app.route('/comments', methods=['GET'])
def comments_list():
    '''List comments, optionally filtered by article_id'''
    article_id = request.args.get('article_id')
    comments = read_comments()

    if article_id:
        try:
            article_id_int = int(article_id)
            comments = [c for c in comments if c['article_id'] == article_id_int]
        except ValueError:
            pass  # Ignore invalid article_id, return all

    return render_template('comments.html', comments=comments, filter_article_id=article_id)


# Route 8: Write Comment Submission
@app.route('/comment', methods=['POST'])
def add_comment():
    '''Add a new comment linked to an article'''
    article_id = None
    commenter_name = None
    comment_text = None
    if request.json:
        article_id = request.json.get('article_id')
        commenter_name = request.json.get('commenter_name')
        comment_text = request.json.get('comment_text')
    else:
        article_id = request.form.get('article_id')
        commenter_name = request.form.get('commenter_name')
        comment_text = request.form.get('comment_text')

    if not article_id or not commenter_name or not comment_text:
        return jsonify({'success': False, 'message': 'Missing fields'}), 400

    try:
        article_id = int(article_id)
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid article_id'}), 400

    articles = read_articles()
    article_title = None
    for article in articles:
        if article['article_id'] == article_id:
            article_title = article['title']
            break
    if not article_title:
        return jsonify({'success': False, 'message': 'Article not found'}), 404

    comments = read_comments()
    comment_id = 1
    if comments:
        comment_id = max(c['comment_id'] for c in comments) + 1

    comment_date = datetime.now().strftime('%Y-%m-%d')
    new_comment = {
        'comment_id': comment_id,
        'article_id': article_id,
        'article_title': article_title,
        'commenter_name': commenter_name,
        'comment_text': comment_text,
        'comment_date': comment_date
    }
    comments.append(new_comment)
    write_comments(comments)

    return jsonify({'success': True, 'comment': new_comment}), 201


# Route 9: Trending Articles Page
@app.route('/trending', methods=['GET'])
def trending_articles():
    '''Display trending articles with optional period filter'''
    period = request.args.get('period', '').strip()
    trending = read_trending()

    if period:
        filtered_trending = [t for t in trending if t['period'].lower() == period.lower()]
    else:
        filtered_trending = trending

    return render_template('trending.html', trending_articles=filtered_trending, period=period)


# Route 10: Category Page
@app.route('/category/<string:category_name>', methods=['GET'])
def category_articles(category_name):
    '''List articles filtered by category with optional sorting'''
    sort_by = request.args.get('sort_by', '').lower()
    articles = read_articles()

    filtered_articles = [a for a in articles if a['category'].lower() == category_name.lower()]

    if sort_by == 'date':
        filtered_articles.sort(key=lambda x: x['date'], reverse=True)  # Newest first
    elif sort_by == 'popularity':
        filtered_articles.sort(key=lambda x: x['views'], reverse=True)

    return render_template('category.html', category_name=category_name, articles=filtered_articles, sort_by=sort_by)


# Route 11: Search Results Page
@app.route('/search', methods=['GET'])
def search_articles():
    '''Search articles by query q in title, author, or keywords in content'''
    q = request.args.get('q', '').strip().lower()
    articles = read_articles()

    if q:
        matched_articles = [a for a in articles if q in a['title'].lower() or q in a['author'].lower() or q in a['content'].lower()]
    else:
        matched_articles = []

    return render_template('search_results.html', query=q, results=matched_articles)


if __name__ == '__main__':
    app.run(debug=True)
