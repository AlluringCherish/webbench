# ContentPublishingHub Web Application Requirements Analysis

## Pages

### 1. Dashboard Page
- Route: `/dashboard`
- Page Name: `dashboard.html`
- Purpose: Main landing page showing content overview and navigation
- Elements IDs:
  - `dashboard-page`
  - `welcome-message`
  - `quick-stats`
  - `create-article-button`
  - `recent-activity`

### 2. Create Article Page
- Route: `/article/create`
- Page Name: `create_article.html`
- Purpose: Editor for creating new articles
- Elements IDs:
  - `create-article-page`
  - `article-title`
  - `article-content`
  - `save-draft-button`
  - `cancel-button`

### 3. Edit Article Page
- Route: `/article/<article_id>/edit`
- Page Name: `edit_article.html`
- Purpose: Edit existing article with version tracking
- Elements IDs:
  - `edit-article-page`
  - `edit-article-title`
  - `edit-article-content`
  - `save-version-button`
  - `cancel-edit`

### 4. Article Version History Page
- Route: `/article/<article_id>/versions`
- Page Name: `version_history.html`
- Purpose: View all versions and restore previous versions
- Elements IDs:
  - `version-history-page`
  - `versions-list`
  - `version-comparison`
  - `restore-version-1`
  - `back-to-edit-history`

### 5. My Articles Page
- Route: `/articles/mine`
- Page Name: `my_articles.html`
- Purpose: List user's articles with filters
- Elements IDs:
  - `my-articles-page`
  - `filter-article-status`
  - `articles-table`
  - `create-new-article`
  - `back-to-dashboard`

### 6. Published Articles Page
- Route: `/articles/published`
- Page Name: `published_articles.html`
- Purpose: Public-facing content library
- Elements IDs:
  - `published-articles-page`
  - `filter-published-category`
  - `published-articles-grid`
  - `sort-published`
  - `back-to-dashboard-published`

### 7. Content Calendar Page
- Route: `/calendar`
- Page Name: `content_calendar.html`
- Purpose: Scheduled publications timeline view
- Elements IDs:
  - `calendar-page`
  - `calendar-view`
  - `calendar-grid`
  - `schedule-button`
  - `back-to-dashboard-calendar`

### 8. Article Analytics Page
- Route: `/article/<article_id>/analytics`
- Page Name: `article_analytics.html`
- Purpose: View engagement metrics for published article
- Elements IDs:
  - `analytics-page`
  - `analytics-overview`
  - `analytics-total-views`
  - `analytics-unique-visitors`
  - `back-to-article-analytics`

## Local Data Storage Formats

### 1. users.txt
- Format: `username|email|fullname|created_date`
- Field Descriptions:
  - username
  - email
  - fullname
  - created_date
- Example Data:
  ```
  john|john@example.com|John Doe|2024-01-15
  alice|alice@example.com|Alice Smith|2024-01-16
  bob|bob@example.com|Bob Johnson|2024-01-17
  admin|admin@example.com|Admin User|2024-01-10
  ```

### 2. articles.txt
- Format: `article_id|title|author|category|status|tags|featured_image|meta_description|created_date|publish_date`
- Field Descriptions:
  - article_id
  - title
  - author
  - category (news, blog, tutorial, announcement, press_release)
  - status (draft, pending_review, under_review, approved, published, rejected, archived)
  - tags
  - featured_image
  - meta_description
  - created_date
  - publish_date
- Example Data:
  ```
  1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
  2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
  3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
  ```

### 3. article_versions.txt
- Format: `version_id|article_id|version_number|content|author|created_date|change_summary`
- Field Descriptions:
  - version_id
  - article_id
  - version_number
  - content
  - author
  - created_date
  - change_summary
- Example Data:
  ```
  1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
  2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
  3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
  ```

### 4. approvals.txt
- Format: `approval_id|article_id|version_id|approver|status|comments|timestamp`
- Field Descriptions:
  - approval_id
  - article_id
  - version_id
  - approver
  - status (approved, rejected, revision_requested)
  - comments
  - timestamp
- Example Data:
  ```
  1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
  2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
  3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
  ```

### 5. workflow_stages.txt
- Format: `stage_id|category|stage_name|stage_order|is_required`
- Field Descriptions:
  - stage_id
  - category
  - stage_name
  - stage_order
  - is_required
- Example Data:
  ```
  1|tutorial|Editor Review|1|yes
  2|tutorial|Publisher Approval|2|yes
  3|news|Editor Review|1|yes
  4|announcement|Editor Review|1|yes
  5|announcement|Publisher Approval|2|yes
  ```

### 6. comments.txt
- Format: `comment_id|article_id|version_id|user|comment_text|timestamp`
- Field Descriptions:
  - comment_id
  - article_id
  - version_id
  - user
  - comment_text
  - timestamp
- Example Data:
  ```
  1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
  2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
  3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
  ```

### 7. analytics.txt
- Format: `analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares`
- Field Descriptions:
  - analytics_id
  - article_id
  - date
  - views
  - unique_visitors
  - avg_time_seconds
  - shares
- Example Data:
  ```
  1|1|2024-01-22|150|120|245|12
  2|1|2024-01-23|230|180|210|18
  3|1|2024-01-24|180|140|220|15
  4|2|2024-01-25|95|75|180|8
  ```
