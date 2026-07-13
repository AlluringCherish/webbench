# Backend Design for ContentPublishingHub

---

## Section 1: Flask Routes Design

### 1. Dashboard Page
- **Route:** `/dashboard`
- **Methods:** GET
- **Responsibilities:**
  - Authenticate user session
  - Load user information
  - Fetch quick stats: counts of articles by status, recent activity feed
  - Render dashboard.html with user data, stats, recent activity

### 2. Create Article Page
- **Route:** `/article/create`
- **Methods:** GET, POST
- **Responsibilities:**
  - GET: Render create_article.html with empty form
  - POST: Validate input; create new article record with status 'draft'
    - Create initial article_versions entry with version_number=1
    - Save author as current user
    - Redirect to `/articles/mine` or `/article/<new_article_id>/edit`

### 3. Edit Article Page
- **Route:** `/article/<int:article_id>/edit`
- **Methods:** GET, POST
- **Responsibilities:**
  - GET: Load article data and latest version content
  - POST: Save a new article_versions entry with incremented version_number
    - Update article's status if needed (e.g., draft to pending_review)
    - Store change summary if provided
    - Redirect back to same edit page or version history

### 4. Article Version History Page
- **Route:** `/article/<int:article_id>/versions`
- **Methods:** GET, POST
- **Responsibilities:**
  - GET: Show all versions of the article with metadata
  - POST: (Restore action) Set the current article version content to selected older version
    - Create a new version entry copying restored version content

### 5. My Articles Page
- **Route:** `/articles/mine`
- **Methods:** GET
- **Responsibilities:**
  - Filter articles authored by current user
  - Support query param for status filter
  - Display articles in tabular form with edit links

### 6. Published Articles Page
- **Route:** `/articles/published`
- **Methods:** GET
- **Responsibilities:**
  - List all articles with status `published`
  - Support category filter and sorting options

### 7. Content Calendar Page
- **Route:** `/calendar`
- **Methods:** GET, POST
- **Responsibilities:**
  - GET: Display scheduled publication dates with articles
  - POST: Schedule or reschedule article publish date
    - Update article record's publish_date

### 8. Article Analytics Page
- **Route:** `/article/<int:article_id>/analytics`
- **Methods:** GET
- **Responsibilities:**
  - Summarize and aggregate analytics data for the article
  - Display metrics like total views, unique visitors, avg time spent, shares


## Section 2: Data Models and File Schemas

### users.txt
- Format: `username|email|fullname|created_date`
- Fields:
  - username: string unique identifier
  - email: string
  - fullname: string
  - created_date: YYYY-MM-DD

- Example:
```
john|john@example.com|John Doe|2024-01-15
alice|alice@example.com|Alice Smith|2024-01-16
bob|bob@example.com|Bob Johnson|2024-01-17
admin|admin@example.com|Admin User|2024-01-10
```

### articles.txt
- Format: `article_id|title|author|category|status|tags|featured_image|meta_description|created_date|publish_date`
- Fields:
  - article_id: int unique
  - title: string
  - author: string (username referencing users.txt)
  - category: enum [news, blog, tutorial, announcement, press_release]
  - status: enum [draft, pending_review, under_review, approved, published, rejected, archived]
  - tags: comma-separated strings
  - featured_image: string (filepath or empty)
  - meta_description: string
  - created_date: YYYY-MM-DD
  - publish_date: YYYY-MM-DD HH:MM:SS or empty

- Example:
```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
```

### article_versions.txt
- Format: `version_id|article_id|version_number|content|author|created_date|change_summary`
- Fields:
  - version_id: int unique
  - article_id: int referencing article
  - version_number: int (incremental)
  - content: text blob
  - author: string (username)
  - created_date: YYYY-MM-DD HH:MM:SS
  - change_summary: short string

- Example:
```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
```

### approvals.txt
- Format: `approval_id|article_id|version_id|approver|status|comments|timestamp`
- Fields:
  - approval_id: int unique
  - article_id: int reference
  - version_id: int reference
  - approver: username string
  - status: enum [approved, rejected, revision_requested]
  - comments: string
  - timestamp: YYYY-MM-DD HH:MM:SS

- Example:
```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
```

### workflow_stages.txt
- Format: `stage_id|category|stage_name|stage_order|is_required`
- Fields:
  - stage_id: int unique
  - category: string (content category)
  - stage_name: string (e.g., Editor Review)
  - stage_order: int (sequence)
  - is_required: string ('yes' or 'no')

- Example:
```
1|tutorial|Editor Review|1|yes
2|tutorial|Publisher Approval|2|yes
3|news|Editor Review|1|yes
4|announcement|Editor Review|1|yes
5|announcement|Publisher Approval|2|yes
```

### comments.txt
- Format: `comment_id|article_id|version_id|user|comment_text|timestamp`
- Fields:
  - comment_id: int unique
  - article_id: int
  - version_id: int
  - user: username string
  - comment_text: string
  - timestamp: YYYY-MM-DD HH:MM:SS

- Example:
```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
```

### analytics.txt
- Format: `analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares`
- Fields:
  - analytics_id: int unique
  - article_id: int
  - date: YYYY-MM-DD
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


### Relationships
- `articles.txt.article_id` referenced by `article_versions.txt.article_id`, `approvals.txt.article_id`, `comments.txt.article_id`, `analytics.txt.article_id`
- `article_versions.txt.version_id` linked by `approvals.txt.version_id` and `comments.txt.version_id`
- `users.txt.username` referenced in articles, versions, approvals, comments
- Workflow stages define approval process per category used to guide status changes


## Section 3: Business Logic and Functional Requirements

### Content Version Control
- Each save in edit creates new version with incremented version_number
- Versions track full article content, author, timestamps, and change summaries
- Version history page lists and allows restoring prior versions
- Restoring a prior version creates a new version copy with old content

### Approval Status Handling
- Articles progress through statuses based on editorial workflow
- Approval records reflect individual approver decisions per version
- All required workflow stages must be approved before advancing status (e.g., to `approved` or `published`)
- Revision requests or rejects update article status accordingly
- Comments and approvals link to specific versions

### Scheduling
- Articles can be scheduled by setting `publish_date` in articles.txt
- Content calendar page manages viewing and updating these dates
- Publish date affects visibility in published articles listing

### Analytics Calculations
- Aggregate analytics data by article across dates
- Display total views, unique visitor counts, average time spent, and shares
- Analytics data retrieved from analytics.txt and aggregated for display

### Backend State Changes Triggered By Routes
- `/article/create` POST: creates new article and initial version
- `/article/<article_id>/edit` POST: adds new version, possibly changes status
- `/article/<article_id>/versions` POST: restores an older version as new
- `/calendar` POST: updates publish_date of article


---

This backend design document provides a definitive blueprint to implement the ContentPublishingHub backend server in Flask, adhering strictly to the provided specification and data schema requirements.