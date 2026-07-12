# NewsPortal Application Design Specifications

---

## Section 1: Flask Routes Specification

| Route Path                  | Function Name          | HTTP Method | Template File             | Context Variables (Name: Type)                                                                                              | Form Data (POST)                  |
|-----------------------------|-----------------------|-------------|---------------------------|----------------------------------------------------------------------------------------------------------------------------|----------------------------------|
| /                           | root_redirect          | GET         | N/A (Redirect to /dashboard) | None                                                                                                                       | N/A                              |
| /dashboard                  | dashboard_page        | GET         | dashboard.html            | featured_articles: list of dicts (article_id: int, title: str, author: str, date: str), trending_articles: list of dicts (article_id: int, title: str), - | N/A                              |
| /articles                   | article_catalog_page  | GET         | article_catalog.html      | articles: list of dicts (article_id: int, title: str, author: str, date: str, category: str), categories: list of dicts (category_id: int, category_name: str) | N/A                              |
| /articles/<int:article_id>  | article_details_page  | GET         | article_details.html      | article: dict (article_id: int, title: str, author: str, date: str, content: str), is_bookmarked: bool                        | POST (bookmark action)            |
| /bookmarks                  | bookmarks_page        | GET         | bookmarks.html            | bookmarks: list of dicts (bookmark_id: int, article_id: int, article_title: str, bookmarked_date: str)                       | POST (remove bookmark)            |
| /comments                   | comments_page         | GET         | comments.html             | comments: list of dicts (comment_id: int, article_id: int, article_title: str, commenter_name: str, comment_text: str), articles: list of dicts (article_id: int, title: str) | N/A                              |
| /comments/write             | write_comment_page    | GET         | write_comment.html        | articles: list of dicts (article_id: int, title: str)                                                                         | POST (comment submission)         |
| /trending                  | trending_articles_page | GET         | trending_articles.html    | trending_articles: list of dicts (article_id: int, title: str, category: str, view_count: int, period: str)                   | N/A                              |
| /category/<string:category_name> | category_articles_page | GET         | category.html             | category_name: str, category_articles: list of dicts (article_id: int, title: str, date: str, popularity: int)                 | N/A                              |
| /search                    | search_results_page   | GET         | search_results.html       | query: str, results: list of dicts (article_id: int, title: str, excerpt: str)                                               | N/A                              |

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- File path: templates/dashboard.html
- Page title: News Portal
- Page <h1>: News Portal
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page
  - featured-articles (Div): Display of featured article recommendations
  - browse-articles-button (Button): Navigate to article catalog page
  - view-bookmarks-button (Button): Navigate to bookmarks page
  - trending-articles-button (Button): Navigate to trending articles page
- Context Variables:
  - featured_articles: list of dicts with keys article_id (int), title (str), author (str), date (str)
  - trending_articles: list of dicts with keys article_id (int), title (str)
- Navigation:
  - browse-articles-button: url_for('article_catalog_page')
  - view-bookmarks-button: url_for('bookmarks_page')
  - trending-articles-button: url_for('trending_articles_page')

### 2. article_catalog.html
- File path: templates/article_catalog.html
- Page title: Article Catalog
- Page <h1>: Article Catalog
- Element IDs:
  - catalog-page (Div): Container for the catalog page
  - search-input (Input): Field to search articles
  - category-filter (Dropdown): Dropdown to filter by category
  - articles-grid (Div): Grid displaying article cards
  - view-article-button-{article_id} (Button): Button to view article details
- Context Variables:
  - articles: list of dicts with article_id (int), title (str), author (str), date (str), category (str)
  - categories: list of dicts with category_id (int), category_name (str)
- Navigation:
  - view-article-button-{article_id}: url_for('article_details_page', article_id=article_id)

### 3. article_details.html
- File path: templates/article_details.html
- Page title: Article Details
- Page <h1>: Article Details
- Element IDs:
  - article-details-page (Div): Container for the article details page
  - article-title (H1): Display article title
  - article-author (Div): Display article author
  - article-date (Div): Display article publication date
  - bookmark-button (Button): Button to bookmark the article
  - article-content (Div): Full article content
- Context Variables:
  - article: dict with article_id (int), title (str), author (str), date (str), content (str)
  - is_bookmarked: bool (indicates if article is bookmarked)
- Navigation:
  - bookmark-button: POST action on current route to bookmark

### 4. bookmarks.html
- File path: templates/bookmarks.html
- Page title: My Bookmarks
- Page <h1>: My Bookmarks
- Element IDs:
  - bookmarks-page (Div): Container for bookmarks page
  - bookmarks-list (Div): List displaying all bookmarked articles
  - remove-bookmark-button-{bookmark_id} (Button): Button to remove bookmark
  - read-bookmark-button-{bookmark_id} (Button): Button to read bookmarked article details
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - bookmarks: list of dicts with bookmark_id (int), article_id (int), article_title (str), bookmarked_date (str)
- Navigation:
  - read-bookmark-button-{bookmark_id}: url_for('article_details_page', article_id=article_id)
  - back-to-dashboard: url_for('dashboard_page')

