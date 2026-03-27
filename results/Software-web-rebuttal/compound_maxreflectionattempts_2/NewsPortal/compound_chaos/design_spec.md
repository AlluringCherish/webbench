# Design Specification for NewsPortal Web Application

---

## Section 1: Flask Routes Specification

| Route Path              | Flask Function Name      | HTTP Method(s) | Template File Rendered           | Context Variables Passed to Templates                           | Form Data in POST Routes                         |
|-------------------------|-------------------------|----------------|---------------------------------|----------------------------------------------------------------|-------------------------------------------------|
| /                       | root_redirect            | GET            | None (redirect)                  | None                                                           | None                                            |
| /dashboard              | dashboard                | GET            | dashboard.html                  | featured_articles (list of dict), trending_articles (list of dict) | None                                            |
| /catalog                | article_catalog          | GET            | article_catalog.html            | articles (list of dict), categories (list of dict), search_query (str, optional), selected_category (str, optional) | None                                            |
| /catalog/search         | catalog_search           | POST           | search_results.html             | search_query (str), results (list of dict)                     | search_query (str), category_filter (str, optional) |
| /article/<int:article_id> | article_details         | GET            | article_details.html            | article (dict), is_bookmarked (bool)                           | None                                            |
| /article/<int:article_id>/bookmark | bookmark_article    | POST           | None (redirect to article_details) | None                                                           | None (uses route param)                          |
| /bookmarks              | bookmarks                | GET            | bookmarks.html                  | bookmarks (list of dict)                                      | None                                            |
| /bookmarks/remove/<int:bookmark_id> | remove_bookmark     | POST           | None (redirect to bookmarks)    | None                                                           | None (uses route param)                          |
| /comments               | comments                 | GET            | comments.html                  | comments (list of dict), articles (list of dict), selected_article (str, optional) | None                                            |
| /comments/filter         | filter_comments          | POST           | comments.html                  | comments (list of dict), articles (list of dict), selected_article (str) | selected_article (str)                           |
| /comments/write          | write_comment_page       | GET            | write_comment.html             | articles (list of dict)                                      | None                                            |
| /comments/submit         | submit_comment           | POST           | None (redirect to comments)    | None                                                           | article_id (int), commenter_name (str), comment_text (str) |
| /trending               | trending_articles        | GET            | trending.html                  | trending_articles (list of dict), time_period (str, optional) | None                                            |
| /trending/filter         | filter_trending          | POST           | trending.html                  | trending_articles (list of dict), time_period (str)            | time_period (str)                                |
| /category/<category_name> | category_articles       | GET            | category.html                  | category_name (str), articles (list of dict)                   | None                                            |
| /category/<category_name>/sort | sort_category_articles | POST           | category.html                  | category_name (str), articles (list of dict), sort_option (str) | sort_option (str)                                |


Notes:
- The root route `/` redirects to `/dashboard`.
- POST routes are used for filtering, sorting, submitting, or modifying data.
- Context variables are structured data objects (list or dict) mirroring the data schema and requirements.
- Function names precisely reflect the purpose of the route and use lowercase_underscore style.

---

## Section 2: HTML Template Specifications

### templates/dashboard.html
- Page Title: News Portal
- Element IDs:
  - dashboard-page (Div): Main container for Dashboard page.
  - featured-articles (Div): Displays list of featured articles.
  - browse-articles-button (Button): Navigates to article catalog page.
  - view-bookmarks-button (Button): Navigates to bookmarks page.
  - trending-articles-button (Button): Navigates to trending articles page.
- Context Variables:
  - featured_articles: list of dicts (article_id:int, title:str, author:str, category:str, date:str, excerpt:str)
  - trending_articles: list of dicts (article_id:int, title:str, category:str, view_count:int)
- Navigation Mappings:
  - browse-articles-button: url_for('article_catalog')
  - view-bookmarks-button: url_for('bookmarks')
  - trending-articles-button: url_for('trending_articles')
