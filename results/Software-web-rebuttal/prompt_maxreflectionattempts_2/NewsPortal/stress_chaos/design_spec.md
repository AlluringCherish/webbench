# NewsPortal Application Design Specification

---

## 1. Flask Routes Specification

| Route Path & URL Pattern          | Flask Function Name      | HTTP Methods | Template to Render        | Context Variables (Name: Type - Description)                                                                                                      | POST Route Form Data (if applicable)                 |
|----------------------------------|--------------------------|--------------|---------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| `/` (root)                       | root                     | GET          | None (Redirect)            | None                                                                                                                                           | None                                                |
| `/dashboard`                    | dashboard                | GET          | dashboard.html            | dashboard_page_id: str - Div container ID for dashboard page
featured_articles_id: str - Div ID for featured articles display
browse_articles_button_id: str - Button ID to navigate to articles catalog
view_bookmarks_button_id: str - Button ID to navigate to bookmarks page
trending_articles_button_id: str - Button ID to navigate to trending articles page | None                                                |
| `/articles`                    | article_catalog           | GET          | articles.html             | catalog_page_id: str - Div container ID for article catalog
search_input_id: str - Input field ID for search
category_filter_id: str - Dropdown ID for category filter
articles_grid_id: str - Div ID for articles grid | None                                                |
| `/article/<int:article_id>`    | article_details           | GET          | article_details.html      | article_details_page_id: str - Div container ID for article details page
article_title_id: str - H1 ID for article title
article_author_id: str - Div ID for article author
article_date_id: str - Div ID for article date
bookmark_button_id: str - Button ID for bookmarking
article_content_id: str - Div ID for full article content | None                                                |
| `/bookmarks`                   | bookmarks_page            | GET          | bookmarks.html            | bookmarks_page_id: str - Div container ID for bookmarks list
bookmarks_list_id: str - Div ID for bookmarks list display
remove_bookmark_button_id_prefix: str - Prefix for remove bookmark buttons
read_bookmark_button_id_prefix: str - Prefix for read bookmark buttons
back_to_dashboard_button_id: str - Button ID to go back to dashboard | None                                                |
| `/comments`                   | comments_page             | GET          | comments.html             | comments_page_id: str - Div container ID for comments page
comments_list_id: str - Div ID listing comments
write_comment_button_id: str - Button ID to navigate to write comment
filter_by_article_id: str - Dropdown ID to filter comments by article
back_to_dashboard_button_id: str - Button ID to return to dashboard | None                                                |
| `/write-comment`              | write_comment_page        | GET          | write_comment.html        | write_comment_page_id: str - Div container ID for write comment page
select_article_id: str - Dropdown ID to select article for comment
commenter_name_input_id: str - Input ID for commenter name
comment_text_textarea_id: str - Textarea ID for comment text
submit_comment_button_id: str - Button ID to submit comment | commenter_name: str
comment_text: str
article_id: int (selected article from dropdown) |
| `/trending`                   | trending_articles_page    | GET          | trending.html             | trending_page_id: str - Div container ID for trending articles
trending_list_id: str - Div for ranked list of trending articles
time_period_filter_id: str - Dropdown ID to filter by time period
view_article_button_id_prefix: str - Prefix for view article buttons
back_to_dashboard_button_id: str - Button ID to return to dashboard | None                                                |
| `/category/<string:category_name>` | category_page             | GET          | category.html             | category_page_id: str - Div container ID for category page
category_title_id: str - H1 ID for category name
category_articles_id: str - Div ID for listing category articles
sort_by_date_button_id: str - Button ID for sorting by date
sort_by_popularity_button_id: str - Button ID for sorting by popularity
back_to_dashboard_button_id: str - Button ID to return to dashboard | None                                                |
| `/search-results`             | search_results_page       | GET          | search_results.html       | search_results_page_id: str - Div container ID for search results
search_query_display_id: str - Div ID displaying search query
results_list_id: str - Div ID listing search results
no_results_message_id: str - Div ID displayed when no search results
back_to_dashboard_button_id: str - Button ID to return to dashboard | None                                                |

---

## 2. HTML Template Specifications

