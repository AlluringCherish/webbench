from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# Helper functions to read/write data files

def read_articles():
    articles = []
    try:
        with open(os.path.join(DATA_DIR, 'articles.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                category = {
                    'category_id': parts[0],
                    'category_name': parts[1],
                    'description': parts[2]
                }
                categories.append(category)
    except FileNotFoundError:
        pass
    return categories


def read_bookmarks():
    bookmarks = []
    try:
        with open(os.path.join(DATA_DIR, 'bookmarks.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                bookmark = {
                    'bookmark_id': parts[0],
                    'article_id': parts[1],
                    'article_title': parts[2],
                    'bookmarked_date': parts[3]
                }
                bookmarks.append(bookmark)
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
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                comment = {
                    'comment_id': parts[0],
                    'article_id': parts[1],
                    'article_title': parts[2],
                    'commenter_name': parts[3],
                    'comment_text': parts[4],
                    'comment_date': parts[5]
                }
                comments.append(comment)
    except FileNotFoundError:
        pass
    return comments


def write_comments(comments):
    with open(os.path.join(DATA_DIR, 'comments.txt'), 'w', encoding='utf-8') as f:
        for c in comments:
            line = '|'.join([c['comment_id'], c['article_id'], c['article_title'], c['commenter_name'], c['comment_text'], c['comment_date']])
            f.write(line + '\n')


def read_trending():
    trending = []
    try:
        with open(os.path.join(DATA_DIR, 'trending.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                trend = {
                    'article_id': parts[0],
                    'article_title': parts[1],
                    'category': parts[2],
                    'view_count': int(parts[3]),
                    'period': parts[4]
                }
                trending.append(trend)
    except FileNotFoundError:
        pass
    return trending

# Routes and views

@app.route('/')
@app.route('/dashboard')
def dashboard():
    articles = read_articles()
    # Let's consider featured articles as top 3 by views
    featured = sorted(articles, key=lambda x: x['views'], reverse=True)[:3]
    return render_template('dashboard.html', featured_articles=featured)

@app.route('/catalog')
def catalog():
    articles = read_articles()
    categories = read_categories()

    search_query = request.args.get('search', '').strip().lower()
    selected_category = request.args.get('category', '')

    filtered_articles = articles

    if search_query:
        filtered_articles = [a for a in filtered_articles if search_query in a['title'].lower()]
    if selected_category:
        filtered_articles = [a for a in filtered_articles if a['category'] == selected_category]

    return render_template('catalog.html', articles=filtered_articles, categories=categories, search_query=search_query, selected_category=selected_category)

@app.route('/article/<article_id>', methods=['GET', 'POST'])
def article_details(article_id):
    articles = read_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404

    if request.method == 'POST':
        # Bookmark action
        bookmarks = read_bookmarks()
        existing = next((b for b in bookmarks if b['article_id'] == article_id), None)
        if not existing:
            new_id = str(max([int(b['bookmark_id']) for b in bookmarks], default=0) + 1)
            bookmark_date = datetime.now().strftime('%Y-%m-%d')
            bookmarks.append({
                'bookmark_id': new_id,
                'article_id': article_id,
                'article_title': article['title'],
                'bookmarked_date': bookmark_date
            })
            write_bookmarks(bookmarks)
        return redirect(url_for('article_details', article_id=article_id))

    return render_template('article_details.html', article=article)

@app.route('/bookmarks', methods=['GET', 'POST'])
def bookmarks():
    bookmarks = read_bookmarks()
    if request.method == 'POST':
        # Identify which bookmark to remove
        remove_id = request.form.get('remove_id')
        if remove_id:
            bookmarks = [b for b in bookmarks if b['bookmark_id'] != remove_id]
            write_bookmarks(bookmarks)
        return redirect(url_for('bookmarks'))

    return render_template('bookmarks.html', bookmarks=bookmarks)

@app.route('/comments')
def comments():
    comments = read_comments()
    articles = read_articles()
    selected_article = request.args.get('article_id', '')
    filtered_comments = comments
    if selected_article:
        filtered_comments = [c for c in comments if c['article_id'] == selected_article]
    return render_template('comments.html', comments=filtered_comments, articles=articles, selected_article=selected_article)

@app.route('/write-comment', methods=['GET', 'POST'])
def write_comment():
    articles = read_articles()
    if request.method == 'POST':
        article_id = request.form.get('select_article')
        commenter_name = request.form.get('commenter_name')
        comment_text = request.form.get('comment_text')

        article = next((a for a in articles if a['article_id'] == article_id), None)
        if article and commenter_name and comment_text:
            comments = read_comments()
            new_id = str(max([int(c['comment_id']) for c in comments], default=0) + 1)
            comment_date = datetime.now().strftime('%Y-%m-%d')
            comments.append({
                'comment_id': new_id,
                'article_id': article_id,
                'article_title': article['title'],
                'commenter_name': commenter_name,
                'comment_text': comment_text,
                'comment_date': comment_date
            })
            write_comments(comments)
            # Redirect to comments page after submission
            return redirect(url_for('comments'))

    return render_template('write_comment.html', articles=articles)

@app.route('/trending')
def trending():
    trending_data = read_trending()
    time_period = request.args.get('period', '')
    filtered_trending = trending_data
    if time_period:
        filtered_trending = [t for t in trending_data if t['period'] == time_period]
    periods = ['Today','This Week','This Month','This Year']
    return render_template('trending.html', trending=filtered_trending, periods=periods, selected_period=time_period)

@app.route('/category/<category_name>')
def category(category_name):
    articles = read_articles()
    filtered_articles = [a for a in articles if a['category'].lower() == category_name.lower()]

    sort = request.args.get('sort', '')
    if sort == 'date':
        filtered_articles = sorted(filtered_articles, key=lambda x: x['date'], reverse=True)
    elif sort == 'popularity':
        filtered_articles = sorted(filtered_articles, key=lambda x: x['views'], reverse=True)

    return render_template('category.html', category_name=category_name, articles=filtered_articles, sort=sort)

@app.route('/search-results')
def search_results():
    query = request.args.get('query', '').strip().lower()
    articles = read_articles()
    filtered_results = [a for a in articles if query in a['title'].lower()] if query else []
    return render_template('search_results.html', query=query, results=filtered_results)

if __name__ == '__main__':
    app.run(debug=True)
