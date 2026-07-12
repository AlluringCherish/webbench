# NewsPortal Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                  | Flask Function Name        | HTTP Method | Template File             | Context Variables (Name:Type)                                                                              | Notes on Form Data (POST)                                    |
|-----------------------------|----------------------------|-------------|---------------------------|------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------|
| /                           | root_redirect               | GET         | None                      | None                                                                                                       | Redirects to /dashboard                                      |
| /dashboard                  | dashboard                  | GET         | dashboard.html            | featured_articles: list of dicts ({article_id:int, title:str, author:str, date:str}), trending_articles: list of dicts, categories: list of dicts |                                                           |
| /catalog                    | article_catalog            | GET         | catalog.html              | articles: list of dicts ({article_id:int, title:str, author:str, category:str, date:str}), categories: list of dicts, search_query: str (optional), selected_category: str (optional) |                                                           |
| /catalog/search             | catalog_search             | POST        | catalog.html              | articles: list of dicts, categories: list of dicts, search_query: str, selected_category: str                  | Form data: search_input (str), category_filter (str)         |
| /article/<int:article_id>   | article_details            | GET         | article_details.html      | article: dict ({article_id:int, title:str, author:str, date:str, content:str}), is_bookmarked: bool           |                                                           |
| /article/<int:article_id>/bookmark | bookmark_article        | POST        | article_details.html      | article: dict, is_bookmarked: bool                                                                             | No form fields, action to toggle bookmark status             |
| /bookmarks                 | bookmarks                  | GET         | bookmarks.html            | bookmarks: list of dicts ({bookmark_id:int, article_id:int, article_title:str, bookmarked_date:str})           |                                                           |
| /bookmarks/<int:bookmark_id>/remove | remove_bookmark           | POST        | bookmarks.html            | bookmarks: list of dicts                                                                                      | No form fields, action to remove bookmark                    |
| /comments                  | comments                   | GET         | comments.html             | comments: list of dicts ({comment_id:int, article_id:int, article_title:str, commenter_name:str, comment_text:str, comment_date:str}), articles: list of dicts |                                                           |
| /comments/filter           | comments_filter            | POST        | comments.html             | comments: list of dicts, articles: list of dicts, selected_article_id: int or None                             | Form data: filter_by_article (int or "All")                 |
| /comments/write            | write_comment              | GET         | write_comment.html        | articles: list of dicts                                                                                        |                                                           |
| /comments/write            | submit_comment             | POST        | write_comment.html        | submission_success: bool (optional), articles: list of dicts                                                 | Form data: select_article (int), commenter_name (str), comment_text (str) |
| /trending                  | trending_articles          | GET         | trending.html             | trending_articles: list of dicts ({article_id:int, title:str, category:str, view_count:int}), time_period: str  |                                                           |
| /trending/filter           | trending_filter            | POST        | trending.html             | trending_articles: list of dicts, time_period: str                                                          | Form data: time_period_filter (str)                         |
| /category/<string:category_name> | category_articles         | GET         | category.html             | category_name: str, articles: list of dicts                                                                  |                                                           |
| /category/<string:category_name>/sort | category_sort             | POST        | category.html             | category_name: str, articles: list of dicts                                                                  | Form data: sort_order (str: "date" or "popularity")      |
| /search/results            | search_results             | GET         | search_results.html       | search_query: str, articles: list of dicts                                                                   |                                                           |

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- File Path: templates/dashboard.html
- Page Title: News Portal
- Elements:
  - dashboard-page: Div - Container for dashboard page
  - featured-articles: Div - Display of featured article recommendations
  - browse-articles-button: Button - Navigates to Article Catalog page
  - view-bookmarks-button: Button - Navigates to Bookmarks page
  - trending-articles-button: Button - Navigates to Trending Articles page
- Context Variables:
  - featured_articles: list of dicts with keys: article_id (int), title (str), author (str), date (str)
  - trending_articles: list of dicts (structure depends on use)
- Navigation Mappings:
  - browse-articles-button -> url_for('article_catalog')
  - view-bookmarks-button -> url_for('bookmarks')
  - trending-articles-button -> url_for('trending_articles')

### 2. Article Catalog Page
- File Path: templates/catalog.html
- Page Title: Article Catalog
- Elements:
  - catalog-page: Div - Container for catalog page
  - search-input: Input - Search field for title, author or keywords
  - category-filter: Dropdown - Filter articles by category
  - articles-grid: Div - Grid displaying article cards
  - view-article-button-{article_id}: Button - View article details for each article
- Context Variables:
  - articles: list of dicts (article_id, title, author, category, date)
  - categories: list of dicts (category_id, category_name, description)
  - search_query: str (optional)
  - selected_category: str (optional)
- Navigation Mappings:
  - view-article-button-{article_id} -> url_for('article_details', article_id=article_id)

### 3. Article Details Page
- File Path: templates/article_details.html
- Page Title: Article Details
- Elements:
  - article-details-page: Div - Container for details page
  - article-title: H1 - Article title display
  - article-author: Div - Article author
  - article-date: Div - Article publication date
  - bookmark-button: Button - Bookmark the article
  - article-content: Div - Full article content
- Context Variables:
  - article: dict (article_id, title, author, date, content)
  - is_bookmarked: bool
- Navigation Mappings:
  - bookmark-button - POST action to url_for('bookmark_article', article_id=article.article_id)

