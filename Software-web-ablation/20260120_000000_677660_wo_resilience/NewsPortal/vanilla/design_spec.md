# NewsPortal Design Specification

## Section 1: Flask Routes Specification

| Route Path | Flask Function Name | HTTP Method | Template | Context Variables | Form Data (POST) |
|------------|---------------------|-------------|----------|-------------------|------------------|
| / | root_redirect | GET | N/A (redirect) | None | None |
| /dashboard | dashboard | GET | dashboard.html | featured_articles (list of dict), trending_articles (list of dict) | None |
| /catalog | article_catalog | GET | article_catalog.html | articles (list of dict), categories (list of dict), selected_category (str or None), search_query (str or None) | None |
| /article/<int:article_id> | article_details | GET | article_details.html | article (dict), is_bookmarked (bool) | None |
| /article/<int:article_id>/bookmark | bookmark_article | POST | N/A (redirect) | None | bookmark action (no extra fields, action triggered by POST) |
| /bookmarks | bookmarks | GET | bookmarks.html | bookmarks (list of dict) | None |
| /bookmarks/<int:bookmark_id>/remove | remove_bookmark | POST | N/A (redirect) | None | removal action (no extra fields, action triggered by POST) |
| /comments | comments_page | GET | comments.html | comments (list of dict), articles (list of dict), selected_article_id (int or None) | None |
| /comments/write | write_comment | GET, POST | write_comment.html | articles (list of dict) | commenter_name (str), comment_text (str), article_id (int) for POST |
| /trending | trending_articles | GET | trending.html | trending_list (list of dict), time_period (str) | None |
| /category/<string:category_name> | category_articles | GET | category.html | category_name (str), articles (list of dict) | None |
| /search | search_results | GET | search_results.html | search_query (str), results (list of dict) | None |

**Details per route:**

- **/**
  - Redirect to `/dashboard`

- **/dashboard**
  - Shows featured articles and trending articles summary
  - Context variables:
    - `featured_articles`: List of articles to feature (each dict with keys: article_id(int), title(str), author(str), date(str))
    - `trending_articles`: List of trending articles summary (dict with article_id(int), title(str), category(str), view_count(int))

- **/catalog**
  - Shows all articles
  - Supports optional query parameters for search and category filtering
  - Context variables:
    - `articles`: List of article dicts with keys: article_id(int), title(str), author(str), date(str), category(str)
    - `categories`: List of categories dicts with keys: category_id(int), category_name(str), description(str)
    - `selected_category`: str or None - category filter applied
    - `search_query`: str or None - current search term

- **/article/<int:article_id>**
  - Shows article details
  - Context variables:
    - `article`: dict with keys: article_id(int), title(str), author(str), category(str), content(str), date(str), views(int)
    - `is_bookmarked`: bool indicating if this article is bookmarked

- **/article/<int:article_id>/bookmark**
  - POST to bookmark the article
  - No template, redirects back to article details
  - Expects no form data other than POST trigger

- **/bookmarks**
  - Lists all bookmarked articles
  - Context variables:
    - `bookmarks`: list of dicts with keys: bookmark_id(int), article_id(int), article_title(str), bookmarked_date(str)

- **/bookmarks/<int:bookmark_id>/remove**
  - POST to remove a bookmark
  - No template, redirects back to bookmarks page
  - No form data except POST trigger

- **/comments**
  - Displays all comments
  - Context variables:
    - `comments`: list of dicts with keys: comment_id(int), article_id(int), article_title(str), commenter_name(str), comment_text(str), comment_date(str)
    - `articles`: list of dicts for filtering with keys: article_id(int), title(str)
    - `selected_article_id`: int or None

- **/comments/write**
  - GET shows form to write comment
  - POST to submit comment
  - Context variables for GET:
    - `articles`: list of dicts with keys: article_id(int), title(str)
  - POST form data:
    - `article_id` (int)
    - `commenter_name` (str)
    - `comment_text` (str)

- **/trending**
  - Shows trending articles filtered by time period
  - Context variables:
    - `trending_list`: list of dicts with keys: article_id(int), article_title(str), category(str), view_count(int), period(str)
    - `time_period`: str (e.g., "Today", "This Week", "This Month")

