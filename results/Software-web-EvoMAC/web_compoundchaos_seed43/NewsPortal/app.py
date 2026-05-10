'''
Main application file for NewsPortal web application.
Implements all required pages and functionalities using Flask.
Data is managed through local text files in the 'data' directory.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
ARTICLES_FILE = os.path.join(DATA_DIR, 'articles.txt')
CATEGORIES_FILE = os.path.join(DATA_DIR, 'categories.txt')
BOOKMARKS_FILE = os.path.join(DATA_DIR, 'bookmarks.txt')
COMMENTS_FILE = os.path.join(DATA_DIR, 'comments.txt')
TRENDING_FILE = os.path.join(DATA_DIR, 'trending.txt')
# Utility functions to read and write data
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
            article = {
                'article_id': parts[0],
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
            category = {
                'category_id': parts[0],
                'category_name': parts[1],
                'description': parts[2]
            }
            categories.append(category)
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
            bookmark = {
                'bookmark_id': parts[0],
                'article_id': parts[1],
                'article_title': parts[2],
                'bookmarked_date': parts[3]
            }
            bookmarks.append(bookmark)
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
            comment = {
                'comment_id': parts[0],
                'article_id': parts[1],
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
            item = {
                'article_id': parts[0],
                'article_title': parts[1],
                'category': parts[2],
                'view_count': int(parts[3]),
                'period': parts[4]
            }
            trending.append(item)
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
            val = int(item[id_key])
            if val > max_id:
                max_id = val
        except:
            continue
    return str(max_id + 1)
# Routes
@app.route('/')
def dashboard():
    articles = read_articles()
    trending = read_trending()
    # Featured articles: top 3 by views
    featured_articles = sorted(articles, key=lambda x: x['views'], reverse=True)[:3]
    return render_template('dashboard.html',
                           featured_articles=featured_articles,
                           trending=trending)
@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    articles = read_articles()
    categories = read_categories()
    search_query = ''
    selected_category = ''
    filtered_articles = articles
    if request.method == 'POST':
        search_query = request.form.get('search-input', '').strip()
        selected_category = request.form.get('category-filter', '')
        # Filter by category if selected
        if selected_category and selected_category != 'All':
            filtered_articles = [a for a in filtered_articles if a['category'] == selected_category]
        # Search by title, author, or keywords in content
        if search_query:
            sq = search_query.lower()
            filtered_articles = [a for a in filtered_articles if
                                 sq in a['title'].lower() or
                                 sq in a['author'].lower() or
                                 sq in a['content'].lower()]
    else:
        # GET request: show all articles
        filtered_articles = articles
    return render_template('catalog.html',
                           articles=filtered_articles,
                           categories=categories,
                           selected_category=selected_category,
                           search_query=search_query)
@app.route('/article/<article_id>')
def article_details(article_id):
    articles = read_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404
    # Increment views count
    article['views'] += 1
    write_articles(articles)
    return render_template('article_details.html', article=article)
@app.route('/bookmark/<article_id>', methods=['POST'])
def bookmark_article(article_id):
    articles = read_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404
    bookmarks = read_bookmarks()
    # Check if already bookmarked
    for b in bookmarks:
        if b['article_id'] == article_id:
            # Already bookmarked
            return redirect(url_for('bookmarks'))
    bookmark_id = get_next_id(bookmarks, 'bookmark_id')
    bookmarked_date = datetime.now().strftime('%Y-%m-%d')
    bookmarks.append({
        'bookmark_id': bookmark_id,
        'article_id': article_id,
        'article_title': article['title'],
        'bookmarked_date': bookmarked_date
    })
    write_bookmarks(bookmarks)
    return redirect(url_for('bookmarks'))
@app.route('/bookmarks')
def bookmarks():
    bookmarks = read_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)
@app.route('/remove_bookmark/<bookmark_id>', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = read_bookmarks()
    bookmarks = [b for b in bookmarks if b['bookmark_id'] != bookmark_id]
    write_bookmarks(bookmarks)
    return redirect(url_for('bookmarks'))
@app.route('/read_bookmark/<bookmark_id>')
def read_bookmark(bookmark_id):
    bookmarks = read_bookmarks()
    bookmark = next((b for b in bookmarks if b['bookmark_id'] == bookmark_id), None)
    if not bookmark:
        return "Bookmark not found", 404
    return redirect(url_for('article_details', article_id=bookmark['article_id']))
@app.route('/comments', methods=['GET', 'POST'])
def comments():
    comments = read_comments()
    articles = read_articles()
    filter_article = request.args.get('filter-by-article', '')
    filtered_comments = comments
    if filter_article:
        filtered_comments = [c for c in comments if c['article_id'] == filter_article]
    return render_template('comments.html',
                           comments=filtered_comments,
                           articles=articles,
                           selected_article=filter_article)
@app.route('/write_comment', methods=['GET', 'POST'])
def write_comment():
    articles = read_articles()
    if request.method == 'POST':
        article_id = request.form.get('select-article', '')
        commenter_name = request.form.get('commenter-name', '').strip()
        comment_text = request.form.get('comment-text', '').strip()
        if not article_id or not commenter_name or not comment_text:
            error = "All fields are required."
            return render_template('write_comment.html', articles=articles, error=error,
                                   selected_article=article_id,
                                   commenter_name=commenter_name,
                                   comment_text=comment_text)
        article = next((a for a in articles if a['article_id'] == article_id), None)
        if not article:
            error = "Selected article not found."
            return render_template('write_comment.html', articles=articles, error=error)
        comments = read_comments()
        comment_id = get_next_id(comments, 'comment_id')
        comment_date = datetime.now().strftime('%Y-%m-%d')
        comments.append({
            'comment_id': comment_id,
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
    trending = read_trending()
    time_period = request.args.get('time-period-filter', 'This Week')
    filtered_trending = [t for t in trending if t['period'] == time_period]
    # Sort by view_count descending
    filtered_trending = sorted(filtered_trending, key=lambda x: x['view_count'], reverse=True)
    return render_template('trending.html',
                           trending=filtered_trending,
                           time_period=time_period)
@app.route('/category/<category_name>', methods=['GET', 'POST'])
def category_page(category_name):
    articles = read_articles()
    filtered_articles = [a for a in articles if a['category'].lower() == category_name.lower()]
    sort_by = request.args.get('sort', 'date')  # 'date' or 'popularity'
    if sort_by == 'date':
        filtered_articles = sorted(filtered_articles, key=lambda x: x['date'], reverse=True)
    elif sort_by == 'popularity':
        filtered_articles = sorted(filtered_articles, key=lambda x: x['views'], reverse=True)
    return render_template('category.html',
                           category_name=category_name,
                           articles=filtered_articles,
                           sort_by=sort_by)
@app.route('/search_results', methods=['GET'])
def search_results():
    query = request.args.get('q', '').strip()
    articles = read_articles()
    results = []
    if query:
        q = query.lower()
        for a in articles:
            if q in a['title'].lower() or q in a['author'].lower() or q in a['content'].lower():
                excerpt = a['content'][:150] + ('...' if len(a['content']) > 150 else '')
                results.append({
                    'article_id': a['article_id'],
                    'title': a['title'],
                    'excerpt': excerpt
                })
    return render_template('search_results.html',
                           query=query,
                           results=results)
# Navigation routes for buttons on dashboard and other pages
@app.route('/go_to_catalog', methods=['POST'])
def go_to_catalog():
    return redirect(url_for('catalog'))
@app.route('/go_to_bookmarks', methods=['POST'])
def go_to_bookmarks():
    return redirect(url_for('bookmarks'))
@app.route('/go_to_trending', methods=['POST'])
def go_to_trending():
    return redirect(url_for('trending'))
@app.route('/back_to_dashboard', methods=['POST'])
def back_to_dashboard():
    return redirect(url_for('dashboard'))
if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)