from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_dir = 'data'

# Utility functions for data loading and saving

def read_articles():
    articles_path = os.path.join(data_dir, 'articles.txt')
    articles = []
    try:
        with open(articles_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
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
    except Exception:
        pass
    return articles

def read_categories():
    categories_path = os.path.join(data_dir, 'categories.txt')
    categories = []
    try:
        with open(categories_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 3:
                    continue
                category = {
                    'category_id': int(parts[0]),
                    'category_name': parts[1],
                    'description': parts[2]
                }
                categories.append(category)
    except Exception:
        pass
    return categories

def read_bookmarks():
    bookmarks_path = os.path.join(data_dir, 'bookmarks.txt')
    bookmarks = []
    try:
        with open(bookmarks_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 4:
                    continue
                bookmark = {
                    'bookmark_id': int(parts[0]),
                    'article_id': int(parts[1]),
                    'article_title': parts[2],
                    'bookmarked_date': parts[3]
                }
                bookmarks.append(bookmark)
    except Exception:
        pass
    return bookmarks

def save_bookmarks(bookmarks):
    bookmarks_path = os.path.join(data_dir, 'bookmarks.txt')
    try:
        with open(bookmarks_path, 'w', encoding='utf-8') as f:
            for bm in bookmarks:
                line = f"{bm['bookmark_id']}|{bm['article_id']}|{bm['article_title']}|{bm['bookmarked_date']}\n"
                f.write(line)
        return True
    except Exception:
        return False

def read_comments():
    comments_path = os.path.join(data_dir, 'comments.txt')
    comments = []
    try:
        with open(comments_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 6:
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
    except Exception:
        pass
    return comments

def save_comments(comments):
    comments_path = os.path.join(data_dir, 'comments.txt')
    try:
        with open(comments_path, 'w', encoding='utf-8') as f:
            for c in comments:
                line = f"{c['comment_id']}|{c['article_id']}|{c['article_title']}|{c['commenter_name']}|{c['comment_text']}|{c['comment_date']}\n"
                f.write(line)
        return True
    except Exception:
        return False

def read_trending():
    trending_path = os.path.join(data_dir, 'trending.txt')
    trending = []
    try:
        with open(trending_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 5:
                    continue
                trending.append({
                    'article_id': int(parts[0]),
                    'article_title': parts[1],
                    'category': parts[2],
                    'view_count': int(parts[3]),
                    'period': parts[4]
                })
    except Exception:
        pass
    return trending


@app.route('/')
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    context = {
        'dashboard_page_id': 'dashboard-page',
        'featured_articles_id': 'featured-articles',
        'browse_articles_button_id': 'browse-articles-button',
        'view_bookmarks_button_id': 'view-bookmarks-button',
        'trending_articles_button_id': 'trending-articles-button'
    }
    return render_template('dashboard.html', **context)


@app.route('/articles')
def article_catalog():
    articles = read_articles()
    context = {
        'catalog_page_id': 'catalog-page',
        'search_input_id': 'search-input',
        'category_filter_id': 'category-filter',
        'articles_grid_id': 'articles-grid',
        'articles': [{
            'article_id': a['article_id'],
            'title': a['title'],
            'author': a['author'],
            'date': a['date'],
            'thumbnail_url': ''  # No thumbnail data available in spec
        } for a in articles]
    }
    return render_template('articles.html', **context)


@app.route('/article/<int:article_id>')
def article_details(article_id):
    articles = read_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        # Article not found, redirect to article catalog
        return redirect(url_for('article_catalog'))
    context = {
        'article_details_page_id': 'article-details-page',
        'article_title': article['title'],
        'article_author': article['author'],
        'article_date': article['date'],
        'article_content': article['content'],
        'bookmark_button_id': 'bookmark-button'
    }
    return render_template('article_details.html', **context)


@app.route('/bookmarks')
def bookmarks_page():
    bookmarks = read_bookmarks()
    context = {
        'bookmarks_page_id': 'bookmarks-page',
        'bookmarks_list': [{
            'bookmark_id': bm['bookmark_id'],
            'article_id': bm['article_id'],
            'article_title': bm['article_title'],
            'bookmarked_date': bm['bookmarked_date']
        } for bm in bookmarks],
        'remove_bookmark_button_id_prefix': 'remove-bookmark-button-',
        'read_bookmark_button_id_prefix': 'read-bookmark-button-',
        'back_to_dashboard_button_id': 'back-to-dashboard'
    }
    return render_template('bookmarks.html', **context)


@app.route('/comments')
def comments_page():
    comments = read_comments()
    context = {
        'comments_page_id': 'comments-page',
        'comments_list': [{
            'article_title': c['article_title'],
            'commenter_name': c['commenter_name'],
            'comment_text': c['comment_text'],
            'comment_date': c['comment_date']
        } for c in comments],
        'write_comment_button_id': 'write-comment-button',
        'filter_by_article_id': 'filter-by-article',
        'back_to_dashboard_button_id': 'back-to-dashboard'
    }
    return render_template('comments.html', **context)


@app.route('/write-comment', methods=['GET', 'POST'])
def write_comment_page():
    if request.method == 'POST':
        commenter_name = request.form.get('commenter_name', '').strip()
        comment_text = request.form.get('comment_text', '').strip()
        article_id_str = request.form.get('article_id', '').strip()
        try:
            article_id = int(article_id_str)
        except ValueError:
            article_id = None

        if not commenter_name or not comment_text or article_id is None:
            # Missing data, re-render GET with articles list
            articles = read_articles()
            context = {
                'write_comment_page_id': 'write-comment-page',
                'articles': [{'article_id': a['article_id'], 'title': a['title']} for a in articles]
            }
            return render_template('write_comment.html', **context)

        # Load existing comments
        comments = read_comments()
        # Load articles to find article title
        articles = read_articles()
        article = next((a for a in articles if a['article_id'] == article_id), None)
        if article is None:
            # Invalid article_id
            context = {
                'write_comment_page_id': 'write-comment-page',
                'articles': [{'article_id': a['article_id'], 'title': a['title']} for a in articles]
            }
            return render_template('write_comment.html', **context)
        # New comment ID
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

    # GET method render page
    articles = read_articles()
    context = {
        'write_comment_page_id': 'write-comment-page',
        'articles': [{'article_id': a['article_id'], 'title': a['title']} for a in articles]
    }
    return render_template('write_comment.html', **context)


@app.route('/trending')
def trending_articles_page():
    trending = read_trending()
    # Sort trending by view_count desc and assign rank
    trending_sorted = sorted(trending, key=lambda x: x['view_count'], reverse=True)
    for i, t in enumerate(trending_sorted, 1):
        t['rank'] = i
    context = {
        'trending_page_id': 'trending-page',
        'trending_articles': [{
            'article_id': t['article_id'],
            'title': t['article_title'],
            'category': t['category'],
            'view_count': t['view_count'],
            'rank': t['rank']
        } for t in trending_sorted],
        'time_period_filter_id': 'time-period-filter',
        'view_article_button_id_prefix': 'view-article-button-',
        'back_to_dashboard_button_id': 'back-to-dashboard'
    }
    return render_template('trending.html', **context)


@app.route('/category/<string:category_name>')
def category_page(category_name):
    articles = read_articles()
    filtered_articles = [
        {
            'article_id': a['article_id'],
            'title': a['title'],
            'author': a['author'],
            'date': a['date']
        }
        for a in articles if a['category'].lower() == category_name.lower()
    ]
    context = {
        'category_page_id': 'category-page',
        'category_name': category_name,
        'category_articles': filtered_articles,
        'sort_by_date_button_id': 'sort-by-date',
        'sort_by_popularity_button_id': 'sort-by-popularity',
        'back_to_dashboard_button_id': 'back-to-dashboard'
    }
    return render_template('category.html', **context)


@app.route('/search-results')
def search_results_page():
    search_query = request.args.get('query', '').strip()
    articles = read_articles()
    results = []
    if search_query:
        lowered = search_query.lower()
        for a in articles:
            if lowered in a['title'].lower() or lowered in a['content'].lower():
                excerpt = a['content'][:100] + ('...' if len(a['content']) > 100 else '')
                results.append({
                    'article_id': a['article_id'],
                    'title': a['title'],
                    'excerpt': excerpt
                })

    context = {
        'search_results_page_id': 'search-results-page',
        'search_query': search_query,
        'results_list': results,
        'no_results_message_id': 'no-results-message',
        'back_to_dashboard_button_id': 'back-to-dashboard'
    }
    return render_template('search_results.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
