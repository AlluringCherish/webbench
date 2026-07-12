# ContentPublishingHub Design Specification

---

## Section 1: Flask Routes Specification

| Route Pattern                    | HTTP Methods | Function Name               | Template Rendered       | Context Variables (name : type / description)                               |
|---------------------------------|--------------|----------------------------|-------------------------|----------------------------------------------------------------------------|
| /dashboard                      | GET          | dashboard                  | dashboard.html          | username: str (current logged-in user)
  quick_stats: dict (stat name to value)
  recent_activity: list of dict {activity_text: str, timestamp: str}
|
| /article/create                 | GET, POST    | create_article             | create_article.html     | (GET) No inputs
  (POST) form inputs, on success redirect elsewhere or re-render with errors
|
| /article/<int:article_id>/edit | GET, POST    | edit_article               | edit_article.html       | article_id: int
  article_title: str
  article_content: str
  (POST) form inputs for saving new version
|
| /article/<int:article_id>/versions | GET      | article_version_history    | version_history.html    | article_id: int
  versions_list: list of dict {version_id: int, version_number: int, author: str, created_date: str, change_summary: str}
  comparison_data: dict (optional, for comparing versions)
|
| /articles/mine                 | GET          | my_articles                | my_articles.html        | articles: list of dict {article_id: int, title: str, status: str, category: str, publish_date: str}
  filter_status: str (current selected filter)
|
| /articles/published            | GET          | published_articles         | published_articles.html | articles: list of dict {article_id: int, title: str, category: str, publish_date: str, featured_image: str}
  filter_category: str
  sort_by: str
|
| /calendar                     | GET          | content_calendar           | content_calendar.html   | calendar_view: str (e.g., month, week, day)
  scheduled_articles: list of dict {article_id: int, title: str, publish_date: str}
|
| /article/<int:article_id>/analytics | GET      | article_analytics          | article_analytics.html  | article_id: int
  analytics_overview: dict {total_views: int, unique_visitors: int, average_time_seconds: int, shares: int}
|
---

## Section 2: HTML Template Structure

### 1. dashboard.html
- Page container: `<div id="dashboard-page">`
- Welcome message: `<span id="welcome-message">` displays username
- Quick stats section: `<section id="quick-stats">` shows summarized metrics
- Create Article button: `<button id="create-article-button">` navigates to /article/create
- Recent activity feed: `<div id="recent-activity">` lists recent user or system activities

### 2. create_article.html
- Page container: `<div id="create-article-page">`
- Article title input: `<input id="article-title" type="text">`
- Content editor textarea: `<textarea id="article-content"></textarea>`
- Save as Draft button: `<button id="save-draft-button">`
- Cancel button: `<button id="cancel-button">`

### 3. edit_article.html
- Page container: `<div id="edit-article-page">`
- Article title input: `<input id="edit-article-title" type="text">`
- Content editor textarea: `<textarea id="edit-article-content"></textarea>`
- Save New Version button: `<button id="save-version-button">`
- Cancel button: `<button id="cancel-edit">`

### 4. version_history.html
- Page container: `<div id="version-history-page">`
- Versions list: `<ul id="versions-list">` each item shows version details
- Version comparison section: `<section id="version-comparison">` displays side-by-side diff
- Restore button: `<button id="restore-version-1">` (assumes dynamic id for each version button)
- Back to Edit button: `<button id="back-to-edit-history">` navigates back to edit page

### 5. my_articles.html
- Page container: `<div id="my-articles-page">`
- Filter by status dropdown: `<select id="filter-article-status">` for statuses
- Articles table: `<table id="articles-table">` columns: Title, Status, Category, Publish Date
- Create New Article button: `<button id="create-new-article">`
- Back to Dashboard button: `<button id="back-to-dashboard">`

### 6. published_articles.html
- Page container: `<div id="published-articles-page">`
- Filter by category dropdown: `<select id="filter-published-category">`
- Articles grid: `<div id="published-articles-grid">` showing article thumbnails
- Sort by dropdown: `<select id="sort-published">`
- Back to Dashboard button: `<button id="back-to-dashboard-published">`

