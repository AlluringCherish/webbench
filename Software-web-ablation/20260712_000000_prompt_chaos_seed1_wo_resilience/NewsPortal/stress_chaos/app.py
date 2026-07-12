from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions for loading data from text files

def load_articles():
    articles = []
    path = os.path.join(DATA_DIR, 'articles.txt')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                article_id, title, author, category, content, date, views = parts
                # Convert types
                try:
                    articles.append({
                        'article_id': int(article_id),
                        'title': title,
                        'author': author,
                        'category': category,
                        'content': content,
                        'date': date,
                        'views': int(views)
                    })
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return articles


def load_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                category_id, category_name, description = parts
                try:
                    categories.append({
                        'category_id': int(category_id),
                        'category_name': category_name
                    })
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return categories


def load_bookmarks():
    bookmarks = []
    path = os.path.join(DATA_DIR, 'bookmarks.txt')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 4:
                    continue
                bookmark_id, article_id, article_title, bookmarked_date = parts
                try:
                    bookmarks.append({
                        'bookmark_id': int(bookmark_id),
                        'article_id': int(article_id),
                        'article_title': article_title,
                        'bookmarked_date': bookmarked_date
                    })
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return bookmarks


def save_bookmarks(bookmarks):
    path = os.path.join(DATA_DIR, 'bookmarks.txt')
    with open(path, 'w', encoding='utf-8') as file:
        for b in bookmarks:
            line = f"{b['bookmark_id']}|{b['article_id']}|{b['article_title']}|{b['bookmarked_date']}\n"
            file.write(line)


