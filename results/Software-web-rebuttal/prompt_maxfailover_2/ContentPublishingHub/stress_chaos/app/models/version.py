class Version:
    def __init__(self, version_id, article_id, version_number, content, status='draft'):
        self.version_id = version_id
        self.article_id = article_id
        self.version_number = version_number
        self.content = content
        self.status = status  # draft, approved, rejected
        self.approvals = []  # list of approval dictionaries
        self.comments = []  # list of comment dictionaries

    def to_dict(self):
        return {
            'version_id': self.version_id,
            'article_id': self.article_id,
            'version_number': self.version_number,
            'content': self.content,
            'status': self.status,
            'approvals': self.approvals,
            'comments': self.comments
        }
