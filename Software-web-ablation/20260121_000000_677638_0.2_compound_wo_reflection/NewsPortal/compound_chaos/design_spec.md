# NewsPortal Web Application Design Specification

---

## 1. Flask Routes Specification

| Route Path                         | Function Name              | HTTP Method | Template File Rendered       | Context Variables (name:type)                                                        | Expected Form Data (POST routes)               |
|----------------------------------|----------------------------|-------------|------------------------------|--------------------------------------------------------------------------------------|------------------------------------------------|
| /                                | root_redirect              | GET         | None (redirect to dashboard) | None                                                                                 | None                                           |
| /dashboard                       | dashboard                 | GET         | dashboard.html               | featured_articles: list(dict), trending_articles: list(dict)                         | None                                           |
| /articles                       | article_catalog           | GET         | article_catalog.html         | articles: list(dict), categories: list(dict), search_query: str (optional), category_filter: str (optional) | None                                           |
| /article/<int:article_id>       | article_details           | GET         | article_details.html         | article: dict, is_bookmarked: bool                                                     | None                                           |
| /article/<int:article_id>/bookmark | bookmark_article         | POST        | None (redirect or JSON)      | None                                                                                 | None                                           |
| /bookmarks                      | bookmarks                 | GET         | bookmarks.html               | bookmarks: list(dict)                                                                | None                                           |
| /bookmarks/remove/<int:bookmark_id> | remove_bookmark          | POST        | None (redirect)              | None                                                                                 | None                                           |
| /comments                      | comments                  | GET         | comments.html                | comments: list(dict), articles: list(dict), filter_article_id: int (optional)         | None                                           |
| /comments/write                | write_comment             | GET         | write_comment.html           | articles: list(dict)                                                                 | None                                           |
| /comments/write                | submit_comment            | POST        | None (redirect to comments) | None                                                                                 | article_id: int, commenter_name: str, comment_text: str |
| /trending                     | trending_articles         | GET         | trending_articles.html       | trending_articles: list(dict), time_period: str (optional)                           | None                                           |
| /category/<string:category_name> | category_articles         | GET         | category.html                | category_name: str, articles: list(dict)                                             | None                                           |
| /search                       | search_results            | GET         | search_results.html          | query: str, results: list(dict)                                                     | None                                           |

---

## 2. HTML Template Specifications

### Dashboard Page
- File Path: templates/dashboard.html
- Page Title: News Portal
- Element IDs:
  - dashboard-page: Div - Container for the dashboard page.
  - featured-articles: Div - Display of featured article recommendations.
  - browse-articles-button: Button - Button to navigate to article catalog page.
  - view-bookmarks-button: Button - Button to navigate to bookmarks page.
  - trending-articles-button: Button - Button to navigate to trending articles page.
- Context Variables:
  - featured_articles: list of dicts with keys: article_id (int), title (str), author (str), date (str)
  - trending_articles: list of dicts with keys: article_id (int), title (str), category (str), view_count (int)
- Navigation:
  - browse-articles-button -> url_for('article_catalog')
  - view-bookmarks-button -> url_for('bookmarks')
  - trending-articles-button -> url_for('trending_articles')

---

### Article Catalog Page
- File Path: templates/article_catalog.html
- Page Title: Article Catalog
- Element IDs:
  - catalog-page: Div - Container for the catalog page.
  - search-input: Input - Field to search articles by title, author, or keywords.
  - category-filter: Dropdown - Dropdown to filter by category.
  - articles-grid: Div - Grid displaying article cards.
  - view-article-button-{article_id}: Button - Button to view article details.
- Context Variables:
  - articles: list of dicts with keys: article_id (int), title (str), author (str), date (str), category (str), content (str)
  - categories: list of dicts with keys: category_id (int), category_name (str), description (str)
  - search_query: str (optional)
  - category_filter: str (optional)
- Navigation:
  - view-article-button-{article_id} -> url_for('article_details', article_id=article_id)

---

### Article Details Page
- File Path: templates/article_details.html
- Page Title: Article Details
- Element IDs:
  - article-details-page: Div - Container for the article details page.
  - article-title: H1 - Display article title.
  - article-author: Div - Display article author.
  - article-date: Div - Display article publication date.
  - bookmark-button: Button - Button to bookmark the article.
  - article-content: Div - Full article content display.
- Context Variables:
  - article: dict with keys: article_id (int), title (str), author (str), date (str), content (str), category (str)
  - is_bookmarked: bool
- Navigation:
  - bookmark-button: POST form to route url_for('bookmark_article', article_id=article['article_id'])

---

### Bookmarks Page
- File Path: templates/bookmarks.html
- Page Title: My Bookmarks
- Element IDs:
  - bookmarks-page: Div - Container for the bookmarks page.
  - bookmarks-list: Div - List displaying bookmarked articles.
  - remove-bookmark-button-{bookmark_id}: Button - Remove bookmark.
  - read-bookmark-button-{bookmark_id}: Button - Read bookmarked article.
  - back-to-dashboard: Button - Navigate back to dashboard.
