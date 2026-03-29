# NewsPortal Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                         | Function Name            | HTTP Method | Template File                | Context Variables (name: type)                                                                                                                             | Form Data (POST routes)                          |
|----------------------------------|--------------------------|-------------|------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------|
| /                                | redirect_to_dashboard    | GET         | N/A (redirect)                | None                                                                                                                                                       | None                                            |
| /dashboard                       | dashboard                | GET         | dashboard.html               | featured_articles: list of dict (article_id:int, title:str, author:str, date:str),
                                                                 trending_articles: list of dict (article_id:int, title:str, category:str, view_count:int)                      | None                                            |
| /catalog                        | article_catalog          | GET         | catalog.html                 | articles: list of dict (article_id:int, title:str, author:str, date:str, category:str, thumbnail:str),
                                                      categories: list of dict (category_id:int, category_name:str)                                                            | None                                            |
| /catalog/search                 | search_results           | POST        | search_results.html          | query: str,
results: list of dict (article_id:int, title:str, excerpt:str)                                                                                         | search_query: str (from form 'search-input')    |
| /articles/<int:article_id>      | article_details          | GET         | article_details.html         | article: dict (article_id:int, title:str, author:str, date:str, content:str),
                                                                            bookmarked: bool                                                                                                   | None                                            |
| /articles/<int:article_id>/bookmark | bookmark_article        | POST        | N/A (redirect to article_details) | None                                                                                                                                                       | None                                            |
| /bookmarks                     | bookmarks                | GET         | bookmarks.html               | bookmarks: list of dict (bookmark_id:int, article_id:int, article_title:str, bookmarked_date:str)                                                            | None                                            |
| /bookmarks/<int:bookmark_id>/remove | remove_bookmark          | POST        | N/A (redirect to bookmarks) | None                                                                                                                                                       | None                                            |
| /comments                     | comments                 | GET         | comments.html                | comments: list of dict (comment_id:int, article_title:str, commenter_name:str, comment_text:str),
                                                        articles: list of dict (article_id:int, title:str)                                                                                                | None                                            |
| /comments/filter              | filter_comments           | POST        | comments.html                | selected_article_id: int,
comments: list of dict (comment_id:int, article_title:str, commenter_name:str, comment_text:str),
articles: list of dict (article_id:int, title:str)                                    | filter_article_id: int (from form 'filter-by-article') |
| /comments/write               | write_comment             | GET         | write_comment.html           | articles: list of dict (article_id:int, title:str)                                                                                                         | None                                            |
| /comments/submit              | submit_comment            | POST        | N/A (redirect to comments)  | None                                                                                                                                                       | article_id: int (from form 'select-article'),
commenter_name: str (from form 'commenter-name'),
comment_text: str (from form 'comment-text')          |
| /trending                    | trending_articles          | GET         | trending.html                | trending_articles: list of dict (article_id:int, title:str, category:str, view_count:int, rank:int),
periods: list of str (e.g., "Today", "This Week", "This Month")                                      | None                                            |
| /trending/filter             | filter_trending            | POST        | trending.html                | selected_period: str,
trending_articles: list of dict (article_id:int, title:str, category:str, view_count:int, rank:int),
periods: list of str                                      | time_period: str (from form 'time-period-filter') |
| /category/<string:category_name> | category_articles         | GET         | category.html                | category_name: str,
articles: list of dict (article_id:int, title:str, date:str, popularity:int)                                                           | None                                            |
| /category/<string:category_name>/sort/<string:sort_key> | sort_category_articles      | GET         | category.html                | category_name: str,
articles: list of dict (article_id:int, title:str, date:str, popularity:int)                                                           | None                                            |

---

## Section 2: HTML Template Specifications

### Dashboard Page Template
- File Path: templates/dashboard.html
- Page Title: News Portal

#### Elements (ID: Type - Description)
- dashboard-page: Div - Container for the dashboard page.
- featured-articles: Div - Display of featured article recommendations.
- browse-articles-button: Button - Button to navigate to Article Catalog page.
- view-bookmarks-button: Button - Button to navigate to Bookmarks page.
- trending-articles-button: Button - Button to navigate to Trending Articles page.

