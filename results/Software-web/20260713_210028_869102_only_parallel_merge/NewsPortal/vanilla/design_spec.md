# NewsPortal Web Application Design Specification

---

## Overview

This document consolidates and unifies the design specifications from two independent analysts for the NewsPortal web application. It provides a comprehensive, consistent, and implementation-ready blueprint covering all nine required pages with exact Flask routes, UI element IDs, navigation details, and local text file data formats and usages.

---

## 1. Flask Routes, Page Titles & Templates

| Route URL                   | Function Name          | HTTP Method | Template Filename          | Page Title           |
|-----------------------------|-----------------------|-------------|----------------------------|----------------------|
| /                           | dashboard_page        | GET         | dashboard.html             | News Portal          |
| /catalog                    | article_catalog       | GET         | catalog.html               | Article Catalog      |
| /article/<int:article_id>   | article_details       | GET         | article_details.html       | Article Details      |
| /bookmarks                  | bookmarks_page        | GET         | bookmarks.html             | My Bookmarks         |
| /bookmarks/remove/<int:bookmark_id> | remove_bookmark         | POST        | n/a                        | n/a                  |
| /comments                   | comments_page         | GET         | comments.html              | Article Comments     |
| /write-comment              | write_comment_page_get| GET         | write_comment.html         | Write a Comment      |
| /write-comment              | write_comment_page_post| POST       | n/a                        | n/a                  |
| /trending                  | trending_page         | GET         | trending.html              | Trending Articles    |
| /category/<string:category_name> | category_page          | GET         | category.html              | Category Articles    |
| /search                    | search_results        | GET         | search_results.html        | Search Results       |

Notes:
- The route for removing bookmarks is explicitly defined as a POST route.
- For the write comment page, GET and POST handlers are distinct functions.
- `<int:article_id>` and `<string:category_name>` are type-constrained URL parameters for clarity and robustness.

---

## 2. Page UI Elements and Navigation Buttons

### 1. Dashboard Page
- Container ID: `dashboard-page` (div)
- Elements:
  - `featured-articles` (div) - shows featured article recommendations
  - Buttons:
    - `browse-articles-button` (button) - navigates to `/catalog` via `article_catalog`
    - `view-bookmarks-button` (button) - navigates to `/bookmarks` via `bookmarks_page`
    - `trending-articles-button` (button) - navigates to `/trending` via `trending_page`

### 2. Article Catalog Page
- Container ID: `catalog-page` (div)
- Elements:
  - `search-input` (input) - search field for title, author, or keywords
  - `category-filter` (dropdown select) - filter articles by category (Technology, Sports, Business, Health, Entertainment, etc.)
  - `articles-grid` (div) - displays article cards with thumbnail, title, author, date
  - For each article card, a button `view-article-button-{article_id}` (button) navigates to `/article/<article_id>` via `article_details`

### 3. Article Details Page
- Container ID: `article-details-page` (div)
- Elements:
  - `article-title` (h1) - displays article title
  - `article-author` (div) - displays article author
  - `article-date` (div) - displays article publication date
  - `bookmark-button` (button) - bookmarks the current article
  - `article-content` (div) - full article content

### 4. Bookmarks Page
- Container ID: `bookmarks-page` (div)
- Elements:
  - `bookmarks-list` (div) - list of bookmarked articles showing title and date
  - For each bookmark:
    - `remove-bookmark-button-{bookmark_id}` (button) - removes bookmark
    - `read-bookmark-button-{bookmark_id}` (button) - navigates to article details `/article/<article_id>` (article_id resolved from bookmark)
  - Button `back-to-dashboard` (button) - navigates back to dashboard `/` via `dashboard_page`

### 5. Comments Page
- Container ID: `comments-page` (div)
- Elements:
  - `comments-list` (div) - list all comments with article title, commenter name, comment text
  - `write-comment-button` (button) - navigates to write comment page `/write-comment` via `write_comment_page_get`
  - `filter-by-article` (dropdown select) - filter comments by article
  - Button `back-to-dashboard` (button) - navigates back to dashboard `/` via `dashboard_page`

### 6. Write Comment Page
- Container ID: `write-comment-page` (div)
- Elements:
  - `select-article` (dropdown select) - select article to comment on
  - `commenter-name` (input) - input commenter name
  - `comment-text` (textarea) - write comment text
  - `submit-comment-button` (button) - submits the comment (POST to `write_comment_page_post`)

### 7. Trending Articles Page
- Container ID: `trending-page` (div)
- Elements:
  - `trending-list` (div) - ranked list of trending articles with rank, title, category, view count
  - `time-period-filter` (dropdown select) - filters by time period (Today, This Week, This Month)
  - For each trending article:
    - `view-article-button-{article_id}` (button) - navigates to article details `/article/<article_id>` via `article_details`
  - Button `back-to-dashboard` (button) - navigates back to dashboard `/` via `dashboard_page`