### Common Jinja2 Usage
- Use `{{ variable_name }}` for injecting context variables.
- Use Jinja2 control structures `{% %}` for loops and conditional rendering.
- Use `url_for('function_name', **kwargs)` for URL routing.

---

### 1. dashboard.html
- File: `templates/dashboard.html`
- Page Title: `News Portal`
- H1 Title: `Dashboard`
- Element IDs:
  - `dashboard-page` (Div): Container for the dashboard page.
  - `featured-articles` (Div): Display area for featured articles.
  - `browse-articles-button` (Button): Navigates to article catalog page.
  - `view-bookmarks-button` (Button): Navigates to bookmarks page.
  - `trending-articles-button` (Button): Navigates to trending articles page.
- Context Variables:
  - `dashboard_page_id`: string
  - `featured_articles_id`: string
  - `browse_articles_button_id`: string
  - `view_bookmarks_button_id`: string
  - `trending_articles_button_id`: string
- Navigation Mappings:
  - `browse-articles-button` triggers navigation to route `article_catalog`.
  - `view-bookmarks-button` triggers navigation to route `bookmarks_page`.
  - `trending-articles-button` triggers navigation to route `trending_articles_page`.

---

### 2. articles.html
- File: `templates/articles.html`
- Page Title: `Article Catalog`
- H1 Title: `Article Catalog`
- Element IDs:
  - `catalog-page` (Div): Container for the article catalog.
  - `search-input` (Input): Text field for searching articles.
  - `category-filter` (Dropdown): Filter articles by category.
  - `articles-grid` (Div): Grid container displaying article cards.
  - `view-article-button-{{ article_id }}` (Button): Button inside each article card to view details.
- Context Variables:
  - `catalog_page_id`: string
  - `search_input_id`: string
  - `category_filter_id`: string
  - `articles_grid_id`: string
  - `articles`: list of dict (each with keys: article_id, title, author, date, thumbnail_url)
- Navigation Mappings:
  - Each `view-article-button-{{ article_id }}` triggers navigation to route `article_details` with article_id parameter.

---

### 3. article_details.html
- File: `templates/article_details.html`
- Page Title: `Article Details`
- H1 Title: Article title dynamically inserted.
- Element IDs:
  - `article-details-page` (Div): Container for article details page.
  - `article-title` (H1): Displays the article title.
  - `article-author` (Div): Displays the article author.
  - `article-date` (Div): Displays the publication date.
  - `bookmark-button` (Button): Button to add the article to bookmarks.
  - `article-content` (Div): Displays the full article content.
- Context Variables:
  - `article_details_page_id`: string
  - `article_title`: string
  - `article_author`: string
  - `article_date`: string
  - `article_content`: string
- Navigation Mappings:
  - `bookmark-button` triggers backend action to save bookmark via AJAX or POST (not specified here).

---

### 4. bookmarks.html
- File: `templates/bookmarks.html`
- Page Title: `My Bookmarks`
- H1 Title: `My Bookmarks`
- Element IDs:
  - `bookmarks-page` (Div): Container for bookmarks page.
  - `bookmarks-list` (Div): List container of bookmarks.
  - `remove-bookmark-button-{{ bookmark_id }}` (Button): Button to remove a bookmark.
  - `read-bookmark-button-{{ bookmark_id }}` (Button): Button to read bookmarked article.
  - `back-to-dashboard` (Button): Button to navigate back to dashboard.
- Context Variables:
  - `bookmarks_page_id`: string
  - `bookmarks_list`: list of dict (keys: bookmark_id, article_title, bookmarked_date)
- Navigation Mappings:
  - `remove-bookmark-button-{{ bookmark_id }}` triggers bookmark removal.
  - `read-bookmark-button-{{ bookmark_id }}` navigates to article details for the bookmarked article.
  - `back-to-dashboard` navigates to dashboard.

---

### 5. comments.html
- File: `templates/comments.html`
- Page Title: `Article Comments`
- H1 Title: `Comments`
- Element IDs:
  - `comments-page` (Div): Container for comments page.
  - `comments-list` (Div): List container displaying comments.
  - `write-comment-button` (Button): Navigate to write comment page.
  - `filter-by-article` (Dropdown): Filter comments by article.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- Context Variables:
  - `comments_page_id`: string
  - `comments_list`: list of dict (keys: article_title, commenter_name, comment_text, comment_date)
