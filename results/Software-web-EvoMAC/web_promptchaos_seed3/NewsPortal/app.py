'''
Main backend application for NewsPortal web application.
Handles routing, data reading/writing from/to local text files in the data/ directory,
and rendering HTML templates with appropriate data.
Implements all functionalities: article management, bookmarks, comments, trending data,
search/filter, and navigation.
No authentication; all features directly accessible.
Website starts from Dashboard page at route '/'.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
ARTICLES_FILE = os.path.join(DATA_DIR, 'articles.txt')
CATEGORIES_FILE = os.path.join(DATA_DIR, 'categories.txt')
BOOKMARKS_FILE = os.path.join(DATA_DIR, 'bookmarks.txt')
COMMENTS_FILE = os.path.join(DATA_DIR, 'comments.txt')
TRENDING_FILE = os.path.join(DATA_DIR, 'trending.txt')
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
                str(b['bookmark_id']),
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
def write_trending(trending):
    with open(TRENDING_FILE, 'w', encoding='utf-8') as f:
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
            iid = int(item[id_key])
            if iid > max_id:
                max_id = iid
        except Exception:
            continue
    return max_id + 1
# ROUTES
@app.route('/')
def dashboard():
    # Dashboard page: featured articles, trending news, quick navigation
    articles = read_articles()
    trending = read_trending()
    # Featured articles: let's pick top 3 articles by views
    featured_articles = sorted(articles, key=lambda x: x['views'], reverse=True)[:3]
    # Trending articles: filter by period "This Week" for dashboard trending display
    trending_this_week = [t for t in trending if t['period'] == 'This Week']
    trending_this_week_sorted = sorted(trending_this_week, key=lambda x: x['view_count'], reverse=True)
    return render_template('dashboard.html',
                           featured_articles=featured_articles,
                           trending_articles=trending_this_week_sorted)
@app.route('/articles')
def article_catalog():
    # Article Catalog page with search and filter
    articles = read_articles()
    categories = read_categories()
    # Get search query and category filter from query parameters
    search_query = request.args.get('search', '').strip().lower()
    category_filter = request.args.get('category', '').strip()
    filtered_articles = articles
    if category_filter:
        filtered_articles = [a for a in filtered_articles if a['category'].lower() == category_filter.lower()]
    if search_query:
        def matches_search(a):
            # Search in title, author, or content keywords
            return (search_query in a['title'].lower() or
                    search_query in a['author'].lower() or
                    search_query in a['content'].lower())
        filtered_articles = [a for a in filtered_articles if matches_search(a)]
    # Sort articles by date descending
    filtered_articles.sort(key=lambda x: x['date'], reverse=True)
    return render_template('article_catalog.html',
                           articles=filtered_articles,
                           categories=categories,
                           selected_category=category_filter,
                           search_query=search_query)
@app.route('/article/<article_id>', methods=['GET', 'POST'])
def article_details(article_id):
    # Article Details page with bookmark option
    articles = read_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404
    # Increment views count on GET request
    if request.method == 'GET':
        article['views'] += 1
        write_articles(articles)
        # Update trending data accordingly
        trending = read_trending()
        # Find trending entry for this article and period "This Week"
        period = 'This Week'
        trending_entry = next((t for t in trending if t['article_id'] == article_id and t['period'] == period), None)
        if trending_entry:
            trending_entry['view_count'] = article['views']
        else:
            trending.append({
                'article_id': article['article_id'],
                'article_title': article['title'],
                'category': article['category'],
                'view_count': article['views'],
                'period': period
            })
        write_trending(trending)
    # Check if article is bookmarked
    bookmarks = read_bookmarks()
    is_bookmarked = any(b['article_id'] == article_id for b in bookmarks)
    if request.method == 'POST':
        # Bookmark button clicked
        if not is_bookmarked:
            # Add bookmark
            bookmark_id = get_next_id(bookmarks, 'bookmark_id')
            bookmarked_date = datetime.now().strftime('%Y-%m-%d')
            bookmarks.append({
                'bookmark_id': str(bookmark_id),
                'article_id': article['article_id'],
                'article_title': article['title'],
                'bookmarked_date': bookmarked_date
            })
            write_bookmarks(bookmarks)
        return redirect(url_for('article_details', article_id=article_id))
    return render_template('article_details.html',
                           article=article,
                           is_bookmarked=is_bookmarked)
@app.route('/bookmarks', methods=['GET', 'POST'])
def bookmarks():
    # Bookmarks page with removal and reading options
    bookmarks = read_bookmarks()
    articles = read_articles()
    if request.method == 'POST':
        # Handle remove bookmark or read bookmark buttons
        action = request.form.get('action')
        bookmark_id = request.form.get('bookmark_id')
        if action == 'remove' and bookmark_id:
            bookmarks = [b for b in bookmarks if b['bookmark_id'] != bookmark_id]
            write_bookmarks(bookmarks)
            return redirect(url_for('bookmarks'))
        elif action == 'read' and bookmark_id:
            bookmark = next((b for b in bookmarks if b['bookmark_id'] == bookmark_id), None)
            if bookmark:
                return redirect(url_for('article_details', article_id=bookmark['article_id']))
    # Sort bookmarks by bookmarked_date descending
    bookmarks.sort(key=lambda x: x['bookmarked_date'], reverse=True)
    return render_template('bookmarks.html', bookmarks=bookmarks)
@app.route('/comments', methods=['GET', 'POST'])
def comments():
    # Comments page with filter by article and write comment navigation
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
    # Write Comment page
    articles = read_articles()
    if request.method == 'POST':
        article_id = request.form.get('select-article', '').strip()
        commenter_name = request.form.get('commenter-name', '').strip()
        comment_text = request.form.get('comment-text', '').strip()
        if not article_id or not commenter_name or not comment_text:
            error = "All fields are required."
            return render_template('write_comment.html', articles=articles, error=error,
                                   selected_article_id=article_id,
                                   commenter_name=commenter_name,
                                   comment_text=comment_text)
        article = next((a for a in articles if a['article_id'] == article_id), None)
        if not article:
            error = "Selected article not found."
            return render_template('write_comment.html', articles=articles, error=error,
                                   selected_article_id=article_id,
                                   commenter_name=commenter_name,
                                   comment_text=comment_text)
        comments = read_comments()
        comment_id = get_next_id(comments, 'comment_id')
        comment_date = datetime.now().strftime('%Y-%m-%d')
        comments.append({
            'comment_id': str(comment_id),
            'article_id': article_id,
            'article_title': article['title'],
            'commenter_name': commenter_name,
            'comment_text': comment_text,
            'comment_date': comment_date
        })
        write_comments(comments)
        return redirect(url_for('comments'))
    return render_template('write_comment.html', articles=articles)
@app.route('/trending', methods=['GET', 'POST'])
def trending():
    # Trending Articles page with time period filter
    trending = read_trending()
    time_period_filter = request.args.get('period', 'This Week').strip()
    valid_periods = ['Today', 'This Week', 'This Month']
    if time_period_filter not in valid_periods:
        time_period_filter = 'This Week'
    filtered_trending = [t for t in trending if t['period'] == time_period_filter]
    # Sort by view_count descending
    filtered_trending.sort(key=lambda x: x['view_count'], reverse=True)
    return render_template('trending.html',
                           trending_articles=filtered_trending,
                           selected_period=time_period_filter,
                           valid_periods=valid_periods)
@app.route('/category/<category_name>', methods=['GET', 'POST'])
def category_page(category_name):
    # Category Articles page with sorting options
    articles = read_articles()
    categories = read_categories()
    category_name_lower = category_name.lower()
    category_obj = next((c for c in categories if c['category_name'].lower() == category_name_lower), None)
    if not category_obj:
        return "Category not found", 404
    filtered_articles = [a for a in articles if a['category'].lower() == category_name_lower]
    sort_by = request.args.get('sort', 'date')  # 'date' or 'popularity'
    if sort_by == 'popularity':
        filtered_articles.sort(key=lambda x: x['views'], reverse=True)
    else:
        # Default sort by date descending
        filtered_articles.sort(key=lambda x: x['date'], reverse=True)
    return render_template('category.html',
                           category=category_obj,
                           articles=filtered_articles,
                           sort_by=sort_by)
@app.route('/search_results')
def search_results():
    # Search Results page
    query = request.args.get('q', '').strip().lower()
    articles = read_articles()
    if not query:
        # No query, show empty results
        results = []
    else:
        def matches_search(a):
            return (query in a['title'].lower() or
                    query in a['author'].lower() or
                    query in a['content'].lower())
        results = [a for a in articles if matches_search(a)]
    # Sort results by date descending
    results.sort(key=lambda x: x['date'], reverse=True)
    return render_template('search_results.html',
                           search_query=query,
                           results=results)
# Run the app on local port 5000
if __name__ == '__main__':
    app.run(port=5000, debug=True)