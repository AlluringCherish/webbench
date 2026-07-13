from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
from collections import defaultdict
import html

app = Flask(__name__, template_folder='templates_candidate_a')
app.secret_key = 'supersecretkey'

data_dir = 'data'

# Utility functions to parse data files

def parse_users():
    users = []
    try:
        with open(os.path.join(data_dir, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 4:
                    users.append({'username': parts[0], 'email': parts[1], 'fullname': parts[2], 'created_date': parts[3]})
    except FileNotFoundError:
        pass
    return users

def parse_articles():
    articles = []
    try:
        with open(os.path.join(data_dir, 'articles.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 10:
                    article = {
                        'article_id': int(parts[0]),
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
                    articles.append(article)
    except FileNotFoundError:
        pass
    return articles

def parse_article_versions():
    versions = []
    try:
        with open(os.path.join(data_dir, 'article_versions.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # content may contain pipes - handle with splitting max 6 parts
                parts = line.split('|', 6)
                if len(parts) == 7:
                    version_id = int(parts[0])
                    article_id = int(parts[1])
                    version_number = int(parts[2])
                    content = parts[3]
                    author = parts[4]
                    created_date = parts[5]
                    change_summary = parts[6]
                    versions.append({'version_id': version_id, 'article_id': article_id, 'version_number': version_number,
                                     'content': content, 'author': author, 'created_date': created_date, 'change_summary': change_summary})
    except FileNotFoundError:
        pass
    return versions

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
                    approvals.append({'approval_id': int(parts[0]), 'article_id': int(parts[1]), 'version_id': int(parts[2]),
                                      'approver': parts[3], 'status': parts[4], 'comments': parts[5], 'timestamp': parts[6]})
    except FileNotFoundError:
        pass
    return approvals

def parse_workflow_stages():
    stages = []
    try:
        with open(os.path.join(data_dir, 'workflow_stages.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 5:
                    stages.append({'stage_id': int(parts[0]), 'category': parts[1], 'stage_name': parts[2],
                                   'stage_order': int(parts[3]), 'is_required': parts[4]})
    except FileNotFoundError:
        pass
    return stages

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
                    comments.append({'comment_id': int(parts[0]), 'article_id': int(parts[1]), 'version_id': int(parts[2]),
                                     'user': parts[3], 'comment_text': parts[4], 'timestamp': parts[5]})
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
                    analytics.append({'analytics_id': int(parts[0]), 'article_id': int(parts[1]), 'date': parts[2], 'views': int(parts[3]),
                                      'unique_visitors': int(parts[4]), 'avg_time_seconds': int(parts[5]), 'shares': int(parts[6])})
    except FileNotFoundError:
        pass
    return analytics


# Helper: get next article id
# Scan all articles and return max+1

def next_article_id():
    articles = parse_articles()
    if not articles:
        return 1
    return max(article['article_id'] for article in articles) + 1

# Helper: get next version id

def next_version_id():
    versions = parse_article_versions()
    if not versions:
        return 1
    return max(version['version_id'] for version in versions) + 1

# Helper: get next comment id

def next_comment_id():
    comments = parse_comments()
    if not comments:
        return 1
    return max(comment['comment_id'] for comment in comments) + 1

# Helper: get next approval id

def next_approval_id():
    approvals = parse_approvals()
    if not approvals:
        return 1
    return max(app['approval_id'] for app in approvals) + 1


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

# Helper to update articles.txt record

def save_articles(articles):
    lines = []
    for a in articles:
        tags_str = ','.join(a['tags']) if isinstance(a['tags'], list) else ''
        line = f"{a['article_id']}|{a['title']}|{a['author']}|{a['category']}|{a['status']}|{tags_str}|{a['featured_image']}|{a['meta_description']}|{a['created_date']}|{a['publish_date']}"
        lines.append(line)
    with open(os.path.join(data_dir, 'articles.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# Helper to append to article_versions.txt

def add_article_version(version):
    # Escape pipes in content
    content_escaped = version['content'].replace('|', '&#124;')
    line = f"{version['version_id']}|{version['article_id']}|{version['version_number']}|{content_escaped}|{version['author']}|{version['created_date']}|{version['change_summary']}"
    with open(os.path.join(data_dir, 'article_versions.txt'), 'a', encoding='utf-8') as f:
        f.write(line + '\n')


# ROUTES

@app.route('/dashboard')
def dashboard():
    # For demo purposes assume logged in user 'john'
    current_user = 'john'
    users = parse_users()
    articles = parse_articles()
    comments = parse_comments()

    # Stats: counts of drafts, published, pending review, etc for user
    user_articles = [a for a in articles if a['author'] == current_user]
    status_counts = defaultdict(int)
    for a in user_articles:
        status_counts[a['status']] += 1

    # Recent activity: recent edits, comments, approvals
    recent_activities = []
    # Recent edits: latest versions edited by user
    versions = parse_article_versions()
    user_versions = [v for v in versions if v['author'] == current_user]
    user_versions_sorted = sorted(user_versions, key=lambda v: v['created_date'], reverse=True)[:5]
    for v in user_versions_sorted:
        recent_activities.append(f"Edited Article ID {v['article_id']} - Version {v['version_number']}")

    # Recent comments
    user_comments = [c for c in comments if c['user'] == current_user]
    user_comments_sorted = sorted(user_comments, key=lambda c: c['timestamp'], reverse=True)[:3]
    for c in user_comments_sorted:
        recent_activities.append(f"Commented on Article ID {c['article_id']}: {c['comment_text']}")

    # sort general recent_activities by text as rough
    recent_activities = recent_activities[:5]

    return render_template('dashboard.html', username=current_user, status_counts=status_counts, recent_activities=recent_activities)


@app.route('/article/create', methods=['GET', 'POST'])
def create_article():
    current_user = 'john'
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
        # New article record
        new_article = {
            'article_id': new_article_id,
            'title': title,
            'author': current_user,
            'category': 'blog',
            'status': 'draft',
            'tags': [],
            'featured_image': '',
            'meta_description': '',
            'created_date': now_str,
            'publish_date': ''
        }
        articles = parse_articles()
        articles.append(new_article)
        save_articles(articles)

        # Add initial version
        version_id = next_version_id()
        new_version = {
            'version_id': version_id,
            'article_id': new_article_id,
            'version_number': 1,
            'content': content,
            'author': current_user,
            'created_date': now_str,
            'change_summary': 'Initial draft'
        }
        add_article_version(new_version)
        flash('Article saved as draft.', 'success')
        return redirect(url_for('my_articles'))

    return render_template('create_article.html')


@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    current_user = 'john'
    articles = parse_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        flash('Article not found.', 'error')
        return redirect(url_for('my_articles'))

    if article['author'] != current_user:
        flash('Permission denied to edit this article.', 'error')
        return redirect(url_for('my_articles'))

    latest_version = get_latest_version(article_id)
    title = article['title']
    content = ''
    if latest_version:
        content = latest_version['content'].replace('&#124;', '|')

    if request.method == 'POST':
        new_title = request.form.get('edit-article-title', '').strip()
        new_content = request.form.get('edit-article-content', '').strip()
        if not new_title:
            flash('Title is required.', 'error')
            return render_template('edit_article.html', article=article, content=content)
        if not new_content:
            flash('Content is required.', 'error')
            return render_template('edit_article.html', article=article, content=content)

        # Save new version
        versions = get_article_versions(article_id)
        new_version_number = max(v['version_number'] for v in versions) + 1 if versions else 1
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        version_id = next_version_id()
        new_version_data = {
            'version_id': version_id,
            'article_id': article_id,
            'version_number': new_version_number,
            'content': new_content,
            'author': current_user,
            'created_date': now_str,
            'change_summary': f'Version {new_version_number} update'
        }
        add_article_version(new_version_data)
        # Update article title if changed
        if new_title != article['title']:
            article['title'] = new_title
            save_articles(articles)
        flash('New version saved.', 'success')
        return redirect(url_for('my_articles'))

    return render_template('edit_article.html', article=article, content=content)


@app.route('/article/<int:article_id>/versions', methods=['GET', 'POST'])
def version_history(article_id):
    articles = parse_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        flash('Article not found.', 'error')
        return redirect(url_for('my_articles'))

    versions = get_article_versions(article_id)

    selected_v1 = request.args.get('v1', type=int)
    selected_v2 = request.args.get('v2', type=int)

    # defaults to last two versions if none selected
    if not selected_v1 or not selected_v2:
        if len(versions) >= 2:
            selected_v1 = versions[-2]['version_number']
            selected_v2 = versions[-1]['version_number']
        elif len(versions) == 1:
            selected_v1 = selected_v2 = versions[0]['version_number']

    content_v1 = ''
    content_v2 = ''

    for v in versions:
        if v['version_number'] == selected_v1:
            content_v1 = v['content'].replace('&#124;', '|')
        if v['version_number'] == selected_v2:
            content_v2 = v['content'].replace('&#124;', '|')

    if request.method == 'POST':
        for vnr in [selected_v1, selected_v2]:
            if request.form.get(f'restore-version-{vnr}'):
                # find version to restore
                version_to_restore = next((v for v in versions if v['version_number'] == vnr), None)
                if not version_to_restore:
                    flash('Version not found for restore.', 'error')
                    break
                # create new version from restored content
                now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                new_version_id = next_version_id()
                new_version_number = max(v['version_number'] for v in versions) + 1
                new_version = {
                    'version_id': new_version_id,
                    'article_id': article_id,
                    'version_number': new_version_number,
                    'content': version_to_restore['content'],
                    'author': 'john',
                    'created_date': now_str,
                    'change_summary': f'Restored version {vnr}'
                }
                add_article_version(new_version)
                flash(f'Version {vnr} restored as new version.', 'success')
                return redirect(url_for('edit_article', article_id=article_id))

    return render_template('version_history.html', article=article, versions=versions,
                           selected_v1=selected_v1, selected_v2=selected_v2, content_v1=content_v1, content_v2=content_v2)


@app.route('/articles/mine')
def my_articles():
    current_user = 'john'
    articles = parse_articles()

    status_filter = request.args.get('status', '')
    user_articles = [a for a in articles if a['author'] == current_user]
    if status_filter:
        user_articles = [a for a in user_articles if a['status'] == status_filter]

    statuses = ['draft', 'pending_review', 'under_review', 'approved', 'published', 'rejected', 'archived']

    return render_template('my_articles.html', articles=user_articles, statuses=statuses, current_status=status_filter)


@app.route('/articles/published')
def published_articles():
    articles = parse_articles()
    # Show only published
    published = [a for a in articles if a['status'] == 'published']

    category_filter = request.args.get('category', '')
    sort_option = request.args.get('sort', 'date_desc')

    if category_filter:
        published = [a for a in published if a['category'] == category_filter]

    # Sort
    if sort_option == 'date_asc':
        published.sort(key=lambda x: x['publish_date'] or '')
    elif sort_option == 'date_desc':
        published.sort(key=lambda x: x['publish_date'] or '', reverse=True)
    elif sort_option == 'popularity':
        # We do not have popularity metric in articles so skip or could sort by views from analytics
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
    # Show calendar of articles scheduled
    articles = parse_articles()
    sched_articles = [a for a in articles if a['publish_date']]

    calendar_view = request.form.get('calendar-view') if request.method == 'POST' else 'month'

    if request.method == 'POST':
        # For simplicity, assume scheduling new publish date via modal was done
        # We will simulate scheduling: get article_id and new date from form
        new_article_id = request.form.get('scheduled-article-id')
        new_publish_date = request.form.get('scheduled-publish-date')
        if new_article_id and new_publish_date:
            try:
                new_article_id = int(new_article_id)
                articles_all = parse_articles()
                article = next((a for a in articles_all if a['article_id'] == new_article_id), None)
                if article:
                    article['publish_date'] = new_publish_date
                    # Update status to published if publish date is past or current
                    now = datetime.now()
                    publish_dt = datetime.strptime(new_publish_date, '%Y-%m-%d %H:%M:%S')
                    if publish_dt <= now and article['status'] != 'published':
                        article['status'] = 'published'
                    save_articles(articles_all)
                    flash('Article scheduled successfully.', 'success')
            except Exception as e:
                flash('Invalid scheduling input.', 'error')

    return render_template('content_calendar.html', scheduled_articles=sched_articles, calendar_view=calendar_view)


@app.route('/article/<int:article_id>/analytics')
def article_analytics(article_id):
    articles = parse_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article or article['status'] != 'published':
        flash('Article not found or not published.', 'error')
        return redirect(url_for('my_articles'))

    analytics_data = parse_analytics()
    article_analytics = [a for a in analytics_data if a['article_id'] == article_id]

    total_views = sum(a['views'] for a in article_analytics)
    unique_visitors = sum(a['unique_visitors'] for a in article_analytics)

    return render_template('article_analytics.html', article=article, total_views=total_views, unique_visitors=unique_visitors)


if __name__ == '__main__':
    app.run(debug=True)
