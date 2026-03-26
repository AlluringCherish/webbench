from flask import Flask, request, jsonify, redirect, url_for
from uuid import UUID, uuid4
from datetime import datetime
import os
import json
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change_this_to_a_secret_key'

DATA_DIR = 'data'

# Lock for file access synchronization
file_lock = threading.Lock()

# File paths constants
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
ARTICLES_FILE = os.path.join(DATA_DIR, 'articles.txt')
VERSIONS_FILE = os.path.join(DATA_DIR, 'versions.txt')
APPROVALS_FILE = os.path.join(DATA_DIR, 'approvals.txt')
COMMENTS_FILE = os.path.join(DATA_DIR, 'comments.txt')
WORKFLOW_STAGES_FILE = os.path.join(DATA_DIR, 'workflow_stages.txt')
ANALYTICS_FILE = os.path.join(DATA_DIR, 'analytics.txt')

# Utility functions for UUID validation

def is_valid_uuid(val):
    try:
        UUID(str(val))
        return True
    except Exception:
        return False

# --- Data Loading and Saving Utilities ---

# Each data file is stored in JSON Lines (one JSON object per line) or JSON array format.
# The original architecture discussed text files but for structured data JSON lines or JSON array allows robust parsing.

# We'll use JSON arrays for all files - easier for random access.

# Thread safety is applied using file_lock where needed.


def load_json_array_file(path):
    with file_lock:
        if not os.path.exists(path):
            return []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                data = json.loads(content)
                if not isinstance(data, list):
                    return []
                return data
        except Exception:
            # Corrupt or unreadable file
            return []

def save_json_array_file(path, data_list):
    with file_lock:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data_list, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

# --- Data Models ---
# Not ORM but dict/data structure based since reading from text files

# USERS
# User schema assumed: {"user_id":uuid4 str, "username":str, "email":str, "profile":dict}

def get_user_by_id(user_id):
    users = load_json_array_file(USERS_FILE)
    for u in users:
        if u.get('user_id') == user_id:
            return u
    return None

# Currently, no authentication is described. We simulate current user via a header 'X-User-Id'.
# This is a simplified stand-in for real authentication middleware.

def get_current_user():
    user_id = request.headers.get('X-User-Id')
    if user_id and is_valid_uuid(user_id):
        user = get_user_by_id(user_id)
        if user:
            return user
    return None

# ARTICLES
# Article schema assumed: {"article_id": UUID str, "owner_id":UUID str, "title":str, "category":str, "created_at":datetime ISO8601 str}

def get_article_by_id(article_id):
    articles = load_json_array_file(ARTICLES_FILE)
    for a in articles:
        if a.get('article_id') == article_id:
            return a
    return None

# VERSIONS
# Version schema: {"version_id":uuid str, "article_id": uuid str, "version_number": int, "content":str, "author_id": uuid str, "timestamp": ISO8601 str, "change_summary": str, "status":str}
# status in workflow stages (Draft, Editor Review, Approval, Published, Archived)

def get_versions_by_article(article_id):
    versions = load_json_array_file(VERSIONS_FILE)
    article_versions = [v for v in versions if v.get('article_id') == article_id]
    # Sorted by version_number ascending
    article_versions.sort(key=lambda x: x.get('version_number', 0))
    return article_versions

def get_version_by_id(version_id):
    versions = load_json_array_file(VERSIONS_FILE)
    for v in versions:
        if v.get('version_id') == version_id:
            return v
    return None

# Approvals
# Schema: {"approval_id": uuid str, "version_id": uuid str, "approver_id": uuid str, "status": str, "comments": str, "timestamp": ISO8601 str}

def get_approvals_by_version(version_id):
    approvals = load_json_array_file(APPROVALS_FILE)
    return [a for a in approvals if a.get('version_id') == version_id]

# Comments
# Schema: {"comment_id": uuid str, "article_id": uuid str, "version_id": uuid str, "user_id": uuid str, "comment": str, "timestamp": ISO8601 str}

def get_comments_by_article_version(article_id, version_id):
    comments = load_json_array_file(COMMENTS_FILE)
    return [c for c in comments if c.get('article_id') == article_id and c.get('version_id') == version_id]

# Workflow stages
# Schema: [{"stage_name":str, "order":int, "permissions": [str]}]

