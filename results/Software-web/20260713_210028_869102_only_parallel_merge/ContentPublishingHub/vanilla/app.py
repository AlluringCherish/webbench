from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
from collections import defaultdict
import html

app = Flask(__name__, template_folder='templates')
app.secret_key = 'supersecretkey'

data_dir = 'data'

# UTILITIES TO LOAD DATA FROM FILES

def parse_users():
    users = {}
    try:
        with open(os.path.join(data_dir, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 4:
                    username, email, fullname, created_date = parts
                    users[username] = {
                        'username': username,
                        'email': email,
                        'fullname': fullname,
                        'created_date': created_date
                    }
    except FileNotFoundError:
        pass
    return users


def parse_articles():
    articles = {}
    try:
        with open(os.path.join(data_dir, 'articles.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 10:
                    article_id = int(parts[0])
                    articles[article_id] = {
                        'article_id': article_id,
                        'title': parts[1],
                        'author': parts[2],
                        'category': parts[3],
                        'status': parts[4],
                        'tags': parts[5].split(',') if parts[5] else [],
                        'featured_image': parts[6],
                        'meta_description': parts[7],
                        'created_date': parts[8],
                        'publish_date': parts[9]
                    }
    except FileNotFoundError:
        pass
    return articles


def write_articles(articles):
    lines = []
    for a in sorted(articles.values(), key=lambda x: x['article_id']):
        tags_str = ','.join(a['tags']) if isinstance(a['tags'], list) else a['tags']
        line = f"{a['article_id']}|{a['title']}|{a['author']}|{a['category']}|{a['status']}|{tags_str}|{a['featured_image']}|{a['meta_description']}|{a['created_date']}|{a['publish_date']}"
        lines.append(line)
    with open(os.path.join(data_dir, 'articles.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def parse_article_versions():
    versions = []
    try:
        with open(os.path.join(data_dir, 'article_versions.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = []
                current = ''
                escape = False
                for ch in line:
                    if ch == '|' and not escape:
                        parts.append(current)
                        current = ''
                    elif ch == '\\' and not escape:
                        escape = True
                    else:
                        if escape:
                            current += ch
                            escape = False
                        else:
                            current += ch
                parts.append(current)
                if len(parts) == 7:
                    try:
                        version_id = int(parts[0])
                        article_id = int(parts[1])
                        version_number = int(parts[2])
                        content = parts[3]
                        author = parts[4]
                        created_date = parts[5]
                        change_summary = parts[6]
                        versions.append({
                            'version_id': version_id,
                            'article_id': article_id,
                            'version_number': version_number,
                            'content': content,
                            'author': author,
                            'created_date': created_date,
                            'change_summary': change_summary
                        })
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return versions


def write_article_versions(versions):
    with open(os.path.join(data_dir, 'article_versions.txt'), 'w', encoding='utf-8') as f:
        for v in versions:
            content = v['content'].replace('|', '\\|')
            line = '|'.join([
                str(v['version_id']),
                str(v['article_id']),
                str(v['version_number']),
                content,
                v['author'],
                v['created_date'],
                v['change_summary']
            ])
            f.write(line + '\n')


def parse_approvals():
    approvals = []
    try:
        with open(os.path.join(data_dir, 'approvals.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 7:
                    try:
                        approvals.append({'approval_id': int(parts[0]), 'article_id': int(parts[1]), 'version_id': int(parts[2]),
                                      'approver': parts[3], 'status': parts[4], 'comments': parts[5], 'timestamp': parts[6]})
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return approvals


def parse_comments():
    comments = []
    try:
        with open(os.path.join(data_dir, 'comments.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|',5)
                if len(parts) == 6:
                    try:
                        comments.append({'comment_id': int(parts[0]), 'article_id': int(parts[1]), 'version_id': int(parts[2]),
                                     'user': parts[3], 'comment_text': parts[4], 'timestamp': parts[5]})
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return comments


def parse_analytics():
    analytics = []
    try:
        with open(os.path.join(data_dir, 'analytics.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 7:
                    try:
                        analytics.append({'analytics_id': int(parts[0]), 'article_id': int(parts[1]), 'date': parts[2], 'views': int(parts[3]),
                                      'unique_visitors': int(parts[4]), 'avg_time_seconds': int(parts[5]), 'shares': int(parts[6])})
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return analytics


# Helper: get next article id
# Scan all articles and return max+1

def next_article_id():
    articles = parse_articles()
    if not articles:
        return 1
    return max(articles.keys()) + 1

# Helper: get next version id

def next_version_id():
    versions = parse_article_versions()
    if not versions:
        return 1
    return max(v['version_id'] for v in versions) + 1

# Helper: get next comment id

def next_comment_id():
    comments = parse_comments()
    if not comments:
        return 1
    return max(c['comment_id'] for c in comments) + 1

# Helper: get next approval id

def next_approval_id():
    approvals = parse_approvals()
    if not approvals:
        return 1
    return max(a['approval_id'] for a in approvals) + 1


# Helper to load latest version of article

def get_latest_version(article_id):
    versions = [v for v in parse_article_versions() if v['article_id'] == article_id]
    if not versions:
        return None
    return max(versions, key=lambda v: v['version_number'])

# Helper to get all versions sorted

def get_article_versions(article_id):
    versions = [v for v in parse_article_versions() if v['article_id'] == article_id]
    return sorted(versions, key=lambda v: v['version_number'])


# ROUTES

LOGGED_IN_USER = 'john'

@app.route('/dashboard')
def dashboard():
    users = parse_users()
    user = users.get(LOGGED_IN_USER, {'fullname': LOGGED_IN_USER})
    articles = parse_articles()
    comments = parse_comments()
    approvals = parse_approvals()

    # Quick stats calculation for logged in user
    draft_count = sum(1 for a in articles.values() if a['author'] == LOGGED_IN_USER and a['status'] == 'draft')
    published_count = sum(1 for a in articles.values() if a['author'] == LOGGED_IN_USER and a['status'] == 'published')
    pending_review_count = sum(1 for a in articles.values() if a['author'] == LOGGED_IN_USER and a['status'] == 'pending_review')

    recent_activity = []

    # Recent edits from article_versions by user
    versions = parse_article_versions()
    user_versions = [v for v in versions if v['author'] == LOGGED_IN_USER]
    user_versions_sorted = sorted(user_versions, key=lambda v: v['created_date'], reverse=True)[:5]
    for v in user_versions_sorted:
        recent_activity.append(f"Edited article ID {v['article_id']} - Version {v['version_number']}")

    # Recent comments
    user_comments = [c for c in comments if c['user'] == LOGGED_IN_USER]
    user_comments_sorted = sorted(user_comments, key=lambda c: c['timestamp'], reverse=True)[:3]
    for c in user_comments_sorted:
        recent_activity.append(f"Commented on Article ID {c['article_id']}: {c['comment_text']}")

    recent_activity = recent_activity[:5]

    return render_template('dashboard.html', username=LOGGED_IN_USER, status_counts={'draft': draft_count, 'published': published_count, 'pending_review': pending_review_count}, recent_activities=recent_activity)


@app.route('/article/create', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        title = request.form.get('article-title', '').strip()
        content = request.form.get('article-content', '').strip()
        if not title:
            flash('Title is required.', 'error')
            return render_template('create_article.html')
        if not content:
            flash('Content is required.', 'error')
            return render_template('create_article.html')

        new_article_id = next_article_id()
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        articles = parse_articles()

        new_article = {
            'article_id': new_article_id,
            'title': title,
            'author': LOGGED_IN_USER,
            'category': 'blog',
            'status': 'draft',
            'tags': [],
            'featured_image': '',
            'meta_description': '',
            'created_date': now_str,
            'publish_date': ''
        }
        articles[new_article_id] = new_article
        write_articles(articles)

        # Add initial version
        version_id = next_version_id()
        versions = parse_article_versions()
        new_version = {
            'version_id': version_id,
            'article_id': new_article_id,
            'version_number': 1,
            'content': content,
            'author': LOGGED_IN_USER,
            'created_date': now_str,
            'change_summary': 'Initial draft'
        }
        versions.append(new_version)
        write_article_versions(versions)

        flash('Article saved as draft.', 'success')
        return redirect(url_for('my_articles'))

    return render_template('create_article.html')


@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    articles = parse_articles()
    if article_id not in articles:
        flash('Article not found.', 'error')
        return redirect(url_for('my_articles'))
    article = articles[article_id]
    if article['author'] != LOGGED_IN_USER:
        flash('Permission denied to edit this article.', 'error')
        return redirect(url_for('my_articles'))

    versions = parse_article_versions()
    article_versions = [v for v in versions if v['article_id'] == article_id]
    if not article_versions:
        flash('No versions found for this article.', 'error')
        return redirect(url_for('my_articles'))
    latest_version = max(article_versions, key=lambda v: v['version_number'])

    if request.method == 'POST':
        new_title = request.form.get('edit-article-title', '').strip()
        new_content = request.form.get('edit-article-content', '').strip()
        if not new_title:
            flash('Title is required.', 'error')
            return render_template('edit_article.html', article=article, content=latest_version['content'])
        if not new_content:
            flash('Content is required.', 'error')
            return render_template('edit_article.html', article=article, content=latest_version['content'])

        new_version_number = latest_version['version_number'] + 1
        version_id = next_version_id()
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        new_version = {
            'version_id': version_id,
            'article_id': article_id,
            'version_number': new_version_number,
            'content': new_content,
            'author': LOGGED_IN_USER,
            'created_date': now_str,
            'change_summary': f'Version {new_version_number} update'
        }
        versions.append(new_version)
        write_article_versions(versions)

        if new_title != article['title']:
            article['title'] = new_title
            articles[article_id] = article
            write_articles(articles)

        flash('New version saved.', 'success')
        return redirect(url_for('my_articles'))

    return render_template('edit_article.html', article=article, content=latest_version['content'])


@app.route('/article/<int:article_id>/versions', methods=['GET', 'POST'])
def version_history(article_id):
    articles = parse_articles()
    if article_id not in articles:
        flash('Article not found.', 'error')
        return redirect(url_for('my_articles'))
    article = articles[article_id]

    versions = parse_article_versions()
    article_versions = sorted([v for v in versions if v['article_id'] == article_id], key=lambda v: v['version_number'])
    if not article_versions:
        flash('No versions found for this article.', 'error')
        return redirect(url_for('edit_article', article_id=article_id))

    selected_v1_id = None
    selected_v2_id = None
    compare_result = None

    if request.method == 'POST':
        # fix restore form input detection according to validation reports
        if 'restore_version' in request.form:
            restore_version_number = int(request.form['restore_version'])
            version_to_restore = next((v for v in article_versions if v['version_number'] == restore_version_number), None)
            if not version_to_restore:
                flash('Version to restore not found.', 'error')
                return redirect(url_for('version_history', article_id=article_id))

            new_version_number = max(v['version_number'] for v in article_versions) + 1
            version_id = next_version_id()
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            new_version = {
                'version_id': version_id,
                'article_id': article_id,
                'version_number': new_version_number,
                'content': version_to_restore['content'],
                'author': LOGGED_IN_USER,
                'created_date': now_str,
                'change_summary': f'Restored version {restore_version_number}'
            }
            versions.append(new_version)
            write_article_versions(versions)

            flash(f'Version {restore_version_number} restored as new version.', 'success')
            return redirect(url_for('edit_article', article_id=article_id))

        selected_v1_id = int(request.form.get('version1', 0))
        selected_v2_id = int(request.form.get('version2', 0))

        v1 = next((v for v in article_versions if v['version_number'] == selected_v1_id), None)
        v2 = next((v for v in article_versions if v['version_number'] == selected_v2_id), None)

        if v1 and v2:
            compare_result = {
                'v1': v1,
                'v2': v2,
                'diff_html_v1': html.escape(v1['content']).replace('\n', '<br>'),
                'diff_html_v2': html.escape(v2['content']).replace('\n', '<br>')
            }
        else:
            flash('Select two valid versions to compare.', 'error')

    # Unpack compare_result to match template expected variables
    selected_v1 = None
    selected_v2 = None
    content_v1 = None
    content_v2 = None
    if compare_result:
        selected_v1 = compare_result['v1']['version_number']
        selected_v2 = compare_result['v2']['version_number']
        content_v1 = compare_result['diff_html_v1']
        content_v2 = compare_result['diff_html_v2']

    return render_template('version_history.html',
                           article=article,
                           versions=article_versions,
                           selected_v1=selected_v1,
                           selected_v2=selected_v2,
                           content_v1=content_v1,
                           content_v2=content_v2)


@app.route('/articles/mine')
def my_articles():
    articles = parse_articles()
    filter_status = request.args.get('status', '')

    user_articles = [a for a in articles.values() if a['author'] == LOGGED_IN_USER]
    if filter_status:
        user_articles = [a for a in user_articles if a['status'] == filter_status]

    statuses = ['draft', 'pending_review', 'under_review', 'approved', 'published', 'rejected', 'archived']
    return render_template('my_articles.html', articles=user_articles, statuses=statuses, current_status=filter_status)


@app.route('/articles/published')
def published_articles():
    articles = parse_articles()
    category_filter = request.args.get('category', '')
    sort_option = request.args.get('sort', 'date_desc')

    published = [a for a in articles.values() if a['status'] == 'published']
    if category_filter:
        published = [a for a in published if a['category'] == category_filter]

    if sort_option == 'date_asc':
        published.sort(key=lambda x: x['publish_date'] or '')
    elif sort_option == 'date_desc':
        published.sort(key=lambda x: x['publish_date'] or '', reverse=True)
    elif sort_option == 'popularity':
        analytics_data = parse_analytics()
        views_map = defaultdict(int)
        for ad in analytics_data:
            views_map[ad['article_id']] += ad['views']
        published.sort(key=lambda x: views_map[x['article_id']], reverse=True)
    elif sort_option == 'title_asc':
        published.sort(key=lambda x: x['title'].lower())
    elif sort_option == 'title_desc':
        published.sort(key=lambda x: x['title'].lower(), reverse=True)

    categories = ['news', 'blog', 'tutorial', 'announcement', 'press_release']

    return render_template('published_articles.html', articles=published, categories=categories,
                           current_category=category_filter, current_sort=sort_option)


@app.route('/calendar', methods=['GET', 'POST'])
def content_calendar():
    articles = parse_articles()
    calendar_view = request.form.get('calendar-view') if request.method == 'POST' else 'month'

    if request.method == 'POST':
        new_article_id = request.form.get('scheduled-article-id')
        new_publish_date = request.form.get('scheduled-publish-date')
        if new_article_id and new_publish_date:
            try:
                new_article_id = int(new_article_id)
                article = articles.get(new_article_id)
                if article:
                    article['publish_date'] = new_publish_date
                    now = datetime.now()
                    publish_dt = datetime.strptime(new_publish_date, '%Y-%m-%d %H:%M:%S')
                    if publish_dt <= now and article['status'] != 'published':
                        article['status'] = 'published'
                    write_articles(articles)
                    flash('Article scheduled successfully.', 'success')
            except Exception:
                flash('Invalid scheduling input.', 'error')

    scheduled_articles = [a for a in articles.values() if a['publish_date']]
    return render_template('content_calendar.html', scheduled_articles=scheduled_articles, calendar_view=calendar_view)


@app.route('/article/<int:article_id>/analytics')
def article_analytics(article_id):
    articles = parse_articles()
    article = articles.get(article_id)
    if not article or article['status'] != 'published':
        flash('Article not found or not published.', 'error')
        return redirect(url_for('my_articles'))

    analytics_data = parse_analytics()
    article_analytics = [a for a in analytics_data if a['article_id'] == article_id]

    total_views = sum(a['views'] for a in article_analytics)
    unique_visitors = sum(a['unique_visitors'] for a in article_analytics)
    avg_time = int((sum(a['avg_time_seconds'] for a in article_analytics) / len(article_analytics)) if article_analytics else 0)
    total_shares = sum(a['shares'] for a in article_analytics)

    return render_template('article_analytics.html', article=article, total_views=total_views,
                           unique_visitors=unique_visitors, avg_time=avg_time, total_shares=total_shares)


if __name__ == '__main__':
    app.run(debug=True)
