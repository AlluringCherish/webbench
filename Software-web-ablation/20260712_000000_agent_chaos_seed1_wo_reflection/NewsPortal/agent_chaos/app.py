from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load and save data

def load_articles():
    articles = []
    try:
        with open(os.path.join(DATA_DIR, 'articles.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
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
    except FileNotFoundError:
        pass
    return articles


def load_categories():
    categories = []
    try:
        with open(os.path.join(DATA_DIR, 'categories.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    category = {
                        'category_id': int(parts[0]),
                        'category_name': parts[1],
                        'description': parts[2]
                    }
                    categories.append(category)
    except FileNotFoundError:
        pass
    return categories


def load_bookmarks():
    bookmarks = []
    try:
        with open(os.path.join(DATA_DIR, 'bookmarks.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    bookmark = {
                        'bookmark_id': int(parts[0]),
                        'article_id': int(parts[1]),
                        'article_title': parts[2],
                        'bookmarked_date': parts[3]
                    }
                    bookmarks.append(bookmark)
    except FileNotFoundError:
        pass
    return bookmarks


def save_bookmarks(bookmarks):
    try:
        with open(os.path.join(DATA_DIR, 'bookmarks.txt'), 'w', encoding='utf-8') as f:
            for b in bookmarks:
                f.write(f"{b['bookmark_id']}|{b['article_id']}|{b['article_title']}|{b['bookmarked_date']}\n")
    except OSError:
        pass


def load_comments():
    comments = []
    try:
        with open(os.path.join(DATA_DIR, 'comments.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    comment = {
                        'comment_id': int(parts[0]),
                        'article_id': int(parts[1]),
                        'article_title': parts[2],
                        'commenter_name': parts[3],
                        'comment_text': parts[4],
                        'comment_date': parts[5]
                    }
                    comments.append(comment)
    except FileNotFoundError:
        pass
    return comments


def save_comments(comments):
    try:
        with open(os.path.join(DATA_DIR, 'comments.txt'), 'w', encoding='utf-8') as f:
            for c in comments:
                f.write(f"{c['comment_id']}|{c['article_id']}|{c['article_title']}|{c['commenter_name']}|{c['comment_text']}|{c['comment_date']}\n")
    except OSError:
        pass


def load_trending():
    trending = []
    try:
        with open(os.path.join(DATA_DIR, 'trending.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    entry = {
                        'article_id': int(parts[0]),
                        'article_title': parts[1],
                        'category': parts[2],
                        'view_count': int(parts[3]),
                        'period': parts[4]
                    }
                    trending.append(entry)
    except FileNotFoundError:
        pass
    return trending


# Flask Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    articles = load_articles()
    trending = load_trending()

    featured_articles = sorted(articles, key=lambda x: x['date'], reverse=True)[:5]

    trending_articles = []
    used_ids = {fa['article_id'] for fa in featured_articles}
    for ta in sorted(trending, key=lambda x: x['view_count'], reverse=True):
        if ta['article_id'] not in used_ids:
            trending_articles.append({
                'article_id': ta['article_id'],
                'title': ta['article_title'],
                'author': next((a['author'] for a in articles if a['article_id'] == ta['article_id']), 'Unknown'),
                'date': next((a['date'] for a in articles if a['article_id'] == ta['article_id']), '')
            })
            if len(trending_articles) >= 5:
                break

    return render_template('dashboard.html', featured_articles=featured_articles, trending_articles=trending_articles)

@app.route('/catalog')
def article_catalog_page():
    articles = load_articles()
    categories = load_categories()

    search_query = request.args.get('search', '').lower()
    category_filter = request.args.get('category', '')

    filtered_articles = articles

    if search_query:
        filtered_articles = [a for a in filtered_articles if search_query in a['title'].lower() or search_query in a['content'].lower()]

    if category_filter:
        filtered_articles = [a for a in filtered_articles if a['category'] == category_filter]

    articles_context = [{'article_id': a['article_id'], 'title': a['title'], 'author': a['author'], 'date': a['date']} for a in filtered_articles]

    categories_context = [{'category_id': c['category_id'], 'category_name': c['category_name']} for c in categories]

    return render_template('catalog.html', articles=articles_context, categories=categories_context)

@app.route('/article/<int:article_id>')
def article_details_page(article_id):
    articles = load_articles()
    bookmarks = load_bookmarks()

    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return redirect(url_for('article_catalog_page'))

    is_bookmarked = any(b['article_id'] == article_id for b in bookmarks)

    return render_template('article_details.html', article=article, is_bookmarked=is_bookmarked)

@app.route('/article/<int:article_id>/bookmark', methods=['POST'])
def bookmark_article(article_id):
    articles = load_articles()
    bookmarks = load_bookmarks()

    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return redirect(url_for('article_details_page', article_id=article_id))

    if any(b['article_id'] == article_id for b in bookmarks):
        return redirect(url_for('article_details_page', article_id=article_id))

    new_id = max([b['bookmark_id'] for b in bookmarks], default=0) + 1
    today_str = datetime.now().strftime('%Y-%m-%d')
    new_bookmark = {
        'bookmark_id': new_id,
        'article_id': article_id,
        'article_title': article['title'],
        'bookmarked_date': today_str
    }
    bookmarks.append(new_bookmark)
    save_bookmarks(bookmarks)

    return redirect(url_for('article_details_page', article_id=article_id))

@app.route('/bookmarks')
def bookmarks_page():
    bookmarks = load_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)

@app.route('/bookmarks/<int:bookmark_id>/remove', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = load_bookmarks()
    bookmarks = [b for b in bookmarks if b['bookmark_id'] != bookmark_id]
    save_bookmarks(bookmarks)
    return redirect(url_for('bookmarks_page'))

@app.route('/comments')
def comments_page():
    comments = load_comments()
    articles = load_articles()

    selected_article_id = request.args.get('article_id', None)
    if selected_article_id is not None:
        try:
            selected_article_id = int(selected_article_id)
        except ValueError:
            selected_article_id = None

    filtered_comments = comments
    if selected_article_id is not None:
        filtered_comments = [c for c in comments if c['article_id'] == selected_article_id]

    comments_context = [{'comment_id': c['comment_id'], 'article_title': c['article_title'], 'commenter_name': c['commenter_name'], 'comment_text': c['comment_text']} for c in filtered_comments]

    articles_context = [{'article_id': a['article_id'], 'title': a['title']} for a in articles]

    return render_template('comments.html', comments=comments_context, articles=articles_context, selected_article_id=selected_article_id)

@app.route('/comments/write')
def write_comment_page():
    articles = load_articles()
    articles_context = [{'article_id': a['article_id'], 'title': a['title']} for a in articles]
    return render_template('write_comment.html', articles=articles_context)

@app.route('/comments/submit', methods=['POST'])
def submit_comment():
    commenter_name = request.form.get('commenter_name', '').strip()
    comment_text = request.form.get('comment_text', '').strip()
    article_id_str = request.form.get('article_id', '').strip()

    if not commenter_name or not comment_text or not article_id_str:
        return redirect(url_for('write_comment_page'))

    try:
        article_id = int(article_id_str)
    except ValueError:
        return redirect(url_for('write_comment_page'))

    articles = load_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return redirect(url_for('write_comment_page'))

    comments = load_comments()
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
    save_comments(comments)

    return redirect(url_for('comments_page'))

@app.route('/trending')
def trending_articles_page():
    trending = load_trending()

    time_period = request.args.get('time_period', '')

    filtered_trending = trending
    if time_period:
        filtered_trending = [t for t in trending if t['period'] == time_period]

    trending_articles_context = [{'article_id': t['article_id'], 'article_title': t['article_title'], 'category': t['category'], 'view_count': t['view_count']} for t in filtered_trending]

    return render_template('trending.html', trending_articles=trending_articles_context, time_period=time_period)

@app.route('/category/<string:category_name>')
def category_page(category_name):
    articles = load_articles()

    category_articles = [a for a in articles if a['category'] == category_name]

    sort_by = request.args.get('sort', None)

    if sort_by == 'date':
        category_articles.sort(key=lambda x: x['date'], reverse=True)
    elif sort_by == 'popularity':
        category_articles.sort(key=lambda x: x['views'], reverse=True)

    articles_context = [{'article_id': a['article_id'], 'title': a['title'], 'date': a['date'], 'popularity': a['views']} for a in category_articles]

    return render_template('category.html', category_name=category_name, articles=articles_context)

@app.route('/search')
def search_results_page():
    query = request.args.get('q', '').strip()
    articles = load_articles()

    results = []
    if query:
        lower_query = query.lower()
        for a in articles:
            if lower_query in a['title'].lower() or lower_query in a['content'].lower():
                excerpt = a['content'][:100] + ('...' if len(a['content']) > 100 else '')
                results.append({'article_id': a['article_id'], 'title': a['title'], 'excerpt': excerpt})

    return render_template('search_results.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)
