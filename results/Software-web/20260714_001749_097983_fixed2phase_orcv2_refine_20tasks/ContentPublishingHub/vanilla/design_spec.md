# ContentPublishingHub Web Application Design Specification

---

## Section 1: Page and Route Specifications

### 1. Dashboard Page
- **Route:** `/dashboard`
- **Template:** `dashboard.html`
- **Page Container ID:** `dashboard-page`
- **Element IDs:**
  - `welcome-message` (Welcomes the user by username)
  - `quick-stats` (Displays summary metrics such as article counts, recent approvals, etc.)
  - `create-article-button` (Button to navigate to create article page)
  - `recent-activity` (List or feed of recent actions and changes)

### 2. Create Article Page
- **Route:** `/article/create`
- **Template:** `create_article.html`
- **Page Container ID:** `create-article-page`
- **Element IDs:**
  - `article-title` (Input for new article title)
  - `article-content` (Textarea editor for article content)
  - `save-draft-button` (Save article as draft)
  - `cancel-button` (Cancel creation and navigate back)

### 3. Edit Article Page
- **Route:** `/article/<article_id>/edit`
- **Template:** `edit_article.html`
- **Page Container ID:** `edit-article-page`
- **Element IDs:**
  - `edit-article-title` (Input for editing article title)
  - `edit-article-content` (Textarea editor for editing content)
  - `save-version-button` (Save as a new version)
  - `cancel-edit` (Cancel editing and go back)

### 4. Article Version History Page
- **Route:** `/article/<article_id>/versions`
- **Template:** `version_history.html`
- **Page Container ID:** `version-history-page`
- **Element IDs:**
  - `versions-list` (List of all versions for the article)
  - `version-comparison` (View for comparing versions side-by-side or diff)
  - `restore-version-1` (Restore button for a selected version — ID suffixed by version number)
  - `back-to-edit-history` (Button to return to article edit page)

### 5. My Articles Page
- **Route:** `/articles/mine`
- **Template:** `my_articles.html`
- **Page Container ID:** `my-articles-page`
- **Element IDs:**
  - `filter-article-status` (Dropdown to filter articles by status)
  - `articles-table` (Table listing articles owned by the user)
  - `create-new-article` (Button to create a new article)
  - `back-to-dashboard` (Button to return to dashboard)

### 6. Published Articles Page
- **Route:** `/articles/published`
- **Template:** `published_articles.html`
- **Page Container ID:** `published-articles-page`
- **Element IDs:**
  - `filter-published-category` (Dropdown to filter published articles by category)
  - `published-articles-grid` (Grid layout of public articles)
  - `sort-published` (Dropdown to sort articles by various criteria)
  - `back-to-dashboard-published` (Button to return to dashboard)

### 7. Content Calendar Page
- **Route:** `/calendar`
- **Template:** `content_calendar.html`
- **Page Container ID:** `calendar-page`
- **Element IDs:**
  - `calendar-view` (Selector for different calendar views such as daily, weekly, monthly)
  - `calendar-grid` (Calendar showing scheduled publication dates)
  - `schedule-button` (Opens scheduling modal or page)
  - `back-to-dashboard-calendar` (Button to return to dashboard)

### 8. Article Analytics Page
- **Route:** `/article/<article_id>/analytics`
- **Template:** `article_analytics.html`
- **Page Container ID:** `analytics-page`
- **Element IDs:**
  - `analytics-overview` (Summary block for engagement metrics)
  - `analytics-total-views` (Displays total views count)
  - `analytics-unique-visitors` (Displays unique visitors count)
  - `back-to-article-analytics` (Button to return to article edit or view page)


---

## Section 2: UI Element and Interaction Details

### Dashboard Page Start Point
- The application testing starts from the Dashboard page (`/dashboard`). Upon login, users are directed here.
- The welcome message (`welcome-message`) reflects the logged-in user's name.
- Quick stats (`quick-stats`) provide an at-a-glance snapshot of the user's content, approval stats, and recent updates.
- Recent activity (`recent-activity`) lists latest system actions relevant to the user.
- The 'Create Article' button (`create-article-button`) navigates smoothly to the article creation page `/article/create`.

