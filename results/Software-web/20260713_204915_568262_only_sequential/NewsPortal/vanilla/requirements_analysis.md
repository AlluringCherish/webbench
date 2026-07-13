# Requirements Analysis for NewsPortal Web Application

---

## Overview
The NewsPortal web application consists of nine main pages, each with specified element IDs, functionality, navigation paths, and data storage in local text files. The application allows browsing articles by category, searching, viewing details, bookmarking, commenting, and tracking trending articles. No authentication is required.

---

## 1. Pages and Their Elements

### 1. Dashboard Page
- **Title**: News Portal
- **Route Path**: `/dashboard` (GET)
- **Element IDs**:
  - `dashboard-page` (Div): Container for dashboard content.
  - `featured-articles` (Div): Shows featured article recommendations.
  - `browse-articles-button` (Button): Navigates to Article Catalog page.
  - `view-bookmarks-button` (Button): Navigates to Bookmarks page.
  - `trending-articles-button` (Button): Navigates to Trending Articles page.

---

### 2. Article Catalog Page
- **Title**: Article Catalog
- **Route Path**: `/articles` (GET)
- **Element IDs**:
  - `catalog-page` (Div): Container for catalog content.
  - `search-input` (Input): Search field for article title, author, or keywords.
  - `category-filter` (Dropdown): Filter articles by category.
  - `articles-grid` (Div): Displays article cards.
  - `view-article-button-{article_id}` (Button): For each article card, navigates to Article Details page for that article.

---

### 3. Article Details Page
- **Title**: Article Details
- **Route Path**: `/articles/{article_id}` (GET)
- **Element IDs**:
  - `article-details-page` (Div): Container for article details.
  - `article-title` (H1): Displays article title.
  - `article-author` (Div): Displays article author.
  - `article-date` (Div): Displays article publication date.
  - `bookmark-button` (Button): Adds the article to bookmarks.
  - `article-content` (Div): Displays full article content.

---

### 4. Bookmarks Page
- **Title**: My Bookmarks
- **Route Path**: `/bookmarks` (GET)
- **Element IDs**:
  - `bookmarks-page` (Div): Container for bookmarks.
  - `bookmarks-list` (Div): List of bookmarked articles.
  - `remove-bookmark-button-{bookmark_id}` (Button): Removes bookmark.
  - `read-bookmark-button-{bookmark_id}` (Button): Opens bookmarked article details.
  - `back-to-dashboard` (Button): Navigates back to Dashboard.

---

### 5. Comments Page
- **Title**: Article Comments
- **Route Path**: `/comments` (GET)
- **Element IDs**:
  - `comments-page` (Div): Container for comments.
  - `comments-list` (Div): List all comments with article title, commenter name, comment text.
  - `write-comment-button` (Button): Navigates to Write Comment page.
  - `filter-by-article` (Dropdown): Filter comments by article.
  - `back-to-dashboard` (Button): Navigates back to Dashboard.

---

### 6. Write Comment Page
- **Title**: Write a Comment
- **Route Path**: `/comments/write` (GET for page load, POST for submission)
- **Element IDs**:
  - `write-comment-page` (Div): Container for comment form.
  - `select-article` (Dropdown): Select article to comment on.
  - `commenter-name` (Input): Enter commenter name.
  - `comment-text` (Textarea): Enter comment text.
  - `submit-comment-button` (Button): Submit the comment.

---

### 7. Trending Articles Page
- **Title**: Trending Articles
- **Route Path**: `/trending` (GET)
- **Element IDs**:
  - `trending-page` (Div): Container for trending article list.
  - `trending-list` (Div): Ranked list of trending articles.
  - `time-period-filter` (Dropdown): Filter by time period (Today, This Week, This Month).
  - `view-article-button-{article_id}` (Button): View detailed article.
  - `back-to-dashboard` (Button): Back to Dashboard.

---

### 8. Category Page
- **Title**: Category Articles
- **Route Path**: `/category/{category_id}` (GET)
- **Element IDs**:
  - `category-page` (Div): Container for category articles.
  - `category-title` (H1): Displays category name.
  - `category-articles` (Div): List articles of the category.
  - `sort-by-date` (Button): Sort articles by date.
  - `sort-by-popularity` (Button): Sort articles by popularity.
  - `back-to-dashboard` (Button): Return to Dashboard.

---

### 9. Search Results Page
- **Title**: Search Results
- **Route Path**: `/search` (GET)
- **Element IDs**:
  - `search-results-page` (Div): Container for search results.
  - `search-query-display` (Div): Shows the search query.
  - `results-list` (Div): Displays articles matching search.
  - `no-results-message` (Div): Message if no results found.
  - `back-to-dashboard` (Button): Return to Dashboard.

