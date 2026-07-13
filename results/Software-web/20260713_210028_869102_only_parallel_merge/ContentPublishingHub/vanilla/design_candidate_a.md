# ContentPublishingHub Design Candidate A

---

## 1. Pages and Routing

### 1.1 Dashboard Page
- Route: `/dashboard`
- Template: `dashboard.html`
- Page Container ID: `dashboard-page`
- Key UI Elements:
  - Welcome message: id=`welcome-message` (displays "Welcome, [username]!")
  - Quick stats section: id=`quick-stats` (shows content counts — drafts, published, pending review)
  - Create Article button: id=`create-article-button` (navigates to `/article/create`)
  - Recent activity feed: id=`recent-activity` (lists recent edits, comments, approvals)

### 1.2 Create Article Page
- Route: `/article/create`
- Template: `create_article.html`
- Page Container ID: `create-article-page`
- Key UI Elements:
  - Article title input: id=`article-title` (text input for new title)
  - Content editor textarea: id=`article-content` (rich text area for article body)
  - Save as Draft button: id=`save-draft-button` (saves article with status `draft`)
  - Cancel button: id=`cancel-button` (returns to `/dashboard`)

### 1.3 Edit Article Page
- Route: `/article/<article_id>/edit`
- Template: `edit_article.html`
- Page Container ID: `edit-article-page`
- Key UI Elements:
  - Article title input: id=`edit-article-title` (editable title text input)
  - Content editor textarea: id=`edit-article-content` (editable article body)
  - Save New Version button: id=`save-version-button` (creates a new version in `article_versions.txt`)
  - Cancel button: id=`cancel-edit` (navigates back to `/articles/mine` or last page)

### 1.4 Article Version History Page
- Route: `/article/<article_id>/versions`
- Template: `version_history.html`
- Page Container ID: `version-history-page`
- Key UI Elements:
  - Versions list: id=`versions-list` (table or list showing all versions with version number, date, author, summary)
  - Version comparison section: id=`version-comparison` (side-by-side or diff view of selected versions)
  - Restore button: id=`restore-version-1` (button to restore selected version as current)
  - Back to Edit button: id=`back-to-edit-history` (returns to `/article/<article_id>/edit`)

### 1.5 My Articles Page
- Route: `/articles/mine`
- Template: `my_articles.html`
- Page Container ID: `my-articles-page`
- Key UI Elements:
  - Filter by status dropdown: id=`filter-article-status` (filter list by draft, pending_review, etc.)
  - Articles table: id=`articles-table` (shows article title, status, category, publish date)
  - Create New Article button: id=`create-new-article` (link to `/article/create`)
  - Back to Dashboard button: id=`back-to-dashboard` (link to `/dashboard`)

### 1.6 Published Articles Page
- Route: `/articles/published`
- Template: `published_articles.html`
- Page Container ID: `published-articles-page`
- Key UI Elements:
  - Filter by category dropdown: id=`filter-published-category` (categories like news, blog, tutorial)
  - Articles grid: id=`published-articles-grid` (cards with article title, image, excerpt)
  - Sort by dropdown: id=`sort-published` (sort by date, popularity)
  - Back to Dashboard button: id=`back-to-dashboard-published` (link to `/dashboard`)

### 1.7 Content Calendar Page
- Route: `/calendar`
- Template: `content_calendar.html`
- Page Container ID: `calendar-page`
- Key UI Elements:
  - Calendar view selector: id=`calendar-view` (day, week, month views)
  - Calendar grid: id=`calendar-grid` (displays scheduled publication dates with clickable events)
  - Schedule button: id=`schedule-button` (opens create or edit scheduling modal/page)
  - Back to Dashboard button: id=`back-to-dashboard-calendar` (link to `/dashboard`)

### 1.8 Article Analytics Page
- Route: `/article/<article_id>/analytics`
- Template: `article_analytics.html`
- Page Container ID: `analytics-page`
- Key UI Elements:
  - Analytics overview container: id=`analytics-overview` (summary of analytics data)
  - Total views: id=`analytics-total-views` (sum of views from analytics records)
  - Unique visitors: id=`analytics-unique-visitors` (sum or distinct unique visitors)
  - Back to Article button: id=`back-to-article-analytics` (returns to `/article/<article_id>/edit` or previous page)

---

## 2. UI Element Details

Each page's container id is the root for its content. All buttons, inputs, dropdowns as listed above have explicit element IDs to facilitate JavaScript interaction and backend form bindings.

- Buttons like `save-draft-button`, `save-version-button`, or `create-article-button` trigger POST requests to backend routes to write or update records.
- Dropdowns filter articles or change views and update content dynamically via AJAX or page reloads with query parameters.
- Tables or grids display data read from text files transformed in backend views.
- Version comparison allows selecting two versions, displaying side-by-side or diff-highlighted text areas.


---

## 3. Data Storage Formats

### 3.1 users.txt
- Fields: `username|email|fullname|created_date`
- Descriptions:
  - username: unique user ID
  - email: user email
  - fullname: full name of user
  - created_date: account creation date (YYYY-MM-DD)
- Example:
```text
john|john@example.com|John Doe|2024-01-15
alice|alice@example.com|Alice Smith|2024-01-16
bob|bob@example.com|Bob Johnson|2024-01-17
admin|admin@example.com|Admin User|2024-01-10
```

