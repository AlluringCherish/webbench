# NewsPortal Flask App Design Specification

## Section 1: Flask Page Templates

### 1. Dashboard Page
- **Page Title**: News Portal
- **Elements:**
  - `dashboard-page` (Div) - Container for the dashboard page.
  - `featured-articles` (Div) - Display area for featured articles.
  - `browse-articles-button` (Button) - Navigate to Article Catalog page.
  - `view-bookmarks-button` (Button) - Navigate to Bookmarks page.
  - `trending-articles-button` (Button) - Navigate to Trending Articles page.

### 2. Article Catalog Page
- **Page Title**: Article Catalog
- **Elements:**
  - `catalog-page` (Div) - Container for article catalog.
  - `search-input` (Input[text]) - Search field for articles.
  - `category-filter` (Dropdown) - Category filter selection.
  - `articles-grid` (Div) - Grid displaying article cards.
  - `view-article-button-{article_id}` (Button) - Button to view specific article details.

### 3. Article Details Page
- **Page Title**: Article Details
- **Elements:**
  - `article-details-page` (Div) - Container.
  - `article-title` (H1) - Article title display.
  - `article-author` (Div) - Author name display.
  - `article-date` (Div) - Publication date display.
  - `bookmark-button` (Button) - Bookmark the article.
  - `article-content` (Div) - Full article text.

### 4. Bookmarks Page
- **Page Title**: My Bookmarks
- **Elements:**
  - `bookmarks-page` (Div) - Container.
  - `bookmarks-list` (Div) - List of bookmarked articles.
  - `remove-bookmark-button-{bookmark_id}` (Button) - Remove bookmark.
  - `read-bookmark-button-{bookmark_id}` (Button) - Read bookmarked article.
  - `back-to-dashboard` (Button) - Navigate to Dashboard.

### 5. Comments Page
- **Page Title**: Article Comments
- **Elements:**
  - `comments-page` (Div) - Container.
  - `comments-list` (Div) - List all comments.
  - `write-comment-button` (Button) - Navigate to Write Comment page.
  - `filter-by-article` (Dropdown) - Filter comments by article.
  - `back-to-dashboard` (Button) - Navigate to Dashboard.

### 6. Write Comment Page
- **Page Title**: Write a Comment
- **Elements:**
  - `write-comment-page` (Div) - Container.
  - `select-article` (Dropdown) - Select article to comment on.
  - `commenter-name` (Input[text]) - Commenter's name input.
  - `comment-text` (Textarea) - Comment content.
  - `submit-comment-button` (Button) - Submit comment.

### 7. Trending Articles Page
- **Page Title**: Trending Articles
- **Elements:**
  - `trending-page` (Div) - Container.
  - `trending-list` (Div) - Ranked list of trending articles.
  - `time-period-filter` (Dropdown) - Filter by time period.
  - `view-article-button-{article_id}` (Button) - View article details.
  - `back-to-dashboard` (Button) - Navigate to Dashboard.

### 8. Category Page
- **Page Title**: Category Articles
- **Elements:**
  - `category-page` (Div) - Container.
  - `category-title` (H1) - Category name display.
  - `category-articles` (Div) - List of articles in category.
  - `sort-by-date` (Button) - Sort articles by date.
  - `sort-by-popularity` (Button) - Sort by popularity.
  - `back-to-dashboard` (Button) - Navigate to Dashboard.

### 9. Search Results Page
- **Page Title**: Search Results
- **Elements:**
  - `search-results-page` (Div) - Container.
  - `search-query-display` (Div) - Displays user's search query.
  - `results-list` (Div) - List of search result articles.
  - `no-results-message` (Div) - Shown if no results found.
  - `back-to-dashboard` (Button) - Navigate to Dashboard.

---

## Section 2: Navigation Flow

- **Starting Point:** Dashboard page (`/dashboard` route).
- **Routes:**
  - `/dashboard` → Dashboard page.
  - `/catalog` → Article Catalog page.
  - `/article/<article_id>` → Article Details page.
  - `/bookmarks` → Bookmarks page.
  - `/comments` → Comments page.
  - `/write-comment` → Write Comment page.
  - `/trending` → Trending Articles page.
  - `/category/<category_name>` → Category page.
  - `/search-results` → Search Results page.

- **Navigation Logic:**
  - From **Dashboard:** Buttons to `/catalog`, `/bookmarks`, `/trending`.
  - From **Article Catalog:** Each article card's `view-article-button-{article_id}` leads to `/article/<article_id>`.
  - From **Article Details:** `bookmark-button` adds bookmark; navigation back to dashboard or catalog as needed.
  - From **Bookmarks:** Buttons to read or remove bookmarks, back to dashboard via `back-to-dashboard`.
  - From **Comments:** `write-comment-button` to `/write-comment`; filter comments by article; back to dashboard.
  - From **Write Comment:** Form submission adds comment, then navigates to `/comments` or dashboard.
  - From **Trending Articles:** Article view buttons lead to details; `back-to-dashboard` goes to dashboard.
  - From **Category:** Sort buttons adjust listing; `back-to-dashboard` returns to dashboard.
  - From **Search Results:** Results shown with option to return to dashboard.

- All navigation uses GET requests except form submissions (POST).
- No authentication is required; all pages are publicly accessible directly.

---

## Section 3: Local Text File Data Management

### File Names & Formats

1. `articles.txt`
   - Format: `article_id|title|author|category|content|date|views`
   - Example:
     ```
     1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
     2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
     3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891
     ```

2. `categories.txt`
   - Format: `category_id|category_name|description`
   - Example:
     ```
     1|Technology|Latest tech news and innovations
     2|Sports|Sports news and event coverage
     3|Business|Business and finance news
     ```

3. `bookmarks.txt`
   - Format: `bookmark_id|article_id|article_title|bookmarked_date`
   - Example:
     ```
     1|1|Breaking: New Technology Breakthrough|2025-01-20
     2|3|Business: Market Trends Analysis|2025-01-18
     ```

4. `comments.txt`
   - Format: `comment_id|article_id|article_title|commenter_name|comment_text|comment_date`
   - Example:
     ```
     1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
     2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19
     ```

5. `trending.txt`
   - Format: `article_id|article_title|category|view_count|period`
   - Example:
     ```
     1|Breaking: New Technology Breakthrough|Technology|5432|This Week
     2|Sports: Championship Victory|Sports|3210|This Week
     3|Business: Market Trends Analysis|Business|2891|This Month
     ```

### Read/Write Methods

- **Reading:**
  - Read files line-by-line using UTF-8 encoding.
  - Split each line by pipe character `|`.
  - Parse fields sequentially per format.
- **Writing:**
  - Overwrite files on update.
  - Concatenate data fields joined by pipe `|`.
  - Write each record as a single line.

- All files reside in a local `data/` directory relative to the app root.

---

This specification fully addresses all pages, UI elements with exact IDs, navigation starting from Dashboard, and data storage formats for the NewsPortal Flask app.