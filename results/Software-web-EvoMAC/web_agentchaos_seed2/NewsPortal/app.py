'''
Main backend Python application file for NewsPortal web application.
Handles routing for all nine pages, processes data from local text files in the `data/` directory,
manages reading and writing operations for articles, bookmarks, comments, and trending data,
and serves the HTML templates with the appropriate data.
No authentication required; all features directly accessible.
Website accessible via local port 5000, starting at route '/' (Dashboard page).
'''
import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
ARTICLES_FILE = os.path.join(DATA_DIR, 'articles.txt')
CATEGORIES_FILE = os.path.join(DATA_DIR, 'categories.txt')
BOOKMARKS_FILE = os.path.join(DATA_DIR, 'bookmarks.txt')
COMMENTS_FILE = os.path.join(DATA_DIR, 'comments.txt')
TRENDING_FILE = os.path.join(DATA_DIR, 'trending.txt')
# Utility functions to read and write data files
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
            current_id = int(item[id_key])
            if current_id > max_id:
                max_id = current_id
        except Exception:
            continue
    return max_id + 1
# ROUTES
@app.route('/')
def dashboard():
    # Dashboard page: featured articles, trending news, quick navigation
    articles = read_articles()
    trending = read_trending()
    # Featured articles: let's pick top 3 articles by views as featured
    featured_articles = sorted(articles, key=lambda x: x['views'], reverse=True)[:3]
    # Trending articles for dashboard: top 3 trending articles for "This Week" period
    trending_this_week = [t for t in trending if t['period'] == 'This Week']
    trending_articles = sorted(trending_this_week, key=lambda x: x['view_count'], reverse=True)[:3]
    return render_template('dashboard.html',
                           featured_articles=featured_articles,
                           trending_articles=trending_articles)
@app.route('/articles')
def article_catalog():
    # Article Catalog page: all articles with search and filter
    articles = read_articles()
    categories = read_categories()
    # Get query parameters for search and category filter
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()
    filtered_articles = articles
    if search_query:
        search_query_lower = search_query.lower()
        filtered_articles = [a for a in filtered_articles if
                             search_query_lower in a['title'].lower() or
                             search_query_lower in a['author'].lower() or
                             search_query_lower in a['content'].lower()]
    if category_filter and category_filter != 'All':
        filtered_articles = [a for a in filtered_articles if a['category'] == category_filter]
    # Sort articles by date descending by default
    filtered_articles.sort(key=lambda x: x['date'], reverse=True)
    # Ensure 'All' is selected if no category_filter provided
    selected_category = category_filter if category_filter else 'All'
    return render_template('article_catalog.html',
                           articles=filtered_articles,
                           categories=categories,
                           selected_category=selected_category,
                           search_query=search_query)
@app.route('/article/<article_id>')
def article_details(article_id):
    # Article Details page: detailed info about a specific article
    articles = read_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404
    # Increment view count for the article
    article['views'] += 1
    write_articles(articles)
    # Update trending data accordingly (simplified: update or add for "This Week")
    trending = read_trending()
    found = False
    for t in trending:
        if t['article_id'] == article_id and t['period'] == 'This Week':
            t['view_count'] = article['views']
            found = True
            break
    if not found:
        trending.append({
            'article_id': article['article_id'],
            'article_title': article['title'],
            'category': article['category'],
            'view_count': article['views'],
            'period': 'This Week'
        })
    write_trending(trending)
    # Check if article is bookmarked
    bookmarks = read_bookmarks()
    is_bookmarked = any(b['article_id'] == article_id for b in bookmarks)
    return render_template('article_details.html',
                           article=article,
                           is_bookmarked=is_bookmarked)
@app.route('/bookmark/<article_id>', methods=['POST'])
def bookmark_article(article_id):
    # Add bookmark for the article
    articles = read_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404
    bookmarks = read_bookmarks()
    # Check if already bookmarked
    if any(b['article_id'] == article_id for b in bookmarks):
        # Already bookmarked, do nothing or redirect
        return redirect(url_for('article_details', article_id=article_id))
    new_id = get_next_id(bookmarks, 'bookmark_id')
    bookmarked_date = datetime.now().strftime('%Y-%m-%d')
    bookmarks.append({
        'bookmark_id': str(new_id),
        'article_id': article['article_id'],
        'article_title': article['title'],
        'bookmarked_date': bookmarked_date
    })
    write_bookmarks(bookmarks)
    return redirect(url_for('article_details', article_id=article_id))
