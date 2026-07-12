# ContentPublishingHub Design Specification

---

## Section 1: Flask Routes Specification

| Route Pattern                    | HTTP Method(s) | Function Name             | Template Rendered        | Context Variables Passed to Template                     |
|--------------------------------|----------------|---------------------------|--------------------------|----------------------------------------------------------|
| `/dashboard`                   | GET            | dashboard                 | dashboard.html           | `username` (str): Current user's username                |
| `/article/create`              | GET, POST      | create_article            | create_article.html      | GET: none; POST: validation errors (dict) if any         |
| `/article/<article_id>/edit`   | GET, POST      | edit_article              | edit_article.html        | `article_id` (int), `article` (dict with article data), `validation_errors` (POST only, dict) |
| `/article/<article_id>/versions`| GET           | article_version_history    | version_history.html     | `article_id` (int), `versions` (list of dict), `selected_version_comparison` (optional, dict) |
| `/articles/mine`               | GET            | my_articles               | my_articles.html         | `username` (str), `articles` (list of dict), `filter_status` (str) |
| `/articles/published`          | GET            | published_articles        | published_articles.html  | `articles` (list of dict), `filter_category` (str), `sort_option` (str) |
| `/calendar`                   | GET, POST      | content_calendar           | content_calendar.html    | GET: `schedule_data` (list/dict), POST: result status or errors |
| `/article/<article_id>/analytics` | GET         | article_analytics          | article_analytics.html   | `article_id` (int), `analytics` (dict of engagement metrics) |

### Route Details:

1. **Dashboard** (`/dashboard`, GET)
   - Renders `dashboard.html`
   - Context:
     - `username`: string, logged-in user's username
     - Additional context such as quick stats and recent activity feed data (can be extracted from server side)

2. **Create Article** (`/article/create`, GET, POST)
   - GET: Display form
   - POST: Process new article creation; on failure, return validation errors
   - Context (POST): validation errors

3. **Edit Article** (`/article/<article_id>/edit`, GET, POST)
   - GET: Load article content and metadata
   - POST: Save new version, validate inputs
   - Context:
     - `article_id`: int
     - `article`: dict with article fields
     - `validation_errors` on POST failure

4. **Article Version History** (`/article/<article_id>/versions`, GET)
   - List all versions of article
   - Context:
     - `article_id`: int
     - `versions`: list of version dicts (version_id, version_number, content, author, created_date, change_summary)
     - `selected_version_comparison` (optional): dict comparing two versions

5. **My Articles** (`/articles/mine`, GET)
   - List articles by current user
   - Filter by status via dropdown
   - Context:
     - `username`: string
     - `articles`: list of dicts with article info
     - `filter_status`: string representing current filter

6. **Published Articles** (`/articles/published`, GET)
   - Displays public articles
   - Supports category filters and sorting
   - Context:
     - `articles`: list of dicts representing published articles
     - `filter_category`: string
     - `sort_option`: string

7. **Content Calendar** (`/calendar`, GET, POST)
   - GET: Show scheduled publications with calendar view
   - POST: Schedule new publications or update
   - Context:
     - `schedule_data`: structured data for calendar grid

8. **Article Analytics** (`/article/<article_id>/analytics`, GET)
   - Show engagement metrics
   - Context:
     - `article_id`: int
     - `analytics`: dict or structured data covering total views, unique visitors, avg time, shares

---

## Section 2: HTML Template Structure

### 1. dashboard.html
- Page container: `<div id="dashboard-page">`
- Welcome message (username displayed): `<span id="welcome-message">`
- Quick stats section: `<section id="quick-stats">`
- Create Article button: `<button id="create-article-button">`
- Recent activity feed container: `<div id="recent-activity">`

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
- Versions list container: `<ul id="versions-list">` (each version as `<li>`)
- Version comparison section: `<div id="version-comparison">`
- Restore button for a selected version: `<button id="restore-version-1">` (ID ends with version number, e.g., restore-version-1)
- Back to Edit button: `<button id="back-to-edit-history">`

### 5. my_articles.html
- Page container: `<div id="my-articles-page">`
- Filter by status dropdown: `<select id="filter-article-status">`
- Articles table: `<table id="articles-table">`
- Create New Article button: `<button id="create-new-article">`
- Back to Dashboard button: `<button id="back-to-dashboard">`

### 6. published_articles.html
- Page container: `<div id="published-articles-page">`
- Filter by category dropdown: `<select id="filter-published-category">`
- Articles grid container: `<div id="published-articles-grid">`
- Sort by dropdown: `<select id="sort-published">`
- Back to Dashboard button: `<button id="back-to-dashboard-published">`

