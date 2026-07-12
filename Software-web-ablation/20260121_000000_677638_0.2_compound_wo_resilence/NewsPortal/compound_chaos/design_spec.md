# NewsPortal Design Specification

## Section 1: Flask Routes Specification

| Route Path | Flask Function Name | HTTP Method | Template | Context Variables | Form Data (POST) |
|------------|---------------------|-------------|----------|-------------------|------------------|
| / | root_redirect | GET | N/A (redirect) | None | None |
| /dashboard | dashboard | GET | dashboard.html | featured_articles (list of dict), trending_articles (list of dict) | None |
| /catalog | article_catalog | GET | article_catalog.html | articles (list of dict), categories (list of dict), search_query (str or None), selected_category (str or None) | None |
| /article/<int:article_id> | article_details | GET | article_details.html | article (dict), is_bookmarked (bool) | None |
| /article/<int:article_id>/bookmark | bookmark_article | POST | N/A (redirect) | None | None (form submission via bookmark button) |
| /bookmarks | bookmarks | GET | bookmarks.html | bookmarks (list of dict) | None |
| /bookmarks/<int:bookmark_id>/remove | remove_bookmark | POST | N/A (redirect) | None | None (form submission from remove button) |
| /comments | comments_page | GET | comments.html | comments (list of dict), articles (list of dict), selected_article_id (int or None) | None |
| /comments/write | write_comment | GET | write_comment.html | articles (list of dict) | None |
| /comments/write/submit | submit_comment | POST | N/A (redirect) | None | article_id (int), commenter_name (str), comment_text (str) |
| /trending | trending_articles | GET | trending.html | trending_list (list of dict), time_period (str) | None |
| /category/<string:category_name> | category_articles | GET | category.html | category_name (str), articles (list of dict) | None |
| /search | search_results | GET | search_results.html | search_query (str), results (list of dict) | None |

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- File Path: templates/dashboard.html
- Page Title: News Portal
- HTML Title Tag: <title>News Portal</title>
- H1 Tag: <h1>News Portal</h1>
- Element IDs and Descriptions:
  - dashboard-page (Div): Container for the dashboard page.
  - featured-articles (Div): Display container for featured article recommendations.
  - browse-articles-button (Button): Navigates to article catalog page.
  - view-bookmarks-button (Button): Navigates to bookmarks page.
  - trending-articles-button (Button): Navigates to trending articles page.
- Context Variables:
  - featured_articles (list of dict): Each dict having keys: article_id (int), title (str), author (str), date (str), excerpt (str).
  - trending_articles (list of dict): Each dict having keys: article_id (int), title (str), category (str), view_count (int).
- Navigation Mappings:
  - browse-articles-button: href or onclick -> url_for('article_catalog')
  - view-bookmarks-button: href or onclick -> url_for('bookmarks')
  - trending-articles-button: href or onclick -> url_for('trending_articles')

---

### 2. Article Catalog Page
- File Path: templates/article_catalog.html
- Page Title: Article Catalog
- HTML Title Tag: <title>Article Catalog</title>
- H1 Tag: <h1>Article Catalog</h1>
- Element IDs and Descriptions:
  - catalog-page (Div): Container for the catalog page.
  - search-input (Input): Input field for searching articles by title, author, or keywords.
  - category-filter (Dropdown): Dropdown for filtering by category.
  - articles-grid (Div): Grid displaying article cards.
  - view-article-button-{article_id} (Button): Button to view article details for each article.
- Context Variables:
  - articles (list of dict): Each dict has article_id (int), title (str), author (str), date (str), thumbnail_url (optional str).
  - categories (list of dict): Each dict has category_id (int), category_name (str).
  - search_query (str or None): Search keyword.
  - selected_category (str or None): Selected category name.
- Navigation Mappings:
  - view-article-button-{article_id}: url_for('article_details', article_id=article_id)

---

