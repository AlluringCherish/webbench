from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__, template_folder='templates_candidate_b')
app.secret_key = 'newsportal_secret_key'

DATA_DIR = 'data'

# Helper functions for reading files

def read_articles():
    articles = []
    path = os.path.join(DATA_DIR, 'articles.txt')
    if not os.path.exists(path):
        return articles
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 7:
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
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 3:
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
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 4:
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
        for b in bookmarks:
            line = f"{b['bookmark_id']}|{b['article_id']}|{b['article_title']}|{b['bookmarked_date']}"
            f.write(line + '\n')


def read_comments():
    comments = []
    path = os.path.join(DATA_DIR, 'comments.txt')
    if not os.path.exists(path):
        return comments
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 6:
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
        for c in comments:
            line = f"{c['comment_id']}|{c['article_id']}|{c['article_title']}|{c['commenter_name']}|{c['comment_text']}|{c['comment_date']}"
            f.write(line + '\n')


def read_trending():
    trending = []
    path = os.path.join(DATA_DIR, 'trending.txt')
    if not os.path.exists(path):
        return trending
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 5:
                    article_id, article_title, category, view_count, period = parts
                    trending.append({
                        'article_id': int(article_id),
                        'article_title': article_title,
                        'category': category,
                        'view_count': int(view_count),
                        'period': period
                    })
    return trending

# Util: find article by id

def find_article(articles, article_id):
    for a in articles:
        if a['article_id'] == article_id:
            return a
    return None

# Util: find bookmark by bookmark_id

def find_bookmark(bookmarks, bookmark_id):
    for b in bookmarks:
        if b['bookmark_id'] == bookmark_id:
            return b
    return None


# Route Implementations

@app.route('/')
def dashboard_page():
    articles = read_articles()
    trending = read_trending()

    # For featured articles we pick top 3 by views
    featured_articles = sorted(articles, key=lambda x: x['views'], reverse=True)[:3]

    return render_template('dashboard.html', page_title='News Portal', featured_articles=featured_articles)


@app.route('/catalog')
def article_catalog():
    articles = read_articles()
    categories = read_categories()

    query = request.args.get('q', '').strip().lower()
    category_filter = request.args.get('category', '').strip()

    filtered_articles = articles

    if query:
        filtered_articles = [a for a in filtered_articles if 
                             query in a['title'].lower() or
                             query in a['author'].lower() or
                             query in a['content'].lower()]

    if category_filter:
        filtered_articles = [a for a in filtered_articles if a['category'].lower() == category_filter.lower()]

    return render_template('catalog.html', page_title='Article Catalog',
                           articles=filtered_articles, categories=categories,
                           selected_category=category_filter, search_query=query)


@app.route('/article/<int:article_id>')
def article_details(article_id):
    articles = read_articles()
    article = find_article(articles, article_id)
    if not article:
        flash('Article not found', 'error')
        return redirect(url_for('dashboard_page'))

    # Increase view count for this article
    article['views'] += 1
    # Write back updated views
    # Must update articles.txt
    try:
        path = os.path.join(DATA_DIR, 'articles.txt')
        lines = []
        for a in articles:
            line = f"{a['article_id']}|{a['title']}|{a['author']}|{a['category']}|{a['content']}|{a['date']}|{a['views']}"
            lines.append(line)
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')
    except Exception as e:
        flash('Failed to update article views', 'error')

    # Read bookmarks to check if bookmarked
    bookmarks = read_bookmarks()
    is_bookmarked = any(b['article_id'] == article_id for b in bookmarks)

    return render_template('article_details.html', page_title='Article Details', article=article, is_bookmarked=is_bookmarked)


@app.route('/bookmarks')
def bookmarks_page():
    bookmarks = read_bookmarks()
    return render_template('bookmarks.html', page_title='My Bookmarks', bookmarks=bookmarks)


