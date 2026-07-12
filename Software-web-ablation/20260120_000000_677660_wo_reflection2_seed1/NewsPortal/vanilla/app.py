from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions for file operations

def read_articles():
    filepath = os.path.join(DATA_DIR, 'articles.txt')
    articles = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    article_id = int(parts[0])
                    title = parts[1]
                    author = parts[2]
                    category = parts[3]
                    content = parts[4]
                    date = parts[5]
                    views = int(parts[6])
                    articles.append({
                        'article_id': article_id,
                        'title': title,
                        'author': author,
                        'category': category,
                        'content': content,
                        'date': date,
                        'views': views
                    })
    except FileNotFoundError:
        pass
    return articles


def read_categories():
    filepath = os.path.join(DATA_DIR, 'categories.txt')
    categories = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    category_id = int(parts[0])
                    category_name = parts[1]
                    description = parts[2]
                    categories.append({
                        'category_id': category_id,
                        'category_name': category_name,
                        'description': description
                    })
    except FileNotFoundError:
        pass
    return categories


def read_bookmarks():
    filepath = os.path.join(DATA_DIR, 'bookmarks.txt')
    bookmarks = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    bookmark_id = int(parts[0])
                    article_id = int(parts[1])
                    article_title = parts[2]
                    bookmarked_date = parts[3]
                    bookmarks.append({
                        'bookmark_id': bookmark_id,
                        'article_id': article_id,
                        'article_title': article_title,
                        'bookmarked_date': bookmarked_date
                    })
    except FileNotFoundError:
        pass
    return bookmarks


