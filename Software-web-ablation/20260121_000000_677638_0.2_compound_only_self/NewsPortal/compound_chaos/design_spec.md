# NewsPortal Web Application Design Specification

---

## 1. Flask Routes Specification

| Route Path                     | Flask Function Name            | HTTP Method | Template File             | Context Variables Passed to Templates with Data Types                                      | Expected POST Form Data                   |
|-------------------------------|-------------------------------|-------------|---------------------------|--------------------------------------------------------------------------------------------|------------------------------------------|
| /                             | root                          | GET         | None (redirect to /dashboard) | None                                                                                      | None                                     |
| /dashboard                    | dashboard_page                | GET         | dashboard.html            | featured_articles (list of dict), trending_articles (list of dict)                         | None                                     |
| /catalog                     | article_catalog               | GET         | catalog.html              | articles (list of dict), categories (list of dict), selected_category (str/None), search_query (str/None) | None                                     |
| /article/<article_id>         | article_detail                | GET         | article_detail.html       | article (dict), is_bookmarked (bool)                                                      | None                                     |
| /bookmarks                   | bookmarks_page                | GET         | bookmarks.html            | bookmarks (list of dict)                                                                  | None                                     |
| /comments                    | comments_page                 | GET         | comments.html             | comments (list of dict), articles (list of dict), selected_article_id (str/None)          | None                                     |
| /comments/write/<article_id> | write_comment_page            | GET, POST   | write_comment.html        | article (dict), articles (list of dict)                                                  | commenter_name (str), comment_text (str) |
| /trending                   | trending_page                 | GET         | trending.html             | trending_articles (list of dict), time_period (str)                                       | None                                     |
| /category/<category_id>       | category_page                | GET         | category.html             | category (dict), articles (list of dict), sort_method (str)                              | None                                     |
| /search                     | search_results                | GET         | search_results.html       | search_query (str), matching_articles (list of dict)                                     | None                                     |

---

## 2. HTML Template Specifications

### 2.1 Dashboard Page (`templates/dashboard.html`)
- Title: "News Portal"
- H1: "News Portal"
- Element IDs:
  - `dashboard-page` (Div): Container for dashboard page.
  - `featured-articles` (Div): Display featured article recommendations.
  - `browse-articles-button` (Button): Navigate to article catalog page.
  - `view-bookmarks-button` (Button): Navigate to bookmarks page.
  - `trending-articles-button` (Button): Navigate to trending articles page.
- Context Variables:
  - featured_articles (List[Dict]): Each dict has article_id, title, author, date, category.
  - trending_articles (List[Dict]): Each dict has article_id, title, category, view_count.
- Navigation Mapping:
  - `browse-articles-button` → `url_for('article_catalog')`
  - `view-bookmarks-button` → `url_for('bookmarks_page')`
  - `trending-articles-button` → `url_for('trending_page')`

---

### 2.2 Article Catalog Page (`templates/catalog.html`)
- Title: "Article Catalog"
- H1: "Article Catalog"
- Element IDs:
  - `catalog-page` (Div): Container for catalog page.
  - `search-input` (Input): Field for article search by title, author, or keywords.
  - `category-filter` (Dropdown): Filter by category (e.g., Technology, Sports).
  - `articles-grid` (Div): Grid showing article cards with thumbnail, title, author, date.
  - `view-article-button-{article_id}` (Button): Button to view article details.
- Context Variables:
  - articles (List[Dict]): Each dict includes article_id, title, author, date, category, snippet.
  - categories (List[Dict]): Each dict includes category_id, category_name.
  - selected_category (str or None)
  - search_query (str or None)
- Navigation Mapping:
  - `view-article-button-{article_id}` → `url_for('article_detail', article_id=article_id)`

---

### 2.3 Article Details Page (`templates/article_detail.html`)
- Title: "Article Details"
- H1: `{{ article.title }}`
- Element IDs:
  - `article-details-page` (Div): Container for article details.
  - `article-title` (H1): Article title.
  - `article-author` (Div): Article author.
  - `article-date` (Div): Article publication date.
  - `bookmark-button` (Button): Button to bookmark article.
  - `article-content` (Div): Full article content.
- Context Variables:
  - article (Dict): with keys article_id, title, author, date, content, category, views.
  - is_bookmarked (Bool)
- Navigation Mapping:
  - `bookmark-button` → POST request to toggle bookmark (handled backend).

---

### 2.4 Bookmarks Page (`templates/bookmarks.html`)
- Title: "My Bookmarks"
- H1: "My Bookmarks"
- Element IDs:
  - `bookmarks-page` (Div): Container for bookmarks page.
  - `bookmarks-list` (Div): List of bookmarked articles with title and date.
  - `remove-bookmark-button-{bookmark_id}` (Button): Remove specific bookmark.
  - `read-bookmark-button-{bookmark_id}` (Button): Read bookmarked article.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- Context Variables:
  - bookmarks (List[Dict]): Each dict includes bookmark_id, article_id, article_title, bookmarked_date.
- Navigation Mapping:
  - `remove-bookmark-button-{bookmark_id}` → POST to remove bookmark backend route.
  - `read-bookmark-button-{bookmark_id}` → `url_for('article_detail', article_id=article_id)`
  - `back-to-dashboard` → `url_for('dashboard_page')`

---

### 2.5 Comments Page (`templates/comments.html`)
- Title: "Article Comments"
- H1: "Article Comments"
- Element IDs:
  - `comments-page` (Div): Container for comments page.
  - `comments-list` (Div): List of comments with article title, commenter name, comment text.
  - `write-comment-button` (Button): Navigate to write comment page.
  - `filter-by-article` (Dropdown): Filter comments by article.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- Context Variables:
  - comments (List[Dict]): Each dict includes comment_id, article_id, article_title, commenter_name, comment_text, comment_date.
  - articles (List[Dict]): article_id and title for filtering dropdown.
  - selected_article_id (str or None)
