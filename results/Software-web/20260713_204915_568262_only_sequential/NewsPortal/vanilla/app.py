from flask import Flask, render_template, request, redirect, url_for, abort
import os
from datetime import datetime

app = Flask(__name__)

# Data file paths
ARTICLES_FILE = 'data/articles.txt'
CATEGORIES_FILE = 'data/categories.txt'
BOOKMARKS_FILE = 'data/bookmarks.txt'
COMMENTS_FILE = 'data/comments.txt'
TRENDING_FILE = 'data/trending.txt'

# Utility functions to load data

def load_articles():
    articles = []
    if not os.path.exists(ARTICLES_FILE):
        return articles
    with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) !=7:
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
    if not os.path.exists(CATEGORIES_FILE):
        return categories
    with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) !=3:
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
    if not os.path.exists(BOOKMARKS_FILE):
        return bookmarks
    with open(BOOKMARKS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts)!=4:
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

def write_bookmarks(bookmarks):
    lines = []
    for bm in bookmarks:
        line = f"{bm['bookmark_id']}|{bm['article_id']}|{bm['article_title']}|{bm['bookmarked_date']}"
        lines.append(line)
    with open(BOOKMARKS_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines)+'\n')


def load_comments():
    comments = []
    if not os.path.exists(COMMENTS_FILE):
        return comments
    with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts)!=6:
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

def write_comments(comments):
    lines = []
    for c in comments:
        line = f"{c['comment_id']}|{c['article_id']}|{c['article_title']}|{c['commenter_name']}|{c['comment_text']}|{c['comment_date']}"
        lines.append(line)
    with open(COMMENTS_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines)+'\n')


def load_trending():
    trending = []
    if not os.path.exists(TRENDING_FILE):
        return trending
    with open(TRENDING_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts)!=5:
                continue
            try:
                trend = {
                    'article_id': int(parts[0]),
                    'article_title': parts[1],
                    'category': parts[2],
                    'view_count': int(parts[3]),
                    'period': parts[4]
                }
                trending.append(trend)
            except:
                continue
    return trending

# Helper functions

def get_article_by_id(article_id):
    articles = load_articles()
    for article in articles:
        if article['article_id'] == article_id:
            return article
    return None

def get_category_by_id(category_id):
    categories = load_categories()
    for category in categories:
        if category['category_id'] == category_id:
            return category
    return None

# Routes

@app.route('/dashboard')
def dashboard():
    # For dashboard, show some featured articles (could treat top 3 by views as featured)
    articles = load_articles()
    featured_articles = sorted(articles, key=lambda x: x['views'], reverse=True)[:3]
    return render_template('dashboard.html',
                           title='News Portal',
                           featured_articles=featured_articles,
                           element_ids={
                               'dashboard_page': 'dashboard-page',
                               'featured_articles': 'featured-articles',
                               'browse_articles_button': 'browse-articles-button',
                               'view_bookmarks_button': 'view-bookmarks-button',
                               'trending_articles_button': 'trending-articles-button'
                           })

@app.route('/articles')
def articles_catalog():
    # Load articles and categories
    articles = load_articles()
    categories = load_categories()

    # Filtering by category query param
    category_filter = request.args.get('category', '')  # category name expected
    if category_filter:
        articles = [a for a in articles if a['category'].lower() == category_filter.lower()]

    # Search query param
    search_query = request.args.get('search', '')
    if search_query:
        articles = [a for a in articles if search_query.lower() in a['title'].lower()]

    # Send category options for dropdown
    category_names = [c['category_name'] for c in categories]

    return render_template('articles_catalog.html',
                           title='Article Catalog',
                           articles=articles,
                           categories=categories,
                           category_filter=category_filter,
                           search_query=search_query,
                           element_ids={
                               'catalog_page': 'catalog-page',
                               'search_input': 'search-input',
                               'category_filter': 'category-filter',
                               'articles_grid': 'articles-grid'
                           })

@app.route('/articles/<int:article_id>')
def article_details(article_id):
    article = get_article_by_id(article_id)
    if not article:
        abort(404)
    return render_template('article_details.html',
                           title='Article Details',
                           article=article,
                           element_ids={
                               'article_details_page': 'article-details-page',
                               'article_title': 'article-title',
                               'article_author': 'article-author',
                               'article_date': 'article-date',
                               'bookmark_button': 'bookmark-button',
                               'article_content': 'article-content'
                           })

@app.route('/articles/<int:article_id>/bookmark', methods=['POST'])
def post_bookmark(article_id):
    article = get_article_by_id(article_id)
    if not article:
        abort(404)
    bookmarks = load_bookmarks()
    # Check if already bookmarked
    for bm in bookmarks:
        if bm['article_id'] == article_id:
            # Already bookmarked, redirect to dashboard
            return redirect(url_for('dashboard'))
    # Add new bookmark
    new_id = max([bm['bookmark_id'] for bm in bookmarks], default=0) + 1
    bookmarked_date = datetime.now().strftime('%Y-%m-%d')
    new_bm = {
        'bookmark_id': new_id,
        'article_id': article['article_id'],
        'article_title': article['title'],
        'bookmarked_date': bookmarked_date
    }
    bookmarks.append(new_bm)
    write_bookmarks(bookmarks)
    return redirect(url_for('dashboard'))

