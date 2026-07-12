# NewsPortal Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                | Flask Function Name      | HTTP Method | Template Rendered       | Context Variables (name: type)                                  | Form Data on POST               |
|---------------------------|-------------------------|-------------|------------------------|-----------------------------------------------------------------|--------------------------------|
| `/`                       | root_redirect            | GET         | None (redirect)         | None                                                            | None                           |
| `/dashboard`              | dashboard_page          | GET         | dashboard.html          | featured_articles: list(dict), e.g., [{"article_id": int, "title": str, "author": str, "date": str}],  
                                                trending_articles: list(dict) [{"article_id": int, "title": str, "category": str, "view_count": int}],  
                                                categories: list(dict) [{"category_id": int, "category_name": str}]                  | None                           |
| `/catalog`                | article_catalog_page    | GET         | catalog.html            | articles: list(dict) [{"article_id": int, "title": str, "author": str, "date": str, "category": str, "thumbnail_url": str}],  
                                                categories: list(dict) [{"category_id": int, "category_name": str}]                                         | None                           |
| `/catalog`                | article_catalog_search  | POST        | catalog.html            | articles: list(dict) filtered and searched same as GET,  
                                                categories: list(dict)                                          | search_query: str, filter_category: str (optional) |
| `/article/<int:article_id>`| article_details_page     | GET         | article_details.html    | article: dict {"article_id": int, "title": str, "author": str, "category": str, "content": str, "date": str, "views": int},  
                                              bookmarked: bool                                               | None                           |
| `/article/<int:article_id>/bookmark` | bookmark_article      | POST        | None (redirect to article details) | None                                                            | None (But implicitly bookmarks the article)  |
| `/bookmarks`              | bookmarks_page          | GET         | bookmarks.html          | bookmarks: list(dict) [{"bookmark_id": int, "article_id": int, "article_title": str, "bookmarked_date": str}]               | None                           |
| `/bookmarks/<int:bookmark_id>/remove` | remove_bookmark        | POST        | None (redirect to bookmarks) | None                                                            | None                           |
| `/comments`               | comments_page           | GET         | comments.html           | comments: list(dict) [{"comment_id": int, "article_id": int, "article_title": str, "commenter_name": str, "comment_text": str, "comment_date": str}],  
                                              articles: list(dict) [{"article_id": int, "title": str}]                     | None                           |
| `/comments/filter`        | filter_comments         | POST        | comments.html           | comments: list(dict) filtered,  
                                              articles: list(dict)                                         | article_id: int (optional)     |
| `/comments/write`         | write_comment_page      | GET         | write_comment.html      | articles: list(dict) [{"article_id": int, "title": str}]                                                     | None                           |
| `/comments/write`         | submit_comment          | POST        | None (redirect to comments page) | None                                                            | article_id: int, commenter_name: str, comment_text: str |
| `/trending`               | trending_articles_page  | GET         | trending.html           | trending_articles: list(dict) [{"article_id": int, "article_title": str, "category": str, "view_count": int}],  
                                              time_periods: list(str) ["Today", "This Week", "This Month"]                       | None                           |
| `/trending/filter`        | filter_trending         | POST        | trending.html           | trending_articles: list(dict) filtered,  
                                              time_periods: list(str)                                         | time_period: str               |
| `/category/<string:category_name>` | category_page          | GET         | category.html           | category_name: str,  
                                              articles: list(dict) [{"article_id": int, "title": str, "date": str, "category": str, "views": int}],  | None                           |
| `/category/<string:category_name>/sort` | sort_category_articles  | POST        | category.html           | category_name: str,  
                                              articles: list(dict) sorted,  
                                              sort_method: str ["date" or "popularity"]                                           | sort_method: str               |
| `/search`                 | search_results_page     | GET         | search_results.html     | query: str,  
                                              results: list(dict) [{"article_id": int, "title": str, "excerpt": str}]                           | None                           |

---

## Section 2: HTML Template Specifications

### 1. Template: templates/dashboard.html
- Page Title: News Portal
- <h1> Title: News Portal
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page
  - featured-articles (Div): Display of featured article recommendations list
  - browse-articles-button (Button): Button to navigate to article catalog page
  - view-bookmarks-button (Button): Button to navigate to bookmarks page
  - trending-articles-button (Button): Button to navigate to trending articles page
