# NewsPortal Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                 | Flask Function Name       | HTTP Method | Template File                | Context Variables (type)                                                                                     | Form Data (POST routes)                                         |
|----------------------------|---------------------------|-------------|------------------------------|--------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------|
| /                          | root_redirect             | GET         | None (redirect)              | None                                                                                                         | None                                                           |
| /dashboard                 | dashboard                 | GET         | dashboard.html               | featured_articles (list[dict{article_id:int, title:str, author:str, date:str}]),                                |
|                            |                           |             |                              | None                                                                                                         | None                                                           |
| /catalog                   | article_catalog           | GET         | article_catalog.html         | articles (list[dict{article_id:int, title:str, author:str, category:str, date:str}]),                          |
|                            |                           |             |                              | categories (list[str])                                                                                         | None                                                           |
| /catalog                   | article_catalog           | POST        | article_catalog.html         | articles (list[dict{article_id:int, title:str, author:str, category:str, date:str}]),                          |
|                            |                           |             |                              | categories (list[str])                                                                                         | search_query (str), category_filter (str, optional)            |
| /article/<int:article_id>  | article_details           | GET         | article_details.html         | article (dict{article_id:int, title:str, author:str, date:str, content:str}),                                  |
|                            |                           |             |                              | is_bookmarked (bool)                                                                                           | None                                                           |
| /bookmark                  | add_bookmark              | POST        | None (redirect to bookmarks)| None                                                                                                         | article_id (int)                                               |
| /bookmarks                 | bookmarks                 | GET         | bookmarks.html               | bookmarks (list[dict{bookmark_id:int, article_id:int, article_title:str, bookmarked_date:str}])                | None                                                           |
| /bookmark/remove/<int:id>  | remove_bookmark           | POST        | None (redirect to bookmarks)| None                                                                                                         | bookmark_id (int)                                              |
| /comments                  | comments                  | GET         | comments.html                | comments (list[dict{comment_id:int, article_id:int, article_title:str, commenter_name:str, comment_text:str}]),|
|                            |                           |             |                              | articles (list[dict{article_id:int, title:str}])                                                                | None                                                           |
| /comment/write             | write_comment             | GET         | write_comment.html           | articles (list[dict{article_id:int, title:str}])                                                             | None                                                           |
| /comment/write             | submit_comment            | POST        | None (redirect to comments) | None                                                                                                         | article_id (int), commenter_name (str), comment_text (str)    |
| /trending                  | trending_articles         | GET         | trending.html                | trending_articles (list[dict{article_id:int, article_title:str, category:str, view_count:int, period:str}])    |
|                            |                           |             |                              | None                                                                                                         | None                                                           |
| /category/<category_name>  | category_articles         | GET         | category.html                | category_name (str), articles (list[dict{article_id:int, title:str, date:str, popularity:int}])               | None                                                           |
| /category/<category_name>  | category_articles         | POST        | category.html                | category_name (str), articles (list[dict{article_id:int, title:str, date:str, popularity:int}])               | sort_by (str) (values: 'date' or 'popularity')                 |
| /search                   | search_results            | GET         | search_results.html          | query (str), results (list[dict{article_id:int, title:str, excerpt:str}])                                    | None                                                           |
| /search                   | search_results            | POST        | search_results.html          | query (str), results (list[dict{article_id:int, title:str, excerpt:str}])                                    | search_query (str)                                             |


---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- File path: templates/dashboard.html
- Page title: "News Portal"
- Elements:
  - ID: dashboard-page (Div) - Container for the dashboard page
  - ID: featured-articles (Div) - Display of featured article recommendations
  - ID: browse-articles-button (Button) - Navigate to article catalog page
  - ID: view-bookmarks-button (Button) - Navigate to bookmarks page
  - ID: trending-articles-button (Button) - Navigate to trending articles page
- Context variables:
  - featured_articles: list of dict with keys: article_id (int), title (str), author (str), date (str)
- Navigation mappings:
  - browse-articles-button: url_for('article_catalog')
  - view-bookmarks-button: url_for('bookmarks')
  - trending-articles-button: url_for('trending_articles')

---

### 2. Article Catalog Page
- File path: templates/article_catalog.html
- Page title: "Article Catalog"
- Elements:
  - ID: catalog-page (Div) - Container for the catalog page
  - ID: search-input (Input) - Field for search by title, author, keywords
  - ID: category-filter (Dropdown) - Filter by category
  - ID: articles-grid (Div) - Grid showing article cards
  - ID pattern: view-article-button-{article_id} (Button) - Button to view article details
- Context variables:
  - articles: list of dict with keys: article_id (int), title (str), author (str), category (str), date (str)
  - categories: list of strings
- Navigation mappings:
  - view-article-button-{article_id}: url_for('article_details', article_id=article_id)

---

### 3. Article Details Page
- File path: templates/article_details.html
- Page title: "Article Details"
- Elements:
  - ID: article-details-page (Div) - Container for article details page
  - ID: article-title (H1) - Article title display
  - ID: article-author (Div) - Article author display
  - ID: article-date (Div) - Article publication date display
  - ID: bookmark-button (Button) - Button to bookmark article
  - ID: article-content (Div) - Full article content section
- Context variables:
  - article: dict with keys: article_id (int), title (str), author (str), date (str), content (str)
  - is_bookmarked: bool
- Navigation mappings:
  - bookmark-button: form POST to /bookmark with article_id

---

