# ContentPublishingHub - Final Design Specification

---

## 1. Flask Routes, Templates, and Description

| Route                                  | HTTP Method(s) | Template File          | Description                                  |
|----------------------------------------|----------------|------------------------|----------------------------------------------|
| `/dashboard`                           | GET            | `dashboard.html`       | Main dashboard showing overview and navigation|
| `/article/create`                      | GET, POST      | `create_article.html`  | Editor page to create new articles            |
| `/article/<int:article_id>/edit`      | GET, POST      | `edit_article.html`    | Edit existing articles with version control   |
| `/article/<int:article_id>/versions`  | GET            | `version_history.html` | View all versions of an article, compare and restore|
| `/articles/mine`                      | GET            | `my_articles.html`     | List user's articles with filtering            |
| `/articles/published`                 | GET            | `published_articles.html`| Public-facing library of published articles |
| `/calendar`                          | GET, POST      | `content_calendar.html`| Content scheduling calendar                    |
| `/article/<int:article_id>/analytics`| GET            | `article_analytics.html`| Analytics dashboard for published articles   |

---

## 2. Pages and Key UI Elements

### 2.1 Dashboard Page
- Page container div: `dashboard-page`
- Welcome message: `welcome-message` (shows "Welcome, [username]!")
- Quick stats section: `quick-stats` (shows counts of drafts, published, pending review, etc.)
- Create Article button: `create-article-button` (triggers navigation to `/article/create`)
- Recent activity feed: `recent-activity` (lists recent edits, comments, approvals)

### 2.2 Create Article Page
- Page container div: `create-article-page`
- Article title input: `article-title` (text input)
- Content editor textarea: `article-content` (rich text editor or textarea)
- Save as Draft button: `save-draft-button` (POST to save article as draft)
- Cancel button: `cancel-button` (navigate back to `/dashboard` or previous page)

### 2.3 Edit Article Page
- Page container div: `edit-article-page`
- Article title input: `edit-article-title` (editable text input)
- Content editor textarea: `edit-article-content` (editable article body)
- Save New Version button: `save-version-button` (POST to create new version)
- Cancel button: `cancel-edit` (return to `/articles/mine` or previous page)

### 2.4 Article Version History Page
- Page container div: `version-history-page`
- Versions list: `versions-list` (table or list showing version number, date, author, change summary)
- Version comparison section: `version-comparison` (side-by-side or diff view of selected versions)
- Restore button(s): `restore-version-<version_number>` (button to restore a specific version)
- Back to Edit button: `back-to-edit-history` (navigates to `/article/<article_id>/edit`)

### 2.5 My Articles Page
- Page container div: `my-articles-page`
- Filter by status dropdown: `filter-article-status` (select dropdown with statuses: draft, pending_review, under_review, approved, published, rejected, archived)
- Articles table: `articles-table` (columns including title, status, category, publish date)
- Create New Article button: `create-new-article` (navigates to `/article/create`)
- Back to Dashboard button: `back-to-dashboard` (navigates to `/dashboard`)

### 2.6 Published Articles Page
- Page container div: `published-articles-page`
- Filter by category dropdown: `filter-published-category` (categories like news, blog, tutorial, announcement, press_release)
- Articles grid: `published-articles-grid` (cards with article title, image, excerpt)
- Sort by dropdown: `sort-published` (date ascending/descending, popularity, title A-Z/Z-A)
- Back to Dashboard button: `back-to-dashboard-published` (navigates to `/dashboard`)

### 2.7 Content Calendar Page
- Page container div: `calendar-page`
- Calendar view selector: `calendar-view` (select dropdown for day, week, month views)
- Calendar grid: `calendar-grid` (table or div representation showing scheduled publish dates with clickable events)
- Schedule button: `schedule-button` (opens modal or page to create or edit publication schedule)
- Back to Dashboard button: `back-to-dashboard-calendar` (navigates to `/dashboard`)

### 2.8 Article Analytics Page
- Page container div: `analytics-page`
- Analytics overview section: `analytics-overview` (summary of analytics data)
- Total views label: `analytics-total-views` (span with total views count)
- Unique visitors label: `analytics-unique-visitors` (span with unique visitors count)
- Back to Article button: `back-to-article-analytics` (returns to `/article/<article_id>/edit` or previous page)

---

## 3. Data Storage Formats (UTF-8 Plain Text Files in `data/` Directory)

### 3.1 users.txt
- Fields:
  - `username|email|fullname|created_date`
- Description:
  - username: unique user ID
  - email: user's email
  - fullname: full name
  - created_date: YYYY-MM-DD
- Example:
  ```
  john|john@example.com|John Doe|2024-01-15
  alice|alice@example.com|Alice Smith|2024-01-16
  bob|bob@example.com|Bob Johnson|2024-01-17
  admin|admin@example.com|Admin User|2024-01-10
  ```

### 3.2 articles.txt
- Fields:
  - `article_id|title|author|category|status|tags|featured_image|meta_description|created_date|publish_date`
