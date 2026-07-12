# NewsPortal Application Design Specifications

---

## Section 1: Flask Routes Specification

| Route Path                    | Flask Function Name       | HTTP Method | Template File               | Context Variables (name:type)                                                                                         | Notes (form data)                                                      |
|-------------------------------|--------------------------|-------------|-----------------------------|-----------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|
| `/`                           | `root_redirect`           | GET         | None (redirect)              | None                                                                                                                  | Redirects to `/dashboard`                                            |
| `/dashboard`                  | `dashboard`               | GET         | `dashboard.html`             | `featured_articles` (list of dicts), `trending_articles_button_url` (str), `browse_articles_url` (str),  `view_bookmarks_url` (str),  `trending_articles_url` (str) | None                                                                 |
| `/catalog`                   | `article_catalog`          | GET         | `catalog.html`               | `articles` (list of dicts), `categories` (list of dicts)                                                              | None                                                                 |
| `/article/<int:article_id>`  | `article_details`          | GET         | `article_details.html`       | `article` (dict with fields: article_id:int, title:str, author:str, category:str, content:str, date:str, views:int)    | None                                                                 |
| `/article/<int:article_id>/bookmark` | `bookmark_article`       | POST        | Redirect to `/article/<article_id>` | None                                                                                                                  | Expects form data: none, handles bookmarking action                   |
| `/bookmarks`                 | `bookmarks`                | GET         | `bookmarks.html`             | `bookmarks` (list of dicts)                                                                                            | None                                                                 |
| `/bookmarks/<int:bookmark_id>/remove` | `remove_bookmark`        | POST        | Redirect to `/bookmarks`     | None                                                                                                                  | Expects form data: none, handles bookmark removal action              |
| `/comments`                  | `comments_page`            | GET         | `comments.html`              | `comments` (list of dicts), `articles` (list of dicts)                                                                 | None                                                                 |
| `/write-comment`             | `write_comment`            | GET         | `write_comment.html`         | `articles` (list of dicts)                                                                                             | None                                                                 |
| `/write-comment`             | `submit_comment`           | POST        | Redirect to `/comments`      | None                                                                                                                  | Form data: `select_article` (int), `commenter_name` (str), `comment_text` (str) |
| `/trending`                 | `trending_articles`        | GET         | `trending.html`              | `trending_articles` (list of dicts), `time_period` (str)                                                              | None                                                                 |
| `/category/<string:category_name>` | `category_articles`       | GET         | `category.html`              | `category_name` (str), `category_articles` (list of dicts)                                                             | None                                                                 |
| `/search`                   | `search_results`           | GET         | `search_results.html`        | `search_query` (str), `search_results` (list of dicts)                                                                 | Query param: `q` for search query                                    |

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- File path: `templates/dashboard.html`
- Page title: "News Portal"
- Page heading & title tag: "News Portal"
- Element IDs:
  - `dashboard-page`: Div, container for the dashboard page
  - `featured-articles`: Div, displays featured article recommendations
  - `browse-articles-button`: Button, navigates to article catalog page
  - `view-bookmarks-button`: Button, navigates to bookmarks page
  - `trending-articles-button`: Button, navigates to trending articles page
- Context variables:
  - `featured_articles`: List of dicts with article data (fields: article_id:int, title:str, author:str, date:str)
- Navigation mappings:
  - `browse-articles-button` -> `url_for('article_catalog')`
  - `view-bookmarks-button` -> `url_for('bookmarks')`
  - `trending-articles-button` -> `url_for('trending_articles')`

### 2. Article Catalog Page
- File path: `templates/catalog.html`
- Page title: "Article Catalog"
- Page heading & title tag: "Article Catalog"
- Element IDs:
  - `catalog-page`: Div, container for catalog page
  - `search-input`: Input, field for searching articles
  - `category-filter`: Dropdown, to filter by category
  - `articles-grid`: Div, grid displaying article cards
  - `view-article-button-{article_id}`: Button, each article's view details button
- Context variables:
  - `articles`: List of dicts (article_id:int, title:str, author:str, date:str, category:str)
  - `categories`: List of dicts (category_id:int, category_name:str, description:str)
- Navigation mappings:
  - Each `view-article-button-{article_id}` -> `url_for('article_details', article_id=article_id)`

### 3. Article Details Page
- File path: `templates/article_details.html`
- Page title: "Article Details"
- Page heading & title tag: "Article Details"
- Element IDs:
  - `article-details-page`: Div, container
  - `article-title`: H1, displays article title
  - `article-author`: Div, displays article author
  - `article-date`: Div, displays article date
  - `bookmark-button`: Button, bookmarks the article
  - `article-content`: Div, full article content
- Context variables:
  - `article`: Dict (article_id:int, title:str, author:str, category:str, content:str, date:str, views:int)
- Navigation mappings:
  - `bookmark-button` posts to `/article/<article_id>/bookmark` (form submission)

### 4. Bookmarks Page
- File path: `templates/bookmarks.html`
- Page title: "My Bookmarks"
- Page heading & title tag: "My Bookmarks"
- Element IDs:
  - `bookmarks-page`: Div, container
  - `bookmarks-list`: Div, list of bookmarked articles
  - `remove-bookmark-button-{bookmark_id}`: Button, remove bookmark
  - `read-bookmark-button-{bookmark_id}`: Button, read bookmarked article
  - `back-to-dashboard`: Button, back to dashboard
