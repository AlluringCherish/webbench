# ContentPublishingHub Design Specification

---

## Section 1: Flask Routes Specification

| Route Pattern                    | HTTP Method(s) | Function Name             | Template Rendered        | Context Variables Passed to Template                     |
|--------------------------------|----------------|---------------------------|--------------------------|----------------------------------------------------------|
| `/dashboard`                   | GET            | dashboard                 | dashboard.html           | `username` (str): Current user's username                |
| `/article/create`              | GET, POST      | create_article            | create_article.html      | GET: none; POST: validation errors (if any)              |
| `/article/<article_id>/edit`   | GET, POST      | edit_article              | edit_article.html        | GET: `article` (dict with article data), `version_history` (list of dicts);
POST: validation errors (if any)                          |
| `/article/<article_id>/versions`| GET          | version_history           | version_history.html     | `article_id` (int/str), `versions` (list of dicts), `comparison_data` (optional) |
| `/articles/mine`               | GET            | my_articles               | my_articles.html         | `articles` (list of dicts), `filter_status` (str)         |
| `/articles/published`          | GET            | published_articles        | published_articles.html  | `articles` (list of dicts), `filter_category` (str), `sort_order` (str)          |
| `/calendar`                   | GET, POST      | content_calendar          | content_calendar.html    | GET: `schedule_data` (list of dict), `view_selector` (str);
POST: form submission data for scheduling                        |
| `/article/<article_id>/analytics`| GET          | article_analytics         | article_analytics.html   | `article_id` (int/str), `analytics` (dict or list of dicts)                   |

### Detailed Route Descriptions

- **dashboard**
  - URL: `/dashboard`
  - Methods: GET
  - Renders `dashboard.html`
  - Context: `username` (string) for welcome message, quick stats data, recent activity feed data.

- **create_article**
  - URL: `/article/create`
  - Methods: GET (show form), POST (submit new article draft)
  - Renders `create_article.html`
  - Context: No special data on GET; on POST may pass form errors.

- **edit_article**
  - URL: `/article/<article_id>/edit`
  - Methods: GET (load article), POST (submit edits, new version)
  - Renders `edit_article.html`
  - Context variables include full article data and version history for that article.

- **version_history**
  - URL: `/article/<article_id>/versions`
  - Methods: GET
  - Renders `version_history.html`
  - Context: list of all versions of the article, data to support version comparison.

- **my_articles**
  - URL: `/articles/mine`
  - Methods: GET
  - Renders `my_articles.html`
  - Context: list of articles filtered by the current user's ownership; filter status value.

- **published_articles**
  - URL: `/articles/published`
  - Methods: GET
  - Renders `published_articles.html`
  - Context: list of all published articles; filter category and sort order options.

- **content_calendar**
  - URL: `/calendar`
  - Methods: GET (view schedule), POST (to schedule publication)
  - Renders `content_calendar.html`
  - Context: data to render publication schedule, selected calendar view.

- **article_analytics**
  - URL: `/article/<article_id>/analytics`
  - Methods: GET
  - Renders `article_analytics.html`
  - Context: analytics metrics for the specified article.

---

## Section 2: HTML Template Structure

### 1. dashboard.html
- Page container: `<div id="dashboard-page">`
- Elements:
  - Welcome message: `<span id="welcome-message"></span>`
  - Quick stats section: `<section id="quick-stats"></section>`
  - Create Article button: `<button id="create-article-button"></button>`
  - Recent activity feed: `<div id="recent-activity"></div>`

- Navigation:
  - Clicking "Create Article" button navigates to `/article/create`
  - Links or buttons present to go to My Articles, Published Articles, Content Calendar, etc. (not specified but recommended)

### 2. create_article.html
- Page container: `<div id="create-article-page">`
- Elements:
  - Article title input: `<input id="article-title" type="text" />`
  - Content editor textarea: `<textarea id="article-content"></textarea>`
  - Save as Draft button: `<button id="save-draft-button"></button>`
  - Cancel button: `<button id="cancel-button"></button>`

- Navigation:
  - Cancel button returns user to dashboard or previous page

### 3. edit_article.html
- Page container: `<div id="edit-article-page">`
- Elements:
  - Article title input: `<input id="edit-article-title" type="text" />`
  - Content editor textarea: `<textarea id="edit-article-content"></textarea>`
  - Save New Version button: `<button id="save-version-button"></button>`
  - Cancel button: `<button id="cancel-edit"></button>`

### 4. version_history.html
- Page container: `<div id="version-history-page">`
- Elements:
  - Versions list: `<ul id="versions-list"></ul>`
  - Version comparison section: `<div id="version-comparison"></div>`
  - Restore button: `<button id="restore-version-1"></button>` <!-- Note: This ID should be dynamic per version but requires at least one as example -->
  - Back to Edit button: `<button id="back-to-edit-history"></button>`

