from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def load_news():
    news = []
    news_path = os.path.join(DATA_DIR, 'news.txt')
    if not os.path.exists(news_path):
        return news
    with open(news_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            title, date, category, summary, link = parts
            news.append({
                'title': title,
                'date': date,
                'category': category,
                'summary': summary,
                'link': link
            })
    return news


def load_comments():
    comments = []
    comments_path = os.path.join(DATA_DIR, 'comments.txt')
    if not os.path.exists(comments_path):
        return comments
    with open(comments_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 4:
                continue
            news_title, username, comment_text, date = parts
            comments.append({
                'news_title': news_title,
                'username': username,
                'comment_text': comment_text,
                'date': date
            })
    return comments


def load_bookmarks():
    bookmarks = []
    bookmarks_path = os.path.join(DATA_DIR, 'bookmarks.txt')
    if not os.path.exists(bookmarks_path):
        return bookmarks
    with open(bookmarks_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                bookmarks.append(line)
    return bookmarks


def save_bookmarks(bookmarks):
    bookmarks_path = os.path.join(DATA_DIR, 'bookmarks.txt')
    with open(bookmarks_path, 'w', encoding='utf-8') as f:
        for bookmark in bookmarks:
            f.write(bookmark + '\n')


@app.route('/')
def index():
    news = load_news()
    bookmarks = load_bookmarks()
    return render_template('index.html', news=news, bookmarks=bookmarks)


@app.route('/news/<title>')
def news_detail(title):
    news = load_news()
    comments = load_comments()
    news_item = next((item for item in news if item['title'] == title), None)
    if news_item is None:
        return 'News not found', 404
    news_comments = [c for c in comments if c['news_title'] == title]
    return render_template('news_detail.html', news=news_item, comments=news_comments)


@app.route('/bookmark/<title>', methods=['POST'])
def bookmark(title):
    bookmarks = load_bookmarks()
    if title not in bookmarks:
        bookmarks.append(title)
        save_bookmarks(bookmarks)
    return redirect(url_for('index'))


@app.route('/comment/<title>', methods=['POST'])
def comment(title):
    username = request.form.get('username')
    comment_text = request.form.get('comment')
    if not username or not comment_text:
        return redirect(url_for('news_detail', title=title))
    comments_path = os.path.join(DATA_DIR, 'comments.txt')
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(comments_path, 'a', encoding='utf-8') as f:
        f.write(f'{title}|{username}|{comment_text}|{date}\n')
    return redirect(url_for('news_detail', title=title))


@app.route('/trending')
def trending():
    news = load_news()
    trending_news = [item for item in news if 'trending' in item['category'].lower()]
    bookmarks = load_bookmarks()
    return render_template('index.html', news=trending_news, bookmarks=bookmarks)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
