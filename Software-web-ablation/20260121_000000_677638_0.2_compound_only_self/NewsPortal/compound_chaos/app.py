from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_dir = 'data'

def ensure_data_files():
    os.makedirs(data_dir, exist_ok=True)
    files_and_contents = {
        'articles.txt': (
            "1|First News Article|John Doe|Technology|This is the content of the first news article.|2024-06-01|150\n"
            "2|Second News Article|Jane Doe|Health|This is the content of the second news article, which is longer and has more details.|2024-06-02|300\n"
            "3|Third News Article|John Smith|Sports|Summary and details about the third news article related to sports.|2024-06-03|200\n"
        ),
        'categories.txt': (
            "1|Technology|Articles related to technology trends and news.\n"
            "2|Health|Health and wellness related articles.\n"
            "3|Sports|Sports news and updates.\n"
        ),
        'bookmarks.txt': (
            "1|2|Second News Article|2024-06-05\n"
        ),
        'comments.txt': (
            "1|1|First News Article|Alice|Great article on technology!|2024-06-06\n"
            "2|2|Second News Article|Bob|Very informative and helpful.|2024-06-07\n"
        ),
        'trending.txt': (
            "1|First News Article|Technology|150|This Week\n"
            "2|Second News Article|Health|300|This Week\n"
            "3|Third News Article|Sports|200|This Week\n"
        )
    }
    for filename, content in files_and_contents.items():
        path = os.path.join(data_dir, filename)
        if not os.path.isfile(path):
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

ensure_data_files()