- Jinja2 Usage:
  - Loop over featured_articles to generate article previews inside featured-articles div.
  - Loop over trending_articles to show a summarized list.


### templates/article_catalog.html
- Page Title: Article Catalog
- Element IDs:
  - catalog-page (Div): Main container.
  - search-input (Input): Text input for search queries.
  - category-filter (Dropdown): Select dropdown for article categories.
  - articles-grid (Div): Grid layout for article cards.
  - view-article-button-{{article_id}} (Button): Button for each article card to view details.
- Context Variables:
  - articles: list of dicts (article_id:int, title:str, author:str, category:str, date:str, excerpt:str)
  - categories: list of dicts (category_id:int, category_name:str)
  - search_query: str (optional)
  - selected_category: str (optional)
- Navigation Mappings:
  - view-article-button-{{article_id}}: url_for('article_details', article_id=article_id)
- Jinja2 Usage:
  - Loop over articles to create article cards.
  - Loop over categories to populate category-filter dropdown.


### templates/article_details.html
- Page Title: Article Details
- Element IDs:
  - article-details-page (Div): Main container.
  - article-title (H1): Article title display.
  - article-author (Div): Article author display.
  - article-date (Div): Publication date display.
  - bookmark-button (Button): Bookmark the article.
  - article-content (Div): Full article content.
- Context Variables:
  - article: dict with keys (article_id:int, title:str, author:str, category:str, content:str, date:str, views:int)
  - is_bookmarked: bool
- Navigation Mappings:
  - bookmark-button: POST to url_for('bookmark_article', article_id=article['article_id'])
- Jinja2 Usage:
  - Display article fields using variable substitutions.


### templates/bookmarks.html
- Page Title: My Bookmarks
- Element IDs:
  - bookmarks-page (Div): Main container.
  - bookmarks-list (Div): Shows list of bookmarked articles.
  - remove-bookmark-button-{{bookmark_id}} (Button): Remove bookmark button per bookmark.
  - read-bookmark-button-{{bookmark_id}} (Button): View bookmarked article button per bookmark.
  - back-to-dashboard (Button): Navigates back to dashboard.
- Context Variables:
  - bookmarks: list of dicts (bookmark_id:int, article_id:int, article_title:str, bookmarked_date:str)
- Navigation Mappings:
  - remove-bookmark-button-{{bookmark_id}}: POST to url_for('remove_bookmark', bookmark_id=bookmark_id)
  - read-bookmark-button-{{bookmark_id}}: url_for('article_details', article_id=article_id)
  - back-to-dashboard: url_for('dashboard')
- Jinja2 Usage:
  - Loop over bookmarks to display bookmarks-list.


### templates/comments.html
- Page Title: Article Comments
- Element IDs:
  - comments-page (Div): Main container.
  - comments-list (Div): List of comments.
  - write-comment-button (Button): Navigates to write comment page.
  - filter-by-article (Dropdown): Dropdown to filter comments by article.
  - back-to-dashboard (Button): Navigates back to dashboard.
- Context Variables:
  - comments: list of dicts (comment_id:int, article_id:int, article_title:str, commenter_name:str, comment_text:str, comment_date:str)
  - articles: list of dicts (article_id:int, title:str)
  - selected_article: str (optional)
- Navigation Mappings:
  - write-comment-button: url_for('write_comment_page')
  - back-to-dashboard: url_for('dashboard')
- Jinja2 Usage:
  - Loop over comments to render comments-list.
  - Loop over articles for filter-by-article dropdown.


### templates/write_comment.html
- Page Title: Write a Comment
- Element IDs:
  - write-comment-page (Div): Main container.
  - select-article (Dropdown): Dropdown to select article for commenting.
  - commenter-name (Input): Input field for commenter name.
  - comment-text (Textarea): Textarea for comment text.
  - submit-comment-button (Button): Submit comment button.
