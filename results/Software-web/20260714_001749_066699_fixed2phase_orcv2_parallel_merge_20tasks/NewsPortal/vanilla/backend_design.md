# NewsPortal Backend Design Specification

---

## Section 1: Flask Routes Specification

### 1. Dashboard Page
- **Route:** `/` 
- **Methods:** GET
- **Function:** `dashboard()`
- **Behavior:**
  - Reads `articles.txt` to fetch featured articles.
  - Reads `trending.txt` for trending articles.
  - Returns a rendered template or JSON containing featured & trending articles summary.

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

### 3. Article Details Page
- **Route:** `/article/<int:article_id>`
- **Methods:** GET
- **Function:** `article_details(article_id)`
- **Behavior:**
  - Reads `articles.txt` to display full article details.
  - Increments and updates the 'views' count for the article in `articles.txt` (write-back updated views).
  - Returns the article detail data.

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

### 7. Comments Page
- **Route:** `/comments`
- **Methods:** GET
- **Function:** `comments_list()`
- **Inputs:** Optional query parameter `article_id` for filtering.
- **Behavior:**
  - Reads `comments.txt` and optionally filters by article_id.
  - Returns all or filtered comments.

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

### 9. Trending Articles Page
- **Route:** `/trending`
- **Methods:** GET
- **Function:** `trending_articles()`
- **Inputs:** Optional query parameter `period` (Today, This Week, This Month).
- **Behavior:**
  - Reads `trending.txt`, filters by period.
  - Returns trending articles list.

### 10. Category Page
- **Route:** `/category/<string:category_name>`
- **Methods:** GET
- **Function:** `category_articles(category_name)`
- **Inputs:** Optional query parameter `sort_by` (date or popularity/views).
- **Behavior:**
  - Reads `articles.txt`, filters by category.
  - Sorts by date or views as per query.
  - Returns list of articles.

### 11. Search Results Page
- **Route:** `/search`
- **Methods:** GET
- **Function:** `search_articles()`
- **Inputs:** Query parameter `q` (search text).
- **Behavior:**
  - Reads `articles.txt`.
  - Filters articles matching query in title, author, or keywords in content.
  - Returns matched articles.

---

## Section 2: Data File Schemas

### 1. Articles Data
- **File:** `data/articles.txt`
- **Format:**
  - Fields: `article_id|title|author|category|content|date|views`
  - Delimiter: pipe (`|`)
  - `article_id`: integer, unique
  - `title`: string
  - `author`: string
  - `category`: string (must match category_name in categories.txt)
  - `content`: string (article body, no pipe characters inside)
  - `date`: ISO format date `YYYY-MM-DD`
  - `views`: integer (non-negative)

- **Example line:**
  ```
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  ```

- **Manipulations:**
  - Views incremented on each article detail page GET, updated back to file.
  - New articles not specified in requirements (read-only for now).

### 2. Categories Data
- **File:** `data/categories.txt`
- **Format:**
  - Fields: `category_id|category_name|description`
  - Delimiter: pipe (`|`)
  - `category_id`: integer, unique
  - `category_name`: string
  - `description`: string

- **Example line:**
  ```
  1|Technology|Latest tech news and innovations
  ```

- **Manipulations:** Read-only for category filtering and dropdown building.

### 3. Bookmarks Data
- **File:** `data/bookmarks.txt`
- **Format:**
  - Fields: `bookmark_id|article_id|article_title|bookmarked_date`
  - Delimiter: pipe (`|`)
  - `bookmark_id`: integer, unique
  - `article_id`: integer, must refer to existing article
  - `article_title`: string (cached from articles.txt for display)
  - `bookmarked_date`: ISO date `YYYY-MM-DD`

- **Example line:**
  ```
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  ```

- **Manipulations:**
  - New bookmark added on POST by finding max `bookmark_id` + 1.
  - Bookmark removed by `bookmark_id`.

### 4. Comments Data
- **File:** `data/comments.txt`
- **Format:**
  - Fields: `comment_id|article_id|article_title|commenter_name|comment_text|comment_date`
  - Delimiter: pipe (`|`)
  - `comment_id`: integer, unique
  - `article_id`: integer, refers to article
  - `article_title`: string
  - `commenter_name`: string
  - `comment_text`: string
  - `comment_date`: ISO date `YYYY-MM-DD`

- **Example line:**
  ```
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  ```

- **Manipulations:**
  - New comments appended with max `comment_id` + 1.
  - No edits or deletes defined.

### 5. Trending Data
- **File:** `data/trending.txt`
- **Format:**
  - Fields: `article_id|article_title|category|view_count|period`
  - Delimiter: pipe (`|`)
  - `article_id`: integer
  - `article_title`: string
  - `category`: string
  - `view_count`: integer
  - `period`: string ("Today", "This Week", "This Month")

- **Example line:**
  ```
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  ```

- **Manipulations:**
  - Read-only for display, updated externally.

---

## Section 3: Operational Notes

- Authentication and user management are not involved; all users have full access.
- Data files are stored locally in the `data` directory relative to the Flask application.
- All write operations must update the respective text files completely (read-modify-write).
- All read operations must handle file reading from the local filesystem.
- Data formats and delimiters must be strictly followed for consistency.
- Appropriate error handling and validation must be implemented for data integrity.

---

This specification is sufficient for backend development of the NewsPortal application with Flask using local text files for data management.