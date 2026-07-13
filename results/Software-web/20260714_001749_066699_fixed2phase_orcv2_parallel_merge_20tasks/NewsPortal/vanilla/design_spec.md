# NewsPortal Design Specification

---

## Section 1: Consolidated Flask Routes and Data Schemas

### 1. Dashboard Page
- **Route:** `/` 
- **Methods:** GET
- **Function:** `dashboard()`
- **Behavior:**
  - Reads `articles.txt` to fetch featured articles.
  - Reads `trending.txt` for trending articles.
  - Returns a rendered template (dashboard.html) or JSON containing featured & trending articles summary.

### 2. Article Catalog Page
- **Route:** `/articles` 
- **Methods:** GET
- **Function:** `article_catalog()`
- **Inputs:** Optional query parameters:
  - `search` (string): search query to filter articles by title, author, or keywords.
  - `category` (string): category name filter.
- **Behavior:**
  - Reads `articles.txt` to list articles filtered and/or searched.
  - Returns all articles matching filters.
  - Renders template: `article_catalog.html` with UI elements to support search-input, category-filter, articles-grid.

### 3. Article Details Page
- **Route:** `/article/<int:article_id>`
- **Methods:** GET
- **Function:** `article_details(article_id)`
- **Behavior:**
  - Reads `articles.txt` to display full article details.
  - Increments and updates the 'views' count for the article in `articles.txt` (write-back updated views).
  - Returns the article detail data.
  - Renders template: `article_details.html` with elements including article-title, article-author, article-date, bookmark-button, article-content.

### 4. Bookmark an Article
- **Route:** `/bookmark` 
- **Methods:** POST
- **Function:** `add_bookmark()`
- **Inputs:** JSON or form data with `article_id`.
- **Behavior:**
  - Reads `articles.txt` to get article title for the given `article_id`.
  - Reads `bookmarks.txt` to check if bookmark exists.
  - If not, appends new bookmark with new `bookmark_id` (auto-increment), current date.
  - Writes updated `bookmarks.txt` file.
  - Returns success status.

### 5. Remove Bookmark
- **Route:** `/bookmark/<int:bookmark_id>`
- **Methods:** DELETE
- **Function:** `remove_bookmark(bookmark_id)`
- **Behavior:**
  - Reads `bookmarks.txt`, removes bookmark record with `bookmark_id`.
  - Writes updated `bookmarks.txt`.
  - Returns success status.

### 6. Bookmarks Page
- **Route:** `/bookmarks`
- **Methods:** GET
- **Function:** `view_bookmarks()`
- **Behavior:**
  - Reads `bookmarks.txt` to fetch all bookmarks.
  - Returns list of bookmarks.
  - Renders template: `bookmarks.html` with UI elements bookmarks-list, remove-bookmark-button-{bookmark_id}, read-bookmark-button-{bookmark_id}, back-to-dashboard.

### 7. Comments Page
- **Route:** `/comments`
- **Methods:** GET
- **Function:** `comments_list()`
- **Inputs:** Optional query parameter `article_id` for filtering.
- **Behavior:**
  - Reads `comments.txt` and optionally filters by article_id.
  - Returns all or filtered comments.
  - Renders template: `comments.html` with comments-list, write-comment-button, filter-by-article, back-to-dashboard.

### 8. Write Comment Page (Submission)
- **Route:** `/comment`
- **Methods:** POST
- **Function:** `add_comment()`
- **Inputs:** JSON or form data with `article_id`, `commenter_name`, `comment_text`.
- **Behavior:**
  - Reads `articles.txt` to get article title.
  - Reads `comments.txt` to determine next `comment_id`.
  - Adds comment with current date.
  - Writes updated `comments.txt`.
  - Returns success status.
  - The write comment page itself is served via client navigation; submission handled here.

### 9. Trending Articles Page
- **Route:** `/trending`
- **Methods:** GET
- **Function:** `trending_articles()`
- **Inputs:** Optional query parameter `period` (Today, This Week, This Month).
- **Behavior:**
  - Reads `trending.txt`, filters by period.
  - Returns trending articles list.
  - Renders template: `trending.html` with trending-list, time-period-filter, view-article-button-{article_id}, back-to-dashboard.

### 10. Category Page
- **Route:** `/category/<string:category_name>`
- **Methods:** GET
- **Function:** `category_articles(category_name)`
- **Inputs:** Optional query parameter `sort_by` (date or popularity/views).
- **Behavior:**
  - Reads `articles.txt`, filters by category.
  - Sorts by date or views as per query.
  - Returns list of articles.
  - Renders template: `category.html` with category-title, category-articles, sort-by-date, sort-by-popularity, back-to-dashboard.

### 11. Search Results Page
- **Route:** `/search`
- **Methods:** GET
- **Function:** `search_articles()`
- **Inputs:** Query parameter `q` (search text).
- **Behavior:**
  - Reads `articles.txt`.
  - Filters articles matching query in title, author, or keywords in content.
  - Returns matched articles.
  - Renders template: `search_results.html` with search-query-display, results-list, no-results-message, back-to-dashboard.

---

## Section 2: Unified Frontend Template Specifications

### Dashboard Page - dashboard.html
- Page Title: News Portal
- Container: `dashboard-page`
- Displays:
  - `featured-articles`
  - `browse-articles-button`
  - `view-bookmarks-button`
  - `trending-articles-button`

