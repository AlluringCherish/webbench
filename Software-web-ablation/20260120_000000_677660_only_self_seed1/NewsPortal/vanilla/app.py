from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load and save data files

def load_articles():
    articles = []
    filepath = os.path.join(DATA_DIR, 'articles.txt')
    if not os.path.exists(filepath):
        return articles
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            article_id = int(parts[0])
            title = parts[1]
            author = parts[2]
            category = parts[3]
            content = parts[4]
            date = parts[5]
            try:
                views = int(parts[6])
            except:
                views = 0
            articles.append({
                'article_id': article_id,
                'title': title,
                'author': author,
                'category': category,
                'content': content,
                'date': date,
                'views': views
            })
    return articles

def load_categories():
    categories = []
    filepath = os.path.join(DATA_DIR, 'categories.txt')
    if not os.path.exists(filepath):
        return categories
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            try:
                category_id = int(parts[0])
            except:
                continue
            category_name = parts[1]
            description = parts[2]
            categories.append({
                'category_id': category_id,
                'category_name': category_name,
                'description': description
            })
    return categories

def load_bookmarks():
    bookmarks = []
    filepath = os.path.join(DATA_DIR, 'bookmarks.txt')
    if not os.path.exists(filepath):
        return bookmarks
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 4:
                continue
            try:
                bookmark_id = int(parts[0])
                article_id = int(parts[1])
            except:
                continue
            article_title = parts[2]
            bookmarked_date = parts[3]
            bookmarks.append({
                'bookmark_id': bookmark_id,
                'article_id': article_id,
                'article_title': article_title,
                'bookmarked_date': bookmarked_date
            })
    return bookmarks