### 4. Bookmarks Page
- File Path: templates/bookmarks.html
- Page Title: My Bookmarks
- Elements:
  - bookmarks-page: Div - Container for bookmarks page
  - bookmarks-list: Div - List of bookmarked articles
  - remove-bookmark-button-{bookmark_id}: Button - Remove bookmark
  - read-bookmark-button-{bookmark_id}: Button - Read bookmarked article
  - back-to-dashboard: Button - Navigate to dashboard
- Context Variables:
  - bookmarks: list of dicts (bookmark_id, article_id, article_title, bookmarked_date)
- Navigation Mappings:
  - remove-bookmark-button-{bookmark_id} - POST action to url_for('remove_bookmark', bookmark_id=bookmark_id)
  - read-bookmark-button-{bookmark_id} -> url_for('article_details', article_id=article_id)
  - back-to-dashboard -> url_for('dashboard')

### 5. Comments Page
- File Path: templates/comments.html
- Page Title: Article Comments
- Elements:
  - comments-page: Div - Container for comments page
  - comments-list: Div - List all comments
  - write-comment-button: Button - Navigate to Write Comment page
  - filter-by-article: Dropdown - Filter comments by article
  - back-to-dashboard: Button - Navigate to dashboard
- Context Variables:
  - comments: list of dicts (comment_id, article_id, article_title, commenter_name, comment_text, comment_date)
  - articles: list of dicts (article_id, title, author, category, date)
- Navigation Mappings:
  - write-comment-button -> url_for('write_comment')
  - back-to-dashboard -> url_for('dashboard')

### 6. Write Comment Page
- File Path: templates/write_comment.html
- Page Title: Write a Comment
- Elements:
  - write-comment-page: Div - Container for write comment page
  - select-article: Dropdown - Select article to comment on
  - commenter-name: Input - Input commenter name
  - comment-text: Textarea - Write comment content
  - submit-comment-button: Button - Submit comment
- Context Variables:
  - articles: list of dicts (article_id, title, author, category, date)
- Navigation Mappings:
  - submit-comment-button - POST action to url_for('submit_comment')

### 7. Trending Articles Page
- File Path: templates/trending.html
- Page Title: Trending Articles
- Elements:
  - trending-page: Div - Container for trending articles
  - trending-list: Div - Ranked list of trending articles
  - time-period-filter: Dropdown - Filter by time period
  - view-article-button-{article_id}: Button - View article details
  - back-to-dashboard: Button - Navigate to dashboard
- Context Variables:
  - trending_articles: list of dicts (article_id, title, category, view_count)
  - time_period: str
- Navigation Mappings:
  - view-article-button-{article_id} -> url_for('article_details', article_id=article_id)
  - back-to-dashboard -> url_for('dashboard')

### 8. Category Page
- File Path: templates/category.html
- Page Title: Category Articles
- Elements:
  - category-page: Div - Container for category page
  - category-title: H1 - Display category name
  - category-articles: Div - List articles in category
  - sort-by-date: Button - Sort articles by date
  - sort-by-popularity: Button - Sort articles by popularity
  - back-to-dashboard: Button - Navigate to dashboard
- Context Variables:
  - category_name: str
  - articles: list of dicts
- Navigation Mappings:
  - sort-by-date - POST action to url_for('category_sort', category_name=category_name) with form sort_order='date'
  - sort-by-popularity - POST action to url_for('category_sort', category_name=category_name) with form sort_order='popularity'
  - back-to-dashboard -> url_for('dashboard')

### 9. Search Results Page
- File Path: templates/search_results.html
- Page Title: Search Results
- Elements:
  - search-results-page: Div - Container for search results
  - search-query-display: Div - Display search query
  - results-list: Div - List search results
  - no-results-message: Div - Message if no results
  - back-to-dashboard: Button - Navigate back to dashboard
- Context Variables:
  - search_query: str
  - articles: list of dicts (article_id, title, excerpt)
- Navigation Mappings:
  - back-to-dashboard -> url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. Articles Data
- File Path: data/articles.txt
- Format: pipe-delimited (`|`)
- Fields Order:
  1. article_id (int)
  2. title (str)
  3. author (str)
  4. category (str)
  5. content (str)
  6. date (str in YYYY-MM-DD format)
  7. views (int)
- Description: Stores all news articles with metadata and content.
- Example Rows:
  ```
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891
  ```

### 2. Categories Data
- File Path: data/categories.txt
- Format: pipe-delimited (`|`)
- Fields Order:
  1. category_id (int)
  2. category_name (str)
  3. description (str)
- Description: Stores categories available for articles.
- Example Rows:
  ```
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news
  ```

### 3. Bookmarks Data
- File Path: data/bookmarks.txt
- Format: pipe-delimited (`|`)
- Fields Order:
  1. bookmark_id (int)
  2. article_id (int)
  3. article_title (str)
  4. bookmarked_date (str YYYY-MM-DD)
- Description: Stores user bookmarks referenced by article.
- Example Rows:
  ```
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18
  ```

### 4. Comments Data
- File Path: data/comments.txt
- Format: pipe-delimited (`|`)
- Fields Order:
  1. comment_id (int)
  2. article_id (int)
  3. article_title (str)
  4. commenter_name (str)
  5. comment_text (str)
  6. comment_date (str YYYY-MM-DD)
- Description: Stores comments on articles.
- Example Rows:
  ```
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19
  ```

### 5. Trending Data
- File Path: data/trending.txt
- Format: pipe-delimited (`|`)
- Fields Order:
  1. article_id (int)
  2. article_title (str)
  3. category (str)
  4. view_count (int)
  5. period (str)
- Description: Stores trending articles data by period.
- Example Rows:
  ```
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month
  ```