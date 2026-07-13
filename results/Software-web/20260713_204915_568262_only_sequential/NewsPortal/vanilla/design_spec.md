# NewsPortal Flask Application Design Specification

---

## 1. Flask Routes

| Route Path                | HTTP Method | Function Name            | Template Filename       |
|---------------------------|-------------|--------------------------|-------------------------|
| `/dashboard`              | GET         | dashboard                | dashboard.html          |
| `/articles`               | GET         | articles_catalog         | articles_catalog.html   |
| `/articles/<int:article_id>` | GET         | article_details          | article_details.html    |
| `/articles/<int:article_id>/bookmark` | POST        | post_bookmark            | (redirect or dashboard) |
| `/bookmarks`              | GET         | bookmarks                | bookmarks.html          |
| `/bookmarks/<int:bookmark_id>/remove` | POST        | remove_bookmark          | (redirect bookmarks)     |
| `/bookmarks/<int:bookmark_id>/read` | GET         | read_bookmark            | article_details.html    |
| `/comments`               | GET         | comments                 | comments.html           |
| `/comments/write`         | GET         | write_comment_page       | write_comment.html      |
| `/comments/write`         | POST        | submit_comment           | (redirect comments)     |
| `/trending`               | GET         | trending_articles        | trending_articles.html  |
| `/category/<int:category_id>` | GET         | category_articles        | category_articles.html  |
| `/search`                 | GET         | search_results           | search_results.html     |

---

## 2. Page Titles & Element IDs

### 1. Dashboard Page
- Title: `News Portal`
- Elements:
  - `dashboard-page` (Div)
  - `featured-articles` (Div)
  - `browse-articles-button` (Button)
  - `view-bookmarks-button` (Button)
  - `trending-articles-button` (Button)

### 2. Article Catalog Page
- Title: `Article Catalog`
- Elements:
  - `catalog-page` (Div)
  - `search-input` (Input)
  - `category-filter` (Dropdown)
  - `articles-grid` (Div)
  - `view-article-button-{article_id}` (Button) for each article card

### 3. Article Details Page
- Title: `Article Details`
- Elements:
  - `article-details-page` (Div)
  - `article-title` (H1)
  - `article-author` (Div)
  - `article-date` (Div)
  - `bookmark-button` (Button)
  - `article-content` (Div)

### 4. Bookmarks Page
- Title: `My Bookmarks`
- Elements:
  - `bookmarks-page` (Div)
  - `bookmarks-list` (Div)
  - `remove-bookmark-button-{bookmark_id}` (Button) for each bookmark
  - `read-bookmark-button-{bookmark_id}` (Button) for each bookmark
  - `back-to-dashboard` (Button)

### 5. Comments Page
- Title: `Article Comments`
- Elements:
  - `comments-page` (Div)
  - `comments-list` (Div)
  - `write-comment-button` (Button)
  - `filter-by-article` (Dropdown)
  - `back-to-dashboard` (Button)

### 6. Write Comment Page
- Title: `Write a Comment`
- Elements:
  - `write-comment-page` (Div)
  - `select-article` (Dropdown)
  - `commenter-name` (Input)
  - `comment-text` (Textarea)
  - `submit-comment-button` (Button)

### 7. Trending Articles Page
- Title: `Trending Articles`
- Elements:
  - `trending-page` (Div)
  - `trending-list` (Div)
  - `time-period-filter` (Dropdown)
  - `view-article-button-{article_id}` (Button) for each trending article
  - `back-to-dashboard` (Button)

### 8. Category Page
- Title: `Category Articles`
- Elements:
  - `category-page` (Div)
  - `category-title` (H1)
  - `category-articles` (Div)
  - `sort-by-date` (Button)
  - `sort-by-popularity` (Button)
  - `back-to-dashboard` (Button)

### 9. Search Results Page
- Title: `Search Results`
- Elements:
  - `search-results-page` (Div)
  - `search-query-display` (Div)
  - `results-list` (Div)
  - `no-results-message` (Div)
  - `back-to-dashboard` (Button)

---

## 3. Data Schema

### 3.1 Articles Data
- File: `data/articles.txt`
- Format: Pipe-delimited
```
article_id|title|author|category|content|date|views
```
- Fields:
  1. article_id (int)
  2. title (string)
  3. author (string)
  4. category (string)
  5. content (string)
  6. date (YYYY-MM-DD string)
  7. views (int)
- Example Data:
```
1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891
```

