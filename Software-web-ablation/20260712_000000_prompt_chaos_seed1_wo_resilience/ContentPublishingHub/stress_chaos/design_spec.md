# ContentPublishingHub Design Specification

---

## Section 1: Flask Routes Specification

1. `/dashboard`
   - Methods: GET
   - Function Name: `dashboard`
   - Template: `dashboard.html`
   - Context Variables:
     - `username`: str (logged-in user's username to display in welcome message)
     - `quick_stats`: dict (key metrics summary for display)
     - `recent_activity`: list of dict (recent user and system activities with relevant info)

2. `/article/create`
   - Methods: GET, POST
   - Function Name: `create_article`
   - Template: `create_article.html`
   - Context Variables (GET): None (blank form)
   - POST expects form data: title, content
   - On GET: Render create article form

3. `/article/<article_id>/edit`
   - Methods: GET, POST
   - Function Name: `edit_article`
   - Template: `edit_article.html`
   - Context Variables (GET):
     - `article_id`: int (from URL path)
     - `title`: str (existing article title)
     - `content`: str (latest content of article)
   - POST expects updated title and content

4. `/article/<article_id>/versions`
   - Methods: GET
   - Function Name: `article_version_history`
   - Template: `version_history.html`
   - Context Variables:
     - `article_id`: int
     - `versions`: list of dict with fields: version_id, version_number, created_date, change_summary
     - `version_comparison`: dict (details of compared versions for display)

5. `/articles/mine`
   - Methods: GET
   - Function Name: `my_articles`
   - Template: `my_articles.html`
   - Context Variables:
     - `articles`: list of dict (user's articles with fields matching those in articles.txt)
     - `status_filter_options`: list of str (all status values)
     - `selected_status_filter`: str

6. `/articles/published`
   - Methods: GET
   - Function Name: `published_articles`
   - Template: `published_articles.html`
   - Context Variables:
     - `articles`: list of dict (published articles with fields matching articles.txt)
     - `category_filter_options`: list of str
     - `selected_category`: str
     - `sort_options`: list of str (possible sort fields)
     - `selected_sort`: str

7. `/calendar`
   - Methods: GET
   - Function Name: `content_calendar`
   - Template: `content_calendar.html`
   - Context Variables:
     - `calendar_views`: list of str (e.g. day, week, month)
     - `selected_view`: str
     - `schedule_items`: list of dict (scheduled publications with date and article info)

8. `/article/<article_id>/analytics`
   - Methods: GET
   - Function Name: `article_analytics`
   - Template: `article_analytics.html`
   - Context Variables:
     - `article_id`: int
     - `analytics_overview`: dict with keys: total_views (int), unique_visitors (int), average_time_seconds (float), shares (int)

---

## Section 2: HTML Template Structure

### 1. dashboard.html
- Page container: `<div id="dashboard-page">`
- Elements:
  - Welcome message: `<div id="welcome-message">` (Displays username)
  - Quick stats section: `<section id="quick-stats">` (summary stats)
  - Create Article button: `<button id="create-article-button">` (navigate to `/article/create`)
  - Recent activity feed: `<div id="recent-activity">` (list of recent activities)

### 2. create_article.html
- Page container: `<div id="create-article-page">`
- Elements:
  - Article title input: `<input type="text" id="article-title">`
  - Content editor: `<textarea id="article-content"></textarea>`
  - Save as Draft button: `<button id="save-draft-button">`
  - Cancel button: `<button id="cancel-button">` (typically routes back or resets form)

### 3. edit_article.html
- Page container: `<div id="edit-article-page">`
- Elements:
  - Article title input: `<input type="text" id="edit-article-title">`
  - Content editor: `<textarea id="edit-article-content"></textarea>`
  - Save New Version button: `<button id="save-version-button">`
  - Cancel button: `<button id="cancel-edit">`

### 4. version_history.html
- Page container: `<div id="version-history-page">`
- Elements:
  - Versions list: `<ul id="versions-list">` (list each version as a clickable item)
  - Version comparison section: `<div id="version-comparison">` (diff or side-by-side content comparison)
  - Restore button: `<button id="restore-version-1">` (ID uses version number or specific version ID, here example is `1`)
  - Back to Edit button: `<button id="back-to-edit-history">`

### 5. my_articles.html
- Page container: `<div id="my-articles-page">`
- Elements:
  - Filter by status dropdown: `<select id="filter-article-status">` (options corresponding to statuses)
  - Articles table: `<table id="articles-table">` (columns: article_id, title, status, publish_date, etc.)
  - Create New Article button: `<button id="create-new-article">`
  - Back to Dashboard button: `<button id="back-to-dashboard">`

### 6. published_articles.html
- Page container: `<div id="published-articles-page">`
- Elements:
  - Filter by category dropdown: `<select id="filter-published-category">`
  - Articles grid: `<div id="published-articles-grid">` (grid layout for articles display)
  - Sort by dropdown: `<select id="sort-published">`
  - Back to Dashboard button: `<button id="back-to-dashboard-published">`

### 7. content_calendar.html
- Page container: `<div id="calendar-page">`
- Elements:
  - Calendar view selector: `<select id="calendar-view">` (day, week, month views)
  - Calendar grid: `<div id="calendar-grid">` (visual calendar interface)
  - Schedule button: `<button id="schedule-button">`
  - Back to Dashboard button: `<button id="back-to-dashboard-calendar">`

### 8. article_analytics.html
- Page container: `<div id="analytics-page">`
- Elements:
  - Analytics overview: `<section id="analytics-overview">`
  - Total views display: `<div id="analytics-total-views">`
  - Unique visitors display: `<div id="analytics-unique-visitors">`
  - Back to Article button: `<button id="back-to-article-analytics">`

---

## Section 3: Data File Schemas

### 1. users.txt
- Delimiter: pipe (`|`)
- Fields Order and Description:
  1. `username`: str - unique user identifier
  2. `email`: str - user email address
  3. `fullname`: str - full name of the user
  4. `created_date`: str (YYYY-MM-DD) - date user account created
- Example Rows:
  ```
john|john@example.com|John Doe|2024-01-15
alice|alice@example.com|Alice Smith|2024-01-16
bob|bob@example.com|Bob Johnson|2024-01-17
admin|admin@example.com|Admin User|2024-01-10
```

### 2. articles.txt
- Delimiter: pipe (`|`)
- Fields Order and Description:
  1. `article_id`: int - unique ID
  2. `title`: str - article title
  3. `author`: str - username of the article author
  4. `category`: str - one of [news, blog, tutorial, announcement, press_release]
  5. `status`: str - one of [draft, pending_review, under_review, approved, published, rejected, archived]
  6. `tags`: str - comma-separated tags
  7. `featured_image`: str - file path or empty string if none
  8. `meta_description`: str - brief description
  9. `created_date`: str (YYYY-MM-DD)
  10. `publish_date`: str (YYYY-MM-DD HH:MM:SS) or empty if not published
- Example Rows:
  ```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
```

### 3. article_versions.txt
- Delimiter: pipe (`|`)
- Fields Order and Description:
  1. `version_id`: int - unique version identifier
  2. `article_id`: int - article this version belongs to
  3. `version_number`: int - sequential version number
  4. `content`: str - full text content
  5. `author`: str - username who created the version
  6. `created_date`: str (YYYY-MM-DD HH:MM:SS) - creation timestamp
  7. `change_summary`: str - brief summary of the changes
- Example Rows:
  ```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
```

### 4. approvals.txt
- Delimiter: pipe (`|`)
- Fields Order and Description:
  1. `approval_id`: int - unique approval record
  2. `article_id`: int
  3. `version_id`: int
  4. `approver`: str - username who reviewed
  5. `status`: str - [approved, rejected, revision_requested]
  6. `comments`: str - textual comments
  7. `timestamp`: str (YYYY-MM-DD HH:MM:SS)
- Example Rows:
  ```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
```

### 5. workflow_stages.txt
- Delimiter: pipe (`|`)
- Fields Order and Description:
  1. `stage_id`: int - unique workflow stage ID
  2. `category`: str - article category applicable
  3. `stage_name`: str - name of the workflow stage
  4. `stage_order`: int - execution order of the stage
  5. `is_required`: str - 'yes' or 'no' indicating mandatory stage
- Example Rows:
  ```
1|tutorial|Editor Review|1|yes
2|tutorial|Publisher Approval|2|yes
3|news|Editor Review|1|yes
4|announcement|Editor Review|1|yes
5|announcement|Publisher Approval|2|yes
```

### 6. comments.txt
- Delimiter: pipe (`|`)
- Fields Order and Description:
  1. `comment_id`: int - unique comment record
  2. `article_id`: int
  3. `version_id`: int
  4. `user`: str - username of commenter
  5. `comment_text`: str
  6. `timestamp`: str (YYYY-MM-DD HH:MM:SS)
- Example Rows:
  ```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
```

### 7. analytics.txt
- Delimiter: pipe (`|`)
- Fields Order and Description:
  1. `analytics_id`: int - unique analytics record
  2. `article_id`: int
  3. `date`: str (YYYY-MM-DD)
  4. `views`: int - total views count
  5. `unique_visitors`: int
  6. `avg_time_seconds`: int - average time spent on article
  7. `shares`: int - social shares count
- Example Rows:
  ```
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
```

---

This design specification enables backend and frontend developers to work independently with clear contract of routes, data structures, and UI element IDs.
