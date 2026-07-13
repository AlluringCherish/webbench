# ContentPublishingHub Design Specification

---

## Section 1: Flask Route Paths, Templates, and UI Element IDs

### 1. Dashboard Page
- Route: `/dashboard`
- Template: `dashboard.html`
- UI Element IDs:
  - Page container: `dashboard-page`
  - Welcome message: `welcome-message`
  - Quick stats section: `quick-stats`
  - Create Article button: `create-article-button`
  - Recent activity feed: `recent-activity`

### 2. Create Article Page
- Route: `/article/create`
- Template: `create_article.html`
- UI Element IDs:
  - Page container: `create-article-page`
  - Article title input: `article-title`
  - Content editor textarea: `article-content`
  - Save as Draft button: `save-draft-button`
  - Cancel button: `cancel-button`

### 3. Edit Article Page
- Route: `/article/<article_id>/edit`
- Template: `edit_article.html`
- UI Element IDs:
  - Page container: `edit-article-page`
  - Article title input: `edit-article-title`
  - Content editor textarea: `edit-article-content`
  - Save New Version button: `save-version-button`
  - Cancel button: `cancel-edit`

### 4. Article Version History Page
- Route: `/article/<article_id>/versions`
- Template: `version_history.html`
- UI Element IDs:
  - Page container: `version-history-page`
  - Versions list: `versions-list`
  - Version comparison section: `version-comparison`
  - Restore button (per version): `restore-version-<version_id>`
  - Back to Edit button: `back-to-edit-history`

### 5. My Articles Page
- Route: `/articles/mine`
- Template: `my_articles.html`
- UI Element IDs:
  - Page container: `my-articles-page`
  - Filter by status dropdown: `filter-article-status`
  - Articles table: `articles-table`
  - Create New Article button: `create-new-article`
  - Back to Dashboard button: `back-to-dashboard`

### 6. Published Articles Page
- Route: `/articles/published`
- Template: `published_articles.html`
- UI Element IDs:
  - Page container: `published-articles-page`
  - Filter by category dropdown: `filter-published-category`
  - Articles grid: `published-articles-grid`
  - Sort by dropdown: `sort-published`
  - Back to Dashboard button: `back-to-dashboard-published`

### 7. Content Calendar Page
- Route: `/calendar`
- Template: `content_calendar.html`
- UI Element IDs:
  - Page container: `calendar-page`
  - Calendar view selector: `calendar-view`
  - Calendar grid: `calendar-grid`
  - Schedule button: `schedule-button`
  - Back to Dashboard button: `back-to-dashboard-calendar`

### 8. Article Analytics Page
- Route: `/article/<article_id>/analytics`
- Template: `article_analytics.html`
- UI Element IDs:
  - Page container: `analytics-page`
  - Analytics overview: `analytics-overview`
  - Total views: `analytics-total-views`
  - Unique visitors: `analytics-unique-visitors`
  - Back to Article button: `back-to-article-analytics`

---

## Section 2: UI Element Roles and User Interaction Flows

### Starting Point
- Testing begins from the Dashboard page.

### Dashboard Page
- Displays a personalized welcome message.
- Shows quick stats (e.g., drafts, published articles count).
- "Create Article" button navigates to Create Article Page.
- Recent activity feed shows latest user actions and system events.

### Create Article Page
- User inputs title and content.
- "Save as Draft" saves the article with `draft` status and sets creation date.
- "Cancel" returns to Dashboard without saving.

### Edit Article Page
- Loads existing article title and content.
- "Save New Version" saves updated content as a new version with incremented version number and timestamp.
- "Cancel" returns to My Articles or last visited page without saving changes.

### Article Version History Page
- Displays list of all article versions sorted descending by version number.
- User can select two versions for side-by-side comparison in `version-comparison`.
- "Restore" button restores selected version making it current editable version.
- "Back to Edit" navigates back to Edit Article Page.

### My Articles Page
- Lists user's articles in table with filters by status.
- User can create new articles or return to Dashboard.

### Published Articles Page
- Displays published articles in grid with category filter and sorting options.
- Back to Dashboard navigation link.

### Content Calendar Page
- User views scheduled articles by day, week, or month.
- Schedule button opens scheduling input.
- Back navigates to Dashboard.

### Article Analytics Page
- Presents article engagement metrics: total views, unique visitors, avg time on page, shares.
- Back navigates to article edit or detail view.

### Version Control & Editorial Workflow
- Article edits produce new versions saved with metadata.
- Approvals linked to versions and track reviewer comments, status.
- Editorial comments attached to specific versions.
- Workflow stages define sequential review steps per category.
- Users with roles can approve, reject, or request revision updating article status.

---

## Section 3: Data Formats, Field Orders, Examples, and Relationships

### 1. users.txt
- Format: `username|email|fullname|created_date`
- Field Types:
  - username: string, unique
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

### 2. articles.txt
- Format: `article_id|title|author|category|status|tags|featured_image|meta_description|created_date|publish_date`
- Field Types:
  - article_id: int
  - title: string
  - author: string (username)
  - category: enum [news, blog, tutorial, announcement, press_release]
  - status: enum [draft, pending_review, under_review, approved, published, rejected, archived]
  - tags: comma-separated string
  - featured_image: string (optional URL/path)
  - meta_description: string
  - created_date: date (YYYY-MM-DD)
  - publish_date: datetime (YYYY-MM-DD HH:MM:SS) or empty if unpublished
- Example:
```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
```

### 3. article_versions.txt
- Format: `version_id|article_id|version_number|content|author|created_date|change_summary`
- Field Types:
  - version_id: int
  - article_id: int (FK to articles)
  - version_number: int
  - content: string
  - author: string (username)
  - created_date: datetime (YYYY-MM-DD HH:MM:SS)
  - change_summary: string
- Example:
```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
```

### 4. approvals.txt
- Format: `approval_id|article_id|version_id|approver|status|comments|timestamp`
- Field Types:
  - approval_id: int
  - article_id: int (FK to articles)
  - version_id: int (FK to article_versions)
  - approver: string (username)
  - status: enum [approved, rejected, revision_requested]
  - comments: string
  - timestamp: datetime (YYYY-MM-DD HH:MM:SS)
- Example:
```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
```

### 5. workflow_stages.txt
- Format: `stage_id|category|stage_name|stage_order|is_required`
- Field Types:
  - stage_id: int
  - category: string
  - stage_name: string
  - stage_order: int
  - is_required: enum [yes, no]
- Example:
```
1|tutorial|Editor Review|1|yes
2|tutorial|Publisher Approval|2|yes
3|news|Editor Review|1|yes
4|announcement|Editor Review|1|yes
5|announcement|Publisher Approval|2|yes
```

### 6. comments.txt
- Format: `comment_id|article_id|version_id|user|comment_text|timestamp`
- Field Types:
  - comment_id: int
  - article_id: int (FK to articles)
  - version_id: int (FK to article_versions)
  - user: string (username)
  - comment_text: string
  - timestamp: datetime (YYYY-MM-DD HH:MM:SS)
- Example:
```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
```

### 7. analytics.txt
- Format: `analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares`
- Field Types:
  - analytics_id: int
  - article_id: int (FK to articles)
  - date: date (YYYY-MM-DD)
  - views: int
  - unique_visitors: int
  - avg_time_seconds: int
  - shares: int
- Example:
```
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
```

---

This design_spec.md fully encompasses the ContentPublishingHub application including all pages, UI elements, interaction flows, version control mechanisms, and detailed data storage formats as required, with the Dashboard as the testing start point.