# NewsPortal Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                     | Flask Function Name           | HTTP Method | Template File               | Context Variables                                                                                              | Form Data (POST)                        |
|-------------------------------|------------------------------|-------------|-----------------------------|---------------------------------------------------------------------------------------------------------------|---------------------------------------|
| `/`                           | root_redirect                 | GET         | N/A (redirect)              | None                                                                                                          | None                                  |
| `/dashboard`                  | dashboard_page                | GET         | dashboard.html              | featured_articles: list of dicts (article data), trending_articles: list of dicts (article data)              | None                                  |
| `/catalog`                   | article_catalog               | GET         | catalog.html                | articles: list of dicts (article_id:int, title:str, author:str, category:str, date:str),
|                                           | None                                  |
|                               |                              |             |                             | categories: list of dicts (category_id:int, category_name:str)                                                 |                                       |
| `/catalog/search`             | catalog_search_results        | POST        | search_results.html         | query: str, results: list of dicts (article_id:int, title:str, excerpt:str)                                   | search_query:str                       |
| `/catalog/category/<string:category_name>` | category_page              | GET         | category.html               | category_name: str, category_articles: list of dicts (article_id:int, title:str, date:str, popularity:int)    | None                                  |
| `/article/<int:article_id>`   | article_details              | GET         | article_details.html        | article: dict (article_id:int, title:str, author:str, date:str, content:str)                                  | None                                  |
| `/article/<int:article_id>/bookmark` | bookmark_article              | POST        | N/A (redirect to article_details) | None                                                                                                         | None (adds bookmark)                  |
| `/bookmarks`                 | bookmarks_page                | GET         | bookmarks.html              | bookmarks: list of dicts (bookmark_id:int, article_id:int, article_title:str, bookmarked_date:str)             | None                                  |
| `/bookmarks/remove/<int:bookmark_id>` | remove_bookmark              | POST        | N/A (redirect to bookmarks) | None                                                                                                         | None (remove specified bookmark)      |
| `/comments`                  | comments_page                 | GET         | comments.html               | comments: list of dicts (comment_id:int, article_id:int, article_title:str, commenter_name:str, comment_text:str),
|                               |             |                             | articles: list of dicts (article_id:int, title:str)                                                           | None                                  |
| `/comments/write`             | write_comment_page            | GET         | write_comment.html          | articles: list of dicts (article_id:int, title:str)                                                           | None                                  |
| `/comments/submit`            | submit_comment                | POST        | N/A (redirect to comments) | None                                                                                                          | article_id:int, commenter_name:str, comment_text:str |
| `/trending`                  | trending_articles_page        | GET         | trending.html               | trending: list of dicts (article_id:int, title:str, category:str, view_count:int, period:str)                  | None                                  |
| `/trending/filter`            | filter_trending_by_period     | POST        | trending.html               | trending_filtered: list of dicts (article_id:int, title:str, category:str, view_count:int, period:str)         | time_period:str                       |
| `/search`                   | search_results_page           | GET         | search_results.html         | query: str, results: list of dicts (article_id:int, title:str, excerpt:str)                                   | None                                  |

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- File Path: `templates/dashboard.html`
- Page Title: "News Portal" (used in `<title>` and `<h1>`)
- Element IDs:
  - `dashboard-page`: Div container for the dashboard page
  - `featured-articles`: Div to display featured article recommendations
  - `browse-articles-button`: Button to navigate to article catalog page
  - `view-bookmarks-button`: Button to navigate to bookmarks page
  - `trending-articles-button`: Button to navigate to trending articles page
- Context Variables:
  - `featured_articles`: List of dicts with article info (article_id:int, title:str, summary:str)
  - `trending_articles`: List of dicts with trending article info (article_id:int, title:str, category:str, view_count:int)
- Navigation:
  - `browse-articles-button` -> `url_for('article_catalog')`
  - `view-bookmarks-button` -> `url_for('bookmarks_page')`
  - `trending-articles-button` -> `url_for('trending_articles_page')`

