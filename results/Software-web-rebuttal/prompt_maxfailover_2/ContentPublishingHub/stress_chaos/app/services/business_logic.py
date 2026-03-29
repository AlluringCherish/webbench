# Business logic related to articles, versions, approvals, comments
from app.models.article import Article
from app.models.version import Version

# Store articles in memory for demo purposes
articles_store = {}
versions_store = {}


def create_article(article_id, title, content, author):
    article = Article(article_id, title, content, author)
    articles_store[article_id] = article
    return article


def create_version(article_id, version_id, version_number, content):
    if article_id not in articles_store:
        raise ValueError("Article does not exist")
    version = Version(version_id, article_id, version_number, content)
    if article_id not in versions_store:
        versions_store[article_id] = []
    versions_store[article_id].append(version)
    articles_store[article_id].versions.append(version)
    return version


def approve_version(article_id, version_id, approver):
    if article_id not in versions_store:
        raise ValueError("No versions found for article")
    for version in versions_store[article_id]:
        if version.version_id == version_id:
            # add approval
            approval = {'approver': approver, 'status': 'approved'}
            version.approvals.append(approval)
            version.status = 'approved'
            return version
    raise ValueError("Version not found")


def add_comment(article_id, version_id, commenter, comment_text):
    if article_id not in versions_store:
        raise ValueError("No versions found for article")
    for version in versions_store[article_id]:
        if version.version_id == version_id:
            comment = {'commenter': commenter, 'comment': comment_text}
            version.comments.append(comment)
            return version
    raise ValueError("Version not found")


def get_article_versions(article_id):
    if article_id not in versions_store:
        return []
    return versions_store[article_id]
