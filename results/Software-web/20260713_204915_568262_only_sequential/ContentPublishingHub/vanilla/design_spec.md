# ContentPublishingHub Web Application Design Specification

## 1. Flask Routes Specification

| Route Path                    | HTTP Method(s) | Flask Function Name          | Template File           |
|-------------------------------|----------------|-----------------------------|-------------------------|
| /dashboard                    | GET            | dashboard()                 | dashboard.html          |
| /article/create              | GET, POST      | create_article()            | create_article.html     |
| /article/<article_id>/edit   | GET, POST      | edit_article(article_id)    | edit_article.html       |
| /article/<article_id>/versions| GET          | article_version_history(article_id) | version_history.html   |
| /articles/mine               | GET            | my_articles()               | my_articles.html        |
| /articles/published          | GET            | published_articles()        | published_articles.html |
| /calendar                   | GET            | content_calendar()          | content_calendar.html   |
| /article/<article_id>/analytics| GET         | article_analytics(article_id) | article_analytics.html |

---

## 2. HTML Template Details

### Dashboard Page (`dashboard.html`)
- Element IDs:
  - `dashboard-page` (page container)
  - `welcome-message` (welcome message with username)
  - `quick-stats` (quick statistics section)
  - `create-article-button` (button to navigate to article creation page)
  - `recent-activity` (recent activities feed)

### Create Article Page (`create_article.html`)
- Element IDs:
  - `create-article-page` (page container)
  - `article-title` (input field for article title)
  - `article-content` (textarea for article content)
  - `save-draft-button` (button to save article as draft)
  - `cancel-button` (button to cancel article creation and navigate back)

### Edit Article Page (`edit_article.html`)
- Element IDs:
  - `edit-article-page` (page container)
  - `edit-article-title` (input field for editing article title)
  - `edit-article-content` (textarea for editing article content)
  - `save-version-button` (button to save a new version of the article)
  - `cancel-edit` (button to cancel editing and navigate back)

### Article Version History Page (`version_history.html`)
- Element IDs:
  - `version-history-page` (page container)
  - `versions-list` (list of all article versions)
  - `version-comparison` (section to compare selected versions)
  - `restore-version-1` (button for restoring a specific version)
  - `back-to-edit-history` (button to navigate back to edit page)

