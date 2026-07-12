from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_dir = 'data'

# Helper functions to load data from text files

def load_users():
    users = []
    path = os.path.join(data_dir, 'users.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    user = {
                        'user_id': parts[0],
                        'username': parts[1],
                        'email': parts[2]
                    }
                    users.append(user)
    except (FileNotFoundError, IOError):
        pass
    return users


def load_posts():
    posts = []
    path = os.path.join(data_dir, 'posts.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    post = {
                        'post_id': parts[0],
                        'user_id': parts[1],
                        'title': parts[2],
                        'content': parts[3]
                    }
                    posts.append(post)
    except (FileNotFoundError, IOError):
        pass
    return posts


def load_comments():
    comments = []
    path = os.path.join(data_dir, 'comments.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    comment = {
                        'comment_id': parts[0],
                        'post_id': parts[1],
                        'user_id': parts[2],
                        'content': parts[3],
                        'timestamp': parts[4]
                    }
                    comments.append(comment)
    except (FileNotFoundError, IOError):
        pass
    return comments


@app.route('/')
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    users = load_users()
    posts = load_posts()
    comments = load_comments()
    return render_template('dashboard.html', users=users, posts=posts, comments=comments)


@app.route('/user/<user_id>')
def user_profile(user_id):
    users = load_users()
    posts = load_posts()
    user = next((u for u in users if u['user_id'] == user_id), None)
    user_posts = [p for p in posts if p['user_id'] == user_id]
    return render_template('user_profile.html', user=user, posts=user_posts)


@app.route('/post/<post_id>')
def post_detail(post_id):
    posts = load_posts()
    comments = load_comments()
    post = next((p for p in posts if p['post_id'] == post_id), None)
    post_comments = [c for c in comments if c['post_id'] == post_id]
    return render_template('post_detail.html', post=post, comments=post_comments)


@app.route('/post/<post_id>/comment', methods=['POST'])
def add_comment(post_id):
    user_id = request.form.get('user_id')
    content = request.form.get('content')
    if not (user_id and content):
        return redirect(url_for('post_detail', post_id=post_id))

    # Load comments
    comments = load_comments()

    # Generate new comment_id
    max_id = 0
    for c in comments:
        try:
            cid = int(c['comment_id'])
            if cid > max_id:
                max_id = cid
        except ValueError:
            continue
    new_comment_id = str(max_id + 1)

    from datetime import datetime
    timestamp = datetime.utcnow().isoformat() + 'Z'

    new_comment = f"{new_comment_id}|{post_id}|{user_id}|{content}|{timestamp}\n"
    path = os.path.join(data_dir, 'comments.txt')
    try:
        with open(path, 'a', encoding='utf-8') as f:
            f.write(new_comment)
    except (FileNotFoundError, IOError):
        pass

    return redirect(url_for('post_detail', post_id=post_id))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