### 3.2 Categories Data
- File: `data/categories.txt`
- Format: Pipe-delimited
```
category_id|category_name|description
```
- Fields:
  1. category_id (int)
  2. category_name (string)
  3. description (string)
- Example Data:
```
1|Technology|Latest tech news and innovations
2|Sports|Sports news and event coverage
3|Business|Business and finance news
```

### 3.3 Bookmarks Data
- File: `data/bookmarks.txt`
- Format: Pipe-delimited
```
bookmark_id|article_id|article_title|bookmarked_date
```
- Fields:
  1. bookmark_id (int)
  2. article_id (int)
  3. article_title (string)
  4. bookmarked_date (YYYY-MM-DD string)
- Example Data:
```
1|1|Breaking: New Technology Breakthrough|2025-01-20
2|3|Business: Market Trends Analysis|2025-01-18
```

### 3.4 Comments Data
- File: `data/comments.txt`
- Format: Pipe-delimited
```
comment_id|article_id|article_title|commenter_name|comment_text|comment_date
```
- Fields:
  1. comment_id (int)
  2. article_id (int)
  3. article_title (string)
  4. commenter_name (string)
  5. comment_text (string)
  6. comment_date (YYYY-MM-DD string)
- Example Data:
```
1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19
```

### 3.5 Trending Data
- File: `data/trending.txt`
- Format: Pipe-delimited
```
article_id|article_title|category|view_count|period
```
- Fields:
  1. article_id (int)
  2. article_title (string)
  3. category (string)
  4. view_count (int)
  5. period (string) (e.g., "Today", "This Week", "This Month")
- Example Data:
```
1|Breaking: New Technology Breakthrough|Technology|5432|This Week
2|Sports: Championship Victory|Sports|3210|This Week
3|Business: Market Trends Analysis|Business|2891|This Month
```

---

## 4. UI Navigation Flows

| From Page           | Element/Button ID                | Target Route (Function)                        | HTTP Method |
|---------------------|--------------------------------|---------------------------------------------|-------------|
| Dashboard           | `browse-articles-button`        | `/articles` (articles_catalog)               | GET         |
| Dashboard           | `view-bookmarks-button`         | `/bookmarks` (bookmarks)                      | GET         |
| Dashboard           | `trending-articles-button`      | `/trending` (trending_articles)               | GET         |
| Article Catalog     | `view-article-button-{article_id}` | `/articles/<article_id>` (article_details)  | GET         |
| Article Details     | `bookmark-button`               | `/articles/<article_id>/bookmark` (post_bookmark) | POST        |
| Bookmarks           | `remove-bookmark-button-{bookmark_id}` | `/bookmarks/<bookmark_id>/remove` (remove_bookmark) | POST        |
| Bookmarks           | `read-bookmark-button-{bookmark_id}` | `/bookmarks/<bookmark_id>/read` (read_bookmark) | GET         |
| Bookmarks           | `back-to-dashboard`             | `/dashboard` (dashboard)                      | GET         |
| Comments            | `write-comment-button`          | `/comments/write` (write_comment_page)       | GET         |
| Comments            | `filter-by-article`             | Same `/comments` page with filter parameter | GET/client-side |
| Comments            | `back-to-dashboard`             | `/dashboard` (dashboard)                      | GET         |
| Write Comment       | `submit-comment-button`         | `/comments/write` (submit_comment)           | POST        |
| Trending Articles   | `view-article-button-{article_id}` | `/articles/<article_id>` (article_details)  | GET         |
| Trending Articles   | `time-period-filter`            | Same `/trending` page with filter parameter  | GET/client-side |
| Trending Articles   | `back-to-dashboard`             | `/dashboard` (dashboard)                      | GET         |
| Category            | `sort-by-date` or `sort-by-popularity` | Same `/category/<category_id>` page sorted  | GET/client-side |
| Category            | `back-to-dashboard`             | `/dashboard` (dashboard)                      | GET         |
| Search Results      | `back-to-dashboard`             | `/dashboard` (dashboard)                      | GET         |

---

## Templates Directory Structure

```
templates/
  dashboard.html
  articles_catalog.html
  article_details.html
  bookmarks.html
  comments.html
  write_comment.html
  trending_articles.html
  category_articles.html
  search_results.html
```

---

This design specification fully defines the Flask app architecture, templates, routes, data schema, page elements, and navigation flows for NewsPortal. It enables developers to implement backend logic, frontend templates, and data management without any ambiguity.
