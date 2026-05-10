'''
Main backend Python application file for NewsPortal web application.
Implements routing, data handling, and business logic for all nine pages.
Uses local text files in 'data' directory for data storage.
No authentication; all features directly accessible.
Website starts at Dashboard page on route '/'.
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
                b['bookmark_id'],
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
# Helper to get next ID for bookmarks and comments
def get_next_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            val = int(item[id_key])
            if val > max_id:
                max_id = val
        except:
            continue
    return str(max_id + 1)
# Route: Dashboard page (start page)
@app.route('/')
def dashboard():
    articles = read_articles()
    trending = read_trending()
    # Featured articles: top 3 by views
    featured_articles = sorted(articles, key=lambda x: x['views'], reverse=True)[:3]
    # Trending articles for "This Week" period (default)
    trending_this_week = [t for t in trending if t['period'] == 'This Week']
    # Sort trending by view_count desc
    trending_this_week = sorted(trending_this_week, key=lambda x: x['view_count'], reverse=True)
    return render_template('dashboard.html',
                           featured_articles=featured_articles,
                           trending_articles=trending_this_week)
# Route: Article Catalog page
@app.route('/catalog', methods=['GET', 'POST'])
def article_catalog():
    articles = read_articles()
    categories = read_categories()
    search_query = ''
    selected_category = ''
    filtered_articles = articles
    if request.method == 'POST':
        search_query = request.form.get('search-input', '').strip()
        selected_category = request.form.get('category-filter', '')
        # Filter by category if selected and not empty
        if selected_category:
            filtered_articles = [a for a in filtered_articles if a['category'] == selected_category]
        # Filter by search query if provided
        if search_query:
            sq = search_query.lower()
            filtered_articles = [a for a in filtered_articles if
                                 sq in a['title'].lower() or
                                 sq in a['author'].lower() or
                                 sq in a['content'].lower()]
    else:
        # GET request: if category filter in query string
        selected_category = request.args.get('category-filter', '')
        if selected_category:
            filtered_articles = [a for a in articles if a['category'] == selected_category]
    # Sort articles by date descending
    filtered_articles = sorted(filtered_articles, key=lambda x: x['date'], reverse=True)
    return render_template('article_catalog.html',
                           articles=filtered_articles,
                           categories=categories,
                           selected_category=selected_category,
                           search_query=search_query)
# Route: Article Details page
@app.route('/article/<article_id>', methods=['GET', 'POST'])
def article_details(article_id):
    articles = read_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404
    # Increment views count on each visit
    article['views'] += 1
    write_articles(articles)
    # Handle bookmark button POST
    if request.method == 'POST':
        # Add bookmark for this article if not already bookmarked
        bookmarks = read_bookmarks()
        already_bookmarked = any(b['article_id'] == article_id for b in bookmarks)
        if not already_bookmarked:
            bookmark_id = get_next_id(bookmarks, 'bookmark_id')
            bookmarked_date = datetime.now().strftime('%Y-%m-%d')
            bookmarks.append({
                'bookmark_id': bookmark_id,
                'article_id': article['article_id'],
                'article_title': article['title'],
                'bookmarked_date': bookmarked_date
            })
            write_bookmarks(bookmarks)
        # Redirect back to article details page to avoid form resubmission
        return redirect(url_for('article_details', article_id=article_id))
    return render_template('article_details.html',
                           article=article)
# Route: Bookmarks page
@app.route('/bookmarks', methods=['GET', 'POST'])
def bookmarks():
    bookmarks = read_bookmarks()
    articles = read_articles()
    if request.method == 'POST':
        # Check if remove bookmark or read bookmark button pressed
        for key in request.form:
            if key.startswith('remove-bookmark-button-'):
                bookmark_id = key[len('remove-bookmark-button-'):]
                bookmarks = [b for b in bookmarks if b['bookmark_id'] != bookmark_id]
                write_bookmarks(bookmarks)
                return redirect(url_for('bookmarks'))
            elif key.startswith('read-bookmark-button-'):
                bookmark_id = key[len('read-bookmark-button-'):]
                bookmark = next((b for b in bookmarks if b['bookmark_id'] == bookmark_id), None)
                if bookmark:
                    return redirect(url_for('article_details', article_id=bookmark['article_id']))
        # Back to dashboard button
        if 'back-to-dashboard' in request.form:
            return redirect(url_for('dashboard'))
    # Sort bookmarks by bookmarked_date descending
    bookmarks = sorted(bookmarks, key=lambda x: x['bookmarked_date'], reverse=True)
    return render_template('bookmarks.html',
                           bookmarks=bookmarks)
# Route: Comments page
@app.route('/comments', methods=['GET', 'POST'])
def comments():
    comments = read_comments()
    articles = read_articles()
    article_titles = sorted(set(a['title'] for a in articles))
    filter_article = ''
    if request.method == 'POST':
        # Filter by article dropdown
        filter_article = request.form.get('filter-by-article', '')
        if filter_article:
            comments = [c for c in comments if c['article_title'] == filter_article]
        # Write comment button
        if 'write-comment-button' in request.form:
            return redirect(url_for('write_comment'))
        # Back to dashboard button
        if 'back-to-dashboard' in request.form:
            return redirect(url_for('dashboard'))
    else:
        # GET request: filter by query param
        filter_article = request.args.get('filter-by-article', '')
        if filter_article:
            comments = [c for c in comments if c['article_title'] == filter_article]
    # Sort comments by comment_date descending
    comments = sorted(comments, key=lambda x: x['comment_date'], reverse=True)
    return render_template('comments.html',
                           comments=comments,
                           articles=article_titles,
                           filter_article=filter_article)
# Route: Write Comment page
@app.route('/write_comment', methods=['GET', 'POST'])
def write_comment():
    articles = read_articles()
    article_choices = [(a['article_id'], a['title']) for a in articles]
    if request.method == 'POST':
        selected_article_id = request.form.get('select-article', '')
        commenter_name = request.form.get('commenter-name', '').strip()
        comment_text = request.form.get('comment-text', '').strip()
        if not selected_article_id or not commenter_name or not comment_text:
            error = "All fields are required."
            return render_template('write_comment.html',
                                   articles=article_choices,
                                   error=error,
                                   selected_article_id=selected_article_id,
                                   commenter_name=commenter_name,
                                   comment_text=comment_text)
        # Find article title by id
        article = next((a for a in articles if a['article_id'] == selected_article_id), None)
        if not article:
            error = "Selected article not found."
            return render_template('write_comment.html',
                                   articles=article_choices,
                                   error=error,
                                   selected_article_id=selected_article_id,
                                   commenter_name=commenter_name,
                                   comment_text=comment_text)
        comments = read_comments()
        comment_id = get_next_id(comments, 'comment_id')
        comment_date = datetime.now().strftime('%Y-%m-%d')
        comments.append({
            'comment_id': comment_id,
            'article_id': article['article_id'],
            'article_title': article['title'],
            'commenter_name': commenter_name,
            'comment_text': comment_text,
            'comment_date': comment_date
        })
        write_comments(comments)
        return redirect(url_for('comments'))
    return render_template('write_comment.html',
                           articles=article_choices)
# Route: Trending Articles page
@app.route('/trending', methods=['GET', 'POST'])
def trending():
    trending = read_trending()
    time_period = 'This Week'  # default
    if request.method == 'POST':
        time_period = request.form.get('time-period-filter', 'This Week')
        # Back to dashboard button
        if 'back-to-dashboard' in request.form:
            return redirect(url_for('dashboard'))
        # Check if view article button pressed
        for key in request.form:
            if key.startswith('view-article-button-'):
                article_id = key[len('view-article-button-'):]
                return redirect(url_for('article_details', article_id=article_id))
    else:
        # GET request: time period filter from query param
        time_period = request.args.get('time-period-filter', 'This Week')
    filtered_trending = [t for t in trending if t['period'] == time_period]
    filtered_trending = sorted(filtered_trending, key=lambda x: x['view_count'], reverse=True)
    # Add rank to each trending article
    for idx, t in enumerate(filtered_trending, start=1):
        t['rank'] = idx
    return render_template('trending.html',
                           trending_list=filtered_trending,
                           time_period=time_period)
# Route: Category page
@app.route('/category/<category_name>', methods=['GET', 'POST'])
def category_page(category_name):
    articles = read_articles()
    categories = read_categories()
    category_names = [c['category_name'] for c in categories]
    if category_name not in category_names:
        return "Category not found", 404
    filtered_articles = [a for a in articles if a['category'] == category_name]
    sort_by = None
    if request.method == 'POST':
        if 'sort-by-date' in request.form:
            sort_by = 'date'
        elif 'sort-by-popularity' in request.form:
            sort_by = 'popularity'
        elif 'back-to-dashboard' in request.form:
            return redirect(url_for('dashboard'))
    if sort_by == 'date':
        filtered_articles = sorted(filtered_articles, key=lambda x: x['date'], reverse=True)
    elif sort_by == 'popularity':
        filtered_articles = sorted(filtered_articles, key=lambda x: x['views'], reverse=True)
    else:
        # Default sort by date descending
        filtered_articles = sorted(filtered_articles, key=lambda x: x['date'], reverse=True)
    return render_template('category.html',
                           category_name=category_name,
                           articles=filtered_articles)
# Route: Search Results page
@app.route('/search_results', methods=['GET', 'POST'])
def search_results():
    articles = read_articles()
    search_query = ''
    results = []
    if request.method == 'POST':
        search_query = request.form.get('search-input', '').strip()
        if search_query:
            sq = search_query.lower()
            results = [a for a in articles if
                       sq in a['title'].lower() or
                       sq in a['author'].lower() or
                       sq in a['content'].lower()]
    else:
        # GET request: search query from query param
        search_query = request.args.get('q', '').strip()
        if search_query:
            sq = search_query.lower()
            results = [a for a in articles if
                       sq in a['title'].lower() or
                       sq in a['author'].lower() or
                       sq in a['content'].lower()]
    # Sort results by date descending
    results = sorted(results, key=lambda x: x['date'], reverse=True)
    no_results = (len(results) == 0)
    return render_template('search_results.html',
                           search_query=search_query,
                           results=results,
                           no_results=no_results)
# Run the app on local port 5000
if __name__ == '__main__':
    app.run(port=5000, debug=True)