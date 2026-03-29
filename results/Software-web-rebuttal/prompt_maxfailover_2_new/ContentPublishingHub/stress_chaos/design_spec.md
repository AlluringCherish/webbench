# ContentPublishingHub Design Specification

## Flask Routes Specification

### 1. Dashboard Page
- Route URL: `/dashboard`
- HTTP Methods: GET
- Function Handler Name: `dashboard`
- Template Rendered: `dashboard.html`
- Context Variables to Template:
  - `username` (str): current logged-in user's name
  - `quick_stats` (dict): statistics summary
  - `recent_activity` (list): recent user activity entries

### 2. Create Article Page
- Route URL: `/article/create`
- HTTP Methods: GET, POST
- Function Handler Name: `create_article`
- Template Rendered: `create_article.html`
- Context Variables:
  - For GET: none or blank form
  - For POST: validation errors, success messages

### 3. Edit Article Page
- Route URL: `/article/<article_id>/edit`
- HTTP Methods: GET, POST
- Function Handler Name: `edit_article`
- Template Rendered: `edit_article.html`
- Context Variables:
  - `article` (dict): article details including current title and content

### 4. Article Version History Page
- Route URL: `/article/<article_id>/versions`
- HTTP Methods: GET
- Function Handler Name: `version_history`
- Template Rendered: `version_history.html`
- Context Variables:
  - `versions` (list): list of versions with metadata for the article
  - `current_version_id` (int)

### 5. My Articles Page
- Route URL: `/articles/mine`
- HTTP Methods: GET
- Function Handler Name: `my_articles`
- Template Rendered: `my_articles.html`
- Context Variables:
  - `articles` (list): user's articles filtered by status
  - `filter_status` (str): current filter status

### 6. Published Articles Page
- Route URL: `/articles/published`
- HTTP Methods: GET
- Function Handler Name: `published_articles`
- Template Rendered: `published_articles.html`
- Context Variables:
  - `articles` (list): published articles filtered by category and sort
  - `filter_category` (str)
  - `sort_order` (str)

### 7. Content Calendar Page
- Route URL: `/calendar`
- HTTP Methods: GET
- Function Handler Name: `content_calendar`
- Template Rendered: `content_calendar.html`
- Context Variables:
  - `calendar_view` (str): current selected calendar view
  - `scheduled_articles` (list): scheduled articles for display

### 8. Article Analytics Page
- Route URL: `/article/<article_id>/analytics`
- HTTP Methods: GET
- Function Handler Name: `article_analytics`
- Template Rendered: `article_analytics.html`
- Context Variables:
  - `analytics_data` (dict): engagement metrics for article


## HTML Templates Specification

### `dashboard.html`
- Page container id: `dashboard-page`
- Elements:
  - Welcome message with id `welcome-message`
  - Quick stats section id `quick-stats`
  - Create Article button id `create-article-button` (link to `/article/create`)
  - Recent activity feed id `recent-activity`

### `create_article.html`
- Page container id: `create-article-page`
- Form elements:
  - Article title input id `article-title`
  - Content editor textarea id `article-content`
  - Save as Draft button id `save-draft-button`
  - Cancel button id `cancel-button` (navigates back or dashboard)

### `edit_article.html`
- Page container id: `edit-article-page`
- Form elements:
  - Article title input id `edit-article-title`
  - Content editor textarea id `edit-article-content`
  - Save New Version button id `save-version-button`
  - Cancel button id `cancel-edit`

### `version_history.html`
- Page container id: `version-history-page`
- Versions list container id: `versions-list` (listing all versions)
- Version comparison section id: `version-comparison`
- Restore button specifically: `restore-version-1` for version 1 and similar pattern for others
- Back to Edit button id: `back-to-edit-history`

### `my_articles.html`
- Page container id: `my-articles-page`
- Filter dropdown id: `filter-article-status`
- Articles table id: `articles-table`
- Create New Article button id: `create-new-article` (links to `/article/create`)
- Back to Dashboard button id: `back-to-dashboard`

### `published_articles.html`
- Page container id: `published-articles-page`
- Filter by category dropdown id: `filter-published-category`
- Articles grid container id: `published-articles-grid`
- Sort by dropdown id: `sort-published`
- Back to Dashboard button id: `back-to-dashboard-published`