- **/category/<string:category_name>**
  - Shows articles filtered by category
  - Context variables:
    - `category_name`: str
    - `articles`: list of dicts with keys: article_id(int), title(str), author(str), date(str), views(int)

- **/search**
  - Shows search results
  - Context variables:
    - `search_query`: str
    - `results`: list of dicts with keys: article_id(int), title(str), excerpt(str)

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- File path: templates/dashboard.html
- Page title (in <title> and <h1>): News Portal
- Element IDs:
  - dashboard-page (Div): Container for dashboard
  - featured-articles (Div): Featured article recommendations display
  - browse-articles-button (Button): Nav to Article Catalog
  - view-bookmarks-button (Button): Nav to Bookmarks page
  - trending-articles-button (Button): Nav to Trending Articles page
- Context variables:
  - featured_articles (list of dict): Each dict: article_id(int), title(str), author(str), date(str)
  - trending_articles (list of dict): Each dict: article_id(int), title(str), category(str), view_count(int)
- Navigation mappings:
  - browse-articles-button: url_for('article_catalog')
  - view-bookmarks-button: url_for('bookmarks')
  - trending-articles-button: url_for('trending_articles')
- Template usage:
  - Loop over featured_articles to display summaries
  - Loop over trending_articles for trending section

---

### 2. article_catalog.html
- File path: templates/article_catalog.html
- Page title: Article Catalog
- Element IDs:
  - catalog-page (Div): Container for catalog
  - search-input (Input): Search field for title/author/keywords
  - category-filter (Dropdown): Filter by category
  - articles-grid (Div): Grid of article cards
  - view-article-button-{article_id} (Button): Button to view article details
- Context variables:
  - articles (list of dict): article_id(int), title(str), author(str), date(str), category(str)
  - categories (list of dict): category_id(int), category_name(str), description(str)
  - selected_category (str or None)
  - search_query (str or None)
- Navigation:
  - view-article-button-{article_id}: url_for('article_details', article_id=article_id)
- Template usage:
  - Dropdown populated from categories list
  - Articles displayed filtered by search and category

---

### 3. article_details.html
- File path: templates/article_details.html
- Page title: Article Details
- Element IDs:
  - article-details-page (Div): Container
  - article-title (H1): Article title
  - article-author (Div): Article author
  - article-date (Div): Publication date
  - bookmark-button (Button): Bookmark the article
  - article-content (Div): Full article content
- Context variables:
  - article (dict): article_id(int), title(str), author(str), category(str), content(str), date(str), views(int)
  - is_bookmarked (bool)
- Navigation:
  - bookmark-button: posts to url_for('bookmark_article', article_id=article['article_id'])

---

### 4. bookmarks.html
- File path: templates/bookmarks.html
- Page title: My Bookmarks
- Element IDs:
  - bookmarks-page (Div): Container
  - bookmarks-list (Div): Display list of bookmarks
  - remove-bookmark-button-{bookmark_id} (Button): Remove bookmark
  - read-bookmark-button-{bookmark_id} (Button): Read bookmarked article
  - back-to-dashboard (Button): Nav to Dashboard
- Context variables:
  - bookmarks (list of dict): bookmark_id(int), article_id(int), article_title(str), bookmarked_date(str)
- Navigation:
  - remove-bookmark-button-{bookmark_id}: posts to url_for('remove_bookmark', bookmark_id=bookmark_id)
  - read-bookmark-button-{bookmark_id}: url_for('article_details', article_id=article_id)
  - back-to-dashboard: url_for('dashboard')

---

### 5. comments.html
- File path: templates/comments.html
- Page title: Article Comments
- Element IDs:
  - comments-page (Div): Container
  - comments-list (Div): List of comments
  - write-comment-button (Button): Nav to write comment page
  - filter-by-article (Dropdown): Filter comments by article
  - back-to-dashboard (Button): Nav to dashboard
- Context variables:
  - comments (list of dict): comment_id(int), article_id(int), article_title(str), commenter_name(str), comment_text(str), comment_date(str)
  - articles (list of dict): article_id(int), title(str)
  - selected_article_id (int or None)
