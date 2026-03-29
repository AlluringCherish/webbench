from flask import Flask, redirect, request, url_for, render_template
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = 'data'

# Functions to load and save data

def load_articles():
    articles = []
    try:
        with open(os.path.join(DATA_DIR, 'articles.txt'), encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
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

def load_categories():
    categories = []
    try:
        with open(os.path.join(DATA_DIR, 'categories.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split('|')
                if len(parts) != 3:
                    continue
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

def load_bookmarks():
    bookmarks = []
    try:
        with open(os.path.join(DATA_DIR, 'bookmarks.txt'), encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split('|')
                if len(parts) != 4:
                    continue
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

def save_bookmarks(bookmarks):
    with open(os.path.join(DATA_DIR, 'bookmarks.txt'), 'w', encoding='utf-8') as f:
        for bm in bookmarks:
            line = f"{bm['bookmark_id']}|{bm['article_id']}|{bm['article_title']}|{bm['bookmarked_date']}\n"
            f.write(line)

def load_comments():
    comments = []
    try:
        with open(os.path.join(DATA_DIR, 'comments.txt'), encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
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

def save_comments(comments):
    with open(os.path.join(DATA_DIR, 'comments.txt'), 'w', encoding='utf-8') as f:
        for cm in comments:
            line = f"{cm['comment_id']}|{cm['article_id']}|{cm['article_title']}|{cm['commenter_name']}|{cm['comment_text']}|{cm['comment_date']}\n"
            f.write(line)

def load_trending():
    trending = []
    try:
        with open(os.path.join(DATA_DIR, 'trending.txt'), encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                article_id = int(parts[0])
                article_title = parts[1]
                category = parts[2]
                view_count = int(parts[3])
                period = parts[4]
                rank = int(parts[5])
                trending.append({
                    'article_id': article_id,
                    'article_title': article_title,
                    'category': category,
                    'view_count': view_count,
                    'period': period,
                    'rank': rank
                })
    except FileNotFoundError:
        pass
    return trending

@app.route('/')
def home_route():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    articles = load_articles()
    featured_articles = sorted(articles, key=lambda x: x['views'], reverse=True)[:5]

    trending = load_trending()
    trending_articles = [
        {
            'article_id': t['article_id'],
            'title': t['article_title'],
            'category': t['category'],
            'view_count': t['view_count']
        }
        for t in trending if t['period'] == 'Today'
    ]

    return render_template('dashboard.html',
                           featured_articles=featured_articles,
                           trending_articles=trending_articles)

@app.route('/catalog')
def catalog():
    categories = load_categories()
    articles = load_articles()
    articles_context = [
        {
            'article_id': a['article_id'],
            'title': a['title'],
            'author': a['author'],
            'date': a['date'],
            'category': a['category'],
            'thumbnail': ''  # Placeholder thumbnail
        }
        for a in articles
    ]
    categories_context = [
        {
            'category_id': c['category_id'],
            'category_name': c['category_name']
        }
        for c in categories
    ]
    return render_template('catalog.html', articles=articles_context, categories=categories_context)

@app.route('/search')
def search():
    search_query = request.args.get('q', '')
    articles = load_articles()
    results = []
    if search_query:
        lower_query = search_query.lower()
        for a in articles:
            if (lower_query in a['title'].lower() or
                lower_query in a['author'].lower() or
                lower_query in a['content'].lower()):
                excerpt = a['content'][:100] + ('...' if len(a['content']) > 100 else '')
                results.append({
                    'article_id': a['article_id'],
                    'title': a['title'],
                    'excerpt': excerpt
                })
    return render_template('search_results.html', query=search_query, results=results)

@app.route('/articles/<int:article_id>')
def article_details(article_id):
    articles = load_articles()
    bookmarks = load_bookmarks()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if article is None:
        return "Article not found", 404
    bookmarked = any(bm['article_id'] == article_id for bm in bookmarks)
    article_dict = {
        'article_id': article['article_id'],
        'title': article['title'],
        'author': article['author'],
        'date': article['date'],
        'content': article['content']
    }
    return render_template('article_details.html', article=article_dict, bookmarked=bookmarked)

@app.route('/articles/<int:article_id>/bookmark', methods=['POST'])
def bookmark_article(article_id):
    articles = load_articles()
    bookmarks = load_bookmarks()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if article is None:
        return "Article not found", 404
    for bm in bookmarks:
        if bm['article_id'] == article_id:
            # Remove bookmark
            bookmarks.remove(bm)
            save_bookmarks(bookmarks)
            return redirect(url_for('article_details', article_id=article_id))
    new_id = max((bm['bookmark_id'] for bm in bookmarks), default=0) + 1
    today_str = datetime.now().strftime('%Y-%m-%d')
    new_bm = {
        'bookmark_id': new_id,
        'article_id': article_id,
        'article_title': article['title'],
        'bookmarked_date': today_str
    }
    bookmarks.append(new_bm)
    save_bookmarks(bookmarks)
    return redirect(url_for('article_details', article_id=article_id))

@app.route('/bookmarks')
def bookmarks_view():
    bookmarks = load_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)

@app.route('/bookmarks/<int:bookmark_id>/remove')
def remove_bookmark(bookmark_id):
    bookmarks = load_bookmarks()
    bookmarks = [bm for bm in bookmarks if bm['bookmark_id'] != bookmark_id]
    save_bookmarks(bookmarks)
    return redirect(url_for('bookmarks_view'))

@app.route('/comments')
def comments():
    comments = load_comments()
    articles = load_articles()
    comments_context = [
        {
            'comment_id': c['comment_id'],
            'article_title': c['article_title'],
            'commenter_name': c['commenter_name'],
            'comment_text': c['comment_text']
        }
        for c in comments
    ]
    articles_context = [
        {
            'article_id': a['article_id'],
            'title': a['title']
        }
        for a in articles
    ]
    return render_template('comments.html', comments=comments_context, articles=articles_context, selected_article_id=None)

@app.route('/comments/filter', methods=['POST'])
def filter_comments():
    filter_article_id = request.form.get('filter-by-article')
    if filter_article_id:
        try:
            filter_article_id = int(filter_article_id)
        except ValueError:
            filter_article_id = None
    else:
        filter_article_id = None
    comments = load_comments()
    articles = load_articles()
    if filter_article_id is not None:
        filtered_comments = [c for c in comments if c['article_id'] == filter_article_id]
    else:
        filtered_comments = comments
    comments_context = [
        {
            'comment_id': c['comment_id'],
            'article_title': c['article_title'],
            'commenter_name': c['commenter_name'],
            'comment_text': c['comment_text']
        }
        for c in filtered_comments
    ]
    articles_context = [
        {
            'article_id': a['article_id'],
            'title': a['title']
        }
        for a in articles
    ]
    selected_article_id = filter_article_id
    return render_template('comments.html', comments=comments_context, articles=articles_context, selected_article_id=selected_article_id)

@app.route('/comments/submit', methods=['POST'])
def submit_comment():
    article_id_str = request.form.get('select-article')
    commenter_name = request.form.get('commenter-name','').strip()
    comment_text = request.form.get('comment-text','').strip()
    try:
        article_id = int(article_id_str)
    except:
        return redirect(url_for('comments'))
    if not commenter_name or not comment_text:
        return redirect(url_for('comments'))
    comments = load_comments()
    articles = load_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if article is None:
        return redirect(url_for('comments'))
    new_id = max((cm['comment_id'] for cm in comments), default=0) + 1
    today_str = datetime.now().strftime('%Y-%m-%d')
    new_comment = {
        'comment_id': new_id,
        'article_id': article_id,
        'article_title': article['title'],
        'commenter_name': commenter_name,
        'comment_text': comment_text,
        'comment_date': today_str
    }
    comments.append(new_comment)
    save_comments(comments)
    return redirect(url_for('comments'))

@app.route('/trending')
def trending_articles():
    trending = load_trending()
    periods = ['Today', 'Week', 'Month']
    default_period = 'Today'
    filtered_trending = [t for t in trending if t['period'] == default_period]
    sorted_trending = sorted(filtered_trending, key=lambda x: x['view_count'], reverse=True)
    trending_articles_list = []
    rank = 1
    for t in sorted_trending:
        trending_articles_list.append({
            'article_id': t['article_id'],
            'title': t['article_title'],
            'category': t['category'],
            'view_count': t['view_count'],
            'rank': rank
        })
        rank += 1
    return render_template('trending.html', trending_articles=trending_articles_list, periods=periods, selected_period=default_period)

@app.route('/trending/filter', methods=['POST'])
def filter_trending():
    time_period = request.form.get('time-period-filter', '').strip()
    trending = load_trending()
    if not time_period:
        time_period = 'Today'
    filtered = [t for t in trending if t['period'] == time_period]
    sorted_trending = sorted(filtered, key=lambda x: x['view_count'], reverse=True)
    trending_articles_list = []
    rank = 1
    for t in sorted_trending:
        trending_articles_list.append({
            'article_id': t['article_id'],
            'title': t['article_title'],
            'category': t['category'],
            'view_count': t['view_count'],
            'rank': rank
        })
        rank += 1
    periods = ['Today', 'Week', 'Month']
    return render_template('trending.html', trending_articles=trending_articles_list, periods=periods, selected_period=time_period)

@app.route('/category/<string:category_name>')
def category_articles(category_name):
    articles = load_articles()
    filtered_articles = [a for a in articles if a['category'].lower() == category_name.lower()]
    articles_context = [
        {
            'article_id': a['article_id'],
            'title': a['title'],
            'date': a['date'],
            'popularity': a['views']
        }
        for a in filtered_articles
    ]
    return render_template('category.html', category_name=category_name, articles=articles_context)

@app.route('/category/<string:category_name>/sort/<string:sort_key>')
def sort_category_articles(category_name, sort_key):
    articles = load_articles()
    filtered_articles = [a for a in articles if a['category'].lower() == category_name.lower()]
    if sort_key == 'date':
        sorted_articles = sorted(filtered_articles, key=lambda x: x['date'], reverse=True)
    elif sort_key == 'popularity':
        sorted_articles = sorted(filtered_articles, key=lambda x: x['views'], reverse=True)
    else:
        sorted_articles = filtered_articles
    articles_context = [
        {
            'article_id': a['article_id'],
            'title': a['title'],
            'date': a['date'],
            'popularity': a['views']
        }
        for a in sorted_articles
    ]
    return render_template('category.html', category_name=category_name, articles=articles_context)

if __name__ == '__main__':
    app.run(debug=True)