def get_workflow_stages():
    stages = load_json_array_file(WORKFLOW_STAGES_FILE)
    # sort by order asc
    stages.sort(key=lambda x: x.get('order', 0))
    return stages

# Analytics
# Schema: [{"article_id": uuid str, "views": int, "unique_visitors": int, "avg_time_seconds": float, "shares": int}]

def get_analytics_by_article(article_id):
    analytics_list = load_json_array_file(ANALYTICS_FILE)
    for a in analytics_list:
        if a.get('article_id') == article_id:
            return a
    return {
        'article_id': article_id,
        'views': 0,
        'unique_visitors': 0,
        'avg_time_seconds': 0.0,
        'shares': 0
    }

# --- Route Implementations ---

@app.route('/')
def root():
    # Redirect to /dashboard
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    # Provide quick stats and summaries
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized, missing or invalid user'}), 401

    articles = load_json_array_file(ARTICLES_FILE)
    versions = load_json_array_file(VERSIONS_FILE)
    approvals = load_json_array_file(APPROVALS_FILE)
    comments = load_json_array_file(COMMENTS_FILE)

    total_articles = len(articles)
    total_versions = len(versions)
    total_approvals = len(approvals)
    total_comments = len(comments)

    # For user owned articles count
    owned_articles_count = sum(1 for a in articles if a.get('owner_id') == user['user_id'])

    # Recent articles (latest 5 by created_at)
    articles_sorted = sorted(articles, key=lambda x: x.get('created_at', ''), reverse=True)
    recent_articles = articles_sorted[:5]

    return jsonify({
        'user': {'user_id': user['user_id'], 'username': user['username']},
        'total_articles': total_articles,
        'total_versions': total_versions,
        'total_approvals': total_approvals,
        'total_comments': total_comments,
        'owned_articles_count': owned_articles_count,
        'recent_articles': recent_articles
    })

@app.route('/articles/create', methods=['GET', 'POST'])
def create_article():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized, missing or invalid user'}), 401

    if request.method == 'GET':
        # Return basic info or form field info
        return jsonify({'message': 'Provide Title and Content in POST to create article'})

    # POST method: create new article + initial version
    title = request.form.get('Title') or request.json.get('Title') if request.is_json else request.form.get('Title')
    content = request.form.get('Content') or request.json.get('Content') if request.is_json else request.form.get('Content')

    if not title or not content:
        return jsonify({'error': 'Title and Content are required'}), 400

    # Create article
    articles = load_json_array_file(ARTICLES_FILE)

    article_id = str(uuid4())
    now_iso = datetime.utcnow().isoformat() + 'Z'
    new_article = {
        'article_id': article_id,
        'owner_id': user['user_id'],
        'title': title,
        'category': '',  # default empty until extended
        'created_at': now_iso
    }
    articles.append(new_article)
    if not save_json_array_file(ARTICLES_FILE, articles):
        return jsonify({'error': 'Failed to save article data'}), 500

    # Create initial version
    versions = load_json_array_file(VERSIONS_FILE)
    version_id = str(uuid4())
    new_version = {
        'version_id': version_id,
        'article_id': article_id,
        'version_number': 1,
        'content': content,
        'author_id': user['user_id'],
        'timestamp': now_iso,
        'change_summary': 'Initial version',
        'status': 'Draft'
    }
    versions.append(new_version)
    if not save_json_array_file(VERSIONS_FILE, versions):
        return jsonify({'error': 'Failed to save article version data'}), 500

    return jsonify({'message': 'Article created successfully', 'article_id': article_id, 'version_id': version_id}), 201

