# ContentPublishingHub Design Specification

---

## 1. Flask Routes Specification

| Route URL Pattern             | HTTP Method(s) | Function Name          | Template Rendered       | Context Variables Passed to Template            |
|-------------------------------|----------------|------------------------|-------------------------|-----------------------------------------------|
| `/dashboard`                  | GET            | dashboard              | dashboard.html          | username (str), quick_stats (dict), recent_activity (list of dicts) |
| `/article/create`             | GET, POST      | create_article         | create_article.html     | (GET) - None; (POST - Redirect after save)     |
| `/article/<article_id>/edit` | GET, POST      | edit_article           | edit_article.html       | article_id (int), article_title (str), article_content (str)        |
| `/article/<article_id>/versions` | GET, POST  | version_history        | version_history.html    | article_id (int), versions_list (list of dict), version_comparison (dict), restore_button_id (str: 'restore-version-1') |
| `/articles/mine`             | GET            | my_articles            | my_articles.html        | filter_status_options (list of str), user_articles (list of dicts)  |
| `/articles/published`         | GET            | published_articles     | published_articles.html | filter_category_options (list of str), articles_grid (list of dicts), sort_options (list of str) |
| `/calendar`                  | GET            | content_calendar       | content_calendar.html   | calendar_views (list of str), calendar_events (list of dicts)       |
| `/article/<article_id>/analytics` | GET        | article_analytics      | article_analytics.html  | article_id (int), analytics_overview (dict), total_views (int), unique_visitors (int) |

---

## 2. HTML Template Structures

### 2.1. dashboard.html
- Page container element: `<div>` with id `dashboard-page`
- Elements:
  - Welcome message: id `welcome-message` (displays username)
  - Quick stats section: id `quick-stats` (shows key statistics)
  - Create Article button: id `create-article-button` (navigates to `/article/create`)
  - Recent activity feed: id `recent-activity` (shows recent user or system activities)

### 2.2. create_article.html
- Page container element: `<div>` with id `create-article-page`
- Elements:
  - Article title input field: `<input>` with id `article-title`
  - Content editor textarea: `<textarea>` with id `article-content`
  - Save as Draft button: `<button>` with id `save-draft-button`
  - Cancel button: `<button>` with id `cancel-button` (navigates back to dashboard or previous page)

### 2.3. edit_article.html
- Page container element: `<div>` with id `edit-article-page`
- Elements:
  - Article title input field: `<input>` with id `edit-article-title`
  - Content editor textarea: `<textarea>` with id `edit-article-content`
  - Save New Version button: `<button>` with id `save-version-button`
  - Cancel button: `<button>` with id `cancel-edit` (navigates back to previous or dashboard)

### 2.4. version_history.html
- Page container element: `<div>` with id `version-history-page`
- Elements:
  - Versions list container: id `versions-list` (displays all versions for an article)
  - Version comparison section: id `version-comparison` (to compare selected versions)
  - Restore button: `<button>` with id `restore-version-1`
  - Back to Edit button: `<button>` with id `back-to-edit-history` (navigates back to edit article page)

### 2.5. my_articles.html
- Page container element: `<div>` with id `my-articles-page`
- Elements:
  - Filter by status dropdown: `<select>` with id `filter-article-status`
  - Articles table: `<table>` with id `articles-table` (displays user articles with columns such as Title, Status, Date)
  - Create New Article button: `<button>` with id `create-new-article` (navigates to `/article/create`)
  - Back to Dashboard button: `<button>` with id `back-to-dashboard` (navigates to `/dashboard`)

### 2.6. published_articles.html
- Page container element: `<div>` with id `published-articles-page`
- Elements:
  - Filter by category dropdown: `<select>` with id `filter-published-category`
  - Articles grid: `<div>` or similar with id `published-articles-grid` (displays published articles as a grid or cards)
  - Sort by dropdown: `<select>` with id `sort-published`
  - Back to Dashboard button: `<button>` with id `back-to-dashboard-published` (navigates to `/dashboard`)

### 2.7. content_calendar.html
- Page container element: `<div>` with id `calendar-page`
- Elements:
  - Calendar view selector: `<select>` with id `calendar-view` (e.g., daily, weekly, monthly views)
  - Calendar grid: `<div>` with id `calendar-grid` (displays scheduled articles on calendar slots)
  - Schedule button: `<button>` with id `schedule-button` (to schedule new publication)
  - Back to Dashboard button: `<button>` with id `back-to-dashboard-calendar` (navigates to `/dashboard`)

