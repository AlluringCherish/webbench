class Article:
    def __init__(self, article_id, title, content, author, published=False):
        self.article_id = article_id
        self.title = title
        self.content = content
        self.author = author
        self.published = published
        self.versions = []  # list of version objects

    def to_dict(self):
        return {
            'article_id': self.article_id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'published': self.published,
            'versions': [v.to_dict() for v in self.versions]
        }
