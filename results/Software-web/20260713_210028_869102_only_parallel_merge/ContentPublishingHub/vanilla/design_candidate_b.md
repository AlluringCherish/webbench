# ContentPublishingHub - Design Candidate B

---

## Overview
ContentPublishingHub is a Flask-based web application enabling collaborative content creation, version-controlled editorial workflows, content scheduling, and analytics tracking. This design covers all pages, Flask routes, UI components IDs and types, data storage formats, and detailed user workflows.

---

# 1. Pages and Routes

## 1.1 Dashboard Page
- **Route:** `/dashboard` (GET)
- **Template:** `dashboard.html`
- **Purpose:** Landing page summarizes user content and activity
- 
### UI Elements
| Element Description         | Element ID           | Type            |
|-----------------------------|----------------------|-----------------|
| Page container              | `dashboard-page`     | `<div>`         |
| Welcome message             | `welcome-message`    | `<h2>`          |
| Quick stats section         | `quick-stats`        | `<section>`     |
| Create Article button       | `create-article-button`| `<button>`    |
| Recent activity feed        | `recent-activity`    | `<ul>` or `<div>`|

### Workflow
- On login, user directed here.
- Display user name from session.
- Show latest stats: total articles, drafts, published, awaiting reviews.
- Quick access to article creation and recent editorial activities.


## 1.2 Create Article Page
- **Route:** `/article/create` (GET, POST)
- **Template:** `create_article.html`
- **Purpose:** Editor interface to compose new articles

### UI Elements
| Element Description         | Element ID           | Type          |
|-----------------------------|----------------------|---------------|
| Page container              | `create-article-page` | `<div>`      |
| Article title input         | `article-title`       | `<input type=text>` |
| Content editor textarea     | `article-content`     | `<textarea>` |
| Save as Draft button        | `save-draft-button`   | `<button>`    |
| Cancel button               | `cancel-button`       | `<button>`    |

### Workflow
- GET: Render blank form.
- POST: Save article metadata with status="draft" and initial version in `article_versions.txt`.
- Redirect to My Articles or Dashboard on cancel.


## 1.3 Edit Article Page
- **Route:** `/article/<article_id>/edit` (GET, POST)
- **Template:** `edit_article.html`
- **Purpose:** Edit existing article, save new versions

### UI Elements
| Element Description         | Element ID           | Type          |
|-----------------------------|----------------------|---------------|
| Page container              | `edit-article-page`   | `<div>`      |
| Article title input         | `edit-article-title`  | `<input type=text>` |
| Content editor textarea     | `edit-article-content`| `<textarea>` |
| Save New Version button     | `save-version-button` | `<button>`    |
| Cancel button               | `cancel-edit`         | `<button>`    |

### Workflow
- GET: Load latest article version.
- POST: Save new version with incremented version number.
- Update `articles.txt` if needed metadata changed.
- Redirect accordingly.


## 1.4 Article Version History Page
- **Route:** `/article/<article_id>/versions` (GET)
- **Template:** `version_history.html`
- **Purpose:** Review, compare, and restore past versions

### UI Elements
| Element Description          | Element ID           | Type         |
|------------------------------|----------------------|--------------|
| Page container               | `version-history-page`| `<div>`     |
| Versions list                | `versions-list`       | `<ul>` or `<table>` |
| Version comparison section   | `version-comparison`  | `<div>`     |
| Restore button               | `restore-version-1`   | `<button>`  | <!-- ID suffixed by version number, example here is version 1 -->
| Back to Edit button          | `back-to-edit-history`| `<button>`  |

### Workflow
- Display all versions with metadata.
- Allow selection of two versions to compare side-by-side.
- Restore button enabled on selected version to overwrite current.


## 1.5 My Articles Page
- **Route:** `/articles/mine` (GET)
- **Template:** `my_articles.html`
- **Purpose:** List user's authored articles, filter by status

### UI Elements
| Element Description         | Element ID           | Type         |
|-----------------------------|----------------------|--------------|
| Page container              | `my-articles-page`    | `<div>`     |
| Filter by status dropdown   | `filter-article-status`| `<select>` |
| Articles table              | `articles-table`      | `<table>`   |
| Create New Article button   | `create-new-article`  | `<button>`  |
| Back to Dashboard button    | `back-to-dashboard`   | `<button>`  |

### Workflow
- Load user's articles from `articles.txt`.
- Filter options: draft, pending_review, under_review, approved, published, rejected, archived
- Clicking article row navigates to Edit Page.


## 1.6 Published Articles Page
- **Route:** `/articles/published` (GET)
- **Template:** `published_articles.html`
- **Purpose:** Public-facing content library

