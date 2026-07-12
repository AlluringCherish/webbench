# NewsPortal Design Specifications

---

## Section 1: Flask Routes Specification

| Route Path                         | Flask Function Name         | HTTP Method | Template File                  | Context Variables (name: type)                                   | Notes (form data for POST)                                    |
|-----------------------------------|-----------------------------|-------------|-------------------------------|-----------------------------------------------------------------|---------------------------------------------------------------|
| /                                 | root_redirect                | GET         | None (Redirect)                | None                                                            | Redirects to /dashboard                                        |
| /dashboard                        | dashboard_page              | GET         | templates/dashboard.html       | featured_articles: list(dict), trending_articles: list(dict)    |                                                                 |
| /catalog                         | article_catalog             | GET         | templates/catalog.html         | articles: list(dict), categories: list(dict), search_query: str |                                                                 |
| /article/<int:article_id>         | article_details             | GET         | templates/article_details.html | article: dict                                                  |                                                                 |
| /article/<int:article_id>/bookmark| bookmark_article            | POST        | None (Redirect to article_details) | None                                                         | Form data: hidden or CSRF token not specified; trigger bookmark action |
| /bookmarks                       | bookmarks_page              | GET         | templates/bookmarks.html       | bookmarks: list(dict)                                          |                                                                 |
| /bookmarks/remove/<int:bookmark_id>| remove_bookmark             | POST        | None (Redirect to bookmarks)   | None                                                            | Form data: none, bookmark removal by ID                        |
| /comments                       | comments_page               | GET         | templates/comments.html        | comments: list(dict), articles: list(dict)                     |                                                                 |
| /comments/write                 | write_comment               | GET         | templates/write_comment.html   | articles: list(dict)                                           |                                                                 |
| /comments/write                 | submit_comment              | POST        | None (Redirect to comments)    | None                                                            | Form data: article_id (int), commenter_name (str), comment_text (str) |
| /trending                      | trending_articles           | GET         | templates/trending.html        | trending_articles: list(dict), time_period: str                |                                                                 |
| /category/<string:category_name>  | category_page               | GET         | templates/category.html        | category_name: str, category_articles: list(dict)             |                                                                 |
| /search                         | search_results              | GET         | templates/search_results.html  | search_query: str, search_results: list(dict)                  |                                                                 |

Notes:
- All list(dict) context variables refer to lists of data dicts representing objects like articles, bookmarks, comments, etc.
- Redirect routes do not render templates but redirect user appropriately.

---

## Section 2: HTML Template Specifications

### Template: templates/dashboard.html
- Page Title: News Portal
- <title> and <h1>: "News Portal"
- Element IDs and descriptions:
  - dashboard-page: Div container for dashboard
  - featured-articles: Div for featured article recommendations
  - browse-articles-button: Button to navigate to Article Catalog page
  - view-bookmarks-button: Button to navigate to Bookmarks page
  - trending-articles-button: Button to navigate to Trending Articles page
- Context variables:
  - featured_articles (list of dicts): Each dict with keys - article_id (int), title (str), excerpt (str), author (str), date (str)
  - trending_articles (list of dicts): Each dict with keys - article_id (int), title (str), category (str), view_count (int)
- Navigation mappings:
  - browse-articles-button -> url_for('article_catalog')
  - view-bookmarks-button -> url_for('bookmarks_page')
  - trending-articles-button -> url_for('trending_articles')

---

### Template: templates/catalog.html
- Page Title: Article Catalog
- <title> and <h1>: "Article Catalog"
- Element IDs and descriptions:
  - catalog-page: Div container for catalog page
  - search-input: Input field for search queries
  - category-filter: Dropdown for filtering articles by category
  - articles-grid: Div grid displaying article cards
  - view-article-button-{article_id}: Button on each article card to view details
- Context variables:
  - articles (list of dicts): Each dict with keys - article_id (int), title (str), author (str), category (str), date (str), excerpt (str)
  - categories (list of dicts): Each dict with keys - category_id (int), category_name (str), description (str)
  - search_query (str): Current search string
- Navigation mappings:
  - view-article-button-{article_id} -> url_for('article_details', article_id=article_id)

---

### Template: templates/article_details.html
- Page Title: Article Details
- <title>: "Article Details"
- <h1> (ID: article-title): displays article title
- Element IDs and descriptions:
  - article-details-page: Div container
  - article-title: H1 for article title
  - article-author: Div displaying article author
  - article-date: Div displaying article date
  - bookmark-button: Button to bookmark this article
  - article-content: Div displaying full article content
- Context variables:
  - article (dict): Fields - article_id (int), title (str), author (str), category (str), content (str), date (str), views (int)
- Navigation mappings:
  - bookmark-button triggers POST to url_for('bookmark_article', article_id=article.article_id)

---

### Template: templates/bookmarks.html
- Page Title: My Bookmarks
- <title> and <h1>: "My Bookmarks"
- Element IDs and descriptions:
  - bookmarks-page: Div container
  - bookmarks-list: Div listing bookmarked articles
  - remove-bookmark-button-{bookmark_id}: Button to remove bookmark
  - read-bookmark-button-{bookmark_id}: Button to read bookmarked article
  - back-to-dashboard: Button to return to dashboard
- Context variables:
  - bookmarks (list of dicts): Each dict with keys - bookmark_id (int), article_id (int), article_title (str), bookmarked_date (str)
