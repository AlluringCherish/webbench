# Requirements Document for 'NewsPortal' Web Application

## 1. Objective
Develop a comprehensive web application named 'NewsPortal' using Python, with data managed through local text files. The application enables users to browse news articles by category, read detailed articles, bookmark favorites, view comments, and track trending articles. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'NewsPortal' application is Python.

## 3. Page Design

The 'NewsPortal' web application will consist of the following nine pages:

### 1. Dashboard Page
- **Page Title**: News Portal
- **Overview**: The main hub displaying featured articles, trending news, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-articles** - Type: Div - Display of featured article recommendations.
  - **ID: browse-articles-button** - Type: Button - Button to navigate to article catalog page.
  - **ID: view-bookmarks-button** - Type: Button - Button to navigate to bookmarks page.
  - **ID: trending-articles-button** - Type: Button - Button to navigate to trending articles page.

### 2. Article Catalog Page
- **Page Title**: Article Catalog
- **Overview**: A page displaying all available articles with search and filter capabilities.
- **Elements**:
  - **ID: catalog-page** - Type: Div - Container for the catalog page.
  - **ID: search-input** - Type: Input - Field to search articles by title, author, or keywords.
  - **ID: category-filter** - Type: Dropdown - Dropdown to filter by category (Technology, Sports, Business, Health, Entertainment, etc.).
  - **ID: articles-grid** - Type: Div - Grid displaying article cards with thumbnail, title, author, and date.
  - **ID: view-article-button-{article_id}** - Type: Button - Button to view article details (each article card has this).

### 3. Article Details Page
- **Page Title**: Article Details
- **Overview**: A page displaying detailed information about a specific article.
- **Elements**:
  - **ID: article-details-page** - Type: Div - Container for the article details page.
  - **ID: article-title** - Type: H1 - Display article title.
  - **ID: article-author** - Type: Div - Display article author.
  - **ID: article-date** - Type: Div - Display article publication date.
  - **ID: bookmark-button** - Type: Button - Button to bookmark the article.
  - **ID: article-content** - Type: Div - Section displaying the full article content.

### 4. Bookmarks Page
- **Page Title**: My Bookmarks
- **Overview**: A page displaying all bookmarked articles with removal and reading options.
- **Elements**:
  - **ID: bookmarks-page** - Type: Div - Container for the bookmarks page.
  - **ID: bookmarks-list** - Type: Div - List displaying all bookmarked articles with title and date.
  - **ID: remove-bookmark-button-{bookmark_id}** - Type: Button - Button to remove bookmark (each bookmark has this).
  - **ID: read-bookmark-button-{bookmark_id}** - Type: Button - Button to read bookmarked article (each bookmark has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 5. Comments Page
- **Page Title**: Article Comments
- **Overview**: A page displaying all comments on articles and allowing users to write new comments.
- **Elements**:
  - **ID: comments-page** - Type: Div - Container for the comments page.
  - **ID: comments-list** - Type: Div - List of all comments with article title, commenter name, and comment text.
  - **ID: write-comment-button** - Type: Button - Button to navigate to write comment page.
  - **ID: filter-by-article** - Type: Dropdown - Dropdown to filter comments by article.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 6. Write Comment Page
- **Page Title**: Write a Comment
- **Overview**: A page for users to write comments on articles.
- **Elements**:
  - **ID: write-comment-page** - Type: Div - Container for the write comment page.
  - **ID: select-article** - Type: Dropdown - Dropdown to select article to comment on.
  - **ID: commenter-name** - Type: Input - Field to input commenter name.
  - **ID: comment-text** - Type: Textarea - Field to write comment text.
  - **ID: submit-comment-button** - Type: Button - Button to submit comment.

### 7. Trending Articles Page
- **Page Title**: Trending Articles
- **Overview**: A page displaying top trending articles ranked by views and engagement.
- **Elements**:
  - **ID: trending-page** - Type: Div - Container for the trending articles page.
  - **ID: trending-list** - Type: Div - Ranked list of trending articles with rank, title, category, and view count.
  - **ID: time-period-filter** - Type: Dropdown - Dropdown to filter by time period (Today, This Week, This Month).
  - **ID: view-article-button-{article_id}** - Type: Button - Button to view article details (each trending article has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Category Page
- **Page Title**: Category Articles
- **Overview**: A page displaying articles from a specific category.
- **Elements**:
  - **ID: category-page** - Type: Div - Container for the category page.
  - **ID: category-title** - Type: H1 - Display the category name.
  - **ID: category-articles** - Type: Div - List of articles in the selected category.
  - **ID: sort-by-date** - Type: Button - Button to sort articles by date.
  - **ID: sort-by-popularity** - Type: Button - Button to sort articles by popularity.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 9. Search Results Page
- **Page Title**: Search Results
- **Overview**: A page displaying search results based on user query.
- **Elements**:
  - **ID: search-results-page** - Type: Div - Container for the search results page.
  - **ID: search-query-display** - Type: Div - Display the search query performed.
  - **ID: results-list** - Type: Div - List of search results with article title and excerpt.
  - **ID: no-results-message** - Type: Div - Message displayed when no results found.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'NewsPortal' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Articles Data
- **File Name**: `articles.txt`
- **Data Format**:
  ```
  article_id|title|author|category|content|date|views
  ```
- **Example Data**:
  ```
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891
  ```

### 2. Categories Data
- **File Name**: `categories.txt`
- **Data Format**:
  ```
  category_id|category_name|description
  ```
- **Example Data**:
  ```
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news
  ```

### 3. Bookmarks Data
- **File Name**: `bookmarks.txt`
- **Data Format**:
  ```
  bookmark_id|article_id|article_title|bookmarked_date
  ```
- **Example Data**:
  ```
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18
  ```

### 4. Comments Data
- **File Name**: `comments.txt`
- **Data Format**:
  ```
  comment_id|article_id|article_title|commenter_name|comment_text|comment_date
  ```
- **Example Data**:
  ```
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19
  ```

### 5. Trending Data
- **File Name**: `trending.txt`
- **Data Format**:
  ```
  article_id|article_title|category|view_count|period
  ```
- **Example Data**:
  ```
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month
  ```
