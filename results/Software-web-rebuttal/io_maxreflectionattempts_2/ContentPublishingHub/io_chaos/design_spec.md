# ContentPublishingHub Design Specification

---

## Section 1: Flask Routes Specification

| Route Pattern                      | Methods  | Function Name                  | Template Rendered       | Context Variables                             |
|----------------------------------|----------|-------------------------------|------------------------|-----------------------------------------------|
| `/dashboard`                     | GET      | dashboard                     | dashboard.html         | `username` (str), `quick_stats` (dict), `recent_activity` (list of dicts) |
| `/article/create`                | GET, POST| create_article                | create_article.html    | GET: None; POST: result messages or validation errors |
| `/article/<article_id>/edit`    | GET, POST| edit_article                  | edit_article.html      | `article_id` (int), `title` (str), `content` (str) |
| `/article/<article_id>/versions`| GET      | article_version_history       | version_history.html   | `article_id` (int), `versions` (list of dicts), `comparison` (dict), `current_version` (int) |
| `/articles/mine`                | GET      | my_articles                   | my_articles.html       | `articles` (list of dicts), `filter_status` (str) |
| `/articles/published`           | GET      | published_articles            | published_articles.html| `articles` (list of dicts), `filter_category` (str), `sort_option` (str) |
| `/calendar`                    | GET, POST| content_calendar              | content_calendar.html  | `calendar_view` (str), `calendar_data` (list or dict of scheduled articles) |
| `/article/<article_id>/analytics`| GET    | article_analytics             | article_analytics.html | `article_id` (int), `analytics` (dict) |

---

## Section 2: HTML Template Structure

### 1. Dashboard Page (`dashboard.html`)
- Page container: `<div id="dashboard-page">`
- Welcome message: `<div id="welcome-message">` displays "Welcome, {username}!"
- Quick stats section: `<section id="quick-stats">`
- Create Article button: `<button id="create-article-button">Create Article</button>`
- Recent activity feed: `<div id="recent-activity">` List recent content actions

### 2. Create Article Page (`create_article.html`)
- Page container: `<div id="create-article-page">`
- Article title input: `<input type="text" id="article-title" name="article_title">`
- Content editor textarea: `<textarea id="article-content" name="article_content"></textarea>`
- Save as Draft button: `<button id="save-draft-button">Save as Draft</button>`
- Cancel button: `<button id="cancel-button">Cancel</button>`

### 3. Edit Article Page (`edit_article.html`)
- Page container: `<div id="edit-article-page">`
- Article title input: `<input type="text" id="edit-article-title" name="edit_article_title" value="{{ title }}">`
- Content editor textarea: `<textarea id="edit-article-content" name="edit_article_content">{{ content }}</textarea>`
- Save New Version button: `<button id="save-version-button">Save New Version</button>`
- Cancel button: `<button id="cancel-edit">Cancel</button>`

### 4. Article Version History Page (`version_history.html`)
- Page container: `<div id="version-history-page">`
- Versions list: `<ul id="versions-list">` with each version listed (version number, date, change summary)
- Version comparison section: `<div id="version-comparison">` to show diff between versions
- Restore button: `<button id="restore-version-1">Restore Selected Version</button>`
- Back to Edit button: `<button id="back-to-edit-history">Back to Edit</button>`

### 5. My Articles Page (`my_articles.html`)
- Page container: `<div id="my-articles-page">`
- Filter by status dropdown: `<select id="filter-article-status">` with options: draft, pending_review, under_review, approved, published, rejected, archived
- Articles table: `<table id="articles-table">` with columns for Title, Category, Status, Publish Date, Actions
- Create New Article button: `<button id="create-new-article">Create New Article</button>`
- Back to Dashboard button: `<button id="back-to-dashboard">Back to Dashboard</button>`

### 6. Published Articles Page (`published_articles.html`)
- Page container: `<div id="published-articles-page">`
- Filter by category dropdown: `<select id="filter-published-category">` with options: news, blog, tutorial, announcement, press_release
- Articles grid: `<div id="published-articles-grid">` shows article previews (title, image, publish date)
- Sort by dropdown: `<select id="sort-published">` with options like publish_date ascending/descending
- Back to Dashboard button: `<button id="back-to-dashboard-published">Back to Dashboard</button>`

