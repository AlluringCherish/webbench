# Design Specification for NewsPortal Web Application

---

## 1. Flask Routes Specification

| Route Path                     | Flask Function Name         | HTTP Methods | Template Filename           | Context Variables (Name: Type)                                                                        | Notes                                                                                     |
|-------------------------------|-----------------------------|--------------|-----------------------------|-----------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| `/`                           | root_redirect               | GET          | None                        | None                                                                                                | Redirects to dashboard page `/dashboard`                                                  |
| `/dashboard`                  | dashboard_page             | GET          | dashboard.html              | featured_articles: list[dict], trending_articles: list[dict]                                     | None                                                                                      |
| `/catalog`                   | article_catalog_page        | GET          | catalog.html                | articles: list[dict], categories: list[dict]                                                     | Accepts query parameters for search and category filtering                              |
| `/article/<int:article_id>`  | article_details_page        | GET          | article_details.html        | article: dict, is_bookmarked: bool                                                               | None                                                                                      |
| `/article/<int:article_id>/bookmark` | bookmark_article         | POST         | None                        | None                                                                                                | Form data: None. Bookmark article identified by article_id                                |
| `/bookmarks`                 | bookmarks_page              | GET          | bookmarks.html              | bookmarks: list[dict]                                                                            | None                                                                                      |
| `/bookmarks/<int:bookmark_id>/remove` | remove_bookmark          | POST         | None                        | None                                                                                                | Form data: None. Remove bookmark by bookmark_id                                          |
| `/comments`                  | comments_page               | GET          | comments.html               | comments: list[dict], articles: list[dict], selected_article_id: int or None                       | Optional filter by article ID as query parameter                                        |
| `/comments/write`            | write_comment_page          | GET          | write_comment.html          | articles: list[dict]                                                                             | None                                                                                      |
| `/comments/submit`           | submit_comment              | POST         | None                        | None                                                                                                | Form data: commenter_name (str), comment_text (str), article_id (int)                     |
| `/trending`                  | trending_articles_page      | GET          | trending.html               | trending_articles: list[dict], time_period: str                                                   | Optional query parameter for time_period filter                                         |
| `/category/<string:category_name>` | category_page             | GET          | category.html               | category_name: str, articles: list[dict]                                                        | None                                                                                      |
| `/search`                   | search_results_page         | GET          | search_results.html         | query: str, results: list[dict]                                                                 | Query parameter `q` for search query input                                               |

---

## 2. HTML Template Specifications

### 2.1 dashboard.html
- File path: `templates/dashboard.html`
- Page Title (for `<title>` and `<h1>`): "News Portal"
- Element IDs:
  - `dashboard-page`: Div - Container for the dashboard page
  - `featured-articles`: Div - Display of featured article recommendations
  - `browse-articles-button`: Button - Navigate to article catalog page
  - `view-bookmarks-button`: Button - Navigate to bookmarks page
  - `trending-articles-button`: Button - Navigate to trending articles page
- Context variables:
  - `featured_articles`: list of dicts, each with at least keys `article_id` (int), `title` (str), `author` (str), `date` (str)
  - `trending_articles`: list of dicts as above
- Navigation mappings:
  - `browse-articles-button` -> `url_for('article_catalog_page')`
  - `view-bookmarks-button` -> `url_for('bookmarks_page')`
  - `trending-articles-button` -> `url_for('trending_articles_page')`

### 2.2 catalog.html
- File path: `templates/catalog.html`
- Page Title: "Article Catalog"
- Element IDs:
  - `catalog-page`: Div - Container for catalog page
  - `search-input`: Input - Search box for articles
  - `category-filter`: Dropdown - Filter articles by category
  - `articles-grid`: Div - Displays article cards
  - `view-article-button-{article_id}`: Button - View article details for each article
- Context variables:
  - `articles`: list of dicts with keys `article_id` (int), `title` (str), `author` (str), `date` (str), and possibly `thumbnail` (str)
  - `categories`: list of dicts with `category_id` (int), `category_name` (str)
- Navigation mappings:
  - Each `view-article-button-{article_id}` -> `url_for('article_details_page', article_id=article_id)`

### 2.3 article_details.html
- File path: `templates/article_details.html`
- Page Title: "Article Details"
- Element IDs:
  - `article-details-page`: Div
  - `article-title`: H1
  - `article-author`: Div
  - `article-date`: Div
  - `bookmark-button`: Button
  - `article-content`: Div
- Context variables:
  - `article`: dict with fields `article_id` (int), `title` (str), `author` (str), `date` (str), `content` (str)
  - `is_bookmarked`: bool
- Navigation mappings:
  - `bookmark-button`: Submits POST to `url_for('bookmark_article', article_id=article['article_id'])`

### 2.4 bookmarks.html
- File path: `templates/bookmarks.html`
- Page Title: "My Bookmarks"
- Element IDs:
  - `bookmarks-page`: Div
  - `bookmarks-list`: Div
  - `remove-bookmark-button-{bookmark_id}`: Button for each bookmark
  - `read-bookmark-button-{bookmark_id}`: Button for each bookmark
  - `back-to-dashboard`: Button
