# ContentPublishingHub Design Specification

---

## Section 1: Flask Routes Specification

| Route                                  | HTTP Methods | Function Name                | Template Name          | Context Variables                                                                                       |
|----------------------------------------|--------------|------------------------------|------------------------|-------------------------------------------------------------------------------------------------------|
| /dashboard                             | GET          | dashboard                   | dashboard.html         | username (str), quick_stats (dict), recent_activity (list of dicts)                                   |
| /article/create                       | GET, POST    | create_article              | create_article.html    | (GET) None, (POST) form data handling                                                                |
| /article/<article_id>/edit            | GET, POST    | edit_article                | edit_article.html      | article_id (int), article (dict with title, content, etc.), versions (list), author (str)            |
| /article/<article_id>/versions        | GET          | article_version_history     | version_history.html   | article_id (int), versions (list of version dicts), comparison_data (dict)                            |
| /articles/mine                       | GET          | my_articles                 | my_articles.html       | username (str), articles (list of articles dicts), filter_status (str)                               |
| /articles/published                  | GET          | published_articles          | published_articles.html| articles (list of articles dict), filter_category (str), sort_option (str)                           |
| /calendar                            | GET          | content_calendar            | content_calendar.html  | schedule_events (list), calendar_view (str)                                                          |
| /article/<article_id>/analytics       | GET          | article_analytics           | article_analytics.html | article_id (int), analytics_data (dict)                                                              |

---

## Section 2: HTML Template Structure

### 1. dashboard.html
- Container element: `<div id="dashboard-page">`
- Elements:
  - Welcome message: `<span id="welcome-message">` (displays username)
  - Quick stats section: `<div id="quick-stats">`
  - Create Article button: `<button id="create-article-button">`
  - Recent activity feed: `<div id="recent-activity">`
- Navigation:
  - "Create Article" navigates to `/article/create`

### 2. create_article.html
- Container element: `<div id="create-article-page">`
- Elements:
  - Article title input: `<input type="text" id="article-title">`
  - Content editor: `<textarea id="article-content">`
  - Save as Draft button: `<button id="save-draft-button">`
  - Cancel button: `<button id="cancel-button">`
- Navigation:
  - Cancel returns to `/dashboard`

### 3. edit_article.html
- Container element: `<div id="edit-article-page">`
- Elements:
  - Article title input: `<input type="text" id="edit-article-title">`
  - Content editor: `<textarea id="edit-article-content">`
  - Save New Version button: `<button id="save-version-button">`
  - Cancel button: `<button id="cancel-edit">`
- Navigation:
  - Cancel returns to `/articles/mine` or previous page

### 4. version_history.html
- Container element: `<div id="version-history-page">`
- Elements:
  - Versions list: `<ul id="versions-list">` listing versions with version numbers and dates
  - Version comparison section: `<div id="version-comparison">`
  - Restore button: `<button id="restore-version-1">` (the ID suggests possibly dynamic per version, adapt accordingly)
  - Back to Edit button: `<button id="back-to-edit-history">`
- Navigation:
  - Back to edit article on `/article/<article_id>/edit`

### 5. my_articles.html
- Container element: `<div id="my-articles-page">`
- Elements:
  - Filter by status dropdown: `<select id="filter-article-status">`
  - Articles table: `<table id="articles-table">`
  - Create New Article button: `<button id="create-new-article">`
  - Back to Dashboard button: `<button id="back-to-dashboard">`
- Navigation:
  - Create new article goes to `/article/create`
  - Back to dashboard goes to `/dashboard`

### 6. published_articles.html
- Container element: `<div id="published-articles-page">`
- Elements:
  - Filter by category dropdown: `<select id="filter-published-category">`
  - Articles grid: `<div id="published-articles-grid">`
  - Sort by dropdown: `<select id="sort-published">`
  - Back to Dashboard button: `<button id="back-to-dashboard-published">`
- Navigation:
  - Back to dashboard goes to `/dashboard`

