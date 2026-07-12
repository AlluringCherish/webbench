from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Util funcs for loading and saving data

def load_articles():
    articles = []
    try:
        with open(os.path.join(DATA_DIR, 'articles.txt'), 'r', encoding='utf-8') as f:
            for line in f:
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
                parts = line.strip().split('|')
                if len(parts) != 3:
                    continue
                category_id = int(parts[0])
                category_name = parts[1]
                # description excluded as not needed in context
                categories.append({
                    'category_id': category_id,
                    'category_name': category_name
                })
    except FileNotFoundError:
        pass
    return categories


def load_bookmarks():
    bookmarks = []
    try:
        with open(os.path.join(DATA_DIR, 'bookmarks.txt'), 'r', encoding='utf-8') as f:
            for line in f:
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
    try:
        with open(os.path.join(DATA_DIR, 'bookmarks.txt'), 'w', encoding='utf-8') as f:
            for bm in bookmarks:
                line = f"{bm['bookmark_id']}|{bm['article_id']}|{bm['article_title']}|{bm['bookmarked_date']}\n"
                f.write(line)
    except Exception:
        pass


def load_comments():
    comments = []
    try:
        with open(os.path.join(DATA_DIR, 'comments.txt'), 'r', encoding='utf-8') as f:
            for line in f:
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
    try:
        with open(os.path.join(DATA_DIR, 'comments.txt'), 'w', encoding='utf-8') as f:
            for c in comments:
                line = f"{c['comment_id']}|{c['article_id']}|{c['article_title']}|{c['commenter_name']}|{c['comment_text']}|{c['comment_date']}\n"
                f.write(line)
    except Exception:
        pass


