from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'


# Utility functions to read and write data files

def read_articles():
    articles = []
    path = os.path.join(DATA_DIR, 'articles.txt')
    if not os.path.exists(path):
        return articles
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            article_id, title, author, category, content, date, views = parts
            try:
                articles.append({
                    'article_id': int(article_id),
                    'title': title,
                    'author': author,
                    'category': category,
                    'content': content,
                    'date': date,
                    'views': int(views)
                })
            except ValueError:
                continue
    return articles


def read_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    if not os.path.exists(path):
        return categories
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            category_id, category_name, description = parts
            try:
                categories.append({
                    'category_id': int(category_id),
                    'category_name': category_name,
                    'description': description
                })
            except ValueError:
                continue
    return categories


def read_bookmarks():
    bookmarks = []
    path = os.path.join(DATA_DIR, 'bookmarks.txt')
    if not os.path.exists(path):
        return bookmarks
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 4:
                continue
            bookmark_id, article_id, article_title, bookmarked_date = parts
            try:
                bookmarks.append({
                    'bookmark_id': int(bookmark_id),
                    'article_id': int(article_id),
                    'article_title': article_title,
                    'bookmarked_date': bookmarked_date
                })
            except ValueError:
                continue
    return bookmarks


def write_bookmarks(bookmarks):
    path = os.path.join(DATA_DIR, 'bookmarks.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in bookmarks:
            line = f"{b['bookmark_id']}|{b['article_id']}|{b['article_title']}|{b['bookmarked_date']}\n"
            f.write(line)


def read_comments():
    comments = []
    path = os.path.join(DATA_DIR, 'comments.txt')
    if not os.path.exists(path):
        return comments
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            comment_id, article_id, article_title, commenter_name, comment_text, comment_date = parts
            try:
                comments.append({
                    'comment_id': int(comment_id),
                    'article_id': int(article_id),
                    'article_title': article_title,
                    'commenter_name': commenter_name,
                    'comment_text': comment_text,
                    'comment_date': comment_date
                })
            except ValueError:
                continue
    return comments


def write_comments(comments):
    path = os.path.join(DATA_DIR, 'comments.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for c in comments:
            line = f"{c['comment_id']}|{c['article_id']}|{c['article_title']}|{c['commenter_name']}|{c['comment_text']}|{c['comment_date']}\n"
            f.write(line)


def read_trending():
    trending = []
    path = os.path.join(DATA_DIR, 'trending.txt')
    if not os.path.exists(path):
        return trending
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            article_id, article_title, category, view_count, period = parts
            try:
                trending.append({
                    'article_id': int(article_id),
                    'article_title': article_title,
                    'category': category,
                    'view_count': int(view_count),
                    'period': period
                })
            except ValueError:
                continue
    return trending


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    articles = read_articles()
    trending = read_trending()
    # featured_articles: list(dict) keys: article_id, title, author, date
    # pick top 5 articles by views descending for featured_articles
    sorted_articles = sorted(articles, key=lambda a: a['views'], reverse=True)
    featured_articles = [
        {'article_id': a['article_id'], 'title': a['title'], 'author': a['author'], 'date': a['date']}
        for a in sorted_articles[:5]
    ]
    # trending_articles: list(dict) keys: article_id, title, category, view_count
    trending_articles = [
        {'article_id': t['article_id'], 'title': t['article_title'], 'category': t['category'], 'view_count': t['view_count']}
        for t in trending
    ]
    return render_template('dashboard.html', featured_articles=featured_articles, trending_articles=trending_articles)


@app.route('/articles')
def article_catalog():
    articles = read_articles()
    categories = read_categories()
    search_query = request.args.get('search_query', '').strip()
    category_filter = request.args.get('category_filter', '').strip()

    filtered_articles = articles
    if search_query:
        sq_lower = search_query.lower()
        filtered_articles = [a for a in filtered_articles if (sq_lower in a['title'].lower() or
                                                           sq_lower in a['author'].lower() or
                                                           sq_lower in a['content'].lower())]
    if category_filter:
        filtered_articles = [a for a in filtered_articles if a['category'] == category_filter]

    # context keys: articles, categories, search_query (optional), category_filter (optional)
    context = {
        'articles': filtered_articles,
        'categories': categories
    }
    if search_query:
        context['search_query'] = search_query
    if category_filter:
        context['category_filter'] = category_filter

    return render_template('article_catalog.html', **context)


@app.route('/article/<int:article_id>')
def article_details(article_id):
    articles = read_articles()
    bookmarks = read_bookmarks()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        # Article not found 404
        return "Article not found", 404

    is_bookmarked = any(b['article_id'] == article_id for b in bookmarks)

    # context keys: article, is_bookmarked
    return render_template('article_details.html', article=article, is_bookmarked=is_bookmarked)


@app.route('/article/<int:article_id>/bookmark', methods=['POST'])
def bookmark_article(article_id):
    articles = read_articles()
    bookmarks = read_bookmarks()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404

    if any(b['article_id'] == article_id for b in bookmarks):
        # Already bookmarked, just redirect
        return redirect(url_for('article_details', article_id=article_id))

    # Add new bookmark
    bookmark_id = (max([b['bookmark_id'] for b in bookmarks]) + 1) if bookmarks else 1
    bookmarked_date = datetime.now().strftime('%Y-%m-%d')
    new_bookmark = {
        'bookmark_id': bookmark_id,
        'article_id': article_id,
        'article_title': article['title'],
        'bookmarked_date': bookmarked_date
    }
    bookmarks.append(new_bookmark)
    write_bookmarks(bookmarks)

    return redirect(url_for('article_details', article_id=article_id))


@app.route('/bookmarks')
def bookmarks():
    bookmarks = read_bookmarks()
    # context variables: bookmarks
    return render_template('bookmarks.html', bookmarks=bookmarks)


@app.route('/bookmarks/remove/<int:bookmark_id>', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = read_bookmarks()
    # Remove the bookmark with matching bookmark_id
    new_bookmarks = [b for b in bookmarks if b['bookmark_id'] != bookmark_id]
    if len(new_bookmarks) != len(bookmarks):
        write_bookmarks(new_bookmarks)
    return redirect(url_for('bookmarks'))


@app.route('/comments')
def comments():
    comments = read_comments()
    articles = read_articles()
    filter_article_id = request.args.get('filter_article_id', '').strip()
    try:
        filter_article_id = int(filter_article_id) if filter_article_id else None
    except ValueError:
        filter_article_id = None

    if filter_article_id is not None:
        comments_filtered = [c for c in comments if c['article_id'] == filter_article_id]
    else:
        comments_filtered = comments

    # Enrich comments with article_title from articles file if missing or fallback
    articles_dict = {a['article_id']: a['title'] for a in articles}
    for c in comments_filtered:
        if 'article_title' not in c or not c['article_title']:
            c['article_title'] = articles_dict.get(c['article_id'], 'Unknown Article')

    # articles list to pass: keys: article_id, title
    articles_list = [{'article_id': a['article_id'], 'title': a['title']} for a in articles]

    return render_template('comments.html', comments=comments_filtered, articles=articles_list, filter_article_id=filter_article_id)


@app.route('/comments/write')
def write_comment():
    articles = read_articles()
    articles_list = [{'article_id': a['article_id'], 'title': a['title']} for a in articles]
    return render_template('write_comment.html', articles=articles_list)


@app.route('/comments/write', methods=['POST'])
def submit_comment():
    article_id = request.form.get('article_id', '').strip()
    commenter_name = request.form.get('commenter_name', '').strip()
    comment_text = request.form.get('comment_text', '').strip()

    # Validate inputs
    try:
        article_id = int(article_id)
    except ValueError:
        return "Invalid article ID", 400
    if not commenter_name or not comment_text:
        return "Name and comment text are required", 400

    articles = read_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404

    comments = read_comments()
    comment_id = (max([c['comment_id'] for c in comments]) + 1) if comments else 1
    comment_date = datetime.now().strftime('%Y-%m-%d')
    new_comment = {
        'comment_id': comment_id,
        'article_id': article_id,
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
    trending = read_trending()
    time_period = request.args.get('time_period', '').strip()

    filtered_trending = trending
    if time_period:
        filtered_trending = [t for t in trending if t['period'] == time_period]

    # Context variables: trending_articles, time_period
    return render_template('trending_articles.html', trending_articles=filtered_trending, time_period=time_period if time_period else None)


@app.route('/category/<string:category_name>')
def category_articles(category_name):
    articles = read_articles()
    # Filter articles by category
    filtered_articles = [a for a in articles if a['category'] == category_name]

    # context variables: category_name, articles
    return render_template('category.html', category_name=category_name, articles=filtered_articles)


@app.route('/search')
def search_results():
    query = request.args.get('query', '').strip()
    articles = read_articles()

    results = []
    if query:
        q_lower = query.lower()
        for a in articles:
            if q_lower in a['title'].lower() or q_lower in a['content'].lower():
                excerpt = a['content'][:100] + ('...' if len(a['content']) > 100 else '')
                results.append({'article_id': a['article_id'], 'title': a['title'], 'excerpt': excerpt})

    return render_template('search_results.html', query=query, results=results)


if __name__ == '__main__':
    app.run(debug=True)