@app.route('/bookmarks')
def bookmarks_page():
    # Bookmarks page: display all bookmarked articles with removal and reading options
    bookmarks = read_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)
@app.route('/bookmark/remove/<bookmark_id>', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = read_bookmarks()
    bookmarks = [b for b in bookmarks if b['bookmark_id'] != bookmark_id]
    write_bookmarks(bookmarks)
    return redirect(url_for('bookmarks_page'))
@app.route('/bookmark/read/<bookmark_id>')
def read_bookmarked_article(bookmark_id):
    bookmarks = read_bookmarks()
    bookmark = next((b for b in bookmarks if b['bookmark_id'] == bookmark_id), None)
    if not bookmark:
        return "Bookmark not found", 404
    return redirect(url_for('article_details', article_id=bookmark['article_id']))
@app.route('/comments')
def comments_page():
    # Comments page: display all comments and allow filtering by article
    comments = read_comments()
    articles = read_articles()
    filter_article_id = request.args.get('article_id', '').strip()
    if filter_article_id:
        comments = [c for c in comments if c['article_id'] == filter_article_id]
    return render_template('comments.html',
                           comments=comments,
                           articles=articles,
                           selected_article_id=filter_article_id)
@app.route('/comments/write', methods=['GET', 'POST'])
def write_comment():
    articles = read_articles()
    if request.method == 'POST':
        article_id = request.form.get('select-article', '').strip()
        commenter_name = request.form.get('commenter-name', '').strip()
        comment_text = request.form.get('comment-text', '').strip()
        if not article_id or not commenter_name or not comment_text:
            # Missing fields, re-render with error message
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
            'comment_id': str(new_id),
            'article_id': article_id,
            'article_title': article['title'],
            'commenter_name': commenter_name,
            'comment_text': comment_text,
            'comment_date': comment_date
        })
        write_comments(comments)
        return redirect(url_for('comments_page'))
    # GET request
    return render_template('write_comment.html', articles=articles)
@app.route('/trending')
def trending_page():
    # Trending Articles page: top trending articles ranked by views and engagement
    trending = read_trending()
    time_period_filter = request.args.get('period', 'This Week')
    filtered_trending = [t for t in trending if t['period'] == time_period_filter]
    # Sort by view_count descending
    filtered_trending.sort(key=lambda x: x['view_count'], reverse=True)
    return render_template('trending.html',
                           trending_list=filtered_trending,
                           time_period_filter=time_period_filter)
@app.route('/category/<category_name>')
def category_page(category_name):
    # Category Articles page: display articles from a specific category
    articles = read_articles()
    category_name = category_name.strip()
    category_articles = [a for a in articles if a['category'].lower() == category_name.lower()]
    # Sorting options
    sort_by = request.args.get('sort', 'date')  # 'date' or 'popularity'
    if sort_by == 'popularity':
        category_articles.sort(key=lambda x: x['views'], reverse=True)
    else:
        # Default sort by date descending
        category_articles.sort(key=lambda x: x['date'], reverse=True)
    return render_template('category.html',
                           category_title=category_name,
                           category_articles=category_articles,
                           sort_by=sort_by)
@app.route('/search')
def search_results():
    # Search Results page: display search results based on user query
    query = request.args.get('q', '').strip()
    articles = read_articles()
    if not query:
        # No query, show empty results
        results = []
    else:
        q_lower = query.lower()
        results = [a for a in articles if
                   q_lower in a['title'].lower() or
                   q_lower in a['author'].lower() or
                   q_lower in a['content'].lower()]
    return render_template('search_results.html',
                           search_query=query,
                           results=results)
# Navigation helper routes for buttons that go back to dashboard
@app.route('/back-to-dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard'))
if __name__ == '__main__':
    app.run(port=5000, debug=True)