# ContentPublishingHub Design Specification

---

## Section 1: Flask Routes Specification

| Route Pattern                      | Methods  | Function Name                  | Template Rendered       | Context Variables                             |
|----------------------------------|----------|-------------------------------|------------------------|-----------------------------------------------|
| `/dashboard`                     | GET      | dashboard                     | dashboard.html         | `username` (str), `quick_stats` (dict), `recent_activity` (list of dicts) |
| `/article/create`                | GET, POST| create_article                | create_article.html    | GET: None; POST: form data validation results and status messages |
| `/article/<int:article_id>/edit`| GET, POST| edit_article                  | edit_article.html      | GET: article (dict including title, content, etc.); POST: form validation messages |
| `/article/<int:article_id>/versions` | GET  | article_version_history        | version_history.html   | `article_id` (int), `versions` (list of dicts), `comparison_data` (optional dict) |
| `/articles/mine`                | GET      | my_articles                   | my_articles.html       | `articles` (list of dicts), `filter_status` (str) |
| `/articles/published`           | GET      | published_articles            | published_articles.html| `articles` (list of dicts), `filter_category` (str), `sort_option` (str) |
| `/calendar`                    | GET      | content_calendar              | content_calendar.html  | `calendar_view` (str), `calendar_events` (list), scheduling info as needed |
| `/article/<int:article_id>/analytics` | GET  | article_analytics             | article_analytics.html | `article_id` (int), `analytics_overview` (dict with totals and metrics) |

---

## Section 2: HTML Template Structure

### 1. dashboard.html
- Page container: `<div id="dashboard-page">`
- Welcome message: `<div id="welcome-message">` displays "Welcome, {username}!"
- Quick stats section: `<section id="quick-stats">`
- Create Article button: `<button id="create-article-button">Create Article</button>`
- Recent activity feed: `<div id="recent-activity">` List recent content actions

### 2. create_article.html
- Page container: `<div id="create-article-page">`
- Article title input: `<input type="text" id="article-title" name="article_title">`
- Content editor textarea: `<textarea id="article-content" name="article_content"></textarea>`
- Save as Draft button: `<button id="save-draft-button">Save as Draft</button>`
- Cancel button: `<button id="cancel-button">Cancel</button>`

### 3. edit_article.html
- Page container: `<div id="edit-article-page">`
- Article title input: `<input type="text" id="edit-article-title" name="article_title">`
- Content editor textarea: `<textarea id="edit-article-content" name="article_content"></textarea>`
- Save New Version button: `<button id="save-version-button">Save New Version</button>`
- Cancel button: `<button id="cancel-edit">Cancel</button>`

### 4. version_history.html
- Page container: `<div id="version-history-page">`
- Versions list: `<ul id="versions-list">` each item representing a version
- Version comparison section: `<div id="version-comparison">` shows differences between versions
- Restore button: `<button id="restore-version-1">Restore</button>` (the suffix `1` indicates it is tied to a version id or index; dynamic IDs generated accordingly)
- Back to Edit button: `<button id="back-to-edit-history">Back to Edit</button>`

### 5. my_articles.html
- Page container: `<div id="my-articles-page">`
- Filter by status dropdown: `<select id="filter-article-status">` with article status options
- Articles table: `<table id="articles-table">` with columns for Article ID, Title, Status, Category, Created Date, Actions
- Create New Article button: `<button id="create-new-article">Create New Article</button>`
- Back to Dashboard button: `<button id="back-to-dashboard">Back to Dashboard</button>`

### 6. published_articles.html
- Page container: `<div id="published-articles-page">`
- Filter by category dropdown: `<select id="filter-published-category">` with article category options
- Articles grid: `<div id="published-articles-grid">` grid layout listing articles
- Sort by dropdown: `<select id="sort-published">` with sorting options (e.g., date, popularity)
- Back to Dashboard button: `<button id="back-to-dashboard-published">Back to Dashboard</button>`

### 7. content_calendar.html
- Page container: `<div id="calendar-page">`
- Calendar view selector: `<select id="calendar-view">` (e.g., daily, weekly, monthly)
- Calendar grid: `<div id="calendar-grid">` visual calendar display
- Schedule button: `<button id="schedule-button">Schedule</button>`
- Back to Dashboard button: `<button id="back-to-dashboard-calendar">Back to Dashboard</button>`

