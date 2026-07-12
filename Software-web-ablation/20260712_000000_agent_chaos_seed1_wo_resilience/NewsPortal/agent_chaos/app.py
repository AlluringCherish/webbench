from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions for data handling

def read_authors():
    authors = []
    try:
        with open(os.path.join(DATA_DIR, 'authors.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                # id|name|email
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                authors.append({
                    'id': parts[0],
                    'name': parts[1],
                    'email': parts[2]
                })
    except FileNotFoundError:
        pass
    return authors

def write_authors(authors):
    lines = []
    for a in authors:
        lines.append(f"{a['id']}|{a['name']}|{a['email']}")
    try:
        with open(os.path.join(DATA_DIR, 'authors.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    except FileNotFoundError:
        pass

def read_articles():
    articles = []
    try:
        with open(os.path.join(DATA_DIR, 'articles.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                # id|author_id|title|content|timestamp
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                articles.append({
                    'id': parts[0],
                    'author_id': parts[1],
                    'title': parts[2],
                    'content': parts[3],
                    'timestamp': parts[4],
                })
    except FileNotFoundError:
        pass
    return articles

def write_articles(articles):
    lines = []
    for a in articles:
        lines.append(f"{a['id']}|{a['author_id']}|{a['title']}|{a['content']}|{a['timestamp']}")
    try:
        with open(os.path.join(DATA_DIR, 'articles.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    except FileNotFoundError:
        pass

def read_comments():
    comments = []
    try:
        with open(os.path.join(DATA_DIR, 'comments.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                # id|article_id|author|content|timestamp
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                comments.append({
                    'id': parts[0],
                    'article_id': parts[1],
                    'author': parts[2],
                    'content': parts[3],
                    'timestamp': parts[4]
                })
    except FileNotFoundError:
        pass
    return comments

def write_comments(comments):
    lines = []
    for c in comments:
        lines.append(f"{c['id']}|{c['article_id']}|{c['author']}|{c['content']}|{c['timestamp']}")
    try:
        with open(os.path.join(DATA_DIR, 'comments.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    except FileNotFoundError:
        pass

# Routes

@app.route('/')
def root():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    authors = read_authors()
    articles = read_articles()
    comments = read_comments()
    # Summary counts to pass to dashboard
    context = {
        'authors_count': len(authors),
        'articles_count': len(articles),
        'comments_count': len(comments)
    }
    return render_template('dashboard.html', **context)

@app.route('/authors')
def authors():
    authors = read_authors()
    return render_template('authors.html', authors=authors)

@app.route('/authors/add', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        authors = read_authors()
        new_id = str(max([int(a['id']) for a in authors], default=0) + 1)
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        authors.append({'id': new_id, 'name': name, 'email': email})
        write_authors(authors)
        return redirect(url_for('authors'))
    return render_template('add_author.html')

@app.route('/articles')
def articles():
    articles = read_articles()
    authors = {a['id']: a['name'] for a in read_authors()}
    # Inject author name in articles for display
    for article in articles:
        article['author_name'] = authors.get(article['author_id'], 'Unknown')
    return render_template('articles.html', articles=articles)

@app.route('/articles/add', methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        articles = read_articles()
        authors = read_authors()
        new_id = str(max([int(a['id']) for a in articles], default=0) + 1)
        author_id = request.form.get('author_id', '').strip()
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Validate author_id exists
        if not any(a['id'] == author_id for a in authors):
            return "Invalid author ID", 400
        articles.append({
            'id': new_id,
            'author_id': author_id,
            'title': title,
            'content': content,
            'timestamp': timestamp
        })
        write_articles(articles)
        return redirect(url_for('articles'))
    authors = read_authors()
    return render_template('add_article.html', authors=authors)

@app.route('/comments')
def comments():
    comments = read_comments()
    articles = {a['id']: a['title'] for a in read_articles()}
    # Inject article title in comments for display
    for comment in comments:
        comment['article_title'] = articles.get(comment['article_id'], 'Unknown')
    return render_template('comments.html', comments=comments)

@app.route('/comments/add', methods=['GET', 'POST'])
def add_comment():
    if request.method == 'POST':
        comments = read_comments()
        articles = read_articles()
        new_id = str(max([int(c['id']) for c in comments], default=0) + 1)
        article_id = request.form.get('article_id', '').strip()
        author = request.form.get('author', '').strip()
        content = request.form.get('content', '').strip()
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Validate article_id exists
        if not any(a['id'] == article_id for a in articles):
            return "Invalid article ID", 400
        comments.append({
            'id': new_id,
            'article_id': article_id,
            'author': author,
            'content': content,
            'timestamp': timestamp
        })
        write_comments(comments)
        return redirect(url_for('comments'))
    articles = read_articles()
    return render_template('add_comment.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
