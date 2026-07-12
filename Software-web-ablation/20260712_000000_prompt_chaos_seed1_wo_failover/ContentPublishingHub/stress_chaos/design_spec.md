# ContentPublishingHub Design Specification

---

## Section 1: Flask Routes Specification

| Route                              | HTTP Method(s) | Function Name               | Template Rendered         | Context Variables (name: type & description)                                    |
|-----------------------------------|----------------|-----------------------------|---------------------------|---------------------------------------------------------------------------------|
| /dashboard                       | GET            | dashboard                   | dashboard.html            | username: string (logged-in user's username)
 quick_stats: dict (stat name to value)
 recent_activity: list of dicts (each with details for activity feed)
 |
| /article/create                  | GET, POST      | create_article              | create_article.html       | (GET) no context variables or defaults
 (POST) form data processed, on GET typically context empty or messages |
| /article/<article_id>/edit       | GET, POST      | edit_article                | edit_article.html         | article_id: int|string
 article: dict with fields title, content, etc.
 versions: list (optional for version history display on edit)
 |
| /article/<article_id>/versions   | GET            | article_version_history     | version_history.html      | article_id: int|string
 versions: list of version dicts with version_id, version_number, content summary, author, created_date, change_summary |
| /articles/mine                  | GET            | my_articles                 | my_articles.html          | username: string
 filter_status: string (selected filter)
 articles: list of article dicts with fields id, title, status, etc. |
| /articles/published             | GET            | published_articles          | published_articles.html   | filter_category: string (selected category)
 sort_by: string (selected sort field)
 articles: list of dicts with article data for published articles |
| /calendar                      | GET            | content_calendar            | content_calendar.html     | calendar_view: string (current viewed timeline)
 scheduled_items: list of dict, scheduled articles info |
| /article/<article_id>/analytics  | GET            | article_analytics           | article_analytics.html    | article_id: int|string
 analytics_summary: dict with keys total_views, unique_visitors, avg_time_seconds, shares |

---

## Section 2: HTML Template Structure

### 1. dashboard.html
- Page container id: `dashboard-page`
- Elements:
  - Welcome message (id: `welcome-message`)
  - Quick stats section (id: `quick-stats`)
  - Create Article button (id: `create-article-button`)
  - Recent activity feed (id: `recent-activity`)
- Navigation:
  - Create Article button links to `/article/create`
  - Navigation to other main pages via UI elements (not explicitly specified)

### 2. create_article.html
- Page container id: `create-article-page`
- Elements:
  - Article title input (id: `article-title`)
  - Content editor textarea (id: `article-content`)
  - Save as Draft button (id: `save-draft-button`)
  - Cancel button (id: `cancel-button`)
- Navigation:
  - Cancel button navigates back (likely dashboard or previous page)

### 3. edit_article.html
- Page container id: `edit-article-page`
- Elements:
  - Article title input (id: `edit-article-title`)
  - Content editor textarea (id: `edit-article-content`)
  - Save New Version button (id: `save-version-button`)
  - Cancel button (id: `cancel-edit`)
- Navigation:
  - Cancel button navigates back to article or previous page

### 4. version_history.html
- Page container id: `version-history-page`
- Elements:
  - Versions list container (id: `versions-list`)
  - Version comparison section (id: `version-comparison`)
  - Restore button with id `restore-version-1` (assuming first version for example)
  - Back to Edit button (id: `back-to-edit-history`)
- Navigation:
  - Back to Edit button links back to edit article page

### 5. my_articles.html
- Page container id: `my-articles-page`
- Elements:
  - Filter by status dropdown (id: `filter-article-status`)
  - Articles table (id: `articles-table`)
  - Create New Article button (id: `create-new-article`)
  - Back to Dashboard button (id: `back-to-dashboard`)
- Navigation:
  - Create New Article button links to `/article/create`
  - Back to Dashboard button links to `/dashboard`

### 6. published_articles.html
- Page container id: `published-articles-page`
- Elements:
  - Filter by category dropdown (id: `filter-published-category`)
  - Articles grid (id: `published-articles-grid`)
  - Sort by dropdown (id: `sort-published`)
  - Back to Dashboard button (id: `back-to-dashboard-published`)
- Navigation:
  - Back to Dashboard button links to `/dashboard`

### 7. content_calendar.html
- Page container id: `calendar-page`
- Elements:
  - Calendar view selector dropdown (id: `calendar-view`)
  - Calendar grid container (id: `calendar-grid`)
  - Schedule button (id: `schedule-button`)
  - Back to Dashboard button (id: `back-to-dashboard-calendar`)
- Navigation:
  - Back to Dashboard button links to `/dashboard`

### 8. article_analytics.html
- Page container id: `analytics-page`
- Elements:
  - Analytics overview container (id: `analytics-overview`)
  - Total views display (id: `analytics-total-views`)
  - Unique visitors display (id: `analytics-unique-visitors`)
  - Back to Article button (id: `back-to-article-analytics`)
- Navigation:
  - Back to Article button links back to `/article/<article_id>/edit` or article page

---

## Section 3: Data File Schemas

### 1. users.txt
- Fields: `username|email|fullname|created_date`
- Description:
  - username: string, unique identifier for user
  - email: string, user's email address
  - fullname: string, user's full name
  - created_date: date in YYYY-MM-DD format
- Example:
  ```
  john|john@example.com|John Doe|2024-01-15
  alice|alice@example.com|Alice Smith|2024-01-16
  bob|bob@example.com|Bob Johnson|2024-01-17
  admin|admin@example.com|Admin User|2024-01-10
  ```

### 2. articles.txt
- Fields: `article_id|title|author|category|status|tags|featured_image|meta_description|created_date|publish_date`
- Description:
  - article_id: int, unique article identifier
  - title: string
  - author: string (username)
  - category: string enum (news, blog, tutorial, announcement, press_release)
  - status: string enum (draft, pending_review, under_review, approved, published, rejected, archived)
  - tags: comma-separated string list
  - featured_image: string URL or empty
  - meta_description: string
  - created_date: date YYYY-MM-DD
  - publish_date: datetime YYYY-MM-DD HH:MM:SS or empty if unpublished
- Example:
  ```
  1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
  2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
  3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
  ```

### 3. article_versions.txt
- Fields: `version_id|article_id|version_number|content|author|created_date|change_summary`
- Description:
  - version_id: int unique version identifier
  - article_id: int foreign key linking to articles.txt
  - version_number: int (incrementing per article)
  - content: string (full article content text)
  - author: string (username who edited)
  - created_date: datetime YYYY-MM-DD HH:MM:SS
  - change_summary: string describing version changes
- Example:
  ```
  1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
  2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
  3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
  ```

### 4. approvals.txt
- Fields: `approval_id|article_id|version_id|approver|status|comments|timestamp`
- Description:
  - approval_id: int unique approval record
  - article_id: int
  - version_id: int
  - approver: string (username)
  - status: string enum (approved, rejected, revision_requested)
  - comments: string
  - timestamp: datetime YYYY-MM-DD HH:MM:SS
- Example:
  ```
  1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
  2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
  3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
  ```

### 5. workflow_stages.txt
- Fields: `stage_id|category|stage_name|stage_order|is_required`
- Description:
  - stage_id: int unique
  - category: string (article category)
  - stage_name: string
  - stage_order: int (order of workflow stage)
  - is_required: string enum ('yes', 'no')
- Example:
  ```
  1|tutorial|Editor Review|1|yes
  2|tutorial|Publisher Approval|2|yes
  3|news|Editor Review|1|yes
  4|announcement|Editor Review|1|yes
  5|announcement|Publisher Approval|2|yes
  ```

### 6. comments.txt
- Fields: `comment_id|article_id|version_id|user|comment_text|timestamp`
- Description:
  - comment_id: int unique
  - article_id: int
  - version_id: int
  - user: string (username who commented)
  - comment_text: string
  - timestamp: datetime YYYY-MM-DD HH:MM:SS
- Example:
  ```
  1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
  2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
  3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
  ```

### 7. analytics.txt
- Fields: `analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares`
- Description:
  - analytics_id: int unique
  - article_id: int
  - date: date YYYY-MM-DD
  - views: int number of views
  - unique_visitors: int
  - avg_time_seconds: int average time on page
  - shares: int number of shares
- Example:
  ```
  1|1|2024-01-22|150|120|245|12
  2|1|2024-01-23|230|180|210|18
  3|1|2024-01-24|180|140|220|15
  4|2|2024-01-25|95|75|180|8
  ```

---

This specification document provides clear definitions for routes, template elements, and data file formats enabling separation of backend and frontend development for the ContentPublishingHub application.