### 8. article_analytics.html
- Page container: `<div id="analytics-page">`
- Analytics overview section: `<section id="analytics-overview">`
- Total views display: `<span id="analytics-total-views">`
- Unique visitors display: `<span id="analytics-unique-visitors">`
- Back to Article button: `<button id="back-to-article-analytics">Back to Article</button>`

---

## Section 3: Data File Schemas

### 1. users.txt
- Format (pipe-delimited): `username|email|fullname|created_date`
- Fields:
  - `username` (string): unique user identifier
  - `email` (string): user email address
  - `fullname` (string): user's full name
  - `created_date` (string, `YYYY-MM-DD`): account creation date
- Example rows:
```
john|john@example.com|John Doe|2024-01-15
alice|alice@example.com|Alice Smith|2024-01-16
bob|bob@example.com|Bob Johnson|2024-01-17
admin|admin@example.com|Admin User|2024-01-10
```

### 2. articles.txt
- Format (pipe-delimited): `article_id|title|author|category|status|tags|featured_image|meta_description|created_date|publish_date`
- Fields:
  - `article_id` (int): unique article identifier
  - `title` (string): article title
  - `author` (string): username of author
  - `category` (string): one of `news`, `blog`, `tutorial`, `announcement`, `press_release`
  - `status` (string): one of `draft`, `pending_review`, `under_review`, `approved`, `published`, `rejected`, `archived`
  - `tags` (string): comma-separated keywords
  - `featured_image` (string): URL or relative path to image; can be empty string if none
  - `meta_description` (string): short description for SEO
  - `created_date` (string, `YYYY-MM-DD`)
  - `publish_date` (string, `YYYY-MM-DD HH:MM:SS`); can be empty if unpublished
- Example rows:
```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
```

### 3. article_versions.txt
- Format (pipe-delimited): `version_id|article_id|version_number|content|author|created_date|change_summary`
- Fields:
  - `version_id` (int): unique version record ID
  - `article_id` (int): associated article ID
  - `version_number` (int): incremental version number per article
  - `content` (string): full article content
  - `author` (string): username of content author
  - `created_date` (string, `YYYY-MM-DD HH:MM:SS`): timestamp of version creation
  - `change_summary` (string): brief description of changes
- Example rows:
```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
```

### 4. approvals.txt
- Format (pipe-delimited): `approval_id|article_id|version_id|approver|status|comments|timestamp`
- Fields:
  - `approval_id` (int): unique approval record identifier
  - `article_id` (int): article associated with approval
  - `version_id` (int): article version approved/rejected
  - `approver` (string): username of approver
  - `status` (string): one of `approved`, `rejected`, `revision_requested`
  - `comments` (string): approver comments
  - `timestamp` (string, `YYYY-MM-DD HH:MM:SS`)
- Example rows:
```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
```

### 5. workflow_stages.txt
- Format (pipe-delimited): `stage_id|category|stage_name|stage_order|is_required`
- Fields:
  - `stage_id` (int): unique workflow stage ID
  - `category` (string): article category this stage applies to
  - `stage_name` (string): descriptive name of the stage
  - `stage_order` (int): ordinal position in workflow
  - `is_required` (string): yes/no indicating if stage is mandatory
- Example rows:
```
1|tutorial|Editor Review|1|yes
2|tutorial|Publisher Approval|2|yes
3|news|Editor Review|1|yes
4|announcement|Editor Review|1|yes
5|announcement|Publisher Approval|2|yes
```

### 6. comments.txt
- Format (pipe-delimited): `comment_id|article_id|version_id|user|comment_text|timestamp`
- Fields:
  - `comment_id` (int): unique comment ID
  - `article_id` (int): related article ID
  - `version_id` (int): version for which comment applies
  - `user` (string): username who made comment
  - `comment_text` (string): text content of comment
  - `timestamp` (string, `YYYY-MM-DD HH:MM:SS`)
- Example rows:
```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
```

### 7. analytics.txt
- Format (pipe-delimited): `analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares`
- Fields:
  - `analytics_id` (int): unique analytics record
  - `article_id` (int): article identifier
  - `date` (string, `YYYY-MM-DD`): date of metric
  - `views` (int): total page views
  - `unique_visitors` (int): unique visitors count
  - `avg_time_seconds` (int): average time spent in seconds
  - `shares` (int): number of shares on social media
- Example rows:
```
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
```

---

This design specification document provides all needed details for backend route creation, frontend template development, and data storage formatting for the ContentPublishingHub application.