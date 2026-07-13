# NewsPortal Flask Application Design Specification

## 1. Overview
This document specifies the complete design of the NewsPortal Flask web app, covering all 9 pages with detailed element IDs, navigation flow starting from Dashboard, and local text file data storage formats.

---

## 2. Flask Page Templates and UI Elements

### 2.1 Dashboard Page
- **Route:** `/dashboard` (Starting page)
- **Page Title:** `News Portal`
- **Container Div:** `id="dashboard-page"`
- **UI Elements:**
  - `div` with `id="featured-articles"` - displays recommended featured articles
  - `button` with `id="browse-articles-button"` - navigates to Article Catalog page
  - `button` with `id="view-bookmarks-button"` - navigates to Bookmarks page
  - `button` with `id="trending-articles-button"` - navigates to Trending Articles page

### 2.2 Article Catalog Page
- **Route:** `/catalog`
- **Page Title:** `Article Catalog`
- **Container Div:** `id="catalog-page"`
- **UI Elements:**
  - `input` (text) with `id="search-input"` - to search articles by title, author, or keywords
  - `select` dropdown with `id="category-filter"` - categories filter (Technology, Sports, Business, Health, Entertainment, etc.)
  - `div` with `id="articles-grid"` - grid layout for article cards
  - For each article card:
     - `button` with `id="view-article-button-{article_id}"` - to view article details

### 2.3 Article Details Page
- **Route:** `/article/<article_id>`
- **Page Title:** `Article Details`
- **Container Div:** `id="article-details-page"`
- **UI Elements:**
  - `h1` with `id="article-title"` - article title
  - `div` with `id="article-author"` - article author
  - `div` with `id="article-date"` - publication date
  - `button` with `id="bookmark-button"` - to bookmark this article
  - `div` with `id="article-content"` - full article content

### 2.4 Bookmarks Page
- **Route:** `/bookmarks`
- **Page Title:** `My Bookmarks`
- **Container Div:** `id="bookmarks-page"`
- **UI Elements:**
  - `div` with `id="bookmarks-list"` - list showing bookmarked articles with title and date
  - For each bookmark:
    - `button` with `id="remove-bookmark-button-{bookmark_id}"` - remove bookmark
    - `button` with `id="read-bookmark-button-{bookmark_id}"` - read bookmarked article
  - `button` with `id="back-to-dashboard"` - navigate back to Dashboard

### 2.5 Comments Page
- **Route:** `/comments`
- **Page Title:** `Article Comments`
- **Container Div:** `id="comments-page"`
- **UI Elements:**
  - `div` with `id="comments-list"` - list of all comments with article title, commenter name, and comment text
  - `button` with `id="write-comment-button"` - navigate to Write Comment page
  - `select` dropdown with `id="filter-by-article"` - filter comments by article
  - `button` with `id="back-to-dashboard"` - navigate back to Dashboard

### 2.6 Write Comment Page
- **Route:** `/write-comment`
- **Page Title:** `Write a Comment`
- **Container Div:** `id="write-comment-page"`
- **UI Elements:**
  - `select` dropdown with `id="select-article"` - select article to comment on
  - `input` (text) with `id="commenter-name"` - enter commenter name
  - `textarea` with `id="comment-text"` - enter comment
  - `button` with `id="submit-comment-button"` - submit comment

### 2.7 Trending Articles Page
- **Route:** `/trending`
- **Page Title:** `Trending Articles`
- **Container Div:** `id="trending-page"`
- **UI Elements:**
  - `div` with `id="trending-list"` - ranked trending articles showing rank, title, category, view count
  - `select` dropdown with `id="time-period-filter"` - filter by time period (Today, This Week, This Month)
  - For each trending article:
    - `button` with `id="view-article-button-{article_id}"` - view article details
  - `button` with `id="back-to-dashboard"` - navigate back to Dashboard

### 2.8 Category Page
- **Route:** `/category/<category_name>`
- **Page Title:** `Category Articles`
- **Container Div:** `id="category-page"`
- **UI Elements:**
  - `h1` with `id="category-title"` - name of the category
  - `div` with `id="category-articles"` - list of articles in that category
  - `button` with `id="sort-by-date"` - sort articles by date
  - `button` with `id="sort-by-popularity"` - sort articles by popularity
  - `button` with `id="back-to-dashboard"` - navigate back to Dashboard

