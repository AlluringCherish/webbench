# NewsPortal Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                  | Flask Function Name       | HTTP Method | Template File               | Context Variables (name:type)                                  | Form Data (POST)                             |
|-----------------------------|--------------------------|-------------|-----------------------------|----------------------------------------------------------------|----------------------------------------------|
| /                           | root_redirect             | GET         | N/A (Redirect to /dashboard) | None                                                           | None                                         |
| /dashboard                  | dashboard_page            | GET         | dashboard.html              | featured_articles:list(dict), trending_articles:list(dict)    | None                                         |
| /catalog                   | article_catalog_page       | GET         | catalog.html                | articles:list(dict), categories:list(dict),                       | None                                         |
| /article/&lt;int:article_id&gt;         | article_details_page       | GET         | article_details.html        | article:dict                                                  | None                                         |
| /article/&lt;int:article_id&gt;/bookmark | bookmark_article          | POST        | N/A (Redirect back to article details) | None                                                           | article_id:int (from URL)                     |
| /bookmarks                 | bookmarks_page             | GET         | bookmarks.html              | bookmarks:list(dict)                                        | None                                         |
| /bookmark/&lt;int:bookmark_id&gt;/remove | remove_bookmark           | POST        | N/A (Redirect back to bookmarks) | None                                                           | bookmark_id:int (from URL)                     |
| /comments                  | comments_page              | GET         | comments.html               | comments:list(dict), articles:list(dict)                       | None                                         |
| /comments/write            | write_comment_page         | GET         | write_comment.html          | articles:list(dict)                                           | None                                         |
| /comments/submit           | submit_comment             | POST        | N/A (Redirect to comments)  | None                                                           | commenter_name:str, comment_text:str, article_id:int, from form|
| /trending                  | trending_articles_page     | GET         | trending.html               | trending_articles:list(dict)                                  | None                                         |
| /category/&lt;string:category_name&gt;     | category_articles_page     | GET         | category.html               | category:str, articles:list(dict)                            | None                                         |
| /search                   | search_results_page         | GET         | search_results.html         | query:str, results:list(dict)                                | None                                         |

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- File Path: templates/dashboard.html
- Page Title: "News Portal"
- <title> and <h1>: "News Portal"
- Element IDs:
  - dashboard-page (Div): Container for dashboard page
  - featured-articles (Div): Display of featured articles
  - browse-articles-button (Button): Navigate to article catalog page
  - view-bookmarks-button (Button): Navigate to bookmarks page
  - trending-articles-button (Button): Navigate to trending articles page
- Context Variables:
  - featured_articles: list of dict with keys [article_id:int, title:str, author:str, date:str]
  - trending_articles: list of dict with keys [article_id:int, title:str, category:str, view_count:int]
- Navigation via url_for():
  - browse-articles-button navigates to url_for('article_catalog_page')
  - view-bookmarks-button navigates to url_for('bookmarks_page')
  - trending-articles-button navigates to url_for('trending_articles_page')

### 2. Article Catalog Page
- File Path: templates/catalog.html
- Page Title: "Article Catalog"
- <title> and <h1>: "Article Catalog"
- Element IDs:
  - catalog-page (Div): Container for catalog page
  - search-input (Input): Search field for articles
  - category-filter (Dropdown): Filter articles by category
  - articles-grid (Div): Grid displaying article cards
  - view-article-button-{article_id} (Button): View details for each article
- Context Variables:
  - articles: list of dict with keys [article_id:int, title:str, author:str, category:str, date:str]
  - categories: list of dict with keys [category_id:int, category_name:str]
- Navigation:
  - view-article-button-{article_id} link to url_for('article_details_page', article_id=article_id)

### 3. Article Details Page
- File Path: templates/article_details.html
- Page Title: "Article Details"
- <title> and <h1>: "Article Details"
- Element IDs:
  - article-details-page (Div): Container for article details
  - article-title (H1): Article title
  - article-author (Div): Article author
  - article-date (Div): Article publication date
  - bookmark-button (Button): Bookmark the article
  - article-content (Div): Full article content
- Context Variables:
  - article: dict with keys [article_id:int, title:str, author:str, category:str, content:str, date:str, views:int]
- Navigation:
  - bookmark-button triggers POST to url_for('bookmark_article', article_id=article.article_id)

### 4. Bookmarks Page
- File Path: templates/bookmarks.html
- Page Title: "My Bookmarks"
- <title> and <h1>: "My Bookmarks"
- Element IDs:
  - bookmarks-page (Div): Container for bookmarks page
  - bookmarks-list (Div): List of bookmarked articles
  - remove-bookmark-button-{bookmark_id} (Button): Remove bookmark by id
  - read-bookmark-button-{bookmark_id} (Button): Read bookmarked article
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - bookmarks: list of dict with keys [bookmark_id:int, article_id:int, article_title:str, bookmarked_date:str]
- Navigation:
  - remove-bookmark-button-{bookmark_id} triggers POST to url_for('remove_bookmark', bookmark_id=bookmark_id)
  - read-bookmark-button-{bookmark_id} links to url_for('article_details_page', article_id=article_id)
  - back-to-dashboard links to url_for('dashboard_page')