- Context Variables:
  - featured_articles: list of dicts with keys ["article_id": int, "title": str, "author": str, "date": str]
  - trending_articles: list of dicts with keys ["article_id": int, "title": str, "category": str, "view_count": int]
  - categories: list of dicts with keys ["category_id": int, "category_name": str]
- Navigation Mappings:
  - browse-articles-button -> url_for('article_catalog_page')
  - view-bookmarks-button -> url_for('bookmarks_page')
  - trending-articles-button -> url_for('trending_articles_page')

---

### 2. Template: templates/catalog.html
- Page Title: Article Catalog
- <h1> Title: Article Catalog
- Element IDs:
  - catalog-page (Div): Container for the catalog page
  - search-input (Input): Field to search articles by title, author, or keywords
  - category-filter (Dropdown): Dropdown to filter by category
  - articles-grid (Div): Grid to display article cards
  - view-article-button-{article_id} (Button): Button on each article card to view details
- Context Variables:
  - articles: list of dicts with keys ["article_id": int, "title": str, "author": str, "date": str, "category": str, "thumbnail_url": str]
  - categories: list of dicts with keys ["category_id": int, "category_name": str]
- Navigation Mappings:
  - view-article-button-{article_id} -> url_for('article_details_page', article_id=article_id)

---

### 3. Template: templates/article_details.html
- Page Title: Article Details
- <h1> Title (ID = article-title): Article title from context
- Element IDs:
  - article-details-page (Div): Container for article details page
  - article-title (H1): Article title
  - article-author (Div): Article author
  - article-date (Div): Article publication date
  - bookmark-button (Button): Button to bookmark the article
  - article-content (Div): Full article content
- Context Variables:
  - article: dict with keys ["article_id": int, "title": str, "author": str, "category": str, "content": str, "date": str, "views": int]
  - bookmarked: bool indicating if article is bookmarked
- Navigation Mappings:
  - bookmark-button -> POST to url_for('bookmark_article', article_id=article.article_id)

---

### 4. Template: templates/bookmarks.html
- Page Title: My Bookmarks
- <h1> Title: My Bookmarks
- Element IDs:
  - bookmarks-page (Div): Container for bookmarks page
  - bookmarks-list (Div): List of bookmarked articles
  - remove-bookmark-button-{bookmark_id} (Button): Button to remove bookmark
  - read-bookmark-button-{bookmark_id} (Button): Button to read bookmarked article
  - back-to-dashboard (Button): Button to navigate back to dashboard
- Context Variables:
  - bookmarks: list of dicts with keys ["bookmark_id": int, "article_id": int, "article_title": str, "bookmarked_date": str]
- Navigation Mappings:
  - remove-bookmark-button-{bookmark_id} -> POST to url_for('remove_bookmark', bookmark_id=bookmark_id)
  - read-bookmark-button-{bookmark_id} -> url_for('article_details_page', article_id=article_id)
  - back-to-dashboard -> url_for('dashboard_page')

---

### 5. Template: templates/comments.html
- Page Title: Article Comments
- <h1> Title: Article Comments
- Element IDs:
  - comments-page (Div): Container for comments page
  - comments-list (Div): List of all comments
  - write-comment-button (Button): Button to navigate to write comment page
  - filter-by-article (Dropdown): Dropdown to filter comments by article
  - back-to-dashboard (Button): Button to navigate back to dashboard
- Context Variables:
  - comments: list of dicts with keys ["comment_id": int, "article_id": int, "article_title": str, "commenter_name": str, "comment_text": str, "comment_date": str]
  - articles: list of dicts with keys ["article_id": int, "title": str]
- Navigation Mappings:
  - write-comment-button -> url_for('write_comment_page')
  - back-to-dashboard -> url_for('dashboard_page')

---

### 6. Template: templates/write_comment.html
- Page Title: Write a Comment
- <h1> Title: Write a Comment
- Element IDs:
  - write-comment-page (Div): Container for write comment page
  - select-article (Dropdown): Dropdown to select article
  - commenter-name (Input): Input for commenter name
  - comment-text (Textarea): Textarea for comment text
  - submit-comment-button (Button): Button to submit comment
- Context Variables:
  - articles: list of dicts with keys ["article_id": int, "title": str]
