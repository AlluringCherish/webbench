# NewsPortal Design Specification

---

# Section 1: Flask Routes Specification

| Route Path                         | Function Name             | HTTP Methods | Template              | Context Variables                                                                                                                                                                                               | POST Form Fields                  |
|----------------------------------|---------------------------|--------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------| 
| `/`                              | dashboard                 | GET          | dashboard.html        | - articles (list of dict): article_id (int), title (str), author (str), category (str), content (str), date (str), views (int)
- categories (list of dict): category_id (int), category_name (str), description (str)
- bookmarks (list of dict): bookmark_id (int), article_id (int), article_title (str), bookmarked_date (str)
- trending_articles (list of dict): article_id (int), title (str), category (str), view_count (int), period (str)
- category_filter (str or None)
- sort (str or None)
- page_title (str) | None                            |
| `/catalog`                       | catalog_page              | GET          | catalog.html          | - articles (list of dict): same as dashboard
- categories (list of dict): same as dashboard
- search_query (str or None)
- category_filter (str or None)
- page_title (str)                                                                                         | None                            |
| `/articles/<int:article_id>`     | article_details          | GET, POST    | article_details.html  | - article (dict): article_id (int), title (str), author (str), category (str), content (str), date (str), views (int)
- comments (list of dict): comment_id (int), article_id (int), article_title (str), commenter_name (str), comment_text (str), comment_date (str)
- is_bookmarked (bool)
- page_title (str)                                      | commenter_name (str), comment_text (str)           |
| `/bookmarks`                    | bookmarks_page            | GET          | bookmarks.html        | - bookmarks (list of dict): bookmark_id (int), article_id (int), article_title (str), bookmarked_date (str)
- page_title (str)                                                                                   | None                            |
| `/bookmarks/remove/<int:bookmark_id>` | remove_bookmark          | POST         | None                  | None                                                                                                                                                                                                            | None                            |
| `/comments`                    | comments_page             | GET          | comments.html          | - comments (list of dict): comment_id (int), article_id (int), article_title (str), commenter_name (str), comment_text (str), comment_date (str)
- articles (list of dict): article_id (int), title (str), author (str), category (str), content (str), date (str), views (int)
- selected_article_id (int or None)
- page_title (str)                       | None                            |
| `/write-comment`                | write_comment_page       | GET, POST    | write_comment.html    | - articles (list of dict): as above
- page_title (str)                                                                                                                                                         | commenter_name (str), comment_text (str), article_id (int) |
| `/trending`                     | trending_page             | GET          | trending.html          | - trending_articles (list of dict): article_id (int), article_title (str), category (str), view_count (int), period (str)
- time_period_filter (str or None)
- page_title (str)                                       | None                            |
| `/category/<string:category_name>`| category_page             | GET          | category.html          | - category_name (str)
- articles (list of dict): filtered by category
- page_title (str)
- sort_order (str or None)                                                                                              | None                            |
| `/search`                      | search_results_page       | GET          | search_results.html    | - articles (list of dict): filtered by query and/or category
- query (str or None)
- page_title (str)                                                                                                            | None                            |

---

# Section 2: HTML Template Specifications

## 1. dashboard.html
- **File path**: `templates/dashboard.html`
- **Page title**: News Portal (in `<title>` and `<h1>`)
- **Element IDs and Types**:
  - `dashboard-page` (div): Main container
  - `featured-articles` (div): Display featured articles
  - `browse-articles-button` (button): Navigate to article catalog
  - `view-bookmarks-button` (button): Navigate to bookmarks page
  - `trending-articles-button` (button): Navigate to trending articles
- **Context Variables**:
  - `articles` (list of dict): each dict with article_id (int), title (str), author (str), category (str), content (str), date (str), views (int)
  - `categories` (list of dict): category_id (int), category_name (str), description (str)
  - `bookmarks` (list of dict)
  - `trending_articles` (list of dict): article_id (int), title (str), category (str), view_count (int), period (str)
  - `page_title` (str)
- **Navigation Mappings**:
  - `browse-articles-button`: URL `url_for('catalog_page')`
  - `view-bookmarks-button`: URL `url_for('bookmarks_page')`
  - `trending-articles-button`: URL `url_for('trending_page')`
  - Featured articles or listings could implement buttons linking to `url_for('article_details', article_id=article.article_id)`
- Use Jinja2 templating for loops and conditionals.

## 2. catalog.html
- **File path**: `templates/catalog.html`
- **Page title**: Article Catalog
- **Element IDs and Types**:
  - `catalog-page` (div): container
  - `search-input` (input): text input for search
  - `category-filter` (select dropdown): filter by category
  - `articles-grid` (div): grid for article cards
  - `view-article-button-{article_id}` (button): button on each article card
- **Context Variables**:
  - `articles` (list of dict)
  - `categories` (list of dict)
  - `search_query` (str)
  - `category_filter` (str)
  - `page_title` (str)
- **Navigation**:
  - Article buttons link to `url_for('article_details', article_id=article.article_id)`

