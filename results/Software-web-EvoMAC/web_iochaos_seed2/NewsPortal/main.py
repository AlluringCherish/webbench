'''
Main backend application for NewsPortal web application.
Handles routing, data reading/writing from/to local text files,
business logic for all pages, and serves HTML templates.
No authentication required; all features directly accessible.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
# Utility functions for reading and writing data files
def read_articles():
    articles = []
    path = os.path.join(DATA_DIR, 'articles.txt')
    if not os.path.exists(path):
        return articles
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
    path = os.path.join(DATA_DIR, 'articles.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for a in articles:
            line = '|'.join([
                str(a['article_id']),
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
    path = os.path.join(DATA_DIR, 'categories.txt')
    if not os.path.exists(path):
        return categories
    with open(path, 'r', encoding='utf-8') as f:
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
    path = os.path.join(DATA_DIR, 'bookmarks.txt')
    if not os.path.exists(path):
        return bookmarks
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
                'bookmark_id': bookmark_id,
                'article_id': article_id,
                'article_title': article_title,
                'bookmarked_date': bookmarked_date
            })
    return bookmarks
def write_bookmarks(bookmarks):
    path = os.path.join(DATA_DIR, 'bookmarks.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in bookmarks:
            line = '|'.join([
                str(b['bookmark_id']),
                b['article_id'],
                b['article_title'],
                b['bookmarked_date']
            ])
            f.write(line + '\n')
def read_comments():
    comments = []
    path = os.path.join(DATA_DIR, 'comments.txt')
    if not os.path.exists(path):
        return comments
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
                'comment_id': comment_id,
                'article_id': article_id,
                'article_title': article_title,
                'commenter_name': commenter_name,
                'comment_text': comment_text,
                'comment_date': comment_date
            })
    return comments
def write_comments(comments):
    path = os.path.join(DATA_DIR, 'comments.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for c in comments:
            line = '|'.join([
                str(c['comment_id']),
                c['article_id'],
                c['article_title'],
                c['commenter_name'],
                c['comment_text'],
                c['comment_date']
            ])
            f.write(line + '\n')
def read_trending():
    trending = []
    path = os.path.join(DATA_DIR, 'trending.txt')
    if not os.path.exists(path):
        return trending
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
                'article_id': article_id,
                'article_title': article_title,
                'category': category,
                'view_count': int(view_count),
                'period': period
            })
    return trending
def write_trending(trending):
    path = os.path.join(DATA_DIR, 'trending.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for t in trending:
            line = '|'.join([
                t['article_id'],
                t['article_title'],
                t['category'],
                str(t['view_count']),
                t['period']
            ])
            f.write(line + '\n')
# Helper functions
def get_article_by_id(article_id):
    articles = read_articles()
    for article in articles:
        if article['article_id'] == str(article_id):
            return article
    return None
def get_category_by_name(category_name):
    categories = read_categories()
    for category in categories:
        if category['category_name'].lower() == category_name.lower():
            return category
    return None
def get_next_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            current_id = int(item[id_key])
            if current_id > max_id:
                max_id = current_id
        except:
            continue
    return max_id + 1
def update_article_views(article_id):
    articles = read_articles()
    updated = False
    for article in articles:
        if article['article_id'] == str(article_id):
            article['views'] += 1
            updated = True
            break
    if updated:
        write_articles(articles)
def filter_articles_by_category(category_name):
    articles = read_articles()
    filtered = [a for a in articles if a['category'].lower() == category_name.lower()]
    return filtered
def search_articles(query):
    query_lower = query.lower()
    articles = read_articles()
    results = []
    for a in articles:
        if (query_lower in a['title'].lower() or
            query_lower in a['author'].lower() or
            query_lower in a['content'].lower()):
            results.append(a)
    return results
def sort_articles(articles, by='date', descending=True):
    if by == 'date':
        # date format: YYYY-MM-DD
        articles_sorted = sorted(articles, key=lambda x: x['date'], reverse=descending)
    elif by == 'popularity':
        articles_sorted = sorted(articles, key=lambda x: x['views'], reverse=descending)
    else:
        articles_sorted = articles
    return articles_sorted
def get_featured_articles():
    # For simplicity, featured articles are top 3 by views
    articles = read_articles()
    featured = sort_articles(articles, by='popularity')[:3]
    return featured
def get_trending_articles(period=None):
    trending = read_trending()
    if period:
        trending = [t for t in trending if t['period'].lower() == period.lower()]
    # Sort by view_count descending
    trending_sorted = sorted(trending, key=lambda x: x['view_count'], reverse=True)
    return trending_sorted
def get_comments_by_article(article_id=None):
    comments = read_comments()
    if article_id:
        comments = [c for c in comments if c['article_id'] == str(article_id)]
    return comments
# Routes
@app.route('/')
def dashboard():
    featured_articles = get_featured_articles()
    trending_articles = get_trending_articles(period='This Week')
    return render_template('dashboard.html',
                           featured_articles=featured_articles,
                           trending_articles=trending_articles)
@app.route('/articles')
def article_catalog():
    articles = read_articles()
    categories = read_categories()
    # Get filter parameters
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()
    filtered_articles = articles
    if category_filter:
        filtered_articles = [a for a in filtered_articles if a['category'].lower() == category_filter.lower()]
    if search_query:
        search_query_lower = search_query.lower()
        filtered_articles = [a for a in filtered_articles if
                             search_query_lower in a['title'].lower() or
                             search_query_lower in a['author'].lower() or
                             search_query_lower in a['content'].lower()]
    # Sort by date descending by default
    filtered_articles = sort_articles(filtered_articles, by='date', descending=True)
    return render_template('article_catalog.html',
                           articles=filtered_articles,
                           categories=categories,
                           selected_category=category_filter,
                           search_query=search_query)
@app.route('/article/<article_id>')
def article_details(article_id):
    article = get_article_by_id(article_id)
    if not article:
        return "Article not found", 404
    # Update views count
    update_article_views(article_id)
    return render_template('article_details.html', article=article)
@app.route('/bookmark/<article_id>', methods=['POST'])
def bookmark_article(article_id):
    article = get_article_by_id(article_id)
    if not article:
        return "Article not found", 404
    bookmarks = read_bookmarks()
    # Check if already bookmarked
    for b in bookmarks:
        if b['article_id'] == str(article_id):
            # Already bookmarked, do nothing
            return redirect(url_for('bookmarks'))
    # Add new bookmark
    new_id = get_next_id(bookmarks, 'bookmark_id')
    bookmarked_date = datetime.now().strftime('%Y-%m-%d')
    bookmarks.append({
        'bookmark_id': str(new_id),
        'article_id': str(article_id),
        'article_title': article['title'],
        'bookmarked_date': bookmarked_date
    })
    write_bookmarks(bookmarks)
    return redirect(url_for('bookmarks'))
@app.route('/bookmarks')
def bookmarks():
    bookmarks = read_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)
@app.route('/bookmark/remove/<bookmark_id>', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = read_bookmarks()
    bookmarks = [b for b in bookmarks if b['bookmark_id'] != str(bookmark_id)]
    write_bookmarks(bookmarks)
    return redirect(url_for('bookmarks'))
@app.route('/bookmark/read/<bookmark_id>')
def read_bookmark(bookmark_id):
    bookmarks = read_bookmarks()
    bookmark = None
    for b in bookmarks:
        if b['bookmark_id'] == str(bookmark_id):
            bookmark = b
            break
    if not bookmark:
        return "Bookmark not found", 404
    return redirect(url_for('article_details', article_id=bookmark['article_id']))
@app.route('/comments')
def comments():
    comments = read_comments()
    articles = read_articles()
    filter_article_id = request.args.get('article', '').strip()
    filtered_comments = comments
    if filter_article_id:
        filtered_comments = [c for c in comments if c['article_id'] == filter_article_id]
    return render_template('comments.html',
                           comments=filtered_comments,
                           articles=articles,
                           selected_article=filter_article_id)
@app.route('/comments/write', methods=['GET', 'POST'])
def write_comment():
    articles = read_articles()
    if request.method == 'POST':
        article_id = request.form.get('select-article', '').strip()
        commenter_name = request.form.get('commenter-name', '').strip()
        comment_text = request.form.get('comment-text', '').strip()
        if not article_id or not commenter_name or not comment_text:
            error = "All fields are required."
            return render_template('write_comment.html', articles=articles, error=error,
                                   form_data=request.form)
        article = get_article_by_id(article_id)
        if not article:
            error = "Selected article not found."
            return render_template('write_comment.html', articles=articles, error=error,
                                   form_data=request.form)
        comments = read_comments()
        new_id = get_next_id(comments, 'comment_id')
        comment_date = datetime.now().strftime('%Y-%m-%d')
        comments.append({
            'comment_id': str(new_id),
            'article_id': article_id,
            'article_title': article['title'],
            'commenter_name': commenter_name,
            'comment_text': comment_text,
            'comment_date': comment_date
        })
        write_comments(comments)
        return redirect(url_for('comments'))
    else:
        return render_template('write_comment.html', articles=articles)
@app.route('/trending')
def trending():
    period = request.args.get('period', 'This Week')
    trending_articles = get_trending_articles(period=period)
    return render_template('trending.html',
                           trending_articles=trending_articles,
                           selected_period=period)
@app.route('/category/<category_name>')
def category_page(category_name):
    categories = read_categories()
    category = get_category_by_name(category_name)
    if not category:
        return "Category not found", 404
    articles = filter_articles_by_category(category_name)
    sort_by = request.args.get('sort', 'date')
    if sort_by not in ['date', 'popularity']:
        sort_by = 'date'
    articles = sort_articles(articles, by=sort_by)
    return render_template('category.html',
                           category=category,
                           articles=articles,
                           sort_by=sort_by)
@app.route('/search')
def search_results():
    query = request.args.get('q', '').strip()
    results = []
    if query:
        results = search_articles(query)
    return render_template('search_results.html',
                           query=query,
                           results=results)
# Run the app on local port 5000
if __name__ == '__main__':
    app.run(port=5000, debug=True)