- Navigation:
  - write-comment-button: url_for('write_comment')
  - back-to-dashboard: url_for('dashboard')

---

### 6. write_comment.html
- File path: templates/write_comment.html
- Page title: Write a Comment
- Element IDs:
  - write-comment-page (Div): Container
  - select-article (Dropdown): Select article to comment
  - commenter-name (Input): Commenter name text input
  - comment-text (Textarea): Comment body text
  - submit-comment-button (Button): Submit form
- Context variables:
  - articles (list of dict): article_id(int), title(str)
- Navigation:
  - Form posts to url_for('write_comment') with method POST

---

### 7. trending.html
- File path: templates/trending.html
- Page title: Trending Articles
- Element IDs:
  - trending-page (Div): Container
  - trending-list (Div): Ranked list of trending articles
  - time-period-filter (Dropdown): Filter by time period
  - view-article-button-{article_id} (Button): View article details
  - back-to-dashboard (Button): Nav to dashboard
- Context variables:
  - trending_list (list of dict): article_id(int), article_title(str), category(str), view_count(int), period(str)
  - time_period (str)
- Navigation:
  - view-article-button-{article_id}: url_for('article_details', article_id=article_id)
  - back-to-dashboard: url_for('dashboard')

---

### 8. category.html
- File path: templates/category.html
- Page title: Category Articles
- Element IDs:
  - category-page (Div): Container
  - category-title (H1): Display category
  - category-articles (Div): List of articles
  - sort-by-date (Button): Sort articles by date
  - sort-by-popularity (Button): Sort articles by popularity
  - back-to-dashboard (Button): Nav back to dashboard
- Context variables:
  - category_name (str)
  - articles (list of dict): article_id(int), title(str), author(str), date(str), views(int)
- Navigation:
  - sort-by-date: link or button triggering sorting
  - sort-by-popularity: link or button triggering sorting
  - back-to-dashboard: url_for('dashboard')

---

### 9. search_results.html
- File path: templates/search_results.html
- Page title: Search Results
- Element IDs:
  - search-results-page (Div): Container
  - search-query-display (Div): Shows search query
  - results-list (Div): List search results
  - no-results-message (Div): Displayed if no results found
  - back-to-dashboard (Button): Nav to dashboard
- Context variables:
  - search_query (str)
  - results (list of dict): article_id(int), title(str), excerpt(str)
- Navigation:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. Articles Data
- File path: data/articles.txt
- Format: pipe-delimited `article_id|title|author|category|content|date|views`
- Description: Stores all news articles with metadata and content
- Example rows:
  - `1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432`
  - `2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210`
  - `3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891`

### 2. Categories Data
- File path: data/categories.txt
- Format: pipe-delimited `category_id|category_name|description`
- Description: Lists all categories available in the portal
- Example rows:
  - `1|Technology|Latest tech news and innovations`
  - `2|Sports|Sports news and event coverage`
  - `3|Business|Business and finance news`

### 3. Bookmarks Data
- File path: data/bookmarks.txt
- Format: pipe-delimited `bookmark_id|article_id|article_title|bookmarked_date`
- Description: Stores user bookmarks of articles
- Example rows:
  - `1|1|Breaking: New Technology Breakthrough|2025-01-20`
  - `2|3|Business: Market Trends Analysis|2025-01-18`

### 4. Comments Data
- File path: data/comments.txt
- Format: pipe-delimited `comment_id|article_id|article_title|commenter_name|comment_text|comment_date`
- Description: Stores comments made on articles
- Example rows:
  - `1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20`
  - `2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19`

### 5. Trending Data
- File path: data/trending.txt
- Format: pipe-delimited `article_id|article_title|category|view_count|period`
- Description: Stores trending articles data by period
- Example rows:
  - `1|Breaking: New Technology Breakthrough|Technology|5432|This Week`
  - `2|Sports: Championship Victory|Sports|3210|This Week`
  - `3|Business: Market Trends Analysis|Business|2891|This Month`


---

This completes the NewsPortal design specification for independent backend and frontend development.