- Navigation Mappings:
  - `write-comment-button` navigates to `write_comment_page` route.
  - `back-to-dashboard` navigates to dashboard.

---

### 6. write_comment.html
- File: `templates/write_comment.html`
- Page Title: `Write a Comment`
- H1 Title: `Write a Comment`
- Element IDs:
  - `write-comment-page` (Div): Container for the write comment page.
  - `select-article` (Dropdown): Select article to comment on.
  - `commenter-name` (Input): Input field for commenter name.
  - `comment-text` (Textarea): Textarea for comment text.
  - `submit-comment-button` (Button): Submit comment button.
- Context Variables:
  - `write_comment_page_id`: string
  - `articles`: list of dict (keys: article_id, title)
- Navigation Mappings:
  - `submit-comment-button` submits comment form (POST to `/write-comment` expected).

---

### 7. trending.html
- File: `templates/trending.html`
- Page Title: `Trending Articles`
- H1 Title: `Trending Articles`
- Element IDs:
  - `trending-page` (Div): Container for trending articles.
  - `trending-list` (Div): Display ranked list of trending articles.
  - `time-period-filter` (Dropdown): Filter trending by time period.
  - `view-article-button-{{ article_id }}` (Button): View article details button.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- Context Variables:
  - `trending_page_id`: string
  - `trending_articles`: list of dict (keys: article_id, title, category, view_count, rank)
- Navigation Mappings:
  - `view-article-button-{{ article_id }}` navigates to `article_details` route.
  - `back-to-dashboard` navigates to dashboard.

---

### 8. category.html
- File: `templates/category.html`
- Page Title: `Category Articles`
- H1 Title: Category name dynamically displayed
- Element IDs:
  - `category-page` (Div): Container for category page.
  - `category-title` (H1): Displays category name.
  - `category-articles` (Div): List of articles in the category.
  - `sort-by-date` (Button): Sort articles by date.
  - `sort-by-popularity` (Button): Sort articles by popularity.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- Context Variables:
  - `category_page_id`: string
  - `category_name`: string
  - `category_articles`: list of dict (keys: article_id, title, author, date)
- Navigation Mappings:
  - `sort-by-date` and `sort-by-popularity` trigger sorting on the category page.
  - `back-to-dashboard` navigates to dashboard.

---

### 9. search_results.html
- File: `templates/search_results.html`
- Page Title: `Search Results`
- H1 Title: `Search Results`
- Element IDs:
  - `search-results-page` (Div): Container for search results page.
  - `search-query-display` (Div): Displays the search query string.
  - `results-list` (Div): List of search results.
  - `no-results-message` (Div): Displayed if no results found.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- Context Variables:
  - `search_results_page_id`: string
  - `search_query`: string
  - `results_list`: list of dict (keys: article_id, title, excerpt)
- Navigation Mappings:
  - `back-to-dashboard` navigates to dashboard.

---

## 3. Data File Schemas

### 1. Articles Data
- File path: `data/articles.txt`
- Fields (pipe-delimited): article_id|title|author|category|content|date|views
- Description: Stores all news article details.
- Example rows:
  ```
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891
  ```

### 2. Categories Data
- File path: `data/categories.txt`
- Fields (pipe-delimited): category_id|category_name|description
- Description: Stores information about article categories.
- Example rows:
  ```
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news
  ```

### 3. Bookmarks Data
- File path: `data/bookmarks.txt`
- Fields (pipe-delimited): bookmark_id|article_id|article_title|bookmarked_date
- Description: Stores bookmarked articles by users.
- Example rows:
  ```
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18
  ```

### 4. Comments Data
- File path: `data/comments.txt`
- Fields (pipe-delimited): comment_id|article_id|article_title|commenter_name|comment_text|comment_date
- Description: Stores user comments on articles.
- Example rows:
  ```
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19
  ```

### 5. Trending Data
- File path: `data/trending.txt`
- Fields (pipe-delimited): article_id|article_title|category|view_count|period
- Description: Stores data on trending articles, views, and time period.
- Example rows:
  ```
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month
  ```

---

This design_spec.md provides all necessary details for Backend and Frontend teams to implement the NewsPortal application independently and consistently as per user requirements.