### 7. content_calendar.html
- Container element: `<div id="calendar-page">`
- Elements:
  - Calendar view selector: `<select id="calendar-view">`
  - Calendar grid: `<div id="calendar-grid">`
  - Schedule button: `<button id="schedule-button">`
  - Back to Dashboard button: `<button id="back-to-dashboard-calendar">`
- Navigation:
  - Back to dashboard goes to `/dashboard`

### 8. article_analytics.html
- Container element: `<div id="analytics-page">`
- Elements:
  - Analytics overview: `<div id="analytics-overview">`
  - Total views: `<span id="analytics-total-views">`
  - Unique visitors: `<span id="analytics-unique-visitors">`
  - Back to Article button: `<button id="back-to-article-analytics">`
- Navigation:
  - Back to article edit or view page `/article/<article_id>/edit` (implied)

---

## Section 3: Data File Schemas

### 1. users.txt
- Format: `username|email|fullname|created_date`
- Fields:
  1. username (str): Unique user identifier
  2. email (str): User email address
  3. fullname (str): Full name of user
  4. created_date (date, YYYY-MM-DD): Account creation date
- Example rows:
```
john|john@example.com|John Doe|2024-01-15
alice|alice@example.com|Alice Smith|2024-01-16
bob|bob@example.com|Bob Johnson|2024-01-17
admin|admin@example.com|Admin User|2024-01-10
```

### 2. articles.txt
- Format: `article_id|title|author|category|status|tags|featured_image|meta_description|created_date|publish_date`
- Fields:
  1. article_id (int): Unique article identifier
  2. title (str): Article title
  3. author (str): Username of author
  4. category (enum): One of {news, blog, tutorial, announcement, press_release}
  5. status (enum): One of {draft, pending_review, under_review, approved, published, rejected, archived}
  6. tags (str): Comma-separated list of tags
  7. featured_image (str): URL or path to image, nullable
  8. meta_description (str): Short description
  9. created_date (date, YYYY-MM-DD): Article creation date
  10. publish_date (datetime, YYYY-MM-DD HH:MM:SS), nullable for unpublished
- Example rows:
```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
```

### 3. article_versions.txt
- Format: `version_id|article_id|version_number|content|author|created_date|change_summary`
- Fields:
  1. version_id (int): Unique version identifier
  2. article_id (int): Article identifier
  3. version_number (int): Sequence number
  4. content (str): Version content text
  5. author (str): Username who created version
  6. created_date (datetime, YYYY-MM-DD HH:MM:SS)
  7. change_summary (str): Description of changes
- Example rows:
```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
```

### 4. approvals.txt
- Format: `approval_id|article_id|version_id|approver|status|comments|timestamp`
- Fields:
  1. approval_id (int): Unique approval record ID
  2. article_id (int)
  3. version_id (int)
  4. approver (str): Username of approver
  5. status (enum): One of {approved, rejected, revision_requested}
  6. comments (str): Approval comments
  7. timestamp (datetime, YYYY-MM-DD HH:MM:SS)
- Example rows:
```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
```

### 5. workflow_stages.txt
- Format: `stage_id|category|stage_name|stage_order|is_required`
- Fields:
  1. stage_id (int)
  2. category (enum): Article category
  3. stage_name (str): Name of workflow stage
  4. stage_order (int): Order in workflow
  5. is_required (enum): yes/no
- Example rows:
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
  1. comment_id (int): Unique comment ID
  2. article_id (int)
  3. version_id (int)
  4. user (str): Username making comment
  5. comment_text (str): Text of comment
  6. timestamp (datetime, YYYY-MM-DD HH:MM:SS)
- Example rows:
```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
```

### 7. analytics.txt
- Format: `analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares`
- Fields:
  1. analytics_id (int): Unique analytics record ID
  2. article_id (int)
  3. date (date, YYYY-MM-DD): Date of record
  4. views (int): Number of views
  5. unique_visitors (int): Number of unique visitors
  6. avg_time_seconds (int): Average time spent in seconds
  7. shares (int): Number of shares
- Example rows:
```
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
```