### 5. Comments Page
- File Path: templates/comments.html
- Page Title: "Article Comments"
- <title> and <h1>: "Article Comments"
- Element IDs:
  - comments-page (Div): Container for comments page
  - comments-list (Div): List all comments
  - write-comment-button (Button): Navigate to write comment page
  - filter-by-article (Dropdown): Filter comments by article
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - comments: list of dict with keys [comment_id:int, article_id:int, article_title:str, commenter_name:str, comment_text:str, comment_date:str]
  - articles: list of dict with keys [article_id:int, title:str]
- Navigation:
  - write-comment-button links to url_for('write_comment_page')
  - back-to-dashboard links to url_for('dashboard_page')

### 6. Write Comment Page
- File Path: templates/write_comment.html
- Page Title: "Write a Comment"
- <title> and <h1>: "Write a Comment"
- Element IDs:
  - write-comment-page (Div): Container for write comment page
  - select-article (Dropdown): Select article to comment on
  - commenter-name (Input): Input for commenter name
  - comment-text (Textarea): Text area for comment text
  - submit-comment-button (Button): Submit comment
- Context Variables:
  - articles: list of dict with keys [article_id:int, title:str]
- Navigation:
  - submit-comment-button triggers POST to url_for('submit_comment')

### 7. Trending Articles Page
- File Path: templates/trending.html
- Page Title: "Trending Articles"
- <title> and <h1>: "Trending Articles"
- Element IDs:
  - trending-page (Div): Container for trending articles
  - trending-list (Div): Ranked list of trending articles
  - time-period-filter (Dropdown): Filter by time period
  - view-article-button-{article_id} (Button): View article details
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - trending_articles: list of dict with keys [article_id:int, article_title:str, category:str, view_count:int, period:str]
- Navigation:
  - view-article-button-{article_id} links to url_for('article_details_page', article_id=article_id)
  - back-to-dashboard links to url_for('dashboard_page')

### 8. Category Page
- File Path: templates/category.html
- Page Title: "Category Articles"
- <title> and <h1>: "Category Articles"
- Element IDs:
  - category-page (Div): Container for category page
  - category-title (H1): Display category name
  - category-articles (Div): List of articles
  - sort-by-date (Button): Sort articles by date
  - sort-by-popularity (Button): Sort articles by popularity
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - category: str (category name)
  - articles: list of dict with keys [article_id:int, title:str, author:str, date:str, views:int]
- Navigation:
  - back-to-dashboard links to url_for('dashboard_page')

### 9. Search Results Page
- File Path: templates/search_results.html
- Page Title: "Search Results"
- <title> and <h1>: "Search Results"
- Element IDs:
  - search-results-page (Div): Container for search results
  - search-query-display (Div): Display the search query
  - results-list (Div): List of results
  - no-results-message (Div): Message displayed if no results
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - query: str (search query)
  - results: list of dict with keys [article_id:int, title:str, excerpt:str]
- Navigation:
  - back-to-dashboard links to url_for('dashboard_page')

---

## Section 3: Data File Schemas

### 1. Articles Data
- File Path: data/articles.txt
- Format: Pipe-delimited (|)
- Fields (in order): article_id|title|author|category|content|date|views
- Description: Stores all news articles with metadata and content.
- Example Rows:
  - 1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  - 2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  - 3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891

### 2. Categories Data
- File Path: data/categories.txt
- Format: Pipe-delimited (|)
- Fields (in order): category_id|category_name|description
- Description: Stores all news article categories.
- Example Rows:
  - 1|Technology|Latest tech news and innovations
  - 2|Sports|Sports news and event coverage
  - 3|Business|Business and finance news

### 3. Bookmarks Data
- File Path: data/bookmarks.txt
- Format: Pipe-delimited (|)
- Fields (in order): bookmark_id|article_id|article_title|bookmarked_date
- Description: Stores bookmarked articles by users.
- Example Rows:
  - 1|1|Breaking: New Technology Breakthrough|2025-01-20
  - 2|3|Business: Market Trends Analysis|2025-01-18

### 4. Comments Data
- File Path: data/comments.txt
- Format: Pipe-delimited (|)
- Fields (in order): comment_id|article_id|article_title|commenter_name|comment_text|comment_date
- Description: Stores comments made on articles.
- Example Rows:
  - 1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  - 2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19

### 5. Trending Data
- File Path: data/trending.txt
- Format: Pipe-delimited (|)
- Fields (in order): article_id|article_title|category|view_count|period
- Description: Stores trending articles ranked by views and period.
- Example Rows:
  - 1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  - 2|Sports: Championship Victory|Sports|3210|This Week
  - 3|Business: Market Trends Analysis|Business|2891|This Month

---

End of Design Specification.
