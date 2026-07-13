from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import os
import html

app = Flask(__name__, template_folder='templates_candidate_b')
app.secret_key = 'your_secret_key_here'

DATA_DIR = 'data'

# UTILITIES TO LOAD DATA FROM FILES

def parse_users():
    users = {}
    path = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.isfile(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
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
    return users


def parse_articles():
    articles = {}
    path = os.path.join(DATA_DIR, 'articles.txt')
    if not os.path.isfile(path):
        return articles
    with open(path, 'r', encoding='utf-8') as f:
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
                    'tags': parts[5],
                    'featured_image': parts[6],
                    'meta_description': parts[7],
                    'created_date': parts[8],
                    'publish_date': parts[9]
                }
    return articles


def write_articles(articles):
    path = os.path.join(DATA_DIR, 'articles.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for article_id in sorted(articles.keys()):
            a = articles[article_id]
            line = '|'.join([
                str(a['article_id']),
                a['title'],
                a['author'],
                a['category'],
                a['status'],
                a['tags'],
                a['featured_image'],
                a['meta_description'],
                a['created_date'],
                a['publish_date']
            ])
            f.write(line + '\n')


def parse_article_versions():
    versions = []
    path = os.path.join(DATA_DIR, 'article_versions.txt')
    if not os.path.isfile(path):
        return versions
    with open(path, 'r', encoding='utf-8') as f:
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
    return versions


def write_article_versions(versions):
    path = os.path.join(DATA_DIR, 'article_versions.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for v in versions:
            # We escape any pipe characters in content
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
    path = os.path.join(DATA_DIR, 'approvals.txt')
    if not os.path.isfile(path):
        return approvals
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) == 7:
                try:
                    approval_id = int(parts[0])
                    article_id = int(parts[1])
                    version_id = int(parts[2])
                    approver = parts[3]
                    status = parts[4]
                    comments = parts[5]
                    timestamp = parts[6]
                    approvals.append({
                        'approval_id': approval_id,
                        'article_id': article_id,
                        'version_id': version_id,
                        'approver': approver,
                        'status': status,
                        'comments': comments,
                        'timestamp': timestamp
                    })
                except ValueError:
                    continue
    return approvals


def parse_comments():
    comments = []
    path = os.path.join(DATA_DIR, 'comments.txt')
    if not os.path.isfile(path):
        return comments
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) == 6:
                try:
                    comment_id = int(parts[0])
                    article_id = int(parts[1])
                    version_id = int(parts[2])
                    user = parts[3]
                    comment_text = parts[4]
                    timestamp = parts[5]
                    comments.append({
                        'comment_id': comment_id,
                        'article_id': article_id,
                        'version_id': version_id,
                        'user': user,
                        'comment_text': comment_text,
                        'timestamp': timestamp
                    })
                except ValueError:
                    continue
    return comments


def parse_analytics():
    analytics = []
    path = os.path.join(DATA_DIR, 'analytics.txt')
    if not os.path.isfile(path):
        return analytics
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) == 7:
                try:
                    analytics_id = int(parts[0])
                    article_id = int(parts[1])
                    date = parts[2]
                    views = int(parts[3])
                    unique_visitors = int(parts[4])
                    avg_time_seconds = int(parts[5])
                    shares = int(parts[6])
                    analytics.append({
                        'analytics_id': analytics_id,
                        'article_id': article_id,
                        'date': date,
                        'views': views,
                        'unique_visitors': unique_visitors,
                        'avg_time_seconds': avg_time_seconds,
                        'shares': shares
                    })
                except ValueError:
                    continue
    return analytics


# HELPER for user context - simulate logged in user
# (Authentication out of scope, we fix to 'john' for demonstration)
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
    # Recent activity: combine edits, comments, approvals relevant to user

    recent_activity = []

    # Recent edits from article_versions by user
    versions = parse_article_versions()
    user_versions = [v for v in versions if v['author'] == LOGGED_IN_USER]
    for v in user_versions:
        recent_activity.append({
            'type': 'edit',
            'message': f"Edited article ID {v['article_id']} v{v['version_number']}",
            'timestamp': v['created_date']
        })
    # Comments by or on user's articles
    user_article_ids = [a['article_id'] for a in articles.values() if a['author'] == LOGGED_IN_USER]
    user_comments = [c for c in comments if c['user'] == LOGGED_IN_USER or c['article_id'] in user_article_ids]
    for c in user_comments:
        recent_activity.append({
            'type': 'comment',
            'message': f"Comment on article ID {c['article_id']}: {c['comment_text']}",
            'timestamp': c['timestamp']
        })
    # Approvals by or on user's articles
    user_approvals = [a for a in approvals if a['approver'] == LOGGED_IN_USER or a['article_id'] in user_article_ids]
    for a_ in user_approvals:
        recent_activity.append({
            'type': 'approval',
            'message': f"Approval status on article ID {a_['article_id']}: {a_['status']}",
            'timestamp': a_['timestamp']
        })

    # Sort by timestamp descending
    try:
        recent_activity.sort(key=lambda x: x['timestamp'], reverse=True)
    except Exception:
        pass

    return render_template('dashboard.html', 
                           user=user, 
                           draft_count=draft_count,
                           published_count=published_count,
                           pending_review_count=pending_review_count,
                           recent_activity=recent_activity)


