# NewsPortal Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                       | Function Name          | HTTP Method | Template File          | Context Variables (name: type)                                                                                                                                                    | Form Data (POST routes)                                            |
|--------------------------------|------------------------|-------------|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| /                              | redirect_to_dashboard  | GET         | N/A (redirect)          | None                                                                                                                                                                              | None                                                             |
| /dashboard                    | dashboard              | GET         | dashboard.html         | featured_articles: list of dict (article_id:int, title:str, author:str, date:str, excerpt:str)                                                                                     | None                                                             |
| /catalog                     | article_catalog        | GET         | article_catalog.html   | articles: list of dict (article_id:int, title:str, author:str, date:str, category:str, thumbnail_url:str), categories: list of dict (category_id:int, category_name:str)          | None                                                             |
| /catalog/search              | search_results         | POST        | search_results.html    | query: str, results: list of dict (article_id:int, title:str, excerpt:str)                                                                                                         | search_query: str (input named 'search_query')                    |
| /article/<int:article_id>     | article_details        | GET         | article_details.html   | article: dict (article_id:int, title:str, author:str, date:str, content:str), is_bookmarked: bool                                                                                | None                                                             |
| /article/<int:article_id>/bookmark | bookmark_article    | POST        | N/A (redirect back)    | None                                                                                                                                                                              | No form data; triggers bookmarking of article_id                 |
| /bookmarks                  | bookmarks              | GET         | bookmarks.html         | bookmarks: list of dict (bookmark_id:int, article_id:int, article_title:str, bookmarked_date:str)                                                                                | None                                                             |
| /bookmark/<int:bookmark_id>/remove | remove_bookmark      | POST        | N/A (redirect back)    | None                                                                                                                                                                              | No form data; triggers removal of bookmark with bookmark_id     |
| /comment                    | comments               | GET         | comments.html          | comments: list of dict (comment_id:int, article_id:int, article_title:str, commenter_name:str, comment_text:str, comment_date:str), articles: list of dict (article_id:int, title:str) | None                                                             |
| /comment/write              | write_comment          | GET         | write_comment.html     | articles: list of dict (article_id:int, title:str)                                                                                                                                 | None                                                             |
| /comment/write              | submit_comment         | POST        | N/A (redirect to /comment) | None                                                                                                                                                                            | article_id: int (dropdown), commenter_name: str (input), comment_text: str (textarea) |
| /trending                  | trending_articles      | GET         | trending.html          | trending_articles: list of dict (article_id:int, title:str, category:str, view_count:int, rank:int), time_period: str                                                             | None                                                             |
| /trending/filter           | filter_trending        | POST        | trending.html          | trending_articles: list of dict (article_id:int, title:str, category:str, view_count:int, rank:int), time_period: str                                                             | time_period: str (dropdown selection)                            |
| /category/<category_name>    | category_articles      | GET         | category.html          | category_name: str, articles: list of dict (article_id:int, title:str, date:str, popularity:int)                                                                                   | None                                                             |
| /category/<category_name>/sort | sort_category_articles | POST        | category.html          | category_name: str, sort_by: str ("date" or "popularity"), articles: list of dict (article_id:int, title:str, date:str, popularity:int)                                      | sort_by: str (indicating sort button clicked)                    |

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- File: templates/dashboard.html
- Page title (for <title> and <h1>): News Portal
- Elements:
  - ID: dashboard-page (Div): Container for dashboard page
  - ID: featured-articles (Div): Display of featured articles
  - ID: browse-articles-button (Button): Navigates to Article Catalog page
  - ID: view-bookmarks-button (Button): Navigates to Bookmarks page
  - ID: trending-articles-button (Button): Navigates to Trending Articles page
- Context variables:
  - featured_articles: list of dict (article_id:int, title:str, author:str, date:str, excerpt:str)