#### Context Variables
- featured_articles: List of dicts with fields: article_id (int), title (str), author (str), date (str)
- trending_articles: List of dicts with fields: article_id (int), title (str), category (str), view_count (int)

#### Navigation Mappings
- browse-articles-button: url_for('article_catalog')
- view-bookmarks-button: url_for('bookmarks')
- trending-articles-button: url_for('trending_articles')

---

### Article Catalog Page Template
- File Path: templates/catalog.html
- Page Title: Article Catalog

#### Elements
- catalog-page: Div - Container for the catalog page.
- search-input: Input - Field for searching articles by title, author, or keywords.
- category-filter: Dropdown - Filter articles by category.
- articles-grid: Div - Grid displaying article cards.
- view-article-button-{article_id}: Button - Button to view details of specific article.

#### Context Variables
- articles: List of dicts with fields: article_id (int), title (str), author (str), date (str), category (str), thumbnail (str)
- categories: List of dicts with fields: category_id (int), category_name (str)

#### Navigation Mappings
- view-article-button-{article_id}: url_for('article_details', article_id=article_id)

---

### Article Details Page Template
- File Path: templates/article_details.html
- Page Title: Article Details

#### Elements
- article-details-page: Div - Container for the article details page.
- article-title: H1 - Article title display.
- article-author: Div - Article author display.
- article-date: Div - Article publication date display.
- bookmark-button: Button - Button to bookmark the article.
- article-content: Div - Full article content display.

#### Context Variables
- article: Dict with fields article_id (int), title (str), author (str), date (str), content (str)
- bookmarked: Boolean indicating if article is already bookmarked

#### Navigation Mappings
- bookmark-button: Form POST to url_for('bookmark_article', article_id=article.article_id)

---

### Bookmarks Page Template
- File Path: templates/bookmarks.html
- Page Title: My Bookmarks

#### Elements
- bookmarks-page: Div - Container for bookmarks page.
- bookmarks-list: Div - List of bookmarked articles.
- remove-bookmark-button-{bookmark_id}: Button - Remove bookmark button for each bookmark.
- read-bookmark-button-{bookmark_id}: Button - Read bookmarked article button for each bookmark.
- back-to-dashboard: Button - Navigates back to dashboard.

#### Context Variables
- bookmarks: List of dicts with fields bookmark_id (int), article_id (int), article_title (str), bookmarked_date (str)

#### Navigation Mappings
- remove-bookmark-button-{bookmark_id}: Form POST to url_for('remove_bookmark', bookmark_id=bookmark_id)
- read-bookmark-button-{bookmark_id}: url_for('article_details', article_id=article_id)
- back-to-dashboard: url_for('dashboard')

---

### Comments Page Template
- File Path: templates/comments.html
- Page Title: Article Comments

#### Elements
- comments-page: Div - Container for comments page.
- comments-list: Div - List of all comments.
- write-comment-button: Button - Navigate to Write Comment page.
- filter-by-article: Dropdown - Filter comments by article.
- back-to-dashboard: Button - Navigate back to dashboard.

#### Context Variables
- comments: List of dicts with fields comment_id (int), article_title (str), commenter_name (str), comment_text (str)
- articles: List of dicts with fields article_id (int), title (str)

#### Navigation Mappings
- write-comment-button: url_for('write_comment')
- back-to-dashboard: url_for('dashboard')

---

### Write Comment Page Template
- File Path: templates/write_comment.html
- Page Title: Write a Comment

#### Elements
- write-comment-page: Div - Container for write comment page.
- select-article: Dropdown - Select article to comment on.
- commenter-name: Input - Input field for commenter name.
- comment-text: Textarea - Input field for comment text.
- submit-comment-button: Button - Submit comment.

#### Context Variables
- articles: List of dicts with fields article_id (int), title (str)