@app.route('/article/create', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        title = request.form.get('article-title', '').strip()
        content = request.form.get('article-content', '').strip()
        if not title:
            flash('Article title is required.', 'error')
            return redirect(url_for('create_article'))
        articles = parse_articles()
        versions = parse_article_versions()
        # Generate new article_id
        new_id = max(articles.keys(), default=0) + 1
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Add new article record with status draft
        articles[new_id] = {
            'article_id': new_id,
            'title': title,
            'author': LOGGED_IN_USER,
            'category': 'blog',  # default category blog, no UI for now
            'status': 'draft',
            'tags': '',
            'featured_image': '',
            'meta_description': '',
            'created_date': now_str,
            'publish_date': ''
        }

        write_articles(articles)

        # Add first version
        new_version_id = max((v['version_id'] for v in versions), default=0) + 1
        versions.append({
            'version_id': new_version_id,
            'article_id': new_id,
            'version_number': 1,
            'content': content,
            'author': LOGGED_IN_USER,
            'created_date': now_str,
            'change_summary': 'Initial draft'
        })
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
        flash('Unauthorized access to edit this article.', 'error')
        return redirect(url_for('my_articles'))

    versions = parse_article_versions()
    # get latest version
    article_versions = [v for v in versions if v['article_id'] == article_id]
    if not article_versions:
        flash('No versions found for this article.', 'error')
        return redirect(url_for('my_articles'))
    latest_version = max(article_versions, key=lambda v: v['version_number'])

    if request.method == 'POST':
        new_title = request.form.get('edit-article-title', '').strip()
        new_content = request.form.get('edit-article-content', '').strip()
        if not new_title:
            flash('Article title cannot be empty.', 'error')
            return redirect(url_for('edit_article', article_id=article_id))

        # Save new version
        new_version_number = latest_version['version_number'] + 1
        new_version_id = max((v['version_id'] for v in versions), default=0) + 1
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        versions.append({
            'version_id': new_version_id,
            'article_id': article_id,
            'version_number': new_version_number,
            'content': new_content,
            'author': LOGGED_IN_USER,
            'created_date': now_str,
            'change_summary': f'Version {new_version_number} saved'
        })
        write_article_versions(versions)

        # Update article metadata if title changed
        if new_title != article['title']:
            article['title'] = new_title
            articles[article_id] = article
            write_articles(articles)

        flash('New version saved.', 'success')
        return redirect(url_for('edit_article', article_id=article_id))

    return render_template('edit_article.html', article=article, version=latest_version)


@app.route('/article/<int:article_id>/versions', methods=['GET', 'POST'])
def version_history(article_id):
    articles = parse_articles()
    if article_id not in articles:
        flash('Article not found.', 'error')
        return redirect(url_for('my_articles'))
    article = articles[article_id]

    versions = parse_article_versions()
    article_versions = [v for v in versions if v['article_id'] == article_id]
    if not article_versions:
        flash('No versions found for this article.', 'error')
        return redirect(url_for('edit_article', article_id=article_id))

    selected_v1_id = None
    selected_v2_id = None
    compare_result = None

    if request.method == 'POST':
        # Handle restore or compare
        if 'restore_version' in request.form:
            restore_version_number = int(request.form['restore_version'])
            # find version to restore
            version_to_restore = next((v for v in article_versions if v['version_number'] == restore_version_number), None)
            if not version_to_restore:
                flash('Version to restore not found.', 'error')
                return redirect(url_for('version_history', article_id=article_id))

            # Create new version duplicating content
            new_version_number = max(v['version_number'] for v in article_versions) + 1
            new_version_id = max((v['version_id'] for v in versions), default=0) + 1
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            versions.append({
                'version_id': new_version_id,
                'article_id': article_id,
                'version_number': new_version_number,
                'content': version_to_restore['content'],
                'author': LOGGED_IN_USER,
                'created_date': now_str,
                'change_summary': f'Restored version {restore_version_number}'
            })
            write_article_versions(versions)
            flash(f'Version {restore_version_number} restored as new version.', 'success')
            return redirect(url_for('edit_article', article_id=article_id))

        selected_v1_id = int(request.form.get('version1', 0))
        selected_v2_id = int(request.form.get('version2', 0))

        v1 = next((v for v in article_versions if v['version_number'] == selected_v1_id), None)
        v2 = next((v for v in article_versions if v['version_number'] == selected_v2_id), None)

        if v1 and v2:
            # simple side-by-side comparison
            compare_result = {
                'v1': v1,
                'v2': v2,
                'diff_html_v1': html.escape(v1['content']).replace('\n', '<br>'),
                'diff_html_v2': html.escape(v2['content']).replace('\n', '<br>')
            }
        else:
            flash('Select two valid versions to compare.', 'error')

    return render_template('version_history.html',
                           article=article,
                           versions=article_versions,
                           compare_result=compare_result,
                           selected_v1_id=selected_v1_id,
                           selected_v2_id=selected_v2_id)


@app.route('/articles/mine', methods=['GET', 'POST'])
def my_articles():
    articles = parse_articles()
    filter_status = request.args.get('status', '')

    user_articles = [a for a in articles.values() if a['author'] == LOGGED_IN_USER]
    if filter_status:
        user_articles = [a for a in user_articles if a['status'] == filter_status]

    statuses = ['draft', 'pending_review', 'under_review', 'approved', 'published', 'rejected', 'archived']
    return render_template('my_articles.html', articles=user_articles, statuses=statuses, filter_status=filter_status)


@app.route('/articles/published', methods=['GET', 'POST'])
def published_articles():
    articles = parse_articles()
    filter_category = request.args.get('category', '')
    sort = request.args.get('sort', 'date_desc')

    published = [a for a in articles.values() if a['status'] == 'published']
    if filter_category:
        published = [a for a in published if a['category'] == filter_category]

    if sort == 'date_asc':
        published.sort(key=lambda x: x['publish_date'] or '')
    elif sort == 'date_desc':
        published.sort(key=lambda x: x['publish_date'] or '', reverse=True)
    elif sort == 'popularity':
        # Sort by views from analytics
        analytics = parse_analytics()
        views_map = {}
        for entry in analytics:
            views_map[entry['article_id']] = views_map.get(entry['article_id'], 0) + entry['views']
        published.sort(key=lambda x: views_map.get(x['article_id'], 0), reverse=True)
    elif sort == 'title_az':
        published.sort(key=lambda x: x['title'].lower())
    elif sort == 'title_za':
        published.sort(key=lambda x: x['title'].lower(), reverse=True)

    categories = ['news', 'blog', 'tutorial', 'announcement', 'press_release']

    return render_template('published_articles.html', articles=published, categories=categories, filter_category=filter_category, sort=sort)


@app.route('/calendar', methods=['GET', 'POST'])
def content_calendar():
    articles = parse_articles()
    filter_status = 'approved'

    calendar_view = request.args.get('view', 'month')

    if request.method == 'POST':
        # Scheduling article publish date update
        article_id = request.form.get('article_id', '')
        publish_date = request.form.get('publish_date', '')

        if not article_id or not publish_date:
            flash('Article and publish date are required for scheduling.', 'error')
            return redirect(url_for('content_calendar', view=calendar_view))

        try:
            article_id = int(article_id)
            datetime.strptime(publish_date, '%Y-%m-%d %H:%M:%S')
        except Exception:
            flash('Invalid article ID or publish date format. Use YYYY-MM-DD HH:MM:SS.', 'error')
            return redirect(url_for('content_calendar', view=calendar_view))

        if article_id not in articles:
            flash('Article not found.', 'error')
            return redirect(url_for('content_calendar', view=calendar_view))

        article = articles[article_id]
        article['publish_date'] = publish_date
        article['status'] = 'published'
        write_articles(articles)
        flash('Article scheduled for publication.', 'success')
        return redirect(url_for('content_calendar', view=calendar_view))

    # Filter articles by status approved or published
    calendar_articles = [a for a in articles.values() if a['status'] in ['approved', 'published']]  

    return render_template('content_calendar.html', calendar_view=calendar_view, articles=calendar_articles)


@app.route('/article/<int:article_id>/analytics')
def article_analytics(article_id):
    articles = parse_articles()
    if article_id not in articles:
        flash('Article not found.', 'error')
        return redirect(url_for('my_articles'))
    article = articles[article_id]
    if article['status'] != 'published':
        flash('Analytics only available for published articles.', 'error')
        return redirect(url_for('edit_article', article_id=article_id))

    analytics_data = parse_analytics()
    article_analytics_entries = [a for a in analytics_data if a['article_id'] == article_id]

    total_views = sum(a['views'] for a in article_analytics_entries)
    unique_visitors = sum(a['unique_visitors'] for a in article_analytics_entries)
    avg_time = int((sum(a['avg_time_seconds'] for a in article_analytics_entries) / len(article_analytics_entries)) if article_analytics_entries else 0)
    total_shares = sum(a['shares'] for a in article_analytics_entries)

    return render_template('article_analytics.html', article=article, total_views=total_views,
                           unique_visitors=unique_visitors, avg_time=avg_time, total_shares=total_shares)


if __name__ == '__main__':
    app.run(debug=True)