- Navigation mappings:
  - browse-articles-button: url_for('article_catalog')
  - view-bookmarks-button: url_for('bookmarks')
  - trending-articles-button: url_for('trending_articles')

### 2. Article Catalog Page
- File: templates/article_catalog.html
- Page title (for <title> and <h1>): Article Catalog
- Elements:
  - ID: catalog-page (Div): Container for article catalog page
  - ID: search-input (Input): Input for searching articles
  - ID: category-filter (Dropdown): Dropdown to filter articles by category
  - ID: articles-grid (Div): Grid displaying article cards
  - ID pattern: view-article-button-{article_id} (Button): Button to view article details for each article
- Context variables:
  - articles: list of dict (article_id:int, title:str, author:str, date:str, category:str, thumbnail_url:str)
  - categories: list of dict (category_id:int, category_name:str)
- Navigation mappings:
  - view-article-button-{article_id}: url_for('article_details', article_id=article_id)

### 3. Article Details Page
- File: templates/article_details.html
- Page title (for <title> and <h1>): Article Details
- Elements:
  - ID: article-details-page (Div): Container for article details
  - ID: article-title (H1): Displays article title
  - ID: article-author (Div): Displays article author
  - ID: article-date (Div): Displays publication date
  - ID: bookmark-button (Button): Button to bookmark article
  - ID: article-content (Div): Displays full article content
- Context variables:
  - article: dict (article_id:int, title:str, author:str, date:str, content:str)
  - is_bookmarked: bool
- Navigation mappings:
  - bookmark-button: form POST to url_for('bookmark_article', article_id=article.article_id)

### 4. Bookmarks Page
- File: templates/bookmarks.html
- Page title (for <title> and <h1>): My Bookmarks
- Elements:
  - ID: bookmarks-page (Div): Container for bookmarks page
  - ID: bookmarks-list (Div): List of bookmarked articles
  - ID pattern: remove-bookmark-button-{bookmark_id} (Button): Button to remove bookmark
  - ID pattern: read-bookmark-button-{bookmark_id} (Button): Button to read bookmarked article
  - ID: back-to-dashboard (Button): Navigates back to dashboard
- Context variables:
  - bookmarks: list of dict (bookmark_id:int, article_id:int, article_title:str, bookmarked_date:str)
- Navigation mappings:
  - remove-bookmark-button-{bookmark_id}: form POST to url_for('remove_bookmark', bookmark_id=bookmark_id)
  - read-bookmark-button-{bookmark_id}: url_for('article_details', article_id=article_id)
  - back-to-dashboard: url_for('dashboard')

### 5. Comments Page
- File: templates/comments.html
- Page title (for <title> and <h1>): Article Comments
- Elements:
  - ID: comments-page (Div): Container for comments page
  - ID: comments-list (Div): List of comments
  - ID: write-comment-button (Button): Navigate to write comment page
  - ID: filter-by-article (Dropdown): Dropdown to filter comments by article
  - ID: back-to-dashboard (Button): Navigate back to dashboard
- Context variables:
  - comments: list of dict (comment_id:int, article_id:int, article_title:str, commenter_name:str, comment_text:str, comment_date:str)
  - articles: list of dict (article_id:int, title:str)
- Navigation mappings:
  - write-comment-button: url_for('write_comment')
  - back-to-dashboard: url_for('dashboard')

### 6. Write Comment Page
- File: templates/write_comment.html
- Page title (for <title> and <h1>): Write a Comment
- Elements:
  - ID: write-comment-page (Div): Container for write comment page
  - ID: select-article (Dropdown): Dropdown to select article
  - ID: commenter-name (Input): Input for commenter name
  - ID: comment-text (Textarea): Textarea for comment text
  - ID: submit-comment-button (Button): Submit comment
- Context variables:
  - articles: list of dict (article_id:int, title:str)
- Navigation mappings:
  - form POST to url_for('submit_comment')