### Article Creation and Editing Workflows
- From Dashboard or 'My Articles,' users create new articles.
- On create article page, user inputs title (`article-title`) and content (`article-content`).
  - "Save as Draft" (`save-draft-button`) writes the article as a draft.
  - "Cancel" (`cancel-button`) aborts creation and navigates back to Dashboard.
- Editing an existing article uses `/article/<article_id>/edit` with fields `edit-article-title` and `edit-article-content`.
  - "Save New Version" (`save-version-button`) saves changes as a new version, updating version history.
  - "Cancel" (`cancel-edit`) returns user back to previous page or Dashboard.

### Version History and Restoration
- User navigates to `/article/<article_id>/versions` to see all saved versions in `versions-list`.
- The `version-comparison` element displays differences for two selected versions.
- Users select versions and use the specific restore button (`restore-version-<version_number>`) to revert content to that version.
- "Back to Edit" button (`back-to-edit-history`) brings user back to edit page.

### Article Listings
- "My Articles" (`/articles/mine`) lists all user’s articles with a status filter (`filter-article-status`).
- Articles are displayed in a table (`articles-table`) with metadata columns.
- Buttons for creating new articles and returning to Dashboard ensure smooth navigation.

### Published Articles and Content Calendar
- Published Articles page offers filters by category (`filter-published-category`), sorting options (`sort-published`), and displays articles in a grid layout (`published-articles-grid`).
- Content Calendar shows scheduled articles with view selection (`calendar-view`), the calendar grid (`calendar-grid`), and scheduling button (`schedule-button`).
- Both pages have back navigation to Dashboard.

### Analytics
- Article-specific analytics page shows comprehensive metrics in `analytics-overview`, including total views (`analytics-total-views`) and unique visitor count (`analytics-unique-visitors`).
- A back button returns to the related article page.

---

## Section 3: Data Storage Formats

### 1. users.txt
- **Format:** `username|email|fullname|created_date`
- **Fields:**
  - username: string, unique user ID
  - email: string, user email
  - fullname: string
  - created_date: ISO date `YYYY-MM-DD`
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
  - article_id: integer primary key
  - title: string
  - author: username string
  - category: string (news, blog, tutorial, announcement, press_release)
  - status: string (draft, pending_review, under_review, approved, published, rejected, archived)
  - tags: comma-separated string
  - featured_image: string (path or URL), can be empty
  - meta_description: string
  - created_date: ISO date `YYYY-MM-DD`
  - publish_date: datetime `YYYY-MM-DD HH:MM:SS` or empty if unpublished
- **Example:**
```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
```

### 3. article_versions.txt
- **Format:** `version_id|article_id|version_number|content|author|created_date|change_summary`
- **Fields:**
  - version_id: integer primary key
  - article_id: integer foreign key to articles
  - version_number: integer, incremental per article
  - content: string, full article content
  - author: username string
  - created_date: datetime `YYYY-MM-DD HH:MM:SS`
  - change_summary: string
- **Example:**
```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
```

### 4. approvals.txt
- **Format:** `approval_id|article_id|version_id|approver|status|comments|timestamp`
- **Fields:**
  - approval_id: integer primary key
  - article_id: integer foreign key
  - version_id: integer foreign key
  - approver: username string
  - status: string (approved, rejected, revision_requested)
  - comments: string
  - timestamp: datetime `YYYY-MM-DD HH:MM:SS`
- **Example:**
```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
```

### 5. workflow_stages.txt
- **Format:** `stage_id|category|stage_name|stage_order|is_required`
- **Fields:**
  - stage_id: integer primary key
  - category: string, matches article category
  - stage_name: string
  - stage_order: integer
  - is_required: string (`yes` or `no`)
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
  - comment_id: integer primary key
  - article_id: integer foreign key
  - version_id: integer foreign key
  - user: username string
  - comment_text: string
  - timestamp: datetime `YYYY-MM-DD HH:MM:SS`
- **Example:**
```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
```

### 7. analytics.txt
- **Format:** `analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares`
- **Fields:**
  - analytics_id: integer primary key
  - article_id: integer foreign key
  - date: date `YYYY-MM-DD`
  - views: integer
  - unique_visitors: integer
  - avg_time_seconds: integer average time spent
  - shares: integer
- **Example:**
```
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
```

---

This specification fully covers the ContentPublishingHub Flask web application pages, routes, UI element IDs, user interactions, and data file formats necessary for implementation and testing.