def write_bookmarks(bookmarks):
    filepath = os.path.join(DATA_DIR, 'bookmarks.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for bm in bookmarks:
                line = f"{bm['bookmark_id']}|{bm['article_id']}|{bm['article_title']}|{bm['bookmarked_date']}
"
                f.write(line)
    except Exception:
        pass


def read_comments():
    filepath = os.path.join(DATA_DIR, 'comments.txt')
    comments = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    comment_id = int(parts[0])
                    article_id = int(parts[1])
                    article_title = parts[2]
                    commenter_name = parts[3]
                    comment_text = parts[4]
                    comment_date = parts[5]
                    comments.append({
                        'comment_id': comment_id,
                        'article_id': article_id,
                        'article_title': article_title,
                        'commenter_name': commenter_name,
                        'comment_text': comment_text,
                        'comment_date': comment_date
                    })
    except FileNotFoundError:
        pass
    return comments


def write_comments(comments):
    filepath = os.path.join(DATA_DIR, 'comments.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for c in comments:
                line = f"{c['comment_id']}|{c['article_id']}|{c['article_title']}|{c['commenter_name']}|{c['comment_text']}|{c['comment_date']}
"
                f.write(line)
    except Exception:
        pass


def read_trending():
    filepath = os.path.join(DATA_DIR, 'trending.txt')
    trending_articles = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    article_id = int(parts[0])
                    article_title = parts[1]
                    category = parts[2]
                    view_count = int(parts[3])
                    period = parts[4]
                    trending_articles.append({
                        'article_id': article_id,
                        'article_title': article_title,
                        'category': category,
                        'view_count': view_count,
                        'period': period
                    })
    except FileNotFoundError:
        pass
    return trending_articles


# Routes
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    articles = read_articles()
    # For featured_articles: recommend featured articles from articles list, here select first 5 for example
    featured_articles = []
    for article in articles[:5]:
        featured_articles.append({
            'article_id': article['article_id'],
            'title': article['title'],
            'author': article['author'],
            'category': article['category'],
            'date': article['date'],
            'excerpt': article['content'][:100] + ('...' if len(article['content']) > 100 else '')
        })

    trending_raw = read_trending()
    # trending_articles context: list of dicts with keys: article_id, title, category, view_count
    trending_articles = []
    # Aggregate trending for period "This Week" as a default
    for t in trending_raw:
        if t['period'] == 'This Week':
            trending_articles.append({
                'article_id': t['article_id'],
                'title': t['article_title'],
                'category': t['category'],
                'view_count': t['view_count']
            })

    return render_template('dashboard.html', featured_articles=featured_articles, trending_articles=trending_articles)


@app.route('/catalog')
def article_catalog():
    articles = read_articles()
    categories = read_categories()
    # Get optional query parameters for filter
    selected_category = request.args.get('category')
    search_query = request.args.get('search')

    # Filter by category if selected
    if selected_category:
        articles = [a for a in articles if a['category'] == selected_category]

    # Filter by search_query if given
    if search_query:
        lquery = search_query.lower()
        articles = [a for a in articles if lquery in a['title'].lower() or lquery in a['content'].lower()]

    # We need to pass articles with subset keys: article_id, title, author, category, date, excerpt
    for i in range(len(articles)):
        excerpt = articles[i]['content'][:100] + ('...' if len(articles[i]['content']) > 100 else '')
        articles[i] = {
            'article_id': articles[i]['article_id'],
            'title': articles[i]['title'],
            'author': articles[i]['author'],
            'category': articles[i]['category'],
            'date': articles[i]['date'],
            'excerpt': excerpt
        }

    return render_template('catalog.html', articles=articles, categories=categories, selected_category=selected_category, search_query=search_query)


@app.route('/article/<int:article_id>')
def article_details(article_id):
    articles = read_articles()
    bookmarks = read_bookmarks()
    article = None
    for a in articles:
        if a['article_id'] == article_id:
            article = a
            break

    if article is None:
        # Could render 404 or redirect to catalog
        return redirect(url_for('article_catalog'))

    # Check if bookmarked
    is_bookmarked = False
    for bm in bookmarks:
        if bm['article_id'] == article_id:
            is_bookmarked = True
            break

    return render_template('article_details.html', article=article, is_bookmarked=is_bookmarked)


@app.route('/article/<int:article_id>/bookmark', methods=['POST'])
def bookmark_article(article_id):
    articles = read_articles()
    article = None
    for a in articles:
        if a['article_id'] == article_id:
            article = a
            break
    if article is None:
        return redirect(url_for('article_catalog'))

    bookmarks = read_bookmarks()
    # Check if already bookmarked
    for bm in bookmarks:
        if bm['article_id'] == article_id:
            return redirect(url_for('article_details', article_id=article_id))

    # Add new bookmark
    new_id = 1
    if bookmarks:
        new_id = max(bm['bookmark_id'] for bm in bookmarks) + 1
    today_str = datetime.now().strftime('%Y-%m-%d')
    bookmarks.append({
        'bookmark_id': new_id,
        'article_id': article['article_id'],
        'article_title': article['title'],
        'bookmarked_date': today_str
    })
    write_bookmarks(bookmarks)

    return redirect(url_for('article_details', article_id=article_id))


@app.route('/bookmarks')
def bookmarks_page():
    bookmarks = read_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)


@app.route('/bookmark/<int:bookmark_id>/remove', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = read_bookmarks()
    bookmarks = [bm for bm in bookmarks if bm['bookmark_id'] != bookmark_id]
    write_bookmarks(bookmarks)
    return redirect(url_for('bookmarks_page'))


@app.route('/comments')
def comments_page():
    comments = read_comments()
    articles = read_articles()

    # Filter comments by article if query param
    article_filter = request.args.get('article_id', type=int)

    if article_filter is not None:
        filtered_comments = []
        for c in comments:
            if c['article_id'] == article_filter:
                filtered_comments.append(c)
        comments = filtered_comments

    # For articles: only article_id, title keys needed
    simple_articles = [{'article_id': a['article_id'], 'title': a['title']} for a in articles]

    return render_template('comments.html', comments=comments, articles=simple_articles, selected_article_id=article_filter)


@app.route('/comments/write')
def write_comment_page():
    articles = read_articles()
    simple_articles = [{'article_id': a['article_id'], 'title': a['title']} for a in articles]
    return render_template('write_comment.html', articles=simple_articles)


@app.route('/comments/write', methods=['POST'])
def submit_comment():
    commenter_name = request.form.get('commenter_name','').strip()
    comment_text = request.form.get('comment_text','').strip()
    article_id = request.form.get('article_id')

    if not commenter_name or not comment_text or not article_id:
        # Could handle error display, but spec does not describe it; redirect back
        return redirect(url_for('write_comment_page'))

    try:
        article_id = int(article_id)
    except ValueError:
        return redirect(url_for('write_comment_page'))

    articles = read_articles()
    article = None
    for a in articles:
        if a['article_id'] == article_id:
            article = a
            break
    if article is None:
        return redirect(url_for('write_comment_page'))

    comments = read_comments()
    new_id = 1
    if comments:
        new_id = max(c['comment_id'] for c in comments) + 1
    today_str = datetime.now().strftime('%Y-%m-%d')

    comments.append({
        'comment_id': new_id,
        'article_id': article_id,
        'article_title': article['title'],
        'commenter_name': commenter_name,
        'comment_text': comment_text,
        'comment_date': today_str
    })
    write_comments(comments)

    return redirect(url_for('comments_page'))


@app.route('/trending')
def trending_articles():
    trending_raw = read_trending()
    time_period = request.args.get('period', 'This Week')
    trending_filtered = [t for t in trending_raw if t['period'] == time_period]

    return render_template('trending.html', trending_articles=trending_filtered, time_period=time_period)


@app.route('/category/<string:category_name>')
def category_page(category_name):
    articles = read_articles()
    filtered_articles = [a for a in articles if a['category'] == category_name]

    # Articles context keys: article_id, title, author, date, views
    articles_ctx = []
    for a in filtered_articles:
        articles_ctx.append({
            'article_id': a['article_id'],
            'title': a['title'],
            'author': a['author'],
            'date': a['date'],
            'views': a['views']
        })

    return render_template('category.html', category_name=category_name, articles=articles_ctx)


@app.route('/category/<string:category_name>/sort/<string:sort_type>')
def sort_category_articles(category_name, sort_type):
    articles = read_articles()
    filtered_articles = [a for a in articles if a['category'] == category_name]

    if sort_type == 'date':
        filtered_articles.sort(key=lambda x: x['date'], reverse=True)
    elif sort_type == 'popularity':
        filtered_articles.sort(key=lambda x: x['views'], reverse=True)

    articles_ctx = []
    for a in filtered_articles:
        articles_ctx.append({
            'article_id': a['article_id'],
            'title': a['title'],
            'author': a['author'],
            'date': a['date'],
            'views': a['views']
        })

    return render_template('category.html', category_name=category_name, articles=articles_ctx, sort_type=sort_type)


@app.route('/search')
def search_results():
    search_query = request.args.get('q', '')
    articles = read_articles()
    search_results = []
    if search_query:
        lquery = search_query.lower()
        for a in articles:
            if lquery in a['title'].lower() or lquery in a['content'].lower():
                excerpt = a['content'][:100] + ('...' if len(a['content']) > 100 else '')
                search_results.append({
                    'article_id': a['article_id'],
                    'title': a['title'],
                    'excerpt': excerpt
                })

    return render_template('search_results.html', search_query=search_query, search_results=search_results)


if __name__ == '__main__':
    app.run(debug=True)