@app.route('/bookmarks')
def bookmarks():
    bookmarks = load_bookmarks()
    return render_template('bookmarks.html',
                           title='My Bookmarks',
                           bookmarks=bookmarks,
                           element_ids={
                               'bookmarks_page': 'bookmarks-page',
                               'bookmarks_list': 'bookmarks-list'
                           })

@app.route('/bookmarks/<int:bookmark_id>/remove', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = load_bookmarks()
    bookmarks = [bm for bm in bookmarks if bm['bookmark_id'] != bookmark_id]
    write_bookmarks(bookmarks)
    return redirect(url_for('bookmarks'))

@app.route('/bookmarks/<int:bookmark_id>/read')
def read_bookmark(bookmark_id):
    bookmarks = load_bookmarks()
    bookmark = next((bm for bm in bookmarks if bm['bookmark_id'] == bookmark_id), None)
    if not bookmark:
        abort(404)
    article = get_article_by_id(bookmark['article_id'])
    if not article:
        abort(404)
    return render_template('article_details.html',
                           title='Article Details',
                           article=article,
                           element_ids={
                               'article_details_page': 'article-details-page',
                               'article_title': 'article-title',
                               'article_author': 'article-author',
                               'article_date': 'article-date',
                               'bookmark_button': 'bookmark-button',
                               'article_content': 'article-content'
                           })

@app.route('/comments')
def comments():
    comments = load_comments()
    articles = load_articles()

    # Filter comments by article if query param article_id exists
    try:
        filter_article_id = int(request.args.get('article_id', ''))
    except:
        filter_article_id = None

    if filter_article_id:
        comments = [c for c in comments if c['article_id'] == filter_article_id]

    selected_article_id = str(filter_article_id) if filter_article_id else ''

    return render_template('comments.html',
                           title='Article Comments',
                           comments=comments,
                           articles=articles,
                           filter_article_id=filter_article_id,
                           selected_article_id=selected_article_id,
                           element_ids={
                               'comments_page': 'comments-page',
                               'comments_list': 'comments-list'
                           })

@app.route('/comments/write', methods=['GET'])
def write_comment_page():
    articles = load_articles()
    return render_template('write_comment.html',
                           title='Write a Comment',
                           articles=articles,
                           element_ids={
                               'write_comment_page': 'write-comment-page',
                               'select_article': 'select-article',
                               'commenter_name': 'commenter-name',
                               'comment_text': 'comment-text'
                           })

@app.route('/comments/write', methods=['POST'])
def submit_comment():
    articles = load_articles()
    article_id = request.form.get('article_id', '')
    commenter_name = request.form.get('commenter_name', '').strip()
    comment_text = request.form.get('comment_text', '').strip()

    if not article_id or not commenter_name or not comment_text:
        # Missing input; could handle with flash message or simple redirect back
        return redirect(url_for('write_comment_page'))
    try:
        article_id_int = int(article_id)
    except:
        return redirect(url_for('write_comment_page'))

    article = get_article_by_id(article_id_int)
    if not article:
        return redirect(url_for('write_comment_page'))

    comments = load_comments()
    new_id = max([c['comment_id'] for c in comments], default=0) + 1
    comment_date = datetime.now().strftime('%Y-%m-%d')

    new_comment = {
        'comment_id': new_id,
        'article_id': article_id_int,
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
    trending = load_trending()
    period_filter = request.args.get('period', '')  # e.g., "Today", "This Week", "This Month"
    if period_filter:
        trending = [t for t in trending if t['period'].lower() == period_filter.lower()]
    periods = sorted(set(t['period'] for t in load_trending()))

    return render_template('trending_articles.html',
                           title='Trending Articles',
                           trending=trending,
                           periods=periods,
                           selected_period=period_filter,
                           element_ids={
                               'trending_page': 'trending-page',
                               'trending_list': 'trending-list'
                           })

@app.route('/category/<int:category_id>')
def category_articles(category_id):
    category = get_category_by_id(category_id)
    if not category:
        abort(404)
    articles = load_articles()
    filtered = [a for a in articles if a['category'].lower() == category['category_name'].lower()]

    # Sorting by query param
    sort_by = request.args.get('sort', '')  # 'date' or 'popularity'

    if sort_by == 'date':
        filtered.sort(key=lambda x: x['date'], reverse=True)
    elif sort_by == 'popularity':
        filtered.sort(key=lambda x: x['views'], reverse=True)

    return render_template('category_articles.html',
                           title='Category Articles',
                           category=category,
                           articles=filtered,
                           sort_by=sort_by,
                           element_ids={
                               'category_page': 'category-page',
                               'category_title': 'category-title'
                           })

@app.route('/search')
def search_results():
    query = request.args.get('query', '').strip()
    articles = []
    if query:
        all_articles = load_articles()
        articles = [a for a in all_articles if query.lower() in a['title'].lower() or query.lower() in a['content'].lower()]

    return render_template('search_results.html',
                           title='Search Results',
                           query=query,
                           results=articles,
                           element_ids={
                               'search_results_page': 'search-results-page',
                               'search_query_display': 'search-query-display',
                               'results_list': 'results-list',
                               'no_results_message': 'no-results-message'
                           })

# Run app
if __name__ == '__main__':
    app.run(debug=True)
