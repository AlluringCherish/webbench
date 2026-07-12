import unittest
from flask import url_for
from your_newsportal_app import app

class NewsPortalIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_navigation_flow(self):
        # Test home/dashboard page
        response = self.app.get(url_for('dashboard_page'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Featured Articles', response.data)

        # Test article catalog page
        response = self.app.get(url_for('article_catalog_page'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Articles', response.data)

        # Test one article detail page
        response = self.app.get('/article/1')  # Assuming article_id=1 exists
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Content', response.data)

        # Test bookmarks page
        response = self.app.get(url_for('bookmarks_page'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bookmarks', response.data)

        # Test comments page
        response = self.app.get(url_for('comments_page'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comments', response.data)

        # Test trending articles page
        response = self.app.get(url_for('trending_articles_page'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Trending', response.data)

        # Test search functionality
        response = self.app.get('/search?q=test')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Results', response.data)

    def test_comments_functionality(self):
        # POST a new comment
        response = self.app.post('/write_comment', data={
            'article_id': '1',
            'commenter_name': 'Tester',
            'comment_text': 'This is a test comment'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This is a test comment', response.data)

    def test_bookmarking_functionality(self):
        # POST add a bookmark
        response = self.app.post('/article/1', data={'bookmark': 'true'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bookmark added', response.data)  # Assuming this message

        # POST remove a bookmark
        response = self.app.post('/remove_bookmark', data={'remove_bookmark_id': '1'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bookmark removed', response.data)  # Assuming this message

    def test_article_sorting_comments(self):
        response = self.app.get('/comments')
        self.assertEqual(response.status_code, 200)
        # Can add more checks for sorting and content

    def test_content_and_ids(self):
        response = self.app.get('/articles')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'article_id', response.data)

if __name__ == '__main__':
    unittest.main()
