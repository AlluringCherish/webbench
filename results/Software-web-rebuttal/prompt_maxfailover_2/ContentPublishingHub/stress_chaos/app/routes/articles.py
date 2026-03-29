from flask import Blueprint, request, jsonify
from app.services.business_logic import create_article, create_version, approve_version, add_comment, get_article_versions

articles_bp = Blueprint('articles', __name__)

@articles_bp.route('/article/create', methods=['POST'])
def create_article_route():
    data = request.form
    title = data.get('title')
    content = data.get('content')
    author = data.get('author')
    if not all([title, content, author]):
        return jsonify({'error': 'Missing data'}), 400
    article_id = len(articles_bp.__dict__) + 1  # simple id generation
    article = create_article(article_id, title, content, author)
    return jsonify({'message': 'Article created', 'article_id': article.article_id})

@articles_bp.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
def edit_article_route(article_id):
    if request.method == 'GET':
        versions = [v.to_dict() for v in get_article_versions(article_id)]
        return jsonify({'article_id': article_id, 'versions': versions})
    elif request.method == 'POST':
        content = request.form.get('content')
        if not content:
            return jsonify({'error': 'Missing content'}), 400
        version_id = 1  # For demo, assign static
        version_number = 1
        create_version(article_id, version_id, version_number, content)
        return jsonify({'message': 'Version added'})

@articles_bp.route('/article/<int:article_id>/versions/<int:version_id>/approve', methods=['POST'])
def approve_version_route(article_id, version_id):
    approver = request.form.get('approver')
    if not approver:
        return jsonify({'error': 'Missing approver'}), 400
    try:
        version = approve_version(article_id, version_id, approver)
        return jsonify({'message': 'Version approved'})
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

@articles_bp.route('/article/<int:article_id>/versions/<int:version_id>/comment', methods=['POST'])
def comment_version_route(article_id, version_id):
    commenter = request.form.get('commenter')
    comment_text = request.form.get('comment')
    if not all([commenter, comment_text]):
        return jsonify({'error': 'Missing comment data'}), 400
    try:
        version = add_comment(article_id, version_id, commenter, comment_text)
        return jsonify({'message': 'Comment added'})
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

@articles_bp.route('/article/<int:article_id>/analytics', methods=['GET'])
def analytics_route(article_id):
    # Placeholder analytics data
    data = {
        'article_id': article_id,
        'views': 123,
        'shares': 45,
        'comments': len(get_article_versions(article_id)[-1].comments) if get_article_versions(article_id) else 0
    }
    return jsonify(data)
