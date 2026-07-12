# ContentPublishingHub Design Specification

---

## Section 1: Flask Routes Specification

---

### Route: /dashboard
- Methods: GET
- Function Name: dashboard
- Template: dashboard.html
- Context Variables:
  - username: str (current logged-in user's username)
  - quick_stats: dict (overview stats data to display)
  - recent_activities: list of dict (recent activity feed entries)

---

### Route: /article/create
- Methods: GET, POST
- Function Name: create_article
- Template: create_article.html
- Context Variables (GET): None (empty form)
- POST: Process form submission to create article draft

---

### Route: /article/<article_id>/edit
- Methods: GET, POST
- Function Name: edit_article
- Template: edit_article.html
- Context Variables (GET):
  - article_id: int
  - article_title: str
  - article_content: str
- POST: Process form submission to save new version

---

### Route: /article/<article_id>/versions
- Methods: GET
- Function Name: article_version_history
- Template: version_history.html
- Context Variables:
  - article_id: int
  - versions: list of dict (each with version details: version_id, version_number, author, created_date, change_summary)
  - version_comparison_data: dict (optional data structure showing comparison between selected versions)

---

### Route: /articles/mine
- Methods: GET
- Function Name: my_articles
- Template: my_articles.html
- Context Variables:
  - articles: list of dict (articles belonging to current user)
  - filter_status_options: list of str (status filter values)

---

### Route: /articles/published
- Methods: GET
- Function Name: published_articles
- Template: published_articles.html
- Context Variables:
  - published_articles: list of dict (all published articles)
  - categories: list of str (available categories for filtering)
  - sort_options: list of str (sorting criteria)

---

### Route: /calendar
- Methods: GET
- Function Name: content_calendar
- Template: content_calendar.html
- Context Variables:
  - scheduled_articles: list of dict (articles with scheduling info)
  - calendar_views: list of str (view options: day, week, month)

---

### Route: /article/<article_id>/analytics
- Methods: GET
- Function Name: article_analytics
- Template: article_analytics.html
- Context Variables:
  - article_id: int
  - analytics_overview: dict (total views, unique visitors, etc.)

---

## Section 2: HTML Template Structure

---

### dashboard.html
- Page container id: `dashboard-page`
- Elements:
  - Welcome message id: `welcome-message`
  - Quick stats section id: `quick-stats`
  - Create Article button id: `create-article-button`
  - Recent activity feed id: `recent-activity`
- Navigation:
  - Create Article button links to `/article/create`
  - Other navigations to be included in app header/footer (not specified here)

---

### create_article.html
- Page container id: `create-article-page`
- Elements:
  - Input text field id: `article-title`
  - Textarea id: `article-content`
  - Button id: `save-draft-button`
  - Button id: `cancel-button`
- Navigation:
  - Cancel button returns to `/dashboard`

---

### edit_article.html
- Page container id: `edit-article-page`
- Elements:
  - Input text field id: `edit-article-title`
  - Textarea id: `edit-article-content`
  - Button id: `save-version-button`
  - Button id: `cancel-edit`
- Navigation:
  - Cancel button returns to `/articles/mine` or previous page

---

### version_history.html
- Page container id: `version-history-page`
- Elements:
  - Versions list container id: `versions-list`
  - Version comparison section id: `version-comparison`
  - Button id: `restore-version-1` (restore the selected version)
  - Button id: `back-to-edit-history`
- Navigation:
  - Back to Edit button returns to `/article/<article_id>/edit`

---

### my_articles.html
- Page container id: `my-articles-page`
- Elements:
  - Dropdown id: `filter-article-status`
  - Table id: `articles-table`
  - Button id: `create-new-article` (links to `/article/create`)
  - Button id: `back-to-dashboard`
- Navigation:
  - Back to Dashboard button returns to `/dashboard`

---

### published_articles.html
- Page container id: `published-articles-page`
- Elements:
  - Dropdown id: `filter-published-category`
  - Grid container id: `published-articles-grid`
  - Dropdown id: `sort-published`
  - Button id: `back-to-dashboard-published`
- Navigation:
  - Back to Dashboard button returns to `/dashboard`

---

### content_calendar.html
- Page container id: `calendar-page`
- Elements:
  - Selector dropdown id: `calendar-view`
  - Calendar grid id: `calendar-grid`
  - Button id: `schedule-button`
  - Button id: `back-to-dashboard-calendar`
- Navigation:
  - Back to Dashboard button returns to `/dashboard`

---

### article_analytics.html
- Page container id: `analytics-page`
- Elements:
  - Analytics overview container id: `analytics-overview`
  - Total views display id: `analytics-total-views`
  - Unique visitors display id: `analytics-unique-visitors`
  - Button id: `back-to-article-analytics`
- Navigation:
  - Back to Article button returns to `/article/<article_id>/edit` or read page

---

## Section 3: Data File Schemas

---

### users.txt
- Format: pipe-delimited
- Fields:
  1. username (str) - unique user identifier
  2. email (str) - user email address
  3. fullname (str) - full name of user
  4. created_date (date in YYYY-MM-DD) - account creation date
- Example Rows:
```
john|john@example.com|John Doe|2024-01-15
alice|alice@example.com|Alice Smith|2024-01-16
bob|bob@example.com|Bob Johnson|2024-01-17
admin|admin@example.com|Admin User|2024-01-10
```

---

### articles.txt
- Format: pipe-delimited
- Fields:
  1. article_id (int) - unique article identifier
  2. title (str) - article title
  3. author (str) - username of the article author
  4. category (str) - article category [news, blog, tutorial, announcement, press_release]
  5. status (str) - article status [draft, pending_review, under_review, approved, published, rejected, archived]
  6. tags (str) - comma-separated tags
  7. featured_image (str) - image path (empty if none)
  8. meta_description (str) - SEO description
  9. created_date (date in YYYY-MM-DD)
  10. publish_date (datetime in YYYY-MM-DD HH:MM:SS) (empty if not published)
- Example Rows:
```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
```

---

### article_versions.txt
- Format: pipe-delimited
- Fields:
  1. version_id (int) - unique version identifier
  2. article_id (int) - associated article id
  3. version_number (int) - sequential version number
  4. content (str) - full article content text
  5. author (str) - username who made version
  6. created_date (datetime YYYY-MM-DD HH:MM:SS) - version creation timestamp
  7. change_summary (str) - description of changes
- Example Rows:
```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
```

---

### approvals.txt
- Format: pipe-delimited
- Fields:
  1. approval_id (int) - unique approval record identifier
  2. article_id (int) - article id for approval
  3. version_id (int) - associated version id
  4. approver (str) - username of approver
  5. status (str) - approval status [approved, rejected, revision_requested]
  6. comments (str) - approval remarks
  7. timestamp (datetime YYYY-MM-DD HH:MM:SS) - approval time
- Example Rows:
```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
```

---

### workflow_stages.txt
- Format: pipe-delimited
- Fields:
  1. stage_id (int) - unique stage identifier
  2. category (str) - article category
  3. stage_name (str) - name of workflow stage
  4. stage_order (int) - order of this stage in workflow
  5. is_required (str) - yes/no flag if required
- Example Rows:
```
1|tutorial|Editor Review|1|yes
2|tutorial|Publisher Approval|2|yes
3|news|Editor Review|1|yes
4|announcement|Editor Review|1|yes
5|announcement|Publisher Approval|2|yes
```

---

### comments.txt
- Format: pipe-delimited
- Fields:
  1. comment_id (int) - unique comment identifier
  2. article_id (int) - article id
  3. version_id (int) - article version id
  4. user (str) - username of commenter
  5. comment_text (str) - text of comment
  6. timestamp (datetime YYYY-MM-DD HH:MM:SS) - time posted
- Example Rows:
```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
```

---

### analytics.txt
- Format: pipe-delimited
- Fields:
  1. analytics_id (int) - unique analytics record
  2. article_id (int) - associated article id
  3. date (date YYYY-MM-DD) - date of the analytics record
  4. views (int) - number of views
  5. unique_visitors (int) - number of unique visitors
  6. avg_time_seconds (int) - average time spent in seconds
  7. shares (int) - social shares count
- Example Rows:
```
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
```

---

End of Design Specification