### 4. Bookmarks Page
- File path: templates/bookmarks.html
- Page title: "My Bookmarks"
- Elements:
  - ID: bookmarks-page (Div) - Container for bookmarks page
  - ID: bookmarks-list (Div) - List of bookmarked articles with title and date
  - ID pattern: remove-bookmark-button-{bookmark_id} (Button) - Remove bookmark button
  - ID pattern: read-bookmark-button-{bookmark_id} (Button) - Read bookmarked article button
  - ID: back-to-dashboard (Button) - Navigate back to dashboard
- Context variables:
  - bookmarks: list of dict with keys: bookmark_id (int), article_id (int), article_title (str), bookmarked_date (str)
- Navigation mappings:
  - remove-bookmark-button-{bookmark_id}: form POST to /bookmark/remove/<bookmark_id>
  - read-bookmark-button-{bookmark_id}: url_for('article_details', article_id=article_id)
  - back-to-dashboard: url_for('dashboard')

---

### 5. Comments Page
- File path: templates/comments.html
- Page title: "Article Comments"
- Elements:
  - ID: comments-page (Div) - Container for comments page
  - ID: comments-list (Div) - List of comments showing article title, commenter name, and comment text
  - ID: write-comment-button (Button) - Navigate to write comment page
  - ID: filter-by-article (Dropdown) - Filter comments by article
  - ID: back-to-dashboard (Button) - Navigate back to dashboard
- Context variables:
  - comments: list of dict with keys: comment_id (int), article_id (int), article_title (str), commenter_name (str), comment_text (str)
  - articles: list of dict with keys: article_id (int), title (str)
- Navigation mappings:
  - write-comment-button: url_for('write_comment')
  - back-to-dashboard: url_for('dashboard')

---

### 6. Write Comment Page
- File path: templates/write_comment.html
- Page title: "Write a Comment"
- Elements:
  - ID: write-comment-page (Div) - Container for write comment page
  - ID: select-article (Dropdown) - Select article to comment on
  - ID: commenter-name (Input) - Input field for commenter name
  - ID: comment-text (Textarea) - Textarea for comment text
  - ID: submit-comment-button (Button) - Submit comment
- Context variables:
  - articles: list of dict with keys: article_id (int), title (str)
- Navigation mappings:
  - submit-comment-button: form POST to /comment/write

---

### 7. Trending Articles Page
- File path: templates/trending.html
- Page title: "Trending Articles"
- Elements:
  - ID: trending-page (Div) - Container for trending articles page
  - ID: trending-list (Div) - Ranked list of trending articles
  - ID: time-period-filter (Dropdown) - Filter by time period
  - ID pattern: view-article-button-{article_id} (Button) - View article details button
  - ID: back-to-dashboard (Button) - Navigate back to dashboard
- Context variables:
  - trending_articles: list of dict with keys: article_id (int), article_title (str), category (str), view_count (int), period (str)
- Navigation mappings:
  - view-article-button-{article_id}: url_for('article_details', article_id=article_id)
  - back-to-dashboard: url_for('dashboard')

---

### 8. Category Page
- File path: templates/category.html
- Page title: "Category Articles"
- Elements:
  - ID: category-page (Div) - Container for category page
  - ID: category-title (H1) - Category name display
  - ID: category-articles (Div) - List of articles in the category
  - ID: sort-by-date (Button) - Sort by date button
  - ID: sort-by-popularity (Button) - Sort by popularity button
  - ID: back-to-dashboard (Button) - Navigate back to dashboard
- Context variables:
  - category_name: str
  - articles: list of dict with keys: article_id (int), title (str), date (str), popularity (int)
- Navigation mappings:
  - sort-by-date: form POST to /category/{category_name} with sort_by='date'
  - sort-by-popularity: form POST to /category/{category_name} with sort_by='popularity'
  - back-to-dashboard: url_for('dashboard')

---

### 9. Search Results Page
- File path: templates/search_results.html
- Page title: "Search Results"
- Elements:
  - ID: search-results-page (Div) - Container for search results page
  - ID: search-query-display (Div) - Display the search query
  - ID: results-list (Div) - List of matched articles with title and excerpt
  - ID: no-results-message (Div) - Displayed if no results found
  - ID: back-to-dashboard (Button) - Navigate back to dashboard
- Context variables:
  - query: str
  - results: list of dict with keys: article_id (int), title (str), excerpt (str)
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. articles.txt
- File path: data/articles.txt
- Format (pipe-delimited):
  article_id|title|author|category|content|date|views
- Description: Stores all news articles with metadata and content
- Example rows:
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891

---

### 2. categories.txt
- File path: data/categories.txt
- Format (pipe-delimited):
  category_id|category_name|description
- Description: Stores categories of news articles
- Example rows:
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news

---

### 3. bookmarks.txt
- File path: data/bookmarks.txt
- Format (pipe-delimited):
  bookmark_id|article_id|article_title|bookmarked_date
- Description: Stores user bookmarked articles
- Example rows:
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18

---

### 4. comments.txt
- File path: data/comments.txt
- Format (pipe-delimited):
  comment_id|article_id|article_title|commenter_name|comment_text|comment_date
- Description: Stores comments on articles
- Example rows:
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19

---

### 5. trending.txt
- File path: data/trending.txt
- Format (pipe-delimited):
  article_id|article_title|category|view_count|period
- Description: Stores trending article data with view counts and periods
- Example rows:
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month

---
