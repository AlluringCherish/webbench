# ContentPublishingHub Design Specification

---

## Section 1: Flask Routes Specification

| Route Pattern                    | HTTP Method(s) | Function Name             | Template Rendered        | Context Variables Passed to Template                                                                                               |
|--------------------------------|----------------|---------------------------|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| `/dashboard`                   | GET            | dashboard                 | dashboard.html           | `username` (str): logged-in user's username
  `quick_stats` (dict): stats summary for quick-stats section
  `recent_activity` (list): recent activity items (dicts)                                  |
| `/article/create`              | GET, POST      | create_article            | create_article.html      | On GET: none
On POST (after submission): possible error messages or success state                                                           |
| `/article/<article_id>/edit`  | GET, POST      | edit_article              | edit_article.html        | On GET: `article` (dict): {id, title, content, author, ...}, for filling input fields
On POST: validation/errors context                                  |
| `/article/<article_id>/versions`| GET          | view_article_versions     | version_history.html     | `article_id` (int)
`versions` (list of dicts): each version metadata and content
`comparison_data` (optional) (dict): for version comparison display                    |
| `/articles/mine`              | GET            | my_articles               | my_articles.html         | `articles` (list of dicts): user's articles
`filter_status_options` (list of str): possible status filter dropdown values                                              |
| `/articles/published`         | GET            | published_articles        | published_articles.html  | `articles` (list of dicts): published articles
`category_options` (list of str): categories for filter dropdown
`sort_options` (list of str): sorting criteria                                |
| `/calendar`                   | GET            | content_calendar          | content_calendar.html    | `calendar_views` (list of str): calendar view selector options
`schedule_data` (list/dict): data for calendar grid                                                         |
| `/article/<article_id>/analytics`| GET         | article_analytics         | article_analytics.html   | `article_id` (int)
`analytics` (dict): engagement metrics summary including total views, unique visitors, etc.                                                             |


---

## Section 2: HTML Template Structure

### 1. dashboard.html
- Page container element ID: `dashboard-page`
- Elements:
  - Welcome message: `welcome-message`
  - Quick stats section: `quick-stats`
  - Create Article button: `create-article-button`
  - Recent activity feed: `recent-activity`
- Layout:
  - Navigation buttons to create article and go to other pages
  - Display summary stats and recent activity details clearly

### 2. create_article.html
- Page container element ID: `create-article-page`
- Elements:
  - Article title input field: `article-title`
  - Content editor textarea: `article-content`
  - Save as Draft button: `save-draft-button`
  - Cancel button: `cancel-button`
- Layout:
  - Form inputs with labels for title and content
  - Buttons for saving draft and cancelling creation

### 3. edit_article.html
- Page container element ID: `edit-article-page`
- Elements:
  - Article title input field: `edit-article-title`
  - Content editor textarea: `edit-article-content`
  - Save New Version button: `save-version-button`
  - Cancel button: `cancel-edit`
- Layout:
  - Populate fields with current article data
  - Buttons to save new version and cancel editing

### 4. version_history.html
- Page container element ID: `version-history-page`
- Elements:
  - Versions list container: `versions-list`
  - Version comparison section: `version-comparison`
  - Restore button: `restore-version-1`
  - Back to Edit button: `back-to-edit-history`
- Layout:
  - List all versions with metadata
  - Area to compare selected versions
  - Options to restore a version or return to edit

### 5. my_articles.html
- Page container element ID: `my-articles-page`
- Elements:
  - Filter dropdown: `filter-article-status`
  - Articles table: `articles-table`
  - Create New Article button: `create-new-article`
  - Back to Dashboard button: `back-to-dashboard`
- Layout:
  - Table lists articles with columns such as Title, Status, Date
  - Filter controls to select status
  - Buttons for creating new article and dashboard navigation

### 6. published_articles.html
- Page container element ID: `published-articles-page`
- Elements:
  - Filter dropdown: `filter-published-category`
  - Articles grid: `published-articles-grid`
  - Sort by dropdown: `sort-published`
  - Back to Dashboard button: `back-to-dashboard-published`
