# ContentPublishingHub Design Specification

---

## Section 1: Flask Routes Specification

| Route Pattern                           | HTTP Methods | Function Name               | Template Rendered       | Context Variables (type and description)                       |
|---------------------------------------|--------------|-----------------------------|-------------------------|----------------------------------------------------------------|
| `/dashboard`                          | GET          | dashboard                  | dashboard.html          | `username` (str): Logged-in user's username
|                                       |              |                             |                         | `quick_stats` (dict): Key metrics for display
|                                       |              |                             |                         | `recent_activity` (list of dict): Recent activities/events

| `/article/create`                     | GET, POST    | create_article             | create_article.html      | GET: none
|                                       |              |                             |                         | POST: `title` (str), `content` (str) from form inputs

| `/article/<article_id>/edit`          | GET, POST    | edit_article               | edit_article.html         | GET: `article_id` (int), `title` (str), `content` (str)
|                                       |              |                             |                         | POST: updated `title` (str), `content` (str)

| `/article/<article_id>/versions`      | GET          | article_version_history    | version_history.html      | `article_id` (int)
|                                       |              |                             |                         | `versions` (list of dict): List of versions with metadata

| `/articles/mine`                      | GET          | my_articles                | my_articles.html          | `username` (str): current user
|                                       |              |                             |                         | `articles` (list of dict): User's articles
|                                       |              |                             |                         | `filter_status` (str): currently applied filter

| `/articles/published`                 | GET          | published_articles         | published_articles.html   | `articles` (list of dict): Published articles
|                                       |              |                             |                         | `filter_category` (str): selected category filter
|                                       |              |                             |                         | `sort_order` (str): current sorting criteria

| `/calendar`                          | GET          | content_calendar           | content_calendar.html     | `calendar_view` (str): Current calendar view mode
|                                       |              |                             |                         | `scheduled_items` (list of dict): Scheduled publications

| `/article/<article_id>/analytics`     | GET          | article_analytics          | article_analytics.html    | `article_id` (int)
|                                       |              |                             |                         | `analytics_overview` (dict): engagement metrics

---

## Section 2: HTML Template Structure

### 1. dashboard.html
- Page container: `dashboard-page`
- Elements:
  - Welcome message: `welcome-message`
  - Quick stats section: `quick-stats`
  - Create Article button: `create-article-button`
  - Recent activity feed: `recent-activity`
- Navigation:
  - Create Article button links to `/article/create`
  - Other navigation as per app design (not specified)

### 2. create_article.html
- Page container: `create-article-page`
- Elements:
  - Article title input: `article-title` (input type="text")
  - Content editor textarea: `article-content`
  - Save as Draft button: `save-draft-button`
  - Cancel button: `cancel-button`
- Navigation:
  - Cancel button redirects back (likely to `/dashboard` or previous page)

### 3. edit_article.html
- Page container: `edit-article-page`
- Elements:
  - Article title input: `edit-article-title` (input type="text")
  - Content editor textarea: `edit-article-content`
  - Save New Version button: `save-version-button`
  - Cancel button: `cancel-edit`
- Navigation:
  - Cancel button redirects back to appropriate page (e.g., `/articles/mine` or article detail)

### 4. version_history.html
- Page container: `version-history-page`
- Elements:
  - Versions list (e.g., a list or table): `versions-list`
  - Version comparison section: `version-comparison`
  - Restore button: `restore-version-1`
  - Back to Edit button: `back-to-edit-history`
- Navigation:
  - Back to Edit returns to article edit page

### 5. my_articles.html
- Page container: `my-articles-page`
- Elements:
  - Filter by status dropdown: `filter-article-status`
  - Articles table: `articles-table`
  - Create New Article button: `create-new-article`
  - Back to Dashboard button: `back-to-dashboard`
- Navigation:
  - Create New Article button links to `/article/create`
  - Back to Dashboard button links to `/dashboard`

### 6. published_articles.html
- Page container: `published-articles-page`
- Elements:
  - Filter by category dropdown: `filter-published-category`
  - Articles grid: `published-articles-grid`
  - Sort by dropdown: `sort-published`
  - Back to Dashboard button: `back-to-dashboard-published`
- Navigation:
  - Back to Dashboard button links to `/dashboard`

