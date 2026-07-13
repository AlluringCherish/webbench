# NewsPortal Frontend Design Specification

---

## Section 1: Page Template Specifications

### 1. Dashboard Page
- Filename: dashboard.html
- Page Title: News Portal
- Container Divs:
  - `dashboard-page` (Div) - Main container for the dashboard page.
- UI Elements:
  - `featured-articles` (Div) - Displays featured article recommendations.
  - `browse-articles-button` (Button) - Navigates to Article Catalog page.
  - `view-bookmarks-button` (Button) - Navigates to Bookmarks page.
  - `trending-articles-button` (Button) - Navigates to Trending Articles page.

### 2. Article Catalog Page
- Filename: article_catalog.html
- Page Title: Article Catalog
- Container Divs:
  - `catalog-page` (Div) - Main container for the catalog page.
- UI Elements:
  - `search-input` (Input, type="text") - Text field to search articles by title, author, or keywords.
  - `category-filter` (Dropdown/select) - Dropdown to filter articles by category (Technology, Sports, Business, Health, Entertainment, etc.).
  - `articles-grid` (Div) - Grid container displaying article cards.
  - `view-article-button-{article_id}` (Button) - In each article card; navigates to Article Details page for the article.

### 3. Article Details Page
- Filename: article_details.html
- Page Title: Article Details
- Container Divs:
  - `article-details-page` (Div) - Main container for the article details page.
- UI Elements:
  - `article-title` (H1) - Displays the article title.
  - `article-author` (Div) - Displays the author name.
  - `article-date` (Div) - Displays publication date.
  - `bookmark-button` (Button) - Adds article to bookmarks.
  - `article-content` (Div) - Displays full article content.

### 4. Bookmarks Page
- Filename: bookmarks.html
- Page Title: My Bookmarks
- Container Divs:
  - `bookmarks-page` (Div) - Main container for bookmarks page.
- UI Elements:
  - `bookmarks-list` (Div) - List container for bookmarked articles.
  - `remove-bookmark-button-{bookmark_id}` (Button) - Removes specific bookmark.
  - `read-bookmark-button-{bookmark_id}` (Button) - Opens the bookmarked article in Article Details.
  - `back-to-dashboard` (Button) - Navigates back to Dashboard page.

### 5. Comments Page
- Filename: comments.html
- Page Title: Article Comments
- Container Divs:
  - `comments-page` (Div) - Main container for comments page.
- UI Elements:
  - `comments-list` (Div) - Displays all comments with article title, commenter name, and text.
  - `write-comment-button` (Button) - Navigates to Write Comment page.
  - `filter-by-article` (Dropdown/select) - Filter comments by article.
  - `back-to-dashboard` (Button) - Navigates back to Dashboard page.

### 6. Write Comment Page
- Filename: write_comment.html
- Page Title: Write a Comment
- Container Divs:
  - `write-comment-page` (Div) - Container for write comment page.
- UI Elements:
  - `select-article` (Dropdown/select) - Dropdown to select article to comment on.
  - `commenter-name` (Input, type="text") - Input field for commenter's name.
  - `comment-text` (Textarea) - Textarea for comment content.
  - `submit-comment-button` (Button) - Submit the new comment.

### 7. Trending Articles Page
- Filename: trending.html
- Page Title: Trending Articles
- Container Divs:
  - `trending-page` (Div) - Main container for trending articles page.
- UI Elements:
  - `trending-list` (Div) - Ranked list of trending articles with rank, title, category, and view count.
  - `time-period-filter` (Dropdown/select) - Filter trending articles by time period (Today, This Week, This Month).
  - `view-article-button-{article_id}` (Button) - View details of trending article.
  - `back-to-dashboard` (Button) - Navigate back to Dashboard.

### 8. Category Page
- Filename: category.html
- Page Title: Category Articles
- Container Divs:
  - `category-page` (Div) - Main container for category page.
- UI Elements:
  - `category-title` (H1) - Displays category name.
  - `category-articles` (Div) - List of articles for the category.
  - `sort-by-date` (Button) - Sort articles by publication date.
  - `sort-by-popularity` (Button) - Sort articles by popularity.
  - `back-to-dashboard` (Button) - Navigate back to Dashboard.

### 9. Search Results Page
- Filename: search_results.html
- Page Title: Search Results
- Container Divs:
  - `search-results-page` (Div) - Main container for search results.
- UI Elements:
  - `search-query-display` (Div) - Displays the search query string.
  - `results-list` (Div) - Lists search results with article titles and excerpts.
  - `no-results-message` (Div) - Displays message if no search results.
  - `back-to-dashboard` (Button) - Navigate back to Dashboard.

---

## Section 2: Navigation and Interaction

- Button `browse-articles-button` on Dashboard -> navigates to Article Catalog page.
- Button `view-bookmarks-button` on Dashboard -> navigates to Bookmarks page.
- Button `trending-articles-button` on Dashboard -> navigates to Trending Articles page.

- `view-article-button-{article_id}` on Article Catalog and Trending pages -> opens the Article Details page for the specified article.

- Button `bookmark-button` on Article Details -> adds current article to bookmarks.

- Buttons on Bookmarks page:
  - `remove-bookmark-button-{bookmark_id}` -> removes specific bookmark.
  - `read-bookmark-button-{bookmark_id}` -> opens Article Details page for that bookmarked article.
  - `back-to-dashboard` -> returns to Dashboard.

- Comments page:
  - `write-comment-button` -> navigates to Write Comment page.
  - `filter-by-article` dropdown filters displayed comments by selected article.
  - `back-to-dashboard` returns to Dashboard.

- Write Comment page:
  - `submit-comment-button` submits the comment and typically navigates back to Comments page.

- Trending page:
  - `time-period-filter` filters articles by selected time period.
  - `view-article-button-{article_id}` views details of trending article.
  - `back-to-dashboard` returns to Dashboard.

- Category page:
  - `sort-by-date` sorts category articles by date.
  - `sort-by-popularity` sorts category articles by popularity.
  - `back-to-dashboard` returns to Dashboard.

- Search Results page:
  - `back-to-dashboard` returns to Dashboard.

- Search input (`search-input`) on Article Catalog enables text searching by title, author, or keywords.
- Category filter (`category-filter`) on Article Catalog allows filtering articles shown.

---

## Section 3: Layout and Usability Notes

- Each page main container div (e.g. `dashboard-page`, `catalog-page`) wraps entire page content for easy styling and dynamic content insertion.
- Buttons and interactive elements have distinct IDs with article or bookmark IDs suffixed where applicable for event handling and unique targeting.
- Dropdowns use standard select elements to enable keyboard navigation and accessibility.
- Back to dashboard buttons provide a consistent user experience and easy return path from subsidiary pages.
- Article lists (e.g., `articles-grid`, `bookmarks-list`, `trending-list`, `category-articles`, `results-list`) are div containers expected to hold dynamically rendered lists or cards.
- For article cards and bookmark items, the buttons with IDs suffixed by dynamic IDs enable direct operations on that item.
- Text inputs and textarea fields have clear IDs for binding form data.
- Titles (H1) and date displays have clear, semantic tags for screen readers.
- Recommended to implement responsive design layouts so lists and grids adapt well on different screen sizes.
- UI flows prioritize quick navigation via clearly labeled buttons and dropdowns.

---

This specification provides all element IDs, interaction schemes, and layout grouping needed for frontend implementation of the NewsPortal application.
