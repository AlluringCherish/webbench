from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__, template_folder='templates_candidate_a')
app.secret_key = 'newsportal_secret_key'

DATA_DIR = 'data'

# Helper functions to read and write files

def read_articles():
    articles = []
    path = os.path.join(DATA_DIR, 'articles.txt')
    if not os.path.exists(path):
        return articles
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = [p.strip() for p in line.strip().split('|')]
            if len(parts) >= 7:
                article_id, title, author, category, content, date, views = parts
                articles.append({
                    'article_id': int(article_id),
                    'title': title,
                    'author': author,
                    'category': category,
                    'content': content,
                    'date': date,
                    'views': int(views)
                })
    return articles


def read_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    if not os.path.exists(path):
        return categories
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = [p.strip() for p in line.strip().split('|')]
            if len(parts) >= 3:
                category_id, category_name, description = parts
                categories.append({
                    'category_id': int(category_id),
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
            parts = [p.strip() for p in line.strip().split('|')]
            if len(parts) >= 4:
                bookmark_id, article_id, article_title, bookmarked_date = parts
                bookmarks.append({
                    'bookmark_id': int(bookmark_id),
                    'article_id': int(article_id),
                    'article_title': article_title,
                    'bookmarked_date': bookmarked_date
                })
    return bookmarks


def write_bookmarks(bookmarks):
    path = os.path.join(DATA_DIR, 'bookmarks.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for bm in bookmarks:
            line = f"{bm['bookmark_id']}|{bm['article_id']}|{bm['article_title']}|{bm['bookmarked_date']}\n"
            f.write(line)


def read_comments():
    comments = []
    path = os.path.join(DATA_DIR, 'comments.txt')
    if not os.path.exists(path):
        return comments
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = [p.strip() for p in line.strip().split('|')]
            if len(parts) >= 6:
                comment_id, article_id, article_title, commenter_name, comment_text, comment_date = parts
                comments.append({
                    'comment_id': int(comment_id),
                    'article_id': int(article_id),
                    'article_title': article_title,
                    'commenter_name': commenter_name,
                    'comment_text': comment_text,
                    'comment_date': comment_date
                })
    return comments


def write_comments(comments):
    path = os.path.join(DATA_DIR, 'comments.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for cm in comments:
            line = f"{cm['comment_id']}|{cm['article_id']}|{cm['article_title']}|{cm['commenter_name']}|{cm['comment_text']}|{cm['comment_date']}\n"
            f.write(line)


def read_trending():
    trending = []
    path = os.path.join(DATA_DIR, 'trending.txt')
    if not os.path.exists(path):
        return trending
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = [p.strip() for p in line.strip().split('|')]
            if len(parts) >= 5:
                article_id, article_title, category, view_count, period = parts
                trending.append({
                    'article_id': int(article_id),
                    'article_title': article_title,
                    'category': category,
                    'view_count': int(view_count),
                    'period': period
                })
    return trending


# Utility functions

def get_next_bookmark_id(bookmarks):
    if not bookmarks:
        return 1
    else:
        return max(b['bookmark_id'] for b in bookmarks) + 1

def get_next_comment_id(comments):
    if not comments:
        return 1
    else:
        return max(c['comment_id'] for c in comments) + 1


def find_article_by_id(article_id):
    articles = read_articles()
    for art in articles:
        if art['article_id'] == article_id:
            return art
    return None


def find_bookmark_by_id(bookmark_id):
    bookmarks = read_bookmarks()
    for bm in bookmarks:
        if bm['bookmark_id'] == bookmark_id:
            return bm
    return None


# Routes

@app.route('/')
def dashboard_page():
    # Show featured articles: top 3 by views
    articles = read_articles()
    featured_articles = sorted(articles, key=lambda x: x['views'], reverse=True)[:3]
    return render_template('dashboard.html', page_title='News Portal', featured_articles=featured_articles)


@app.route('/catalog')
def article_catalog():
    articles = read_articles()
    categories = read_categories()

    # Get search and category filter
    search_query = request.args.get('search', '').strip().lower()
    filter_category = request.args.get('category', '')

    filtered_articles = articles

    if filter_category:
        filtered_articles = [a for a in filtered_articles if a['category'].lower() == filter_category.lower()]

    if search_query:
        filtered_articles = [a for a in filtered_articles if search_query in a['title'].lower() or
                             search_query in a['author'].lower() or
                             search_query in a['content'].lower()]

    return render_template('catalog.html', page_title='Article Catalog', articles=filtered_articles, categories=categories, 
                           search_query=search_query, filter_category=filter_category)


@app.route('/article/<int:article_id>')
def article_details(article_id):
    article = find_article_by_id(article_id)
    if not article:
        flash('Article not found', 'error')
        return redirect(url_for('dashboard_page'))
    
    # For bookmarking button
    bookmarks = read_bookmarks()
    already_bookmarked = any(bm['article_id'] == article_id for bm in bookmarks)

    return render_template('article_details.html', page_title='Article Details', article=article, already_bookmarked=already_bookmarked)


@app.route('/bookmarks')
def bookmarks_page():
    bookmarks = read_bookmarks()
    return render_template('bookmarks.html', page_title='My Bookmarks', bookmarks=bookmarks)


@app.route('/bookmarks/remove/<int:bookmark_id>', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = read_bookmarks()
    new_bookmarks = [bm for bm in bookmarks if bm['bookmark_id'] != bookmark_id]
    if len(new_bookmarks) == len(bookmarks):
        flash('Bookmark not found', 'error')
    else:
        write_bookmarks(new_bookmarks)
        flash('Bookmark removed successfully', 'success')
    return redirect(url_for('bookmarks_page'))


@app.route('/bookmarks/add/<int:article_id>', methods=['POST'])
def add_bookmark(article_id):
    article = find_article_by_id(article_id)
    if not article:
        flash('Article not found to bookmark', 'error')
        return redirect(url_for('dashboard_page'))

    bookmarks = read_bookmarks()
    # Check already bookmarked
    if any(bm['article_id'] == article_id for bm in bookmarks):
        flash('Article already bookmarked', 'info')
        return redirect(url_for('article_details', article_id=article_id))

    bookmark_id = get_next_bookmark_id(bookmarks)
    bookmarked_date = datetime.now().strftime('%Y-%m-%d')
    bookmarks.append({
        'bookmark_id': bookmark_id,
        'article_id': article_id,
        'article_title': article['title'],
        'bookmarked_date': bookmarked_date
    })
    write_bookmarks(bookmarks)
    flash('Article bookmarked successfully', 'success')
    return redirect(url_for('article_details', article_id=article_id))


@app.route('/comments')
def comments_page():
    comments = read_comments()
    articles = read_articles()
    filter_article_id = request.args.get('article_id', type=int)

    filtered_comments = comments
    if filter_article_id:
        filtered_comments = [c for c in filtered_comments if c['article_id'] == filter_article_id]

    return render_template('comments.html', page_title='Article Comments', comments=filtered_comments, articles=articles, filter_article_id=filter_article_id)


@app.route('/write-comment', methods=['GET'])
def write_comment_page_get():
    articles = read_articles()
    return render_template('write_comment.html', page_title='Write a Comment', articles=articles)


@app.route('/write-comment', methods=['POST'])
def write_comment_page_post():
    article_id = request.form.get('select-article')
    commenter_name = request.form.get('commenter-name', '').strip()
    comment_text = request.form.get('comment-text', '').strip()

    if not article_id or not commenter_name or not comment_text:
        flash('All fields are required', 'error')
        return redirect(url_for('write_comment_page_get'))

    try:
        article_id = int(article_id)
    except ValueError:
        flash('Invalid article selection', 'error')
        return redirect(url_for('write_comment_page_get'))

    article = find_article_by_id(article_id)
    if not article:
        flash('Selected article does not exist', 'error')
        return redirect(url_for('write_comment_page_get'))

    comments = read_comments()
    comment_id = get_next_comment_id(comments)
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
    flash('Comment submitted successfully', 'success')
    return redirect(url_for('comments_page'))


@app.route('/trending')
def trending_page():
    trending_all = read_trending()
    period_filter = request.args.get('period', 'This Week')

    filtered_trending = [t for t in trending_all if t['period'].lower() == period_filter.lower()]
    # Sort by view_count descending
    filtered_trending.sort(key=lambda x: x['view_count'], reverse=True)

    return render_template('trending.html', page_title='Trending Articles', trending=filtered_trending, period_filter=period_filter)


@app.route('/category/<string:category_name>')
def category_page(category_name):
    articles = read_articles()
    sort_param = request.args.get('sort', 'date')

    category_articles = [a for a in articles if a['category'].lower() == category_name.lower()]

    if sort_param == 'date':
        category_articles.sort(key=lambda x: x['date'], reverse=True)
    elif sort_param == 'popularity':
        category_articles.sort(key=lambda x: x['views'], reverse=True)

    return render_template('category.html', page_title='Category Articles', category_name=category_name, articles=category_articles, sort_param=sort_param)


@app.route('/search')
def search_results():
    query = request.args.get('query', '').strip()
    articles = read_articles()
    results = []
    if query:
        q_lower = query.lower()
        for a in articles:
            if q_lower in a['title'].lower() or q_lower in a['content'].lower() or q_lower in a['author'].lower():
                excerpt = (a['content'][:100] + '...') if len(a['content']) > 100 else a['content']
                results.append({
                    'article_id': a['article_id'],
                    'title': a['title'],
                    'excerpt': excerpt
                })

    return render_template('search_results.html', page_title='Search Results', query=query, results=results)


if __name__ == '__main__':
    app.run(debug=True)
