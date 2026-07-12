# NewsPortal Design Specification

## Section 1: Flask Routes Specification

| Route Path | Flask Function Name | HTTP Method | Template | Context Variables | Form Data (POST) |
|------------|---------------------|-------------|----------|-------------------|------------------|
| / | root_redirect | GET | N/A (redirect) | None | None |
| /dashboard | dashboard | GET | dashboard.html | featured_articles (list of dict), trending_articles (list of dict) | None |
| /catalog | article_catalog | GET | article_catalog.html | articles (list of dict), categories (list of dict), search_query (str or None), selected_category (str or None) | None |
| /article/<int:article_id> | article_details | GET | article_details.html | article (dict), is_bookmarked (bool) | None |
| /article/<int:article_id>/bookmark | bookmark_article | POST | N/A (redirect) | None | None (form submission via POST, no fields expected) |
| /bookmarks | bookmarks | GET | bookmarks.html | bookmarks (list of dict) | None |
| /bookmarks/<int:bookmark_id>/remove | remove_bookmark | POST | N/A (redirect) | None | None (form submission via POST, no fields expected) |
| /comments | comments | GET | comments.html | comments (list of dict), articles (list of dict), selected_article_id (int or None) | None |
| /comments/write | write_comment | GET | write_comment.html | articles (list of dict) | None |
| /comments/write | submit_comment | POST | N/A (redirect) | None | select_article (int), commenter_name (str), comment_text (str) |
| /trending | trending_articles | GET | trending.html | trending_list (list of dict), time_period (str or None) | None |
| /category/<category_name> | category_page | GET | category.html | category_name (str), articles (list of dict) | None |
| /search | search_results | GET | search_results.html | query (str), results (list of dict) | None |

### Notes:
- Root route `/` redirects to `/dashboard`.
- POST routes handle form submissions or actions (like bookmarking, removing bookmarks, submitting comments).
- All GET routes render templates with specified context variables.

---

## Section 2: HTML Template Specifications

---

### 1. dashboard.html
- File Path: templates/dashboard.html
- Page Title: "News Portal"
- Elements:
  - ID: dashboard-page (Div) - Container for the dashboard page.
  - ID: featured-articles (Div) - Display of featured article recommendations.
  - ID: browse-articles-button (Button) - Navigates to article catalog page.
  - ID: view-bookmarks-button (Button) - Navigates to bookmarks page.
  - ID: trending-articles-button (Button) - Navigates to trending articles page.
- Context Variables:
  - featured_articles: list of dict with keys: article_id (int), title (str), author (str), date (str), excerpt (str)
  - trending_articles: list of dict with keys: article_id (int), title (str), category (str), view_count (int)
- Navigation Mappings:
  - browse-articles-button: url_for('article_catalog')
  - view-bookmarks-button: url_for('bookmarks')
  - trending-articles-button: url_for('trending_articles')

---

### 2. article_catalog.html
- File Path: templates/article_catalog.html
- Page Title: "Article Catalog"
- Elements:
  - ID: catalog-page (Div) - Container for the catalog page.
  - ID: search-input (Input) - Field to search articles by title, author, or keywords.
  - ID: category-filter (Dropdown) - Dropdown to filter by category.
  - ID: articles-grid (Div) - Grid displaying article cards.
  - ID Pattern: view-article-button-{article_id} (Button) - View article details.
- Context Variables:
  - articles: list of dict with keys: article_id (int), title (str), author (str), date (str), thumbnail_url (str, optional)
  - categories: list of dict with keys: category_id (int), category_name (str)
  - search_query: str or None
  - selected_category: str or None
- Navigation Mappings:
  - view-article-button-{article_id}: url_for('article_details', article_id=article_id)

---

### 3. article_details.html
- File Path: templates/article_details.html
- Page Title: "Article Details"
- Elements:
  - ID: article-details-page (Div) - Container for the article details page.
  - ID: article-title (H1) - Article title.
  - ID: article-author (Div) - Article author.
  - ID: article-date (Div) - Article publication date.
  - ID: bookmark-button (Button) - Button to bookmark/unbookmark the article.
  - ID: article-content (Div) - Full article content.
- Context Variables:
  - article: dict with keys: article_id (int), title (str), author (str), date (str), content (str)
  - is_bookmarked: bool
- Navigation Mappings:
  - bookmark-button: POST form to url_for('bookmark_article', article_id=article['article_id'])

---

### 4. bookmarks.html
- File Path: templates/bookmarks.html
- Page Title: "My Bookmarks"
- Elements:
  - ID: bookmarks-page (Div) - Container for the bookmarks page.
  - ID: bookmarks-list (Div) - List of bookmarked articles.
  - ID Pattern: remove-bookmark-button-{bookmark_id} (Button) - Remove bookmark action.
  - ID Pattern: read-bookmark-button-{bookmark_id} (Button) - Read bookmarked article.
  - ID: back-to-dashboard (Button) - Navigation back to dashboard.
- Context Variables:
  - bookmarks: list of dict with keys: bookmark_id (int), article_id (int), article_title (str), bookmarked_date (str)
- Navigation Mappings:
  - remove-bookmark-button-{bookmark_id}: POST to url_for('remove_bookmark', bookmark_id=bookmark_id)
  - read-bookmark-button-{bookmark_id}: url_for('article_details', article_id=article_id)
  - back-to-dashboard: url_for('dashboard')

---