### UI Elements
| Element Description         | Element ID              | Type        |
|-----------------------------|-------------------------|-------------|
| Page container              | `published-articles-page`| `<div>`    |
| Filter by category dropdown | `filter-published-category`| `<select>`|
| Articles grid               | `published-articles-grid`| `<div>` (grid styled) |
| Sort by dropdown            | `sort-published`        | `<select>`  |
| Back to Dashboard button    | `back-to-dashboard-published` | `<button>` |

### Workflow
- Show only articles with status = 'published'.
- Filter by category: news, blog, tutorial, announcement, press_release
- Sort options: date ascending/descending, title A-Z/Z-A
- Clicking an article opens detailed view (route not specified, assumes external/public page).


## 1.7 Content Calendar Page
- **Route:** `/calendar` (GET, POST)
- **Template:** `content_calendar.html`
- **Purpose:** Timeline view of scheduled publications

### UI Elements
| Element Description         | Element ID             | Type         |
|-----------------------------|------------------------|--------------|
| Page container              | `calendar-page`         | `<div>`     |
| Calendar view selector      | `calendar-view`         | `<select>`  |
| Calendar grid              | `calendar-grid`          | `<table>` or `<div>` calendar  |
| Schedule button             | `schedule-button`       | `<button>`  |
| Back to Dashboard button    | `back-to-dashboard-calendar`| `<button>`|

### Workflow
- GET: Show calendar with articles marked on their `publish_date`.
- POST: Allow scheduling or rescheduling publication dates.


## 1.8 Article Analytics Page
- **Route:** `/article/<article_id>/analytics` (GET)
- **Template:** `article_analytics.html`
- **Purpose:** Show engagement metrics for an article

### UI Elements
| Element Description         | Element ID             | Type           |
|-----------------------------|------------------------|----------------|
| Page container              | `analytics-page`         | `<div>`       |
| Analytics overview          | `analytics-overview`     | `<section>`   |
| Total views                | `analytics-total-views`   | `<span>`     |
| Unique visitors            | `analytics-unique-visitors`| `<span>`    |
| Back to Article button     | `back-to-article-analytics`| `<button>` |

### Workflow
- Show aggregated and per-day metrics from `analytics.txt`.
- Provide graphs and summary.

---

# 2. Data Storage
All data stored as UTF-8 encoded text files in `data/` directory.

## 2.1 `users.txt`
- Format:
```
username|email|fullname|created_date
```
- Example:
```
john|john@example.com|John Doe|2024-01-15
alice|alice@example.com|Alice Smith|2024-01-16
bob|bob@example.com|Bob Johnson|2024-01-17
admin|admin@example.com|Admin User|2024-01-10
```

## 2.2 `articles.txt`
- Format:
```
article_id|title|author|category|status|tags|featured_image|meta_description|created_date|publish_date
```
- Example:
```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
```

## 2.3 `article_versions.txt`
- Format:
```
version_id|article_id|version_number|content|author|created_date|change_summary
```
- Example:
```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
```

## 2.4 `approvals.txt`
- Format:
```
approval_id|article_id|version_id|approver|status|comments|timestamp
```
- Example:
```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
```
- Status values: `approved`, `rejected`, `revision_requested`

## 2.5 `workflow_stages.txt`
- Format:
```
stage_id|category|stage_name|stage_order|is_required
```
- Example:
```
1|tutorial|Editor Review|1|yes
2|tutorial|Publisher Approval|2|yes
3|news|Editor Review|1|yes
4|announcement|Editor Review|1|yes
5|announcement|Publisher Approval|2|yes
```

## 2.6 `comments.txt`
- Format:
```
comment_id|article_id|version_id|user|comment_text|timestamp
```
- Example:
```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
```

## 2.7 `analytics.txt`
- Format:
```
analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares
```
- Example:
```
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
```

---

# 3. Detailed User Workflows

## 3.1 Article Creation Workflow
1. User navigates from Dashboard or My Articles page using create article button.
2. Completes form with title and content.
3. On save draft, a new article ID is generated (incremental), new article record appended to `articles.txt` with status="draft".
4. Initial version entry is created in `article_versions.txt` with version_number=1.
5. User redirected to My Articles.

## 3.2 Article Editing and Versioning Workflow
1. User selects an article from My Articles to edit.
2. Edit page loads latest version content.
3. User modifies title and content.
4. On save, a new version number increments and saved to `article_versions.txt`.
5. If metadata changes (title, status, category, etc.), `articles.txt` updated.
6. Workflow stages can be evaluated from `workflow_stages.txt` based on category.

## 3.3 Editorial Comments and Approvals
1. Comments added with relation to article version, written to `comments.txt`.
2. Approvers review versions, record approvals or rejections in `approvals.txt`.
3. Status can be updated such as `pending_review -> approved` or `revision_requested`.
4. Notifications can be triggered in UI (not detailed here).

## 3.4 Version History and Restore
1. Users view all versions in version history page.
2. Select versions to compare content side-by-side.
3. Restore overwrites latest version with selected version's content, increments version number.

