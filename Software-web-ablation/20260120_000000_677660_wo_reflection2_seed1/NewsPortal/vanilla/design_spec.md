# NewsPortal Design Specification

## Section 1: Flask Routes Specification

| Route Path | Flask Function Name | HTTP Method | Template | Context Variables | Form Data (POST) |
|------------|--------------------|-------------|----------|-------------------|------------------|
| / | root_redirect     | GET  | None (redirect) | None | None |
| /dashboard | dashboard_page    | GET  | dashboard.html | featured_articles: list of dict, trending_articles: list of dict | None |
| /catalog | article_catalog    | GET  | catalog.html   | articles: list of dict, categories: list of dict, selected_category: str or None, search_query: str or None | None |
| /article/<int:article_id> | article_details  | GET  | article_details.html | article: dict, is_bookmarked: bool | None |
| /article/<int:article_id>/bookmark | bookmark_article | POST | None (redirect to article details) | None | None (implicitly article_id in URL) |
| /bookmarks | bookmarks_page    | GET  | bookmarks.html | bookmarks: list of dict | None |
| /bookmark/<int:bookmark_id>/remove | remove_bookmark | POST | None (redirect to bookmarks) | None | None (implicitly bookmark_id in URL) |
| /comments | comments_page     | GET  | comments.html  | comments: list of dict, articles: list of dict, selected_article_id: int or None | None |
| /comments/write | write_comment_page | GET  | write_comment.html | articles: list of dict | None |
| /comments/write | submit_comment    | POST | None (redirect to comments) | None | commenter_name: str, comment_text: str, article_id: int (from form) |
| /trending | trending_articles  | GET  | trending.html  | trending_articles: list of dict, time_period: str (filter selection) | None |
| /category/<string:category_name> | category_page    | GET  | category.html  | category_name: str, articles: list of dict | None |
| /category/<string:category_name>/sort/<string:sort_type> | sort_category_articles | GET  | category.html  | category_name: str, articles: list of dict, sort_type: str | None |
| /search | search_results     | GET  | search_results.html | search_query: str, search_results: list of dict | None |


### Notes:
- The root route "/" redirects to the dashboard page at "/dashboard".
- Each route renders the template matching the page design as per requirements.
- POST routes used for bookmarking articles and removing bookmarks or submitting comments.
- Context variable dict structures are detailed in Section 2.


## Section 2: HTML Template Specifications

---

### Template: templates/dashboard.html
- Page Title: News Portal
- <title> and <h1>: "News Portal"
- Elements:
  - ID: dashboard-page (Div): Container for the dashboard page
  - ID: featured-articles (Div): Display featured article recommendations
  - ID: browse-articles-button (Button): Navigate to article catalog page
  - ID: view-bookmarks-button (Button): Navigate to bookmarks page
  - ID: trending-articles-button (Button): Navigate to trending articles page
- Context Variables:
  - featured_articles: list of dict, each dict with keys: article_id (int), title (str), author (str), category (str), date (str "YYYY-MM-DD"), excerpt (str)
  - trending_articles: list of dict, each dict with keys: article_id (int), title (str), category (str), view_count (int)
- Navigation:
  - #browse-articles-button -> url_for('article_catalog')
  - #view-bookmarks-button -> url_for('bookmarks_page')
  - #trending-articles-button -> url_for('trending_articles')

---

### Template: templates/catalog.html
- Page Title: Article Catalog
- <title> and <h1>: "Article Catalog"
- Elements:
  - ID: catalog-page (Div): Container for catalog page
  - ID: search-input (Input): Search field text input
  - ID: category-filter (Dropdown): Category filter dropdown
  - ID: articles-grid (Div): Grid for article cards
  - ID: view-article-button-{article_id} (Button): Button per article to view details
- Context Variables:
  - articles: list of dict, each with keys: article_id (int), title (str), author (str), category (str), date (str "YYYY-MM-DD"), excerpt (str)
  - categories: list of dict, each with keys: category_id (int), category_name (str), description (str)
  - selected_category: str or None
  - search_query: str or None
- Navigation:
  - Each #view-article-button-{article_id} -> url_for('article_details', article_id=article_id)

---

### Template: templates/article_details.html
- Page Title: Article Details
- <title> and <h1>: "Article Details"
- Elements:
  - ID: article-details-page (Div): Container for article details
  - ID: article-title (H1): Article title
  - ID: article-author (Div): Article author
  - ID: article-date (Div): Article publication date
  - ID: bookmark-button (Button): Bookmark article
  - ID: article-content (Div): Full article content
- Context Variables:
  - article: dict with keys: article_id (int), title (str), author (str), category (str), content (str), date (str "YYYY-MM-DD"), views (int)
  - is_bookmarked: bool
- Navigation:
  - #bookmark-button -> POST to url_for('bookmark_article', article_id=article.article_id)

---

### Template: templates/bookmarks.html
- Page Title: My Bookmarks
- <title> and <h1>: "My Bookmarks"
- Elements:
  - ID: bookmarks-page (Div): Container for bookmarks page
  - ID: bookmarks-list (Div): List of bookmarked articles
  - ID: remove-bookmark-button-{bookmark_id} (Button): Remove bookmark per bookmark
  - ID: read-bookmark-button-{bookmark_id} (Button): Read bookmarked article per bookmark
  - ID: back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - bookmarks: list of dict, each with keys: bookmark_id (int), article_id (int), article_title (str), bookmarked_date (str "YYYY-MM-DD")
- Navigation:
  - Each #remove-bookmark-button-{bookmark_id} -> POST to url_for('remove_bookmark', bookmark_id=bookmark_id)
  - Each #read-bookmark-button-{bookmark_id} -> url_for('article_details', article_id=article_id)
  - #back-to-dashboard -> url_for('dashboard_page')