- Context Variables:
  - articles: list of dicts (article_id:int, title:str)
- Navigation Mappings:
  - submit-comment-button: form POST to url_for('submit_comment')
- Jinja2 Usage:
  - Loop over articles to populate select-article dropdown.


### templates/trending.html
- Page Title: Trending Articles
- Element IDs:
  - trending-page (Div): Main container.
  - trending-list (Div): Ranked list of trending articles.
  - time-period-filter (Dropdown): Dropdown filter for time period.
  - view-article-button-{{article_id}} (Button): View article details button for each trending article.
  - back-to-dashboard (Button): Navigates back to dashboard.
- Context Variables:
  - trending_articles: list of dicts (article_id:int, article_title:str, category:str, view_count:int)
  - time_period: str (optional)
- Navigation Mappings:
  - view-article-button-{{article_id}}: url_for('article_details', article_id=article_id)
  - back-to-dashboard: url_for('dashboard')
- Jinja2 Usage:
  - Loop over trending_articles for trending-list.
  - Loop over time period options for dropdown.


### templates/category.html
- Page Title: Category Articles
- Element IDs:
  - category-page (Div): Main container.
  - category-title (H1): Displays category name.
  - category-articles (Div): List of articles in this category.
  - sort-by-date (Button): Sort articles by date.
  - sort-by-popularity (Button): Sort articles by popularity.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Context Variables:
  - category_name: str
  - articles: list of dicts (article_id:int, title:str, author:str, date:str, views:int)
- Navigation Mappings:
  - sort-by-date: POST to url_for('sort_category_articles', category_name=category_name) with sort_option='date'
  - sort-by-popularity: POST to url_for('sort_category_articles', category_name=category_name) with sort_option='popularity'
  - back-to-dashboard: url_for('dashboard')
- Jinja2 Usage:
  - Loop over articles for category-articles div.


### templates/search_results.html
- Page Title: Search Results
- Element IDs:
  - search-results-page (Div): Main container.
  - search-query-display (Div): Displays search query string.
  - results-list (Div): List of search result articles.
  - no-results-message (Div): Displays if no results found.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Context Variables:
  - search_query: str
  - results: list of dicts (article_id:int, title:str, excerpt:str)
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')
- Jinja2 Usage:
  - If results list empty, show no-results-message.
  - Loop over results for results-list div.

---

## Section 3: Data File Schemas

### data/articles.txt
- Fields (pipe-delimited):
  1. article_id (int)
  2. title (str)
  3. author (str)
  4. category (str)
  5. content (str)
  6. date (str, YYYY-MM-DD)
  7. views (int)
- Description: Stores all news articles with detailed content and metadata.
- Example Rows:
  ```
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891
  ```

### data/categories.txt
- Fields (pipe-delimited):
  1. category_id (int)
  2. category_name (str)
  3. description (str)
- Description: Defines the categories for articles.
- Example Rows:
  ```
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news
  ```

### data/bookmarks.txt
- Fields (pipe-delimited):
  1. bookmark_id (int)
  2. article_id (int)
  3. article_title (str)
  4. bookmarked_date (str, YYYY-MM-DD)
- Description: Stores user's bookmarked articles.
- Example Rows:
  ```
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18
  ```

### data/comments.txt
- Fields (pipe-delimited):
  1. comment_id (int)
  2. article_id (int)
  3. article_title (str)
  4. commenter_name (str)
  5. comment_text (str)
  6. comment_date (str, YYYY-MM-DD)
- Description: Stores comments made on articles.
- Example Rows:
  ```
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19
  ```

### data/trending.txt
- Fields (pipe-delimited):
  1. article_id (int)
  2. article_title (str)
  3. category (str)
  4. view_count (int)
  5. period (str)
- Description: Stores trending articles ranked by views and time period.
- Example Rows:
  ```
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month
  ```
