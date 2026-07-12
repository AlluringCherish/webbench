# NewsPortal Design Specification

## Section 1: Flask Routes Specification

| Route Path | Flask Function Name | HTTP Method | Template | Context Variables | Form Data (POST) |
|------------|--------------------|-------------|----------|-------------------|------------------|
| / | root_redirect     | GET  | None (redirect) | None | None |
| /dashboard | dashboard_page    | GET  | dashboard.html | featured_articles: list of dict, trending_articles: list of dict | None |
| /catalog | article_catalog    | GET  | catalog.html   | articles: list of dict, categories: list of dict, selected_category: str or None, search_query: str or None | None |
| /article/<int:article_id> | article_details  | GET  | article_details.html | article: dict, is_bookmarked: bool | None |
| /article/<int:article_id>/bookmark | bookmark_article | POST | None (redirect) | None | None (uses URL param article_id) |
| /bookmarks | bookmarks_page    | GET  | bookmarks.html | bookmarks: list of dict | None |
| /bookmarks/<int:bookmark_id>/remove | remove_bookmark | POST | None (redirect) | None | None (uses URL param bookmark_id) |
| /comments | comments_page     | GET  | comments.html  | comments: list of dict, articles: list of dict, selected_article: str or None | None |
| /comments/write | write_comment_page | GET  | write_comment.html | articles: list of dict | None |
| /comments/write | submit_comment    | POST | None (redirect) | None | commenter_name: str, comment_text: str, article_id: int (from form fields) |
| /trending | trending_articles | GET  | trending.html  | trending_articles: list of dict, selected_period: str | None |
| /category/<string:category_name> | category_articles | GET  | category.html  | category_name: str, articles: list of dict | None |
| /category/<string:category_name>/sort/<string:sort_by> | sort_category_articles | GET  | category.html  | category_name: str, articles: list of dict, sort_by: str ("date" or "popularity") | None |
| /search | search_results    | GET  | search_results.html | search_query: str, results: list of dict | None |

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- File path: templates/dashboard.html
- Page title: "News Portal"
- <h1> title: "News Portal"
- Elements:
  - ID: dashboard-page (Div) - Container for the dashboard page
  - ID: featured-articles (Div) - Display of featured article recommendations
  - ID: browse-articles-button (Button) - Navigate to /catalog
  - ID: view-bookmarks-button (Button) - Navigate to /bookmarks
  - ID: trending-articles-button (Button) - Navigate to /trending
- Context variables:
  - featured_articles: list of dict, each dict with keys: article_id (int), title (str), author (str), date (str)
  - trending_articles: list of dict (optional usage, if needed for display on dashboard)
- Navigation Mappings:
  - #browse-articles-button -> url_for('article_catalog')
  - #view-bookmarks-button -> url_for('bookmarks_page')
  - #trending-articles-button -> url_for('trending_articles')

### 2. Article Catalog Page
- File path: templates/catalog.html
- Page title: "Article Catalog"
- <h1> title: "Article Catalog"
- Elements:
  - ID: catalog-page (Div) - Container for the catalog
  - ID: search-input (Input) - Search field for title, author, or keywords
  - ID: category-filter (Dropdown) - Filter by category, options from categories context variable
  - ID: articles-grid (Div) - Grid of article cards
  - ID pattern: view-article-button-{article_id} (Button) - View details for article
- Context variables:
  - articles: list of dict, each dict fields: article_id (int), title (str), author (str), category (str), date (str), excerpt (str)
  - categories: list of dict, fields: category_id (int), category_name (str), description (str)
  - selected_category: str or None
  - search_query: str or None
- Navigation Mappings:
  - Each #view-article-button-{article_id} -> url_for('article_details', article_id=article_id)

### 3. Article Details Page
- File path: templates/article_details.html
- Page title: "Article Details"
- <h1> title: article_title context variable
- Elements:
  - ID: article-details-page (Div) - Container
  - ID: article-title (H1) - Title of article
  - ID: article-author (Div) - Author
  - ID: article-date (Div) - Publication date
  - ID: bookmark-button (Button) - Bookmark article
  - ID: article-content (Div) - Full article content
- Context variables:
  - article: dict with keys: article_id (int), title (str), author (str), category (str), content (str), date (str), views (int)
  - is_bookmarked: bool
- Navigation Mappings:
  - #bookmark-button triggers POST to /article/<int:article_id>/bookmark

### 4. Bookmarks Page
- File path: templates/bookmarks.html
- Page title: "My Bookmarks"
- <h1> title: "My Bookmarks"
- Elements:
  - ID: bookmarks-page (Div) - Container
  - ID: bookmarks-list (Div) - Listing bookmarks
  - ID pattern: remove-bookmark-button-{bookmark_id} (Button) - Remove bookmark
  - ID pattern: read-bookmark-button-{bookmark_id} (Button) - Read bookmarked article
  - ID: back-to-dashboard (Button) - Navigate to /dashboard
- Context variables:
  - bookmarks: list of dict with keys: bookmark_id (int), article_id (int), article_title (str), bookmarked_date (str)