### `content_calendar.html`
- Page container id: `calendar-page`
- Calendar view selector dropdown id: `calendar-view`
- Calendar grid id: `calendar-grid`
- Schedule button id: `schedule-button`
- Back to Dashboard button id: `back-to-dashboard-calendar`

### `article_analytics.html`
- Page container id: `analytics-page`
- Analytics overview section id: `analytics-overview`
- Total views display id: `analytics-total-views`
- Unique visitors display id: `analytics-unique-visitors`
- Back to Article button id: `back-to-article-analytics`


## Data File Schemas Specification

### 1. users.txt
- Pipe-delimited fields:
  `username|email|fullname|created_date`
- Meaning:
  - username: unique user identifier (string)
  - email: user email address (string)
  - fullname: full name of user (string)
  - created_date: account creation date (YYYY-MM-DD string)
- Example rows:
  ```
john|john@example.com|John Doe|2024-01-15
alice|alice@example.com|Alice Smith|2024-01-16
bob|bob@example.com|Bob Johnson|2024-01-17
admin|admin@example.com|Admin User|2024-01-10
```

### 2. articles.txt
- Pipe-delimited fields:
  `article_id|title|author|category|status|tags|featured_image|meta_description|created_date|publish_date`
- Meaning:
  - article_id: integer unique article ID
  - title: article title string
  - author: username string
  - category: enumerated string values ["news", "blog", "tutorial", "announcement", "press_release"]
  - status: enumerated string values ["draft", "pending_review", "under_review", "approved", "published", "rejected", "archived"]
  - tags: comma-separated string list
  - featured_image: URL path string or empty
  - meta_description: short description string
  - created_date: date string YYYY-MM-DD
  - publish_date: datetime string YYYY-MM-DD HH:MM:SS or empty if unpublished
- Example rows:
  ```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
```

### 3. article_versions.txt
- Pipe-delimited fields:
  `version_id|article_id|version_number|content|author|created_date|change_summary`
- Meaning:
  - version_id: unique integer version id
  - article_id: integer article ID
  - version_number: integer (incrementing version number)
  - content: string with full article text
  - author: username string
  - created_date: datetime string YYYY-MM-DD HH:MM:SS
  - change_summary: brief string description of changes
- Example rows:
  ```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
```

### 4. approvals.txt
- Pipe-delimited fields:
  `approval_id|article_id|version_id|approver|status|comments|timestamp`
- Meaning:
  - approval_id: unique integer id
  - article_id: integer article ID
  - version_id: integer article version ID
  - approver: username string
  - status: enumerated string ["approved", "rejected", "revision_requested"]
  - comments: free text comments string
  - timestamp: datetime string YYYY-MM-DD HH:MM:SS
- Example rows:
  ```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
```

### 5. workflow_stages.txt
- Pipe-delimited fields:
  `stage_id|category|stage_name|stage_order|is_required`
- Meaning:
  - stage_id: unique integer stage identifier
  - category: article category string
  - stage_name: name of workflow stage string
  - stage_order: integer order of workflow stages
  - is_required: string "yes" or "no" indicating if stage is mandatory
- Example rows:
  ```
1|tutorial|Editor Review|1|yes
2|tutorial|Publisher Approval|2|yes
3|news|Editor Review|1|yes
4|announcement|Editor Review|1|yes
5|announcement|Publisher Approval|2|yes
```

### 6. comments.txt
- Pipe-delimited fields:
  `comment_id|article_id|version_id|user|comment_text|timestamp`
- Meaning:
  - comment_id: unique integer id
  - article_id: integer article ID
  - version_id: integer article version ID
  - user: username string
  - comment_text: comment content string
  - timestamp: datetime string YYYY-MM-DD HH:MM:SS
- Example rows:
  ```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
```

### 7. analytics.txt
- Pipe-delimited fields:
  `analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares`
- Meaning:
  - analytics_id: unique integer id
  - article_id: integer
  - date: YYYY-MM-DD
  - views: integer total page views
  - unique_visitors: integer unique visitors
  - avg_time_seconds: integer average duration of visit in seconds
  - shares: integer social shares count
- Example rows:
  ```
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
```

---

This design specification document fully aligns with user requirements to enable backend and frontend development concurrently and independently.