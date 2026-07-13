# NewsPortal Web Application Design Specification

---

## Overview

This document details the complete design specification for the NewsPortal web application using Flask and local text file data storage. It covers all nine pages, their Flask routes, HTTP methods, UI element IDs, navigation buttons, and data file usage.

---

## Flask Routes, Page Titles & Templates

| Route URL               | Function Name          | HTTP Method | Template Filename          | Page Title           |
|-------------------------|-----------------------|-------------|----------------------------|----------------------|
| /                       | dashboard             | GET         | dashboard.html             | News Portal          |
| /catalog                | article_catalog       | GET         | article_catalog.html       | Article Catalog      |
| /article/<article_id>   | article_details       | GET         | article_details.html       | Article Details      |
| /bookmarks              | bookmarks             | GET         | bookmarks.html             | My Bookmarks         |
| /comments               | comments              | GET         | comments.html              | Article Comments     |
| /comments/write         | write_comment         | GET, POST   | write_comment.html         | Write a Comment      |
| /trending               | trending_articles     | GET         | trending_articles.html     | Trending Articles    |
| /category/<category_id> | category_articles     | GET         | category_articles.html     | Category Articles    |
| /search-results         | search_results        | GET         | search_results.html        | Search Results       |

---

## Page UI Elements and Navigation Buttons

### 1. Dashboard Page
- Container ID: `dashboard-page` (div)
- Elements:
  - `featured-articles` (div) - shows featured article recommendations
  - Buttons:
    - `browse-articles-button` (button) - navigates to article catalog page `/catalog` via `article_catalog`
    - `view-bookmarks-button` (button) - navigates to bookmarks page `/bookmarks` via `bookmarks`
    - `trending-articles-button` (button) - navigates to trending articles page `/trending` via `trending_articles`

### 2. Article Catalog Page
- Container ID: `catalog-page` (div)
- Elements:
  - `search-input` (input) - search field for title, author, or keywords
  - `category-filter` (dropdown select) - filter articles by category (e.g., Technology, Sports, Business, Health, Entertainment)
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
    - `read-bookmark-button-{bookmark_id}` (button) - navigates to article details `/article/<article_id>`
  - Button `back-to-dashboard` (button) - navigates back to dashboard `/` via `dashboard`

### 5. Comments Page
- Container ID: `comments-page` (div)
- Elements:
  - `comments-list` (div) - list all comments with article title, commenter name, comment text
  - `write-comment-button` (button) - navigates to write comment page `/comments/write`
  - `filter-by-article` (dropdown select) - filter comments by article
  - Button `back-to-dashboard` (button) - navigates back to dashboard `/`

### 6. Write Comment Page
- Container ID: `write-comment-page` (div)
- Elements:
  - `select-article` (dropdown select) - select article to comment on
  - `commenter-name` (input) - input commenter name
  - `comment-text` (textarea) - write comment text
  - `submit-comment-button` (button) - submits the comment (POST handler)

### 7. Trending Articles Page
- Container ID: `trending-page` (div)
- Elements:
  - `trending-list` (div) - ranked list of trending articles with rank, title, category, view count
  - `time-period-filter` (dropdown select) - filters by time period (Today, This Week, This Month)
  - For each trending article:
    - `view-article-button-{article_id}` (button) - navigates to article details `/article/<article_id>`
  - Button `back-to-dashboard` (button) - navigates back to dashboard `/`

### 8. Category Page
- Container ID: `category-page` (div)
- Elements:
  - `category-title` (h1) - displays selected category name
  - `category-articles` (div) - list of articles in category
  - Buttons:
    - `sort-by-date` (button) - sorts articles by date
    - `sort-by-popularity` (button) - sorts articles by popularity
    - `back-to-dashboard` (button) - navigates back to dashboard `/`

### 9. Search Results Page
- Container ID: `search-results-page` (div)
- Elements:
  - `search-query-display` (div) - shows the search query
  - `results-list` (div) - list of search results with article title and excerpt
  - `no-results-message` (div) - displays when no results found
  - Button `back-to-dashboard` (button) - navigates back to dashboard `/`

---

## Data File Usage

All data files are stored in the directory `data/` and are pipe (`|`) delimited with no header row.

### 1. articles.txt
- Fields:
  - `article_id` (str/int)
  - `title` (str)
  - `author` (str)
  - `category` (str)
  - `content` (str)
  - `date` (str, e.g., YYYY-MM-DD)
  - `views` (int)
- Usage:
  - Dashboard: featured articles display
  - Article Catalog: display all articles, searching and filtering
  - Article Details: load full details
  - Bookmarks: display bookmarked articles titles and dates
  - Comments: filter by article
  - Trending Articles & Category & Search Results: show articles accordingly

### 2. categories.txt
- Fields:
  - `category_id` (str/int)
  - `category_name` (str)
  - `description` (str)
- Usage:
  - Article Catalog: populate `category-filter`
  - Comments Page: populate `filter-by-article`
  - Write Comment Page: populate `select-article` with article titles or possibly their category
  - Category Page: display category name and articles with this category

### 3. bookmarks.txt
- Fields:
  - `bookmark_id` (str/int)
  - `article_id` (str/int)
  - `article_title` (str)
  - `bookmarked_date` (str)
- Usage:
  - Bookmarks Page: list bookmarked articles
  - Remove bookmarks via button
  - Read bookmark navigates to article details

### 4. comments.txt
- Fields:
  - `comment_id` (str/int)
  - `article_id` (str/int)
  - `article_title` (str)
  - `commenter_name` (str)
  - `comment_text` (str)
  - `comment_date` (str)
- Usage:
  - Comments page: list all comments
  - Filter by article
  - Write comment: append new comment entry

### 5. trending.txt
- Fields:
  - `article_id` (str/int)
  - `article_title` (str)
  - `category` (str)
  - `view_count` (int)
  - `period` (str: Today, This Week, This Month)
- Usage:
  - Trending Articles page: display ranked trending articles filtered by time period

---

This completes the NewsPortal design candidate specification A, ready for development.