### Article Catalog Page - article_catalog.html
- Page Title: Article Catalog
- Container: `catalog-page`
- Displays:
  - `search-input`
  - `category-filter`
  - `articles-grid` with dynamic buttons `view-article-button-{article_id}`

### Article Details Page - article_details.html
- Page Title: Article Details
- Container: `article-details-page`
- Displays:
  - `article-title` (H1)
  - `article-author`
  - `article-date`
  - `bookmark-button`
  - `article-content`

### Bookmarks Page - bookmarks.html
- Page Title: My Bookmarks
- Container: `bookmarks-page`
- Displays:
  - `bookmarks-list`
  - Dynamic buttons: `remove-bookmark-button-{bookmark_id}`, `read-bookmark-button-{bookmark_id}`
  - `back-to-dashboard`

### Comments Page - comments.html
- Page Title: Article Comments
- Container: `comments-page`
- Displays:
  - `comments-list`
  - `write-comment-button`
  - `filter-by-article`
  - `back-to-dashboard`

### Write Comment Page - write_comment.html
- Page Title: Write a Comment
- Container: `write-comment-page`
- Displays:
  - `select-article`
  - `commenter-name`
  - `comment-text`
  - `submit-comment-button`

### Trending Articles Page - trending.html
- Page Title: Trending Articles
- Container: `trending-page`
- Displays:
  - `trending-list`
  - `time-period-filter`
  - Dynamic buttons: `view-article-button-{article_id}`
  - `back-to-dashboard`

### Category Page - category.html
- Page Title: Category Articles
- Container: `category-page`
- Displays:
  - `category-title` (H1)
  - `category-articles`
  - `sort-by-date` button
  - `sort-by-popularity` button
  - `back-to-dashboard`

### Search Results Page - search_results.html
- Page Title: Search Results
- Container: `search-results-page`
- Displays:
  - `search-query-display`
  - `results-list`
  - `no-results-message`
  - `back-to-dashboard`

---

## Section 3: Data File Schemas

### Articles Data
- File: `data/articles.txt`
- Fields: `article_id|title|author|category|content|date|views`
- Details:
  - `article_id`: integer, unique
  - `title`: string
  - `author`: string
  - `category`: string (matches categories.txt)
  - `content`: string
  - `date`: ISO format `YYYY-MM-DD`
  - `views`: integer (non-negative, incremented per article detail view)

### Categories Data
- File: `data/categories.txt`
- Fields: `category_id|category_name|description`
- Used for category filtering and dropdown options.

### Bookmarks Data
- File: `data/bookmarks.txt`
- Fields: `bookmark_id|article_id|article_title|bookmarked_date`
- Supports adding and removing bookmarks via API.

### Comments Data
- File: `data/comments.txt`
- Fields: `comment_id|article_id|article_title|commenter_name|comment_text|comment_date`
- Supports listing comments and adding new comments.

### Trending Data
- File: `data/trending.txt`
- Fields: `article_id|article_title|category|view_count|period`
- Read-only, used for displaying trending articles with filtering by time period.

---

## Section 4: Navigation and Interaction (Mapped to Routes & UI Elements)

- Dashboard buttons:
  - `browse-articles-button` -> `/articles`
  - `view-bookmarks-button` -> `/bookmarks`
  - `trending-articles-button` -> `/trending`

- Article cards and trending articles have buttons:
  - `view-article-button-{article_id}` -> `/article/<article_id>`

- Article Details:
  - `bookmark-button` triggers POST `/bookmark` with `article_id`

- Bookmarks page buttons:
  - `remove-bookmark-button-{bookmark_id}` triggers DELETE `/bookmark/<bookmark_id>`
  - `read-bookmark-button-{bookmark_id}` opens Article Details page for that article
  - `back-to-dashboard` -> `/`

- Comments page:
  - `write-comment-button` -> write comment page (client side navigation)
  - `filter-by-article` filters via GET `/comments?article_id=...`
  - `back-to-dashboard` -> `/`

- Write Comment page:
  - `submit-comment-button` POSTs to `/comment` with comment data

- Trending page:
  - `time-period-filter` passes optional `period` param to GET `/trending`
  - `back-to-dashboard` -> `/`

- Category page:
  - `sort-by-date` and `sort-by-popularity` buttons trigger GET `/category/<category_name>?sort_by=date` or `?sort_by=popularity`
  - `back-to-dashboard` -> `/`

- Search results page:
  - Navigated with query param `q` via GET `/search?q=...`
  - `back-to-dashboard` -> `/`

- Article Catalog page filters:
  - `search-input` and `category-filter` control query params `search` and `category` for `/articles`

---

## Section 5: Consistency and Coverage Check

- All nine pages are included with matching backend routes and frontend templates.
- The route endpoints and HTTP methods correspond directly to the expected user interactions and UI elements.
- Data file schemas fully support the displayed content and user operations.
- No features beyond the specified ones are introduced.
- All dynamic UI element IDs align with backend data IDs for consistent event handling.
- Navigation paths between pages are consistently defined with buttons and logical flows.

---

This consolidated design specification provides the complete and consistent blueprint for implementing the NewsPortal web application backend and frontend.
Developers can implement the Flask backend routes and templates and bind UI elements following this specification to achieve the full user experience.