### 2. Article Catalog Page
- File Path: `templates/catalog.html`
- Page Title: "Article Catalog"
- Element IDs:
  - `catalog-page`: Div container
  - `search-input`: Input field for search
  - `category-filter`: Dropdown for category filtering
  - `articles-grid`: Div grid showing article cards
  - `view-article-button-{article_id}`: Button on each article card to view details
- Context Variables:
  - `articles`: List of dicts
    - Fields: article_id:int, title:str, author:str, category:str, date:str
  - `categories`: List of dicts
    - Fields: category_id:int, category_name:str
- Navigation:
  - On category selection: navigates to `url_for('category_page', category_name=selected_category_name)`
  - On clicking `view-article-button-{article_id}` -> `url_for('article_details', article_id=article_id)`

### 3. Article Details Page
- File Path: `templates/article_details.html`
- Page Title: "Article Details"
- Element IDs:
  - `article-details-page`: Div container
  - `article-title`: H1 for article title
  - `article-author`: Div for author display
  - `article-date`: Div for publication date
  - `bookmark-button`: Button to bookmark the article
  - `article-content`: Div containing full article content
- Context Variables:
  - `article`: Dict with fields article_id:int, title:str, author:str, content:str, date:str
- Navigation:
  - `bookmark-button` triggers POST to `url_for('bookmark_article', article_id=article.article_id)`

### 4. Bookmarks Page
- File Path: `templates/bookmarks.html`
- Page Title: "My Bookmarks"
- Element IDs:
  - `bookmarks-page`: Div container
  - `bookmarks-list`: Div with all bookmarked articles
  - `remove-bookmark-button-{bookmark_id}`: Button to remove bookmark
  - `read-bookmark-button-{bookmark_id}`: Button to read bookmarked article
  - `back-to-dashboard`: Button to return to dashboard
- Context Variables:
  - `bookmarks`: List of dicts with bookmark_id:int, article_id:int, article_title:str, bookmarked_date:str
- Navigation:
  - `remove-bookmark-button-{bookmark_id}` triggers POST to `url_for('remove_bookmark', bookmark_id=bookmark_id)`
  - `read-bookmark-button-{bookmark_id}` navigates to `url_for('article_details', article_id=article_id)`
  - `back-to-dashboard` -> `url_for('dashboard_page')`

### 5. Comments Page
- File Path: `templates/comments.html`
- Page Title: "Article Comments"
- Element IDs:
  - `comments-page`: Div container
  - `comments-list`: Div listing comments
  - `write-comment-button`: Button to go to write comment page
  - `filter-by-article`: Dropdown to filter comments by article
  - `back-to-dashboard`: Button to return to dashboard
- Context Variables:
  - `comments`: List of dicts with comment_id:int, article_id:int, article_title:str, commenter_name:str, comment_text:str
  - `articles`: List of dicts with article_id:int, title:str for filter dropdown
- Navigation:
  - `write-comment-button` -> `url_for('write_comment_page')`
  - `back-to-dashboard` -> `url_for('dashboard_page')`

### 6. Write Comment Page
- File Path: `templates/write_comment.html`
- Page Title: "Write a Comment"
- Element IDs:
  - `write-comment-page`: Div container
  - `select-article`: Dropdown to select article
  - `commenter-name`: Input for commenter name
  - `comment-text`: Textarea for comment content
  - `submit-comment-button`: Button to submit comment
- Context Variables:
  - `articles`: List of dicts with article_id:int, title:str for dropdown
- Navigation:
  - Form submission posts to `url_for('submit_comment')`

### 7. Trending Articles Page
- File Path: `templates/trending.html`
- Page Title: "Trending Articles"
- Element IDs:
  - `trending-page`: Div container
  - `trending-list`: Div with ranked trending articles
  - `time-period-filter`: Dropdown to select time period
  - `view-article-button-{article_id}`: Button to view article details
  - `back-to-dashboard`: Button to return dashboard
