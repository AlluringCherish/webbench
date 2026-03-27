# NewsPortal Application Design Specification

---

## 1. Flask Routes Specification

| Route Path                  | Function Name            | HTTP Method(s) | Template File               | Context Variables (name: type)                                             | Form Data (POST only)                        |
|-----------------------------|--------------------------|----------------|-----------------------------|----------------------------------------------------------------------------|----------------------------------------------|
| /                           | redirect_to_dashboard    | GET            | None (Redirect)              | None                                                                       | None                                         |
| /dashboard                  | dashboard                | GET            | dashboard.html              | featured_articles: list[dict], trending_articles: list[dict]               | None                                         |
| /catalog                    | article_catalog          | GET            | catalog.html                | articles: list[dict], categories: list[dict], selected_category: str or None, search_query: str or None | None                                   |
| /articles/<int:article_id>  | article_details          | GET            | article_details.html        | article: dict, bookmarked: bool                                             | None                                         |
| /articles/<int:article_id>/bookmark | bookmark_article   | POST           | None (Redirect back to article details) | None                                                              | None (bookmark action triggered by POST)     |
| /bookmarks                  | bookmarks                | GET            | bookmarks.html              | bookmarks: list[dict]                                                      | None                                         |
| /bookmarks/<int:bookmark_id>/remove | remove_bookmark     | POST           | None (Redirect back to bookmarks)       | None                                                              | None (remove action triggered by POST)       |
| /comments                   | comments                 | GET            | comments.html               | comments: list[dict], articles: list[dict], selected_article_id: int or None | None                                   |
| /comments/write             | write_comment            | GET            | write_comment.html          | articles: list[dict]                                                      | None                                         |
| /comments/write             | submit_comment           | POST           | None (Redirect to comments) | None                                                                       | article_id: int, commenter_name: str, comment_text: str |
| /trending                  | trending_articles        | GET            | trending.html               | trending_articles: list[dict], time_period: str or None                   | None                                         |
| /category/<string:category_name> | category_articles    | GET            | category.html               | category_name: str, articles: list[dict]                                  | None                                         |
| /search                    | search_results           | GET            | search_results.html         | query: str, results: list[dict]                                            | None                                         |

---

## 2. HTML Template Specifications

### Dashboard Page (templates/dashboard.html)
- Page Title: News Portal
- Heading (<h1>): News Portal
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page.
  - featured-articles (Div): Display area for featured article recommendations.
  - browse-articles-button (Button): Navigates to article catalog page.
  - view-bookmarks-button (Button): Navigates to bookmarks page.
  - trending-articles-button (Button): Navigates to trending articles page.
- Context Variables:
  - featured_articles: list of dict with keys: article_id:int, title:str, author:str, date:str
  - trending_articles: list of dict with keys: article_id:int, title:str, category:str, views:int
- Navigation Mappings:
  - browse-articles-button: url_for('article_catalog')
  - view-bookmarks-button: url_for('bookmarks')
  - trending-articles-button: url_for('trending_articles')

### Article Catalog Page (templates/catalog.html)
- Page Title: Article Catalog
- Heading (<h1>): Article Catalog
- Element IDs:
  - catalog-page (Div): Container for the catalog page.
  - search-input (Input): Search field to filter articles.
  - category-filter (Dropdown): Dropdown to select category for filtering.
  - articles-grid (Div): Container displaying article cards.
  - view-article-button-{article_id} (Button): Button on each article card to view details.
- Context Variables:
  - articles: list of dict with keys: article_id:int, title:str, author:str, date:str, category:str
  - categories: list of dict with keys: category_id:int, category_name:str
  - selected_category: str or None
  - search_query: str or None
- Navigation Mappings:
  - view-article-button-{article_id}: url_for('article_details', article_id=article.article_id)

### Article Details Page (templates/article_details.html)
- Page Title: Article Details
- Heading (<h1>): Article Details (actual article title is displayed in element with id "article-title")
- Element IDs:
  - article-details-page (Div): Container for the article details page.
  - article-title (H1): Displays the article's title.
  - article-author (Div): Displays article author.
  - article-date (Div): Displays publication date.
  - bookmark-button (Button): Button to bookmark the article.
  - article-content (Div): Full article content display.
- Context Variables:
  - article: dict with fields: article_id:int, title:str, author:str, category:str, content:str, date:str, views:int
  - bookmarked: bool indicating if the article is bookmarked
- Navigation Mappings:
  - bookmark-button: form POST to url_for('bookmark_article', article_id=article.article_id)

### Bookmarks Page (templates/bookmarks.html)
- Page Title: My Bookmarks
- Heading (<h1>): My Bookmarks
- Element IDs:
  - bookmarks-page (Div): Container for bookmarks page.
  - bookmarks-list (Div): List showing bookmarks with title and date.
  - remove-bookmark-button-{bookmark_id} (Button): Remove bookmark button per bookmark.
  - read-bookmark-button-{bookmark_id} (Button): Read bookmarked article button per bookmark.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Context Variables:
  - bookmarks: list of dict with keys: bookmark_id:int, article_id:int, article_title:str, bookmarked_date:str
