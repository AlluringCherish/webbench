# ContentPublishingHub Design Specification

---

## 1. Flask Routes Specification

| Route                              | HTTP Methods | Function Name                | Template Rendered      | Context Variables (name: type & description)                                                                                                   |
|----------------------------------|--------------|-----------------------------|------------------------|----------------------------------------------------------------------------------------------------------------------------|
| `/dashboard`                     | GET          | dashboard                   | dashboard.html          | - username: str (current user's username)
- quick_stats: dict (summary statistics for dashboard display)
- recent_activity: list of dicts (recent activities data) |
| `/article/create`                | GET, POST    | create_article              | create_article.html     | - For GET:
  - No specific context variables required
- For POST (after submission):
  - success_flag: bool (whether article creation succeeded)
  - errors: dict (validation errors if any)                                 |
| `/article/<article_id>/edit`    | GET, POST    | edit_article                | edit_article.html       | - article: dict (detailed article fields including 'title', 'content', 'article_id')
- errors: dict (validation errors on POST)
- current_version: str (content of current version)  |
| `/article/<article_id>/versions`| GET          | article_version_history     | version_history.html    | - article_id: int
- versions: list of dicts (each with 'version_id', 'version_number', 'author', 'created_date', 'change_summary')
- comparison_data: dict (data for version comparison)
|
| `/articles/mine`                | GET          | my_articles                 | my_articles.html        | - articles: list of dicts (user's articles with all relevant fields)
- filter_status_options: list of str (all possible status filters)            |
| `/articles/published`           | GET          | published_articles          | published_articles.html | - published_articles: list of dicts (articles with published status)
- category_options: list of str (all categories available)
- sort_options: list of str (sorting criteria)           |
| `/calendar`                    | GET          | content_calendar            | content_calendar.html   | - calendar_data: dict or list (structured data for the calendar grid display)
- view_options: list of str (calendar view modes)                                    |
| `/article/<article_id>/analytics`| GET         | article_analytics           | article_analytics.html  | - analytics_overview: dict (engagement metrics summarized)
- total_views: int
- unique_visitors: int
- article_id: int
|

---

## 2. HTML Template Structure

### 2.1 dashboard.html
- Main container ID: `dashboard-page`
- Required element IDs:
  - `welcome-message`
  - `quick-stats`
  - `create-article-button`
  - `recent-activity`
- Layout & Navigation:
  - Navigation includes a button (`create-article-button`) that links to `/article/create` for creating new articles.
  - Displays welcome message with username.
  - Shows quick statistics summary.
  - Shows recent activity feed.

### 2.2 create_article.html
- Main container ID: `create-article-page`
- Required element IDs:
  - `article-title` (input field)
  - `article-content` (textarea)
  - `save-draft-button` (button)
  - `cancel-button` (button, should navigate back to `/dashboard` or previous)
- Layout & Navigation:
  - Form to input new article title and content.
  - Save draft triggers POST to server.
  - Cancel leads back to Dashboard.

### 2.3 edit_article.html
- Main container ID: `edit-article-page`
- Required element IDs:
  - `edit-article-title` (input field)
  - `edit-article-content` (textarea)
  - `save-version-button` (button)
  - `cancel-edit` (button, navigates back to user's articles or dashboard)
- Layout & Navigation:
  - Editable form prefilled with article data.
  - Save new version submits changes.
  - Cancel discards edits and goes back.

### 2.4 version_history.html
- Main container ID: `version-history-page`
- Required element IDs:
  - `versions-list` (list or table to show versions)
  - `version-comparison` (section showing diff/comparison of selected versions)
  - `restore-version-1` (button to restore selected version, the '1' suffix implies dynamic naming or adjust for specific version id)
  - `back-to-edit-history` (button to return to edit article page)
- Layout & Navigation:
  - List of article versions with metadata.
  - Version comparison area.
  - Option to restore a version.
  - Navigation back to editing the article.

### 2.5 my_articles.html
- Main container ID: `my-articles-page`
- Required element IDs:
  - `filter-article-status` (dropdown to select article status filter)
  - `articles-table` (table listing user's articles with columns for key fields)
  - `create-new-article` (button linking to `/article/create`)
  - `back-to-dashboard` (button returning to Dashboard)
- Layout & Navigation:
  - Table displays filtered articles.
  - Filter dropdown allows status filtering.
  - Buttons to navigate create new or back.

### 2.6 published_articles.html
- Main container ID: `published-articles-page`
- Required element IDs:
  - `filter-published-category` (dropdown for article category filter)
  - `published-articles-grid` (grid or cards of published articles)
  - `sort-published` (dropdown for sorting by criteria)
  - `back-to-dashboard-published` (button to dashboard)
- Layout & Navigation:
  - Articles displayed visually in grid.
  - Category filter and sort dropdowns.
  - Navigation back to dashboard.

### 2.7 content_calendar.html
- Main container ID: `calendar-page`
- Required element IDs:
  - `calendar-view` (dropdown or selector for calendar views)
  - `calendar-grid` (grid/timeline showing scheduled content)
  - `schedule-button` (button to add new schedule)
  - `back-to-dashboard-calendar` (button to dashboard)
- Layout & Navigation:
  - Timeline or calendar display.
  - View selector to switch modes.
  - Schedule button to create publication schedules.

### 2.8 article_analytics.html
- Main container ID: `analytics-page`
- Required element IDs:
  - `analytics-overview` (container summarizing analytics)
  - `analytics-total-views` (display total view count)
  - `analytics-unique-visitors` (display unique visitor count)
  - `back-to-article-analytics` (button back to article or previous view)
- Layout & Navigation:
  - Displays key engagement metrics.
  - Navigation back to article editing or main article page.

---

## 3. Data File Schemas

### 3.1 users.txt
- Format (pipe-delimited): `username|email|fullname|created_date`
- Fields:
  - username: str, unique user identifier
  - email: str, user's email address
  - fullname: str, full name of user
  - created_date: str (YYYY-MM-DD), date user account was created
- Example:
  ```
  john|john@example.com|John Doe|2024-01-15
  alice|alice@example.com|Alice Smith|2024-01-16
  bob|bob@example.com|Bob Johnson|2024-01-17
  admin|admin@example.com|Admin User|2024-01-10
  ```

### 3.2 articles.txt
- Format: `article_id|title|author|category|status|tags|featured_image|meta_description|created_date|publish_date`
- Fields:
  - article_id: int, unique article identifier
  - title: str, article title
  - author: str (username), creator of article
  - category: str (enumerated) (news, blog, tutorial, announcement, press_release)
  - status: str (enumerated)
    * Possible values: draft, pending_review, under_review, approved, published, rejected, archived
  - tags: str, comma-separated tags
  - featured_image: str (URL or path), optional
  - meta_description: str, short article description
  - created_date: str (YYYY-MM-DD)
  - publish_date: str (YYYY-MM-DD HH:MM:SS), optional (blank if not published)
- Example:
  ```
  1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
  2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
  3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
  ```

### 3.3 article_versions.txt
- Format: `version_id|article_id|version_number|content|author|created_date|change_summary`
- Fields:
  - version_id: int, unique version identifier
  - article_id: int, linked article id
  - version_number: int, version sequence number
  - content: str, full article content text
  - author: str (username)
  - created_date: str (YYYY-MM-DD HH:MM:SS), version creation timestamp
  - change_summary: str, short description of changes
- Example:
  ```
  1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
  2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
  3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
  ```

### 3.4 approvals.txt
- Format: `approval_id|article_id|version_id|approver|status|comments|timestamp`
- Fields:
  - approval_id: int, unique approval record id
  - article_id: int
  - version_id: int
  - approver: str (username)
  - status: str (enumerated: approved, rejected, revision_requested)
  - comments: str, approver's comments
  - timestamp: str (YYYY-MM-DD HH:MM:SS)
- Example:
  ```
  1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
  2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
  3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
  ```

### 3.5 workflow_stages.txt
- Format: `stage_id|category|stage_name|stage_order|is_required`
- Fields:
  - stage_id: int
  - category: str (article category)
  - stage_name: str
  - stage_order: int, defines sequence order for a category
  - is_required: str ("yes" or "no")
- Example:
  ```
  1|tutorial|Editor Review|1|yes
  2|tutorial|Publisher Approval|2|yes
  3|news|Editor Review|1|yes
  4|announcement|Editor Review|1|yes
  5|announcement|Publisher Approval|2|yes
  ```

### 3.6 comments.txt
- Format: `comment_id|article_id|version_id|user|comment_text|timestamp`
- Fields:
  - comment_id: int
  - article_id: int
  - version_id: int
  - user: str (username)
  - comment_text: str
  - timestamp: str (YYYY-MM-DD HH:MM:SS)
- Example:
  ```
  1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
  2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
  3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
  ```

### 3.7 analytics.txt
- Format: `analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares`
- Fields:
  - analytics_id: int
  - article_id: int
  - date: str (YYYY-MM-DD)
  - views: int
  - unique_visitors: int
  - avg_time_seconds: int (average time spent in seconds)
  - shares: int
- Example:
  ```
  1|1|2024-01-22|150|120|245|12
  2|1|2024-01-23|230|180|210|18
  3|1|2024-01-24|180|140|220|15
  4|2|2024-01-25|95|75|180|8
  ```

---

This design specification document provides precise information for backend Flask route implementation, frontend HTML template construction, and data file schema definitions, enabling independent frontend and backend development.

