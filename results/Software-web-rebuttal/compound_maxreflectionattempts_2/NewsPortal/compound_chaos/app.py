from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_dir = 'data'

# Utility functions to read and write data

def read_articles():
    articles = []
    try:
        with open(os.path.join(data_dir, 'articles.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
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
    except FileNotFoundError:
        pass
    return articles

def read_categories():
    categories = []
    try:
        with open(os.path.join(data_dir, 'categories.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 3:
                    continue
                category = {
                    'category_id': int(parts[0]),
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
        with open(os.path.join(data_dir, 'bookmarks.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 4:
                    continue
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

def write_bookmarks(bookmarks):
    try:
        with open(os.path.join(data_dir, 'bookmarks.txt'), 'w', encoding='utf-8') as f:
            for bm in bookmarks:
                line = f"{bm['bookmark_id']}|{bm['article_id']}|{bm['article_title']}|{bm['bookmarked_date']}\n"
                f.write(line)
    except Exception:
        pass

def read_comments():
    comments = []
    try:
        with open(os.path.join(data_dir, 'comments.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
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
    except FileNotFoundError:
        pass
    return comments

def write_comments(comments):
    try:
        with open(os.path.join(data_dir, 'comments.txt'), 'w', encoding='utf-8') as f:
            for c in comments:
                line = f"{c['comment_id']}|{c['article_id']}|{c['article_title']}|{c['commenter_name']}|{c['comment_text']}|{c['comment_date']}\n"
                f.write(line)
    except Exception:
        pass

def read_trending():
    trending = []
    try:
        with open(os.path.join(data_dir, 'trending.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                item = {
                    'article_id': int(parts[0]),
                    'article_title': parts[1],
                    'category': parts[2],
                    'view_count': int(parts[3]),
                    'period': parts[4]
                }
                trending.append(item)
    except FileNotFoundError:
        pass
    return trending

# Flask Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    articles = read_articles()
    trending = read_trending()

    # featured_articles: first 5 articles sorted by date descending
    featured_articles_sorted = sorted(articles, key=lambda x: x['date'], reverse=True)[:5]
    featured_articles = []
    for art in featured_articles_sorted:
        featured_articles.append({
            'article_id': art['article_id'],
            'title': art['title'],
            'author': art['author'],
            'category': art['category'],
            'date': art['date'],
            'excerpt': art['content'][:150] if len(art['content']) > 150 else art['content']
        })

    # trending_articles: top 5 trending entries by view_count
    trending_sorted = sorted(trending, key=lambda x: x['view_count'], reverse=True)[:5]
    trending_articles = []
    for t in trending_sorted:
        trending_articles.append({
            'article_id': t['article_id'],
            'title': t['article_title'],
            'category': t['category'],
            'view_count': t['view_count']
        })

    return render_template('dashboard.html', featured_articles=featured_articles, trending_articles=trending_articles)

@app.route('/catalog')
def article_catalog():
    articles = read_articles()
    categories = read_categories()

    # No search or filter applied initially
    search_query = request.args.get('search_query', '').strip()
    selected_category = request.args.get('selected_category', '').strip()

    filtered_articles = articles
    if search_query:
        # Filter articles by search_query in title or content (case insensitive)
        sq_lower = search_query.lower()
        filtered_articles = [a for a in articles if sq_lower in a['title'].lower() or sq_lower in a['content'].lower()]
    if selected_category:
        filtered_articles = [a for a in filtered_articles if a['category'].lower() == selected_category.lower()]

    articles_for_catalog = []
    for art in filtered_articles:
        articles_for_catalog.append({
            'article_id': art['article_id'],
            'title': art['title'],
            'author': art['author'],
            'category': art['category'],
            'date': art['date'],
            'excerpt': art['content'][:150] if len(art['content']) > 150 else art['content']
        })

    categories_for_dropdown = []
    for cat in categories:
        categories_for_dropdown.append({
            'category_id': cat['category_id'],
            'category_name': cat['category_name']
        })

    return render_template('article_catalog.html', articles=articles_for_catalog, categories=categories_for_dropdown, search_query=search_query, selected_category=selected_category)

@app.route('/catalog/search', methods=['POST'])
def catalog_search():
    search_query = request.form.get('search_query', '').strip()
    category_filter = request.form.get('category_filter', '').strip()

    articles = read_articles()
    results = articles
    if search_query:
        sq_lower = search_query.lower()
        results = [a for a in results if sq_lower in a['title'].lower() or sq_lower in a['content'].lower()]
    if category_filter:
        results = [a for a in results if a['category'].lower() == category_filter.lower()]

    results_for_template = []
    for art in results:
        results_for_template.append({
            'article_id': art['article_id'],
            'title': art['title'],
            'excerpt': art['content'][:150] if len(art['content']) > 150 else art['content']
        })

    return render_template('search_results.html', search_query=search_query, results=results_for_template)

@app.route('/article/<int:article_id>')
def article_details(article_id):
    articles = read_articles()
    bookmarks = read_bookmarks()

    article = None
    for art in articles:
        if art['article_id'] == article_id:
            article = art
            break

    if article is None:
        # Could render a 404 page but not specified, redirect dashboard
        return redirect(url_for('dashboard'))

    # Check if bookmarked
    is_bookmarked = any(b['article_id'] == article_id for b in bookmarks)

    return render_template('article_details.html', article=article, is_bookmarked=is_bookmarked)

@app.route('/article/<int:article_id>/bookmark', methods=['POST'])
def bookmark_article(article_id):
    articles = read_articles()
    bookmarks = read_bookmarks()

    article = None
    for art in articles:
        if art['article_id'] == article_id:
            article = art
            break

    if article is None:
        return redirect(url_for('dashboard'))

    # Prevent duplicate bookmarks
    if any(b['article_id'] == article_id for b in bookmarks):
        return redirect(url_for('article_details', article_id=article_id))

    # Determine new bookmark_id
    new_id = max([b['bookmark_id'] for b in bookmarks], default=0) + 1
    today_str = datetime.today().strftime('%Y-%m-%d')

    new_bookmark = {
        'bookmark_id': new_id,
        'article_id': article['article_id'],
        'article_title': article['title'],
        'bookmarked_date': today_str
    }
    bookmarks.append(new_bookmark)
    write_bookmarks(bookmarks)

    return redirect(url_for('article_details', article_id=article_id))

@app.route('/bookmarks')
def bookmarks():
    bookmarks_list = read_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks_list)

@app.route('/bookmarks/remove/<int:bookmark_id>', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks_list = read_bookmarks()
    bookmarks_list = [b for b in bookmarks_list if b['bookmark_id'] != bookmark_id]
    write_bookmarks(bookmarks_list)
    return redirect(url_for('bookmarks'))

@app.route('/comments')
def comments():
    comments_list = read_comments()
    articles = read_articles()

    selected_article = request.args.get('selected_article', '').strip()

    filtered_comments = comments_list
    if selected_article:
        try:
            art_id = int(selected_article)
            filtered_comments = [c for c in comments_list if c['article_id'] == art_id]
        except ValueError:
            filtered_comments = comments_list
    
    # Build article id to title map
    article_id_title_map = {a['article_id']: a['title'] for a in articles}

    comments_for_template = []
    for c in filtered_comments:
        comments_for_template.append({
            'comment_id': c['comment_id'],
            'article_id': c['article_id'],
            'article_title': article_id_title_map.get(c['article_id'], c['article_title']),
            'commenter_name': c['commenter_name'],
            'comment_text': c['comment_text'],
            'comment_date': c['comment_date']
        })

    articles_for_template = []
    for a in articles:
        articles_for_template.append({
            'article_id': a['article_id'],
            'title': a['title']
        })

    return render_template('comments.html', comments=comments_for_template, articles=articles_for_template, selected_article=selected_article if selected_article else None)

@app.route('/comments/filter', methods=['POST'])
def filter_comments():
    selected_article = request.form.get('selected_article', '').strip()
    return redirect(url_for('comments', selected_article=selected_article))

@app.route('/comments/write')
def write_comment_page():
    articles = read_articles()
    articles_for_template = []
    for a in articles:
        articles_for_template.append({
            'article_id': a['article_id'],
            'title': a['title']
        })
    return render_template('write_comment.html', articles=articles_for_template)

@app.route('/comments/submit', methods=['POST'])
def submit_comment():
    articles = read_articles()
    comments_list = read_comments()

    try:
        article_id = int(request.form.get('article_id', '0'))
    except ValueError:
        return redirect(url_for('comments'))
    commenter_name = request.form.get('commenter_name', '').strip()
    comment_text = request.form.get('comment_text', '').strip()

    if article_id == 0 or not commenter_name or not comment_text:
        return redirect(url_for('comments'))

    article = None
    for art in articles:
        if art['article_id'] == article_id:
            article = art
            break

    if article is None:
        return redirect(url_for('comments'))

    new_comment_id = max([c['comment_id'] for c in comments_list], default=0) + 1
    today_str = datetime.today().strftime('%Y-%m-%d')

    new_comment = {
        'comment_id': new_comment_id,
        'article_id': article['article_id'],
        'article_title': article['title'],
        'commenter_name': commenter_name,
        'comment_text': comment_text,
        'comment_date': today_str
    }

    comments_list.append(new_comment)
    write_comments(comments_list)

    return redirect(url_for('comments'))

@app.route('/trending')
def trending_articles():
    trending = read_trending()

    time_period = request.args.get('time_period', '').strip()

    filtered_trending = trending
    if time_period:
        filtered_trending = [t for t in trending if t['period'].lower() == time_period.lower()]

    trending_articles_list = []
    for t in filtered_trending:
        trending_articles_list.append({
            'article_id': t['article_id'],
            'article_title': t['article_title'],
            'category': t['category'],
            'view_count': t['view_count']
        })

    return render_template('trending.html', trending_articles=trending_articles_list, time_period=time_period if time_period else None)

@app.route('/trending/filter', methods=['POST'])
def filter_trending():
    time_period = request.form.get('time_period', '').strip()
    return redirect(url_for('trending_articles', time_period=time_period))

@app.route('/category/<category_name>')
def category_articles(category_name):
    articles = read_articles()

    filtered_articles = [a for a in articles if a['category'].lower() == category_name.lower()]

    # Map articles for template with required fields
    articles_for_template = []
    for art in filtered_articles:
        articles_for_template.append({
            'article_id': art['article_id'],
            'title': art['title'],
            'author': art['author'],
            'date': art['date'],
            'views': art['views']
        })

    return render_template('category.html', category_name=category_name, articles=articles_for_template)

@app.route('/category/<category_name>/sort', methods=['POST'])
def sort_category_articles(category_name):
    sort_option = request.form.get('sort_option', '').strip()
    articles = read_articles()

    filtered_articles = [a for a in articles if a['category'].lower() == category_name.lower()]

    if sort_option == 'date':
        filtered_articles.sort(key=lambda x: x['date'], reverse=True)
    elif sort_option == 'popularity':
        filtered_articles.sort(key=lambda x: x['views'], reverse=True)

    articles_for_template = []
    for art in filtered_articles:
        articles_for_template.append({
            'article_id': art['article_id'],
            'title': art['title'],
            'author': art['author'],
            'date': art['date'],
            'views': art['views']
        })

    return render_template('category.html', category_name=category_name, articles=articles_for_template, sort_option=sort_option)

if __name__ == '__main__':
    app.run(debug=True)
