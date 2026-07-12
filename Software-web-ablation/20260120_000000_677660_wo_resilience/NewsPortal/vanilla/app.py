from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Constants for data file paths
DATA_DIR = 'data'
ARTICLES_FILE = os.path.join(DATA_DIR, 'articles.txt')
CATEGORIES_FILE = os.path.join(DATA_DIR, 'categories.txt')
BOOKMARKS_FILE = os.path.join(DATA_DIR, 'bookmarks.txt')
COMMENTS_FILE = os.path.join(DATA_DIR, 'comments.txt')
TRENDING_FILE = os.path.join(DATA_DIR, 'trending.txt')

# Helper functions to read and write data files with strict schema parsing

def read_articles():
    articles = []
    try:
        with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
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
    except FileNotFoundError:
        pass
    except Exception:
        pass
    return articles


def write_articles(articles):
    try:
        with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
            for art in articles:
                line = f"{art['article_id']}|{art['title']}|{art['author']}|{art['category']}|{art['content']}|{art['date']}|{art['views']}\n"
                f.write(line)
    except Exception:
        pass


def read_categories():
    categories = []
    try:
        with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                category_id, category_name, description = parts
                categories.append({
                    'category_id': int(category_id),
                    'category_name': category_name,
                    'description': description
                })
    except FileNotFoundError:
        pass
    except Exception:
        pass
    return categories


