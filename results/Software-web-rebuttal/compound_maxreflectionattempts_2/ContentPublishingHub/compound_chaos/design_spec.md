# ContentPublishingHub Design Specification

---

## 1. Flask Routes Specification

### Route: `/dashboard`
- HTTP Methods: GET
- Function Name: `dashboard`
- Template Rendered: `dashboard.html`
- Context Variables:
  - `username` (str): Username to display in welcome message
  - `quick_stats` (dict): Dictionary containing various quick stats (e.g. counts of articles in various statuses)
  - `recent_activity` (list of dict): Recent activity feed items with relevant details (e.g. action description, timestamp)

### Route: `/article/create`
- HTTP Methods: GET, POST
- Function Name: `create_article`
- Template Rendered: `create_article.html`
- Context Variables (GET): None required for rendering
- POST expected to handle form submission for article creation

### Route: `/article/<article_id>/edit`
- HTTP Methods: GET, POST
- Function Name: `edit_article`
- Template Rendered: `edit_article.html`
- Context Variables (GET):
  - `article_id` (int or str): Article identifier
  - `title` (str): Current article title
  - `content` (str): Current article content
- POST expected to handle saving new version

### Route: `/article/<article_id>/versions`
- HTTP Methods: GET
- Function Name: `article_version_history`
- Template Rendered: `version_history.html`
- Context Variables:
  - `article_id` (int or str): Article identifier
  - `versions` (list of dict): List of version details including version number, content summary etc.
  - `comparison` (dict): Data to support version comparison view

### Route: `/articles/mine`
- HTTP Methods: GET
- Function Name: `my_articles`
- Template Rendered: `my_articles.html`
- Context Variables:
  - `articles` (list of dict): User's articles filtered as needed
  - `filter_status_options` (list of str): Statuses for dropdown filter

### Route: `/articles/published`
- HTTP Methods: GET
- Function Name: `published_articles`
- Template Rendered: `published_articles.html`
- Context Variables:
  - `articles` (list of dict): Published articles
  - `categories` (list of str): Categories for filter dropdown
  - `sort_options` (list of str): Sorting options for dropdown

### Route: `/calendar`
- HTTP Methods: GET
- Function Name: `content_calendar`
- Template Rendered: `content_calendar.html`
- Context Variables:
  - `calendar_views` (list of str): Available calendar view modes
  - `calendar_events` (list of dict): Scheduled publication items

### Route: `/article/<article_id>/analytics`
- HTTP Methods: GET
- Function Name: `article_analytics`
- Template Rendered: `article_analytics.html`
- Context Variables:
  - `article_id` (int or str): Article identifier
  - `analytics_overview` (dict): Summary data for engagement metrics
  - `total_views` (int): Total views count
  - `unique_visitors` (int): Unique visitor count

---

## 2. HTML Template Structure

### dashboard.html
- Page container: `<div id="dashboard-page">`
- Elements:
  - Welcome message: `<div id="welcome-message">`
  - Quick stats section: `<section id="quick-stats">`
  - Create Article button: `<button id="create-article-button">`
  - Recent activity feed: `<div id="recent-activity">`
- Navigation:
  - Create Article button links to `/article/create`

### create_article.html
- Page container: `<div id="create-article-page">`
- Elements:
  - Article title input: `<input type="text" id="article-title">`
  - Content editor: `<textarea id="article-content"></textarea>`
  - Save as Draft button: `<button id="save-draft-button">`
  - Cancel button: `<button id="cancel-button">`
- Navigation:
  - Cancel button redirects back (likely to dashboard or previous page)

### edit_article.html
- Page container: `<div id="edit-article-page">`
- Elements:
  - Article title input: `<input type="text" id="edit-article-title">`
  - Content editor: `<textarea id="edit-article-content"></textarea>`
  - Save New Version button: `<button id="save-version-button">`
  - Cancel button: `<button id="cancel-edit">`
- Navigation:
  - Cancel button returns to previous or appropriate page

### version_history.html
- Page container: `<div id="version-history-page">`
- Elements:
  - Versions list: `<ul id="versions-list">` or appropriate list container
  - Version comparison section: `<section id="version-comparison">`
  - Restore button: `<button id="restore-version-1">`
  - Back to Edit button: `<button id="back-to-edit-history">`
- Navigation:
  - Back to Edit returns to `/article/<article_id>/edit`

### my_articles.html
- Page container: `<div id="my-articles-page">`
- Elements:
  - Filter by status dropdown: `<select id="filter-article-status">`
  - Articles table: `<table id="articles-table">`
  - Create New Article button: `<button id="create-new-article">`
  - Back to Dashboard button: `<button id="back-to-dashboard">`
- Navigation:
  - Create New Article links to `/article/create`
  - Back to Dashboard links to `/dashboard`

### published_articles.html
- Page container: `<div id="published-articles-page">`
- Elements:
  - Filter by category dropdown: `<select id="filter-published-category">`
  - Articles grid: `<div id="published-articles-grid">`
  - Sort by dropdown: `<select id="sort-published">`
  - Back to Dashboard button: `<button id="back-to-dashboard-published">`
- Navigation:
  - Back to Dashboard links to `/dashboard`

