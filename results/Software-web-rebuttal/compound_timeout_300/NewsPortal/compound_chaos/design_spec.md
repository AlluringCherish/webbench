# Design Specification for NewsPortal Web Application

---

## 1. Flask Routes Specification

| Route URL Pattern               | Function Name             | HTTP Method(s) | Rendered Template                | Context Variables (Type)                                                                                                        | POST Form Data (Type)                                 |
|--------------------------------|---------------------------|----------------|--------------------------------|-------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| `/`                            | `root`                   | GET            | Redirects to `/dashboard`      | None                                                                                                                          | None                                                  |
| `/dashboard`                   | `dashboard`              | GET            | `dashboard.html`                | featured_articles (List[Dict]): List of featured articles 
trending_articles (List[Dict]): List of trending articles         | None                                                  |
| `/catalog`                    | `article_catalog`         | GET            | `catalog.html`                  | articles (List[Dict]): List of all articles
categories (List[Dict]): List of all categories                             | None                                                  |
| `/catalog/search`             | `search_results`          | GET            | `search_results.html`           | query (str): Search query string
results (List[Dict]): List of matched articles                                              | None                                                  |
| `/category/<string:category_name>` | `category_articles`       | GET            | `category.html`                 | category_name (str): Name of the selected category
articles (List[Dict]): List of articles in category                        | None                                                  |
| `/category/<string:category_name>/sort` | `category_sort`           | POST           | Redirects back to `/category/<category_name>` | sort_by (str): 'date' or 'popularity' from form data                                                                | sort_by (str)                                         |
| `/article/<int:article_id>`    | `article_details`         | GET, POST      | `article_details.html`          | article (Dict): Article details
is_bookmarked (bool): Bookmark status                                                    | action (str): 'bookmark' from form data (POST only)  |
| `/bookmarks`                   | `bookmarks`               | GET            | `bookmarks.html`                | bookmarks (List[Dict]): List of bookmarked articles                                                                           | None                                                  |
| `/bookmarks/remove/<int:bookmark_id>` | `remove_bookmark`         | POST           | Redirects to `/bookmarks`       | None                                                                                                                          | bookmark_id (int)                                     |
| `/comments`                   | `comments`                | GET            | `comments.html`                 | comments (List[Dict]): List of comments
articles (List[Dict]): List of articles for filtering                                | None                                                  |
| `/comments/write`             | `write_comment`           | GET, POST      | `write_comment.html`            | articles (List[Dict]): List of articles                                                                                       | article_id (int), commenter_name (str), comment_text (str) (POST only) |
| `/trending`                   | `trending_articles`       | GET            | `trending.html`                 | trending_articles (List[Dict]): List of trending articles
periods (List[str]): Time period filter options                     | None                                                  |
| `/trending/filter`            | `trending_filter`          | POST           | Redirects to `/trending`        | period (str): Time period from form data                                                                                    | period (str)                                         |

---

## 2. HTML Template Specifications

### templates/dashboard.html
- Page Title: News Portal
- Elements:
  - `dashboard-page` (Div): Container for the dashboard page.
  - `featured-articles` (Div): Display of featured article recommendations.
  - `browse-articles-button` (Button): Navigate to article catalog page.
  - `view-bookmarks-button` (Button): Navigate to bookmarks page.
  - `trending-articles-button` (Button): Navigate to trending articles page.
- Context Variables:
  - featured_articles (List[Dict]): Each dict with keys: article_id (int), title (str), author (str), date (str), excerpt (str)
  - trending_articles (List[Dict]): Each dict with keys: article_id (int), title (str), category (str), view_count (int)
- Navigation using `url_for()`:
  - `browse-articles-button` -> `url_for('article_catalog')`
  - `view-bookmarks-button` -> `url_for('bookmarks')`
  - `trending-articles-button` -> `url_for('trending_articles')`

### templates/catalog.html
- Page Title: Article Catalog
- Elements:
  - `catalog-page` (Div): Container for the catalog page.
  - `search-input` (Input): Search articles by title, author, or keywords (type="text" name="query" form submits GET to `/catalog/search`).
  - `category-filter` (Dropdown): Dropdown to filter by category; value to link to `/category/<category_name>`.
  - `articles-grid` (Div): Grid displaying article cards.
  - `view-article-button-{article_id}` (Button): View article details.
- Context Variables:
  - articles (List[Dict]): Each dict with keys: article_id (int), title (str), author (str), category (str), date (str), excerpt (str)
  - categories (List[Dict]): Each dict with keys: category_id (int), category_name (str), description (str)
- Navigation using `url_for()`:
  - Article buttons: `url_for('article_details', article_id=article.article_id)`
  - Category filter options: `url_for('category_articles', category_name=category.category_name)`

### templates/article_details.html
- Page Title: Article Details
- Elements:
  - `article-details-page` (Div): Container for article details.
  - `article-title` (H1): Article title display.
  - `article-author` (Div): Display article author.
  - `article-date` (Div): Display article publication date.
  - `bookmark-button` (Button): Bookmark the article; form submits POST to `/article/<article_id>` with `action='bookmark'`.
  - `article-content` (Div): Full article content.
- Context Variables:
  - article (Dict): article_id (int), title (str), author (str), category (str), content (str), date (str), views (int)
  - is_bookmarked (bool): Whether the article is bookmarked