- Navigation Mappings:
  - Each #remove-bookmark-button-{bookmark_id} triggers POST to /bookmarks/<int:bookmark_id>/remove
  - Each #read-bookmark-button-{bookmark_id} -> url_for('article_details', article_id=article_id)
  - #back-to-dashboard -> url_for('dashboard_page')

### 5. Comments Page
- File path: templates/comments.html
- Page title: "Article Comments"
- <h1> title: "Article Comments"
- Elements:
  - ID: comments-page (Div) - Container
  - ID: comments-list (Div) - List of comments
  - ID: write-comment-button (Button) - Navigate to /comments/write
  - ID: filter-by-article (Dropdown) - Filter comments by article
  - ID: back-to-dashboard (Button) - Navigate to /dashboard
- Context variables:
  - comments: list of dict with keys: comment_id (int), article_id (int), article_title (str), commenter_name (str), comment_text (str), comment_date (str)
  - articles: list of dict with keys: article_id (int), title (str)
  - selected_article: str or None
- Navigation Mappings:
  - #write-comment-button -> url_for('write_comment_page')
  - #back-to-dashboard -> url_for('dashboard_page')

### 6. Write Comment Page
- File path: templates/write_comment.html
- Page title: "Write a Comment"
- <h1> title: "Write a Comment"
- Elements:
  - ID: write-comment-page (Div) - Container
  - ID: select-article (Dropdown) - Select article to comment
  - ID: commenter-name (Input) - Input commenter name
  - ID: comment-text (Textarea) - Write comment text
  - ID: submit-comment-button (Button) - Submit comment form
- Context variables:
  - articles: list of dict with keys: article_id (int), title (str)
- Navigation Mappings:
  - Form submission POSTs to /comments/write

### 7. Trending Articles Page
- File path: templates/trending.html
- Page title: "Trending Articles"
- <h1> title: "Trending Articles"
- Elements:
  - ID: trending-page (Div) - Container
  - ID: trending-list (Div) - Ranked list
  - ID: time-period-filter (Dropdown) - Filter by time period (Today, This Week, This Month)
  - ID pattern: view-article-button-{article_id} (Button) - View article details
  - ID: back-to-dashboard (Button) - Navigate to /dashboard
- Context variables:
  - trending_articles: list of dict with keys: article_id (int), article_title (str), category (str), view_count (int), period (str)
  - selected_period: str
- Navigation Mappings:
  - Each #view-article-button-{article_id} -> url_for('article_details', article_id=article_id)
  - #back-to-dashboard -> url_for('dashboard_page')

### 8. Category Page
- File path: templates/category.html
- Page title: "Category Articles"
- <h1> title: category_name context variable
- Elements:
  - ID: category-page (Div) - Container
  - ID: category-title (H1) - Display category name
  - ID: category-articles (Div) - List articles in category
  - ID: sort-by-date (Button) - Sort articles by date
  - ID: sort-by-popularity (Button) - Sort articles by popularity
  - ID: back-to-dashboard (Button) - Navigate to /dashboard
- Context variables:
  - category_name: str
  - articles: list of dict with keys: article_id (int), title (str), author (str), date (str), views (int)
- Navigation Mappings:
  - #sort-by-date -> url_for('sort_category_articles', category_name=category_name, sort_by='date')
  - #sort-by-popularity -> url_for('sort_category_articles', category_name=category_name, sort_by='popularity')
  - #back-to-dashboard -> url_for('dashboard_page')

### 9. Search Results Page
- File path: templates/search_results.html
- Page title: "Search Results"
- <h1> title: "Search Results"
- Elements:
  - ID: search-results-page (Div) - Container
  - ID: search-query-display (Div) - Display the search query
  - ID: results-list (Div) - List of search result articles
  - ID: no-results-message (Div) - Message when no results found
  - ID: back-to-dashboard (Button) - Navigate to /dashboard
- Context variables:
  - search_query: str
  - results: list of dict with keys: article_id (int), title (str), excerpt (str)
- Navigation Mappings:
  - #back-to-dashboard -> url_for('dashboard_page')

---

## Section 3: Data File Schemas

### 1. Articles Data
- File path: data/articles.txt
- Pipe-delimited format with fields in exact order:
  article_id|title|author|category|content|date|views
- Description: Contains all news articles with metadata and content.
- Example rows:
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891

### 2. Categories Data
- File path: data/categories.txt
- Pipe-delimited format with fields in exact order:
  category_id|category_name|description
- Description: Contains the categories of news articles.
- Example rows:
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news

### 3. Bookmarks Data
- File path: data/bookmarks.txt
- Pipe-delimited format with fields in exact order:
  bookmark_id|article_id|article_title|bookmarked_date
- Description: Stores user bookmarked articles.
- Example rows:
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18

### 4. Comments Data
- File path: data/comments.txt
- Pipe-delimited format with fields in exact order:
  comment_id|article_id|article_title|commenter_name|comment_text|comment_date
- Description: Stores comments made on articles.
- Example rows:
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19

### 5. Trending Data
- File path: data/trending.txt
- Pipe-delimited format with fields in exact order:
  article_id|article_title|category|view_count|period
- Description: Stores trending articles ranked by views and time period.
- Example rows:
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month
