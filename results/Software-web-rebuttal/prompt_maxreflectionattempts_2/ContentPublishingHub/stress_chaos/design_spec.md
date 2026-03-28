# ContentPublishingHub Design Specification

---

## Section 1: Flask Routes Specification

| Route Pattern                      | Methods  | Function Name                  | Template Rendered       | Context Variables                             |
|----------------------------------|----------|-------------------------------|------------------------|-----------------------------------------------|
| `/dashboard`                     | GET      | dashboard                     | dashboard.html         | `username` (str), `quick_stats` (dict), `recent_activity` (list of dicts) |
| `/article/create`                | GET, POST| create_article                | create_article.html    | GET: None; POST: form data validation results and status messages |
| `/article/<int:article_id>/edit`| GET, POST| edit_article                  | edit_article.html      | `article` (dict including `title`, `content`, etc.), status messages, validation errors |
| `/article/<int:article_id>/versions`| GET  | article_version_history       | version_history.html   | `versions` (list of dicts), `comparison` (dict or None), `article_id` (int) |
| `/articles/mine`                | GET      | my_articles                   | my_articles.html       | `articles` (list of dicts), `filter_status` (str), `user` (str) |
| `/articles/published`           | GET      | published_articles            | published_articles.html | `articles` (list of dicts), `filter_category` (str), `sort_by` (str) |
| `/calendar`                    | GET, POST | content_calendar              | content_calendar.html   | `calendar_view` (str), `calendar_data` (dict/list), status messages |
| `/article/<int:article_id>/analytics`| GET  | article_analytics             | article_analytics.html | `analytics` (dict), `article_id` (int) |

Notes:
- POST methods in create_article/edit_article/content_calendar handle form submissions.
- All article_id parameters are integers.

---

## Section 2: HTML Template Structures

### 1. dashboard.html
- Page container: `<div id="dashboard-page">`
- Welcome message: `<span id="welcome-message">`
- Quick stats section: `<section id="quick-stats">`
- Create Article button: `<button id="create-article-button">`
- Recent activity feed: `<div id="recent-activity">`

Navigation:
- "Create Article" button links to `/article/create` route

### 2. create_article.html
- Page container: `<div id="create-article-page">`
- Article title input: `<input id="article-title" type="text">`
- Content editor textarea: `<textarea id="article-content"></textarea>`
- Save as Draft button: `<button id="save-draft-button" type="submit">`
- Cancel button: `<button id="cancel-button" type="button">`

Navigation:
- Cancel button redirects to `/dashboard`

### 3. edit_article.html
- Page container: `<div id="edit-article-page">`
- Article title input: `<input id="edit-article-title" type="text">`
- Content editor textarea: `<textarea id="edit-article-content"></textarea>`
- Save New Version button: `<button id="save-version-button" type="submit">`
- Cancel button: `<button id="cancel-edit" type="button">`

Navigation:
- Cancel button redirects to `/dashboard`

### 4. version_history.html
- Page container: `<div id="version-history-page">`
- Versions list: `<ul id="versions-list">` or `<table id="versions-list">`
- Version comparison section: `<div id="version-comparison">`
- Restore button: `<button id="restore-version-1">` (Note: this ID implies for restoring one specific version; multiple restore buttons must have unique IDs following this pattern, e.g. `restore-version-<version_id>`)
- Back to Edit button: `<button id="back-to-edit-history" type="button">`

Navigation:
- Back to Edit button returns to `/article/<article_id>/edit`

### 5. my_articles.html
- Page container: `<div id="my-articles-page">`
- Filter by status dropdown: `<select id="filter-article-status">`
- Articles table: `<table id="articles-table">`
- Create New Article button: `<button id="create-new-article">`
- Back to Dashboard button: `<button id="back-to-dashboard">`

Navigation:
- Create New Article button links to `/article/create`
- Back button links to `/dashboard`

### 6. published_articles.html
- Page container: `<div id="published-articles-page">`
- Filter by category dropdown: `<select id="filter-published-category">`
- Articles grid: `<div id="published-articles-grid">` (likely grid of cards or tiles)
- Sort by dropdown: `<select id="sort-published">`
- Back to Dashboard button: `<button id="back-to-dashboard-published">`

Navigation:
- Back button links to `/dashboard`

### 7. content_calendar.html
- Page container: `<div id="calendar-page">`
- Calendar view selector: `<select id="calendar-view">`
- Calendar grid: `<div id="calendar-grid">`
- Schedule button: `<button id="schedule-button">`
- Back to Dashboard button: `<button id="back-to-dashboard-calendar">`