- Navigation using `url_for()`:
  - None specific, main navigation from other templates.

### templates/bookmarks.html
- Page Title: My Bookmarks
- Elements:
  - `bookmarks-page` (Div): Container for bookmarks page.
  - `bookmarks-list` (Div): List displaying bookmarks.
  - `remove-bookmark-button-{bookmark_id}` (Button): Remove bookmark; form POST to `/bookmarks/remove/<bookmark_id>`.
  - `read-bookmark-button-{bookmark_id}` (Button): Read bookmarked article; link to `/article/<article_id>`.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- Context Variables:
  - bookmarks (List[Dict]): Each dict with bookmark_id (int), article_id (int), article_title (str), bookmarked_date (str)
- Navigation using `url_for()`:
  - Remove bookmark buttons: submit POST forms to `url_for('remove_bookmark', bookmark_id=bookmark.bookmark_id)`
  - Read bookmark buttons: `url_for('article_details', article_id=bookmark.article_id)`
  - Back to dashboard button: `url_for('dashboard')`

### templates/comments.html
- Page Title: Article Comments
- Elements:
  - `comments-page` (Div): Container for comments page.
  - `comments-list` (Div): List of comments with article title, commenter name, comment text.
  - `write-comment-button` (Button): Navigate to write comment page.
  - `filter-by-article` (Dropdown): Filter comments by article.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- Context Variables:
  - comments (List[Dict]): comment_id (int), article_id (int), article_title (str), commenter_name (str), comment_text (str), comment_date (str)
  - articles (List[Dict]): article_id (int), title (str)
- Navigation using `url_for()`:
  - Write comment button: `url_for('write_comment')`
  - Filter dropdown options: `url_for('comments')` with query param for filtering if used
  - Back to dashboard button: `url_for('dashboard')`

### templates/write_comment.html
- Page Title: Write a Comment
- Elements:
  - `write-comment-page` (Div): Container for write comment page.
  - `select-article` (Dropdown): Select article to comment on.
  - `commenter-name` (Input): Input for commenter name.
  - `comment-text` (Textarea): Input for comment text.
  - `submit-comment-button` (Button): Submit comment.
- Context Variables:
  - articles (List[Dict]): article_id (int), title (str)
- Navigation using `url_for()`:
  - Form submits POST to `url_for('write_comment')`

### templates/trending.html
- Page Title: Trending Articles
- Elements:
  - `trending-page` (Div): Container for trending articles.
  - `trending-list` (Div): Ranked list of trending articles.
  - `time-period-filter` (Dropdown): Filter by time period.
  - `view-article-button-{article_id}` (Button): View article details.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- Context Variables:
  - trending_articles (List[Dict]): article_id (int), article_title (str), category (str), view_count (int), period (str)
  - periods (List[str]): List of time periods ("Today", "This Week", "This Month")
- Navigation using `url_for()`:
  - View article buttons: `url_for('article_details', article_id=article.article_id)`
  - Back to dashboard button: `url_for('dashboard')`

### templates/category.html
- Page Title: Category Articles
- Elements:
  - `category-page` (Div): Container for category page.
  - `category-title` (H1): Display category name.
  - `category-articles` (Div): List of articles in category.
  - `sort-by-date` (Button): Sort articles by date.
  - `sort-by-popularity` (Button): Sort articles by popularity.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- Context Variables:
  - category_name (str): Name of the category
  - articles (List[Dict]): article_id (int), title (str), author (str), date (str), popularity (int or views proxy)
- Navigation using `url_for()`:
  - Sort buttons submit POST form to `url_for('category_sort', category_name=category_name)`
  - Back to dashboard button: `url_for('dashboard')`

### templates/search_results.html
- Page Title: Search Results
- Elements:
  - `search-results-page` (Div): Container for search results.
  - `search-query-display` (Div): Display the search query.
  - `results-list` (Div): List of search result articles with title and excerpt.
  - `no-results-message` (Div): Message when no results found.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- Context Variables:
  - query (str): Search query
  - results (List[Dict]): article_id (int), title (str), excerpt (str)
- Navigation using `url_for()`:
  - Back to dashboard button: `url_for('dashboard')`

---

## 3. Data File Schemas

### 1. data/articles.txt
- Fields: `article_id|title|author|category|content|date|views`
- Content: Stores news articles with unique ID, metadata and content, date in ISO format, and number of views.
- Examples:
  ```
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891
  ```

### 2. data/categories.txt
- Fields: `category_id|category_name|description`
- Content: Stores news categories with unique ID and description.
- Examples:
  ```
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news
  ```

### 3. data/bookmarks.txt
- Fields: `bookmark_id|article_id|article_title|bookmarked_date`
- Content: Stores user bookmarked articles with bookmark ID and date added.
- Examples:
  ```
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18
  ```

### 4. data/comments.txt
- Fields: `comment_id|article_id|article_title|commenter_name|comment_text|comment_date`
- Content: Stores comments for articles with commenter and date.
- Examples:
  ```
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19
  ```

### 5. data/trending.txt
- Fields: `article_id|article_title|category|view_count|period`
- Content: Stores trending article data by period.
- Examples:
  ```
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month
  ```