def save_bookmarks(bookmarks):
    filepath = os.path.join(DATA_DIR, 'bookmarks.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for bm in bookmarks:
                line = f"{bm['bookmark_id']}|{bm['article_id']}|{bm['article_title']}|{bm['bookmarked_date']}\n"
                f.write(line)
    except Exception:
        pass

def load_comments():
    comments = []
    filepath = os.path.join(DATA_DIR, 'comments.txt')
    if not os.path.exists(filepath):
        return comments
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            try:
                comment_id = int(parts[0])
                article_id = int(parts[1])
            except:
                continue
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
    return comments

def save_comments(comments):
    filepath = os.path.join(DATA_DIR, 'comments.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for cm in comments:
                line = f"{cm['comment_id']}|{cm['article_id']}|{cm['article_title']}|{cm['commenter_name']}|{cm['comment_text']}|{cm['comment_date']}\n"
                f.write(line)
    except Exception:
        pass

def load_trending():
    trending = []
    filepath = os.path.join(DATA_DIR, 'trending.txt')
    if not os.path.exists(filepath):
        return trending
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            try:
                article_id = int(parts[0])
                view_count = int(parts[3])
            except:
                continue
            article_title = parts[1]
            category = parts[2]
            period = parts[4]
            trending.append({
                'article_id': article_id,
                'article_title': article_title,
                'category': category,
                'view_count': view_count,
                'period': period
            })
    return trending


# Route: /
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


# Route: /dashboard
@app.route('/dashboard')
def dashboard_page():
    articles = load_articles()
    trending_articles = load_trending()

    # For featured_articles on dashboard, let's select top 3 by views
    articles_sorted = sorted(articles, key=lambda x: x['views'], reverse=True)
    featured_articles = []
    for art in articles_sorted[:3]:
        featured_articles.append({
            'article_id': art['article_id'],
            'title': art['title'],
            'author': art['author'],
            'date': art['date']
        })

    # trending_articles as loaded

    return render_template('dashboard.html', featured_articles=featured_articles, trending_articles=trending_articles)


# Route: /catalog
@app.route('/catalog')
def article_catalog():
    articles = load_articles()
    categories = load_categories()

    # get query params
    selected_category = request.args.get('category', None)
    search_query = request.args.get('q', None)

    filtered_articles = articles

    # Filter by category if selected
    if selected_category:
        filtered_articles = [a for a in filtered_articles if a['category'].lower() == selected_category.lower()]

    # Filter by search query if present
    if search_query:
        search_lower = search_query.lower()
        filtered_articles = [a for a in filtered_articles if search_lower in a['title'].lower() or
                             search_lower in a['author'].lower() or
                             search_lower in a['content'].lower()]

    # Prepare articles list for context (with excerpt)
    context_articles = []
    for art in filtered_articles:
        excerpt = art['content'][:150] + '...' if len(art['content']) > 150 else art['content']
        context_articles.append({
            'article_id': art['article_id'],
            'title': art['title'],
            'author': art['author'],
            'category': art['category'],
            'date': art['date'],
            'excerpt': excerpt
        })

    return render_template('catalog.html', articles=context_articles, categories=categories,
                           selected_category=selected_category, search_query=search_query)


# Route: /article/<int:article_id>
@app.route('/article/<int:article_id>')
def article_details(article_id):
    articles = load_articles()
    bookmarks = load_bookmarks()

    # find article
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404

    # check if bookmarked
    is_bookmarked = any(bm['article_id'] == article_id for bm in bookmarks)

    return render_template('article_details.html', article=article, is_bookmarked=is_bookmarked)


# Route: /article/<int:article_id>/bookmark POST to bookmark
@app.route('/article/<int:article_id>/bookmark', methods=['POST'])
def bookmark_article(article_id):
    articles = load_articles()
    bookmarks = load_bookmarks()

    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404

    # Check if already bookmarked
    if any(bm['article_id'] == article_id for bm in bookmarks):
        # Already bookmarked, just redirect back to article
        return redirect(url_for('article_details', article_id=article_id))

    # Add bookmark
    bookmark_id = max([bm['bookmark_id'] for bm in bookmarks], default=0) + 1
    bookmarked_date = datetime.now().strftime('%Y-%m-%d')

    new_bm = {
        'bookmark_id': bookmark_id,
        'article_id': article['article_id'],
        'article_title': article['title'],
        'bookmarked_date': bookmarked_date
    }
    bookmarks.append(new_bm)
    save_bookmarks(bookmarks)

    return redirect(url_for('article_details', article_id=article_id))


# Route: /bookmarks
@app.route('/bookmarks')
def bookmarks_page():
    bookmarks = load_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)


# Route: /bookmarks/<int:bookmark_id>/remove POST to remove bookmark
@app.route('/bookmarks/<int:bookmark_id>/remove', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = load_bookmarks()
    bookmarks = [bm for bm in bookmarks if bm['bookmark_id'] != bookmark_id]
    save_bookmarks(bookmarks)
    return redirect(url_for('bookmarks_page'))


# Route: /comments
@app.route('/comments')
def comments_page():
    comments = load_comments()
    articles = load_articles()

    selected_article = request.args.get('article', None)

    filtered_comments = comments
    article_lookup = {a['article_id']: a['title'] for a in articles}

    if selected_article:
        # Filter comments for selected article
        try:
            selected_article_id = int(selected_article)
            filtered_comments = [c for c in comments if c['article_id'] == selected_article_id]
        except:
            filtered_comments = []

    # Compose comments with article_title for context
    context_comments = []
    for c in filtered_comments:
        context_comments.append({
            'comment_id': c['comment_id'],
            'article_id': c['article_id'],
            'article_title': c['article_title'],
            'commenter_name': c['commenter_name'],
            'comment_text': c['comment_text'],
            'comment_date': c['comment_date']
        })

    # Compose articles list for filter dropdown (id and title)
    filter_articles = [{'article_id': a['article_id'], 'title': a['title']} for a in articles]

    return render_template('comments.html', comments=context_comments, articles=filter_articles, selected_article=selected_article)


# Route: /comments/write GET
@app.route('/comments/write', methods=['GET'])
def write_comment_page():
    articles = load_articles()
    articles_list = [{'article_id': a['article_id'], 'title': a['title']} for a in articles]
    return render_template('write_comment.html', articles=articles_list)


# Route: /comments/write POST to submit comment
@app.route('/comments/write', methods=['POST'])
def submit_comment():
    commenter_name = request.form.get('commenter_name', '').strip()
    comment_text = request.form.get('comment_text', '').strip()
    article_id_str = request.form.get('article_id', '').strip()

    if not commenter_name or not comment_text or not article_id_str.isdigit():
        # Missing required fields
        return redirect(url_for('write_comment_page'))

    article_id = int(article_id_str)

    articles = load_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404

    comments = load_comments()
    comment_id = max([c['comment_id'] for c in comments], default=0) + 1
    comment_date = datetime.now().strftime('%Y-%m-%d')

    new_comment = {
        'comment_id': comment_id,
        'article_id': article_id,
        'article_title': article['title'],
        'commenter_name': commenter_name,
        'comment_text': comment_text,
        'comment_date': comment_date
    }
    comments.append(new_comment)
    save_comments(comments)

    return redirect(url_for('comments_page'))


# Route: /trending
@app.route('/trending')
def trending_articles():
    trending = load_trending()
    selected_period = request.args.get('period', 'This Week')

    filtered_trending = [t for t in trending if t['period'].lower() == selected_period.lower()]

    return render_template('trending.html', trending_articles=filtered_trending, selected_period=selected_period)


# Route: /category/<string:category_name>
@app.route('/category/<string:category_name>')
def category_articles(category_name):
    articles = load_articles()

    filtered_articles = [a for a in articles if a['category'].lower() == category_name.lower()]

    context_articles = []
    for art in filtered_articles:
        context_articles.append({
            'article_id': art['article_id'],
            'title': art['title'],
            'author': art['author'],
            'date': art['date'],
            'views': art['views']
        })

    return render_template('category.html', category_name=category_name, articles=context_articles)


# Route: /category/<string:category_name>/sort/<string:sort_by>
@app.route('/category/<string:category_name>/sort/<string:sort_by>')
def sort_category_articles(category_name, sort_by):
    articles = load_articles()

    filtered_articles = [a for a in articles if a['category'].lower() == category_name.lower()]

    if sort_by == 'date':
        # Sort by date descending
        try:
            filtered_articles.sort(key=lambda x: x['date'], reverse=True)
        except:
            pass
    elif sort_by == 'popularity':
        filtered_articles.sort(key=lambda x: x['views'], reverse=True)
    else:
        pass

    context_articles = []
    for art in filtered_articles:
        context_articles.append({
            'article_id': art['article_id'],
            'title': art['title'],
            'author': art['author'],
            'date': art['date'],
            'views': art['views']
        })

    return render_template('category.html', category_name=category_name, articles=context_articles, sort_by=sort_by)


# Route: /search
@app.route('/search')
def search_results():
    search_query = request.args.get('q', '')
    articles = load_articles()

    results = []
    if search_query:
        search_lower = search_query.lower()
        for art in articles:
            if (search_lower in art['title'].lower() or 
                search_lower in art['content'].lower() or 
                search_lower in art['author'].lower()):
                excerpt = art['content'][:150] + '...' if len(art['content']) > 150 else art['content']
                results.append({
                    'article_id': art['article_id'],
                    'title': art['title'],
                    'excerpt': excerpt
                })

    return render_template('search_results.html', search_query=search_query, results=results)


if __name__ == '__main__':
    app.run(debug=True)
