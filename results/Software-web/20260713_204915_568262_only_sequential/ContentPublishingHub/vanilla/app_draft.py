from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__, template_folder='templates_draft')
DATA_DIR = 'data'

# Utility functions to read data files

def read_users():
    users = []
    path = os.path.join(DATA_DIR, 'users.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 4:
                    continue
                users.append({
                    'username': parts[0],
                    'email': parts[1],
                    'fullname': parts[2],
                    'created_date': parts[3]
                })
    return users

def read_articles():
    articles = []
    path = os.path.join(DATA_DIR, 'articles.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 10:
                    continue
                articles.append({
                    'article_id': parts[0],
                    'title': parts[1],
                    'author': parts[2],
                    'category': parts[3],
                    'status': parts[4],
                    'tags': parts[5].split(',') if parts[5] else [],
                    'featured_image': parts[6],
                    'meta_description': parts[7],
                    'created_date': parts[8],
                    'publish_date': parts[9]
                })
    return articles

def read_article_versions():
    versions = []
    path = os.path.join(DATA_DIR, 'article_versions.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                versions.append({
                    'version_id': parts[0],
                    'article_id': parts[1],
                    'version_number': int(parts[2]),
                    'content': parts[3],
                    'author': parts[4],
                    'created_date': parts[5],
                    'change_summary': parts[6]
                })
    return versions

def read_approvals():
    approvals = []
    path = os.path.join(DATA_DIR, 'approvals.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                approvals.append({
                    'approval_id': parts[0],
                    'article_id': parts[1],
                    'version_id': parts[2],
                    'approver': parts[3],
                    'status': parts[4],
                    'comments': parts[5],
                    'timestamp': parts[6]
                })
    return approvals