- Navigation Mapping:
  - `write-comment-button` → `url_for('write_comment_page', article_id=selected_article_id or default)`
  - `back-to-dashboard` → `url_for('dashboard_page')`

---

### 2.6 Write Comment Page (`templates/write_comment.html`)
- Title: "Write a Comment"
- H1: "Write a Comment"
- Element IDs:
  - `write-comment-page` (Div): Comment writing container.
  - `select-article` (Dropdown): Select article to comment on.
  - `commenter-name` (Input): Commenter name field.
  - `comment-text` (Textarea): Comment text field.
  - `submit-comment-button` (Button): Submit comment.
- Context Variables:
  - articles (List[Dict]): list of articles for dropdown selection.
  - article (Dict): current article when accessed with article_id.
- Navigation Mapping:
  - `submit-comment-button` → POST form submission to same route.

---

### 2.7 Trending Articles Page (`templates/trending.html`)
- Title: "Trending Articles"
- H1: "Trending Articles"
- Element IDs:
  - `trending-page` (Div): Container.
  - `trending-list` (Div): Ranked trending articles.
  - `time-period-filter` (Dropdown): Filter by time period (Today, This Week, This Month).
  - `view-article-button-{article_id}` (Button): View article.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- Context Variables:
  - trending_articles (List[Dict]): with keys article_id, title, category, view_count.
  - time_period (str): Currently selected time period.
- Navigation Mapping:
  - `view-article-button-{article_id}` → `url_for('article_detail', article_id=article_id)`
  - `back-to-dashboard` → `url_for('dashboard_page')`

---

### 2.8 Category Page (`templates/category.html`)
- Title: "Category Articles"
- H1: `{{ category.category_name }}`
- Element IDs:
  - `category-page` (Div): Container.
  - `category-title` (H1): Category name.
  - `category-articles` (Div): List of articles.
  - `sort-by-date` (Button): Sort by date.
  - `sort-by-popularity` (Button): Sort by popularity.
  - `back-to-dashboard` (Button): Back to dashboard.
- Context Variables:
  - category (Dict): category_id, category_name, description.
  - articles (List[Dict]): articles in category.
  - sort_method (str): "date" or "popularity"
- Navigation Mapping:
  - `sort-by-date` → reload with sort by date
  - `sort-by-popularity` → reload with sort by popularity
  - `back-to-dashboard` → `url_for('dashboard_page')`

---

### 2.9 Search Results Page (`templates/search_results.html`)
- Title: "Search Results"
- H1: "Search Results"
- Element IDs:
  - `search-results-page` (Div): Container.
  - `search-query-display` (Div): Search query shown.
  - `results-list` (Div): List of matching articles.
  - `no-results-message` (Div): Display if no results.
  - `back-to-dashboard` (Button): Back to dashboard.
- Context Variables:
  - search_query (str)
  - matching_articles (List[Dict]): article_id, title, author, snippet.
- Navigation Mapping:
  - `back-to-dashboard` → `url_for('dashboard_page')`

---

## 3. Data File Schemas

---

### 3.1 Articles Data (`data/articles.txt`)
- Filepath: `data/articles.txt`
- Pipe-delimited fields (no header):
  1. article_id (str)
  2. title (str)
  3. author (str)
  4. category (str)
  5. content (str)
  6. date (str, YYYY-MM-DD)
  7. views (int)
- Content/Purpose:
  Stores all news articles with full content, metadata, and views.
- Example Rows:
  - `1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432`
  - `2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210`
  - `3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891`

---

### 3.2 Categories Data (`data/categories.txt`)
- Filepath: `data/categories.txt`
- Pipe-delimited fields (no header):
  1. category_id (str)
  2. category_name (str)
  3. description (str)
- Content/Purpose:
  Stores categories metadata for article filtering.
- Example Rows:
  - `1|Technology|Latest tech news and innovations`
  - `2|Sports|Sports news and event coverage`
  - `3|Business|Business and finance news`

---

### 3.3 Bookmarks Data (`data/bookmarks.txt`)
- Filepath: `data/bookmarks.txt`
- Pipe-delimited fields (no header):
  1. bookmark_id (str)
  2. article_id (str)
  3. article_title (str)
  4. bookmarked_date (str, YYYY-MM-DD)
- Content/Purpose:
  Stores user's bookmarked articles for quick access.
- Example Rows:
  - `1|1|Breaking: New Technology Breakthrough|2025-01-20`
  - `2|3|Business: Market Trends Analysis|2025-01-18`

---

### 3.4 Comments Data (`data/comments.txt`)
- Filepath: `data/comments.txt`
- Pipe-delimited fields (no header):
  1. comment_id (str)
  2. article_id (str)
  3. article_title (str)
  4. commenter_name (str)
  5. comment_text (str)
  6. comment_date (str, YYYY-MM-DD)
- Content/Purpose:
  Stores comments on articles.
- Example Rows:
  - `1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20`
  - `2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19`

---

### 3.5 Trending Data (`data/trending.txt`)
- Filepath: `data/trending.txt`
- Pipe-delimited fields (no header):
  1. article_id (str)
  2. article_title (str)
  3. category (str)
  4. view_count (int)
  5. period (str) (e.g., Today, This Week, This Month)
- Content/Purpose:
  Stores trending articles and their rankings by time period.
- Example Rows:
  - `1|Breaking: New Technology Breakthrough|Technology|5432|This Week`
  - `2|Sports: Championship Victory|Sports|3210|This Week`
  - `3|Business: Market Trends Analysis|Business|2891|This Month`

---

*End of Design Specification.*