### 3. Article Details Page
- File Path: templates/article_details.html
- Page Title: Article Details
- HTML Title Tag: <title>Article Details</title>
- H1 Tag: <h1 id="article-title">{{ article.title }}</h1>
- Element IDs and Descriptions:
  - article-details-page (Div): Container for the article details page.
  - article-title (H1): Displays article title.
  - article-author (Div): Displays article author.
  - article-date (Div): Displays article publication date.
  - bookmark-button (Button): Button to bookmark the article.
  - article-content (Div): Displays full article content.
- Context Variables:
  - article (dict): Fields include article_id (int), title (str), author (str), category (str), content (str), date (str), views (int).
  - is_bookmarked (bool): Whether the article is bookmarked.
- Navigation Mappings:
  - bookmark-button: POST action to url_for('bookmark_article', article_id=article.article_id)

---

### 4. Bookmarks Page
- File Path: templates/bookmarks.html
- Page Title: My Bookmarks
- HTML Title Tag: <title>My Bookmarks</title>
- H1 Tag: <h1>My Bookmarks</h1>
- Element IDs and Descriptions:
  - bookmarks-page (Div): Container for the bookmarks page.
  - bookmarks-list (Div): List of bookmarked articles with title and date.
  - remove-bookmark-button-{bookmark_id} (Button): Button to remove a bookmark.
  - read-bookmark-button-{bookmark_id} (Button): Button to read bookmarked article.
  - back-to-dashboard (Button): Button to navigate back to dashboard.
- Context Variables:
  - bookmarks (list of dict): Each dict with bookmark_id (int), article_id (int), article_title (str), bookmarked_date (str).
- Navigation Mappings:
  - remove-bookmark-button-{bookmark_id}: POST to url_for('remove_bookmark', bookmark_id=bookmark_id)
  - read-bookmark-button-{bookmark_id}: url_for('article_details', article_id=article_id)
  - back-to-dashboard: url_for('dashboard')

---

### 5. Comments Page
- File Path: templates/comments.html
- Page Title: Article Comments
- HTML Title Tag: <title>Article Comments</title>
- H1 Tag: <h1>Article Comments</h1>
- Element IDs and Descriptions:
  - comments-page (Div): Container for comments page.
  - comments-list (Div): Display of comments (article title, commenter name, comment text).
  - write-comment-button (Button): Navigates to write comment page.
  - filter-by-article (Dropdown): Dropdown to filter comments by article.
  - back-to-dashboard (Button): Button to return to dashboard.
- Context Variables:
  - comments (list of dict): Each dict with comment_id (int), article_id (int), article_title (str), commenter_name (str), comment_text (str), comment_date (str).
  - articles (list of dict): For filter dropdown, each dict with article_id (int), title (str).
  - selected_article_id (int or None): Currently selected article filter.
- Navigation Mappings:
  - write-comment-button: url_for('write_comment')
  - back-to-dashboard: url_for('dashboard')

---

### 6. Write Comment Page
- File Path: templates/write_comment.html
- Page Title: Write a Comment
- HTML Title Tag: <title>Write a Comment</title>
- H1 Tag: <h1>Write a Comment</h1>
- Element IDs and Descriptions:
  - write-comment-page (Div): Container for write comment page.
  - select-article (Dropdown): Dropdown to select article to comment on.
  - commenter-name (Input): Input field for commenter name.
  - comment-text (Textarea): Textarea for comment content.
  - submit-comment-button (Button): Button to submit comment.
- Context Variables:
  - articles (list of dict): Each dict with article_id (int), title (str).
- Navigation Mappings:
  - submit-comment-button: POST to url_for('submit_comment')

---

### 7. Trending Articles Page
- File Path: templates/trending.html
- Page Title: Trending Articles
- HTML Title Tag: <title>Trending Articles</title>
- H1 Tag: <h1>Trending Articles</h1>
- Element IDs and Descriptions:
  - trending-page (Div): Container for trending articles page.
  - trending-list (Div): Ranked list of trending articles (rank, title, category, view count).
  - time-period-filter (Dropdown): Filter trending articles by time period.
  - view-article-button-{article_id} (Button): Button to view article details.
  - back-to-dashboard (Button): Button to return to dashboard.