### 2.9 Search Results Page
- **Route:** `/search-results`
- **Page Title:** `Search Results`
- **Container Div:** `id="search-results-page"`
- **UI Elements:**
  - `div` with `id="search-query-display"` - display the executed search query
  - `div` with `id="results-list"` - list of articles matching the search
  - `div` with `id="no-results-message"` - message when no results found
  - `button` with `id="back-to-dashboard"` - navigate back to Dashboard

---

## 3. Navigation Flow

- Application default start page: `/dashboard` (Dashboard Page)

- From Dashboard:
  - `browse-articles-button` → `/catalog`
  - `view-bookmarks-button` → `/bookmarks`
  - `trending-articles-button` → `/trending`

- From Article Catalog:
  - `view-article-button-{article_id}` → `/article/{article_id}`
  - Filter by category uses `/category/{category_name}` page
  - Search submits query and navigates to `/search-results`
  - No explicit back button (assumed via browser or nav bar)

- From Article Details:
  - `bookmark-button` adds bookmark
  - Navigation back via browser or site nav (no explicit back button required)

- From Bookmarks:
  - `remove-bookmark-button-{bookmark_id}` removes the bookmark
  - `read-bookmark-button-{bookmark_id}` navigates to `/article/{article_id}`
  - `back-to-dashboard` → `/dashboard`

- From Comments:
  - `write-comment-button` → `/write-comment`
  - `filter-by-article` updates displayed comments
  - `back-to-dashboard` → `/dashboard`

- From Write Comment:
  - `submit-comment-button` submits new comment and redirects to `/comments`

- From Trending:
  - `view-article-button-{article_id}` → `/article/{article_id}`
  - `time-period-filter` changes trending articles display
  - `back-to-dashboard` → `/dashboard`

- From Category:
  - `sort-by-date` sorts articles ascending/descending by date
  - `sort-by-popularity` sorts by views
  - `back-to-dashboard` → `/dashboard`

- From Search Results:
  - `back-to-dashboard` → `/dashboard`

---

## 4. Local Text File Data Storage Formats and Usage

All data is stored in the `data/` directory in UTF-8 encoded text files.

### 4.1 Articles Data (`articles.txt`)
- **File Path:** `data/articles.txt`
- **Format:** 
  ```
  article_id|title|author|category|content|date|views
  ```
- **Example:**
  ```
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891
  ```
- **Usage:** Load at app start or on-demand to display articles; update views on article reads.

### 4.2 Categories Data (`categories.txt`)
- **File Path:** `data/categories.txt`
- **Format:** 
  ```
  category_id|category_name|description
  ```
- **Example:**
  ```
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news
  ```
- **Usage:** Populate category filters and category page displays.

### 4.3 Bookmarks Data (`bookmarks.txt`)
- **File Path:** `data/bookmarks.txt`
- **Format:**
  ```
  bookmark_id|article_id|article_title|bookmarked_date
  ```
- **Example:**
  ```
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18
  ```
- **Usage:** Read to show user bookmarks; add/remove bookmarks updates this file.

### 4.4 Comments Data (`comments.txt`)
- **File Path:** `data/comments.txt`
- **Format:**
  ```
  comment_id|article_id|article_title|commenter_name|comment_text|comment_date
  ```
- **Example:**
  ```
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19
  ```
- **Usage:** Read to display comments; append on new comment submission.

### 4.5 Trending Data (`trending.txt`)
- **File Path:** `data/trending.txt`
- **Format:**
  ```
  article_id|article_title|category|view_count|period
  ```
- **Example:**
  ```
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month
  ```
- **Usage:** Used for Trending page display filtered by time period.

---

## 5. Summary
This design specification fully encompasses the required UI elements with exact IDs for all pages, the navigation flow starting from the Dashboard page, and the precise format and usage of all text file-based data stores as specified in the requirements.

This spec can be used as the definitive guide for development and testing of the NewsPortal Flask web app.

---