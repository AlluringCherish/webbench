# ContentPublishingHub Design Specification

---

## Section 1: Flask Routes Specification

| Route                           | HTTP Method(s) | Function Name             | Template Rendered         | Context Variables
|--------------------------------|----------------|---------------------------|---------------------------|------------------
| /dashboard                     | GET            | dashboard                 | dashboard.html            | username: str
|                                |                |                           |                           | quick_stats: dict
|                                |                |                           |                           | recent_activities: list
| /article/create                | GET, POST      | create_article            | create_article.html       | (GET) None
|                                |                |                           |                           | (POST) form data processing
| /article/<article_id>/edit     | GET, POST      | edit_article              | edit_article.html         | (GET) article: dict
|                                |                |                           |                           | (POST) updated form data
| /article/<article_id>/versions | GET            | article_version_history   | version_history.html      | article_id: int
|                                |                |                           |                           | versions: list
| /articles/mine                 | GET            | my_articles               | my_articles.html          | articles: list
|                                |                |                           |                           | filter_statuses: list
| /articles/published            | GET            | published_articles        | published_articles.html   | articles: list
|                                |                |                           |                           | categories: list
| /calendar                     | GET            | content_calendar          | content_calendar.html     | scheduled_publications: list
| /article/<article_id>/analytics| GET            | article_analytics         | article_analytics.html    | analytics_data: dict


## Section 2: HTML Template Structure

### 1. dashboard.html
- Page container id: `dashboard-page`
- Welcome message id: `welcome-message` (shows username)
- Quick stats section id: `quick-stats`
- Create Article button id: `create-article-button`
- Recent activity feed id: `recent-activity`

### 2. create_article.html
- Page container id: `create-article-page`
- Article title input id: `article-title`
- Content editor textarea id: `article-content`
- Save as Draft button id: `save-draft-button`
- Cancel button id: `cancel-button`

### 3. edit_article.html
- Page container id: `edit-article-page`
- Article title input id: `edit-article-title`
- Content editor textarea id: `edit-article-content`
- Save New Version button id: `save-version-button`
- Cancel button id: `cancel-edit`

### 4. version_history.html
- Page container id: `version-history-page`
- Versions list id: `versions-list`
- Version comparison section id: `version-comparison`
- Restore button id: `restore-version-1` (for selected version)
- Back to Edit button id: `back-to-edit-history`

### 5. my_articles.html
- Page container id: `my-articles-page`
- Filter by status dropdown id: `filter-article-status`
- Articles table id: `articles-table`
- Create New Article button id: `create-new-article`
- Back to Dashboard button id: `back-to-dashboard`

### 6. published_articles.html
- Page container id: `published-articles-page`
- Filter by category dropdown id: `filter-published-category`
- Articles grid id: `published-articles-grid`
- Sort by dropdown id: `sort-published`
- Back to Dashboard button id: `back-to-dashboard-published`

### 7. content_calendar.html
- Page container id: `calendar-page`
- Calendar view selector id: `calendar-view`
- Calendar grid id: `calendar-grid`
- Schedule button id: `schedule-button`
- Back to Dashboard button id: `back-to-dashboard-calendar`

### 8. article_analytics.html
- Page container id: `analytics-page`
- Analytics overview id: `analytics-overview`
- Total views id: `analytics-total-views`
- Unique visitors id: `analytics-unique-visitors`
- Back to Article button id: `back-to-article-analytics`


## Section 3: Data File Schemas

### 1. users.txt
- Format: `username|email|fullname|created_date`
- Fields:
  - username: string (unique user login)
  - email: string
  - fullname: string
  - created_date: date in YYYY-MM-DD
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
  - article_id: integer (unique article identifier)
  - title: string
  - author: string (username)
  - category: enum (news, blog, tutorial, announcement, press_release)
  - status: enum (draft, pending_review, under_review, approved, published, rejected, archived)
  - tags: comma-separated string
  - featured_image: string (URL or path, empty if none)
  - meta_description: string
  - created_date: date YYYY-MM-DD
  - publish_date: datetime YYYY-MM-DD HH:MM:SS (empty if unpublished)
- Example rows:
```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
```

### 3. article_versions.txt
- Format: `version_id|article_id|version_number|content|author|created_date|change_summary`
- Fields:
  - version_id: integer (unique version identifier)
  - article_id: integer (references article_id)
  - version_number: integer (incremental per article)
  - content: string (full article content)
  - author: string (username)
  - created_date: datetime YYYY-MM-DD HH:MM:SS
  - change_summary: string
- Example rows:
```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
```

### 4. approvals.txt
- Format: `approval_id|article_id|version_id|approver|status|comments|timestamp`
- Fields:
  - approval_id: integer (unique approval identifier)
  - article_id: integer (references article_id)
  - version_id: integer (references version_id)
  - approver: string (username)
  - status: enum (approved, rejected, revision_requested)
  - comments: string
  - timestamp: datetime YYYY-MM-DD HH:MM:SS
- Example rows:
```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
```

### 5. workflow_stages.txt
- Format: `stage_id|category|stage_name|stage_order|is_required`
- Fields:
  - stage_id: integer (unique stage identifier)
  - category: string (content category, e.g., tutorial, news, announcement)
  - stage_name: string
  - stage_order: integer (order sequence in workflow)
  - is_required: enum (yes, no)
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
  - comment_id: integer (unique comment identifier)
  - article_id: integer (references article_id)
  - version_id: integer (references version_id)
  - user: string (username)
  - comment_text: string
  - timestamp: datetime YYYY-MM-DD HH:MM:SS
- Example rows:
```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
```

### 7. analytics.txt
- Format: `analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares`
- Fields:
  - analytics_id: integer (unique analytics record identifier)
  - article_id: integer (references article_id)
  - date: date YYYY-MM-DD
  - views: integer
  - unique_visitors: integer
  - avg_time_seconds: integer (average visit duration)
  - shares: integer
- Example rows:
```
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
```

---

This design specification document covers all required routes, templates, and data schema details for developers to implement backend and frontend independently and accurately.