- Context Variables:
  - `trending`: List of dicts with article_id:int, title:str, category:str, view_count:int, period:str
- Navigation:
  - `time-period-filter` posts filter to `url_for('filter_trending_by_period')`
  - `view-article-button-{article_id}` -> `url_for('article_details', article_id=article_id)`
  - `back-to-dashboard` -> `url_for('dashboard_page')`

### 8. Category Page
- File Path: `templates/category.html`
- Page Title: "Category Articles"
- Element IDs:
  - `category-page`: Div container
  - `category-title`: H1 for category name
  - `category-articles`: Div listing articles in category
  - `sort-by-date`: Button to sort by date
  - `sort-by-popularity`: Button to sort by popularity
  - `back-to-dashboard`: Button to return dashboard
- Context Variables:
  - `category_name`: str
  - `category_articles`: List of dicts with article_id:int, title:str, date:str, popularity:int
- Navigation:
  - Clicking sort buttons triggers respective sorting on page (could be client-side or server-side implementation)
  - `back-to-dashboard` -> `url_for('dashboard_page')`

### 9. Search Results Page
- File Path: `templates/search_results.html`
- Page Title: "Search Results"
- Element IDs:
  - `search-results-page`: Div container
  - `search-query-display`: Div showing user search query
  - `results-list`: Div listing matched articles
  - `no-results-message`: Div showing no results message (rendered conditionally)
  - `back-to-dashboard`: Button to return dashboard
- Context Variables:
  - `query`: str
  - `results`: List of dicts with article_id:int, title:str, excerpt:str
- Navigation:
  - `back-to-dashboard` -> `url_for('dashboard_page')`

---

## Section 3: Data File Schemas

### 1. Articles Data
- File Path: `data/articles.txt`
- Format: pipe-delimited (`|`), no header row
- Fields in order:
  1. `article_id` (int)
  2. `title` (str)
  3. `author` (str)
  4. `category` (str)
  5. `content` (str)
  6. `date` (str, format YYYY-MM-DD)
  7. `views` (int)
- Data Description: Stores news articles with all core details including reading content and view counts.
- Example rows:
  ```
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891
  ```

### 2. Categories Data
- File Path: `data/categories.txt`
- Format: pipe-delimited (`|`), no header row
- Fields in order:
  1. `category_id` (int)
  2. `category_name` (str)
  3. `description` (str)
- Data Description: Contains list of category identifiers, names, and descriptions.
- Example rows:
  ```
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news
  ```

### 3. Bookmarks Data
- File Path: `data/bookmarks.txt`
- Format: pipe-delimited (`|`), no header row
- Fields in order:
  1. `bookmark_id` (int)
  2. `article_id` (int)
  3. `article_title` (str)
  4. `bookmarked_date` (str, format YYYY-MM-DD)
- Data Description: Stores user bookmarks (no user accounts, so global bookmarks).
- Example rows:
  ```
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18
  ```

### 4. Comments Data
- File Path: `data/comments.txt`
- Format: pipe-delimited (`|`), no header row
- Fields in order:
  1. `comment_id` (int)
  2. `article_id` (int)
  3. `article_title` (str)
  4. `commenter_name` (str)
  5. `comment_text` (str)
  6. `comment_date` (str, format YYYY-MM-DD)
- Data Description: Contains comments on articles with commenter info and text.
- Example rows:
  ```
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19
  ```

### 5. Trending Data
- File Path: `data/trending.txt`
- Format: pipe-delimited (`|`), no header row
- Fields in order:
  1. `article_id` (int)
  2. `article_title` (str)
  3. `category` (str)
  4. `view_count` (int)
  5. `period` (str: e.g., "Today", "This Week", "This Month")
- Data Description: Contains trending articles by view counts and periods.
- Example rows:
  ```
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month
  ```