### 5. comments.html
- File path: templates/comments.html
- Page title: Article Comments
- Page <h1>: Article Comments
- Element IDs:
  - comments-page (Div): Container for comments page
  - comments-list (Div): List of all comments
  - write-comment-button (Button): Navigate to write comment page
  - filter-by-article (Dropdown): Dropdown to filter comments by article
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - comments: list of dicts with comment_id (int), article_id (int), article_title (str), commenter_name (str), comment_text (str)
  - articles: list of dicts with article_id (int), title (str)
- Navigation:
  - write-comment-button: url_for('write_comment_page')
  - back-to-dashboard: url_for('dashboard_page')

### 6. write_comment.html
- File path: templates/write_comment.html
- Page title: Write a Comment
- Page <h1>: Write a Comment
- Element IDs:
  - write-comment-page (Div): Container for the write comment page
  - select-article (Dropdown): Select article to comment on
  - commenter-name (Input): Input for commenter name
  - comment-text (Textarea): Comment text area
  - submit-comment-button (Button): Submit comment
- Context Variables:
  - articles: list of dicts with article_id (int), title (str)
- Navigation:
  - submit-comment-button: POST to current route to submit comment

### 7. trending_articles.html
- File path: templates/trending_articles.html
- Page title: Trending Articles
- Page <h1>: Trending Articles
- Element IDs:
  - trending-page (Div): Container for trending articles page
  - trending-list (Div): Ranked list of trending articles
  - time-period-filter (Dropdown): Filter by time period
  - view-article-button-{article_id} (Button): Button to view article details
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - trending_articles: list of dicts with article_id (int), title (str), category (str), view_count (int), period (str)
- Navigation:
  - view-article-button-{article_id}: url_for('article_details_page', article_id=article_id)
  - back-to-dashboard: url_for('dashboard_page')

### 8. category.html
- File path: templates/category.html
- Page title: Category Articles
- Page <h1>: Category Articles
- Element IDs:
  - category-page (Div): Container for the category page
  - category-title (H1): Display category name
  - category-articles (Div): List of articles in category
  - sort-by-date (Button): Sort articles by date
  - sort-by-popularity (Button): Sort articles by popularity
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - category_name: str
  - category_articles: list of dicts with article_id (int), title (str), date (str), popularity (int)
- Navigation:
  - back-to-dashboard: url_for('dashboard_page')

### 9. search_results.html
- File path: templates/search_results.html
- Page title: Search Results
- Page <h1>: Search Results
- Element IDs:
  - search-results-page (Div): Container for search results
  - search-query-display (Div): Display search query
  - results-list (Div): List of search results
  - no-results-message (Div): Message if no results found
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - query: str
  - results: list of dicts with article_id (int), title (str), excerpt (str)
- Navigation:
  - back-to-dashboard: url_for('dashboard_page')

---

## Section 3: Data File Schemas

### 1. Articles Data
- File path: data/articles.txt
- Format: Pipe-delimited `article_id|title|author|category|content|date|views`
- Description: Stores all news articles with metadata and content
- Example rows:
  - 1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  - 2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  - 3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891

### 2. Categories Data
- File path: data/categories.txt
- Format: Pipe-delimited `category_id|category_name|description`
- Description: Stores news categories and their descriptions
- Example rows:
  - 1|Technology|Latest tech news and innovations
  - 2|Sports|Sports news and event coverage
  - 3|Business|Business and finance news

### 3. Bookmarks Data
- File path: data/bookmarks.txt
- Format: Pipe-delimited `bookmark_id|article_id|article_title|bookmarked_date`
- Description: Stores bookmarked articles with bookmark date
- Example rows:
  - 1|1|Breaking: New Technology Breakthrough|2025-01-20
  - 2|3|Business: Market Trends Analysis|2025-01-18

### 4. Comments Data
- File path: data/comments.txt
- Format: Pipe-delimited `comment_id|article_id|article_title|commenter_name|comment_text|comment_date`
- Description: Stores comments on articles
- Example rows:
  - 1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  - 2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19

### 5. Trending Data
- File path: data/trending.txt
- Format: Pipe-delimited `article_id|article_title|category|view_count|period`
- Description: Stores trending articles data by time period
- Example rows:
  - 1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  - 2|Sports: Championship Victory|Sports|3210|This Week
  - 3|Business: Market Trends Analysis|Business|2891|This Month

---

*End of NewsPortal Design Specifications*