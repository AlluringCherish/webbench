from flask import Flask, render_template, redirect, url_for, request
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
ARTICLES_FILE = 'data/articles.txt'
CATEGORIES_FILE = 'data/categories.txt'
BOOKMARKS_FILE = 'data/bookmarks.txt'
COMMENTS_FILE = 'data/comments.txt'
TRENDING_FILE = 'data/trending.txt'

# Helper functions for reading and writing data

def load_articles():
    articles = []
    if not os.path.exists(ARTICLES_FILE):
        return articles
    try:
        with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                try:
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
                    continue
    except Exception:
        pass
    return articles

def load_categories():
    categories = []
    if not os.path.exists(CATEGORIES_FILE):
        return categories
    try:
        with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 3:
                    continue
                try:
                    category = {
                        'category_id': int(parts[0]),
                        'category_name': parts[1],
                        'description': parts[2]
                    }
                    categories.append(category)
                except Exception:
                    continue
    except Exception:
        pass
    return categories

def load_bookmarks():
    bookmarks = []
    if not os.path.exists(BOOKMARKS_FILE):
        return bookmarks
    try:
        with open(BOOKMARKS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 4:
                    continue
                try:
                    bookmark = {
                        'bookmark_id': int(parts[0]),
                        'article_id': int(parts[1]),
                        'article_title': parts[2],
                        'bookmarked_date': parts[3]
                    }
                    bookmarks.append(bookmark)
                except Exception:
                    continue
    except Exception:
        pass
    return bookmarks

def load_comments():
    comments = []
    if not os.path.exists(COMMENTS_FILE):
        return comments
    try:
        with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 6:
                    continue
                try:
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
                    continue
    except Exception:
        pass
    return comments

def load_trending():
    trending = []
    if not os.path.exists(TRENDING_FILE):
        return trending
    try:
        with open(TRENDING_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 5:
                    continue
                try:
                    trend = {
                        'article_id': int(parts[0]),
                        'article_title': parts[1],
                        'category': parts[2],
                        'view_count': int(parts[3]),
                        'period': parts[4]
                    }
                    trending.append(trend)
                except Exception:
                    continue
    except Exception:
        pass
    return trending

def save_bookmarks(bookmarks):
    try:
        with open(BOOKMARKS_FILE, 'w', encoding='utf-8') as f:
            for bookmark in bookmarks:
                line = f"{bookmark['bookmark_id']}|{bookmark['article_id']}|{bookmark['article_title']}|{bookmark['bookmarked_date']}"
                f.write(line + '\n')
    except Exception:
        pass

def save_comments(comments):
    try:
        with open(COMMENTS_FILE, 'w', encoding='utf-8') as f:
            for comment in comments:
                line = f"{comment['comment_id']}|{comment['article_id']}|{comment['article_title']}|{comment['commenter_name']}|{comment['comment_text']}|{comment['comment_date']}"
                f.write(line + '\n')
    except Exception:
        pass

# Routes

@app.route('/')
def redirect_to_dashboard():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    # Load articles and trending
    articles = load_articles()

    # featured_articles: list[dict] keys: article_id, title, author, date
    # We will select top 5 by views as featured
    featured_articles_raw = sorted(articles, key=lambda x: x['views'], reverse=True)[:5]
    featured_articles = []
    for a in featured_articles_raw:
        featured_articles.append({
            'article_id': a['article_id'],
            'title': a['title'],
            'author': a['author'],
            'date': a['date']
        })

    trending_raw = load_trending()
    # trending_articles keys: article_id, title, category, views
    trending_articles = []
    # pick trending for 'This Week' if exists else any
    tw_trending = [t for t in trending_raw if t['period'] == 'This Week']
    top_trending = tw_trending if tw_trending else trending_raw
    top_trending_sorted = sorted(top_trending, key=lambda x: x['view_count'], reverse=True)[:5]
    for t in top_trending_sorted:
        trending_articles.append({
            'article_id': t['article_id'],
            'title': t['article_title'],
            'category': t['category'],
            'views': t['view_count']
        })

    return render_template('dashboard.html', featured_articles=featured_articles, trending_articles=trending_articles)

@app.route('/catalog')
def article_catalog():
    articles = load_articles()
    categories = load_categories()
    selected_category = request.args.get('category')
    search_query = request.args.get('search')

    filtered_articles = articles
    if selected_category and selected_category.strip():
        filtered_articles = [a for a in filtered_articles if a['category'] == selected_category.strip()]
    if search_query and search_query.strip():
        sq = search_query.strip().lower()
        filtered_articles = [a for a in filtered_articles if sq in a['title'].lower() or sq in a['content'].lower()]

    # Prepare articles list with required keys
    articles_list = []
    for a in filtered_articles:
        articles_list.append({
            'article_id': a['article_id'],
            'title': a['title'],
            'author': a['author'],
            'date': a['date'],
            'category': a['category']
        })

    # categories list with keys: category_id, category_name
    categories_list = []
    for c in categories:
        categories_list.append({
            'category_id': c['category_id'],
            'category_name': c['category_name']
        })

    return render_template('catalog.html', articles=articles_list, categories=categories_list, selected_category=selected_category, search_query=search_query)

@app.route('/articles/<int:article_id>')
def article_details(article_id):
    articles = load_articles()
    bookmarks = load_bookmarks()

    article = next((a for a in articles if a['article_id'] == article_id), None)
    if article is None:
        # Return 404 or redirect to catalog
        return redirect(url_for('article_catalog'))

    bookmarked = any(b['article_id'] == article_id for b in bookmarks)

    return render_template('article_details.html', article=article, bookmarked=bookmarked)

@app.route('/articles/<int:article_id>/bookmark', methods=['POST'])
def bookmark_article(article_id):
    articles = load_articles()
    bookmarks = load_bookmarks()

    article = next((a for a in articles if a['article_id'] == article_id), None)
    if article is None:
        return redirect(url_for('article_catalog'))

    if not any(b['article_id'] == article_id for b in bookmarks):
        # Add new bookmark
        new_id = max((b['bookmark_id'] for b in bookmarks), default=0) + 1
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        new_bookmark = {
            'bookmark_id': new_id,
            'article_id': article_id,
            'article_title': article['title'],
            'bookmarked_date': today
        }
        bookmarks.append(new_bookmark)
        save_bookmarks(bookmarks)

    return redirect(url_for('article_details', article_id=article_id))

@app.route('/bookmarks')
def bookmarks():
    bookmarks = load_bookmarks()
    # bookmarks keys: bookmark_id, article_id, article_title, bookmarked_date
    return render_template('bookmarks.html', bookmarks=bookmarks)

@app.route('/bookmarks/<int:bookmark_id>/remove', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = load_bookmarks()
    bookmarks = [b for b in bookmarks if b['bookmark_id'] != bookmark_id]
    save_bookmarks(bookmarks)
    return redirect(url_for('bookmarks'))

@app.route('/comments')
def comments():
    comments = load_comments()
    articles = load_articles()
    selected_article_id = request.args.get('article_id', type=int)

    # Map article_id to title
    article_title_map = {a['article_id']: a['title'] for a in articles}

    # Filter comments if selected_article_id
    if selected_article_id:
        filtered_comments = [c for c in comments if c['article_id'] == selected_article_id]
    else:
        filtered_comments = comments

    # Prepare comments list with required keys
    comments_list = []
    for c in filtered_comments:
        comments_list.append({
            'comment_id': c['comment_id'],
            'article_id': c['article_id'],
            'article_title': article_title_map.get(c['article_id'], ''),
            'commenter_name': c['commenter_name'],
            'comment_text': c['comment_text'],
            'comment_date': c['comment_date']
        })

    # Prepare articles list with article_id and title
    articles_list = [{'article_id': a['article_id'], 'title': a['title']} for a in articles]

    return render_template('comments.html', comments=comments_list, articles=articles_list, selected_article_id=selected_article_id)

@app.route('/comments/write', methods=['GET'])
def write_comment():
    articles = load_articles()
    articles_list = [{'article_id': a['article_id'], 'title': a['title']} for a in articles]
    return render_template('write_comment.html', articles=articles_list)

@app.route('/comments/write', methods=['POST'])
def submit_comment():
    articles = load_articles()
    comments = load_comments()
    
    # Retrieve form data
    try:
        article_id = int(request.form.get('article_id', 0))
        commenter_name = request.form.get('commenter_name', '').strip()
        comment_text = request.form.get('comment_text', '').strip()
    except Exception:
        return redirect(url_for('comments'))

    # Validation
    if article_id == 0 or not commenter_name or not comment_text:
        return redirect(url_for('comments'))

    # Find article title
    article_title = None
    for a in articles:
        if a['article_id'] == article_id:
            article_title = a['title']
            break
    if article_title is None:
        return redirect(url_for('comments'))

    new_comment_id = max([c['comment_id'] for c in comments], default=0) + 1
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    new_comment = {
        'comment_id': new_comment_id,
        'article_id': article_id,
        'article_title': article_title,
        'commenter_name': commenter_name,
        'comment_text': comment_text,
        'comment_date': today
    }

    comments.append(new_comment)
    save_comments(comments)

    return redirect(url_for('comments'))

@app.route('/trending')
def trending_articles():
    trending = load_trending()
    time_period = request.args.get('period')

    filtered_trending = trending
    if time_period and time_period.strip():
        filtered_trending = [t for t in trending if t['period'] == time_period.strip()]

    trending_articles_list = []
    for t in filtered_trending:
        trending_articles_list.append({
            'article_id': t['article_id'],
            'article_title': t['article_title'],
            'category': t['category'],
            'view_count': t['view_count'],
            'period': t['period']
        })

    return render_template('trending.html', trending_articles=trending_articles_list, time_period=time_period)

@app.route('/category/<string:category_name>')
def category_articles(category_name):
    articles = load_articles()

    sort_param = request.args.get('sort')

    filtered_articles = [a for a in articles if a['category'] == category_name]

    if sort_param == 'date':
        filtered_articles = sorted(filtered_articles, key=lambda x: x['date'], reverse=True)
    elif sort_param == 'popularity':
        filtered_articles = sorted(filtered_articles, key=lambda x: x['views'], reverse=True)

    articles_list = []
    for a in filtered_articles:
        articles_list.append({
            'article_id': a['article_id'],
            'title': a['title'],
            'author': a['author'],
            'date': a['date'],
            'views': a['views']
        })

    return render_template('category.html', category_name=category_name, articles=articles_list)

@app.route('/search')
def search_results():
    query = request.args.get('query', '')
    articles = load_articles()
    results = []
    q = query.strip().lower()
    if q:
        for a in articles:
            if q in a['title'].lower() or q in a['content'].lower():
                # Create excerpt from content - first 100 chars
                excerpt = a['content'][:100] + ('...' if len(a['content'])>100 else '')
                results.append({
                    'article_id': a['article_id'],
                    'title': a['title'],
                    'excerpt': excerpt
                })

    return render_template('search_results.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)