def read_articles():
    articles = []
    try:
        with open(os.path.join(data_dir, 'articles.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                article_id, title, author, category, content, date, views = parts
                articles.append({
                    'article_id': article_id,
                    'title': title,
                    'author': author,
                    'category': category,
                    'content': content,
                    'date': date,
                    'views': int(views)
                })
    except FileNotFoundError:
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
                if len(parts) != 3:
                    continue
                category_id, category_name, description = parts
                categories.append({
                    'category_id': category_id,
                    'category_name': category_name,
                    'description': description
                })
    except FileNotFoundError:
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
                if len(parts) != 4:
                    continue
                bookmark_id, article_id, article_title, bookmarked_date = parts
                bookmarks.append({
                    'bookmark_id': bookmark_id,
                    'article_id': article_id,
                    'article_title': article_title,
                    'bookmarked_date': bookmarked_date
                })
    except FileNotFoundError:
        pass
    return bookmarks

def write_bookmarks(bookmarks):
    try:
        with open(os.path.join(data_dir, 'bookmarks.txt'), 'w', encoding='utf-8') as f:
            for b in bookmarks:
                line = '|'.join([
                    b['bookmark_id'],
                    b['article_id'],
                    b['article_title'],
                    b['bookmarked_date']
                ])
                f.write(line + '\n')
    except Exception:
        pass

def read_comments():
    comments = []
    try:
        with open(os.path.join(data_dir, 'comments.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                comment_id, article_id, article_title, commenter_name, comment_text, comment_date = parts
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

def write_comments(comments):
    try:
        with open(os.path.join(data_dir, 'comments.txt'), 'w', encoding='utf-8') as f:
            for c in comments:
                line = '|'.join([
                    c['comment_id'],
                    c['article_id'],
                    c['article_title'],
                    c['commenter_name'],
                    c['comment_text'],
                    c['comment_date']
                ])
                f.write(line + '\n')
    except Exception:
        pass

def read_trending():
    trending = []
    try:
        with open(os.path.join(data_dir, 'trending.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                article_id, article_title, category, view_count, period = parts
                trending.append({
                    'article_id': article_id,
                    'title': article_title,
                    'category': category,
                    'view_count': int(view_count),
                    'period': period
                })
    except FileNotFoundError:
        pass
    return trending

def get_article_by_id(article_id):
    articles = read_articles()
    for article in articles:
        if article['article_id'] == article_id:
            return article
    return None

def get_category_by_id(category_id):
    categories = read_categories()
    for category in categories:
        if category['category_id'] == category_id:
            return category
    return None

@app.route('/')
def root():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    articles = read_articles()
    sorted_by_views = sorted(articles, key=lambda a: a['views'], reverse=True)
    featured_articles = []
    for art in sorted_by_views[:3]:
        featured_articles.append({
            'article_id': art['article_id'],
            'title': art['title'],
            'author': art['author'],
            'date': art['date'],
            'category': art['category']
        })

    trending_data = read_trending()
    trending_articles = []
    for tr in trending_data:
        trending_articles.append({
            'article_id': tr['article_id'],
            'title': tr['title'],
            'category': tr['category'],
            'view_count': tr['view_count']
        })

    return render_template('dashboard.html', featured_articles=featured_articles, trending_articles=trending_articles)

@app.route('/catalog')
def article_catalog():
    articles = read_articles()
    categories = read_categories()

    selected_category = request.args.get('category')
    search_query = request.args.get('search')

    filtered_articles = articles

    if selected_category:
        filtered_articles = [a for a in filtered_articles if a['category'] == selected_category]

    if search_query:
        sq = search_query.lower()
        filtered_articles = [a for a in filtered_articles if
                             sq in a['title'].lower() or
                             sq in a['author'].lower() or
                             sq in a['content'].lower()]

    articles_context = []
    for a in filtered_articles:
        snippet = a['content'][:100] + ('...' if len(a['content']) > 100 else '')
        articles_context.append({
            'article_id': a['article_id'],
            'title': a['title'],
            'author': a['author'],
            'date': a['date'],
            'category': a['category'],
            'snippet': snippet
        })

    return render_template('catalog.html', articles=articles_context, categories=categories,
                           selected_category=selected_category, search_query=search_query)

@app.route('/article/<article_id>', methods=['GET', 'POST'])
def article_detail(article_id):
    article = get_article_by_id(article_id)
    if not article:
        return render_template('article_detail.html', article=None, is_bookmarked=False)

    if request.method == 'POST':
        bookmarks = read_bookmarks()
        bookmarked = any(b['article_id'] == article_id for b in bookmarks)
        if bookmarked:
            bookmarks = [b for b in bookmarks if b['article_id'] != article_id]
        else:
            used_ids = {int(b['bookmark_id']) for b in bookmarks if b['bookmark_id'].isdigit()}
            new_id = str(max(used_ids) + 1 if used_ids else 1)
            bookmarked_date = datetime.now().strftime('%Y-%m-%d')
            bookmarks.append({
                'bookmark_id': new_id,
                'article_id': article_id,
                'article_title': article['title'],
                'bookmarked_date': bookmarked_date
            })
        write_bookmarks(bookmarks)

    bookmarks = read_bookmarks()
    is_bookmarked = any(b['article_id'] == article_id for b in bookmarks)

    return render_template('article_detail.html', article=article, is_bookmarked=is_bookmarked)

@app.route('/bookmarks', methods=['GET', 'POST'])
def bookmarks_page():
    if request.method == 'POST':
        bookmark_id = request.form.get('bookmark_id')
        if bookmark_id:
            bookmarks = read_bookmarks()
            bookmarks = [b for b in bookmarks if b['bookmark_id'] != bookmark_id]
            write_bookmarks(bookmarks)

    bookmarks = read_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)

@app.route('/comments')
def comments_page():
    articles = read_articles()
    comments = read_comments()

    selected_article_id = request.args.get('article_id')

    filtered_comments = comments
    if selected_article_id:
        filtered_comments = [c for c in filtered_comments if c['article_id'] == selected_article_id]

    return render_template('comments.html', comments=filtered_comments, articles=articles, selected_article_id=selected_article_id)

@app.route('/comments/write/<article_id>', methods=['GET', 'POST'])
def write_comment_page(article_id):
    articles = read_articles()
    article = get_article_by_id(article_id)
    if not article:
        return render_template('write_comment.html', article=None, articles=articles)

    if request.method == 'POST':
        commenter_name = request.form.get('commenter_name')
        comment_text = request.form.get('comment_text')

        if commenter_name and comment_text:
            comments = read_comments()
            used_ids = {int(c['comment_id']) for c in comments if c['comment_id'].isdigit()}
            new_id = str(max(used_ids) + 1 if used_ids else 1)
            comment_date = datetime.now().strftime('%Y-%m-%d')

            comments.append({
                'comment_id': new_id,
                'article_id': article_id,
                'article_title': article['title'],
                'commenter_name': commenter_name,
                'comment_text': comment_text,
                'comment_date': comment_date
            })

            write_comments(comments)

            return redirect(url_for('comments_page', article_id=article_id))

    return render_template('write_comment.html', article=article, articles=articles)

@app.route('/trending')
def trending_page():
    time_period = request.args.get('period', 'This Week')
    trending_data = read_trending()
    filtered_trending = [t for t in trending_data if t['period'] == time_period]

    trending_articles = []
    for tr in filtered_trending:
        trending_articles.append({
            'article_id': tr['article_id'],
            'title': tr['title'],
            'category': tr['category'],
            'view_count': tr['view_count']
        })

    return render_template('trending.html', trending_articles=trending_articles, time_period=time_period)

@app.route('/category/<category_id>')
def category_page(category_id):
    category = get_category_by_id(category_id)
    if not category:
        return render_template('category.html', category=None, articles=[], sort_method='date')

    sort_method = request.args.get('sort', 'date')

    articles = read_articles()
    category_articles = [a for a in articles if a['category'] == category['category_name']]

    if sort_method == 'date':
        category_articles.sort(key=lambda a: a['date'], reverse=True)
    elif sort_method == 'popularity':
        category_articles.sort(key=lambda a: a['views'], reverse=True)

    return render_template('category.html', category=category, articles=category_articles, sort_method=sort_method)

@app.route('/search')
def search_results():
    search_query = request.args.get('q', '')
    articles = read_articles()

    matching_articles = []
    if search_query:
        sq = search_query.lower()
        for a in articles:
            if sq in a['title'].lower() or sq in a['author'].lower() or sq in a['content'].lower():
                snippet = a['content'][:100] + ('...' if len(a['content']) > 100 else '')
                matching_articles.append({
                    'article_id': a['article_id'],
                    'title': a['title'],
                    'author': a['author'],
                    'snippet': snippet
                })

    return render_template('search_results.html', search_query=search_query, matching_articles=matching_articles)


if __name__ == '__main__':
    app.run(debug=True)