- Context variables:
  - `bookmarks`: List of dicts (bookmark_id:int, article_id:int, article_title:str, bookmarked_date:str)
- Navigation mappings:
  - Each `remove-bookmark-button-{bookmark_id}` posts to `/bookmarks/<bookmark_id>/remove`
  - Each `read-bookmark-button-{bookmark_id}` -> `url_for('article_details', article_id=article_id)`
  - `back-to-dashboard` -> `url_for('dashboard')`

### 5. Comments Page
- File path: `templates/comments.html`
- Page title: "Article Comments"
- Page heading & title tag: "Article Comments"
- Element IDs:
  - `comments-page`: Div, container
  - `comments-list`: Div, listing all comments
  - `write-comment-button`: Button, navigate to write comment page
  - `filter-by-article`: Dropdown, filter comments by article
  - `back-to-dashboard`: Button, back to dashboard
- Context variables:
  - `comments`: List of dicts (comment_id:int, article_id:int, article_title:str, commenter_name:str, comment_text:str, comment_date:str)
  - `articles`: List of dicts (article_id:int, title:str)
- Navigation mappings:
  - `write-comment-button` -> `url_for('write_comment')`
  - `back-to-dashboard` -> `url_for('dashboard')`

### 6. Write Comment Page
- File path: `templates/write_comment.html`
- Page title: "Write a Comment"
- Page heading & title tag: "Write a Comment"
- Element IDs:
  - `write-comment-page`: Div, container
  - `select-article`: Dropdown to select article
  - `commenter-name`: Input for commenter name
  - `comment-text`: Textarea for comment text
  - `submit-comment-button`: Button to submit
- Context variables:
  - `articles`: List of dicts (article_id:int, title:str)
- Navigation mappings:
  - Form submits POST to `/write-comment`

### 7. Trending Articles Page
- File path: `templates/trending.html`
- Page title: "Trending Articles"
- Page heading & title tag: "Trending Articles"
- Element IDs:
  - `trending-page`: Div, container
  - `trending-list`: Div, ranked trending articles
  - `time-period-filter`: Dropdown for time period
  - `view-article-button-{article_id}`: Button, view article details
  - `back-to-dashboard`: Button, back to dashboard
- Context variables:
  - `trending_articles`: List of dicts (article_id:int, article_title:str, category:str, view_count:int, period:str)
  - `time_period`: str
- Navigation mappings:
  - Each `view-article-button-{article_id}` -> `url_for('article_details', article_id=article_id)`
  - `back-to-dashboard` -> `url_for('dashboard')`

### 8. Category Page
- File path: `templates/category.html`
- Page title: "Category Articles"
- Page heading & title tag: "Category Articles"
- Element IDs:
  - `category-page`: Div, container
  - `category-title`: H1, category name
  - `category-articles`: Div, list of category articles
  - `sort-by-date`: Button, sort articles by date
  - `sort-by-popularity`: Button, sort articles by popularity
  - `back-to-dashboard`: Button, back to dashboard
- Context variables:
  - `category_name`: str
  - `category_articles`: List of dicts (article_id:int, title:str, author:str, date:str, views:int)
- Navigation mappings:
  - `sort-by-date` and `sort-by-popularity` trigger sorting with appropriate request params (backend)
  - `back-to-dashboard` -> `url_for('dashboard')`

### 9. Search Results Page
- File path: `templates/search_results.html`
- Page title: "Search Results"
- Page heading & title tag: "Search Results"
- Element IDs:
  - `search-results-page`: Div, container
  - `search-query-display`: Div, displays search query
  - `results-list`: Div, lists search results
  - `no-results-message`: Div, shows when no results found
  - `back-to-dashboard`: Button, back to dashboard
- Context variables:
  - `search_query`: str
  - `search_results`: List of dicts (article_id:int, title:str, excerpt:str)
- Navigation mappings:
  - `back-to-dashboard` -> `url_for('dashboard')`

---

## Section 3: Data File Schemas

### 1. Articles Data
- File path: `data/articles.txt`
- Pipe-delimited format: `article_id|title|author|category|content|date|views`
- Description: Contains all news articles with metadata including views count.
- Example rows:
  ```
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891
  ```

### 2. Categories Data
- File path: `data/categories.txt`
- Pipe-delimited format: `category_id|category_name|description`
- Description: List of article categories with descriptions.
- Example rows:
  ```
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news
  ```

### 3. Bookmarks Data
- File path: `data/bookmarks.txt`
- Pipe-delimited format: `bookmark_id|article_id|article_title|bookmarked_date`
- Description: Stores bookmarked articles by users.
- Example rows:
  ```
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18
  ```

### 4. Comments Data
- File path: `data/comments.txt`
- Pipe-delimited format: `comment_id|article_id|article_title|commenter_name|comment_text|comment_date`
- Description: Contains comments made on articles.
- Example rows:
  ```
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19
  ```

### 5. Trending Data
- File path: `data/trending.txt`
- Pipe-delimited format: `article_id|article_title|category|view_count|period`
- Description: Trending articles ranked by views within specified periods.
- Example rows:
  ```
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month
  ```

---

End of Design Specifications.