### My Articles Page (`my_articles.html`)
- Element IDs:
  - `my-articles-page` (page container)
  - `filter-article-status` (dropdown filter for article status)
  - `articles-table` (table listing user's articles)
  - `create-new-article` (button to create a new article)
  - `back-to-dashboard` (button to return to dashboard)

### Published Articles Page (`published_articles.html`)
- Element IDs:
  - `published-articles-page` (page container)
  - `filter-published-category` (dropdown filter by category)
  - `published-articles-grid` (grid displaying published articles)
  - `sort-published` (dropdown to sort published articles)
  - `back-to-dashboard-published` (button to return to dashboard)

### Content Calendar Page (`content_calendar.html`)
- Element IDs:
  - `calendar-page` (page container)
  - `calendar-view` (selector for calendar view mode)
  - `calendar-grid` (grid showing scheduled publications)
  - `schedule-button` (button to schedule new publication)
  - `back-to-dashboard-calendar` (button to return to dashboard)

### Article Analytics Page (`article_analytics.html`)
- Element IDs:
  - `analytics-page` (page container)
  - `analytics-overview` (overview section for analytics)
  - `analytics-total-views` (display total views count)
  - `analytics-unique-visitors` (display unique visitor count)
  - `back-to-article-analytics` (button to go back to article management page)

---

## 3. Data Storage Format Contracts

All data files are stored as pipe-delimited (`|`) text files in the `data` directory.

### 1. users.txt
- File: `data/users.txt`
- Fields Order and Description:
  1. `username` - unique user login name
  2. `email` - user email address
  3. `fullname` - user's full name
  4. `created_date` - date user account created (YYYY-MM-DD format)
- Example Line:
  `john|john@example.com|John Doe|2024-01-15`

### 2. articles.txt
- File: `data/articles.txt`
- Fields Order and Description:
  1. `article_id` - unique article identifier
  2. `title` - article title
  3. `author` - username of article author
  4. `category` - one of (news, blog, tutorial, announcement, press_release)
  5. `status` - one of (draft, pending_review, under_review, approved, published, rejected, archived)
  6. `tags` - comma-separated tags associated with article
  7. `featured_image` - path or URL to featured image (may be empty)
  8. `meta_description` - short meta description text
  9. `created_date` - date article created (YYYY-MM-DD)
  10. `publish_date` - datetime when article was or will be published (YYYY-MM-DD HH:MM:SS), may be empty if unpublished
- Example Line:
  `1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00`

### 3. article_versions.txt
- File: `data/article_versions.txt`
- Fields Order and Description:
  1. `version_id` - unique version record ID
  2. `article_id` - article associated with the version
  3. `version_number` - incremental version number
  4. `content` - full article content for this version
  5. `author` - username who created this version
  6. `created_date` - datetime when version was created (YYYY-MM-DD HH:MM:SS)
  7. `change_summary` - brief summary of changes made
- Example Line:
  `1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft`

### 4. approvals.txt
- File: `data/approvals.txt`
- Fields Order and Description:
  1. `approval_id` - unique approval record ID
  2. `article_id` - article under approval
  3. `version_id` - version of article approved/rejected
  4. `approver` - username of the approver
  5. `status` - one of (approved, rejected, revision_requested)
  6. `comments` - textual comments from approver
  7. `timestamp` - datetime of approval action (YYYY-MM-DD HH:MM:SS)
- Example Line:
  `1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00`

### 5. workflow_stages.txt
- File: `data/workflow_stages.txt`
- Fields Order and Description:
  1. `stage_id` - unique stage ID
  2. `category` - article category this stage applies to
  3. `stage_name` - descriptive name of stage
  4. `stage_order` - integer order in workflow
  5. `is_required` - yes/no if stage must be completed
- Example Line:
  `1|tutorial|Editor Review|1|yes`

### 6. comments.txt
- File: `data/comments.txt`
- Fields Order and Description:
  1. `comment_id` - unique comment ID
  2. `article_id` - article associated
  3. `version_id` - article version associated
  4. `user` - username who made the comment
  5. `comment_text` - comment text
  6. `timestamp` - datetime comment made (YYYY-MM-DD HH:MM:SS)
- Example Line:
  `1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00`

### 7. analytics.txt
- File: `data/analytics.txt`
- Fields Order and Description:
  1. `analytics_id` - unique analytics record ID
  2. `article_id` - article being tracked
  3. `date` - date of metrics record (YYYY-MM-DD)
  4. `views` - total views for the day
  5. `unique_visitors` - number of unique visitors
  6. `avg_time_seconds` - average time spent in seconds
  7. `shares` - number of shares
- Example Line:
  `1|1|2024-01-22|150|120|245|12`

---

## 4. Application Flow and Button Behavior

### Dashboard Page
- `create-article-button`: Navigates to the Create Article page (`/article/create`).

### Create Article Page
- `save-draft-button`: Saves current input as a new article draft entry in `articles.txt` with status `draft`, and initial version in `article_versions.txt`. Redirects user to My Articles page.
- `cancel-button`: Discards inputs and navigates back to Dashboard page (`/dashboard`).

### Edit Article Page
- `save-version-button`: Saves a new article version with incremented version number in `article_versions.txt`, updates the article record if necessary, and retains the current editing session. Redirects as needed based on workflow.
- `cancel-edit`: Cancels editing and returns to My Articles page or last visited page.

### Article Version History Page
- `restore-version-1`: Restores the selected version as current editable article content, creating a new version entry with a change summary indicating restoration.
- `back-to-edit-history`: Returns to Edit Article page for the same article.

### My Articles Page
- `filter-article-status`: Allows filtering articles by status.
- `create-new-article`: Navigates to Create Article page.
- `back-to-dashboard`: Navigates back to Dashboard page.

### Published Articles Page
- `filter-published-category`: Filters displayed articles by selected category.
- `sort-published`: Sorts the published articles by selected criteria.
- `back-to-dashboard-published`: Navigates back to Dashboard page.

### Content Calendar Page
- `schedule-button`: Opens scheduling interface (modal or page) to add new publication date and time.
- `back-to-dashboard-calendar`: Returns to Dashboard page.

### Article Analytics Page
- `back-to-article-analytics`: Returns to the related Article Edit or My Articles page.

### General Navigation
- Dashboard (`/dashboard`) is the app's main landing page.
- Users create articles starting at `/article/create` or from My Articles page.
- Editing articles, viewing versions, scheduling and analytics are accessible through specific article routes.

---

This design specification supports the implementation of backend routes, frontend UI element identification, data file format parsing and writing, and provides exhaustive details for UI automated testing and development.
