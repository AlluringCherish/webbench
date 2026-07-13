# NewsPortal Web Application Design Specification (design_candidate_b.md)

---

## Overview
This design specification outlines the NewsPortal web application architecture focusing on Flask routes, UI element IDs, page titles, navigation, and local data file integration. This independent document supports full implementation without referencing other designs.

---

## 1. Flask Routes and Corresponding Templates

| Page Name                | Route Path                   | HTTP Method | Template Filename           | Page Title          |
|--------------------------|------------------------------|-------------|-----------------------------|---------------------|
| Dashboard                | `/`                          | GET         | dashboard.html              | News Portal         |
| Article Catalog          | `/catalog`                   | GET         | catalog.html                | Article Catalog     |
| Article Details          | `/article/<int:article_id>`  | GET         | article_details.html        | Article Details     |
| Bookmarks                | `/bookmarks`                 | GET         | bookmarks.html              | My Bookmarks        |
| Comments                 | `/comments`                  | GET         | comments.html               | Article Comments    |
| Write Comment            | `/write-comment`             | GET, POST   | write_comment.html          | Write a Comment     |
| Trending Articles        | `/trending`                  | GET         | trending.html               | Trending Articles   |
| Category Articles        | `/category/<string:category_name>` | GET  | category.html               | Category Articles   |
| Search Results           | `/search`                   | GET         | search_results.html         | Search Results      |

---

## 2. UI Element IDs per Page

### Dashboard Page
- **Container:** `dashboard-page` (Div)
- Featured Articles Section: `featured-articles` (Div)
- Navigation Buttons:
  - `browse-articles-button` (Button) &rarr; navigates to `/catalog`
  - `view-bookmarks-button` (Button) &rarr; navigates to `/bookmarks`
  - `trending-articles-button` (Button) &rarr; navigates to `/trending`

### Article Catalog Page
- **Container:** `catalog-page` (Div)
- Search Input: `search-input` (Input)
- Category Filter: `category-filter` (Dropdown)
- Articles Grid: `articles-grid` (Div)
- Article-Specific View Buttons: `view-article-button-{article_id}` (Button) for each article

### Article Details Page
- **Container:** `article-details-page` (Div)
- Article Title: `article-title` (H1)
- Article Author: `article-author` (Div)
- Article Date: `article-date` (Div)
- Bookmark Button: `bookmark-button` (Button)
- Article Content Section: `article-content` (Div)

### Bookmarks Page
- **Container:** `bookmarks-page` (Div)
- Bookmarked Articles List: `bookmarks-list` (Div)
- Remove Bookmark Button per item: `remove-bookmark-button-{bookmark_id}` (Button)
- Read Bookmark Button per item: `read-bookmark-button-{bookmark_id}` (Button)
- Back to Dashboard Button: `back-to-dashboard` (Button) &rarr; navigates to `/`

### Comments Page
- **Container:** `comments-page` (Div)
- Comments List: `comments-list` (Div)
- Write Comment Button: `write-comment-button` (Button) &rarr; navigates to `/write-comment`
- Filter Comments By Article Dropdown: `filter-by-article` (Dropdown)
- Back to Dashboard Button: `back-to-dashboard` (Button) &rarr; navigates to `/`

### Write Comment Page
- **Container:** `write-comment-page` (Div)
- Article Selector Dropdown: `select-article` (Dropdown)
- Commenter Name Input: `commenter-name` (Input)
- Comment Textarea: `comment-text` (Textarea)
- Submit Comment Button: `submit-comment-button` (Button)

### Trending Articles Page
- **Container:** `trending-page` (Div)
- Trending Articles List: `trending-list` (Div)
- Time Period Filter Dropdown: `time-period-filter` (Dropdown)
- Article-Specific View Buttons: `view-article-button-{article_id}` (Button) per trending article
- Back to Dashboard Button: `back-to-dashboard` (Button) &rarr; navigates to `/`

### Category Articles Page
- **Container:** `category-page` (Div)
- Category Title: `category-title` (H1)
- Category Articles List: `category-articles` (Div)
- Sort Buttons:
  - `sort-by-date` (Button)
  - `sort-by-popularity` (Button)