- Navigation Mappings:
  - submit-comment-button -> POST form to url_for('submit_comment')

---

### 7. Template: templates/trending.html
- Page Title: Trending Articles
- <h1> Title: Trending Articles
- Element IDs:
  - trending-page (Div): Container for trending articles
  - trending-list (Div): Ranked list of trending articles
  - time-period-filter (Dropdown): Dropdown to filter time period
  - view-article-button-{article_id} (Button): Button to view article details
  - back-to-dashboard (Button): Button to go back to dashboard
- Context Variables:
  - trending_articles: list of dicts with keys ["article_id": int, "article_title": str, "category": str, "view_count": int]
  - time_periods: list of str ["Today", "This Week", "This Month"]
- Navigation Mappings:
  - view-article-button-{article_id} -> url_for('article_details_page', article_id=article_id)
  - back-to-dashboard -> url_for('dashboard_page')

---

### 8. Template: templates/category.html
- Page Title: Category Articles
- <h1> Title (ID = category-title): Category name from context
- Element IDs:
  - category-page (Div): Container for category page
  - category-title (H1): Displays category name
  - category-articles (Div): List of articles in category
  - sort-by-date (Button): Button to sort articles by date
  - sort-by-popularity (Button): Button to sort articles by popularity
  - back-to-dashboard (Button): Button to go back to dashboard
- Context Variables:
  - category_name: str
  - articles: list of dicts with keys ["article_id": int, "title": str, "date": str, "category": str, "views": int]
  - sort_method: optional str ["date" or "popularity"]
- Navigation Mappings:
  - sort-by-date -> POST form to url_for('sort_category_articles', category_name=category_name) with sort_method="date"
  - sort-by-popularity -> POST form to url_for('sort_category_articles', category_name=category_name) with sort_method="popularity"
  - back-to-dashboard -> url_for('dashboard_page')

---

### 9. Template: templates/search_results.html
- Page Title: Search Results
- <h1> Title: Search Results
- Element IDs:
  - search-results-page (Div): Container for search results page
  - search-query-display (Div): Displays the search query
  - results-list (Div): List of search results
  - no-results-message (Div): Message shown if no results found
  - back-to-dashboard (Button): Button to go back to dashboard
- Context Variables:
  - query: str
  - results: list of dicts with keys ["article_id": int, "title": str, "excerpt": str]
- Navigation Mappings:
  - back-to-dashboard -> url_for('dashboard_page')

---

## Section 3: Data File Schemas

### 1. Articles Data
- File Path: data/articles.txt
- Format: pipe-delimited (|), no header row
- Fields (in order):
  1. article_id (int)
  2. title (str)
  3. author (str)
  4. category (str)
  5. content (str)
  6. date (str: YYYY-MM-DD)
  7. views (int)
- Description: Stores news articles metadata and content
- Example Data Rows:
  ```
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891
  ```

---

### 2. Categories Data
- File Path: data/categories.txt
- Format: pipe-delimited (|), no header row
- Fields (in order):
  1. category_id (int)
  2. category_name (str)
  3. description (str)
- Description: Stores news categories with descriptions
- Example Data Rows:
  ```
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news
  ```

---

### 3. Bookmarks Data
- File Path: data/bookmarks.txt
- Format: pipe-delimited (|), no header row
- Fields (in order):
  1. bookmark_id (int)
  2. article_id (int)
  3. article_title (str)
  4. bookmarked_date (str: YYYY-MM-DD)
- Description: Stores user bookmarks of articles
- Example Data Rows:
  ```
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18
  ```

---

### 4. Comments Data
- File Path: data/comments.txt
- Format: pipe-delimited (|), no header row
- Fields (in order):
  1. comment_id (int)
  2. article_id (int)
  3. article_title (str)
  4. commenter_name (str)
  5. comment_text (str)
  6. comment_date (str: YYYY-MM-DD)
- Description: Stores comments on articles
- Example Data Rows:
  ```
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19
  ```

---

### 5. Trending Data
- File Path: data/trending.txt
- Format: pipe-delimited (|), no header row
- Fields (in order):
  1. article_id (int)
  2. article_title (str)
  3. category (str)
  4. view_count (int)
  5. period (str)
- Description: Stores trending articles and their views over periods
- Example Data Rows:
  ```
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month
  ```

---

# End of Design Spec