import unittest
from unittest.mock import patch, mock_open
import app
from flask import Flask
class TestApp(unittest.TestCase):
    def setUp(self):
        app.app.config['TESTING'] = True
        self.client = app.app.test_client()
    def test_dashboard_page_loads(self):
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'quick_stats', response.data)
        self.assertIn(b'recent_activity', response.data)
    def test_create_article_get(self):
        response = self.client.get('/article/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'create_article', response.data)
    @patch('app.load_articles')
    @patch('app.load_article_versions')
    @patch('app.get_current_user')
    @patch('app.save_articles')
    @patch('app.save_article_versions')
    def test_create_article_post_creates_article(self, mock_save_versions, mock_save_articles, mock_get_user, mock_load_versions, mock_load_articles):
        mock_get_user.return_value = 'john'
        mock_load_articles.return_value = {}
        mock_load_versions.return_value = {}
        response = self.client.post('/article/create', data={
            'article-title': 'Test Article',
            'article-content': 'Content here'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Article created and version saved', response.data)
        mock_save_articles.assert_called_once()
        mock_save_versions.assert_called_once()
    @patch('app.load_articles')
    @patch('app.load_article_versions')
    @patch('app.get_current_user')
    @patch('app.save_articles')
    @patch('app.save_article_versions')
    def test_edit_article_get_and_post(self, mock_save_versions, mock_save_articles, mock_get_user, mock_load_versions, mock_load_articles):
        mock_get_user.return_value = 'john'
        article_id = '1'
        mock_load_articles.return_value = {
            article_id: {
                'article_id': article_id,
                'title': 'Old Title',
                'author': 'john',
                'category': 'blog',
                'status': 'draft',
                'tags': [],
                'featured_image': '',
                'meta_description': '',
                'created_date': '2024-01-20',
                'publish_date': ''
            }
        }
        mock_load_versions.return_value = {
            article_id: [{
                'version_id': '1',
                'article_id': article_id,
                'version_number': 1,
                'content': 'Old content',
                'author': 'john',
                'created_date': '2024-01-20 10:00:00',
                'change_summary': 'Initial draft'
            }]
        }
        # GET request
        response = self.client.get(f'/article/{article_id}/edit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Old Title', response.data)
        # POST request with update
        response = self.client.post(f'/article/{article_id}/edit', data={
            'edit-article-title': 'New Title',
            'edit-article-content': 'New content',
            'change-summary': 'Updated content'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New 2 saved', response.data)
        mock_save_articles.assert_called_once()
        mock_save_versions.assert_called_once()
    @patch('app.load_article_versions')
    @patch('app.get_current_user')
    @patch('app.save_article_versions')
    def test_restore_article_version(self, mock_save_versions, mock_get_user, mock_load_versions):
        article_id = '1'
        mock_get_user.return_value = 'john'
        mock_load_versions.return_value = {
            article_id: [
                {
                    'version_id': '1',
                    'article_id': article_id,
                    'version_number': 1,
                    'content': 'Content v1',
                    'author': 'john',
                    'created_date': '2024-01-20 10:00:00',
                    'change_summary': 'Initial draft'
                },
                {
                    'version_id': '2',
                    'article_id': article_id,
                    'version_number': 2,
                    'content': 'Content v2',
                    'author': 'john',
                    'created_date': '2024-01-21 10:00:00',
                    'change_summary': 'Second draft'
                }
            ]
        }
        with app.app.test_request_context(f'/article/{article_id}/versions', method='POST', data={'restore_version_id': '1'}):
            from restore_version import restore_article_version
            response = restore_article_version(article_id)
            self.assertIn('restored new version', response)
    def test_my_articles_filter_status(self):
        with patch('app.load_articles') as mock_load_articles, patch('app.get_current_user') as mock_get_user:
            mock_get_user.return_value = 'john'
            mock_load_articles.return_value = {
                '1': {'article_id': '1', 'author': 'john', 'status': 'draft', 'title': 'Draft Article', 'category': 'blog', 'created_date': '2024-01-20', 'publish_date': ''},
                '2': {'article_id': '2', 'author': 'john', 'status': 'published', 'title': 'Published Article', 'category': 'blog', 'created_date': '2024-01-21', 'publish_date': '2024-01-22 10:00:00'},
                '3': {'article_id': '3', 'author': 'alice', 'status': 'draft', 'title': 'Other User Article', 'category': 'blog', 'created_date': '2024-01-23', 'publish_date': ''}
            }
            response = self.client.get('/articles/mine?filter-article-status=draft')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Draft Article', response.data)
            self.assertNotIn(b'Published Article', response.data)
            self.assertNotIn(b'Other User Article', response.data)
    def test_published_articles_filter_and_sort(self):
        with patch('app.load_articles') as mock_load_articles:
            mock_load_articles.return_value = {
                '1': {'article_id': '1', 'author': 'john', 'status': 'published', 'title': 'B Title', 'category': 'blog', 'created_date': '2024-01-20', 'publish_date': '2024-01-22 10:00:00'},
                '2': {'article_id': '2', 'author': 'alice', 'status': 'published', 'title': 'A Title', 'category': 'tutorial', 'created_date': '2024-01-21', 'publish_date': '2024-01-23 10:00:00'},
                '3': {'article_id': '3', 'author': 'bob', 'status': 'draft', 'title': 'Draft Article', 'category': 'blog', 'created_date': '2024-01-23', 'publish_date': ''}
            }
            # Filter by category tutorial and sort by title ascending
            response = self.client.get('/articles/published?filter-published-category=tutorial&sort-published=title_asc')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'A Title', response.data)
            self.assertNotIn(b'B Title', response.data)
            self.assertNotIn(b'Draft Article', response.data)
    def test_content_calendar_page(self):
        with patch('app.load_articles') as mock_load_articles:
            mock_load_articles.return_value = {
                '1': {'article_id': '1', 'author': 'john', 'status': 'published', 'title': 'Scheduled Article', 'category': 'blog', 'created_date': '2024-01-20', 'publish_date': '2024-02-01 10:00:00'},
                '2': {'article_id': '2', 'author': 'alice', 'status': 'draft', 'title': 'Draft Article', 'category': 'blog', 'created_date': '2024-01-21', 'publish_date': ''}
            }
            response = self.client.get('/content_calendar')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Scheduled Article', response.data)
            self.assertNotIn(b'Draft Article', response.data)
    def test_article_analytics_page(self):
        with patch('app.load_articles') as mock_load_articles, patch('app.load_analytics') as mock_load_analytics:
            article_id = '1'
            mock_load_articles.return_value = {
                article_id: {'article_id': article_id, 'author': 'john', 'status': 'published', 'title': 'Article', 'category': 'blog', 'created_date': '2024-01-20', 'publish_date': '2024-01-22 10:00:00'}
            }
            mock_load_analytics.return_value = [
                {'analytics_id': '1', 'article_id': article_id, 'date': '2024-01-22', 'views': 150, 'unique_visitors': 120, 'avg_time_seconds': 245, 'shares': 12},
                {'analytics_id': '2', 'article_id': article_id, 'date': '2024-01-23', 'views': 180, 'unique_visitors': 140, 'avg_time_seconds': 220, 'shares': 15}
            ]
            response = self.client.get(f'/article/{article_id}/analytics')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Total Views', response.data)
            self.assertIn(b'Unique Visitors', response.data)
if __name__ == '__main__':
    unittest.main()