## 3.5 Content Scheduling
1. Users access Content Calendar page.
2. View articles on calendar by scheduled `publish_date`.
3. Schedule new publication date or reschedule existing articles with a date picker.
4. Save updates reflected in `articles.txt`'s `publish_date` field.

## 3.6 Analytics Viewing
1. Users select an article with status "published".
2. Visit analytics page to see metrics aggregated from `analytics.txt`.
3. View graphs and summaries for views, visitors, average time, shares.

---

# 4. Flask Template and Route Mapping

| Route                                  | HTTP Method(s) | Template File          | Description                 |
|--------------------------------------|----------------|------------------------|-----------------------------|
| `/dashboard`                         | GET            | `dashboard.html`       | Main dashboard page          |
| `/article/create`                    | GET, POST      | `create_article.html`  | Article creation editor      |
| `/article/<int:article_id>/edit`    | GET, POST      | `edit_article.html`    | Edit article page with versions |
| `/article/<int:article_id>/versions`| GET            | `version_history.html` | Show version history         |
| `/articles/mine`                    | GET            | `my_articles.html`     | User's authored articles     |
| `/articles/published`               | GET            | `published_articles.html`| Public published articles    |
| `/calendar`                        | GET, POST      | `content_calendar.html`| Content scheduling calendar  |
| `/article/<int:article_id>/analytics`| GET          | `article_analytics.html`| Analytics for article        |

---

# 5. UI Element Summary (IDs and Types)

| Page                           | Element ID                  | Type          |
|--------------------------------|-----------------------------|---------------|
| Dashboard                     | `dashboard-page`             | `<div>`       |
| Dashboard                     | `welcome-message`            | `<h2>`        |
| Dashboard                     | `quick-stats`                | `<section>`   |
| Dashboard                     | `create-article-button`      | `<button>`    |
| Dashboard                     | `recent-activity`            | `<ul>` or `<div>` |
| Create Article                | `create-article-page`        | `<div>`       |
| Create Article                | `article-title`              | `<input type=text>` |
| Create Article                | `article-content`            | `<textarea>`  |
| Create Article                | `save-draft-button`          | `<button>`    |
| Create Article                | `cancel-button`              | `<button>`    |
| Edit Article                  | `edit-article-page`          | `<div>`       |
| Edit Article                  | `edit-article-title`         | `<input type=text>` |
| Edit Article                  | `edit-article-content`       | `<textarea>`  |
| Edit Article                  | `save-version-button`        | `<button>`    |
| Edit Article                  | `cancel-edit`                | `<button>`    |
| Version History              | `version-history-page`       | `<div>`       |
| Version History              | `versions-list`              | `<ul>` or `<table>`|
| Version History              | `version-comparison`         | `<div>`       |
| Version History              | `restore-version-<version_number>` | `<button>` |
| Version History              | `back-to-edit-history`       | `<button>`    |
| My Articles                  | `my-articles-page`           | `<div>`       |
| My Articles                  | `filter-article-status`      | `<select>`    |
| My Articles                  | `articles-table`             | `<table>`     |
| My Articles                  | `create-new-article`         | `<button>`    |
| My Articles                  | `back-to-dashboard`          | `<button>`    |
| Published Articles          | `published-articles-page`    | `<div>`       |
| Published Articles          | `filter-published-category`  | `<select>`    |
| Published Articles          | `published-articles-grid`    | `<div>` (grid) |
| Published Articles          | `sort-published`             | `<select>`    |
| Published Articles          | `back-to-dashboard-published`| `<button>`    |
| Content Calendar            | `calendar-page`              | `<div>`       |
| Content Calendar            | `calendar-view`              | `<select>`    |
| Content Calendar            | `calendar-grid`              | `<div>` or `<table>` |
| Content Calendar            | `schedule-button`            | `<button>`    |
| Content Calendar            | `back-to-dashboard-calendar` | `<button>`   |
| Article Analytics           | `analytics-page`             | `<div>`       |
| Article Analytics           | `analytics-overview`         | `<section>`   |
| Article Analytics           | `analytics-total-views`      | `<span>`     |
| Article Analytics           | `analytics-unique-visitors`  | `<span>`     |
| Article Analytics           | `back-to-article-analytics`  | `<button>`    |

---

# 6. Additional Notes

- All textual data fields stored as UTF-8 strings in respective text files.
- Article content in `article_versions.txt` stored as plain text; consider escaping pipe `|` characters.
- IDs for restore buttons in version history are suffixed by version number for clarity (`restore-version-1`, `restore-version-2`, etc.).
- User session management and authentication not detailed but required in implementation.
- Scheduling dates use ISO 8601 format `YYYY-MM-DD HH:MM:SS`.
- Filtering and sorting implemented via query parameters on respective routes.
- Comments and approvals can be loaded asynchronously using AJAX for a richer UX.

---

This completes the design candidate B specification for ContentPublishingHub.

