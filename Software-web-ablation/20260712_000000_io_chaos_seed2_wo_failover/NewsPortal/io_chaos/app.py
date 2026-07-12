from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_folder = 'data'

# Helper functions to load and save data for each entity

def load_articles():
    articles = []
    filepath = os.path.join(data_folder, 'articles.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 7:
                        articles.append({
                            'article_id': int(parts[0]),
                            'title': parts[1],
                            'author': parts[2],
                            'category': parts[3],
                            'content': parts[4],
                            'date': parts[5],
                            'views': int(parts[6])
                        })
    except FileNotFoundError:
        pass
    return articles

def load_categories():
    categories = []
    filepath = os.path.join(data_folder, 'categories.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 3:
                        categories.append({
                            'category_id': int(parts[0]),
                            'category_name': parts[1],
                            'description': parts[2]
                        })
    except FileNotFoundError:
        pass
    return categories

def load_bookmarks():
    bookmarks = []
    filepath = os.path.join(data_folder, 'bookmarks.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 4:
                        bookmarks.append({
                            'bookmark_id': int(parts[0]),
                            'article_id': int(parts[1]),
                            'article_title': parts[2],
                            'bookmarked_date': parts[3]
                        })
    except FileNotFoundError:
        pass
    return bookmarks

def load_comments():
    comments = []
    filepath = os.path.join(data_folder, 'comments.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 6:
                        comments.append({
                            'comment_id': int(parts[0]),
                            'article_id': int(parts[1]),
                            'article_title': parts[2],
                            'commenter_name': parts[3],
                            'comment_text': parts[4],
                            'comment_date': parts[5]
                        })
    except FileNotFoundError:
        pass
    return comments

def load_trending():
    trending = []
    filepath = os.path.join(data_folder, 'trending.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 5:
                        trending.append({
                            'article_id': int(parts[0]),
                            'article_title': parts[1],
                            'category': parts[2],
                            'view_count': int(parts[3]),
                            'period': parts[4]
                        })
    except FileNotFoundError:
        pass
    return trending

def save_bookmarks(bookmarks):
    filepath = os.path.join(data_folder, 'bookmarks.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for bm in bookmarks:
            line = f"{bm['bookmark_id']}|{bm['article_id']}|{bm['article_title']}|{bm['bookmarked_date']}\n"
            f.write(line)

def save_comments(comments):
    filepath = os.path.join(data_folder, 'comments.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for c in comments:
            line = f"{c['comment_id']}|{c['article_id']}|{c['article_title']}|{c['commenter_name']}|{c['comment_text']}|{c['comment_date']}\n"
            f.write(line)

# Route: / redirects to /dashboard
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

# Route: /dashboard (GET)
@app.route('/dashboard')
def dashboard_page():
    articles = load_articles()
    # featured_articles: from spec: fields - article_id, title, excerpt, author, date
    # excerpt not stored; We must simulate excerpt from content by slicing first 100 chars or similar
    featured_articles = []
    for art in articles[:5]:
        excerpt = art['content'][:100] + ('...' if len(art['content']) > 100 else '')
        featured_articles.append({
            'article_id': art['article_id'],
            'title': art['title'],
            'excerpt': excerpt,
            'author': art['author'],
            'date': art['date']
        })

    trending = load_trending()
    # trending_articles: fields - article_id, title, category, view_count
    trending_articles = []
    # We'll filter trending for period 'This Week' as a sample? Specification does not mandate filtering
    # We'll just show all trending ignoring period
    for t in trending[:5]:
        trending_articles.append({
            'article_id': t['article_id'],
            'title': t['article_title'],
            'category': t['category'],
            'view_count': t['view_count']
        })

    return render_template('dashboard.html', featured_articles=featured_articles, trending_articles=trending_articles)

# Route: /catalog (GET)
@app.route('/catalog')
def article_catalog():
    articles = load_articles()
    categories = load_categories()
    search_query = request.args.get('q', '')

    # Filter articles by search_query in title or category or author
    if search_query:
        filtered_articles = []
        sq_lower = search_query.lower()
        for art in articles:
            if sq_lower in art['title'].lower() or sq_lower in art['category'].lower() or sq_lower in art['author'].lower():
                filtered_articles.append(art)
        articles = filtered_articles

    # Prepare articles list with excerpt
    articles_for_template = []
    for art in articles:
        excerpt = art['content'][:100] + ('...' if len(art['content']) > 100 else '')
        articles_for_template.append({
            'article_id': art['article_id'],
            'title': art['title'],
            'author': art['author'],
            'category': art['category'],
            'date': art['date'],
            'excerpt': excerpt
        })

    return render_template('catalog.html', articles=articles_for_template, categories=categories, search_query=search_query)

# Route: /article/<int:article_id> (GET)
@app.route('/article/<int:article_id>')
def article_details(article_id):
    articles = load_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404
    return render_template('article_details.html', article=article)

# Route: /article/<int:article_id>/bookmark (POST)
@app.route('/article/<int:article_id>/bookmark', methods=['POST'])
def bookmark_article(article_id):
    articles = load_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404

    bookmarks = load_bookmarks()
    # Check if already bookmarked
    if any(bm['article_id'] == article_id for bm in bookmarks):
        # Already bookmarked, just redirect back
        return redirect(url_for('article_details', article_id=article_id))

    # Assign new bookmark_id
    new_id = 1
    if bookmarks:
        new_id = max(bm['bookmark_id'] for bm in bookmarks) + 1

    new_bookmark = {
        'bookmark_id': new_id,
        'article_id': article['article_id'],
        'article_title': article['title'],
        'bookmarked_date': datetime.now().strftime('%Y-%m-%d')
    }

    bookmarks.append(new_bookmark)
    save_bookmarks(bookmarks)

    return redirect(url_for('article_details', article_id=article_id))

# Route: /bookmarks (GET)
@app.route('/bookmarks')
def bookmarks_page():
    bookmarks = load_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)

# Route: /bookmarks/remove/<int:bookmark_id> (POST)
@app.route('/bookmarks/remove/<int:bookmark_id>', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = load_bookmarks()
    bookmarks = [bm for bm in bookmarks if bm['bookmark_id'] != bookmark_id]
    save_bookmarks(bookmarks)
    return redirect(url_for('bookmarks_page'))

# Route: /comments (GET)
@app.route('/comments')
def comments_page():
    comments = load_comments()
    articles = load_articles()
    # Map to include article_title in comments (should already be present in comments)
    # But ensure latest titles from articles? Spec says comment dict keys include article_title
    # We'll keep as is.
    return render_template('comments.html', comments=comments, articles=[{'article_id':a['article_id'], 'title':a['title']} for a in articles])

# Route: /comments/write (GET)
@app.route('/comments/write')
def write_comment():
    articles = load_articles()
    return render_template('write_comment.html', articles=[{'article_id':a['article_id'], 'title':a['title']} for a in articles])

# Route: /comments/write (POST)
@app.route('/comments/write', methods=['POST'])
def submit_comment():
    article_id_str = request.form.get('article_id')
    commenter_name = request.form.get('commenter_name', '').strip()
    comment_text = request.form.get('comment_text', '').strip()

    if not article_id_str or not commenter_name or not comment_text:
        return "Missing comment form data", 400
    try:
        article_id = int(article_id_str)
    except ValueError:
        return "Invalid article_id", 400

    articles = load_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404

    comments = load_comments()
    new_comment_id = 1
    if comments:
        new_comment_id = max(c['comment_id'] for c in comments) + 1

    new_comment = {
        'comment_id': new_comment_id,
        'article_id': article_id,
        'article_title': article['title'],
        'commenter_name': commenter_name,
        'comment_text': comment_text,
        'comment_date': datetime.now().strftime('%Y-%m-%d')
    }

    comments.append(new_comment)
    save_comments(comments)

    return redirect(url_for('comments_page'))

# Route: /trending (GET)
@app.route('/trending')
def trending_articles():
    trending = load_trending()
    time_period = request.args.get('period', 'This Week')

    filtered = [t for t in trending if t['period'] == time_period]

    # Prepare template trending_articles with keys from spec
    trending_articles = []
    for t in filtered:
        trending_articles.append({
            'article_id': t['article_id'],
            'article_title': t['article_title'],
            'category': t['category'],
            'view_count': t['view_count'],
            'period': t['period']
        })

    return render_template('trending.html', trending_articles=trending_articles, time_period=time_period)

# Route: /category/<string:category_name> (GET)
@app.route('/category/<string:category_name>')
def category_page(category_name):
    articles = load_articles()

    # Optional sorting parameter, by date or popularity
    sort_by = request.args.get('sort', '')

    category_articles = [
        {
            'article_id': a['article_id'],
            'title': a['title'],
            'author': a['author'],
            'date': a['date'],
            'views': a['views']
        }
        for a in articles if a['category'].lower() == category_name.lower()
    ]

    if sort_by == 'date':
        category_articles.sort(key=lambda x: x['date'], reverse=True)
    elif sort_by == 'popularity':
        category_articles.sort(key=lambda x: x['views'], reverse=True)

    return render_template('category.html', category_name=category_name, category_articles=category_articles)

# Route: /search (GET)
@app.route('/search')
def search_results():
    search_query = request.args.get('q', '')
    articles = load_articles()
    search_results = []
    if search_query:
        sq_lower = search_query.lower()
        for art in articles:
            if sq_lower in art['title'].lower() or sq_lower in art['category'].lower() or sq_lower in art['author'].lower():
                excerpt = art['content'][:100] + ('...' if len(art['content']) > 100 else '')
                search_results.append({
                    'article_id': art['article_id'],
                    'title': art['title'],
                    'excerpt': excerpt
                })

    return render_template('search_results.html', search_query=search_query, search_results=search_results)

if __name__ == '__main__':
    app.run(debug=True)
