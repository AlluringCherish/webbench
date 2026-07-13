from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = 'data'

# Helper functions to read and write data files

def read_articles():
    articles = []
    try:
        with open(os.path.join(DATA_DIR, 'articles.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
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
    except FileNotFoundError:
        pass
    return articles


def write_articles(articles):
    with open(os.path.join(DATA_DIR, 'articles.txt'), 'w', encoding='utf-8') as f:
        for a in articles:
            line = '|'.join([a['article_id'], a['title'], a['author'], a['category'], a['content'], a['date'], str(a['views'])])
            f.write(line + '\n')


def read_categories():
    categories = []
    try:
        with open(os.path.join(DATA_DIR, 'categories.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                categories.append({'category_id': parts[0], 'category_name': parts[1], 'description': parts[2]})
    except FileNotFoundError:
        pass
    return categories


def read_bookmarks():
    bookmarks = []
    try:
        with open(os.path.join(DATA_DIR, 'bookmarks.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 4:
                    continue
                bookmarks.append({'bookmark_id': parts[0], 'article_id': parts[1], 'article_title': parts[2], 'bookmarked_date': parts[3]})
    except FileNotFoundError:
        pass
    return bookmarks


def write_bookmarks(bookmarks):
    with open(os.path.join(DATA_DIR, 'bookmarks.txt'), 'w', encoding='utf-8') as f:
        for b in bookmarks:
            line = '|'.join([b['bookmark_id'], b['article_id'], b['article_title'], b['bookmarked_date']])
            f.write(line + '\n')


def read_comments():
    comments = []
    try:
        with open(os.path.join(DATA_DIR, 'comments.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                comments.append({'comment_id': parts[0], 'article_id': parts[1], 'article_title': parts[2], 'commenter_name': parts[3], 'comment_text': parts[4], 'comment_date': parts[5]})
    except FileNotFoundError:
        pass
    return comments


def write_comment(comment):
    # Append comment
    with open(os.path.join(DATA_DIR, 'comments.txt'), 'a', encoding='utf-8') as f:
        line = '|'.join([comment['comment_id'], comment['article_id'], comment['article_title'], comment['commenter_name'], comment['comment_text'], comment['comment_date']])
        f.write(line + '\n')


def read_trending():
    trending = []
    try:
        with open(os.path.join(DATA_DIR, 'trending.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                trending.append({'article_id': parts[0], 'article_title': parts[1], 'category': parts[2], 'view_count': int(parts[3]), 'period': parts[4]})
    except FileNotFoundError:
        pass
    return trending


@app.route('/dashboard')
def dashboard():
    # Show featured articles - pick top 3 by views from articles
    articles = read_articles()
    featured_articles = sorted(articles, key=lambda x: x['views'], reverse=True)[:3]
    return render_template('dashboard.html', featured_articles=featured_articles)


@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    articles = read_articles()
    categories = [c['category_name'] for c in read_categories()]
    search_query = ''
    selected_category = ''
    filtered_articles = articles

    if request.method == 'POST':
        search_query = request.form.get('search-input', '').strip().lower()
        selected_category = request.form.get('category-filter', '')
        if search_query:
            # Redirect to search results page
            return redirect(url_for('search_results', query=search_query))
        if selected_category and selected_category != 'All':
            filtered_articles = [a for a in articles if a['category'] == selected_category]

    return render_template('catalog.html', articles=filtered_articles, categories=categories, selected_category=selected_category, search_query=search_query)


@app.route('/search-results')
def search_results():
    query = request.args.get('query', '').lower()
    articles = read_articles()
    if query:
        results = [a for a in articles if query in a['title'].lower() or query in a['author'].lower() or query in a['content'].lower()]
    else:
        results = []
    return render_template('search_results.html', query=query, results=results)


@app.route('/article/<article_id>', methods=['GET', 'POST'])
def article_details(article_id):
    articles = read_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404

    if request.method == 'POST':
        # Bookmark article
        bookmarks = read_bookmarks()
        # Check if already bookmarked
        if not any(b['article_id'] == article_id for b in bookmarks):
            bookmark_id = str(len(bookmarks) + 1)
            bookmarks.append({'bookmark_id': bookmark_id,
                              'article_id': article_id,
                              'article_title': article['title'],
                              'bookmarked_date': datetime.now().strftime('%Y-%m-%d')})
            write_bookmarks(bookmarks)

    # Increment views
    for a in articles:
        if a['article_id'] == article_id:
            a['views'] += 1
            break
    write_articles(articles)

    return render_template('article_details.html', article=article)


@app.route('/bookmarks', methods=['GET', 'POST'])
def bookmarks():
    bookmarks = read_bookmarks()
    if request.method == 'POST':
        # Remove bookmark
        for key in request.form.keys():
            if key.startswith('remove-bookmark-button-'):
                bookmark_id = key.replace('remove-bookmark-button-', '')
                bookmarks = [b for b in bookmarks if b['bookmark_id'] != bookmark_id]
                write_bookmarks(bookmarks)
                return redirect(url_for('bookmarks'))
            elif key.startswith('read-bookmark-button-'):
                bookmark_id = key.replace('read-bookmark-button-', '')
                bookmark = next((b for b in bookmarks if b['bookmark_id'] == bookmark_id), None)
                if bookmark:
                    return redirect(url_for('article_details', article_id=bookmark['article_id']))
    return render_template('bookmarks.html', bookmarks=bookmarks)


@app.route('/comments', methods=['GET', 'POST'])
def comments():
    comments = read_comments()
    articles = read_articles()
    filter_article = request.args.get('filter-by-article', '')

    filtered_comments = comments
    if filter_article:
        filtered_comments = [c for c in comments if c['article_title'] == filter_article]

    categories = [c['category_name'] for c in read_categories()]
    article_titles = [a['title'] for a in articles]

    return render_template('comments.html', comments=filtered_comments, articles=article_titles, selected_article=filter_article)


@app.route('/write-comment', methods=['GET', 'POST'])
def write_comment():
    articles = read_articles()
    if request.method == 'POST':
        article_id = request.form.get('select-article')
        commenter_name = request.form.get('commenter-name', '').strip()
        comment_text = request.form.get('comment-text', '').strip()
        if not (article_id and commenter_name and comment_text):
            error = 'Please fill in all fields.'
            return render_template('write_comment.html', articles=articles, error=error)

        article = next((a for a in articles if a['article_id'] == article_id), None)
        if not article:
            error = 'Selected article not found.'
            return render_template('write_comment.html', articles=articles, error=error)

        comments = read_comments()
        comment_id = str(len(comments) + 1)
        comment_date = datetime.now().strftime('%Y-%m-%d')
        new_comment = {
            'comment_id': comment_id,
            'article_id': article_id,
            'article_title': article['title'],
            'commenter_name': commenter_name,
            'comment_text': comment_text,
            'comment_date': comment_date
        }
        write_comment(new_comment)
        return redirect(url_for('comments'))
    return render_template('write_comment.html', articles=articles)


@app.route('/trending', methods=['GET', 'POST'])
def trending():
    trending = read_trending()
    time_period = request.args.get('time-period-filter', 'This Week')
    filtered_trending = [t for t in trending if t['period'] == time_period]

    # Sort by view_count descending
    filtered_trending.sort(key=lambda x: x['view_count'], reverse=True)

    return render_template('trending.html', trending_list=filtered_trending, time_period=time_period)


@app.route('/category/<category_name>', methods=['GET', 'POST'])
def category(category_name):
    articles = read_articles()
    category_articles = [a for a in articles if a['category'] == category_name]

    sort_by = None
    reverse = False
    if request.method == 'POST':
        sort_by = request.form.get('sort-by', '')
        if sort_by == 'date':
            # Toggle sorting by date
            # We'll check a param to toggle ascending/descending
            toggle = request.form.get('toggle', 'asc')
            reverse = (toggle == 'desc')
            category_articles.sort(key=lambda x: x['date'], reverse=reverse)
        elif sort_by == 'popularity':
            category_articles.sort(key=lambda x: x['views'], reverse=True)

    return render_template('category.html', category_name=category_name, category_articles=category_articles)


if __name__ == '__main__':
    app.run(debug=True)