def load_comments():
    comments = []
    path = os.path.join(DATA_DIR, 'comments.txt')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                comment_id, article_id, article_title, commenter_name, comment_text, comment_date = parts
                try:
                    comments.append({
                        'comment_id': int(comment_id),
                        'article_id': int(article_id),
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


def save_comments(comments):
    path = os.path.join(DATA_DIR, 'comments.txt')
    with open(path, 'w', encoding='utf-8') as file:
        for c in comments:
            line = f"{c['comment_id']}|{c['article_id']}|{c['article_title']}|{c['commenter_name']}|{c['comment_text']}|{c['comment_date']}\n"
            file.write(line)


def load_trending():
    trending = []
    path = os.path.join(DATA_DIR, 'trending.txt')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                article_id, article_title, category, view_count, period = parts
                try:
                    trending.append({
                        'article_id': int(article_id),
                        'title': article_title,
                        'category': category,
                        'view_count': int(view_count),
                        'period': period
                    })
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return trending


# Route implementations
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    articles = load_articles()
    trending = load_trending()

    # Featured articles: let's consider top 5 by views descending
    featured_articles_sorted = sorted(articles, key=lambda x: x['views'], reverse=True)[:5]
    featured_articles = [{
        'article_id': a['article_id'],
        'title': a['title'],
        'author': a['author'],
        'date': a['date']
    } for a in featured_articles_sorted]

    # Trending articles: use trending data, simplified to article_id and title only
    trending_articles = [{
        'article_id': t['article_id'],
        'title': t['title']
    } for t in trending]

    return render_template('dashboard.html', featured_articles=featured_articles, trending_articles=trending_articles)


@app.route('/articles')
def article_catalog_page():
    articles = load_articles()
    categories = load_categories()

    # Prepare articles list dict
    articles_list = [{
        'article_id': a['article_id'],
        'title': a['title'],
        'author': a['author'],
        'date': a['date'],
        'category': a['category']
    } for a in articles]

    categories_list = [{
        'category_id': c['category_id'],
        'category_name': c['category_name']
    } for c in categories]

    return render_template('article_catalog.html', articles=articles_list, categories=categories_list)


@app.route('/articles/<int:article_id>', methods=['GET', 'POST'])
def article_details_page(article_id):
    articles = load_articles()
    bookmarks = load_bookmarks()

    # Find the article
    article_obj = next((a for a in articles if a['article_id'] == article_id), None)
    if not article_obj:
        # Article not found, handle by showing 404 page or redirect
        return render_template('article_details.html', article=None, is_bookmarked=False)

    if request.method == 'POST':
        # Bookmark action
        # Check if already bookmarked
        already_bookmarked = any(b['article_id'] == article_id for b in bookmarks)
        if not already_bookmarked:
            # Add new bookmark
            new_id = 1
            if bookmarks:
                new_id = max(b['bookmark_id'] for b in bookmarks) + 1
            bookmark = {
                'bookmark_id': new_id,
                'article_id': article_id,
                'article_title': article_obj['title'],
                'bookmarked_date': datetime.now().strftime('%Y-%m-%d')
            }
            bookmarks.append(bookmark)
            save_bookmarks(bookmarks)
        return redirect(url_for('article_details_page', article_id=article_id))

    is_bookmarked = any(b['article_id'] == article_id for b in bookmarks)

    article = {
        'article_id': article_obj['article_id'],
        'title': article_obj['title'],
        'author': article_obj['author'],
        'date': article_obj['date'],
        'content': article_obj['content']
    }

    return render_template('article_details.html', article=article, is_bookmarked=is_bookmarked)


@app.route('/bookmarks', methods=['GET', 'POST'])
def bookmarks_page():
    bookmarks = load_bookmarks()

    if request.method == 'POST':
        # Remove bookmark action
        bookmark_id_str = request.form.get('remove_bookmark_id')
        if bookmark_id_str:
            try:
                remove_id = int(bookmark_id_str)
                bookmarks = [b for b in bookmarks if b['bookmark_id'] != remove_id]
                save_bookmarks(bookmarks)
            except ValueError:
                pass
        return redirect(url_for('bookmarks_page'))

    return render_template('bookmarks.html', bookmarks=bookmarks)


@app.route('/comments')
def comments_page():
    comments = load_comments()
    articles = load_articles()

    articles_list = [{
        'article_id': a['article_id'],
        'title': a['title']
    } for a in articles]

    comments_list = [{
        'comment_id': c['comment_id'],
        'article_id': c['article_id'],
        'article_title': c['article_title'],
        'commenter_name': c['commenter_name'],
        'comment_text': c['comment_text']
    } for c in comments]

    return render_template('comments.html', comments=comments_list, articles=articles_list)


@app.route('/comments/write', methods=['GET', 'POST'])
def write_comment_page():
    articles = load_articles()
    articles_list = [{
        'article_id': a['article_id'],
        'title': a['title']
    } for a in articles]

    if request.method == 'POST':
        article_id_str = request.form.get('article_id')
        commenter_name = request.form.get('commenter_name', '').strip()
        comment_text = request.form.get('comment_text', '').strip()

        if article_id_str and commenter_name and comment_text:
            try:
                article_id = int(article_id_str)
                article_obj = next((a for a in articles if a['article_id'] == article_id), None)
                if article_obj:
                    comments = load_comments()
                    new_id = 1
                    if comments:
                        new_id = max(c['comment_id'] for c in comments) + 1
                    new_comment = {
                        'comment_id': new_id,
                        'article_id': article_id,
                        'article_title': article_obj['title'],
                        'commenter_name': commenter_name,
                        'comment_text': comment_text,
                        'comment_date': datetime.now().strftime('%Y-%m-%d')
                    }
                    comments.append(new_comment)
                    save_comments(comments)
                    return redirect(url_for('comments_page'))
            except ValueError:
                pass

    return render_template('write_comment.html', articles=articles_list)


@app.route('/trending')
def trending_articles_page():
    trending = load_trending()

    trending_articles = [{
        'article_id': t['article_id'],
        'title': t['title'],
        'category': t['category'],
        'view_count': t['view_count'],
        'period': t['period']
    } for t in trending]

    return render_template('trending_articles.html', trending_articles=trending_articles)


@app.route('/category/<string:category_name>')
def category_articles_page(category_name):
    articles = load_articles()

    filter_articles = [
        {
            'article_id': a['article_id'],
            'title': a['title'],
            'date': a['date'],
            'popularity': a['views']
        }
        for a in articles if a['category'].lower() == category_name.lower()
    ]

    return render_template('category.html', category_name=category_name, category_articles=filter_articles)


@app.route('/search')
def search_results_page():
    query = request.args.get('q', '').strip()
    articles = load_articles()

    results = []
    if query:
        query_lower = query.lower()
        for a in articles:
            if query_lower in a['title'].lower() or query_lower in a['content'].lower():
                excerpt = a['content'][:140] + ('...' if len(a['content']) > 140 else '')
                results.append({
                    'article_id': a['article_id'],
                    'title': a['title'],
                    'excerpt': excerpt
                })

    return render_template('search_results.html', query=query, results=results)


if __name__ == '__main__':
    app.run(debug=True)