### 7. content_calendar.html
- Page container: `calendar-page`
- Elements:
  - Calendar view selector: `calendar-view`
  - Calendar grid: `calendar-grid`
  - Schedule button: `schedule-button`
  - Back to Dashboard button: `back-to-dashboard-calendar`
- Navigation:
  - Back to Dashboard button links to `/dashboard`

### 8. article_analytics.html
- Page container: `analytics-page`
- Elements:
  - Analytics overview section: `analytics-overview`
  - Total views: `analytics-total-views`
  - Unique visitors: `analytics-unique-visitors`
  - Back to Article button: `back-to-article-analytics`
- Navigation:
  - Back to Article button links to article edit or view page

---

## Section 3: Data File Schemas

### 1. users.txt
- Fields (pipe `|` delimited):
  - `username` (str): Unique login identifier
  - `email` (str): User email address
  - `fullname` (str): Full name of the user
  - `created_date` (date, YYYY-MM-DD): Account creation date
- Example:
  ```
john|john@example.com|John Doe|2024-01-15
alice|alice@example.com|Alice Smith|2024-01-16
bob|bob@example.com|Bob Johnson|2024-01-17
admin|admin@example.com|Admin User|2024-01-10
  ```

### 2. articles.txt
- Fields (pipe `|` delimited):
  - `article_id` (int): Unique article identifier
  - `title` (str): Article title
  - `author` (str): Username of the author
  - `category` (str): One of [news, blog, tutorial, announcement, press_release]
  - `status` (str): One of [draft, pending_review, under_review, approved, published, rejected, archived]
  - `tags` (str): Comma-separated tags
  - `featured_image` (str): Path to image or empty
  - `meta_description` (str): Meta description text
  - `created_date` (date, YYYY-MM-DD)
  - `publish_date` (datetime, YYYY-MM-DD HH:MM:SS) or empty if unpublished
- Example:
  ```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
  ```

### 3. article_versions.txt
- Fields (pipe `|` delimited):
  - `version_id` (int): Unique version identifier
  - `article_id` (int): Associated article ID
  - `version_number` (int): Version sequential number
  - `content` (str): Article content text
  - `author` (str): Username of author who created version
  - `created_date` (datetime, YYYY-MM-DD HH:MM:SS)
  - `change_summary` (str): Description of changes
- Example:
  ```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
  ```

### 4. approvals.txt
- Fields (pipe `|` delimited):
  - `approval_id` (int): Unique approval record
  - `article_id` (int): Article ID under review
  - `version_id` (int): Article version ID
  - `approver` (str): Username of approver
  - `status` (str): One of [approved, rejected, revision_requested]
  - `comments` (str): Optional review comments
  - `timestamp` (datetime, YYYY-MM-DD HH:MM:SS)
- Example:
  ```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
  ```

### 5. workflow_stages.txt
- Fields (pipe `|` delimited):
  - `stage_id` (int): Unique workflow stage ID
  - `category` (str): Article category this stage applies to
  - `stage_name` (str): Name of the workflow stage
  - `stage_order` (int): Order number in workflow
  - `is_required` (str): "yes" or "no", if stage is mandatory
- Example:
  ```
1|tutorial|Editor Review|1|yes
2|tutorial|Publisher Approval|2|yes
3|news|Editor Review|1|yes
4|announcement|Editor Review|1|yes
5|announcement|Publisher Approval|2|yes
  ```

### 6. comments.txt
- Fields (pipe `|` delimited):
  - `comment_id` (int): Unique comment ID
  - `article_id` (int): Article related
  - `version_id` (int): Version commented on
  - `user` (str): Username of commenter
  - `comment_text` (str): Comment content
  - `timestamp` (datetime, YYYY-MM-DD HH:MM:SS)
- Example:
  ```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
  ```

### 7. analytics.txt
- Fields (pipe `|` delimited):
  - `analytics_id` (int): Unique analytics record
  - `article_id` (int): Article tracked
  - `date` (date, YYYY-MM-DD): Date of metrics
  - `views` (int): Total views count
  - `unique_visitors` (int): Unique visitor count
  - `avg_time_seconds` (int): Average time spent on article in seconds
  - `shares` (int): Number of article shares
- Example:
  ```
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
  ```

---

This design specification file provides the detailed blueprint for backend Flask route implementation, frontend HTML template structure with exact IDs, and all textual data file schemas necessary for full system development and testing.