- Context Variables:
  - bookmarks: list of dicts with keys: bookmark_id (int), article_id (int), article_title (str), bookmarked_date (str)
- Navigation:
  - remove-bookmark-button-{bookmark_id} -> POST form to url_for('remove_bookmark', bookmark_id=bookmark_id)
  - read-bookmark-button-{bookmark_id} -> url_for('article_details', article_id=article_id)
  - back-to-dashboard -> url_for('dashboard')

---

### Comments Page
- File Path: templates/comments.html
- Page Title: Article Comments
- Element IDs:
  - comments-page: Div - Container for the comments page.
  - comments-list: Div - List of comments.
  - write-comment-button: Button - Navigate to write comment page.
  - filter-by-article: Dropdown - Filter comments by article.
  - back-to-dashboard: Button - Navigate back to dashboard.
- Context Variables:
  - comments: list of dicts with keys: comment_id (int), article_id (int), article_title (str), commenter_name (str), comment_text (str), comment_date (str)
  - articles: list of dicts with keys: article_id (int), title (str)
  - filter_article_id: int (optional)
- Navigation:
  - write-comment-button -> url_for('write_comment')
  - back-to-dashboard -> url_for('dashboard')

---

### Write Comment Page
- File Path: templates/write_comment.html
- Page Title: Write a Comment
- Element IDs:
  - write-comment-page: Div - Container for the write comment page.
  - select-article: Dropdown - Select article to comment on.
  - commenter-name: Input - Input for commenter name.
  - comment-text: Textarea - Input for comment text.
  - submit-comment-button: Button - Submit comment.
- Context Variables:
  - articles: list of dicts with keys: article_id (int), title (str)
- Navigation:
  - submit-comment-button -> POST form to url_for('submit_comment')

---

### Trending Articles Page
- File Path: templates/trending_articles.html
- Page Title: Trending Articles
- Element IDs:
  - trending-page: Div - Container for trending articles.
  - trending-list: Div - Ranked list of trending articles.
  - time-period-filter: Dropdown - Filter by time period.
  - view-article-button-{article_id}: Button - View article details.
  - back-to-dashboard: Button - Navigate back to dashboard.
- Context Variables:
  - trending_articles: list of dicts with keys: article_id (int), article_title (str), category (str), view_count (int), period (str)
  - time_period: str (optional)
- Navigation:
  - view-article-button-{article_id} -> url_for('article_details', article_id=article_id)
  - back-to-dashboard -> url_for('dashboard')

---

### Category Page
- File Path: templates/category.html
- Page Title: Category Articles
- Element IDs:
  - category-page: Div - Container for category articles.
  - category-title: H1 - Display category name.
  - category-articles: Div - List of articles in the category.
  - sort-by-date: Button - Sort articles by date.
  - sort-by-popularity: Button - Sort articles by popularity.
  - back-to-dashboard: Button - Navigate back to dashboard.
- Context Variables:
  - category_name: str
  - articles: list of dicts with keys: article_id (int), title (str), author (str), date (str), views (int), content (str), category (str)
- Navigation:
  - sort-by-date -> triggers sorting logic in frontend/backend
  - sort-by-popularity -> triggers sorting logic in frontend/backend
  - back-to-dashboard -> url_for('dashboard')

---

### Search Results Page
- File Path: templates/search_results.html
- Page Title: Search Results
- Element IDs:
  - search-results-page: Div - Container for search results.
  - search-query-display: Div - Display the search query.
  - results-list: Div - List of search results.
  - no-results-message: Div - Message if no results found.
  - back-to-dashboard: Button - Navigate back to dashboard.
- Context Variables:
  - query: str
  - results: list of dicts with keys: article_id (int), title (str), excerpt (str)
- Navigation:
  - back-to-dashboard -> url_for('dashboard')

---

## 3. Data File Schemas

### Articles Data
- File Path: data/articles.txt
- Format (pipe-delimited):
  article_id|title|author|category|content|date|views
- Content: Stores articles with their metadata and content.
- Example Rows:
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891

---

### Categories Data
- File Path: data/categories.txt
- Format (pipe-delimited):
  category_id|category_name|description
- Content: Lists categories available for articles.
- Example Rows:
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news

---

### Bookmarks Data
- File Path: data/bookmarks.txt
- Format (pipe-delimited):
  bookmark_id|article_id|article_title|bookmarked_date
- Content: Stores user bookmarks with reference to articles.
- Example Rows:
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18

---

### Comments Data
- File Path: data/comments.txt
- Format (pipe-delimited):
  comment_id|article_id|article_title|commenter_name|comment_text|comment_date
- Content: Stores comments for articles with commenter info.
- Example Rows:
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19

---

### Trending Data
- File Path: data/trending.txt
- Format (pipe-delimited):
  article_id|article_title|category|view_count|period
- Content: Stores trending article stats with time period info.
- Example Rows:
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month

---

# End of Design Specification