### 2.8. article_analytics.html
- Page container element: `<div>` with id `analytics-page`
- Elements:
  - Analytics overview section: `<div>` with id `analytics-overview` (summarizes key metrics)
  - Total views display: element with id `analytics-total-views`
  - Unique visitors display: element with id `analytics-unique-visitors`
  - Back to Article button: `<button>` with id `back-to-article-analytics` (navigates back to article edit or view page)

---

## 3. Data File Schemas

### 3.1. users.txt
- Format: `username|email|fullname|created_date`
- Fields:
  1. username (str) - unique user identifier
  2. email (str) - user email address
  3. fullname (str) - full name of user
  4. created_date (date in YYYY-MM-DD format) - account creation date
- Example rows:
  ```
john|john@example.com|John Doe|2024-01-15
alice|alice@example.com|Alice Smith|2024-01-16
bob|bob@example.com|Bob Johnson|2024-01-17
admin|admin@example.com|Admin User|2024-01-10
  ```

### 3.2. articles.txt
- Format: `article_id|title|author|category|status|tags|featured_image|meta_description|created_date|publish_date`
- Fields:
  1. article_id (int) - unique article identifier
  2. title (str) - article title
  3. author (str) - username of the article author
  4. category (str) - one of: news, blog, tutorial, announcement, press_release
  5. status (str) - one of: draft, pending_review, under_review, approved, published, rejected, archived
  6. tags (str) - comma-separated tags
  7. featured_image (str) - path or URL to image; may be empty
  8. meta_description (str) - short description for SEO
  9. created_date (date in YYYY-MM-DD format)
 10. publish_date (datetime in YYYY-MM-DD HH:MM:SS format) or empty if unpublished
- Example rows:
  ```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
  ```

### 3.3. article_versions.txt
- Format: `version_id|article_id|version_number|content|author|created_date|change_summary`
- Fields:
  1. version_id (int) - unique version identifier
  2. article_id (int) - reference to article
  3. version_number (int) - incremental version count
  4. content (str) - full text content of the version
  5. author (str) - username who created this version
  6. created_date (datetime YYYY-MM-DD HH:MM:SS)
  7. change_summary (str) - short summary of changes
- Example rows:
  ```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
  ```

### 3.4. approvals.txt
- Format: `approval_id|article_id|version_id|approver|status|comments|timestamp`
- Fields:
  1. approval_id (int) - unique approval record
  2. article_id (int) - associated article
  3. version_id (int) - associated article version
  4. approver (str) - username of approver
  5. status (str) - one of: approved, rejected, revision_requested
  6. comments (str) - approver comments
  7. timestamp (datetime YYYY-MM-DD HH:MM:SS)
- Example rows:
  ```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
  ```

### 3.5. workflow_stages.txt
- Format: `stage_id|category|stage_name|stage_order|is_required`
- Fields:
  1. stage_id (int) - unique stage identifier
  2. category (str) - article category
  3. stage_name (str) - name of workflow stage
  4. stage_order (int) - order in workflow
  5. is_required (str) - "yes" or "no"
- Example rows:
  ```
1|tutorial|Editor Review|1|yes
2|tutorial|Publisher Approval|2|yes
3|news|Editor Review|1|yes
4|announcement|Editor Review|1|yes
5|announcement|Publisher Approval|2|yes
  ```

### 3.6. comments.txt
- Format: `comment_id|article_id|version_id|user|comment_text|timestamp`
- Fields:
  1. comment_id (int) - unique comment identifier
  2. article_id (int) - article related
  3. version_id (int) - article version related
  4. user (str) - username who made comment
  5. comment_text (str) - comment content
  6. timestamp (datetime YYYY-MM-DD HH:MM:SS)
- Example rows:
  ```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
  ```

### 3.7. analytics.txt
- Format: `analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares`
- Fields:
  1. analytics_id (int) - unique analytics record
  2. article_id (int) - article referenced
  3. date (date YYYY-MM-DD) - date of analytics record
  4. views (int) - number of views
  5. unique_visitors (int) - count of unique visitors
  6. avg_time_seconds (int) - average time spent in seconds
  7. shares (int) - number of shares
- Example rows:
  ```
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
  ```

---

This design specification allows the backend and frontend teams to implement the ContentPublishingHub application independently and consistently per the supplied user requirements.