- Layout:
  - Cards or grid layout for articles
  - Filters for category and sorting
  - Navigation button back to dashboard

### 7. content_calendar.html
- Page container element ID: `calendar-page`
- Elements:
  - Calendar view selector dropdown: `calendar-view`
  - Calendar grid container: `calendar-grid`
  - Schedule button: `schedule-button`
  - Back to Dashboard button: `back-to-dashboard-calendar`
- Layout:
  - Calendar view selector changes calendar grid display
  - Schedule button to open scheduling form
  - Clear navigation controls

### 8. article_analytics.html
- Page container element ID: `analytics-page`
- Elements:
  - Analytics overview container: `analytics-overview`
  - Total views display: `analytics-total-views`
  - Unique visitors display: `analytics-unique-visitors`
  - Back to Article button: `back-to-article-analytics`
- Layout:
  - Summary statistics display
  - Navigation back to article editing or viewing page


---

## Section 3: Data File Schemas

### 1. users.txt
- Format: `username|email|fullname|created_date`
- Fields:
  - username (string): user login name
  - email (string): user's email
  - fullname (string): full name
  - created_date (YYYY-MM-DD string): account creation date
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
  - article_id (integer): unique article identifier
  - title (string): article title
  - author (string): username of author
  - category (enum string): one of [news, blog, tutorial, announcement, press_release]
  - status (enum string): one of [draft, pending_review, under_review, approved, published, rejected, archived]
  - tags (comma-separated string): tags associated
  - featured_image (string): URL/path or empty if none
  - meta_description (string): SEO description
  - created_date (YYYY-MM-DD string): creation date
  - publish_date (YYYY-MM-DD HH:MM:SS string or empty): scheduled or actual publish datetime
- Example:
  ```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
  ```

### 3. article_versions.txt
- Format: `version_id|article_id|version_number|content|author|created_date|change_summary`
- Fields:
  - version_id (integer): unique version ID
  - article_id (integer): article reference
  - version_number (integer): incremental version number
  - content (string): full content text
  - author (string): username who made this version
  - created_date (YYYY-MM-DD HH:MM:SS string): timestamp of version creation
  - change_summary (string): brief description of changes
- Example:
  ```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
  ```

### 4. approvals.txt
- Format: `approval_id|article_id|version_id|approver|status|comments|timestamp`
- Fields:
  - approval_id (int): unique ID
  - article_id (int): article ID
  - version_id (int): version ID
  - approver (string): username who approved/rejected
  - status (enum string): one of [approved, rejected, revision_requested]
  - comments (string): approval comments
  - timestamp (YYYY-MM-DD HH:MM:SS string): action time
- Example:
  ```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
  ```

### 5. workflow_stages.txt
- Format: `stage_id|category|stage_name|stage_order|is_required`
- Fields:
  - stage_id (int): unique stage ID
  - category (string): article category
  - stage_name (string): name of workflow stage
  - stage_order (int): order of stage
  - is_required (string): "yes" or "no" indicating if stage is required
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
  - comment_id (int): unique comment ID
  - article_id (int): article reference
  - version_id (int): article version ID
  - user (string): username of commenter
  - comment_text (string): comment content
  - timestamp (YYYY-MM-DD HH:MM:SS string): comment time
- Example:
  ```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
  ```

### 7. analytics.txt
- Format: `analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares`
- Fields:
  - analytics_id (int): unique analytics record ID
  - article_id (int): article related
  - date (YYYY-MM-DD string): date of metric
  - views (int): number of views
  - unique_visitors (int): number of unique visitors
  - avg_time_seconds (int): average time spent in seconds
  - shares (int): number of shares on social media
- Example:
  ```
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
  ```

---

This design specification document defines the entire backend routes, frontend template element structure including exact element IDs, and data file schema required for implementing the ContentPublishingHub web application, enabling backend and frontend teams to work independently.