### 3.2 articles.txt
- Fields: `article_id|title|author|category|status|tags|featured_image|meta_description|created_date|publish_date`
- Descriptions:
  - article_id: integer unique ID
  - title: article title text
  - author: username of creator
  - category: content category (news, blog, tutorial, etc.)
  - status: `draft`, `pending_review`, `under_review`, `approved`, `published`, `rejected`, `archived`
  - tags: comma-separated keywords
  - featured_image: path or empty
  - meta_description: short summary
  - created_date: creation timestamp
  - publish_date: scheduled publish timestamp or empty
- Example:
```text
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
```

### 3.3 article_versions.txt
- Fields: `version_id|article_id|version_number|content|author|created_date|change_summary`
- Descriptions:
  - version_id: integer unique version record
  - article_id: relates to articles.txt
  - version_number: integer version sequence
  - content: full article body text
  - author: username who edited
  - created_date: timestamp of version creation
  - change_summary: brief notes about the change
- Example:
```text
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
```

### 3.4 approvals.txt
- Fields: `approval_id|article_id|version_id|approver|status|comments|timestamp`
- Descriptions:
  - approval_id: unique record ID
  - article_id: linked article
  - version_id: linked article version
  - approver: username approving/rejecting
  - status: `approved`, `rejected`, `revision_requested`
  - comments: approver remarks
  - timestamp: approval time
- Example:
```text
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
```

### 3.5 workflow_stages.txt
- Fields: `stage_id|category|stage_name|stage_order|is_required`
- Descriptions:
  - stage_id: unique stage record
  - category: article category
  - stage_name: workflow step name
  - stage_order: integer step order
  - is_required: "yes" or "no"
- Example:
```text
1|tutorial|Editor Review|1|yes
2|tutorial|Publisher Approval|2|yes
3|news|Editor Review|1|yes
4|announcement|Editor Review|1|yes
5|announcement|Publisher Approval|2|yes
```

### 3.6 comments.txt
- Fields: `comment_id|article_id|version_id|user|comment_text|timestamp`
- Descriptions:
  - comment_id: unique comment identifier
  - article_id: article related
  - version_id: article version commented on
  - user: commenter username
  - comment_text: text of comment
  - timestamp: time posted
- Example:
```text
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
```

### 3.7 analytics.txt
- Fields: `analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares`
- Descriptions:
  - analytics_id: unique record
  - article_id: linked article
  - date: date of data
  - views: count of views
  - unique_visitors: count of unique visitors
  - avg_time_seconds: average time on page
  - shares: social shares count
- Example:
```text
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
```

---

## 4. Flask Templates and Mappings

| Route                              | Template Name          | Description                                    |
|----------------------------------|-----------------------|------------------------------------------------|
| `/dashboard`                     | dashboard.html         | Dashboard overview page                         |
| `/article/create`                | create_article.html    | Create new article editor                       |
| `/article/<article_id>/edit`    | edit_article.html      | Edit existing article with version control    |
| `/article/<article_id>/versions`| version_history.html   | Show version history and restore options      |
| `/articles/mine`                 | my_articles.html       | List current user articles with filters       |
| `/articles/published`            | published_articles.html| Public published articles library              |
| `/calendar`                     | content_calendar.html  | Content schedule calendar                       |
| `/article/<article_id>/analytics`| article_analytics.html | Analytics dashboard for article                 |

---

## 5. User Workflows

### 5.1 Creating an Article
1. User clicks "Create Article" button on Dashboard or My Articles page.
2. Navigate to `/article/create` (create_article.html).
3. User enters article title and content.
4. User clicks "Save as Draft" button.
5. Backend assigns new `article_id`, stores article with status `draft` in `articles.txt`.
6. Initial version created in `article_versions.txt` with version_number = 1.
7. User redirected to My Articles page to view their articles.

### 5.2 Editing an Article
1. From My Articles page, user selects article and clicks edit.
2. Navigates to `/article/<article_id>/edit` (edit_article.html).
3. User edits title and content.
4. Clicks "Save New Version" to create a new version:
   - Increment version_number
   - Save new content in `article_versions.txt`
5. Article metadata in `articles.txt` is updated if title changes.
6. User can cancel editing to return to My Articles.

### 5.3 Version History and Restoration
1. User navigates to `/article/<article_id>/versions`.
2. Page lists all versions with details.
3. User selects versions to compare (optional).
4. User clicks "Restore" to revert article to selected version:
   - New version created in `article_versions.txt` duplicating old content.
   - Article metadata remains unchanged.
5. Returns to edit page for further amendments.

### 5.4 Editorial Approval Process
1. When an article reaches `pending_review`, editorial users review it.
2. Approval records are stored in `approvals.txt` with status.
3. Editors can add comments in `comments.txt` linked to versions.
4. Articles can be marked:
   - approved: proceed toward publishing
   - rejected: sent back for revision
   - revision_requested: feedback given

### 5.5 Publishing and Scheduling
1. Approved articles can be scheduled via Content Calendar page.
2. Scheduling sets `publish_date` in `articles.txt`.
3. On publish date/time, article status changes to `published`.
4. Published articles appear on the Public Articles page.

### 5.6 Content Analytics
1. `/article/<article_id>/analytics` shows user metrics.
2. Data aggregated from `analytics.txt` by article for graphing and summaries.
3. Shows total views, unique visitors, average reading time, and shares.

---

# End of design_candidate_a.md
