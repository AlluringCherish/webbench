# ContentPublishingHub Design Specification

---

## Section 1: Flask Routes Specification

| Route Pattern                      | HTTP Method(s) | Function Name             | Template Rendered        | Context Variables Passed to Template                                                                                               |
|----------------------------------|----------------|---------------------------|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| `/dashboard`                     | GET            | dashboard                 | dashboard.html           | `username` (str): logged-in user's username
`quick_stats` (dict): stats for quick overview
`recent_activity` (list): recent activities as list of dicts |
| `/article/create`                | GET, POST      | create_article            | create_article.html      | GET: No contextual variables except defaults
POST: On validation error, form data back for user input preservation
`
`|
| `/article/<article_id>/edit`    | GET, POST      | edit_article              | edit_article.html        | GET: `article` (dict): article data, `version` (dict): latest article version
POST: On validation error, form data back                                                                |
| `/article/<article_id>/versions`| GET            | view_article_versions     | version_history.html     | `article` (dict): article metadata
`versions` (list): list of version dicts
`comparison` (dict): diff or comparison details between versions if any |
| `/articles/mine`                | GET            | my_articles               | my_articles.html         | `user_articles` (list): list of articles by user
`filter_status_options` (list): available status filters                                                                             |
| `/articles/published`           | GET            | published_articles        | published_articles.html  | `published_articles` (list): list of published articles
`category_filters` (list): category filter options
`sort_options` (list): sorting options                                                     |
| `/calendar`                    | GET, POST      | content_calendar          | content_calendar.html    | `calendar_data` (dict): scheduled events data
`view_options` (list): available calendar views                                                                                            |
| `/article/<article_id>/analytics`| GET          | article_analytics         | article_analytics.html   | `article` (dict): article metadata
`analytics` (dict): aggregated analytics data                                                                                                     |

---

## Section 2: HTML Template Structure

### 1. dashboard.html
- Page container id: `dashboard-page`
- Elements:
  - `welcome-message` (displays welcome text with username)
  - `quick-stats` (shows summary statistics)
  - `create-article-button` (button to navigate to article creation page)
  - `recent-activity` (list or feed of recent activities)

### 2. create_article.html
- Page container id: `create-article-page`
- Elements:
  - `article-title` (text input for article title)
  - `article-content` (textarea for article content)
  - `save-draft-button` (button to save article as draft)
  - `cancel-button` (button to cancel and navigate back)

### 3. edit_article.html
- Page container id: `edit-article-page`
- Elements:
  - `edit-article-title` (text input for editing title)
  - `edit-article-content` (textarea for editing content)
  - `save-version-button` (button to save new version)
  - `cancel-edit` (button to cancel editing)

### 4. version_history.html
- Page container id: `version-history-page`
- Elements:
  - `versions-list` (list or table showing versions of the article)
  - `version-comparison` (section showing differences between selected versions)
  - `restore-version-1` (button to restore selected version - the number suffix changes dynamically depending on selection but this ID is mandatory for restore button)
  - `back-to-edit-history` (button to go back to edit page)

### 5. my_articles.html
- Page container id: `my-articles-page`
- Elements:
  - `filter-article-status` (dropdown to filter articles by status)
  - `articles-table` (table listing user’s articles)
  - `create-new-article` (button to create new article)
  - `back-to-dashboard` (button to return to dashboard)

### 6. published_articles.html
- Page container id: `published-articles-page`
- Elements:
  - `filter-published-category` (dropdown to filter published articles by category)
  - `published-articles-grid` (grid layout showing published articles)
  - `sort-published` (dropdown to sort published articles by various criteria)
  - `back-to-dashboard-published` (button to return to dashboard)

### 7. content_calendar.html
- Page container id: `calendar-page`
- Elements:
  - `calendar-view` (selector dropdown for different calendar views - daily, weekly, monthly)
  - `calendar-grid` (grid representing the calendar timeline)
  - `schedule-button` (button to add/schedule content publication)
  - `back-to-dashboard-calendar` (button to return to dashboard)

### 8. article_analytics.html
- Page container id: `analytics-page`
- Elements:
  - `analytics-overview` (section summarizing analytics)
  - `analytics-total-views` (display total views count)
  - `analytics-unique-visitors` (display unique visitors count)
  - `back-to-article-analytics` (button to return back to article details or analytics page)