### 7. Content Calendar Page (`content_calendar.html`)
- Page container: `<div id="calendar-page">`
- Calendar view selector: `<select id="calendar-view">` options: daily, weekly, monthly
- Calendar grid: `<div id="calendar-grid">` displays scheduled articles by date
- Schedule button: `<button id="schedule-button">Schedule</button>`
- Back to Dashboard button: `<button id="back-to-dashboard-calendar">Back to Dashboard</button>`

### 8. Article Analytics Page (`article_analytics.html`)
- Page container: `<div id="analytics-page">`
- Analytics overview: `<section id="analytics-overview">`
- Total views: `<span id="analytics-total-views">`
- Unique visitors: `<span id="analytics-unique-visitors">`
- Back to Article button: `<button id="back-to-article-analytics">Back to Article</button>`

---

## Section 3: Data File Schemas

### 1. users.txt
- Format: `username|email|fullname|created_date`
- Fields:
  1. username (str) - unique user identifier
  2. email (str) - user email address
  3. fullname (str) - full name of user
  4. created_date (YYYY-MM-DD) - date user account was created
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
  1. article_id (int) - unique article identifier
  2. title (str) - article title
  3. author (str) - username of author
  4. category (enum) - one of: news, blog, tutorial, announcement, press_release
  5. status (enum) - one of: draft, pending_review, under_review, approved, published, rejected, archived
  6. tags (csv) - comma-separated list of tags
  7. featured_image (str) - path/URL to the featured image (nullable)
  8. meta_description (str) - brief description
  9. created_date (YYYY-MM-DD) - date created
  10. publish_date (YYYY-MM-DD HH:MM:SS) - date/time published (nullable)
- Example:
```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
```

### 3. article_versions.txt
- Format: `version_id|article_id|version_number|content|author|created_date|change_summary`
- Fields:
  1. version_id (int) - unique version identifier
  2. article_id (int) - associated article
  3. version_number (int) - numeric version number
  4. content (str) - article content text
  5. author (str) - username who made the change
  6. created_date (YYYY-MM-DD HH:MM:SS) - version creation timestamp
  7. change_summary (str) - brief description of changes
- Example:
```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
```

### 4. approvals.txt
- Format: `approval_id|article_id|version_id|approver|status|comments|timestamp`
- Fields:
  1. approval_id (int) - unique approval record
  2. article_id (int) - article related
  3. version_id (int) - version approved/rejected
  4. approver (str) - username of approver
  5. status (enum) - approved, rejected, revision_requested
  6. comments (str) - approver comments
  7. timestamp (YYYY-MM-DD HH:MM:SS) - approval timestamp
- Example:
```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
```

### 5. workflow_stages.txt
- Format: `stage_id|category|stage_name|stage_order|is_required`
- Fields:
  1. stage_id (int) - unique workflow stage
  2. category (str) - article category
  3. stage_name (str) - name of the workflow step
  4. stage_order (int) - numeric order of the stage
  5. is_required (str) - "yes" or "no" indicating if mandatory
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
  1. comment_id (int) - unique comment identifier
  2. article_id (int) - article related
  3. version_id (int) - version related
  4. user (str) - username who commented
  5. comment_text (str) - comment content
  6. timestamp (YYYY-MM-DD HH:MM:SS) - comment timestamp
- Example:
```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
```

### 7. analytics.txt
- Format: `analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares`
- Fields:
  1. analytics_id (int) - unique analytics record
  2. article_id (int) - article referenced
  3. date (YYYY-MM-DD) - date of analytics
  4. views (int) - total views
  5. unique_visitors (int) - unique visitors
  6. avg_time_seconds (int) - average time spent in seconds
  7. shares (int) - number of times shared
- Example:
```
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
```

---

*This design specification document enables the backend and frontend teams to implement the 'ContentPublishingHub' application independently and in alignment with all specified requirements.*