### 7. content_calendar.html
- Page container: `<div id="calendar-page">`
- Calendar view selector: `<select id="calendar-view">`
- Calendar grid container: `<div id="calendar-grid">`
- Schedule button: `<button id="schedule-button">`
- Back to Dashboard button: `<button id="back-to-dashboard-calendar">`

### 8. article_analytics.html
- Page container: `<div id="analytics-page">`
- Analytics overview section: `<section id="analytics-overview">`
- Total views display: `<span id="analytics-total-views">`
- Unique visitors display: `<span id="analytics-unique-visitors">`
- Back to Article button: `<button id="back-to-article-analytics">`


---

## Section 3: Data File Schemas

### 1. users.txt
- Field order (pipe-delimited): username|email|fullname|created_date
- Field description:
  - `username` (str): unique user identifier
  - `email` (str): user email address
  - `fullname` (str): user's full name
  - `created_date` (date, `YYYY-MM-DD`): date user was created
- Example rows:
```
john|john@example.com|John Doe|2024-01-15
alice|alice@example.com|Alice Smith|2024-01-16
bob|bob@example.com|Bob Johnson|2024-01-17
admin|admin@example.com|Admin User|2024-01-10
```

### 2. articles.txt
- Field order: article_id|title|author|category|status|tags|featured_image|meta_description|created_date|publish_date
- Fields:
  - `article_id` (int): unique article identifier
  - `title` (str): article title
  - `author` (str): username of author
  - `category` (enum): one of [news, blog, tutorial, announcement, press_release]
  - `status` (enum): one of [draft, pending_review, under_review, approved, published, rejected, archived]
  - `tags` (str): comma-separated tags
  - `featured_image` (str): URL path or empty string if none
  - `meta_description` (str): short description
  - `created_date` (date, `YYYY-MM-DD`)
  - `publish_date` (datetime, `YYYY-MM-DD HH:mm:ss`) or empty if unpublished
- Example:
```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
```

### 3. article_versions.txt
- Field order: version_id|article_id|version_number|content|author|created_date|change_summary
- Fields:
  - `version_id` (int): unique version record id
  - `article_id` (int): related article id
  - `version_number` (int): version number
  - `content` (str): full article content
  - `author` (str): username of content author
  - `created_date` (datetime, `YYYY-MM-DD HH:mm:ss`)
  - `change_summary` (str): short summary of changes
- Example:
```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
```

### 4. approvals.txt
- Field order: approval_id|article_id|version_id|approver|status|comments|timestamp
- Fields:
  - `approval_id` (int): unique approval record id
  - `article_id` (int): related article id
  - `version_id` (int): related version id
  - `approver` (str): username who approved/rejected
  - `status` (enum): one of [approved, rejected, revision_requested]
  - `comments` (str): approver comments
  - `timestamp` (datetime, `YYYY-MM-DD HH:mm:ss`)
- Example:
```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
```

### 5. workflow_stages.txt
- Field order: stage_id|category|stage_name|stage_order|is_required
- Fields:
  - `stage_id` (int): unique stage id
  - `category` (enum): one of article categories [tutorial, news, announcement, ...]
  - `stage_name` (str): name of workflow stage
  - `stage_order` (int): order of stage in workflow
  - `is_required` (str): "yes" or "no" indicating if stage is mandatory
- Example:
```
1|tutorial|Editor Review|1|yes
2|tutorial|Publisher Approval|2|yes
3|news|Editor Review|1|yes
4|announcement|Editor Review|1|yes
5|announcement|Publisher Approval|2|yes
```

### 6. comments.txt
- Field order: comment_id|article_id|version_id|user|comment_text|timestamp
- Fields:
  - `comment_id` (int): unique comment id
  - `article_id` (int): related article id
  - `version_id` (int): related version id
  - `user` (str): username who wrote comment
  - `comment_text` (str): comment content
  - `timestamp` (datetime, `YYYY-MM-DD HH:mm:ss`)
- Example:
```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
```

### 7. analytics.txt
- Field order: analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares
- Fields:
  - `analytics_id` (int): unique analytics record id
  - `article_id` (int): referenced article
  - `date` (date, `YYYY-MM-DD`): analytics date
  - `views` (int): number of views on that date
  - `unique_visitors` (int): number of distinct visitors
  - `avg_time_seconds` (int): average time spent in seconds
  - `shares` (int): number of shares
- Example:
```
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
```

---

This design specification provides the necessary Flask routes, HTML element IDs for templates, and file data schemas enabling independent backend and frontend development.
