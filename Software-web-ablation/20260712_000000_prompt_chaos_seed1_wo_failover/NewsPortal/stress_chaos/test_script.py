import unittest
from app import app

class NewsPortalTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_dashboard_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'News Portal', response.data)

    def test_article_catalog_page(self):
        response = self.app.get('/catalog')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Articles', response.data)

    def test_article_details_page_valid(self):
        # Assuming article_id 1 exists
        response = self.app.get('/article/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Details', response.data)

    def test_article_details_page_invalid(self):
        response = self.app.get('/article/99999')
        self.assertEqual(response.status_code, 302)  # redirect

    def test_bookmarks_page(self):
        response = self.app.get('/bookmarks')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My Bookmarks', response.data)

    def test_add_and_remove_bookmark(self):
        # Bookmark article_id 1
        response = self.app.get('/bookmark/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My Bookmarks', response.data)

        # Remove bookmark with id 1
        response = self.app.get('/remove_bookmark/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My Bookmarks', response.data)

    def test_comments_page(self):
        response = self.app.get('/comments')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comments', response.data)

    def test_submit_comment(self):
        data = {
            'article_id': '1',
            'commenter_name': 'Tester',
            'comment_text': 'This is a test comment.'
        }
        response = self.app.post('/comments/submit', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comments', response.data)

    def test_trending_articles_page(self):
        response = self.app.get('/trending')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Trending', response.data)

    def test_search(self):
        response = self.app.get('/search?query=news')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Search Results', response.data)

if __name__ == '__main__':
    unittest.main()
