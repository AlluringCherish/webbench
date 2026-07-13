# Frontend Design Specification for ContentPublishingHub

## Section 1: Template and Page Specifications

### 1. Dashboard Page (`dashboard.html`)
- Template filename: `dashboard.html`
- Page container ID: `dashboard-page`
- Element IDs and purpose:
  - `welcome-message`: Displays welcome text with logged-in username (text element)
  - `quick-stats`: Section for showing summary statistics (div container)
  - `create-article-button`: Button to navigate to Create Article page
  - `recent-activity`: Section displaying recent activities feed (list or div container)

### 2. Create Article Page (`create_article.html`)
- Template filename: `create_article.html`
- Page container ID: `create-article-page`
- Element IDs and purpose:
  - `article-title`: Input field for entering article title
  - `article-content`: Textarea editor for article content
  - `save-draft-button`: Button to save the article as draft
  - `cancel-button`: Button to cancel creation and return

### 3. Edit Article Page (`edit_article.html`)
- Template filename: `edit_article.html`
- Page container ID: `edit-article-page`
- Element IDs and purpose:
  - `edit-article-title`: Input field for editing article title
  - `edit-article-content`: Textarea editor for editing content
  - `save-version-button`: Button to save the new version of article
  - `cancel-edit`: Button to cancel edits and return

### 4. Article Version History Page (`version_history.html`)
- Template filename: `version_history.html`
- Page container ID: `version-history-page`
- Element IDs and purpose:
  - `versions-list`: List or table showing all versions of the article
  - `version-comparison`: Section to display comparison between versions
  - `restore-version-1`: Button to restore a selected previous version (suffix `1` indicates version id 1 or dynamic id scheme)
  - `back-to-edit-history`: Button to navigate back to article editing page

### 5. My Articles Page (`my_articles.html`)
- Template filename: `my_articles.html`
- Page container ID: `my-articles-page`
- Element IDs and purpose:
  - `filter-article-status`: Dropdown to filter articles by status
  - `articles-table`: Table listing user's articles with details
  - `create-new-article`: Button to create a new article (navigates to create article)
  - `back-to-dashboard`: Button to return to dashboard

### 6. Published Articles Page (`published_articles.html`)
- Template filename: `published_articles.html`
- Page container ID: `published-articles-page`
- Element IDs and purpose:
  - `filter-published-category`: Dropdown filter by article category
  - `published-articles-grid`: Grid or card layout to display published articles
  - `sort-published`: Dropdown to sort articles by parameters (date, popularity, etc.)
  - `back-to-dashboard-published`: Button to return to dashboard

### 7. Content Calendar Page (`content_calendar.html`)
- Template filename: `content_calendar.html`
- Page container ID: `calendar-page`
- Element IDs and purpose:
  - `calendar-view`: Selector to switch calendar views (day, week, month)
  - `calendar-grid`: Container/grid displaying scheduled publication dates and events
  - `schedule-button`: Button to schedule new content/publication
  - `back-to-dashboard-calendar`: Button to return to dashboard

### 8. Article Analytics Page (`article_analytics.html`)
- Template filename: `article_analytics.html`
- Page container ID: `analytics-page`
- Element IDs and purpose:
  - `analytics-overview`: Container section showing overall analytics summary
  - `analytics-total-views`: Displays total page views count
  - `analytics-unique-visitors`: Displays count of unique visitors
  - `back-to-article-analytics`: Button to navigate back to the article edit or detail page

---

## Section 2: Context Variables and Data Bindings

### 1. `dashboard.html`
- `username` (string): Logged-in user's display name
- `quick_stats` (dict): Summary stats key-value pairs (e.g. total articles, drafts, published)
- `recent_activities` (list of dict): Items describing recent actions; each with `type`, `description`, `timestamp`.

### 2. `create_article.html`
- Empty form inputs initially or with defaults

### 3. `edit_article.html`
- `article_id` (int/string)
- `article_title` (string): Current title
- `article_content` (string): Current content
- Possibly `version_info` if needed for display

### 4. `version_history.html`
- `article_id` (int/string)
- `versions` (list of dict): Each with `version_id`, `version_number`, `created_date`, `change_summary`
- `selected_version_content_1` (string): Content of version to compare/restore (matching restore button id suffix)

### 5. `my_articles.html`
- `user_articles` (list of dict): Articles with fields: `article_id`, `title`, `status`, `category`, `publish_date`
- `status_options` (list of strings): Statuses for filter dropdown

### 6. `published_articles.html`
- `published_articles` (list of dict): Including `article_id`, `title`, `category`, `publish_date`, `featured_image`
- `category_options` (list of strings): Categories for filter dropdown
- `sort_options` (list of strings): Sort parameters

### 7. `content_calendar.html`
- `calendar_view_options` (list of strings): e.g. day, week, month
- `scheduled_items` (list of dict): Each with `article_id`, `title`, `publish_date`

### 8. `article_analytics.html`
- `article_id` (int/string)
- `analytics_summary` (dict): with keys: `total_views` (int), `unique_visitors` (int), plus others for extended analytics if desired

---

## Section 3: Navigation and Inter-Page Links

- From Dashboard:
  - `create-article-button` -> Create Article Page (`/article/create`)
  - Navigation to other pages (My Articles, Published Articles, Calendar, Analytics) should be present externally or included in dashboard or global nav but not detailed here.

- Create Article page:
  - `cancel-button` -> returns to Dashboard (`/dashboard` or My Articles)

- Edit Article page:
  - `cancel-edit` -> returns to Dashboard or My Articles
  - Save triggers version save

- Version History page:
  - `restore-version-1` (and other dynamically generated restore buttons) -> triggers version restore action
  - `back-to-edit-history` -> returns to Edit Article page for the same `article_id`

- My Articles page:
  - `create-new-article` -> Create Article page
  - `back-to-dashboard` -> Dashboard
  - Table rows might link to Edit Article pages

- Published Articles page:
  - `back-to-dashboard-published` -> Dashboard
  - Article entries in `published-articles-grid` may link to full article detail (not specified here)

- Content Calendar page:
  - `schedule-button` -> Open Create Article or Scheduling popup
  - `back-to-dashboard-calendar` -> Dashboard

- Article Analytics page:
  - `back-to-article-analytics` -> Edit Article or Article Detail page

---

This specification defines the HTML templates with element IDs aligned with the provided app requirements, including context variables expected from the backend and navigation flow details necessary to implement the frontend templates and user interactions.