def read_workflow_stages():
    stages = []
    path = os.path.join(DATA_DIR, 'workflow_stages.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 5:
                    continue
                stages.append({
                    'stage_id': parts[0],
                    'category': parts[1],
                    'stage_name': parts[2],
                    'stage_order': int(parts[3]),
                    'is_required': parts[4]
                })
    return stages

def read_comments():
    comments = []
    path = os.path.join(DATA_DIR, 'comments.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 6:
                    continue
                comments.append({
                    'comment_id': parts[0],
                    'article_id': parts[1],
                    'version_id': parts[2],
                    'user': parts[3],
                    'comment_text': parts[4],
                    'timestamp': parts[5]
                })
    return comments

def read_analytics():
    analytics = []
    path = os.path.join(DATA_DIR, 'analytics.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                analytics.append({
                    'analytics_id': parts[0],
                    'article_id': parts[1],
                    'date': parts[2],
                    'views': int(parts[3]),
                    'unique_visitors': int(parts[4]),
                    'avg_time_seconds': int(parts[5]),
                    'shares': int(parts[6])
                })
    return analytics

# Utility functions to write data files

def write_articles(articles):
    path = os.path.join(DATA_DIR, 'articles.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for a in articles:
            line = '|'.join([
                a['article_id'],
                a['title'],
                a['author'],
                a['category'],
                a['status'],
                ','.join(a['tags']),
                a['featured_image'],
                a['meta_description'],
                a['created_date'],
                a['publish_date']
            ])
            f.write(line + '\n')

def write_article_versions(versions):
    path = os.path.join(DATA_DIR, 'article_versions.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for v in versions:
            line = '|'.join([
                v['version_id'],
                v['article_id'],
                str(v['version_number']),
                v['content'],
                v['author'],
                v['created_date'],
                v['change_summary']
            ])
            f.write(line + '\n')

# Route: /dashboard
@app.route('/dashboard')
def dashboard():
    # For demo purpose assume logged in user 'john'
    username = 'john'
    users = read_users()
    user = next((u for u in users if u['username'] == username), None)

    articles = read_articles()
    # Quick stats - count total articles, published, drafts for the user
    user_articles = [a for a in articles if a['author'] == username]
    total_articles = len(user_articles)
    published_count = len([a for a in user_articles if a['status'] == 'published'])
    draft_count = len([a for a in user_articles if a['status'] == 'draft'])

    # Recent activity - show last 5 articles created or edited by user
    versions = read_article_versions()
    user_versions = [v for v in versions if v['author'] == username]
    user_versions.sort(key=lambda v: v['created_date'], reverse=True)
    recent_activity = user_versions[:5]

    welcome_message = f"Welcome, {user['fullname']}" if user else "Welcome, User"

    return render_template('dashboard.html',
                           dashboard_page_id='dashboard-page',
                           welcome_message_id='welcome-message',
                           welcome_message=welcome_message,
                           quick_stats_id='quick-stats',
                           total_articles=total_articles,
                           published_count=published_count,
                           draft_count=draft_count,
                           create_article_button_id='create-article-button',
                           recent_activity_id='recent-activity',
                           recent_activity=recent_activity)

# Route: /article/create
@app.route('/article/create', methods=['GET', 'POST'])
def create_article():
    # For demo purpose assume logged in user 'john'
    username = 'john'
    if request.method == 'POST':
        title = request.form.get('article-title', '').strip()
        content = request.form.get('article-content', '').strip()
        if not title or not content:
            # Basic validation: title and content required
            return render_template('create_article.html',
                                   create_article_page_id='create-article-page',
                                   article_title_id='article-title',
                                   article_content_id='article-content',
                                   error='Title and content are required.')

        articles = read_articles()
        # Generate new article_id
        max_id = max([int(a['article_id']) for a in articles], default=0)
        new_id = str(max_id + 1)
        created_date = datetime.now().strftime('%Y-%m-%d')
        publish_date = ''
        category = 'blog'  # default category, no category input in form
        status = 'draft'
        tags = []
        featured_image = ''
        meta_description = ''

        new_article = {
            'article_id': new_id,
            'title': title,
            'author': username,
            'category': category,
            'status': status,
            'tags': tags,
            'featured_image': featured_image,
            'meta_description': meta_description,
            'created_date': created_date,
            'publish_date': publish_date
        }

        articles.append(new_article)
        write_articles(articles)

        # Add initial version
        versions = read_article_versions()
        max_version_id = max([int(v['version_id']) for v in versions], default=0)
        new_version_id = str(max_version_id + 1)

        new_version = {
            'version_id': new_version_id,
            'article_id': new_id,
            'version_number': 1,
            'content': content,
            'author': username,
            'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'change_summary': 'Initial draft'
        }
        versions.append(new_version)
        write_article_versions(versions)

        return redirect(url_for('my_articles'))

    return render_template('create_article.html',
                           create_article_page_id='create-article-page',
                           article_title_id='article-title',
                           article_content_id='article-content')

# Route: /article/<article_id>/edit
@app.route('/article/<article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    # For demo purpose assume logged in user 'john'
    username = 'john'
    articles = read_articles()
    versions = read_article_versions()

    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404

    # Find latest version
    article_versions = [v for v in versions if v['article_id'] == article_id]
    if not article_versions:
        current_content = ''
        current_version_number = 0
    else:
        latest_version = max(article_versions, key=lambda v: v['version_number'])
        current_content = latest_version['content']
        current_version_number = latest_version['version_number']

    if request.method == 'POST':
        new_title = request.form.get('edit-article-title', '').strip()
        new_content = request.form.get('edit-article-content', '').strip()
        if not new_title or not new_content:
            return render_template('edit_article.html',
                                   edit_article_page_id='edit-article-page',
                                   edit_article_title_id='edit-article-title',
                                   edit_article_content_id='edit-article-content',
                                   article=article,
                                   content=current_content,
                                   error='Title and content are required.')

        # Save new version
        max_version_id = max([int(v['version_id']) for v in versions], default=0)
        new_version_id = str(max_version_id + 1)
        new_version_number = current_version_number + 1

        new_version = {
            'version_id': new_version_id,
            'article_id': article_id,
            'version_number': new_version_number,
            'content': new_content,
            'author': username,
            'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'change_summary': 'Updated version'
        }
        versions.append(new_version)
        write_article_versions(versions)

        # Update article title if changed
        if new_title != article['title']:
            article['title'] = new_title
            write_articles(articles)

        # Redirect to same edit page after saving new version
        return redirect(url_for('edit_article', article_id=article_id))

    return render_template('edit_article.html',
                           edit_article_page_id='edit-article-page',
                           edit_article_title_id='edit-article-title',
                           edit_article_content_id='edit-article-content',
                           article=article,
                           content=current_content)

# Route: /article/<article_id>/versions
@app.route('/article/<article_id>/versions')
def article_version_history(article_id):
    articles = read_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404

    versions = read_article_versions()
    article_versions = [v for v in versions if v['article_id'] == article_id]
    article_versions.sort(key=lambda v: v['version_number'], reverse=True)

    return render_template('version_history.html',
                           version_history_page_id='version-history-page',
                           versions_list_id='versions-list',
                           version_comparison_id='version-comparison',
                           restore_version_button_id='restore-version-1',
                           back_to_edit_history_button_id='back-to-edit-history',
                           article=article,
                           versions=article_versions)

# Route: /articles/mine
@app.route('/articles/mine')
def my_articles():
    # For demo purpose assume logged in user 'john'
    username = 'john'
    status_filter = request.args.get('status', '')

    articles = read_articles()
    user_articles = [a for a in articles if a['author'] == username]
    if status_filter:
        user_articles = [a for a in user_articles if a['status'] == status_filter]

    return render_template('my_articles.html',
                           my_articles_page_id='my-articles-page',
                           filter_article_status_id='filter-article-status',
                           articles_table_id='articles-table',
                           create_new_article_button_id='create-new-article',
                           back_to_dashboard_button_id='back-to-dashboard',
                           articles=user_articles,
                           current_status_filter=status_filter)

# Route: /articles/published
@app.route('/articles/published')
def published_articles():
    category_filter = request.args.get('category', '')
    sort_by = request.args.get('sort', '')

    articles = read_articles()
    published_articles = [a for a in articles if a['status'] == 'published']

    if category_filter:
        published_articles = [a for a in published_articles if a['category'] == category_filter]

    # Supported sort_by values: title, created_date, publish_date
    if sort_by == 'title':
        published_articles.sort(key=lambda a: a['title'].lower())
    elif sort_by == 'created_date':
        published_articles.sort(key=lambda a: a['created_date'], reverse=True)
    elif sort_by == 'publish_date':
        published_articles.sort(key=lambda a: a['publish_date'], reverse=True)

    return render_template('published_articles.html',
                           published_articles_page_id='published-articles-page',
                           filter_published_category_id='filter-published-category',
                           published_articles_grid_id='published-articles-grid',
                           sort_published_id='sort-published',
                           back_to_dashboard_published_id='back-to-dashboard-published',
                           articles=published_articles,
                           current_category_filter=category_filter,
                           current_sort=sort_by)

# Route: /calendar
@app.route('/calendar')
def content_calendar():
    # This example will just provide a placeholder calendar view
    # No actual scheduling logic implemented here
    return render_template('content_calendar.html',
                           calendar_page_id='calendar-page',
                           calendar_view_id='calendar-view',
                           calendar_grid_id='calendar-grid',
                           schedule_button_id='schedule-button',
                           back_to_dashboard_calendar_id='back-to-dashboard-calendar')

# Route: /article/<article_id>/analytics
@app.route('/article/<article_id>/analytics')
def article_analytics(article_id):
    articles = read_articles()
    article = next((a for a in articles if a['article_id'] == article_id), None)
    if not article:
        return "Article not found", 404

    analytics = read_analytics()
    article_analytics = [a for a in analytics if a['article_id'] == article_id]

    total_views = sum(a['views'] for a in article_analytics)
    unique_visitors = sum(a['unique_visitors'] for a in article_analytics)

    return render_template('article_analytics.html',
                           analytics_page_id='analytics-page',
                           analytics_overview_id='analytics-overview',
                           analytics_total_views_id='analytics-total-views',
                           analytics_unique_visitors_id='analytics-unique-visitors',
                           back_to_article_analytics_id='back-to-article-analytics',
                           article=article,
                           total_views=total_views,
                           unique_visitors=unique_visitors)

if __name__ == '__main__':
    app.run(debug=True)
