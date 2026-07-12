# ContentPublishingHub Design Specification

---

## Section 1: Flask Routes Specification

| Route Pattern                    | HTTP Method(s) | Function Name             | Template Rendered        | Context Variables Passed to Template                     |
|--------------------------------|----------------|---------------------------|--------------------------|----------------------------------------------------------|
| `/dashboard`                   | GET            | dashboard                 | dashboard.html           | `username` (str): Current user's username                |
| `/article/create`              | GET, POST      | create_article            | create_article.html      | GET: none; POST: validation errors (dict), form data      |
| `/article/<article_id>/edit`  | GET, POST      | edit_article              | edit_article.html        | `article_id` (int), `article` (dict with article data), `current_version` (dict), validation errors (POST) |
| `/article/<article_id>/versions` | GET         | version_history           | version_history.html     | `article_id` (int), `versions` (list of dicts), `selected_version` (optional), `comparison_result` (optional) |
| `/articles/mine`              | GET            | my_articles               | my_articles.html         | `username` (str), `articles` (list of dicts), `status_filter` (str) |
| `/articles/published`         | GET            | published_articles        | published_articles.html  | `articles` (list of dicts), `category_filter` (str), `sort_option` (str) |
| `/calendar`                   | GET, POST      | content_calendar          | content_calendar.html    | `scheduled_articles` (list of dicts), calendar view mode (str), schedule data (POST) |
| `/article/<article_id>/analytics` | GET        | article_analytics         | article_analytics.html   | `article_id` (int), `analytics` (dict)                    |

### Details:

1. **/dashboard** (GET)
   - Function: `dashboard`
   - Renders `dashboard.html`
   - Context:
      - `username`: str, Logged-in user's username

2. **/article/create** (GET, POST)
   - Function: `create_article`
   - GET: Displays article creation form
   - POST: Handles new article submission
   - Context (GET): None
   - Context (POST): e.g. `errors` dict, and possibly prefilled form data on validation failure

3. **/article/<article_id>/edit** (GET, POST)
   - Function: `edit_article`
   - GET: Loads article data and current latest version
   - POST: Saves new version, with validation
   - Context:
     - `article_id`: int
     - `article`: dict with keys matching articles.txt fields
     - `current_version`: dict of current article version
     - `errors`: dict (POST failure)

4. **/article/<article_id>/versions** (GET)
   - Function: `version_history`
   - Renders all previous versions
   - Context:
     - `article_id`: int
     - `versions`: list of dicts with version details
     - Optionally:
       - `selected_version`: details for comparing versions
       - `comparison_result`: diff or comparison data

5. **/articles/mine** (GET)
   - Function: `my_articles`
   - Lists articles by current user
   - Supports filter by status
   - Context:
     - `username`: str
     - `articles`: list of dicts
     - `status_filter`: str

6. **/articles/published** (GET)
   - Function: `published_articles`
   - Lists published articles with category filter and sort
   - Context:
     - `articles`: list of dicts
     - `category_filter`: str
     - `sort_option`: str

7. **/calendar** (GET, POST)
   - Function: `content_calendar`
   - GET: Shows scheduled contents
   - POST: Handles scheduling actions
   - Context:
     - `scheduled_articles`: list of dicts
     - `calendar_view`: str (day, week, month...)

8. **/article/<article_id>/analytics** (GET)
   - Function: `article_analytics`
   - Shows analytics for given article
   - Context:
     - `article_id`: int
     - `analytics`: aggregated or raw analytics data dict

---

## Section 2: HTML Template Structure

### 1. dashboard.html
- Page Container: `<div id="dashboard-page">`
- Elements:
  - Welcome message: id=`welcome-message`
  - Quick stats section: id=`quick-stats`
  - Create Article button: id=`create-article-button`
  - Recent activity feed container: id=`recent-activity`
- Navigation:
  - 'Create Article' button links to `/article/create`
  - Other navigation options may include links to `/articles/mine`, `/calendar`

### 2. create_article.html
- Page Container: `<div id="create-article-page">`
- Elements:
  - Input field for article title: id=`article-title`
  - Textarea for content editor: id=`article-content`
  - Save as Draft button: id=`save-draft-button`
  - Cancel button: id=`cancel-button`
- Navigation:
  - Cancel button returns to `/dashboard`

### 3. edit_article.html
- Page Container: `<div id="edit-article-page">`
- Elements:
  - Input field for article title: id=`edit-article-title`
  - Textarea for content editor: id=`edit-article-content`
  - Save New Version button: id=`save-version-button`
  - Cancel button: id=`cancel-edit`
- Navigation:
  - Cancel button returns to `/articles/mine`

### 4. version_history.html
- Page Container: `<div id="version-history-page">`
- Elements:
  - Versions list container: id=`versions-list`
  - Version comparison area: id=`version-comparison`
  - Restore button for selected version: id=`restore-version-1`
  - Back to Edit button: id=`back-to-edit-history`
- Navigation:
  - Back to Edit button links back to `/article/<article_id>/edit`

### 5. my_articles.html
- Page Container: `<div id="my-articles-page">`
- Elements:
  - Dropdown filter for article status: id=`filter-article-status`
  - Table listing articles: id=`articles-table`
  - Create New Article button: id=`create-new-article`
  - Back to Dashboard button: id=`back-to-dashboard`