@app.route('/articles/edit/<article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized, missing or invalid user'}), 401

    if not is_valid_uuid(article_id):
        return jsonify({'error': 'Invalid article_id format'}), 400

    article = get_article_by_id(article_id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404

    if article['owner_id'] != user['user_id']:
        return jsonify({'error': 'Forbidden: you do not own this article'}), 403

    if request.method == 'GET':
        # Return latest version content for editing
        versions = get_versions_by_article(article_id)
        if not versions:
            return jsonify({'error': 'No versions found for this article'}), 404
        latest_version = versions[-1]
        return jsonify({
            'article_id': article_id,
            'title': article['title'],
            'latest_version': latest_version
        })

    # POST method: create new version with updated content
    content = request.form.get('Content') or request.json.get('Content') if request.is_json else request.form.get('Content')
    change_summary = request.form.get('ChangeSummary') or request.json.get('ChangeSummary') if request.is_json else request.form.get('ChangeSummary')

    if not content:
        return jsonify({'error': 'Content is required'}), 400

    if not change_summary:
        change_summary = 'Updated content'

    versions = load_json_array_file(VERSIONS_FILE)
    article_versions = [v for v in versions if v.get('article_id') == article_id]
    version_numbers = [v.get('version_number', 0) for v in article_versions]
    new_version_number = max(version_numbers) + 1 if version_numbers else 1

    version_id = str(uuid4())
    now_iso = datetime.utcnow().isoformat() + 'Z'

    new_version = {
        'version_id': version_id,
        'article_id': article_id,
        'version_number': new_version_number,
        'content': content,
        'author_id': user['user_id'],
        'timestamp': now_iso,
        'change_summary': change_summary,
        'status': 'Draft'
    }

    versions.append(new_version)
    if not save_json_array_file(VERSIONS_FILE, versions):
        return jsonify({'error': 'Failed to save new version data'}), 500

    return jsonify({'message': 'Article updated with new version', 'version_id': version_id}), 201

@app.route('/article/<article_id>/versions', methods=['GET'])
def article_versions(article_id):
    if not is_valid_uuid(article_id):
        return jsonify({'error': 'Invalid article_id format'}), 400

    article = get_article_by_id(article_id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404

    versions = get_versions_by_article(article_id)

    return jsonify({'article_id': article_id, 'versions': versions})

@app.route('/articles/mine', methods=['GET'])
def my_articles():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized, missing or invalid user'}), 401

    articles = load_json_array_file(ARTICLES_FILE)
    user_articles = [a for a in articles if a.get('owner_id') == user['user_id']]
    return jsonify({'articles': user_articles})

@app.route('/articles/published', methods=['GET'])
def published_articles():
    # Filters
    category = request.args.get('category', '').strip()
    sort_order = request.args.get('sort_order', 'asc').lower()  # asc or desc

    articles = load_json_array_file(ARTICLES_FILE)
    versions = load_json_array_file(VERSIONS_FILE)

    # We want articles whose some version is published
    published_articles_set = set()
    latest_versions_map = {}

    for v in versions:
        if v.get('status', '').lower() == 'published':
            article_id = v.get('article_id')
            # Track latest published version number per article
            if article_id not in latest_versions_map or v['version_number'] > latest_versions_map[article_id]['version_number']:
                latest_versions_map[article_id] = v
            published_articles_set.add(article_id)

    filtered_articles = [a for a in articles if a.get('article_id') in published_articles_set]

    if category:
        filtered_articles = [a for a in filtered_articles if a.get('category') == category]

    # Sort by created_at or title or default by title
    if sort_order not in ['asc', 'desc']:
        sort_order = 'asc'

    # Let's sort by title ascending or descending
    filtered_articles.sort(key=lambda x: x.get('title', '').lower(), reverse=(sort_order == 'desc'))

    # For each article add latest published version number info
    response = []
    for art in filtered_articles:
        article_id = art.get('article_id')
        latest_version = latest_versions_map.get(article_id, None)
        item = art.copy()
        if latest_version:
            item['published_version_number'] = latest_version.get('version_number')
        response.append(item)

    return jsonify({'published_articles': response})

@app.route('/calendar', methods=['GET'])
def calendar():
    # Provide article publishing calendar data
    # Return list of published articles and their published dates

    versions = load_json_array_file(VERSIONS_FILE)
    articles = load_json_array_file(ARTICLES_FILE)

    calendar_entries = []

    for v in versions:
        if v.get('status', '').lower() == 'published':
            article = get_article_by_id(v.get('article_id'))
            if article:
                calendar_entries.append({
                    'article_id': article['article_id'],
                    'title': article.get('title', ''),
                    'published_version_number': v.get('version_number'),
                    'published_at': v.get('timestamp')
                })

    # Sort by published_at ascending
    calendar_entries.sort(key=lambda x: x.get('published_at', ''))

    return jsonify({'calendar': calendar_entries})

@app.route('/analytics/article/<article_id>', methods=['GET'])
def article_analytics(article_id):
    if not is_valid_uuid(article_id):
        return jsonify({'error': 'Invalid article_id format'}), 400

    article = get_article_by_id(article_id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404

    analytics = get_analytics_by_article(article_id)

    return jsonify({'analytics': analytics})

# Approvals and Comments APIs are part of the backend as per architecture
# Here are rudimentary handlers for approval workflow and comments linked to articles and versions

@app.route('/approvals/version/<version_id>', methods=['GET'])
def get_approvals_for_version(version_id):
    if not is_valid_uuid(version_id):
        return jsonify({'error': 'Invalid version_id format'}), 400

    version = get_version_by_id(version_id)
    if not version:
        return jsonify({'error': 'Version not found'}), 404

    approvals = get_approvals_by_version(version_id)
    return jsonify({'approvals': approvals})

@app.route('/approvals/version/<version_id>/add', methods=['POST'])
def add_approval(version_id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    if not is_valid_uuid(version_id):
        return jsonify({'error': 'Invalid version_id format'}), 400

    version = get_version_by_id(version_id)
    if not version:
        return jsonify({'error': 'Version not found'}), 404

    # Only allow approver to add approval if user is authorized - assuming all users for now
    status = request.form.get('Status') or request.json.get('Status') if request.is_json else request.form.get('Status')
    comments = request.form.get('Comments') or request.json.get('Comments') if request.is_json else request.form.get('Comments')

    if not status or status not in ['Approved', 'Rejected', 'Pending']:
        return jsonify({'error': 'Invalid or missing approval status'}), 400

    now_iso = datetime.utcnow().isoformat() + 'Z'
    approvals = load_json_array_file(APPROVALS_FILE)

    new_approval = {
        'approval_id': str(uuid4()),
        'version_id': version_id,
        'approver_id': user['user_id'],
        'status': status,
        'comments': comments or '',
        'timestamp': now_iso
    }

    approvals.append(new_approval)
    if not save_json_array_file(APPROVALS_FILE, approvals):
        return jsonify({'error': 'Failed to save approval'}), 500

    # Transition version status if all required approvals met
    # Simplified: If approved, set version status to Published
    if status == 'Approved':
        versions = load_json_array_file(VERSIONS_FILE)
        for v in versions:
            if v.get('version_id') == version_id:
                v['status'] = 'Published'
                break
        save_json_array_file(VERSIONS_FILE, versions)

    return jsonify({'message': 'Approval recorded successfully'})

@app.route('/comments/article/<article_id>/version/<version_id>', methods=['GET'])
def get_comments(article_id, version_id):
    if not is_valid_uuid(article_id) or not is_valid_uuid(version_id):
        return jsonify({'error': 'Invalid article_id or version_id format'}), 400

    article = get_article_by_id(article_id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404

    version = get_version_by_id(version_id)
    if not version:
        return jsonify({'error': 'Version not found'}), 404

    comments = get_comments_by_article_version(article_id, version_id)

    return jsonify({'comments': comments})

@app.route('/comments/article/<article_id>/version/<version_id>/add', methods=['POST'])
def add_comment(article_id, version_id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    if not is_valid_uuid(article_id) or not is_valid_uuid(version_id):
        return jsonify({'error': 'Invalid article_id or version_id format'}), 400

    article = get_article_by_id(article_id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404

    version = get_version_by_id(version_id)
    if not version:
        return jsonify({'error': 'Version not found'}), 404

    comment_text = request.form.get('Comment') or request.json.get('Comment') if request.is_json else request.form.get('Comment')
    if not comment_text:
        return jsonify({'error': 'Comment text is required'}), 400

    now_iso = datetime.utcnow().isoformat() + 'Z'
    comments = load_json_array_file(COMMENTS_FILE)

    new_comment = {
        'comment_id': str(uuid4()),
        'article_id': article_id,
        'version_id': version_id,
        'user_id': user['user_id'],
        'comment': comment_text,
        'timestamp': now_iso
    }

    comments.append(new_comment)
    if not save_json_array_file(COMMENTS_FILE, comments):
        return jsonify({'error': 'Failed to save comment'}), 500

    return jsonify({'message': 'Comment added successfully', 'comment_id': new_comment['comment_id']})

# Main entry for debug or normal run
if __name__ == '__main__':
    # Create data directory if missing
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    app.run(debug=True, host='0.0.0.0', port=5000)
