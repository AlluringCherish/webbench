# NewsPortal Application Design Specifications

---

## Section 1: Flask Routes Specification

| Route Path               | Flask Function Name        | HTTP Method | Template File           | Context Variables (name:type)                                                                            | Form Data (POST)                        |
|--------------------------|----------------------------|-------------|-------------------------|---------------------------------------------------------------------------------------------------------|----------------------------------------|
| /                        | root_redirect              | GET         | N/A (redirect)          | None                                                                                                    | None                                   |
| /dashboard               | dashboard_page             | GET         | dashboard.html          | featured_articles: list of dicts, trending_articles: list of dicts                                      | None                                   |
| /catalog                 | article_catalog            | GET         | catalog.html            | articles: list of dicts, categories: list of dicts, search_query: str (optional), category_filter: str (optional) | None                                   |
| /catalog/search          | catalog_search             | POST        | catalog.html            | articles: list of dicts, categories: list of dicts, search_query: str, category_filter: str                | search_query: str, category_filter: str|
| /article/<int:article_id>| article_details            | GET         | article_details.html    | article: dict                                                                                           | None                                   |
| /article/<int:article_id>/bookmark | bookmark_article          | POST        | article_details.html    | article: dict, bookmark_success: bool (optional)                                                        | article_id: int                        |
| /bookmarks               | bookmarks_page             | GET         | bookmarks.html          | bookmarks: list of dicts                                                                                 | None                                   |
| /bookmarks/remove/<int:bookmark_id> | remove_bookmark            | POST        | bookmarks.html          | bookmarks: list of dicts                                                                                 | bookmark_id: int                       |
| /comments                | comments_page              | GET         | comments.html           | comments: list of dicts, articles: list of dicts, filter_article_id: int (optional)                       | None                                   |
| /comments/filter         | filter_comments            | POST        | comments.html           | comments: list of dicts, articles: list of dicts, filter_article_id: int                                 | filter_article_id: int                 |
| /comments/write          | write_comment_get          | GET         | write_comment.html      | articles: list of dicts                                                                                   | None                                   |
| /comments/write/submit   | write_comment_post         | POST        | write_comment.html      | articles: list of dicts, submit_success: bool (optional)                                                | article_id: int, commenter_name: str, comment_text: str |
| /trending                | trending_articles          | GET         | trending.html           | trending_articles: list of dicts, time_period: str (optional)                                           | None                                   |
| /trending/filter         | filter_trending            | POST        | trending.html           | trending_articles: list of dicts, time_period: str                                                     | time_period: str                      |
| /category/<string:category_name> | category_articles         | GET         | category.html           | category_name: str, articles: list of dicts                                                             | None                                   |
| /category/<string:category_name>/sort | sort_category_articles     | POST        | category.html           | category_name: str, articles: list of dicts, sort_by: str                                               | sort_by: str                          |
| /search                  | search_results             | POST        | search_results.html     | search_query: str, results: list of dicts                                                               | search_query: str                     |
| /search/results          | search_results_get         | GET         | search_results.html     | search_query: str, results: list of dicts                                                               | None                                   |

**Notes:**
- Root route `/` redirects to `/dashboard`.
- POST routes are mostly for form submissions like search, bookmark, comments, sorting.
- Context variables named explicitly with types like str, int, list, dict.


---

## Section 2: HTML Template Specifications

### 1. Dashboard Page - templates/dashboard.html
- **Page Title:** News Portal
- **<title>** and <h1> tags: "News Portal"
- **Element IDs:**
  - dashboard-page: Div, container for dashboard page
  - featured-articles: Div, displays featured article recommendations
  - browse-articles-button: Button, navigates to article catalog page (/catalog)
  - view-bookmarks-button: Button, navigates to bookmarks page (/bookmarks)
  - trending-articles-button: Button, navigates to trending articles page (/trending)
- **Context Variables:**
  - featured_articles: list of dicts with keys: article_id (int), title (str), excerpt (str)
  - trending_articles: list of dicts with keys: article_id (int), title (str), views (int)
- **Navigation mappings:**
  - browse-articles-button onclick: url_for('article_catalog')
  - view-bookmarks-button onclick: url_for('bookmarks_page')
  - trending-articles-button onclick: url_for('trending_articles')

### 2. Article Catalog Page - templates/catalog.html
- **Page Title:** Article Catalog
- **<title>** and <h1> tags: "Article Catalog"
- **Element IDs:**
  - catalog-page: Div, container for catalog page
  - search-input: Input text, for searching articles by title, author, or keywords
  - category-filter: Dropdown, filter articles by category
  - articles-grid: Div, grid displaying article cards
  - view-article-button-{article_id}: Button per article card to view details
- **Context Variables:**
  - articles: list of dicts with fields: article_id (int), title (str), author (str), category (str), date (str)
  - categories: list of dicts with fields: category_id (int), category_name (str)
  - search_query: str
  - category_filter: str
- **Navigation mappings:**
  - view-article-button-{article_id} onclick: url_for('article_details', article_id=article_id)

### 3. Article Details Page - templates/article_details.html
- **Page Title:** Article Details
- **<title>** and <h1> tags: "Article Details"
- **Element IDs:**
  - article-details-page: Div, container for article details
  - article-title: H1, displays article title
  - article-author: Div, article author
  - article-date: Div, article publication date
  - bookmark-button: Button, bookmarks the article
  - article-content: Div, full article content
- **Context Variables:**
  - article: dict with keys article_id (int), title (str), author (str), category (str), content (str), date (str), views (int)
- **Navigation mappings:**
  - bookmark-button onclick: triggers POST to bookmark the article