- Navigation:
  - Create New Article button links to `/article/create`
  - Back button links to `/dashboard`

### 6. published_articles.html
- Page Container: `<div id="published-articles-page">`
- Elements:
  - Dropdown filter for published categories: id=`filter-published-category`
  - Articles grid: id=`published-articles-grid`
  - Sort dropdown: id=`sort-published`
  - Back to Dashboard button: id=`back-to-dashboard-published`
- Navigation:
  - Back button links to `/dashboard`

### 7. content_calendar.html
- Page Container: `<div id="calendar-page">`
- Elements:
  - Calendar view selector dropdown: id=`calendar-view`
  - Calendar grid display: id=`calendar-grid`
  - Schedule button to add new events: id=`schedule-button`
  - Back to Dashboard button: id=`back-to-dashboard-calendar`
- Navigation:
  - Back button links to `/dashboard`

### 8. article_analytics.html
- Page Container: `<div id="analytics-page">`
- Elements:
  - Analytics overview section: id=`analytics-overview`
  - Total views display: id=`analytics-total-views`
  - Unique visitors display: id=`analytics-unique-visitors`
  - Back to Article button: id=`back-to-article-analytics`
- Navigation:
  - Back button links to `/article/<article_id>/edit` or relevant article page

---

## Section 3: Data File Schemas

### 1. users.txt
- Fields (pipe-delimited):
  1. `username` (str): Unique user identifier
  2. `email` (str): User email address
  3. `fullname` (str): Full name of the user
  4. `created_date` (date, YYYY-MM-DD): User creation date
- Example:
  ```
john|john@example.com|John Doe|2024-01-15
alice|alice@example.com|Alice Smith|2024-01-16
bob|bob@example.com|Bob Johnson|2024-01-17
admin|admin@example.com|Admin User|2024-01-10
  ```

### 2. articles.txt
- Fields (pipe-delimited):
  1. `article_id` (int): Unique article identifier
  2. `title` (str): Article title
  3. `author` (str): Author's username
  4. `category` (str): One of `news`, `blog`, `tutorial`, `announcement`, `press_release`
  5. `status` (str): One of `draft`, `pending_review`, `under_review`, `approved`, `published`, `rejected`, `archived`
  6. `tags` (str): Comma-separated tags
  7. `featured_image` (str): URL or path to image (can be empty)
  8. `meta_description` (str): Meta description for SEO
  9. `created_date` (date YYYY-MM-DD): Creation date
  10. `publish_date` (datetime YYYY-MM-DD HH:MM:SS or empty): Publish datetime
- Example:
  ```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
  ```

### 3. article_versions.txt
- Fields (pipe-delimited):
  1. `version_id` (int): Unique version identifier
  2. `article_id` (int): Associated article id
  3. `version_number` (int): Incremental version number
  4. `content` (str): Article content text
  5. `author` (str): Username who created version
  6. `created_date` (datetime YYYY-MM-DD HH:MM:SS): Version creation datetime
  7. `change_summary` (str): Short description of changes
- Example:
  ```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
  ```

### 4. approvals.txt
- Fields (pipe-delimited):
  1. `approval_id` (int): Unique approval record id
  2. `article_id` (int): Article associated
  3. `version_id` (int): Version approved/rejected
  4. `approver` (str): Username of approver
  5. `status` (str): One of `approved`, `rejected`, `revision_requested`
  6. `comments` (str): Approval comments
  7. `timestamp` (datetime YYYY-MM-DD HH:MM:SS): Approval action time
- Example:
  ```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
  ```

### 5. workflow_stages.txt
- Fields (pipe-delimited):
  1. `stage_id` (int): Unique stage identifier
  2. `category` (str): Article category this stage applies to
  3. `stage_name` (str): Name of the workflow stage
  4. `stage_order` (int): Order number in the workflow
  5. `is_required` (str): Either `yes` or `no`, indicating if stage is mandatory
- Example:
  ```
1|tutorial|Editor Review|1|yes
2|tutorial|Publisher Approval|2|yes
3|news|Editor Review|1|yes
4|announcement|Editor Review|1|yes
5|announcement|Publisher Approval|2|yes
  ```

### 6. comments.txt
- Fields (pipe-delimited):
  1. `comment_id` (int): Unique comment id
  2. `article_id` (int): Article associated
  3. `version_id` (int): Article version
  4. `user` (str): Username who commented
  5. `comment_text` (str): Comment content
  6. `timestamp` (datetime YYYY-MM-DD HH:MM:SS): Comment timestamp
- Example:
  ```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
  ```

### 7. analytics.txt
- Fields (pipe-delimited):
  1. `analytics_id` (int): Unique analytics record id
  2. `article_id` (int): Article associated
  3. `date` (date YYYY-MM-DD): Date of the analytics record
  4. `views` (int): Total views count
  5. `unique_visitors` (int): Unique visitor count
  6. `avg_time_seconds` (int): Average time spent on article (seconds)
  7. `shares` (int): Number of shares
- Example:
  ```
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
  ```

---

This design specification document completes all required components for backend routing, frontend templating, and data storage schema definitions for the ContentPublishingHub application.