#### Navigation Mappings
- submit-comment-button: Form POST to url_for('submit_comment')

---

### Trending Articles Page Template
- File Path: templates/trending.html
- Page Title: Trending Articles

#### Elements
- trending-page: Div - Container for trending articles page.
- trending-list: Div - Ranked list of trending articles.
- time-period-filter: Dropdown - Filter articles by time period.
- view-article-button-{article_id}: Button - View article details button for each trending article.
- back-to-dashboard: Button - Navigate back to dashboard.

#### Context Variables
- trending_articles: List of dicts with fields article_id (int), title (str), category (str), view_count (int), rank (int)
- periods: List of str (time periods: Today, This Week, This Month)

#### Navigation Mappings
- view-article-button-{article_id}: url_for('article_details', article_id=article_id)
- back-to-dashboard: url_for('dashboard')

---

### Category Page Template
- File Path: templates/category.html
- Page Title: Category Articles

#### Elements
- category-page: Div - Container for category page.
- category-title: H1 - Display category name.
- category-articles: Div - List of articles in category.
- sort-by-date: Button - Sort articles by date.
- sort-by-popularity: Button - Sort articles by popularity.
- back-to-dashboard: Button - Navigate back to dashboard.

#### Context Variables
- category_name: str
- articles: List of dicts with fields article_id (int), title (str), date (str), popularity (int)

#### Navigation Mappings
- sort-by-date: url_for('sort_category_articles', category_name=category_name, sort_key='date')
- sort-by-popularity: url_for('sort_category_articles', category_name=category_name, sort_key='popularity')
- back-to-dashboard: url_for('dashboard')

---

### Search Results Page Template
- File Path: templates/search_results.html
- Page Title: Search Results

#### Elements
- search-results-page: Div - Container for search results page.
- search-query-display: Div - Display the search query.
- results-list: Div - List of articles matching search.
- no-results-message: Div - Message indicating no results found.
- back-to-dashboard: Button - Navigate back to dashboard.

#### Context Variables
- query: str
- results: List of dicts with fields article_id (int), title (str), excerpt (str)

#### Navigation Mappings
- back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. Articles Data
- File Path: data/articles.txt
- Format: pipe-delimited (`|`)
- Fields (in order):
  1. article_id (int)
  2. title (str)
  3. author (str)
  4. category (str)
  5. content (str)
  6. date (str, format YYYY-MM-DD)
  7. views (int)

- Description: Stores all news articles with metadata and view counts.

- Example Rows:
  ```
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891
  ```

### 2. Categories Data
- File Path: data/categories.txt
- Format: pipe-delimited (`|`)
- Fields (in order):
  1. category_id (int)
  2. category_name (str)
  3. description (str)

- Description: Contains category information used for filtering and navigation.

- Example Rows:
  ```
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news
  ```

### 3. Bookmarks Data
- File Path: data/bookmarks.txt
- Format: pipe-delimited (`|`)
- Fields (in order):
  1. bookmark_id (int)
  2. article_id (int)
  3. article_title (str)
  4. bookmarked_date (str, format YYYY-MM-DD)

- Description: Stores user bookmarks of articles.

- Example Rows:
  ```
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18
  ```

### 4. Comments Data
- File Path: data/comments.txt
- Format: pipe-delimited (`|`)
- Fields (in order):
  1. comment_id (int)
  2. article_id (int)
  3. article_title (str)
  4. commenter_name (str)
  5. comment_text (str)
  6. comment_date (str, format YYYY-MM-DD)

- Description: Stores comments made on articles.

- Example Rows:
  ```
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19
  ```

### 5. Trending Data
- File Path: data/trending.txt
- Format: pipe-delimited (`|`)
- Fields (in order):
  1. article_id (int)
  2. article_title (str)
  3. category (str)
  4. view_count (int)
  5. period (str) (values: Today, This Week, This Month)

- Description: Stores data about trending articles for different time periods.

- Example Rows:
  ```
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month
  ```

---

**End of Design Specification**
