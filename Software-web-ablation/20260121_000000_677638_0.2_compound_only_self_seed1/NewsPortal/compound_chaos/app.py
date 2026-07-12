from flask import Flask, render_template, redirect, url_for, request
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Read data files functions

def read_articles():
    articles = []
    path = os.path.join(DATA_DIR, 'articles.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                try:
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
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return articles


def read_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                try:
                    category_id = int(parts[0])
                    category_name = parts[1]
                    description = parts[2]
                    categories.append({
                        'category_id': category_id,
                        'category_name': category_name,
                        'description': description
                    })
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return categories


def read_bookmarks():
    bookmarks = []
    path = os.path.join(DATA_DIR, 'bookmarks.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 4:
                    continue
                try:
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
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return bookmarks


def read_comments():
    comments = []
    path = os.path.join(DATA_DIR, 'comments.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                try:
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
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return comments


def read_trending():
    trending = []
    path = os.path.join(DATA_DIR, 'trending.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                try:
                    article_id = int(parts[0])
                    article_title = parts[1]
                    category = parts[2]
                    view_count = int(parts[3])
                    period = parts[4]
                    trending.append({
                        'article_id': article_id,
                        'title': article_title,
                        'category': category,
                        'view_count': view_count,
                        'period': period
                    })
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return trending

# Write data files functions

def write_bookmarks(bookmarks):
    path = os.path.join(DATA_DIR, 'bookmarks.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for bm in bookmarks:
                f.write(f"{bm['bookmark_id']}|{bm['article_id']}|{bm['article_title']}|{bm['bookmarked_date']}\n")
    except Exception:
        pass

def write_comments(comments):
    path = os.path.join(DATA_DIR, 'comments.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for cm in comments:
                f.write(f"{cm['comment_id']}|{cm['article_id']}|{cm['article_title']}|{cm['commenter_name']}|{cm['comment_text']}|{cm['comment_date']}\n")
    except Exception:
        pass

# Flask Routes

@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    articles = read_articles()

    featured_articles = []
    for art in articles[:5]:
        excerpt = art['content'][:150] if len(art['content']) > 150 else art['content']
        featured_articles.append({
            'article_id': art['article_id'],
            'title': art['title'],
            'author': art['author'],
            'date': art['date'],
            'excerpt': excerpt
        })

    trending_data = read_trending()
    trending_articles = [
        {'article_id': t['article_id'], 'title': t['title'], 'category': t['category'], 'view_count': t['view_count']}
        for t in trending_data if t['period'] == 'This Week'
    ]
    if not trending_articles:
        trending_articles = [
            {'article_id': t['article_id'], 'title': t['title'], 'category': t['category'], 'view_count': t['view_count']}
            for t in trending_data[:5]
        ]

    return render_template('dashboard.html', featured_articles=featured_articles, trending_articles=trending_articles)


@app.route('/catalog', methods=['GET'])
def article_catalog():
    articles = read_articles()
    categories = read_categories()

    search_query = request.args.get('search_query')
    selected_category = request.args.get('selected_category')

    filtered_articles = articles

    if selected_category and selected_category.strip():
        filtered_articles = [a for a in filtered_articles if a['category'] == selected_category]

    if search_query and search_query.strip():
        q = search_query.strip().lower()
        filtered_articles = [a for a in filtered_articles if (q in a['title'].lower() or q in a['author'].lower() or q in a['content'].lower())]

    context_articles = []
    for a in filtered_articles:
        context_articles.append({
            'article_id': a['article_id'],
            'title': a['title'],
            'author': a['author'],
            'date': a['date']
        })

    return render_template('article_catalog.html', articles=context_articles, categories=categories, search_query=search_query, selected_category=selected_category)


@app.route('/article/<int:article_id>', methods=['GET'])
def article_details(article_id):
    articles = read_articles()
    bookmarks = read_bookmarks()

    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return redirect(url_for('article_catalog'))

    is_bookmarked = any(b['article_id'] == article_id for b in bookmarks)

    article_dict = {
        'article_id': article['article_id'],
        'title': article['title'],
        'author': article['author'],
        'date': article['date'],
        'content': article['content']
    }

    return render_template('article_details.html', article=article_dict, is_bookmarked=is_bookmarked)


@app.route('/article/<int:article_id>/bookmark', methods=['POST'])
def bookmark_article(article_id):
    articles = read_articles()
    bookmarks = read_bookmarks()

    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return redirect(url_for('article_catalog'))

    # Check if already bookmarked
    existing = next((b for b in bookmarks if b['article_id'] == article_id), None)

    if not existing:
        new_id = max((b['bookmark_id'] for b in bookmarks), default=0) + 1
        today = datetime.date.today().strftime('%Y-%m-%d')
        bookmarks.append({
            'bookmark_id': new_id,
            'article_id': article['article_id'],
            'article_title': article['title'],
            'bookmarked_date': today
        })
        write_bookmarks(bookmarks)

    return redirect(url_for('article_details', article_id=article_id))


@app.route('/bookmarks', methods=['GET'])
def bookmarks():
    bookmarks = read_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)


@app.route('/bookmarks/<int:bookmark_id>/remove', methods=['POST'])
def remove_bookmark(bookmark_id):
    bookmarks = read_bookmarks()
    bookmarks = [b for b in bookmarks if b['bookmark_id'] != bookmark_id]
    write_bookmarks(bookmarks)
    return redirect(url_for('bookmarks'))


@app.route('/comments', methods=['GET'])
def comments():
    comments = read_comments()
    articles = read_articles()

    selected_article_id = request.args.get('selected_article_id')
    if selected_article_id is not None:
        try:
            selected_article_id = int(selected_article_id)
        except ValueError:
            selected_article_id = None
    else:
        selected_article_id = None

    filtered_comments = comments
    if selected_article_id is not None:
        filtered_comments = [c for c in comments if c['article_id'] == selected_article_id]

    context_articles = [{'article_id': a['article_id'], 'title': a['title']} for a in articles]

    return render_template('comments.html', comments=filtered_comments, articles=context_articles, selected_article_id=selected_article_id)


@app.route('/comments/write', methods=['GET'])
def write_comment():
    articles = read_articles()
    context_articles = [{'article_id': a['article_id'], 'title': a['title']} for a in articles]
    return render_template('write_comment.html', articles=context_articles)


@app.route('/comments/write', methods=['POST'])
def submit_comment():
    select_article_raw = request.form.get('select_article')
    commenter_name = request.form.get('commenter_name', '').strip()
    comment_text = request.form.get('comment_text', '').strip()

    try:
        select_article = int(select_article_raw) if select_article_raw else None
    except ValueError:
        select_article = None

    articles = read_articles()
    article = next((a for a in articles if a['article_id'] == select_article), None)
    if not article or not commenter_name or not comment_text:
        return redirect(url_for('write_comment'))

    comments = read_comments()
    new_id = max((c['comment_id'] for c in comments), default=0) + 1
    today = datetime.date.today().strftime('%Y-%m-%d')

    comments.append({
        'comment_id': new_id,
        'article_id': article['article_id'],
        'article_title': article['title'],
        'commenter_name': commenter_name,
        'comment_text': comment_text,
        'comment_date': today
    })
    write_comments(comments)

    return redirect(url_for('comments'))


@app.route('/trending', methods=['GET'])
def trending_articles():
    trending_list = read_trending()
    time_period = request.args.get('time_period')

    filtered_list = trending_list
    if time_period and time_period.strip():
        filtered_list = [t for t in trending_list if t['period'] == time_period]

    return render_template('trending.html', trending_list=filtered_list, time_period=time_period)


@app.route('/category/<category_name>', methods=['GET'])
def category_page(category_name):
    articles = read_articles()
    filtered_articles = [a for a in articles if a['category'] == category_name]

    context_articles = [{
        'article_id': a['article_id'],
        'title': a['title'],
        'author': a['author'],
        'date': a['date'],
        'views': a['views']
    } for a in filtered_articles]

    return render_template('category.html', category_name=category_name, articles=context_articles)


@app.route('/search', methods=['GET'])
def search_results():
    query = request.args.get('query', '').strip()
    articles = read_articles()

    results = []
    if query:
        q = query.lower()
        for a in articles:
            if q in a['title'].lower() or q in a['content'].lower():
                excerpt = a['content'][:150] if len(a['content']) > 150 else a['content']
                results.append({
                    'article_id': a['article_id'],
                    'title': a['title'],
                    'excerpt': excerpt
                })

    return render_template('search_results.html', query=query, results=results)


if __name__ == '__main__':
    app.run(debug=True)