- Navigation mappings:
  - remove-bookmark-button-{bookmark_id} triggers POST to url_for('remove_bookmark', bookmark_id=bookmark_id)
  - read-bookmark-button-{bookmark_id} -> url_for('article_details', article_id=article_id)
  - back-to-dashboard -> url_for('dashboard_page')

---

### Template: templates/comments.html
- Page Title: Article Comments
- <title> and <h1>: "Article Comments"
- Element IDs and descriptions:
  - comments-page: Div container
  - comments-list: Div listing all comments
  - write-comment-button: Button to navigate to write comment page
  - filter-by-article: Dropdown to filter comments by article
  - back-to-dashboard: Button to navigate back to dashboard
- Context variables:
  - comments (list of dicts): Each dict with keys - comment_id (int), article_id (int), article_title (str), commenter_name (str), comment_text (str), comment_date (str)
  - articles (list of dicts): Each dict with keys - article_id (int), title (str)
- Navigation mappings:
  - write-comment-button -> url_for('write_comment')
  - back-to-dashboard -> url_for('dashboard_page')

---

### Template: templates/write_comment.html
- Page Title: Write a Comment
- <title> and <h1>: "Write a Comment"
- Element IDs and descriptions:
  - write-comment-page: Div container
  - select-article: Dropdown to select article
  - commenter-name: Input text field
  - comment-text: Textarea for comment content
  - submit-comment-button: Button to submit comment
- Context variables:
  - articles (list of dicts): Each dict with keys - article_id (int), title (str)
- Navigation mappings:
  - submit-comment-button: triggers POST submitting form data (article_id, commenter_name, comment_text) to url_for('submit_comment')

---

### Template: templates/trending.html
- Page Title: Trending Articles
- <title> and <h1>: "Trending Articles"
- Element IDs and descriptions:
  - trending-page: Div container
  - trending-list: Div listing trending articles ranked
  - time-period-filter: Dropdown filter by time period (Today, This Week, This Month)
  - view-article-button-{article_id}: Button to view article details
  - back-to-dashboard: Button to navigate back
- Context variables:
  - trending_articles (list of dicts): Each dict with keys - article_id (int), article_title (str), category (str), view_count (int), period (str)
  - time_period (str): Current filter value
- Navigation mappings:
  - view-article-button-{article_id} -> url_for('article_details', article_id=article_id)
  - back-to-dashboard -> url_for('dashboard_page')

---

### Template: templates/category.html
- Page Title: Category Articles
- <title> and <h1>: "Category Articles" (with category_name value shown in h1 with ID category-title)
- Element IDs and descriptions:
  - category-page: Div container
  - category-title: H1 displaying category_name
  - category-articles: Div listing articles of this category
  - sort-by-date: Button to sort articles by date
  - sort-by-popularity: Button to sort articles by popularity
  - back-to-dashboard: Button to return to dashboard
- Context variables:
  - category_name (str): Selected category name
  - category_articles (list of dicts): Each dict with keys - article_id (int), title (str), author (str), date (str), views (int)
- Navigation mappings:
  - sort-by-date: triggers reload sorted by date
  - sort-by-popularity: triggers reload sorted by popularity
  - back-to-dashboard -> url_for('dashboard_page')

---

### Template: templates/search_results.html
- Page Title: Search Results
- <title> and <h1>: "Search Results"
- Element IDs and descriptions:
  - search-results-page: Div container
  - search-query-display: Div showing the search query string
  - results-list: Div listing articles matching the search
  - no-results-message: Div showing "no results" message when none found
  - back-to-dashboard: Button to return to dashboard
- Context variables:
  - search_query (str): Query string
  - search_results (list of dicts): Each dict with keys - article_id (int), title (str), excerpt (str)
- Navigation mappings:
  - back-to-dashboard -> url_for('dashboard_page')

---

## Section 3: Data File Schemas

### File: data/articles.txt
- Format: pipe-delimited (|)
- Fields in exact order:
  1. article_id (int)
  2. title (str)
  3. author (str)
  4. category (str)
  5. content (str)
  6. date (str, ISO YYYY-MM-DD)
  7. views (int)
- Description: Stores detailed article data.
- Example rows:
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891

---

### File: data/categories.txt
- Format: pipe-delimited (|)
- Fields in exact order:
  1. category_id (int)
  2. category_name (str)
  3. description (str)
- Description: Contains news categories with descriptions.
- Example rows:
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news

---

### File: data/bookmarks.txt
- Format: pipe-delimited (|)
- Fields in exact order:
  1. bookmark_id (int)
  2. article_id (int)
  3. article_title (str)
  4. bookmarked_date (str, ISO YYYY-MM-DD)
- Description: Stores user bookmarks for articles.
- Example rows:
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18

---

### File: data/comments.txt
- Format: pipe-delimited (|)
- Fields in exact order:
  1. comment_id (int)
  2. article_id (int)
  3. article_title (str)
  4. commenter_name (str)
  5. comment_text (str)
  6. comment_date (str, ISO YYYY-MM-DD)
- Description: Stores comments made on articles.
- Example rows:
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19

---

### File: data/trending.txt
- Format: pipe-delimited (|)
- Fields in exact order:
  1. article_id (int)
  2. article_title (str)
  3. category (str)
  4. view_count (int)
  5. period (str)
- Description: Lists trending articles by views and time period.
- Example rows:
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month

---

End of design specification.