def load_trending():
    trending = []
    try:
        with open(os.path.join(DATA_DIR, 'trending.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                article_id = int(parts[0])
                article_title = parts[1]
                category = parts[2]
                view_count = int(parts[3])
                period = parts[4]
                trending.append({
                    'article_id': article_id,
                    'article_title': article_title,
                    'category': category,
                    'view_count': view_count,
                    'period': period
                })
    except FileNotFoundError:
        pass
    return trending


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    articles = load_articles()
    categories = load_categories()

    # featured_articles: list of dict with keys article_id:int,title:str,author:str,date:str
    # Choose featured: could be 5 articles with highest views
    featured_articles_sorted = sorted(articles, key=lambda x: x['views'], reverse=True)[:5]
    featured_articles = []
    for art in featured_articles_sorted:
        featured_articles.append({
            'article_id': art['article_id'],
            'title': art['title'],
            'author': art['author'],
            'date': art['date']
        })

    # trending_articles: list of dict with keys article_id,int,title,str,category,str,view_count,int
    trending = load_trending()
    # For dashboard just get latest time period trends or the top by view_count
    # Let's take top 5 trending regardless period
    trending_sorted = sorted(trending, key=lambda x: x['view_count'], reverse=True)[:5]
    trending_articles = []
    for t in trending_sorted:
        trending_articles.append({
            'article_id': t['article_id'],
            'title': t['article_title'],
            'category': t['category'],
            'view_count': t['view_count']
        })

    return render_template('dashboard.html',
                           featured_articles=featured_articles,
                           trending_articles=trending_articles,
                           categories=categories)


@app.route('/catalog', methods=['GET'])
def article_catalog_page():
    articles_all = load_articles()
    categories = load_categories()

    articles = []
    for art in articles_all:
        thumbnail_url = f"/static/thumbnails/{art['article_id']}.jpg"  # Template expects thumbnail_url
        articles.append({
            'article_id': art['article_id'],
            'title': art['title'],
            'author': art['author'],
            'date': art['date'],
            'category': art['category'],
            'thumbnail_url': thumbnail_url
        })

    return render_template('catalog.html', articles=articles, categories=categories)


@app.route('/catalog', methods=['POST'])
def article_catalog_search():
    search_query = request.form.get('search_query', '').strip().lower()
    filter_category = request.form.get('filter_category', '').strip()

    articles_all = load_articles()
    categories = load_categories()

    filtered_articles = []
    for art in articles_all:
        matches_search = (search_query in art['title'].lower()) or (search_query in art['author'].lower()) or (search_query in art['content'].lower())
        matches_category = (filter_category == '' or filter_category == art['category'])
        if (search_query == '' or matches_search) and matches_category:
            thumbnail_url = f"/static/thumbnails/{art['article_id']}.jpg"
            filtered_articles.append({
                'article_id': art['article_id'],
                'title': art['title'],
                'author': art['author'],
                'date': art['date'],
                'category': art['category'],
                'thumbnail_url': thumbnail_url
            })

    return render_template('catalog.html', articles=filtered_articles, categories=categories)


@app.route('/article/<int:article_id>')
def article_details_page(article_id):
    articles = load_articles()
    bookmarks = load_bookmarks()

    article = None
    for art in articles:
        if art['article_id'] == article_id:
            article = art
            break
    if article is None:
        # Could render 404 or redirect dashboard
        return redirect(url_for('dashboard_page'))

    # bookmarked: if article_id in bookmarks
    bookmarked = any(bm['article_id'] == article_id for bm in bookmarks)

    return render_template('article_details.html', article=article, bookmarked=bookmarked)


@app.route('/article/<int:article_id>/bookmark', methods=['POST'])
def bookmark_article(article_id):
    bookmarks = load_bookmarks()
    articles = load_articles()

    # Check if already bookmarked
    if not any(bm['article_id'] == article_id for bm in bookmarks):
        # Find article title
        article_title = None
        for art in articles:
            if art['article_id'] == article_id:
                article_title = art['title']
                break
        if article_title is not None:
            # Determine new bookmark_id
            max_id = max([bm['bookmark_id'] for bm in bookmarks], default=0)
            new_id = max_id + 1
            bookmarked_date = datetime.now().strftime('%Y-%m-%d')
            bookmarks.append({
                'bookmark_id': new_id,
                'article_id': article_id,
                'article_title': article_title,
                'bookmarked_date': bookmarked_date
            })
            save_bookmarks(bookmarks)

    return redirect(url_for('article_details_page', article_id=article_id))


@app.route('/bookmarks')
def bookmarks_page():
    bookmarks = load_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)


@app.route('/bookmarks/<int:bookmark_id>/remove', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = load_bookmarks()
    bookmarks = [bm for bm in bookmarks if bm['bookmark_id'] != bookmark_id]
    save_bookmarks(bookmarks)
    return redirect(url_for('bookmarks_page'))


@app.route('/comments')
def comments_page():
    comments = load_comments()
    articles_all = load_articles()
    # articles as list of dicts with article_id and title
    articles = [{'article_id': art['article_id'], 'title': art['title']} for art in articles_all]
    return render_template('comments.html', comments=comments, articles=articles)


@app.route('/comments/filter', methods=['POST'])
def filter_comments():
    article_id_raw = request.form.get('article_id', '').strip()
    comments = load_comments()
    articles_all = load_articles()
    articles = [{'article_id': art['article_id'], 'title': art['title']} for art in articles_all]

    if article_id_raw == '' or article_id_raw is None:
        filtered_comments = comments
    else:
        try:
            article_id = int(article_id_raw)
            filtered_comments = [c for c in comments if c['article_id'] == article_id]
        except ValueError:
            filtered_comments = comments

    return render_template('comments.html', comments=filtered_comments, articles=articles)


@app.route('/comments/write', methods=['GET'])
def write_comment_page():
    articles_all = load_articles()
    articles = [{'article_id': art['article_id'], 'title': art['title']} for art in articles_all]
    return render_template('write_comment.html', articles=articles)


@app.route('/comments/write', methods=['POST'])
def submit_comment():
    try:
        article_id = int(request.form.get('article_id', '').strip())
        commenter_name = request.form.get('commenter_name', '').strip()
        comment_text = request.form.get('comment_text', '').strip()
        if not commenter_name or not comment_text:
            return redirect(url_for('write_comment_page'))
    except Exception:
        return redirect(url_for('write_comment_page'))

    articles = load_articles()
    article_title = None
    for art in articles:
        if art['article_id'] == article_id:
            article_title = art['title']
            break
    if article_title is None:
        return redirect(url_for('write_comment_page'))

    comments = load_comments()
    max_id = max([c['comment_id'] for c in comments], default=0)
    new_id = max_id + 1
    comment_date = datetime.now().strftime('%Y-%m-%d')
    comments.append({
        'comment_id': new_id,
        'article_id': article_id,
        'article_title': article_title,
        'commenter_name': commenter_name,
        'comment_text': comment_text,
        'comment_date': comment_date
    })
    save_comments(comments)

    return redirect(url_for('comments_page'))


@app.route('/trending')
def trending_articles_page():
    trending = load_trending()
    time_periods = ["Today", "This Week", "This Month"]

    # Choose trending by default to This Week or top
    trending_filtered = [t for t in trending if t['period'] == "This Week"]
    if not trending_filtered:
        trending_filtered = trending  # fallback all

    return render_template('trending.html', trending_articles=trending_filtered, time_periods=time_periods)


@app.route('/trending/filter', methods=['POST'])
def filter_trending():
    time_period = request.form.get('time_period', '').strip()
    trending = load_trending()
    time_periods = ["Today", "This Week", "This Month"]

    if time_period not in time_periods:
        filtered = trending
    else:
        filtered = [t for t in trending if t['period'] == time_period]

    return render_template('trending.html', trending_articles=filtered, time_periods=time_periods)


@app.route('/category/<string:category_name>')
def category_page(category_name):
    articles = load_articles()

    # Filter by category name
    filtered = [a for a in articles if a['category'] == category_name]

    articles_list = []
    for art in filtered:
        articles_list.append({
            'article_id': art['article_id'],
            'title': art['title'],
            'date': art['date'],
            'category': art['category'],
            'views': art['views']
        })

    return render_template('category.html', category_name=category_name, articles=articles_list, sort_method=None)


@app.route('/category/<string:category_name>/sort', methods=['POST'])
def sort_category_articles(category_name):
    sort_method = request.form.get('sort_method', '')
    articles = load_articles()

    filtered = [a for a in articles if a['category'] == category_name]

    if sort_method == 'date':
        # Sort by date descending
        filtered = sorted(filtered, key=lambda a: a['date'], reverse=True)
    elif sort_method == 'popularity':
        # Sort by views descending
        filtered = sorted(filtered, key=lambda a: a['views'], reverse=True)

    articles_list = []
    for art in filtered:
        articles_list.append({
            'article_id': art['article_id'],
            'title': art['title'],
            'date': art['date'],
            'category': art['category'],
            'views': art['views']
        })

    return render_template('category.html', category_name=category_name, articles=articles_list, sort_method=sort_method)


@app.route('/search')
def search_results_page():
    query = request.args.get('query', '').strip().lower()
    articles = load_articles()

    results = []
    for art in articles:
        if query and (query in art['title'].lower() or query in art['content'].lower() or query in art['author'].lower()):
            # excerpt: first 100 chars of content
            excerpt = art['content'][:100]
            results.append({'article_id': art['article_id'], 'title': art['title'], 'excerpt': excerpt})

    return render_template('search_results.html', query=query, results=results)


if __name__ == '__main__':
    app.run(debug=True)