### 7. Trending Articles Page
- File: templates/trending.html
- Page title (for <title> and <h1>): Trending Articles
- Elements:
  - ID: trending-page (Div): Container for trending articles page
  - ID: trending-list (Div): Ranked list of trending articles
  - ID: time-period-filter (Dropdown): Dropdown to filter trending by time period
  - ID pattern: view-article-button-{article_id} (Button): Button to view article details
  - ID: back-to-dashboard (Button): Navigate back to dashboard
- Context variables:
  - trending_articles: list of dict (article_id:int, title:str, category:str, view_count:int, rank:int)
  - time_period: str
- Navigation mappings:
  - view-article-button-{article_id}: url_for('article_details', article_id=article_id)
  - back-to-dashboard: url_for('dashboard')

### 8. Category Page
- File: templates/category.html
- Page title (for <title> and <h1>): Category Articles
- Elements:
  - ID: category-page (Div): Container for category page
  - ID: category-title (H1): Displays category name
  - ID: category-articles (Div): List of articles in category
  - ID: sort-by-date (Button): Button to sort articles by date
  - ID: sort-by-popularity (Button): Button to sort articles by popularity
  - ID: back-to-dashboard (Button): Navigate back to dashboard
- Context variables:
  - category_name: str
  - articles: list of dict (article_id:int, title:str, date:str, popularity:int)
- Navigation mappings:
  - sort-by-date: form POST to url_for('sort_category_articles', category_name=category_name) with sort_by='date'
  - sort-by-popularity: form POST to url_for('sort_category_articles', category_name=category_name) with sort_by='popularity'
  - back-to-dashboard: url_for('dashboard')

### 9. Search Results Page
- File: templates/search_results.html
- Page title (for <title> and <h1>): Search Results
- Elements:
  - ID: search-results-page (Div): Container for search results
  - ID: search-query-display (Div): Displays the search query
  - ID: results-list (Div): List of search results
  - ID: no-results-message (Div): Message shown if no results found
  - ID: back-to-dashboard (Button): Navigate back to dashboard
- Context variables:
  - query: str
  - results: list of dict (article_id:int, title:str, excerpt:str)
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. Articles Data
- File path: data/articles.txt
- Format: Pipe-delimited (|)
- Fields (in order):
  1. article_id (int)
  2. title (str)
  3. author (str)
  4. category (str)
  5. content (str)
  6. date (str, YYYY-MM-DD)
  7. views (int)
- Description: Stores all news articles with details
- Example data rows:
  ```
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891
  ```

### 2. Categories Data
- File path: data/categories.txt
- Format: Pipe-delimited (|)
- Fields (in order):
  1. category_id (int)
  2. category_name (str)
  3. description (str)
- Description: Stores categories for news articles
- Example data rows:
  ```
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news
  ```

### 3. Bookmarks Data
- File path: data/bookmarks.txt
- Format: Pipe-delimited (|)
- Fields (in order):
  1. bookmark_id (int)
  2. article_id (int)
  3. article_title (str)
  4. bookmarked_date (str, YYYY-MM-DD)
- Description: Stores bookmarked articles
- Example data rows:
  ```
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18
  ```

### 4. Comments Data
- File path: data/comments.txt
- Format: Pipe-delimited (|)
- Fields (in order):
  1. comment_id (int)
  2. article_id (int)
  3. article_title (str)
  4. commenter_name (str)
  5. comment_text (str)
  6. comment_date (str, YYYY-MM-DD)
- Description: Stores comments made on articles
- Example data rows:
  ```
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19
  ```

### 5. Trending Data
- File path: data/trending.txt
- Format: Pipe-delimited (|)
- Fields (in order):
  1. article_id (int)
  2. article_title (str)
  3. category (str)
  4. view_count (int)
  5. period (str) # Example values: Today, This Week, This Month
- Description: Stores trending articles data ranked by views and period
- Example data rows:
  ```
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month
  ```

---

*End of Design Specification Document*