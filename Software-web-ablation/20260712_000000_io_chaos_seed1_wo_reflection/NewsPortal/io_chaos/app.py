from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_dir = 'data'

# Utility functions for file handling and data parsing

def read_articles():
    articles = []
    try:
        with open(os.path.join(data_dir, 'articles.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 7:
                    article = {
                        'article_id': int(fields[0]),
                        'title': fields[1],
                        'author': fields[2],
                        'category': fields[3],
                        'content': fields[4],
                        'date': fields[5],
                        'views': int(fields[6])
                    }
                    articles.append(article)
    except FileNotFoundError:
        pass
    return articles


def read_categories():
    categories = []
    try:
        with open(os.path.join(data_dir, 'categories.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 3:
                    category = {
                        'category_id': int(fields[0]),
                        'category_name': fields[1],
                        'description': fields[2]
                    }
                    categories.append(category)
    except FileNotFoundError:
        pass
    return categories


def read_bookmarks():
    bookmarks = []
    try:
        with open(os.path.join(data_dir, 'bookmarks.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 4:
                    bookmark = {
                        'bookmark_id': int(fields[0]),
                        'article_id': int(fields[1]),
                        'article_title': fields[2],
                        'bookmarked_date': fields[3]
                    }
                    bookmarks.append(bookmark)
    except FileNotFoundError:
        pass
    return bookmarks


def write_bookmarks(bookmarks):
    lines = []
    for b in bookmarks:
        line = f"{b['bookmark_id']}|{b['article_id']}|{b['article_title']}|{b['bookmarked_date']}"
        lines.append(line)
    content = '\n'.join(lines)
    # Use the required write_text_file tool to write bookmarks.txt
    from functions import write_text_file
    write_text_file({
        'filename': os.path.join(data_dir, 'bookmarks.txt'),
        'content': content
    })


def read_comments():
    comments = []
    try:
        with open(os.path.join(data_dir, 'comments.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 6:
                    comment = {
                        'comment_id': int(fields[0]),
                        'article_id': int(fields[1]),
                        'article_title': fields[2],
                        'commenter_name': fields[3],
                        'comment_text': fields[4],
                        'comment_date': fields[5]
                    }
                    comments.append(comment)
    except FileNotFoundError:
        pass
    return comments


def write_comments(comments):
    lines = []
    for c in comments:
        line = f"{c['comment_id']}|{c['article_id']}|{c['article_title']}|{c['commenter_name']}|{c['comment_text']}|{c['comment_date']}"
        lines.append(line)
    content = '\n'.join(lines)
    # Use the required write_text_file tool to write comments.txt
    from functions import write_text_file
    write_text_file({
        'filename': os.path.join(data_dir, 'comments.txt'),
        'content': content
    })


def read_trending():
    trending = []
    try:
        with open(os.path.join(data_dir, 'trending.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 5:
                    item = {
                        'article_id': int(fields[0]),
                        'article_title': fields[1],
                        'category': fields[2],
                        'view_count': int(fields[3]),
                        'period': fields[4]
                    }
                    trending.append(item)
    except FileNotFoundError:
        pass
    return trending


def write_articles(articles):
    lines = []
    for a in articles:
        line = f"{a['article_id']}|{a['title']}|{a['author']}|{a['category']}|{a['content']}|{a['date']}|{a['views']}"
        lines.append(line)
    content = '\n'.join(lines)
    from functions import write_text_file
    write_text_file({
        'filename': os.path.join(data_dir, 'articles.txt'),
        'content': content
    })


# Flask Routes

@app.route('/')
def root_redirect():
    # Redirect to dashboard as specified
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    articles = read_articles()
    # featured_articles keys: article_id, title, excerpt (excerpt from content)
    # Fix: Ensure at least some articles exist, and excerpt should handle empty content safely
    featured_articles = []
    for a in articles[:5]:
        excerpt = a['content'][:150] if a['content'] else ''
        featured_articles.append({'article_id': a['article_id'], 'title': a['title'], 'excerpt': excerpt})
    trending = read_trending()
    # trending_articles keys: article_id, title, views
    trending_articles = [
        {'article_id': t['article_id'], 'title': t['article_title'], 'views': t['view_count']}
        for t in trending if t['period'] == 'This Week'
    ]
    return render_template('dashboard.html', featured_articles=featured_articles, trending_articles=trending_articles)


@app.route('/catalog')
def article_catalog():
    articles = read_articles()
    categories = read_categories()
    # Optional filters from query args
    search_query = request.args.get('search_query', '').strip()
    category_filter = request.args.get('category_filter', '').strip()

    filtered_articles = articles
    if search_query:
        search_lower = search_query.lower()
        filtered_articles = [a for a in filtered_articles if search_lower in a['title'].lower() or search_lower in a['author'].lower() or search_lower in a['content'].lower()]
    if category_filter:
        filtered_articles = [a for a in filtered_articles if a['category'] == category_filter]

    return render_template('catalog.html', articles=filtered_articles, categories=categories, search_query=search_query, category_filter=category_filter)


@app.route('/catalog/search', methods=['POST'])
def catalog_search():
    search_query = request.form.get('search_query', '').strip()
    category_filter = request.form.get('category_filter', '').strip()
    articles = read_articles()
    categories = read_categories()

    filtered_articles = articles
    if search_query:
        search_lower = search_query.lower()
        filtered_articles = [a for a in filtered_articles if search_lower in a['title'].lower() or search_lower in a['author'].lower() or search_lower in a['content'].lower()]
    if category_filter:
        filtered_articles = [a for a in filtered_articles if a['category'] == category_filter]

    return render_template('catalog.html', articles=filtered_articles, categories=categories, search_query=search_query, category_filter=category_filter)


@app.route('/article/<int:article_id>')
def article_details(article_id):
    articles = read_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        # Handle 404 gracefully by rendering a template with empty context or error message
        article = {'article_id': article_id, 'title': 'Article Not Found', 'author': '', 'category': '', 'content': '', 'date': '', 'views': 0}
    return render_template('article_details.html', article=article)


@app.route('/article/<int:article_id>/bookmark', methods=['POST'])
def bookmark_article(article_id):
    articles = read_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        bookmark_success = False
        # Pass empty article dict to avoid template error
        article = {'article_id': article_id, 'title': '', 'author': '', 'category': '', 'content': '', 'date': '', 'views': 0}
    else:
        bookmarks = read_bookmarks()
        # Check if already bookmarked
        already_bookmarked = any(b['article_id'] == article_id for b in bookmarks)
        if not already_bookmarked:
            new_id = max([b['bookmark_id'] for b in bookmarks], default=0) + 1
            bookmarked_date = datetime.now().strftime('%Y-%m-%d')
            new_bookmark = {
                'bookmark_id': new_id,
                'article_id': article_id,
                'article_title': article['title'],
                'bookmarked_date': bookmarked_date
            }
            bookmarks.append(new_bookmark)
            write_bookmarks(bookmarks)
        bookmark_success = True
    return render_template('article_details.html', article=article, bookmark_success=bookmark_success)


@app.route('/bookmarks')
def bookmarks_page():
    bookmarks = read_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)


@app.route('/bookmarks/remove/<int:bookmark_id>', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = read_bookmarks()
    bookmarks = [b for b in bookmarks if b['bookmark_id'] != bookmark_id]
    write_bookmarks(bookmarks)
    return render_template('bookmarks.html', bookmarks=bookmarks)


@app.route('/comments')
def comments_page():
    comments = read_comments()
    articles = read_articles()
    # Add article_title to comments if missing or just ensure consistency
    articles_map = {a['article_id']: a['title'] for a in articles}
    for c in comments:
        if c['article_id'] in articles_map:
            c['article_title'] = articles_map[c['article_id']]
        else:
            # Provide fallback if article not found
            c['article_title'] = 'Unknown Article'
    filter_article_id = request.args.get('filter_article_id', type=int)
    if filter_article_id:
        comments = [c for c in comments if c['article_id'] == filter_article_id]
    return render_template('comments.html', comments=comments, articles=[{'article_id': a['article_id'], 'title': a['title']} for a in articles], filter_article_id=filter_article_id)


@app.route('/comments/filter', methods=['POST'])
def filter_comments():
    filter_article_id = request.form.get('filter_article_id', type=int)
    comments = read_comments()
    articles = read_articles()
    articles_map = {a['article_id']: a['title'] for a in articles}
    for c in comments:
        if c['article_id'] in articles_map:
            c['article_title'] = articles_map[c['article_id']]
        else:
            c['article_title'] = 'Unknown Article'
    if filter_article_id:
        comments = [c for c in comments if c['article_id'] == filter_article_id]
    return render_template('comments.html', comments=comments, articles=[{'article_id': a['article_id'], 'title': a['title']} for a in articles], filter_article_id=filter_article_id)


@app.route('/comments/write')
def write_comment_get():
    articles = read_articles()
    return render_template('write_comment.html', articles=[{'article_id': a['article_id'], 'title': a['title']} for a in articles])


@app.route('/comments/write/submit', methods=['POST'])
def write_comment_post():
    article_id = request.form.get('article_id', type=int)
    commenter_name = request.form.get('commenter_name', '').strip()
    comment_text = request.form.get('comment_text', '').strip()
    articles = read_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)

    submit_success = False
    if article and commenter_name and comment_text:
        comments = read_comments()
        new_id = max([c['comment_id'] for c in comments], default=0) + 1
        comment_date = datetime.now().strftime('%Y-%m-%d')
        new_comment = {
            'comment_id': new_id,
            'article_id': article_id,
            'article_title': article['title'],
            'commenter_name': commenter_name,
            'comment_text': comment_text,
            'comment_date': comment_date
        }
        comments.append(new_comment)
        write_comments(comments)
        submit_success = True

    return render_template('write_comment.html', articles=[{'article_id': a['article_id'], 'title': a['title']} for a in articles], submit_success=submit_success)


@app.route('/trending')
def trending_articles():
    trending = read_trending()
    time_period = request.args.get('time_period', 'This Week')
    filtered_trending = [t for t in trending if t['period'] == time_period]
    return render_template('trending.html', trending_articles=filtered_trending, time_period=time_period)


@app.route('/trending/filter', methods=['POST'])
def filter_trending():
    time_period = request.form.get('time_period', '').strip()
    trending = read_trending()
    filtered_trending = [t for t in trending if t['period'] == time_period]
    return render_template('trending.html', trending_articles=filtered_trending, time_period=time_period)


@app.route('/category/<string:category_name>')
def category_articles(category_name):
    articles = read_articles()
    filtered_articles = [a for a in articles if a['category'] == category_name]
    # Include views in the context
    filtered_articles = [{
        'article_id': a['article_id'],
        'title': a['title'],
        'author': a['author'],
        'date': a['date'],
        'views': a['views']
    } for a in filtered_articles]
    return render_template('category.html', category_name=category_name, articles=filtered_articles)


@app.route('/category/<string:category_name>/sort', methods=['POST'])
def sort_category_articles(category_name):
    sort_by = request.form.get('sort_by', '')
    articles = read_articles()
    filtered_articles = [a for a in articles if a['category'] == category_name]

    if sort_by == 'date':
        # Sort by date descending
        filtered_articles.sort(key=lambda x: x['date'], reverse=True)
    elif sort_by == 'popularity':
        # Sort by views descending
        filtered_articles.sort(key=lambda x: x['views'], reverse=True)

    filtered_articles = [{
        'article_id': a['article_id'],
        'title': a['title'],
        'author': a['author'],
        'date': a['date'],
        'views': a['views']
    } for a in filtered_articles]

    return render_template('category.html', category_name=category_name, articles=filtered_articles, sort_by=sort_by)


@app.route('/search', methods=['POST'])
def search_results():
    search_query = request.form.get('search_query', '').strip()
    articles = read_articles()
    results = []
    if search_query:
        search_lower = search_query.lower()
        results = [
            {'article_id': a['article_id'], 'title': a['title'], 'excerpt': a['content'][:150]}
            for a in articles
            if search_lower in a['title'].lower() or search_lower in a['author'].lower() or search_lower in a['content'].lower()
        ]
    return render_template('search_results.html', search_query=search_query, results=results)


@app.route('/search/results')
def search_results_get():
    search_query = request.args.get('search_query', '').strip()
    articles = read_articles()
    results = []
    if search_query:
        search_lower = search_query.lower()
        results = [
            {'article_id': a['article_id'], 'title': a['title'], 'excerpt': a['content'][:150]}
            for a in articles
            if search_lower in a['title'].lower() or search_lower in a['author'].lower() or search_lower in a['content'].lower()
        ]
    return render_template('search_results.html', search_query=search_query, results=results)


if __name__ == '__main__':
    app.run(debug=True)