def read_bookmarks():
    bookmarks = []
    try:
        with open(BOOKMARKS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 4:
                    continue
                bookmark_id, article_id, article_title, bookmarked_date = parts
                bookmarks.append({
                    'bookmark_id': int(bookmark_id),
                    'article_id': int(article_id),
                    'article_title': article_title,
                    'bookmarked_date': bookmarked_date
                })
    except FileNotFoundError:
        pass
    except Exception:
        pass
    return bookmarks


def write_bookmarks(bookmarks):
    try:
        with open(BOOKMARKS_FILE, 'w', encoding='utf-8') as f:
            for bm in bookmarks:
                line = f"{bm['bookmark_id']}|{bm['article_id']}|{bm['article_title']}|{bm['bookmarked_date']}\n"
                f.write(line)
    except Exception:
        pass


def read_comments():
    comments = []
    try:
        with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                comment_id, article_id, article_title, commenter_name, comment_text, comment_date = parts
                comments.append({
                    'comment_id': int(comment_id),
                    'article_id': int(article_id),
                    'article_title': article_title,
                    'commenter_name': commenter_name,
                    'comment_text': comment_text,
                    'comment_date': comment_date
                })
    except FileNotFoundError:
        pass
    except Exception:
        pass
    return comments


def write_comments(comments):
    try:
        with open(COMMENTS_FILE, 'w', encoding='utf-8') as f:
            for com in comments:
                line = f"{com['comment_id']}|{com['article_id']}|{com['article_title']}|{com['commenter_name']}|{com['comment_text']}|{com['comment_date']}\n"
                f.write(line)
    except Exception:
        pass


def read_trending():
    trending = []
    try:
        with open(TRENDING_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                article_id, article_title, category, view_count, period = parts
                trending.append({
                    'article_id': int(article_id),
                    'article_title': article_title,
                    'category': category,
                    'view_count': int(view_count),
                    'period': period
                })
    except FileNotFoundError:
        pass
    except Exception:
        pass
    return trending

# Routes implementation

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    articles = read_articles()
    trending = read_trending()

    # featured_articles: pick first 5 articles sorted by date descending
    try:
        sorted_articles = sorted(articles, key=lambda x: x['date'], reverse=True)
        featured_articles = [{'article_id': a['article_id'], 'title': a['title'], 'author': a['author'], 'date': a['date']} for a in sorted_articles[:5]]
    except Exception:
        featured_articles = []

    # trending_articles: aggregate trending for latest period available
    try:
        trending_articles = []
        if trending:
            latest_period = trending[-1]['period']
            trending_articles = [
                {'article_id': t['article_id'], 'title': t['article_title'], 'category': t['category'], 'view_count': t['view_count']}
                for t in trending if t['period'] == latest_period
            ]
        else:
            trending_articles = []
    except Exception:
        trending_articles = []

    return render_template('dashboard.html', featured_articles=featured_articles, trending_articles=trending_articles)

@app.route('/catalog')
def article_catalog():
    articles = read_articles()
    categories = read_categories()

    selected_category = request.args.get('category')
    search_query = request.args.get('search')

    filtered_articles = articles
    if selected_category:
        filtered_articles = [a for a in filtered_articles if a['category'].lower() == selected_category.lower()]

    if search_query:
        q = search_query.lower()
        filtered_articles = [a for a in filtered_articles if q in a['title'].lower() or q in a['author'].lower() or q in a['content'].lower()]

    articles_context = [
        {
            'article_id': a['article_id'],
            'title': a['title'],
            'author': a['author'],
            'date': a['date'],
            'category': a['category']
        } for a in filtered_articles
    ]

    return render_template('article_catalog.html', articles=articles_context, categories=categories, selected_category=selected_category if selected_category else None, search_query=search_query if search_query else None)

@app.route('/article/<int:article_id>')
def article_details(article_id):
    articles = read_articles()
    bookmarks = read_bookmarks()

    article = next((a for a in articles if a['article_id'] == article_id), None)
    if article is None:
        return 'Article not found', 404

    is_bookmarked = any(bm['article_id'] == article_id for bm in bookmarks)

    return render_template('article_details.html', article=article, is_bookmarked=is_bookmarked)

@app.route('/article/<int:article_id>/bookmark', methods=['POST'])
def bookmark_article(article_id):
    articles = read_articles()
    bookmarks = read_bookmarks()

    article = next((a for a in articles if a['article_id'] == article_id), None)
    if article is None:
        return 'Article not found.', 404

    if any(bm['article_id'] == article_id for bm in bookmarks):
        return redirect(url_for('article_details', article_id=article_id))

    max_id = max([bm['bookmark_id'] for bm in bookmarks], default=0)
    new_id = max_id + 1
    bookmarked_date = datetime.now().strftime('%Y-%m-%d')

    new_bookmark = {
        'bookmark_id': new_id,
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
    return render_template('bookmarks.html', bookmarks=bookmarks)

@app.route('/bookmarks/<int:bookmark_id>/remove', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = read_bookmarks()
    updated_bookmarks = [bm for bm in bookmarks if bm['bookmark_id'] != bookmark_id]
    write_bookmarks(updated_bookmarks)
    return redirect(url_for('bookmarks'))

@app.route('/comments')
def comments_page():
    comments = read_comments()
    articles = read_articles()

    selected_article_id_param = request.args.get('article_id')
    selected_article_id = None
    try:
        if selected_article_id_param is not None:
            selected_article_id = int(selected_article_id_param)
    except ValueError:
        selected_article_id = None

    filtered_comments = comments
    if selected_article_id is not None:
        filtered_comments = [c for c in comments if c['article_id'] == selected_article_id]

    articles_context = [{'article_id': a['article_id'], 'title': a['title']} for a in articles]

    return render_template('comments.html', comments=filtered_comments, articles=articles_context, selected_article_id=selected_article_id)

@app.route('/comments/write', methods=['GET', 'POST'])
def write_comment():
    articles = read_articles()
    articles_context = [{'article_id': a['article_id'], 'title': a['title']} for a in articles]

    if request.method == 'POST':
        try:
            article_id = int(request.form.get('article_id', 0))
            commenter_name = request.form.get('commenter_name', '').strip()
            comment_text = request.form.get('comment_text', '').strip()

            if article_id == 0 or not commenter_name or not comment_text:
                return render_template('write_comment.html', articles=articles_context)

            articles_all = read_articles()
            article = next((a for a in articles_all if a['article_id'] == article_id), None)
            if article is None:
                return 'Article not found', 404

            comments = read_comments()
            max_id = max([c['comment_id'] for c in comments], default=0)
            new_id = max_id + 1
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

            return redirect(url_for('comments_page'))
        except Exception:
            return render_template('write_comment.html', articles=articles_context)
    else:
        return render_template('write_comment.html', articles=articles_context)

@app.route('/trending')
def trending_articles():
    trending = read_trending()
    time_period_raw = request.args.get('period')

    if time_period_raw and time_period_raw.strip():
        time_period = time_period_raw.strip()
        trending_list = [t for t in trending if t['period'].lower() == time_period.lower()]
    else:
        trending_list = trending
        time_period = None

    return render_template('trending.html', trending_list=trending_list, time_period=time_period if time_period else 'All')

@app.route('/category/<string:category_name>')
def category_articles(category_name):
    articles = read_articles()

    filtered_articles = [a for a in articles if a['category'].lower() == category_name.lower()]

    sort_by = request.args.get('sort')
    if sort_by == 'popularity':
        filtered_articles.sort(key=lambda x: x['views'], reverse=True)
    else:
        filtered_articles.sort(key=lambda x: x['date'], reverse=True)

    articles_context = [
        {
            'article_id': a['article_id'],
            'title': a['title'],
            'author': a['author'],
            'date': a['date'],
            'views': a['views']
        } for a in filtered_articles
    ]

    return render_template('category.html', category_name=category_name, articles=articles_context)

@app.route('/search')
def search_results():
    search_query = request.args.get('q', '').strip()
    articles = read_articles()

    results = []
    if search_query:
        q = search_query.lower()
        for a in articles:
            if q in a['title'].lower():
                excerpt = a['content'][:100] if len(a['content']) > 100 else a['content']
                results.append({'article_id': a['article_id'], 'title': a['title'], 'excerpt': excerpt})

    return render_template('search_results.html', search_query=search_query, results=results)

if __name__ == '__main__':
    app.run(debug=True)