---

## Section 3: Data File Schemas

### 1. users.txt
- **Format:** `username|email|fullname|created_date`
- **Fields:**
  - `username` (string): unique user login name
  - `email` (string): user's email address
  - `fullname` (string): full name of the user
  - `created_date` (date YYYY-MM-DD): account creation date
- **Example:**
```
john|john@example.com|John Doe|2024-01-15
alice|alice@example.com|Alice Smith|2024-01-16
bob|bob@example.com|Bob Johnson|2024-01-17
admin|admin@example.com|Admin User|2024-01-10
```

### 2. articles.txt
- **Format:** `article_id|title|author|category|status|tags|featured_image|meta_description|created_date|publish_date`
- **Fields:**
  - `article_id` (int): unique identifier for the article
  - `title` (string): article title
  - `author` (string): author's username
  - `category` (string): one of `news`, `blog`, `tutorial`, `announcement`, `press_release`
  - `status` (string): one of `draft`, `pending_review`, `under_review`, `approved`, `published`, `rejected`, `archived`
  - `tags` (string): comma separated tags
  - `featured_image` (string): URL or path to featured image (empty if none)
  - `meta_description` (string): short meta description
  - `created_date` (date YYYY-MM-DD): creation date
  - `publish_date` (datetime YYYY-MM-DD HH:mm:ss): scheduled or actual publish time (empty if not published)
- **Example:**
```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
```

### 3. article_versions.txt
- **Format:** `version_id|article_id|version_number|content|author|created_date|change_summary`
- **Fields:**
  - `version_id` (int): unique version identifier
  - `article_id` (int): article identifier this version belongs to
  - `version_number` (int): incremental version number
  - `content` (string): full versioned content (text)
  - `author` (string): username of creator of this version
  - `created_date` (datetime YYYY-MM-DD HH:mm:ss): timestamp of creation
  - `change_summary` (string): short description of changes in this version
- **Example:**
```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
```

### 4. approvals.txt
- **Format:** `approval_id|article_id|version_id|approver|status|comments|timestamp`
- **Fields:**
  - `approval_id` (int): unique approval record identifier
  - `article_id` (int): article associated
  - `version_id` (int): article version approved/rejected
  - `approver` (string): username of the approver
  - `status` (string): one of `approved`, `rejected`, `revision_requested`
  - `comments` (string): textual comments from approver
  - `timestamp` (datetime YYYY-MM-DD HH:mm:ss): time of approval action
- **Example:**
```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
```

### 5. workflow_stages.txt
- **Format:** `stage_id|category|stage_name|stage_order|is_required`
- **Fields:**
  - `stage_id` (int): unique stage identifier
  - `category` (string): article category this stage applies to
  - `stage_name` (string): descriptive name of workflow stage
  - `stage_order` (int): sequential ordering number
  - `is_required` (string): 'yes' or 'no' whether stage is mandatory
- **Example:**
```
1|tutorial|Editor Review|1|yes
2|tutorial|Publisher Approval|2|yes
3|news|Editor Review|1|yes
4|announcement|Editor Review|1|yes
5|announcement|Publisher Approval|2|yes
```

### 6. comments.txt
- **Format:** `comment_id|article_id|version_id|user|comment_text|timestamp`
- **Fields:**
  - `comment_id` (int): unique comment identifier
  - `article_id` (int): article associated
  - `version_id` (int): version of article commented on
  - `user` (string): username who commented
  - `comment_text` (string): textual comment content
  - `timestamp` (datetime YYYY-MM-DD HH:mm:ss): time comment was made
- **Example:**
```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
```

### 7. analytics.txt
- **Format:** `analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares`
- **Fields:**
  - `analytics_id` (int): unique analytics record
  - `article_id` (int): article being analyzed
  - `date` (date YYYY-MM-DD): date data recorded
  - `views` (int): total page views
  - `unique_visitors` (int): count of unique visitors
  - `avg_time_seconds` (int): average time spent on page in seconds
  - `shares` (int): number of shares across platforms
- **Example:**
```
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
```

---

This specification is designed to fully delineate Flask routes, front-end template elements, and data formats to support independent implementation by back-end and front-end developers without ambiguity.