## 3. article_details.html
- **File path**: `templates/article_details.html`
- **Page title**: Article Details
- **Element IDs and Types**:
  - `article-details-page` (div): container
  - `article-title` (h1): article title
  - `article-author` (div): article author
  - `article-date` (div): publication date
  - `bookmark-button` (button): bookmark toggle
  - `article-content` (div): full content text
- **Context Variables**:
  - `article` (dict)
  - `comments` (list of dict)
  - `is_bookmarked` (bool)
  - `page_title` (str)
- **Navigation**:
  - Back buttons and article comment write links as appropriate.

## 4. bookmarks.html
- **File path**: `templates/bookmarks.html`
- **Page title**: My Bookmarks
- **Element IDs**:
  - `bookmarks-page` (div)
  - `bookmarks-list` (div)
  - `remove-bookmark-button-{bookmark_id}` (button)
  - `read-bookmark-button-{bookmark_id}` (button)
  - `back-to-dashboard` (button)
- **Context**: bookmarks list
- Navigations for remove post and read bookmark link.

## 5. comments.html
- **File path**: `templates/comments.html`
- **Page title**: Article Comments
- **Element IDs**:
  - `comments-page` (div)
  - `comments-list` (div)
  - `write-comment-button` (button)
  - `filter-by-article` (dropdown)
  - `back-to-dashboard` (button)
- **Context Variables**:
  - comments list
  - articles list
  - selected article filter

## 6. write_comment.html
- **File path**: `templates/write_comment.html`
- **Page title**: Write a Comment
- **Element IDs**:
  - `write-comment-page` (div)
  - `select-article` (dropdown)
  - `commenter-name` (input)
  - `comment-text` (textarea)
  - `submit-comment-button` (button)
- **Context Variables**:
  - articles list

## 7. trending.html
- **File path**: `templates/trending.html`
- **Page title**: Trending Articles
- **Element IDs**:
  - `trending-page` (div)
  - `trending-list` (div)
  - `time-period-filter` (dropdown)
  - `view-article-button-{article_id}` (button)
  - `back-to-dashboard` (button)
- **Context Variables**:
  - trending_articles list
  - time_period_filter (str)

## 8. category.html
- **File path**: `templates/category.html`
- **Page title**: Category Articles
- **Element IDs**:
  - `category-page` (div)
  - `category-title` (h1)
  - `category-articles` (div)
  - `sort-by-date` (button)
  - `sort-by-popularity` (button)
  - `back-to-dashboard` (button)
- **Context Variables**:
  - category name (str)
  - filtered articles list
  - sort_order (str)

## 9. search_results.html
- **File path**: `templates/search_results.html`
- **Page title**: Search Results
- **Element IDs**:
  - `search-results-page` (div)
  - `search-query-display` (div)
  - `results-list` (div)
  - `no-results-message` (div), shows when no results
  - `back-to-dashboard` (button)
- **Context Variables**:
  - articles list
  - query (str)

---

# Section 3: Data File Schemas

## 1. articles.txt
- **Path:** `data/articles.txt`
- **Format:** Pipe-delimited (`|`) no header
- **Fields:**
  1. article_id (int)
  2. title (str)
  3. author (str)
  4. category (str)
  5. content (str)
  6. date (str, `YYYY-MM-DD`)
  7. views (int)
- **Description:** Stores all news articles.
- **Examples:**
  ```
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891
  ```

## 2. categories.txt
- **Path:** `data/categories.txt`
- **Format:** Pipe-delimited, no header
- **Fields:**
  1. category_id (int)
  2. category_name (str)
  3. description (str)
- **Description:** Stores categories of articles.
- **Examples:**
  ```
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news
  ```

## 3. bookmarks.txt
- **Path:** `data/bookmarks.txt`
- **Format:** Pipe-delimited, no header
- **Fields:**
  1. bookmark_id (int)
  2. article_id (int)
  3. article_title (str)
  4. bookmarked_date (str, `YYYY-MM-DD`)
- **Description:** User bookmarked articles.
- **Examples:**
  ```
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18
  ```

## 4. comments.txt
- **Path:** `data/comments.txt`
- **Format:** Pipe-delimited, no header
- **Fields:**
  1. comment_id (int)
  2. article_id (int)
  3. article_title (str)
  4. commenter_name (str)
  5. comment_text (str)
  6. comment_date (str, `YYYY-MM-DD`)
- **Description:** Comments on articles.
- **Examples:**
  ```
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19
  ```

## 5. trending.txt
- **Path:** `data/trending.txt`
- **Format:** Pipe-delimited, no header
- **Fields:**
  1. article_id (int)
  2. article_title (str)
  3. category (str)
  4. view_count (int)
  5. period (str)
- **Description:** Trending articles with views and period.
- **Examples:**
  ```
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month
  ```

---

This specification enables Backend developers to implement `app.py` routes and data parsing precisely, and Frontend developers to create templates strictly following IDs, variable names, and structure with no assumptions beyond this document.