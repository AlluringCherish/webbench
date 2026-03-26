'''
Flask backend application for NewsPortal web application.
Implements routing and data handling for all nine pages,
managing data stored in local text files under 'data/' directory.
Includes initialization to ensure data directory and files exist.
'''
import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
ARTICLES_FILE = os.path.join(DATA_DIR, 'articles.txt')
CATEGORIES_FILE = os.path.join(DATA_DIR, 'categories.txt')
BOOKMARKS_FILE = os.path.join(DATA_DIR, 'bookmarks.txt')
COMMENTS_FILE = os.path.join(DATA_DIR, 'comments.txt')
TRENDING_FILE = os.path.join(DATA_DIR, 'trending.txt')
def ensure_data_files():
    """
    Ensure that the data directory and required data files exist.
    If files do not exist, create them with empty content.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    for file_path in [ARTICLES_FILE, CATEGORIES_FILE, BOOKMARKS_FILE, COMMENTS_FILE, TRENDING_FILE]:
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('')  # create empty file
# Call ensure_data_files at startup
ensure_data_files()
# Utility functions to read/write data files
def read_articles():
    articles = []
    if not os.path.exists(ARTICLES_FILE):
        return articles
    with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            article_id, title, author, category, content, date, views = parts
            articles.append({
                'article_id': article_id,
                'title': title,
                'author': author,
                'category': category,
                'content': content,
                'date': date,
                'views': int(views)
            })
    return articles
def write_articles(articles):
    with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
        for a in articles:
            line = '|'.join([
                a['article_id'],
                a['title'],
                a['author'],
                a['category'],
                a['content'],
                a['date'],
                str(a['views'])
            ])
            f.write(line + '\n')
def read_categories():
    categories = []
    if not os.path.exists(CATEGORIES_FILE):
        return categories
    with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            category_id, category_name, description = parts
            categories.append({
                'category_id': category_id,
                'category_name': category_name,
                'description': description
            })
    return categories
def read_bookmarks():
    bookmarks = []
    if not os.path.exists(BOOKMARKS_FILE):
        return bookmarks
    with open(BOOKMARKS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 4:
                continue
            bookmark_id, article_id, article_title, bookmarked_date = parts
            bookmarks.append({
                'bookmark_id': bookmark_id,
                'article_id': article_id,
                'article_title': article_title,
                'bookmarked_date': bookmarked_date
            })
    return bookmarks
def write_bookmarks(bookmarks):
    with open(BOOKMARKS_FILE, 'w', encoding='utf-8') as f:
        for b in bookmarks:
            line = '|'.join([
                b['bookmark_id'],
                b['article_id'],
                b['article_title'],
                b['bookmarked_date']
            ])
            f.write(line + '\n')
def read_comments():
    comments = []
    if not os.path.exists(COMMENTS_FILE):
        return comments
    with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            comment_id, article_id, article_title, commenter_name, comment_text, comment_date = parts
            comments.append({
                'comment_id': comment_id,
                'article_id': article_id,
                'article_title': article_title,
                'commenter_name': commenter_name,
                'comment_text': comment_text,
                'comment_date': comment_date
            })
    return comments
def write_comments(comments):
    with open(COMMENTS_FILE, 'w', encoding='utf-8') as f:
        for c in comments:
            line = '|'.join([
                c['comment_id'],
                c['article_id'],
                c['article_title'],
                c['commenter_name'],
                c['comment_text'],
                c['comment_date']
            ])
            f.write(line + '\n')
def read_trending():
    trending = []
    if not os.path.exists(TRENDING_FILE):
        return trending
    with open(TRENDING_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            article_id, article_title, category, view_count, period = parts
            trending.append({
                'article_id': article_id,
                'article_title': article_title,
                'category': category,
                'view_count': int(view_count),
                'period': period
            })
    return trending
def get_next_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            cur_id = int(item[id_key])
            if cur_id > max_id:
                max_id = cur_id
        except Exception:
            continue
    return str(max_id + 1)
# Routes
@app.route('/')
def dashboard():
    # Dashboard page: show featured articles, trending news, and navigation buttons
    articles = read_articles()
    trending = read_trending()
    # Featured articles: let's pick top 3 articles by views
    featured_articles = sorted(articles, key=lambda x: x['views'], reverse=True)[:3]
    # Trending articles: filter for 'This Week' period for dashboard display
    trending_this_week = [t for t in trending if t['period'] == 'This Week']
    trending_this_week_sorted = sorted(trending_this_week, key=lambda x: x['view_count'], reverse=True)[:5]
    return render_template('dashboard.html',
                           featured_articles=featured_articles,
                           trending_articles=trending_this_week_sorted)
@app.route('/article_catalog', methods=['GET'])
def article_catalog():
    articles = read_articles()
    categories = read_categories()
    # Get search and filter parameters
    search_query = request.args.get('search', '').strip().lower()
    category_filter = request.args.get('category', '').strip()
    filtered_articles = articles
    # Filter by category if selected and valid
    if category_filter:
        filtered_articles = [a for a in filtered_articles if a['category'].lower() == category_filter.lower()]
    # Search by title, author, or keywords in title/content
    if search_query:
        filtered_articles = [a for a in filtered_articles if
                             search_query in a['title'].lower() or
                             search_query in a['author'].lower() or
                             search_query in a['content'].lower()]
    # Sort articles by date descending
    filtered_articles.sort(key=lambda x: x['date'], reverse=True)
    return render_template('article_catalog.html',
                           articles=filtered_articles,
                           categories=categories,
                           selected_category=category_filter,
                           search_query=search_query)
@app.route('/article_details/<article_id>', methods=['GET'])
def article_details(article_id):
    articles = read_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404
    # Increment views count for the article
    article['views'] += 1
    write_articles(articles)
    # Check if article is bookmarked
    bookmarks = read_bookmarks()
    bookmarked = any(b['article_id'] == article_id for b in bookmarks)
    return render_template('article_details.html',
                           article=article,
                           bookmarked=bookmarked)
@app.route('/bookmark_article/<article_id>', methods=['POST'])
def bookmark_article(article_id):
    articles = read_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404
    bookmarks = read_bookmarks()
    # Check if already bookmarked
    if any(b['article_id'] == article_id for b in bookmarks):
        # Already bookmarked, do nothing or redirect
        return redirect(url_for('bookmarks'))
    # Add new bookmark
    new_id = get_next_id(bookmarks, 'bookmark_id')
    bookmarked_date = datetime.now().strftime('%Y-%m-%d')
    bookmarks.append({
        'bookmark_id': new_id,
        'article_id': article['article_id'],
        'article_title': article['title'],
        'bookmarked_date': bookmarked_date
    })
    write_bookmarks(bookmarks)
    return redirect(url_for('bookmarks'))
@app.route('/bookmarks', methods=['GET'])
def bookmarks():
    bookmarks = read_bookmarks()
    # Sort bookmarks by bookmarked_date descending
    bookmarks.sort(key=lambda x: x['bookmarked_date'], reverse=True)
    return render_template('bookmarks.html', bookmarks=bookmarks)
@app.route('/remove_bookmark/<bookmark_id>', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = read_bookmarks()
    bookmarks = [b for b in bookmarks if b['bookmark_id'] != bookmark_id]
    write_bookmarks(bookmarks)
    return redirect(url_for('bookmarks'))
@app.route('/read_bookmark/<bookmark_id>', methods=['GET'])
def read_bookmark(bookmark_id):
    bookmarks = read_bookmarks()
    bookmark = next((b for b in bookmarks if b['bookmark_id'] == bookmark_id), None)
    if not bookmark:
        return "Bookmark not found", 404
    return redirect(url_for('article_details', article_id=bookmark['article_id']))
@app.route('/comments', methods=['GET'])
def comments():
    comments = read_comments()
    articles = read_articles()
    filter_article_id = request.args.get('article_id', '').strip()
    filtered_comments = comments
    if filter_article_id:
        filtered_comments = [c for c in comments if c['article_id'] == filter_article_id]
    # Sort comments by comment_date descending
    filtered_comments.sort(key=lambda x: x['comment_date'], reverse=True)
    return render_template('comments.html',
                           comments=filtered_comments,
                           articles=articles,
                           selected_article_id=filter_article_id)
@app.route('/write_comment', methods=['GET', 'POST'])
def write_comment():
    articles = read_articles()
    if request.method == 'POST':
        article_id = request.form.get('select-article', '').strip()
        commenter_name = request.form.get('commenter-name', '').strip()
        comment_text = request.form.get('comment-text', '').strip()
        if not article_id or not commenter_name or not comment_text:
            # Missing fields, reload form with error message
            error = "All fields are required."
            return render_template('write_comment.html', articles=articles, error=error,
                                   selected_article_id=article_id,
                                   commenter_name=commenter_name,
                                   comment_text=comment_text)
        article = next((a for a in articles if a['article_id'] == article_id), None)
        if not article:
            error = "Selected article not found."
            return render_template('write_comment.html', articles=articles, error=error)
        comments = read_comments()
        new_id = get_next_id(comments, 'comment_id')
        comment_date = datetime.now().strftime('%Y-%m-%d')
        comments.append({
            'comment_id': new_id,
            'article_id': article_id,
            'article_title': article['title'],
            'commenter_name': commenter_name,
            'comment_text': comment_text,
            'comment_date': comment_date
        })
        write_comments(comments)
        return redirect(url_for('comments'))
    # GET request
    return render_template('write_comment.html', articles=articles)
@app.route('/trending_articles', methods=['GET'])
def trending_articles():
    trending = read_trending()
    time_period_filter = request.args.get('period', '').strip()
    if time_period_filter:
        filtered_trending = [t for t in trending if t['period'].lower() == time_period_filter.lower()]
    else:
        filtered_trending = trending
    # Sort by view_count descending
    filtered_trending.sort(key=lambda x: x['view_count'], reverse=True)
    return render_template('trending_articles.html',
                           trending_articles=filtered_trending,
                           selected_period=time_period_filter)
@app.route('/category/<category_name>', methods=['GET'])
def category_page(category_name):
    articles = read_articles()
    categories = read_categories()
    category_name_lower = category_name.lower()
    # Find category display name and description
    category_obj = next((c for c in categories if c['category_name'].lower() == category_name_lower), None)
    if not category_obj:
        return "Category not found", 404
    category_articles = [a for a in articles if a['category'].lower() == category_name_lower]
    # Sorting
    sort_by = request.args.get('sort', '').lower()
    if sort_by == 'date':
        category_articles.sort(key=lambda x: x['date'], reverse=True)
    elif sort_by == 'popularity':
        category_articles.sort(key=lambda x: x['views'], reverse=True)
    else:
        # Default sort by date descending
        category_articles.sort(key=lambda x: x['date'], reverse=True)
    return render_template('category.html',
                           category=category_obj,
                           articles=category_articles,
                           sort_by=sort_by)
@app.route('/search_results', methods=['GET'])
def search_results():
    query = request.args.get('q', '').strip()
    articles = read_articles()
    if not query:
        # No query, show empty results
        results = []
    else:
        query_lower = query.lower()
        results = [a for a in articles if
                   query_lower in a['title'].lower() or
                   query_lower in a['author'].lower() or
                   query_lower in a['content'].lower()]
    # Sort results by date descending
    results.sort(key=lambda x: x['date'], reverse=True)
    return render_template('search_results.html',
                           query=query,
                           results=results)
if __name__ == '__main__':
    app.run(port=5000, debug=True)