- Context Variables:
  - trending_list (list of dict): Each dict with article_id (int), article_title (str), category (str), view_count (int), period (str).
  - time_period (str): Current filter selection.
- Navigation Mappings:
  - view-article-button-{article_id}: url_for('article_details', article_id=article_id)
  - back-to-dashboard: url_for('dashboard')

---

### 8. Category Page
- File Path: templates/category.html
- Page Title: Category Articles
- HTML Title Tag: <title>Category Articles</title>
- H1 Tag: <h1 id="category-title">{{ category_name }}</h1>
- Element IDs and Descriptions:
  - category-page (Div): Container for category page.
  - category-title (H1): Display the category name.
  - category-articles (Div): List of articles in selected category.
  - sort-by-date (Button): Button to sort articles by date.
  - sort-by-popularity (Button): Button to sort articles by popularity.
  - back-to-dashboard (Button): Button to return to dashboard.
- Context Variables:
  - category_name (str): The selected category name.
  - articles (list of dict): Each dict with article_id (int), title (str), author (str), date (str), views (int).
- Navigation Mappings:
  - sort-by-date: triggers sorting by date (can be GET with query param or JS event)
  - sort-by-popularity: triggers sorting by popularity
  - back-to-dashboard: url_for('dashboard')

---

### 9. Search Results Page
- File Path: templates/search_results.html
- Page Title: Search Results
- HTML Title Tag: <title>Search Results</title>
- H1 Tag: <h1>Search Results</h1>
- Element IDs and Descriptions:
  - search-results-page (Div): Container for search results page.
  - search-query-display (Div): Displays the search query term.
  - results-list (Div): List of articles matching search.
  - no-results-message (Div): Message displayed if no results found.
  - back-to-dashboard (Button): Button to return to dashboard.
- Context Variables:
  - search_query (str): The search query string.
  - results (list of dict): Each dict with article_id (int), title (str), excerpt (str).
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. Articles Data
- File Path: data/articles.txt
- Format: Pipe-delimited (|)
- Fields (in exact order):
  1. article_id (int)
  2. title (str)
  3. author (str)
  4. category (str)
  5. content (str)
  6. date (str, YYYY-MM-DD)
  7. views (int)
- Description: Stores all news articles with metadata and full content.
- Example Rows:
  ```
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891
  ```

---

### 2. Categories Data
- File Path: data/categories.txt
- Format: Pipe-delimited (|)
- Fields (in exact order):
  1. category_id (int)
  2. category_name (str)
  3. description (str)
- Description: Categories available for articles with brief descriptions.
- Example Rows:
  ```
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news
  ```

---

### 3. Bookmarks Data
- File Path: data/bookmarks.txt
- Format: Pipe-delimited (|)
- Fields (in exact order):
  1. bookmark_id (int)
  2. article_id (int)
  3. article_title (str)
  4. bookmarked_date (str, YYYY-MM-DD)
- Description: Stores user bookmarked articles with timestamp.
- Example Rows:
  ```
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18
  ```

---

### 4. Comments Data
- File Path: data/comments.txt
- Format: Pipe-delimited (|)
- Fields (in exact order):
  1. comment_id (int)
  2. article_id (int)
  3. article_title (str)
  4. commenter_name (str)
  5. comment_text (str)
  6. comment_date (str, YYYY-MM-DD)
- Description: Stores all comments made by users on articles.
- Example Rows:
  ```
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19
  ```

---

### 5. Trending Data
- File Path: data/trending.txt
- Format: Pipe-delimited (|)
- Fields (in exact order):
  1. article_id (int)
  2. article_title (str)
  3. category (str)
  4. view_count (int)
  5. period (str - e.g., "Today", "This Week", "This Month")
- Description: Stores trending articles ranked by views within a specified period.
- Example Rows:
  ```
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month
  ```