@app.route('/bookmarks/remove/<int:bookmark_id>', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = read_bookmarks()
    bookmark = find_bookmark(bookmarks, bookmark_id)
    if bookmark:
        bookmarks = [b for b in bookmarks if b['bookmark_id'] != bookmark_id]
        write_bookmarks(bookmarks)
        flash('Bookmark removed successfully', 'success')
    else:
        flash('Bookmark not found', 'error')
    return redirect(url_for('bookmarks_page'))


@app.route('/comments')
def comments_page():
    comments = read_comments()
    articles = read_articles()
    categories = read_categories()

    filter_article_id = request.args.get('article_id')
    if filter_article_id:
        try:
            filter_article_id = int(filter_article_id)
            comments = [c for c in comments if c['article_id'] == filter_article_id]
        except ValueError:
            pass

    return render_template('comments.html', page_title='Article Comments',
                           comments=comments, articles=articles)


@app.route('/write-comment', methods=['GET'])
def write_comment_page_get():
    articles = read_articles()
    return render_template('write_comment.html', page_title='Write a Comment', articles=articles)


@app.route('/write-comment', methods=['POST'])
def write_comment_page_post():
    articles = read_articles()
    
    article_id_str = request.form.get('select-article')
    commenter_name = request.form.get('commenter-name', '').strip()
    comment_text = request.form.get('comment-text', '').strip()

    if not article_id_str or not commenter_name or not comment_text:
        flash('All fields are required.', 'error')
        return redirect(url_for('write_comment_page_get'))

    try:
        article_id = int(article_id_str)
    except ValueError:
        flash('Invalid article selected.', 'error')
        return redirect(url_for('write_comment_page_get'))

    article = find_article(articles, article_id)
    if not article:
        flash('Selected article not found.', 'error')
        return redirect(url_for('write_comment_page_get'))

    comments = read_comments()
    new_comment_id = max([c['comment_id'] for c in comments], default=0) + 1
    new_comment_date = datetime.now().strftime('%Y-%m-%d')

    new_comment = {
        'comment_id': new_comment_id,
        'article_id': article_id,
        'article_title': article['title'],
        'commenter_name': commenter_name,
        'comment_text': comment_text,
        'comment_date': new_comment_date
    }

    comments.append(new_comment)

    try:
        write_comments(comments)
        flash('Comment submitted successfully.', 'success')
        return redirect(url_for('comments_page'))
    except Exception as e:
        flash('Failed to save comment.', 'error')
        return redirect(url_for('write_comment_page_get'))


@app.route('/trending')
def trending_page():
    trending = read_trending()
    time_period = request.args.get('period', 'This Week')

    filtered_trending = [t for t in trending if t['period'].lower() == time_period.lower()]

    # Sort by view_count descending
    filtered_trending.sort(key=lambda x: x['view_count'], reverse=True)

    return render_template('trending.html', page_title='Trending Articles', trending=filtered_trending, time_period=time_period)


@app.route('/category/<string:category_name>')
def category_page(category_name):
    articles = read_articles()
    category_name_lower = category_name.lower()
    filtered_articles = [a for a in articles if a['category'].lower() == category_name_lower]

    sort_key = request.args.get('sort')
    if sort_key == 'date':
        filtered_articles.sort(key=lambda x: x['date'], reverse=True)
    elif sort_key == 'popularity':
        filtered_articles.sort(key=lambda x: x['views'], reverse=True)

    return render_template('category.html', page_title='Category Articles', category_name=category_name, articles=filtered_articles)


@app.route('/search')
def search_results():
    articles = read_articles()
    query = request.args.get('q', '').strip()
    query_lower = query.lower()

    results = []
    if query:
        results = [a for a in articles if 
                   query_lower in a['title'].lower() or
                   query_lower in a['author'].lower() or
                   query_lower in a['content'].lower()]

    return render_template('search_results.html', page_title='Search Results', query=query, results=results)


@app.route('/article/<int:article_id>/bookmark', methods=['POST'])
def bookmark_article(article_id):
    articles = read_articles()
    article = find_article(articles, article_id)
    if not article:
        flash('Article not found.', 'error')
        return redirect(url_for('article_details', article_id=article_id))

    bookmarks = read_bookmarks()
    # Check if already bookmarked
    for b in bookmarks:
        if b['article_id'] == article_id:
            flash('Article already bookmarked.', 'info')
            return redirect(url_for('article_details', article_id=article_id))

    new_bookmark_id = max([b['bookmark_id'] for b in bookmarks], default=0) + 1
    bookmarked_date = datetime.now().strftime('%Y-%m-%d')
    new_bookmark = {
        'bookmark_id': new_bookmark_id,
        'article_id': article_id,
        'article_title': article['title'],
        'bookmarked_date': bookmarked_date
    }

    bookmarks.append(new_bookmark)
    try:
        write_bookmarks(bookmarks)
        flash('Article bookmarked successfully.', 'success')
    except Exception as e:
        flash('Failed to bookmark article.', 'error')

    return redirect(url_for('article_details', article_id=article_id))


if __name__ == '__main__':
    app.run(debug=True)