---

## 2. Navigation Flows and Routes

| From Page           | Element/Button ID                | Action/Navigation Path                  | HTTP Method |
|---------------------|--------------------------------|----------------------------------------|-------------|
| Dashboard           | `browse-articles-button`        | Navigate to Article Catalog             | GET         |
| Dashboard           | `view-bookmarks-button`         | Navigate to Bookmarks                   | GET         |
| Dashboard           | `trending-articles-button`      | Navigate to Trending Articles           | GET         |
| Article Catalog     | `view-article-button-{article_id}` | Navigate to Article Details `/articles/{article_id}` | GET          |
| Article Details     | `bookmark-button`               | POST bookmark, stay or redirect back   | POST        |
| Bookmarks           | `remove-bookmark-button-{bookmark_id}` | POST remove bookmark                 | POST        |
| Bookmarks           | `read-bookmark-button-{bookmark_id}` | Navigate to Article Details           | GET         |
| Bookmarks           | `back-to-dashboard`             | Navigate back to Dashboard              | GET         |
| Comments            | `write-comment-button`          | Navigate to Write Comment page          | GET         |
| Comments            | `filter-by-article`             | Filter comments display on same page    | GET or client-side|
| Comments            | `back-to-dashboard`             | Navigate back to Dashboard              | GET         |
| Write Comment       | `submit-comment-button`         | POST new comment                        | POST        |
| Trending Articles   | `view-article-button-{article_id}` | Navigate to Article Details             | GET         |
| Trending Articles   | `time-period-filter`            | Filter trending list (client or GET)    | GET or client-side|
| Trending Articles   | `back-to-dashboard`             | Navigate back to Dashboard              | GET         |
| Category            | `sort-by-date` or `sort-by-popularity` | Sort articles in category              | GET or client-side|
| Category            | `back-to-dashboard`             | Navigate back to Dashboard              | GET         |
| Search Results      | `back-to-dashboard`             | Navigate back to Dashboard              | GET         |

---

## 3. Data Files and Formats

### 3.1 Articles Data
- **File**: `data/articles.txt`
- **Format**: Pipe-delimited
```
article_id|title|author|category|content|date|views
```
- **Example**:
```
1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891
```

### 3.2 Categories Data
- **File**: `data/categories.txt`
- **Format**: Pipe-delimited
```
category_id|category_name|description
```
- **Example**:
```
1|Technology|Latest tech news and innovations
2|Sports|Sports news and event coverage
3|Business|Business and finance news
```

### 3.3 Bookmarks Data
- **File**: `data/bookmarks.txt`
- **Format**: Pipe-delimited
```
bookmark_id|article_id|article_title|bookmarked_date
```
- **Example**:
```
1|1|Breaking: New Technology Breakthrough|2025-01-20
2|3|Business: Market Trends Analysis|2025-01-18
```

### 3.4 Comments Data
- **File**: `data/comments.txt`
- **Format**: Pipe-delimited
```
comment_id|article_id|article_title|commenter_name|comment_text|comment_date
```
- **Example**:
```
1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19
```

### 3.5 Trending Data
- **File**: `data/trending.txt`
- **Format**: Pipe-delimited
```
article_id|article_title|category|view_count|period
```
- **Example**:
```
1|Breaking: New Technology Breakthrough|Technology|5432|This Week
2|Sports: Championship Victory|Sports|3210|This Week
3|Business: Market Trends Analysis|Business|2891|This Month
```

---

## 4. Functional Highlights

### Bookmarking
- Users can bookmark an article from the Article Details page using `bookmark-button`.
- Bookmarks are saved in `bookmarks.txt` with bookmark_id, article_id, article_title, and date.
- Bookmarks are viewed and managed on the Bookmarks page.
- Users can remove bookmarks using `remove-bookmark-button-{bookmark_id}`.
- Users can read bookmarked articles via `read-bookmark-button-{bookmark_id}`.

### Comments
- Comments are listed on the Comments page.
- Users can filter comments by article using `filter-by-article`.
- Users navigate to Write Comment page via `write-comment-button`.
- New comments submitted on Write Comment page are saved to `comments.txt`.
- Comment entries include comment_id, article_id, article_title, commenter_name, comment_text, and comment_date.

### Trending Articles
- Trending articles are displayed on the Trending Articles page.
- Trending data is sourced from `trending.txt` and ranked by views.
- Users can filter trending articles by time period using `time-period-filter`.
- Articles link to details via `view-article-button-{article_id}`.

---

This document provides a comprehensive trace of pages, elements, routes, data formats, and navigation flows necessary for designing and implementing the NewsPortal web application. All identifiers and data fields align exactly with the initial requirements.