- Description:
  - article_id: integer unique ID
  - title: article title
  - author: username
  - category: news, blog, tutorial, announcement, press_release
  - status: draft, pending_review, under_review, approved, published, rejected, archived
  - tags: comma separated keywords
  - featured_image: path or blank
  - meta_description: short summary
  - created_date: ISO timestamp (YYYY-MM-DD HH:MM:SS)
  - publish_date: ISO timestamp or blank for unscheduled
- Example:
  ```
  1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
  2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
  3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
  ```

### 3.3 article_versions.txt
- Fields:
  - `version_id|article_id|version_number|content|author|created_date|change_summary`
- Description:
  - version_id: unique version record ID
  - article_id: references articles.txt
  - version_number: integer sequence
  - content: full article body text (pipe characters escaped as needed)
  - author: username who edited
  - created_date: ISO timestamp
  - change_summary: brief description of change
- Example:
  ```
  1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
  2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
  3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
  ```

### 3.4 approvals.txt
- Fields:
  - `approval_id|article_id|version_id|approver|status|comments|timestamp`
- Description:
  - approval_id: unique approval record
  - article_id: linked to article
  - version_id: linked to article version
  - approver: username
  - status: approved, rejected, revision_requested
  - comments: approver remarks
  - timestamp: ISO datetime
- Example:
  ```
  1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
  2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
  3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
  ```

### 3.5 workflow_stages.txt
- Fields:
  - `stage_id|category|stage_name|stage_order|is_required`
- Description:
  - Defines editorial workflow stages per category
- Example:
  ```
  1|tutorial|Editor Review|1|yes
  2|tutorial|Publisher Approval|2|yes
  3|news|Editor Review|1|yes
  4|announcement|Editor Review|1|yes
  5|announcement|Publisher Approval|2|yes
  ```

### 3.6 comments.txt
- Fields:
  - `comment_id|article_id|version_id|user|comment_text|timestamp`
- Description:
  - Comments linked to article and version
- Example:
  ```
  1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
  2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
  3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
  ```

### 3.7 analytics.txt
- Fields:
  - `analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares`
- Description:
  - Aggregated article engagement metrics
- Example:
  ```
  1|1|2024-01-22|150|120|245|12
  2|1|2024-01-23|230|180|210|18
  3|1|2024-01-24|180|140|220|15
  4|2|2024-01-25|95|75|180|8
  ```

---

## 4. Detailed User Workflows

### 4.1 Creating an Article
1. User clicks `create-article-button` on Dashboard or `create-new-article` on My Articles.
2. Navigates to `/article/create` to fill in article title and content.
3. On Save as Draft (`save-draft-button` click), backend:
   - Assigns new incremental `article_id`.
   - Saves article metadata with status `draft` in `articles.txt`.
   - Creates initial version with `version_number=1` in `article_versions.txt`.
4. User redirected to My Articles page.

### 4.2 Editing an Article
1. User selects article on My Articles and navigates to `/article/<article_id>/edit`.
2. Loads latest version content.
3. User modifies title and content.
4. On Save New Version (`save-version-button`), backend:
   - Increments version number.
   - Saves new version record in `article_versions.txt`.
   - Updates metadata in `articles.txt` if title or other fields change.
5. Cancel (`cancel-edit`) returns to My Articles.

### 4.3 Version History and Restore
1. User visits `/article/<article_id>/versions`.
2. Versions list shown with detailed metadata.
3. User can select two versions to compare side-by-side.
4. Clicking Restore (`restore-version-<version_number>`) creates a new version duplicating selected content.
5. Returns user to edit page for further editing.

### 4.4 Editorial Approval Process
1. Articles in status `pending_review` undergo editorial checks.
2. Approvals or rejections saved in `approvals.txt` with comments.
3. Comments added in `comments.txt` linked to article versions.
4. Status transitions: `pending_review` → `approved` or `rejected` or `revision_requested`.

### 4.5 Publishing and Scheduling
1. Approved articles can be scheduled on Content Calendar page.
2. Scheduling updates `publish_date` field in `articles.txt`.
3. At publish date/time, status updates to `published`.
4. Published articles appear in Published Articles page.

### 4.6 Content Analytics
1. User visits `/article/<article_id>/analytics` for published articles.
2. Displays aggregated metrics from `analytics.txt`:
   - Total views, unique visitors, average reading time, shares
3. Analytics overview section presents data visually.

---

## 5. UI Element and Interaction Notes

- All page containers uniquely identified for Reactivity and scripting.
- Buttons trigger HTTP POST requests as appropriate.
- Dropdowns filter and sort content with backend support, reloading or AJAX.
- Version comparison supports selection and side-by-side highlighting.
- Restore buttons suffixed by version number for clarity.
- Dates and timestamps follow ISO 8601 format.
- User authentication and session management is assumed but out of scope.
- Comment and approval lists can be loaded asynchronously.

---

This comprehensive specification integrates design candidates A and B, fulfilling all outlined requirements for the ContentPublishingHub Flask web application.