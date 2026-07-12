# ContentPublishingHub Design Specification

---

## Section 1: Flask Routes Specification

| Route                                  | HTTP Method(s) | Function Name                | Template Rendered           | Context Variables Passed (name: type/structure)                              |
|----------------------------------------|----------------|------------------------------|-----------------------------|------------------------------------------------------------------------------|
| `/dashboard`                           | GET            | dashboard                    | dashboard.html              | username: str                                                                |
| `/article/create`                      | GET, POST      | create_article               | create_article.html          | (GET) None; (POST) form data processing result/context for reload             |
| `/article/<article_id>/edit`           | GET, POST      | edit_article                 | edit_article.html            | article_id: str or int; article: dict (fields: title:str, content:str, etc.)  |
| `/article/<article_id>/versions`       | GET            | version_history              | version_history.html         | article_id: str or int; versions: list of dicts                              |
| `/articles/mine`                      | GET            | my_articles                  | my_articles.html             | articles: list of dicts; user info if needed                                 |
| `/articles/published`                 | GET            | published_articles           | published_articles.html      | articles: list of dicts                                                       |
| `/calendar`                          | GET            | content_calendar             | content_calendar.html        | scheduled_publications: list or calendar data                                |
| `/article/<article_id>/analytics`      | GET            | article_analytics            | article_analytics.html       | analytics: dict; article_id: str/int                                         |

---

## Section 2: HTML Template Structure

### 1. dashboard.html
- Page container: id = `dashboard-page`
- Welcome message: id = `welcome-message`
- Quick stats section: id = `quick-stats`
- Create Article button: id = `create-article-button`
- Recent activity feed: id = `recent-activity`

Navigation includes link/button to create article, view my articles, published articles, content calendar.

### 2. create_article.html
- Page container: id = `create-article-page`
- Article title input: id = `article-title` (text input)
- Content editor textarea: id = `article-content`
- Save as Draft button: id = `save-draft-button`
- Cancel button: id = `cancel-button`

### 3. edit_article.html
- Page container: id = `edit-article-page`
- Article title input: id = `edit-article-title`
- Content editor textarea: id = `edit-article-content`
- Save New Version button: id = `save-version-button`
- Cancel button: id = `cancel-edit`

### 4. version_history.html
- Page container: id = `version-history-page`
- Versions list: id = `versions-list` (likely a list or table showing versions)
- Version comparison section: id = `version-comparison`
- Restore button: id = `restore-version-1` (assumed to be dynamically changed per version)
- Back to Edit button: id = `back-to-edit-history`

### 5. my_articles.html
- Page container: id = `my-articles-page`
- Filter by status dropdown: id = `filter-article-status`
- Articles table: id = `articles-table`
- Create New Article button: id = `create-new-article`
- Back to Dashboard button: id = `back-to-dashboard`

### 6. published_articles.html
- Page container: id = `published-articles-page`
- Filter by category dropdown: id = `filter-published-category`
- Articles grid: id = `published-articles-grid`
- Sort by dropdown: id = `sort-published`
- Back to Dashboard button: id = `back-to-dashboard-published`

### 7. content_calendar.html
- Page container: id = `calendar-page`
- Calendar view selector: id = `calendar-view`
- Calendar grid: id = `calendar-grid`
- Schedule button: id = `schedule-button`
- Back to Dashboard button: id = `back-to-dashboard-calendar`

### 8. article_analytics.html
- Page container: id = `analytics-page`
- Analytics overview section: id = `analytics-overview`
- Total views: id = `analytics-total-views`
- Unique visitors: id = `analytics-unique-visitors`
- Back to Article button: id = `back-to-article-analytics`

---

## Section 3: Data File Schemas

### 1. users.txt
- Fields (pipe-delimited): 
  1. username (str)
  2. email (str)
  3. fullname (str)
  4. created_date (YYYY-MM-DD string)
- Example:
```
john|john@example.com|John Doe|2024-01-15
alice|alice@example.com|Alice Smith|2024-01-16
bob|bob@example.com|Bob Johnson|2024-01-17
admin|admin@example.com|Admin User|2024-01-10
```

### 2. articles.txt
- Fields (pipe-delimited):
  1. article_id (int)
  2. title (str)
  3. author (username str)
  4. category (enum: news, blog, tutorial, announcement, press_release)
  5. status (enum: draft, pending_review, under_review, approved, published, rejected, archived)
  6. tags (comma-separated str list)
  7. featured_image (URL or file path str, optional)
  8. meta_description (str)
  9. created_date (YYYY-MM-DD string)
  10. publish_date (YYYY-MM-DD HH:MM:SS string, optional)
- Example:
```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
```

### 3. article_versions.txt
- Fields (pipe-delimited):
  1. version_id (int)
  2. article_id (int)
  3. version_number (int)
  4. content (str)
  5. author (username str)
  6. created_date (YYYY-MM-DD HH:MM:SS string)
  7. change_summary (str)
- Example:
```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
```

### 4. approvals.txt
- Fields (pipe-delimited):
  1. approval_id (int)
  2. article_id (int)
  3. version_id (int)
  4. approver (username str)
  5. status (enum: approved, rejected, revision_requested)
  6. comments (str)
  7. timestamp (YYYY-MM-DD HH:MM:SS string)
- Example:
```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
```

### 5. workflow_stages.txt
- Fields (pipe-delimited):
  1. stage_id (int)
  2. category (str)
  3. stage_name (str)
  4. stage_order (int)
  5. is_required (enum: yes, no)
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
  1. comment_id (int)
  2. article_id (int)
  3. version_id (int)
  4. user (username str)
  5. comment_text (str)
  6. timestamp (YYYY-MM-DD HH:MM:SS string)
- Example:
```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
```

### 7. analytics.txt
- Fields (pipe-delimited):
  1. analytics_id (int)
  2. article_id (int)
  3. date (YYYY-MM-DD string)
  4. views (int)
  5. unique_visitors (int)
  6. avg_time_seconds (int)
  7. shares (int)
- Example:
```
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
```

---

This design specification fully enables independent backend and frontend development for the ContentPublishingHub application as per the provided user requirements.