- Context variables:
  - `bookmarks`: list of dicts with keys `bookmark_id` (int), `article_id` (int), `article_title` (str), `bookmarked_date` (str)
- Navigation mappings:
  - `remove-bookmark-button-{bookmark_id}`: POST to `url_for('remove_bookmark', bookmark_id=bookmark_id)`
  - `read-bookmark-button-{bookmark_id}`: `url_for('article_details_page', article_id=article_id)`
  - `back-to-dashboard`: `url_for('dashboard_page')`

### 2.5 comments.html
- File path: `templates/comments.html`
- Page Title: "Article Comments"
- Element IDs:
  - `comments-page`: Div
  - `comments-list`: Div
  - `write-comment-button`: Button
  - `filter-by-article`: Dropdown
  - `back-to-dashboard`: Button
- Context variables:
  - `comments`: list of dicts with fields `comment_id` (int), `article_title` (str), `commenter_name` (str), `comment_text` (str)
  - `articles`: list of dicts to populate `filter-by-article` dropdown
  - `selected_article_id`: int or None
- Navigation mappings:
  - `write-comment-button`: `url_for('write_comment_page')`
  - `back-to-dashboard`: `url_for('dashboard_page')`

### 2.6 write_comment.html
- File path: `templates/write_comment.html`
- Page Title: "Write a Comment"
- Element IDs:
  - `write-comment-page`: Div
  - `select-article`: Dropdown
  - `commenter-name`: Input
  - `comment-text`: Textarea
  - `submit-comment-button`: Button
- Context variables:
  - `articles`: list of dicts with `article_id` (int), `title` (str)
- Navigation mappings:
  - Form submission POST to `url_for('submit_comment')`

### 2.7 trending.html
- File path: `templates/trending.html`
- Page Title: "Trending Articles"
- Element IDs:
  - `trending-page`: Div
  - `trending-list`: Div
  - `time-period-filter`: Dropdown
  - `view-article-button-{article_id}`: Button
  - `back-to-dashboard`: Button
- Context variables:
  - `trending_articles`: list of dicts with `article_id` (int), `article_title` (str), `category` (str), `view_count` (int)
  - `time_period`: str
- Navigation mappings:
  - Each `view-article-button-{article_id}`: `url_for('article_details_page', article_id=article_id)`
  - `back-to-dashboard`: `url_for('dashboard_page')`

### 2.8 category.html
- File path: `templates/category.html`
- Page Title: "Category Articles"
- Element IDs:
  - `category-page`: Div
  - `category-title`: H1
  - `category-articles`: Div
  - `sort-by-date`: Button
  - `sort-by-popularity`: Button
  - `back-to-dashboard`: Button
- Context variables:
  - `category_name`: str
  - `articles`: list of dicts with `article_id` (int), `title` (str), `date` (str), `popularity` (int)
- Navigation mappings:
  - `sort-by-date`: triggers sorting (implementation detail)
  - `sort-by-popularity`: triggers sorting
  - `back-to-dashboard`: `url_for('dashboard_page')`

### 2.9 search_results.html
- File path: `templates/search_results.html`
- Page Title: "Search Results"
- Element IDs:
  - `search-results-page`: Div
  - `search-query-display`: Div
  - `results-list`: Div
  - `no-results-message`: Div
  - `back-to-dashboard`: Button
- Context variables:
  - `query`: str
  - `results`: list of dicts with `article_id` (int), `title` (str), `excerpt` (str)
- Navigation mappings:
  - `back-to-dashboard`: `url_for('dashboard_page')`

---

## 3. Data File Schemas

### 3.1 articles.txt
- Filename: `articles.txt`
- Fields (pipe-delimited):
  1. article_id (int)
  2. title (str)
  3. author (str)
  4. category (str)
  5. content (str)
  6. date (str, YYYY-MM-DD)
  7. views (int)
- Description: Contains all news articles with metadata and content.
- Example rows:
  ```
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891
  ```

### 3.2 categories.txt
- Filename: `categories.txt`
- Fields (pipe-delimited):
  1. category_id (int)
  2. category_name (str)
  3. description (str)
- Description: Lists all article categories.
- Example rows:
  ```
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news
  ```

### 3.3 bookmarks.txt
- Filename: `bookmarks.txt`
- Fields (pipe-delimited):
  1. bookmark_id (int)
  2. article_id (int)
  3. article_title (str)
  4. bookmarked_date (str, YYYY-MM-DD)
- Description: Stores user bookmarked articles.
- Example rows:
  ```
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18
  ```

### 3.4 comments.txt
- Filename: `comments.txt`
- Fields (pipe-delimited):
  1. comment_id (int)
  2. article_id (int)
  3. article_title (str)
  4. commenter_name (str)
  5. comment_text (str)
  6. comment_date (str, YYYY-MM-DD)
- Description: Contains comments on articles.
- Example rows:
  ```
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19
  ```

### 3.5 trending.txt
- Filename: `trending.txt`
- Fields (pipe-delimited):
  1. article_id (int)
  2. article_title (str)
  3. category (str)
  4. view_count (int)
  5. period (str)
- Description: Tracks trending article data by period.
- Example rows:
  ```
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month
  ```

---

**End of design_spec.md**