---

### Template: templates/comments.html
- Page Title: Article Comments
- <title> and <h1>: "Article Comments"
- Elements:
  - ID: comments-page (Div): Container for comments page
  - ID: comments-list (Div): List of comments
  - ID: write-comment-button (Button): Navigate to write comment page
  - ID: filter-by-article (Dropdown): Filter comments by article
  - ID: back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - comments: list of dict, each with keys: comment_id (int), article_id (int), article_title (str), commenter_name (str), comment_text (str), comment_date (str "YYYY-MM-DD")
  - articles: list of dict, each with keys: article_id (int), title (str)
  - selected_article_id: int or None
- Navigation:
  - #write-comment-button -> url_for('write_comment_page')
  - #back-to-dashboard -> url_for('dashboard_page')

---

### Template: templates/write_comment.html
- Page Title: Write a Comment
- <title> and <h1>: "Write a Comment"
- Elements:
  - ID: write-comment-page (Div): Container for write comment page
  - ID: select-article (Dropdown): Select article to comment on
  - ID: commenter-name (Input): Input for commenter name
  - ID: comment-text (Textarea): Textarea for comment text
  - ID: submit-comment-button (Button): Submit comment
- Context Variables:
  - articles: list of dict, each with keys: article_id (int), title (str)
- Navigation:
  - Form POST to url_for('submit_comment')

---

### Template: templates/trending.html
- Page Title: Trending Articles
- <title> and <h1>: "Trending Articles"
- Elements:
  - ID: trending-page (Div): Container for trending articles page
  - ID: trending-list (Div): Ranked list of trending articles
  - ID: time-period-filter (Dropdown): Filter by time period
  - ID: view-article-button-{article_id} (Button): View article details per trending article
  - ID: back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - trending_articles: list of dict, each with keys: article_id (int), article_title (str), category (str), view_count (int), period (str)
  - time_period: str
- Navigation:
  - Each #view-article-button-{article_id} -> url_for('article_details', article_id=article_id)
  - #back-to-dashboard -> url_for('dashboard_page')

---

### Template: templates/category.html
- Page Title: Category Articles
- <title> and <h1>: "Category Articles"
- Elements:
  - ID: category-page (Div): Container for category page
  - ID: category-title (H1): Category name display
  - ID: category-articles (Div): List of articles
  - ID: sort-by-date (Button): Sort articles by date
  - ID: sort-by-popularity (Button): Sort articles by popularity
  - ID: back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - category_name: str
  - articles: list of dict, each with keys: article_id (int), title (str), author (str), date (str), views (int)
- Navigation:
  - #sort-by-date -> url_for('sort_category_articles', category_name=category_name, sort_type='date')
  - #sort-by-popularity -> url_for('sort_category_articles', category_name=category_name, sort_type='popularity')
  - #back-to-dashboard -> url_for('dashboard_page')

---

### Template: templates/search_results.html
- Page Title: Search Results
- <title> and <h1>: "Search Results"
- Elements:
  - ID: search-results-page (Div): Container for search results page
  - ID: search-query-display (Div): Display user search query
  - ID: results-list (Div): List of article results
  - ID: no-results-message (Div): Message shown if no results found
  - ID: back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - search_query: str
  - search_results: list of dict, each with keys: article_id (int), title (str), excerpt (str)
- Navigation:
  - #back-to-dashboard -> url_for('dashboard_page')


## Section 3: Data File Schemas

---

### 1. Articles Data
- File Path: data/articles.txt
- Format: Pipe-delimited (|)
- Fields in order:
  1. article_id (int)
  2. title (str)
  3. author (str)
  4. category (str)
  5. content (str)
  6. date (str, format YYYY-MM-DD)
  7. views (int)
- Description: Stores all news articles with metadata and content
- Example rows:
  - 1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  - 2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  - 3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891

---

### 2. Categories Data
- File Path: data/categories.txt
- Format: Pipe-delimited (|)
- Fields in order:
  1. category_id (int)
  2. category_name (str)
  3. description (str)
- Description: List of news categories with descriptions
- Example rows:
  - 1|Technology|Latest tech news and innovations
  - 2|Sports|Sports news and event coverage
  - 3|Business|Business and finance news

---

### 3. Bookmarks Data
- File Path: data/bookmarks.txt
- Format: Pipe-delimited (|)
- Fields in order:
  1. bookmark_id (int)
  2. article_id (int)
  3. article_title (str)
  4. bookmarked_date (str, format YYYY-MM-DD)
- Description: Stores user bookmarked articles
- Example rows:
  - 1|1|Breaking: New Technology Breakthrough|2025-01-20
  - 2|3|Business: Market Trends Analysis|2025-01-18

---

### 4. Comments Data
- File Path: data/comments.txt
- Format: Pipe-delimited (|)
- Fields in order:
  1. comment_id (int)
  2. article_id (int)
  3. article_title (str)
  4. commenter_name (str)
  5. comment_text (str)
  6. comment_date (str, format YYYY-MM-DD)
- Description: All comments made on news articles
- Example rows:
  - 1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  - 2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19

---

### 5. Trending Data
- File Path: data/trending.txt
- Format: Pipe-delimited (|)
- Fields in order:
  1. article_id (int)
  2. article_title (str)
  3. category (str)
  4. view_count (int)
  5. period (str) (e.g., Today, This Week, This Month)
- Description: Articles ranked by views for different time periods
- Example rows:
  - 1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  - 2|Sports: Championship Victory|Sports|3210|This Week
  - 3|Business: Market Trends Analysis|Business|2891|This Month