Navigation:
- Back button links to `/dashboard`

### 8. article_analytics.html
- Page container: `<div id="analytics-page">`
- Analytics overview: `<section id="analytics-overview">`
- Total views: `<span id="analytics-total-views">`
- Unique visitors: `<span id="analytics-unique-visitors">`
- Back to Article button: `<button id="back-to-article-analytics">`

Navigation:
- Back button links to `/article/<article_id>/edit` or article view page

---

## Section 3: Data File Schemas

### 1. users.txt
- Format (pipe-delimited): `username|email|fullname|created_date`
- Fields:
  - username (str): Unique user identifier
  - email (str): User email address
  - fullname (str): User full name
  - created_date (str): Account creation date (`YYYY-MM-DD`)
- Example:
  ```
john|john@example.com|John Doe|2024-01-15
alice|alice@example.com|Alice Smith|2024-01-16
bob|bob@example.com|Bob Johnson|2024-01-17
admin|admin@example.com|Admin User|2024-01-10
```

### 2. articles.txt
- Format: `article_id|title|author|category|status|tags|featured_image|meta_description|created_date|publish_date`
- Fields:
  - article_id (int): Unique article identifier
  - title (str): Article title
  - author (str): Username of author
  - category (str): One of [news, blog, tutorial, announcement, press_release]
  - status (str): One of [draft, pending_review, under_review, approved, published, rejected, archived]
  - tags (str): Comma-separated list of tags
  - featured_image (str): Path to featured image (empty string if none)
  - meta_description (str): Meta description for SEO
  - created_date (str): Date created (`YYYY-MM-DD`)
  - publish_date (str): Datetime of scheduled publish (`YYYY-MM-DD HH:MM:SS`), may be empty if not published
- Example:
  ```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
```

### 3. article_versions.txt
- Format: `version_id|article_id|version_number|content|author|created_date|change_summary`
- Fields:
  - version_id (int): Unique version identifier
  - article_id (int): Related article identifier
  - version_number (int): Sequential version number
  - content (str): Text content of the article version
  - author (str): Username of author who made the version
  - created_date (str): Datetime of version creation (`YYYY-MM-DD HH:MM:SS`)
  - change_summary (str): Summary description of changes
- Example:
  ```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
```

### 4. approvals.txt
- Format: `approval_id|article_id|version_id|approver|status|comments|timestamp`
- Fields:
  - approval_id (int): Unique approval record ID
  - article_id (int): Related article ID
  - version_id (int): Related version ID
  - approver (str): Username of approver
  - status (str): One of [approved, rejected, revision_requested]
  - comments (str): Approver comments
  - timestamp (str): Datetime of approval action (`YYYY-MM-DD HH:MM:SS`)
- Example:
  ```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
```

### 5. workflow_stages.txt
- Format: `stage_id|category|stage_name|stage_order|is_required`
- Fields:
  - stage_id (int): Unique workflow stage ID
  - category (str): Article category this stage applies to
  - stage_name (str): Name of the workflow stage
  - stage_order (int): Order of stage in workflow sequence
  - is_required (str): "yes" or "no" for mandatory stage
- Example:
  ```
1|tutorial|Editor Review|1|yes
2|tutorial|Publisher Approval|2|yes
3|news|Editor Review|1|yes
4|announcement|Editor Review|1|yes
5|announcement|Publisher Approval|2|yes
```

### 6. comments.txt
- Format: `comment_id|article_id|version_id|user|comment_text|timestamp`
- Fields:
  - comment_id (int): Unique comment ID
  - article_id (int): Related article ID
  - version_id (int): Related article version ID
  - user (str): Username who made comment
  - comment_text (str): Text of comment
  - timestamp (str): Datetime of comment (`YYYY-MM-DD HH:MM:SS`)
- Example:
  ```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
```

### 7. analytics.txt
- Format: `analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares`
- Fields:
  - analytics_id (int): Unique analytics record ID
  - article_id (int): Related published article ID
  - date (str): Date of record (`YYYY-MM-DD`)
  - views (int): Number of views
  - unique_visitors (int): Count of unique visitors
  - avg_time_seconds (int): Average time spent in seconds
  - shares (int): Number of times shared
- Example:
  ```
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
```

---

This completes the detailed design specification for the ContentPublishingHub application, providing clear direction for backend route definitions, frontend template structure with element IDs, and data storage schemas for all core functionality described in the user requirements.