### content_calendar.html
- Page container: `<div id="calendar-page">`
- Elements:
  - Calendar view selector: `<select id="calendar-view">`
  - Calendar grid: `<div id="calendar-grid">`
  - Schedule button: `<button id="schedule-button">`
  - Back to Dashboard button: `<button id="back-to-dashboard-calendar">`
- Navigation:
  - Back to Dashboard links to `/dashboard`

### article_analytics.html
- Page container: `<div id="analytics-page">`
- Elements:
  - Analytics overview: `<section id="analytics-overview">`
  - Total views display: `<span id="analytics-total-views">`
  - Unique visitors display: `<span id="analytics-unique-visitors">`
  - Back to Article button: `<button id="back-to-article-analytics">`
- Navigation:
  - Back to Article returns to article editing or detail view `/article/<article_id>/edit` or similar

---

## 3. Data File Schemas

### users.txt
- Format: `username|email|fullname|created_date`
- Fields:
  1. `username` (str): Unique user identifier
  2. `email` (str): User email address
  3. `fullname` (str): User full name
  4. `created_date` (date `YYYY-MM-DD`): Account creation date
- Example rows:
  ```
  john|john@example.com|John Doe|2024-01-15
  alice|alice@example.com|Alice Smith|2024-01-16
  bob|bob@example.com|Bob Johnson|2024-01-17
  admin|admin@example.com|Admin User|2024-01-10
  ```

### articles.txt
- Format: `article_id|title|author|category|status|tags|featured_image|meta_description|created_date|publish_date`
- Fields:
  1. `article_id` (int): Unique article identifier
  2. `title` (str): Article title
  3. `author` (str): Username of article author
  4. `category` (enum): One of `news`, `blog`, `tutorial`, `announcement`, `press_release`
  5. `status` (enum): One of `draft`, `pending_review`, `under_review`, `approved`, `published`, `rejected`, `archived`
  6. `tags` (str): Comma-separated list of tags
  7. `featured_image` (str): Path or URL to featured image (may be empty)
  8. `meta_description` (str): Short meta description of article
  9. `created_date` (date `YYYY-MM-DD`): Creation date
  10. `publish_date` (datetime `YYYY-MM-DD HH:MM:SS` or empty): Publish date and time
- Example rows:
  ```
  1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
  2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
  3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
  ```

### article_versions.txt
- Format: `version_id|article_id|version_number|content|author|created_date|change_summary`
- Fields:
  1. `version_id` (int): Unique version identifier
  2. `article_id` (int): Related article ID
  3. `version_number` (int): The version sequence number
  4. `content` (str): Article content text
  5. `author` (str): Username who authored this version
  6. `created_date` (datetime `YYYY-MM-DD HH:MM:SS`): Version creation timestamp
  7. `change_summary` (str): Short summary of changes made
- Example rows:
  ```
  1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
  2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
  3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
  ```

### approvals.txt
- Format: `approval_id|article_id|version_id|approver|status|comments|timestamp`
- Fields:
  1. `approval_id` (int): Unique approval record ID
  2. `article_id` (int): Article ID this approval concerns
  3. `version_id` (int): Article version ID approved or rejected
  4. `approver` (str): Username of approver
  5. `status` (enum): One of `approved`, `rejected`, `revision_requested`
  6. `comments` (str): Approval comments
  7. `timestamp` (datetime `YYYY-MM-DD HH:MM:SS`): When approval was given
- Example rows:
  ```
  1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
  2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
  3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
  ```

### workflow_stages.txt
- Format: `stage_id|category|stage_name|stage_order|is_required`
- Fields:
  1. `stage_id` (int): Unique stage identifier
  2. `category` (str): Related article category
  3. `stage_name` (str): Name of workflow stage
  4. `stage_order` (int): Order in workflow
  5. `is_required` (enum): Either `yes` or `no` indicating if stage is mandatory
- Example rows:
  ```
  1|tutorial|Editor Review|1|yes
  2|tutorial|Publisher Approval|2|yes
  3|news|Editor Review|1|yes
  4|announcement|Editor Review|1|yes
  5|announcement|Publisher Approval|2|yes
  ```

### comments.txt
- Format: `comment_id|article_id|version_id|user|comment_text|timestamp`
- Fields:
  1. `comment_id` (int): Unique comment identifier
  2. `article_id` (int): Related article ID
  3. `version_id` (int): Version of article commented on
  4. `user` (str): Username who made comment
  5. `comment_text` (str): Text content of comment
  6. `timestamp` (datetime `YYYY-MM-DD HH:MM:SS`): When comment was made
- Example rows:
  ```
  1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
  2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
  3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
  ```

### analytics.txt
- Format: `analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares`
- Fields:
  1. `analytics_id` (int): Unique analytics record ID
  2. `article_id` (int): Article ID related to analytics
  3. `date` (date `YYYY-MM-DD`): Date of the analytics record
  4. `views` (int): Number of views
  5. `unique_visitors` (int): Unique visitors count
  6. `avg_time_seconds` (int): Average time spent in seconds
  7. `shares` (int): Number of shares
- Example rows:
  ```
  1|1|2024-01-22|150|120|245|12
  2|1|2024-01-23|230|180|210|18
  3|1|2024-01-24|180|140|220|15
  4|2|2024-01-25|95|75|180|8
  ```

---

**End of Design Specification Document**