### 4. Bookmarks Page - templates/bookmarks.html
- **Page Title:** My Bookmarks
- **<title>** and <h1> tags: "My Bookmarks"
- **Element IDs:**
  - bookmarks-page: Div, container for bookmarks page
  - bookmarks-list: Div, list displaying all bookmarked articles
  - remove-bookmark-button-{bookmark_id}: Button, removes bookmark
  - read-bookmark-button-{bookmark_id}: Button, reads bookmarked article
  - back-to-dashboard: Button, navigates back to dashboard
- **Context Variables:**
  - bookmarks: list of dicts with keys: bookmark_id (int), article_id (int), article_title (str), bookmarked_date (str)
- **Navigation mappings:**
  - remove-bookmark-button-{bookmark_id} onclick: POST to remove bookmark
  - read-bookmark-button-{bookmark_id} onclick: url_for('article_details', article_id=article_id)
  - back-to-dashboard onclick: url_for('dashboard_page')

### 5. Comments Page - templates/comments.html
- **Page Title:** Article Comments
- **<title>** and <h1> tags: "Article Comments"
- **Element IDs:**
  - comments-page: Div, container for comments page
  - comments-list: Div, list of all comments
  - write-comment-button: Button, navigates to write comment page
  - filter-by-article: Dropdown, filter comments by article
  - back-to-dashboard: Button, navigates back to dashboard
- **Context Variables:**
  - comments: list of dicts with keys: comment_id (int), article_id (int), article_title (str), commenter_name (str), comment_text (str), comment_date (str)
  - articles: list of dicts with article_id (int), title (str)
- **Navigation mappings:**
  - write-comment-button onclick: url_for('write_comment_get')
  - back-to-dashboard onclick: url_for('dashboard_page')

### 6. Write Comment Page - templates/write_comment.html
- **Page Title:** Write a Comment
- **<title>** and <h1> tags: "Write a Comment"
- **Element IDs:**
  - write-comment-page: Div, container for write comment page
  - select-article: Dropdown, select article to comment on
  - commenter-name: Input, text input for commenter name
  - comment-text: Textarea, input for comment text
  - submit-comment-button: Button, submits the comment
- **Context Variables:**
  - articles: list of dicts with article_id (int), title (str)
- **Navigation mappings:**
  - submit-comment-button onclick: POST form submission

### 7. Trending Articles Page - templates/trending.html
- **Page Title:** Trending Articles
- **<title>** and <h1> tags: "Trending Articles"
- **Element IDs:**
  - trending-page: Div, container for trending page
  - trending-list: Div, ranked listing of trending articles
  - time-period-filter: Dropdown, filter trending by time period
  - view-article-button-{article_id}: Button, reads detailed article
  - back-to-dashboard: Button, navigates back to dashboard
- **Context Variables:**
  - trending_articles: list of dicts with article_id (int), article_title (str), category (str), view_count (int), period (str)
  - time_period: str
- **Navigation mappings:**
  - view-article-button-{article_id} onclick: url_for('article_details', article_id=article_id)
  - back-to-dashboard onclick: url_for('dashboard_page')

### 8. Category Page - templates/category.html
- **Page Title:** Category Articles
- **<title>** and <h1> tags: "Category Articles"
- **Element IDs:**
  - category-page: Div, container for category page
  - category-title: H1, displays the category name
  - category-articles: Div, list of articles from category
  - sort-by-date: Button, sort articles by date
  - sort-by-popularity: Button, sort articles by popularity
  - back-to-dashboard: Button, navigates back to dashboard
- **Context Variables:**
  - category_name: str
  - articles: list of dicts with article_id (int), title (str), author (str), date (str), views (int)
- **Navigation mappings:**
  - sort-by-date onclick: POST to sort_category_articles with sort_by='date'
  - sort-by-popularity onclick: POST to sort_category_articles with sort_by='popularity'
  - back-to-dashboard onclick: url_for('dashboard_page')

### 9. Search Results Page - templates/search_results.html
- **Page Title:** Search Results
- **<title>** and <h1> tags: "Search Results"
- **Element IDs:**
  - search-results-page: Div, container for search results page
  - search-query-display: Div, displays user’s search query
  - results-list: Div, list of search results with title and excerpt
  - no-results-message: Div, message when no search results
  - back-to-dashboard: Button, navigates back to dashboard
- **Context Variables:**
  - search_query: str
  - results: list of dicts with article_id (int), title (str), excerpt (str)
- **Navigation mappings:**
  - back-to-dashboard onclick: url_for('dashboard_page')


---

## Section 3: Data File Schemas

### 1. Articles Data
- **File Path:** data/articles.txt
- **Format:** Pipe-delimited (|)
- **Fields (in order):** article_id|title|author|category|content|date|views
- **Description:** Stores all articles details.
- **Example Rows:**
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891

### 2. Categories Data
- **File Path:** data/categories.txt
- **Format:** Pipe-delimited (|)
- **Fields (in order):** category_id|category_name|description
- **Description:** Stores categories and their descriptions.
- **Example Rows:**
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news

### 3. Bookmarks Data
- **File Path:** data/bookmarks.txt
- **Format:** Pipe-delimited (|)
- **Fields (in order):** bookmark_id|article_id|article_title|bookmarked_date
- **Description:** Stores user bookmarks of articles.
- **Example Rows:**
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18

### 4. Comments Data
- **File Path:** data/comments.txt
- **Format:** Pipe-delimited (|)
- **Fields (in order):** comment_id|article_id|article_title|commenter_name|comment_text|comment_date
- **Description:** Stores comments on articles.
- **Example Rows:**
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19

### 5. Trending Data
- **File Path:** data/trending.txt
- **Format:** Pipe-delimited (|)
- **Fields (in order):** article_id|article_title|category|view_count|period
- **Description:** Stores trending articles by period.
- **Example Rows:**
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month

---

**End of Design Specification**