### 5. comments.html
- File Path: templates/comments.html
- Page Title: "Article Comments"
- Elements:
  - ID: comments-page (Div) - Container for comments page.
  - ID: comments-list (Div) - List of comments.
  - ID: write-comment-button (Button) - Navigate to write comment page.
  - ID: filter-by-article (Dropdown) - Filter comments by article.
  - ID: back-to-dashboard (Button) - Navigate back to dashboard.
- Context Variables:
  - comments: list of dict with keys: comment_id (int), article_id (int), article_title (str), commenter_name (str), comment_text (str), comment_date (str)
  - articles: list of dict with keys: article_id (int), title (str)
  - selected_article_id: int or None
- Navigation Mappings:
  - write-comment-button: url_for('write_comment')
  - back-to-dashboard: url_for('dashboard')

---

### 6. write_comment.html
- File Path: templates/write_comment.html
- Page Title: "Write a Comment"
- Elements:
  - ID: write-comment-page (Div) - Container for write comment page.
  - ID: select-article (Dropdown) - Select article to comment on.
  - ID: commenter-name (Input) - Input commenter name.
  - ID: comment-text (Textarea) - Write comment text.
  - ID: submit-comment-button (Button) - Submit comment.
- Context Variables:
  - articles: list of dict with keys: article_id (int), title (str)
- Navigation Mappings:
  - submit-comment-button: POST form submit to url_for('submit_comment')

---

### 7. trending.html
- File Path: templates/trending.html
- Page Title: "Trending Articles"
- Elements:
  - ID: trending-page (Div) - Container for trending articles page.
  - ID: trending-list (Div) - Ranked list of trending articles.
  - ID: time-period-filter (Dropdown) - Filter by time period.
  - ID Pattern: view-article-button-{article_id} (Button) - View article details.
  - ID: back-to-dashboard (Button) - Navigate back to dashboard.
- Context Variables:
  - trending_list: list of dict with keys: article_id (int), title (str), category (str), view_count (int), period (str)
  - time_period: str or None
- Navigation Mappings:
  - view-article-button-{article_id}: url_for('article_details', article_id=article_id)
  - back-to-dashboard: url_for('dashboard')

---

### 8. category.html
- File Path: templates/category.html
- Page Title: "Category Articles"
- Elements:
  - ID: category-page (Div) - Container for category page.
  - ID: category-title (H1) - Displays category name.
  - ID: category-articles (Div) - List of articles in category.
  - ID: sort-by-date (Button) - Sort articles by date.
  - ID: sort-by-popularity (Button) - Sort articles by popularity.
  - ID: back-to-dashboard (Button) - Navigate back to dashboard.
- Context Variables:
  - category_name: str
  - articles: list of dict with keys: article_id (int), title (str), author (str), date (str), views (int)
- Navigation Mappings:
  - sort-by-date: (client side or server side sorting, route unchanged)
  - sort-by-popularity: (client side or server side sorting, route unchanged)
  - back-to-dashboard: url_for('dashboard')

---

### 9. search_results.html
- File Path: templates/search_results.html
- Page Title: "Search Results"
- Elements:
  - ID: search-results-page (Div) - Container for search results page.
  - ID: search-query-display (Div) - Displays the search query.
  - ID: results-list (Div) - List of search results.
  - ID: no-results-message (Div) - Displayed if no results found.
  - ID: back-to-dashboard (Button) - Navigate back to dashboard.
- Context Variables:
  - query: str
  - results: list of dict with keys: article_id (int), title (str), excerpt (str)
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. data/articles.txt
- File Path: data/articles.txt
- Format: Pipe-delimited (|), no header
- Fields (in order):
  1. article_id (int)
  2. title (str)
  3. author (str)
  4. category (str)
  5. content (str)
  6. date (YYYY-MM-DD str)
  7. views (int)
- Description: Stores all articles with full content and metadata.
- Example Rows:
  ```
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891
  ```

---

### 2. data/categories.txt
- File Path: data/categories.txt
- Format: Pipe-delimited (|), no header
- Fields (in order):
  1. category_id (int)
  2. category_name (str)
  3. description (str)
- Description: Stores all article categories with descriptions.
- Example Rows:
  ```
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news
  ```

---

### 3. data/bookmarks.txt
- File Path: data/bookmarks.txt
- Format: Pipe-delimited (|), no header
- Fields (in order):
  1. bookmark_id (int)
  2. article_id (int)
  3. article_title (str)
  4. bookmarked_date (YYYY-MM-DD str)
- Description: Stores user bookmarked articles.
- Example Rows:
  ```
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18
  ```

---

### 4. data/comments.txt
- File Path: data/comments.txt
- Format: Pipe-delimited (|), no header
- Fields (in order):
  1. comment_id (int)
  2. article_id (int)
  3. article_title (str)
  4. commenter_name (str)
  5. comment_text (str)
  6. comment_date (YYYY-MM-DD str)
- Description: Stores comments made by users on articles.
- Example Rows:
  ```
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19
  ```

---

### 5. data/trending.txt
- File Path: data/trending.txt
- Format: Pipe-delimited (|), no header
- Fields (in order):
  1. article_id (int)
  2. article_title (str)
  3. category (str)
  4. view_count (int)
  5. period (str) - e.g. "Today", "This Week", "This Month"
- Description: Stores top trending articles by time period.
- Example Rows:
  ```
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month
  ```

---

# End of Design Specification