### 8. Category Page
- Container ID: `category-page` (div)
- Elements:
  - `category-title` (h1) - displays selected category name
  - `category-articles` (div) - list of articles in category
  - Buttons:
    - `sort-by-date` (button) - sorts articles by date
    - `sort-by-popularity` (button) - sorts articles by popularity
    - `back-to-dashboard` (button) - navigates back to dashboard `/` via `dashboard_page`

### 9. Search Results Page
- Container ID: `search-results-page` (div)
- Elements:
  - `search-query-display` (div) - shows the search query
  - `results-list` (div) - list of search results with article title and excerpt
  - `no-results-message` (div) - displays when no results found
  - Button `back-to-dashboard` (button) - navigates back to dashboard `/` via `dashboard_page`

---

## 3. Navigation and Route Function Names for Buttons

| Button ID                      | Target Route                            | Flask Function Name        |
|-------------------------------|---------------------------------------|---------------------------|
| browse-articles-button          | `/catalog`                            | article_catalog            |
| view-bookmarks-button           | `/bookmarks`                         | bookmarks_page             |
| trending-articles-button        | `/trending`                         | trending_page              |
| view-article-button-{article_id}| `/article/<article_id>`              | article_details            |
| back-to-dashboard               | `/`                                 | dashboard_page             |
| remove-bookmark-button-{bookmark_id} | POST `/bookmarks/remove/<bookmark_id>` | remove_bookmark           |
| read-bookmark-button-{bookmark_id} | `/article/<article_id>` (lookup article_id by bookmark) | article_details           |
| write-comment-button            | `/write-comment`                    | write_comment_page_get     |
| submit-comment-button           | POST `/write-comment`                | write_comment_page_post    |
| filter-by-article               | Reload `/comments` with filter param| comments_page              |
| select-article                 | Part of comment form on `/write-comment` | n/a                     |
| time-period-filter              | Reload `/trending` with time param  | trending_page              |
| sort-by-date                   | Reload `/category/<category_name>` with sort param | category_page           |
| sort-by-popularity             | Reload `/category/<category_name>` with sort param | category_page           |

---

## 4. Data File Usage and Formats

All data files reside under the `data/` directory. Files are pipe (`|`) delimited text files without header rows.

### 4.1 Articles Data (data/articles.txt)
- Fields order & types:
  - `article_id` (str/int)
  - `title` (str)
  - `author` (str)
  - `category` (str)
  - `content` (str)
  - `date` (str, formatted YYYY-MM-DD)
  - `views` (int)
- Usage:
  - Dashboard, Article Catalog, Article Details, Bookmarks, Comments, Trending, Category, Search Results.

### 4.2 Categories Data (data/categories.txt)
- Fields order & types:
  - `category_id` (str/int)
  - `category_name` (str)
  - `description` (str)
- Usage:
  - Populate dropdowns such as `category-filter`, `filter-by-article`, `select-article`.
  - Display category names and descriptions on relevant pages.

### 4.3 Bookmarks Data (data/bookmarks.txt)
- Fields order & types:
  - `bookmark_id` (str/int)
  - `article_id` (str/int)
  - `article_title` (str)
  - `bookmarked_date` (str)
- Usage:
  - Bookmarks Page listing and management.
  - Linking bookmark to articles for reading.

### 4.4 Comments Data (data/comments.txt)
- Fields order & types:
  - `comment_id` (str/int)
  - `article_id` (str/int)
  - `article_title` (str)
  - `commenter_name` (str)
  - `comment_text` (str)
  - `comment_date` (str)
- Usage:
  - Comments listing and filtering.
  - Append new comments from Write Comment page.

### 4.5 Trending Data (data/trending.txt)
- Fields order & types:
  - `article_id` (str/int)
  - `article_title` (str)
  - `category` (str)
  - `view_count` (int)
  - `period` (str, values: Today, This Week, This Month)
- Usage:
  - Trending Articles page filtered by selected time period.

---

## 5. Additional Implementation Notes

- UI element IDs must be used exactly as specified for consistent DOM manipulation, CSS styling, and automated testing.
- Flask function names are uniquely assigned, ensuring no conflicts with routes.
- Navigation buttons use GET requests for page loads and POST for data changes (e.g., bookmark removal, comment submission).
- Data files are read at request time for real-time content updates; caching is recommended for performance optimization.
- Sorting and filtering controls reload pages with appropriate query parameters set.
- The application starts at the Dashboard page (`/`) with route `dashboard_page`.

---

This unified design specification is comprehensive and ready for direct implementation of the NewsPortal application.