### 7. content_calendar.html
- Page container: `<div id="calendar-page">`
- Calendar view selector: `<select id="calendar-view">` (month, week, day)
- Calendar grid: `<div id="calendar-grid">` displays scheduled content
- Schedule button: `<button id="schedule-button">`
- Back to Dashboard button: `<button id="back-to-dashboard-calendar">`

### 8. article_analytics.html
- Page container: `<div id="analytics-page">`
- Analytics overview: `<section id="analytics-overview">`
- Total views: `<span id="analytics-total-views">`
- Unique visitors: `<span id="analytics-unique-visitors">`
- Back to Article button: `<button id="back-to-article-analytics">`

---

## Section 3: Data File Schemas

### 1. users.txt
- Format: `username|email|fullname|created_date`
- Fields:
  - username: str (unique user identifier)
  - email: str (user email)
  - fullname: str (user's full name)
  - created_date: str (ISO date `YYYY-MM-DD` user account created)
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
  - article_id: int (unique article identifier)
  - title: str (article title)
  - author: str (username of creator)
  - category: str (one of: news, blog, tutorial, announcement, press_release)
  - status: str (one of: draft, pending_review, under_review, approved, published, rejected, archived)
  - tags: str (comma-separated keywords)
  - featured_image: str (path URL or empty string)
  - meta_description: str (short summary)
  - created_date: str (ISO date `YYYY-MM-DD` created)
  - publish_date: str (ISO datetime `YYYY-MM-DD HH:MM:SS` or empty if not published)
- Example:
  ```
  1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
  2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
  3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
  ```

### 3. article_versions.txt
- Format: `version_id|article_id|version_number|content|author|created_date|change_summary`
- Fields:
  - version_id: int (unique version identifier)
  - article_id: int (link to article)
  - version_number: int (incremental version number)
  - content: str (full article text content)
  - author: str (username of editor)
  - created_date: str (ISO datetime `YYYY-MM-DD HH:MM:SS` of version save)
  - change_summary: str (short description of changes)
- Example:
  ```
  1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
  2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
  3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
  ```

### 4. approvals.txt
- Format: `approval_id|article_id|version_id|approver|status|comments|timestamp`
- Fields:
  - approval_id: int (unique approval record)
  - article_id: int (article linked)
  - version_id: int (version linked)
  - approver: str (username who approved)
  - status: str (one of: approved, rejected, revision_requested)
  - comments: str (remarks by approver)
  - timestamp: str (ISO datetime `YYYY-MM-DD HH:MM:SS`)
- Example:
  ```
  1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
  2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
  3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
  ```

### 5. workflow_stages.txt
- Format: `stage_id|category|stage_name|stage_order|is_required`
- Fields:
  - stage_id: int (unique workflow stage ID)
  - category: str (article category this stage applies to)
  - stage_name: str (name of workflow stage)
  - stage_order: int (ordering sequence)
  - is_required: str ("yes" or "no" indicating if stage is mandatory)
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
  - comment_id: int (unique comment ID)
  - article_id: int (article linked)
  - version_id: int (version linked)
  - user: str (username who made comment)
  - comment_text: str (comment content)
  - timestamp: str (ISO datetime `YYYY-MM-DD HH:MM:SS`)
- Example:
  ```
  1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
  2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
  3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
  ```

### 7. analytics.txt
- Format: `analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares`
- Fields:
  - analytics_id: int (unique analytics record ID)
  - article_id: int (article linked)
  - date: str (ISO date `YYYY-MM-DD`)
  - views: int (total page views on date)
  - unique_visitors: int (unique visitors count on date)
  - avg_time_seconds: int (average time spent on article in seconds)
  - shares: int (number of article shares on date)
- Example:
  ```
  1|1|2024-01-22|150|120|245|12
  2|1|2024-01-23|230|180|210|18
  3|1|2024-01-24|180|140|220|15
  4|2|2024-01-25|95|75|180|8
  ```

---

This design specification document fully describes the routes, pages with precise element IDs, and data storage schema for the ContentPublishingHub web application. Backend and frontend teams can independently implement their respective components unambiguously with this spec.
