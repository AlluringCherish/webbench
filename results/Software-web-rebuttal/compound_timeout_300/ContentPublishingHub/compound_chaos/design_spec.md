# ContentPublishingHub Web Application Design Specification

## 1. Flask Routes Specification

| Route                             | HTTP Methods | Handler Function Name        | Template               | Context Variables
|----------------------------------|--------------|-----------------------------|------------------------|------------------
| `/dashboard`                     | GET          | dashboard                   | dashboard.html         | username: str, quick_stats: dict, recent_activity: list
| `/article/create`                | GET, POST    | create_article              | create_article.html    | (GET) -, (POST) form data and submission status
| `/article/<article_id>/edit`    | GET, POST    | edit_article                | edit_article.html      | article_title: str, article_content: str
| `/article/<article_id>/versions`| GET          | article_versions            | version_history.html   | versions_list: list
| `/articles/mine`                | GET          | my_articles                 | my_articles.html       | articles_list: list, filter_status: str
| `/articles/published`           | GET          | published_articles          | published_articles.html| filter_category: str, published_articles_grid: list, sort_order: str
| `/calendar`                    | GET          | content_calendar            | content_calendar.html  | calendar_view: str, calendar_grid: list
| `/article/<article_id>/analytics`| GET         | article_analytics           | article_analytics.html | analytics_overview: dict


## 2. HTML Template Structure

### dashboard.html
- Container element ID: `dashboard-page`
- Element IDs:
  - `welcome-message` (span or div for username greeting)
  - `quick-stats` (section for displaying key metrics)
  - `create-article-button` (button to navigate to article creation route)
  - `recent-activity` (list or feed of recent user activities)

### create_article.html
- Container ID: `create-article-page`
- Elements:
  - `article-title` (input text for article title)
  - `article-content` (textarea for article body)
  - `save-draft-button` (button for saving draft)
  - `cancel-button` (button to cancel creation and navigate away)

### edit_article.html
- Container ID: `edit-article-page`
- Elements:
  - `edit-article-title` (input text for editing title)
  - `edit-article-content` (textarea for editing article content)
  - `save-version-button` (button to save new version)
  - `cancel-edit` (button to cancel editing and return)

### version_history.html
- Container ID: `version-history-page`
- Elements:
  - `versions-list` (list or table of article versions)
  - `version-comparison` (element to show comparison of versions)
  - `restore-version-1` (button to restore selected previous version)
  - `back-to-edit-history` (button or link to return to article edit page)

### my_articles.html
- Container ID: `my-articles-page`
- Elements:
  - `filter-article-status` (dropdown for filtering articles by status)
  - `articles-table` (table listing articles with metadata)
  - `create-new-article` (button linking to create article page)
  - `back-to-dashboard` (button or link to return to dashboard)

### published_articles.html
- Container ID: `published-articles-page`
- Elements:
  - `filter-published-category` (dropdown for category filtering)
  - `published-articles-grid` (grid or list displaying articles)
  - `sort-published` (dropdown to change sorting order)
  - `back-to-dashboard-published` (button or link back to dashboard)

### content_calendar.html
- Container ID: `calendar-page`
- Elements:
  - `calendar-view` (selector for calendar view mode)
  - `calendar-grid` (calendar display container)
  - `schedule-button` (button for scheduling content)
  - `back-to-dashboard-calendar` (navigation button to dashboard)

### article_analytics.html
- Container ID: `analytics-page`
- Elements:
  - `analytics-overview` (section summarizing analytics metrics)
  - `analytics-total-views` (display for total views)
  - `analytics-unique-visitors` (display for unique visitors)
  - `back-to-article-analytics` (button to go back to article detail)


## 3. Data File Schemas

### users.txt
- Fields (pipe delimited): `username|email|fullname|created_date`
- Types:
  - username: string
  - email: string
  - fullname: string
  - created_date: date (YYYY-MM-DD)
- Example:
  ```
  john|john@example.com|John Doe|2024-01-15
  alice|alice@example.com|Alice Smith|2024-01-16
  bob|bob@example.com|Bob Johnson|2024-01-17
  admin|admin@example.com|Admin User|2024-01-10
  ```

### articles.txt
- Fields: `article_id|title|author|category|status|tags|featured_image|meta_description|created_date|publish_date`
- Types:
  - article_id: string
  - title: string
  - author: username string
  - category: string (news, blog, tutorial, announcement, press_release)
  - status: string (draft, pending_review, under_review, approved, published, rejected, archived)
  - tags: comma-separated string
  - featured_image: string (URL or file path, can be empty)
  - meta_description: string
  - created_date: datetime (YYYY-MM-DD HH:MM:SS)
  - publish_date: datetime (YYYY-MM-DD HH:MM:SS) or empty
- Example:
  ```
  1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
  2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
  3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
  ```

### article_versions.txt
- Fields: `version_id|article_id|version_number|content|author|created_date|change_summary`
- Types:
  - version_id: string
  - article_id: string
  - version_number: integer
  - content: string
  - author: string (username)
  - created_date: datetime
  - change_summary: string
- Example:
  ```
  1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
  2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
  3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
  ```

### approvals.txt
- Fields: `approval_id|article_id|version_id|approver|status|comments|timestamp`
- Types:
  - approval_id: string
  - article_id: string
  - version_id: string
  - approver: string (username)
  - status: string (approved, rejected, revision_requested)
  - comments: string
  - timestamp: datetime
- Example:
  ```
  1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
  2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
  3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
  ```

### workflow_stages.txt
- Fields: `stage_id|category|stage_name|stage_order|is_required`
- Types:
  - stage_id: string
  - category: string
  - stage_name: string
  - stage_order: integer
  - is_required: string ("yes" or "no")
- Example:
  ```
  1|tutorial|Editor Review|1|yes
  2|tutorial|Publisher Approval|2|yes
  3|news|Editor Review|1|yes
  4|announcement|Editor Review|1|yes
  5|announcement|Publisher Approval|2|yes
  ```

### comments.txt
- Fields: `comment_id|article_id|version_id|user|comment_text|timestamp`
- Types:
  - comment_id: string
  - article_id: string
  - version_id: string
  - user: string (username)
  - comment_text: string
  - timestamp: datetime
- Example:
  ```
  1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
  2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
  3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
  ```

### analytics.txt
- Fields: `analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares`
- Types:
  - analytics_id: string
  - article_id: string
  - date: date
  - views: integer
  - unique_visitors: integer
  - avg_time_seconds: integer
  - shares: integer
- Example:
  ```
  1|1|2024-01-22|150|120|245|12
  2|1|2024-01-23|230|180|210|18
  3|1|2024-01-24|180|140|220|15
  4|2|2024-01-25|95|75|180|8
  ```

---

*This design specification enables backend and frontend developers to implement all components independently, following exact route URLs, element IDs, and data file formats as per the requirements.*
