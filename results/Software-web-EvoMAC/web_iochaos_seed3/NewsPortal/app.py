'''
Backend application for NewsPortal web application.
Handles routing, data management, and business logic for all pages:
- Dashboard
- Article Catalog
- Article Details
- Bookmarks
- Comments
- Write Comment
- Trending Articles
- Category Articles
- Search Results
Data is stored in plain text files under the 'data' directory.
No authentication is required; all features are directly accessible.
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
# Utility functions for reading and writing data files
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
# Route: Dashboard page (start page)
@app.route('/')
def dashboard():
    articles = read_articles()
    trending = read_trending()
    # Featured articles: top 3 by views
    featured_articles = sorted(articles, key=lambda x: x['views'], reverse=True)[:3]
    # Trending articles: filter by period 'This Week' for dashboard display
    trending_this_week = [t for t in trending if t['period'] == 'This Week']
    trending_this_week_sorted = sorted(trending_this_week, key=lambda x: x['view_count'], reverse=True)[:5]
    return render_template('dashboard.html',
                           featured_articles=featured_articles,
                           trending_articles=trending_this_week_sorted)
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
        selected_category = request.form.get('category-filter', '').strip()
        # Filter by category if selected and not empty or 'All'
        if selected_category and selected_category.lower() != 'all':
            filtered_articles = [a for a in filtered_articles if a['category'].lower() == selected_category.lower()]
        # Filter by search query if provided (search in title, author, content)
        if search_query:
            sq = search_query.lower()
            filtered_articles = [a for a in filtered_articles if
                                 sq in a['title'].lower() or
                                 sq in a['author'].lower() or
                                 sq in a['content'].lower()]
    else:
        # GET request: show all articles
        filtered_articles = articles
    # Sort articles by date descending by default
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
    # Increment views count for the article
    article['views'] += 1
    write_articles(articles)
    # Update trending data for 'This Week' period (simplified: update or add)
    trending = read_trending()
    # Check if article already in trending for 'This Week'
    trending_entry = next((t for t in trending if t['article_id'] == article_id and t['period'] == 'This Week'), None)
    if trending_entry:
        trending_entry['view_count'] = article['views']
    else:
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
    if request.method == 'POST':
        # Handle bookmark button click
        if 'bookmark-button' in request.form:
            if not is_bookmarked:
                # Add bookmark
                bookmark_id = get_next_id(bookmarks, 'bookmark_id')
                bookmarked_date = datetime.now().strftime('%Y-%m-%d')
                bookmarks.append({
                    'bookmark_id': bookmark_id,
                    'article_id': article['article_id'],
                    'article_title': article['title'],
                    'bookmarked_date': bookmarked_date
                })
                write_bookmarks(bookmarks)
            else:
                # Remove bookmark
                bookmarks = [b for b in bookmarks if b['article_id'] != article_id]
                write_bookmarks(bookmarks)
            return redirect(url_for('article_details', article_id=article_id))
    return render_template('article_details.html',
                           article=article,
                           is_bookmarked=is_bookmarked)
# Route: Bookmarks page
@app.route('/bookmarks', methods=['GET', 'POST'])
def bookmarks():
    bookmarks = read_bookmarks()
    articles = read_articles()
    if request.method == 'POST':
        # Remove bookmark
        for key in request.form:
            if key.startswith('remove-bookmark-button-'):
                bookmark_id = key[len('remove-bookmark-button-'):]
                bookmarks = [b for b in bookmarks if b['bookmark_id'] != bookmark_id]
                write_bookmarks(bookmarks)
                break
            elif key.startswith('read-bookmark-button-'):
                bookmark_id = key[len('read-bookmark-button-'):]
                bookmark = next((b for b in bookmarks if b['bookmark_id'] == bookmark_id), None)
                if bookmark:
                    return redirect(url_for('article_details', article_id=bookmark['article_id']))
        # Back to dashboard
        if 'back-to-dashboard' in request.form:
            return redirect(url_for('dashboard'))
    # Sort bookmarks by bookmarked_date descending
    bookmarks_sorted = sorted(bookmarks, key=lambda x: x['bookmarked_date'], reverse=True)
    return render_template('bookmarks.html', bookmarks=bookmarks_sorted)
# Route: Comments page
@app.route('/comments', methods=['GET', 'POST'])
def comments():
    comments = read_comments()
    articles = read_articles()
    article_titles = sorted(set(a['title'] for a in articles))
    filter_article = request.args.get('filter-by-article', '')
    filtered_comments = comments
    if filter_article:
        filtered_comments = [c for c in comments if c['article_title'] == filter_article]
    if request.method == 'POST':
        if 'write-comment-button' in request.form:
            return redirect(url_for('write_comment'))
        if 'back-to-dashboard' in request.form:
            return redirect(url_for('dashboard'))
    # Sort comments by comment_date descending
    filtered_comments = sorted(filtered_comments, key=lambda x: x['comment_date'], reverse=True)
    return render_template('comments.html',
                           comments=filtered_comments,
                           articles=article_titles,
                           selected_article=filter_article)
# Route: Write Comment page
@app.route('/write_comment', methods=['GET', 'POST'])
def write_comment():
    articles = read_articles()
    article_choices = [(a['article_id'], a['title']) for a in articles]
    if request.method == 'POST':
        article_id = request.form.get('select-article', '').strip()
        commenter_name = request.form.get('commenter-name', '').strip()
        comment_text = request.form.get('comment-text', '').strip()
        if not article_id or not commenter_name or not comment_text:
            error = "All fields are required."
            return render_template('write_comment.html', articles=article_choices, error=error,
                                   selected_article=article_id,
                                   commenter_name=commenter_name,
                                   comment_text=comment_text)
        # Find article title by article_id
        article = next((a for a in articles if a['article_id'] == article_id), None)
        if not article:
            error = "Selected article not found."
            return render_template('write_comment.html', articles=article_choices, error=error,
                                   selected_article=article_id,
                                   commenter_name=commenter_name,
                                   comment_text=comment_text)
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
    return render_template('write_comment.html', articles=article_choices)
# Route: Trending Articles page
@app.route('/trending', methods=['GET', 'POST'])
def trending():
    trending = read_trending()
    time_period_filter = request.args.get('time-period-filter', 'This Week')
    if request.method == 'POST':
        # Back to dashboard
        if 'back-to-dashboard' in request.form:
            return redirect(url_for('dashboard'))
        # View article buttons
        for key in request.form:
            if key.startswith('view-article-button-'):
                article_id = key[len('view-article-button-'):]
                return redirect(url_for('article_details', article_id=article_id))
    # Filter trending by time period
    filtered_trending = [t for t in trending if t['period'] == time_period_filter]
    # Sort by view_count descending
    filtered_trending = sorted(filtered_trending, key=lambda x: x['view_count'], reverse=True)
    # Add rank
    for idx, item in enumerate(filtered_trending, start=1):
        item['rank'] = idx
    return render_template('trending.html',
                           trending_list=filtered_trending,
                           time_period_filter=time_period_filter)
# Route: Category Articles page
@app.route('/category/<category_name>', methods=['GET', 'POST'])
def category_page(category_name):
    articles = read_articles()
    category_name_lower = category_name.lower()
    filtered_articles = [a for a in articles if a['category'].lower() == category_name_lower]
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
                           category_title=category_name,
                           category_articles=filtered_articles)
# Route: Search Results page
@app.route('/search_results', methods=['GET', 'POST'])
def search_results():
    query = request.args.get('q', '').strip()
    articles = read_articles()
    results = []
    if query:
        q = query.lower()
        for a in articles:
            if q in a['title'].lower() or q in a['author'].lower() or q in a['content'].lower():
                # Provide excerpt: first 100 chars of content
                excerpt = a['content'][:100] + ('...' if len(a['content']) > 100 else '')
                results.append({
                    'article_id': a['article_id'],
                    'title': a['title'],
                    'excerpt': excerpt
                })
    if request.method == 'POST':
        if 'back-to-dashboard' in request.form:
            return redirect(url_for('dashboard'))
        # View article buttons
        for key in request.form:
            if key.startswith('view-article-button-'):
                article_id = key[len('view-article-button-'):]
                return redirect(url_for('article_details', article_id=article_id))
    return render_template('search_results.html',
                           search_query=query,
                           results_list=results,
                           no_results_message="No results found." if not results else "")
# Run the app on local port 5000
if __name__ == '__main__':
    app.run(port=5000, debug=True)