- Back to Dashboard Button: `back-to-dashboard` (Button) &rarr; navigates to `/`

### Search Results Page
- **Container:** `search-results-page` (Div)
- Search Query Display: `search-query-display` (Div)
- Results List: `results-list` (Div)
- No Results Message: `no-results-message` (Div)
- Back to Dashboard Button: `back-to-dashboard` (Button) &rarr; navigates to `/`

---

## 3. Navigation Button Routes and Function Names

| Button ID                      | Target Route                            | Flask Function Name        |
|-------------------------------|---------------------------------------|---------------------------|
| browse-articles-button          | `/catalog`                            | catalog_page              |
| view-bookmarks-button           | `/bookmarks`                         | bookmarks_page            |
| trending-articles-button        | `/trending`                         | trending_page             |
| view-article-button-{article_id}| `/article/<article_id>`              | article_details           |
| back-to-dashboard               | `/`                                 | dashboard_page            |
| remove-bookmark-button-{bookmark_id} | POST (via form or AJAX) to `/bookmarks/remove/<bookmark_id>` | remove_bookmark           |
| read-bookmark-button-{bookmark_id} | `/article/<article_id>` (lookup article_id by bookmark) | article_details           |
| write-comment-button            | `/write-comment`                    | write_comment_page_get    |
| submit-comment-button           | POST `/write-comment`                | write_comment_page_post   |
| filter-by-article               | Reload `/comments` with filter param| comments_page             |
| select-article                 | Part of comment form on `/write-comment` | n/a                    |
| time-period-filter              | Reload `/trending` with time param  | trending_page             |
| sort-by-date                   | Reload `/category/<category_name>` with sort param | category_page             |
| sort-by-popularity             | Reload `/category/<category_name>` with sort param | category_page             |

---

## 4. Data Files Description and Usage

All data files are plain text files located under the `data/` directory.

### 4.1 Articles Data
- **File:** `data/articles.txt`
- **Format per line:**
  ```
  article_id|title|author|category|content|date|views
  ```
- **Usage:**
  - Read for displaying article catalog, details, search results, category articles, trending.
  - Fields used:
    - `article_id`: unique identifier for article
    - `title`, `author`, `category` for display and filtering
    - `content` for detailed article page
    - `date` for sorting and display
    - `views` for trending and popularity

### 4.2 Categories Data
- **File:** `data/categories.txt`
- **Format per line:**
  ```
  category_id|category_name|description
  ```
- **Usage:**
  - Populate category filter dropdowns (`category-filter`, `select-article`, `filter-by-article`, etc.)
  - Display category descriptions

### 4.3 Bookmarks Data
- **File:** `data/bookmarks.txt`
- **Format per line:**
  ```
  bookmark_id|article_id|article_title|bookmarked_date
  ```
- **Usage:**
  - Load bookmarks page list
  - Removal/modification operations
  - Linking to article details for reading bookmarked articles

### 4.4 Comments Data
- **File:** `data/comments.txt`
- **Format per line:**
  ```
  comment_id|article_id|article_title|commenter_name|comment_text|comment_date
  ```
- **Usage:**
  - Display all comments on comments page
  - Filter comments by article
  - Store new comments submitted from write comment page

### 4.5 Trending Data
- **File:** `data/trending.txt`
- **Format per line:**
  ```
  article_id|article_title|category|view_count|period
  ```
- **Usage:**
  - Display trending articles filtered by time period (Today, This Week, This Month)
  - Data source for trending articles page

---

## 5. Additional Implementation Notes

- UI elements must use IDs exactly as specified for consistent DOM manipulation and testing.
- All navigation buttons trigger either page reloads via GET or POST requests as appropriate.
- Data files are read at request time to serve fresh content; consider caching strategies for performance.
- Article, bookmark, comment, and trending IDs must be consistently used to link data records and UI elements.
- Sorting and filtering actions reload the respective pages with query parameters reflecting user selections.

---

This design intends to provide a clear, implementable blueprint for the NewsPortal application in alignment with given requirements.
