from flask import Flask, render_template, redirect, url_for, request, abort
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_dir = 'data'

# Utility functions for file operations and parsing

def read_articles():
    articles = []
    try:
        with open(os.path.join(data_dir, 'articles.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                article = {
                    'article_id': int(parts[0]),
                    'title': parts[1],
                    'author': parts[2],
                    'category': parts[3],
                    'content': parts[4],
                    'date': parts[5],
                    'views': int(parts[6])
                }
                articles.append(article)
    except Exception:
        pass
    return articles

def read_categories():
    categories = []
    try:
        with open(os.path.join(data_dir, 'categories.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 3:
                    continue
                category = {
                    'category_id': int(parts[0]),
                    'category_name': parts[1],
                    'description': parts[2]
                }
                categories.append(category)
    except Exception:
        pass
    return categories

def read_bookmarks():
    bookmarks = []
    try:
        with open(os.path.join(data_dir, 'bookmarks.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 4:
                    continue
                bookmark = {
                    'bookmark_id': int(parts[0]),
                    'article_id': int(parts[1]),
                    'article_title': parts[2],
                    'bookmarked_date': parts[3]
                }
                bookmarks.append(bookmark)
    except Exception:
        pass
    return bookmarks

def read_comments():
    comments = []
    try:
        with open(os.path.join(data_dir, 'comments.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 6:
                    continue
                comment = {
                    'comment_id': int(parts[0]),
                    'article_id': int(parts[1]),
                    'article_title': parts[2],
                    'commenter_name': parts[3],
                    'comment_text': parts[4],
                    'comment_date': parts[5]
                }
                comments.append(comment)
    except Exception:
        pass
    return comments

def read_trending():
    trending = []
    try:
        with open(os.path.join(data_dir, 'trending.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 5:
                    continue
                item = {
                    'article_id': int(parts[0]),
                    'title': parts[1],
                    'category': parts[2],
                    'view_count': int(parts[3]),
                    'period': parts[4]
                }
                trending.append(item)
    except Exception:
        pass
    return trending

def write_bookmarks(bookmarks):
    try:
        with open(os.path.join(data_dir, 'bookmarks.txt'), 'w', encoding='utf-8') as f:
            for bm in bookmarks:
                line = f"{bm['bookmark_id']}|{bm['article_id']}|{bm['article_title']}|{bm['bookmarked_date']}\n"
                f.write(line)
    except Exception:
        pass

def write_comments(comments):
    try:
        with open(os.path.join(data_dir, 'comments.txt'), 'w', encoding='utf-8') as f:
            for c in comments:
                line = f"{c['comment_id']}|{c['article_id']}|{c['article_title']}|{c['commenter_name']}|{c['comment_text']}|{c['comment_date']}\n"
                f.write(line)
    except Exception:
        pass


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    articles = read_articles()
    trending = read_trending()
    featured_articles = sorted(articles, key=lambda x: x['date'], reverse=True)[:5]
    categories = read_categories()
    return render_template('dashboard.html', featured_articles=featured_articles, trending_articles=trending, categories=categories)

@app.route('/catalog')
def article_catalog():
    articles = read_articles()
    categories = read_categories()
    search_query = request.args.get('search_query', '')
    selected_category = request.args.get('selected_category', '')

    filtered_articles = articles
    if search_query:
        search_lower = search_query.lower()
        filtered_articles = [a for a in filtered_articles if search_lower in a['title'].lower() or search_lower in a['author'].lower() or search_lower in a['content'].lower()]
    if selected_category:
        filtered_articles = [a for a in filtered_articles if a['category'] == selected_category]

    return render_template('catalog.html', articles=filtered_articles, categories=categories, search_query=search_query, selected_category=selected_category)

@app.route('/catalog/search', methods=['POST'])
def catalog_search():
    search_input = request.form.get('search_input', '')
    category_filter = request.form.get('category_filter', '')

    articles = read_articles()
    categories = read_categories()

    filtered_articles = articles
    if search_input:
        s_lower = search_input.lower()
        filtered_articles = [a for a in filtered_articles if s_lower in a['title'].lower() or s_lower in a['author'].lower() or s_lower in a['content'].lower()]
    if category_filter:
        filtered_articles = [a for a in filtered_articles if a['category'] == category_filter]

    return render_template('catalog.html', articles=filtered_articles, categories=categories, search_query=search_input, selected_category=category_filter)

@app.route('/article/<int:article_id>')
def article_details(article_id):
    articles = read_articles()
    bookmarks = read_bookmarks()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        abort(404)
    is_bookmarked = any(b['article_id'] == article_id for b in bookmarks)
    return render_template('article_details.html', article=article, is_bookmarked=is_bookmarked)

@app.route('/article/<int:article_id>/bookmark', methods=['POST'])
def bookmark_article(article_id):
    articles = read_articles()
    bookmarks = read_bookmarks()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        abort(404)

    bookmark = next((b for b in bookmarks if b['article_id'] == article_id), None)
    if bookmark:
        bookmarks = [b for b in bookmarks if b['article_id'] != article_id]
    else:
        new_id = 1
        if bookmarks:
            new_id = max(b['bookmark_id'] for b in bookmarks) + 1
        bookmarks.append({
            'bookmark_id': new_id,
            'article_id': article_id,
            'article_title': article['title'],
            'bookmarked_date': datetime.now().strftime('%Y-%m-%d')
        })
    write_bookmarks(bookmarks)
    is_bookmarked = not bool(bookmark)
    return render_template('article_details.html', article=article, is_bookmarked=is_bookmarked)

@app.route('/bookmarks')
def bookmarks():
    bookmarks = read_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)

@app.route('/bookmarks/<int:bookmark_id>/remove', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = read_bookmarks()
    bookmarks = [b for b in bookmarks if b['bookmark_id'] != bookmark_id]
    write_bookmarks(bookmarks)
    return render_template('bookmarks.html', bookmarks=bookmarks)

@app.route('/comments')
def comments():
    comments_list = read_comments()
    articles = read_articles()
    return render_template('comments.html', comments=comments_list, articles=articles)

@app.route('/comments/filter', methods=['POST'])
def comments_filter():
    filter_by_article = request.form.get('filter_by_article', 'All')
    comments_list = read_comments()
    articles = read_articles()

    if filter_by_article == 'All':
        filtered_comments = comments_list
        selected_article_id = None
    else:
        try:
            filter_id = int(filter_by_article)
            filtered_comments = [c for c in comments_list if c['article_id'] == filter_id]
            selected_article_id = filter_id
        except ValueError:
            filtered_comments = comments_list
            selected_article_id = None
    return render_template('comments.html', comments=filtered_comments, articles=articles, selected_article_id=selected_article_id)

@app.route('/comments/write', methods=['GET'])
def write_comment():
    articles = read_articles()
    return render_template('write_comment.html', articles=articles)

@app.route('/comments/write', methods=['POST'])
def submit_comment():
    select_article = request.form.get('select_article')
    commenter_name = request.form.get('commenter_name', '').strip()
    comment_text = request.form.get('comment_text', '').strip()
    articles = read_articles()

    submission_success = False
    if select_article and commenter_name and comment_text:
        try:
            article_id = int(select_article)
            article_obj = next((a for a in articles if a['article_id'] == article_id), None)
            if article_obj:
                comments_list = read_comments()
                new_id = 1
                if comments_list:
                    new_id = max(c['comment_id'] for c in comments_list) + 1
                new_comment = {
                    'comment_id': new_id,
                    'article_id': article_id,
                    'article_title': article_obj['title'],
                    'commenter_name': commenter_name,
                    'comment_text': comment_text,
                    'comment_date': datetime.now().strftime('%Y-%m-%d')
                }
                comments_list.append(new_comment)
                write_comments(comments_list)
                submission_success = True
        except ValueError:
            submission_success = False

    return render_template('write_comment.html', submission_success=submission_success, articles=articles)

@app.route('/trending')
def trending_articles():
    trending = read_trending()
    time_period = 'This Week'
    filtered_trending = [t for t in trending if t['period'] == time_period]
    return render_template('trending.html', trending_articles=filtered_trending, time_period=time_period)

@app.route('/trending/filter', methods=['POST'])
def trending_filter():
    time_period_filter = request.form.get('time_period_filter', 'This Week')
    trending = read_trending()
    filtered_trending = [t for t in trending if t['period'] == time_period_filter]
    return render_template('trending.html', trending_articles=filtered_trending, time_period=time_period_filter)

@app.route('/category/<string:category_name>')
def category_articles(category_name):
    articles = read_articles()
    filtered_articles = [a for a in articles if a['category'] == category_name]
    return render_template('category.html', category_name=category_name, articles=filtered_articles)

@app.route('/category/<string:category_name>/sort', methods=['POST'])
def category_sort(category_name):
    sort_order = request.form.get('sort_order', 'date')
    articles = read_articles()
    filtered_articles = [a for a in articles if a['category'] == category_name]
    if sort_order == 'date':
        sorted_articles = sorted(filtered_articles, key=lambda x: x['date'], reverse=True)
    elif sort_order == 'popularity':
        sorted_articles = sorted(filtered_articles, key=lambda x: x['views'], reverse=True)
    else:
        sorted_articles = filtered_articles
    return render_template('category.html', category_name=category_name, articles=sorted_articles)

@app.route('/search/results')
def search_results():
    search_query = request.args.get('search_query', '')
    articles = read_articles()
    search_lower = search_query.lower()
    filtered_articles = [
        {
            'article_id': a['article_id'],
            'title': a['title'],
            'excerpt': (a['content'][:100] + '...') if len(a['content']) > 100 else a['content']
        }
        for a in articles if search_lower in a['title'].lower() or search_lower in a['author'].lower() or search_lower in a['content'].lower()
    ]
    return render_template('search_results.html', search_query=search_query, articles=filtered_articles)


if __name__ == '__main__':
    app.run(debug=True)