- Navigation Mappings:
  - remove-bookmark-button-{bookmark_id}: form POST to url_for('remove_bookmark', bookmark_id=bookmark.bookmark_id)
  - read-bookmark-button-{bookmark_id}: url_for('article_details', article_id=bookmark.article_id)
  - back-to-dashboard: url_for('dashboard')

### Comments Page (templates/comments.html)
- Page Title: Article Comments
- Heading (<h1>): Article Comments
- Element IDs:
  - comments-page (Div): Container for comments page.
  - comments-list (Div): List of all comments with article title, commenter name, and comment text.
  - write-comment-button (Button): Navigates to write comment page.
  - filter-by-article (Dropdown): Dropdown to filter comments by article.
  - back-to-dashboard (Button): Navigates back to dashboard.
- Context Variables:
  - comments: list of dict with keys: comment_id:int, article_id:int, article_title:str, commenter_name:str, comment_text:str, comment_date:str
  - articles: list of dict with keys: article_id:int, title:str
  - selected_article_id: int or None
- Navigation Mappings:
  - write-comment-button: url_for('write_comment')
  - back-to-dashboard: url_for('dashboard')

### Write Comment Page (templates/write_comment.html)
- Page Title: Write a Comment
- Heading (<h1>): Write a Comment
- Element IDs:
  - write-comment-page (Div): Container for the write comment page.
  - select-article (Dropdown): Select article to comment on.
  - commenter-name (Input): Input for commenter's name.
  - comment-text (Textarea): Textarea for comment content.
  - submit-comment-button (Button): Submit comment.
- Context Variables:
  - articles: list of dict with keys: article_id:int, title:str
- Navigation Mappings:
  - submit-comment-button: form POST to url_for('submit_comment')

### Trending Articles Page (templates/trending.html)
- Page Title: Trending Articles
- Heading (<h1>): Trending Articles
- Element IDs:
  - trending-page (Div): Container for the trending articles page.
  - trending-list (Div): Ranked list of trending articles.
  - time-period-filter (Dropdown): Dropdown to filter by time period.
  - view-article-button-{article_id} (Button): Button on each trending article to view details.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Context Variables:
  - trending_articles: list of dict with keys: article_id:int, article_title:str, category:str, view_count:int, period:str
  - time_period: str or None
- Navigation Mappings:
  - view-article-button-{article_id}: url_for('article_details', article_id=article.article_id)
  - back-to-dashboard: url_for('dashboard')

### Category Page (templates/category.html)
- Page Title: Category Articles
- Heading (<h1>): Category Articles
- Element IDs:
  - category-page (Div): Container for the category page.
  - category-title (H1): Displays the category name.
  - category-articles (Div): List of articles in the selected category.
  - sort-by-date (Button): Sort articles by date.
  - sort-by-popularity (Button): Sort articles by popularity.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Context Variables:
  - category_name: str
  - articles: list of dict with keys: article_id:int, title:str, author:str, date:str, views:int
- Navigation Mappings:
  - sort-by-date: url_for('category_articles', category_name=category_name) with query param sort='date'
  - sort-by-popularity: url_for('category_articles', category_name=category_name) with query param sort='popularity'
  - back-to-dashboard: url_for('dashboard')

### Search Results Page (templates/search_results.html)
- Page Title: Search Results
- Heading (<h1>): Search Results
- Element IDs:
  - search-results-page (Div): Container for search results page.
  - search-query-display (Div): Displays the search query performed.
  - results-list (Div): List of matched search result articles.
  - no-results-message (Div): Message shown when no results found.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Context Variables:
  - query: str
  - results: list of dict with keys: article_id:int, title:str, excerpt:str
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')

---

## 3. Data File Schemas

### 1. Articles Data (data/articles.txt)
- Fields (pipe-delimited):
  1. article_id (int)
  2. title (str)
  3. author (str)
  4. category (str)
  5. content (str)
  6. date (str, format YYYY-MM-DD)
  7. views (int)
- Description: Stores all news articles with their metadata.
- Example Data:
  ```
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891
  ```

### 2. Categories Data (data/categories.txt)
- Fields (pipe-delimited):
  1. category_id (int)
  2. category_name (str)
  3. description (str)
- Description: Stores category metadata.
- Example Data:
  ```
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news
  ```

### 3. Bookmarks Data (data/bookmarks.txt)
- Fields (pipe-delimited):
  1. bookmark_id (int)
  2. article_id (int)
  3. article_title (str)
  4. bookmarked_date (str, format YYYY-MM-DD)
- Description: Stores users' bookmarked articles.
- Example Data:
  ```
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18
  ```

### 4. Comments Data (data/comments.txt)
- Fields (pipe-delimited):
  1. comment_id (int)
  2. article_id (int)
  3. article_title (str)
  4. commenter_name (str)
  5. comment_text (str)
  6. comment_date (str, format YYYY-MM-DD)
- Description: Stores comments made on articles.
- Example Data:
  ```
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19
  ```

### 5. Trending Data (data/trending.txt)
- Fields (pipe-delimited):
  1. article_id (int)
  2. article_title (str)
  3. category (str)
  4. view_count (int)
  5. period (str) - values like 'Today', 'This Week', 'This Month'
- Description: Stores trending article data by time period.
- Example Data:
  ```
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month
  ```

---

# End of NewsPortal Design Specification