### 5. my_articles.html
- Page container: `<div id="my-articles-page">`
- Elements:
  - Filter by status dropdown: `<select id="filter-article-status"></select>`
  - Articles table: `<table id="articles-table"></table>`
  - Create New Article button: `<button id="create-new-article"></button>`
  - Back to Dashboard button: `<button id="back-to-dashboard"></button>`

### 6. published_articles.html
- Page container: `<div id="published-articles-page">`
- Elements:
  - Filter by category dropdown: `<select id="filter-published-category"></select>`
  - Articles grid: `<div id="published-articles-grid"></div>`
  - Sort by dropdown: `<select id="sort-published"></select>`
  - Back to Dashboard button: `<button id="back-to-dashboard-published"></button>`

### 7. content_calendar.html
- Page container: `<div id="calendar-page">`
- Elements:
  - Calendar view selector: `<select id="calendar-view"></select>`
  - Calendar grid: `<div id="calendar-grid"></div>`
  - Schedule button: `<button id="schedule-button"></button>`
  - Back to Dashboard button: `<button id="back-to-dashboard-calendar"></button>`

### 8. article_analytics.html
- Page container: `<div id="analytics-page">`
- Elements:
  - Analytics overview: `<section id="analytics-overview"></section>`
  - Total views: `<span id="analytics-total-views"></span>`
  - Unique visitors: `<span id="analytics-unique-visitors"></span>`
  - Back to Article button: `<button id="back-to-article-analytics"></button>`

---

## Section 3: Data File Schemas

Each data file is pipe (`|`) delimited. All timestamps and dates use `YYYY-MM-DD` or `YYYY-MM-DD HH:MM:SS` formats.

### 1. users.txt
- Fields (in order):
  1. username (string) - user login name
  2. email (string) - user's email address
  3. fullname (string) - user's full name
  4. created_date (YYYY-MM-DD) - account creation date

- Example rows:
```
john|john@example.com|John Doe|2024-01-15
alice|alice@example.com|Alice Smith|2024-01-16
bob|bob@example.com|Bob Johnson|2024-01-17
admin|admin@example.com|Admin User|2024-01-10
```

### 2. articles.txt
- Fields (in order):
  1. article_id (int) - unique article identifier
  2. title (string) - article title
  3. author (string) - username of the article author
  4. category (string) - one of [news, blog, tutorial, announcement, press_release]
  5. status (string) - article status, one of [draft, pending_review, under_review, approved, published, rejected, archived]
  6. tags (string) - comma-separated list of tags
  7. featured_image (string) - file path or URL to image, may be empty
  8. meta_description (string) - short description
  9. created_date (YYYY-MM-DD) - article creation date
  10. publish_date (YYYY-MM-DD HH:MM:SS) - scheduled or actual publish datetime, may be empty if unpublished

- Example rows:
```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
```

### 3. article_versions.txt
- Fields (in order):
  1. version_id (int) - unique version identifier
  2. article_id (int) - linked article id
  3. version_number (int) - version number for the article
  4. content (string) - full content of the article version
  5. author (string) - username of editor who created version
  6. created_date (YYYY-MM-DD HH:MM:SS) - time version created
  7. change_summary (string) - one line summary of changes

- Example rows:
```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
```

### 4. approvals.txt
- Fields (in order):
  1. approval_id (int) - unique approval identifier
  2. article_id (int) - article linked to approval
  3. version_id (int) - article version linked
  4. approver (string) - username of approver
  5. status (string) - one of [approved, rejected, revision_requested]
  6. comments (string) - text comments
  7. timestamp (YYYY-MM-DD HH:MM:SS) - time of approval action

- Example rows:
```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
```

### 5. workflow_stages.txt
- Fields (in order):
  1. stage_id (int) - unique workflow stage identifier
  2. category (string) - article category the stage applies to
  3. stage_name (string) - descriptive name of stage
  4. stage_order (int) - numeric order in workflow
  5. is_required (string) - 'yes' or 'no' indicating if stage is mandatory

- Example rows:
```
1|tutorial|Editor Review|1|yes
2|tutorial|Publisher Approval|2|yes
3|news|Editor Review|1|yes
4|announcement|Editor Review|1|yes
5|announcement|Publisher Approval|2|yes
```

### 6. comments.txt
- Fields (in order):
  1. comment_id (int) - unique comment identifier
  2. article_id (int) - linked article
  3. version_id (int) - linked article version
  4. user (string) - username of commenter
  5. comment_text (string) - comment content
  6. timestamp (YYYY-MM-DD HH:MM:SS) - comment time

- Example rows:
```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
```

### 7. analytics.txt
- Fields (in order):
  1. analytics_id (int) - unique analytics record
  2. article_id (int) - linked article
  3. date (YYYY-MM-DD) - date recorded
  4. views (int) - number of views
  5. unique_visitors (int) - number of unique visitors
  6. avg_time_seconds (int) - average time spent in seconds
  7. shares (int) - number of shares on social media

- Example rows:
```
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
```
