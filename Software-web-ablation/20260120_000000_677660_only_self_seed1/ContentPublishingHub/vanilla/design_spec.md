# ContentPublishingHub Design Specification

---

## Section 1: Flask Routes Specification

| Route Pattern                    | HTTP Method(s) | Function Name             | Template Rendered        | Context Variables Passed to Template                     |
|--------------------------------|----------------|---------------------------|--------------------------|----------------------------------------------------------|
| `/dashboard`                   | GET            | dashboard                 | dashboard.html           | `username` (str): Current user's username                |
| `/article/create`              | GET, POST      | create_article            | create_article.html      | GET: none; POST: validation errors (dict) if any         |
| `/article/<article_id>/edit`   | GET, POST      | edit_article              | edit_article.html        | `article_id` (int), `article` (dict with article data), `current_version` (dict), validation errors (POST) |
| `/article/<article_id>/versions` | GET          | article_version_history   | version_history.html     | `article_id` (int), `versions` (list of dict), `selected_version` (optional), `comparison_data` (optional) |
| `/articles/mine`               | GET            | my_articles               | my_articles.html         | `username` (str), `articles` (list of dict), `filter_status` (str) |
| `/articles/published`          | GET            | published_articles        | published_articles.html  | `articles` (list of dict), `filter_category` (str), `sort_order` (str) |
| `/calendar`                   | GET, POST      | content_calendar          | content_calendar.html    | `calendar_view` (str), `scheduled_items` (list of dict)  |
| `/article/<article_id>/analytics` | GET          | article_analytics         | article_analytics.html   | `article_id` (int), `analytics_data` (dict)              |


### Route Details

1. **Dashboard Page**
   - Route: `/dashboard`
   - Method: GET
   - Function: `dashboard`
   - Template: `dashboard.html`
   - Context:
     - `username` (str): Logged in user to show welcome message

2. **Create Article Page**
   - Route: `/article/create`
   - Methods: GET (render empty form), POST (save draft or submit article)
   - Function: `create_article`
   - Template: `create_article.html`
   - Context:
     - On GET: none
     - On POST error: errors dict if validation fails

3. **Edit Article Page**
   - Route: `/article/<article_id>/edit`
   - Methods: GET, POST
   - Function: `edit_article`
   - Template: `edit_article.html`
   - Context:
     - `article_id` (int)
     - `article`: dict with article details and metadata
     - `current_version`: dict with the latest version content
     - On POST error: validation error messages

4. **Article Version History**
   - Route: `/article/<article_id>/versions`
   - Method: GET
   - Function: `article_version_history`
   - Template: `version_history.html`
   - Context:
     - `article_id` (int)
     - `versions`: list of dicts with version metadata
     - May include data for version comparison and selected version

5. **My Articles Page**
   - Route: `/articles/mine`
   - Method: GET
   - Function: `my_articles`
   - Template: `my_articles.html`
   - Context:
     - `username` (str)
     - `articles`: filtered list of article dicts belonging to user
     - `filter_status`: current status filter applied

6. **Published Articles Page**
   - Route: `/articles/published`
   - Method: GET
   - Function: `published_articles`
   - Template: `published_articles.html`
   - Context:
     - `articles`: list of published articles dicts
     - `filter_category`: category filter
     - `sort_order`: sorting criteria

7. **Content Calendar Page**
   - Route: `/calendar`
   - Methods: GET (view calendar), POST (schedule publication)
   - Function: `content_calendar`
   - Template: `content_calendar.html`
   - Context:
     - `calendar_view`: current selected calendar view
     - `scheduled_items`: list of scheduled publications

8. **Article Analytics Page**
   - Route: `/article/<article_id>/analytics`
   - Method: GET
   - Function: `article_analytics`
   - Template: `article_analytics.html`
   - Context:
     - `article_id` (int)
     - `analytics_data`: dict with views, unique visitors, avg time, shares


---

## Section 2: HTML Template Structure

### 1. dashboard.html
- Page container id: `dashboard-page`
- Element IDs:
  - `welcome-message` (displays username welcome)
  - `quick-stats` (display article counts, views, etc.)
  - `create-article-button` (button linking to `/article/create`)
  - `recent-activity` (feed of recent article changes and comments)

### 2. create_article.html
- Page container id: `create-article-page`
- Input IDs:
  - `article-title` (text input for article title)
  - `article-content` (textarea editor for content)
- Button IDs:
  - `save-draft-button` (to save article draft)
  - `cancel-button` (to cancel and return to previous page or dashboard)

### 3. edit_article.html
- Page container id: `edit-article-page`
- Input IDs:
  - `edit-article-title` (text input for article title)
  - `edit-article-content` (textarea editor for content)
- Button IDs:
  - `save-version-button` (to save new version)
  - `cancel-edit` (to cancel editing and return)

### 4. version_history.html
- Page container id: `version-history-page`
- Element IDs:
  - `versions-list` (list or table with version entries)
  - `version-comparison` (section to display diffs between versions)
  - `restore-version-1` (button to restore the selected version)
  - `back-to-edit-history` (button to go back to edit article)

### 5. my_articles.html
- Page container id: `my-articles-page`
- Element IDs:
  - `filter-article-status` (dropdown to filter articles by status)
  - `articles-table` (table listing user's articles)
  - `create-new-article` (button linking to create article page)
  - `back-to-dashboard` (button linking to `/dashboard`)

### 6. published_articles.html
- Page container id: `published-articles-page`
- Element IDs:
  - `filter-published-category` (dropdown filter for categories)
  - `published-articles-grid` (grid or cards showing articles)
  - `sort-published` (dropdown to sort articles)
  - `back-to-dashboard-published` (button linking to dashboard)

### 7. content_calendar.html
- Page container id: `calendar-page`
- Element IDs:
  - `calendar-view` (selector for daily/week/month views etc.)
  - `calendar-grid` (visual calendar grid for scheduled articles)
  - `schedule-button` (button to open scheduling dialog)
  - `back-to-dashboard-calendar` (button linking to dashboard)

### 8. article_analytics.html
- Page container id: `analytics-page`
- Element IDs:
  - `analytics-overview` (summary section for analytics)
  - `analytics-total-views` (display total views number)
  - `analytics-unique-visitors` (display unique visitors number)
  - `back-to-article-analytics` (button to go back to article page)


Navigation Buttons Note: All buttons linking to other pages should use routes defined under Section 1 and use the defined element IDs.

---

## Section 3: Data File Schemas

### 1. users.txt
- Format: Pipe-delimited fields
- Fields (in order):
  1. `username` (string) — unique user identifier
  2. `email` (string)
  3. `fullname` (string)
  4. `created_date` (YYYY-MM-DD format string)

- Example rows:
  ```
john|john@example.com|John Doe|2024-01-15
alice|alice@example.com|Alice Smith|2024-01-16
bob|bob@example.com|Bob Johnson|2024-01-17
admin|admin@example.com|Admin User|2024-01-10
  ```

---

### 2. articles.txt
- Format: Pipe-delimited
- Fields (in order):
  1. `article_id` (int, unique)
  2. `title` (string)
  3. `author` (string, username)
  4. `category` (enum): one of [news, blog, tutorial, announcement, press_release]
  5. `status` (enum): one of [draft, pending_review, under_review, approved, published, rejected, archived]
  6. `tags` (comma-separated strings)
  7. `featured_image` (string, URL or path, optional)
  8. `meta_description` (string)
  9. `created_date` (YYYY-MM-DD string)
  10. `publish_date` (YYYY-MM-DD HH:MM:SS string, optional)

- Example rows:
  ```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
  ```

---

### 3. article_versions.txt
- Format: Pipe-delimited
- Fields (in order):
  1. `version_id` (int, unique)
  2. `article_id` (int, linked to articles)
  3. `version_number` (int, increments per article)
  4. `content` (string, full article content)
  5. `author` (string, username)
  6. `created_date` (Datetime string, e.g. YYYY-MM-DD HH:MM:SS)
  7. `change_summary` (string, description of changes)

- Example rows:
  ```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
  ```

---

### 4. approvals.txt
- Format: Pipe-delimited
- Fields (in order):
  1. `approval_id` (int, unique)
  2. `article_id` (int)
  3. `version_id` (int)
  4. `approver` (string, username)
  5. `status` (enum): [approved, rejected, revision_requested]
  6. `comments` (string)
  7. `timestamp` (Datetime string)

- Example rows:
  ```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
  ```

---

### 5. workflow_stages.txt
- Format: Pipe-delimited
- Fields (in order):
  1. `stage_id` (int, unique)
  2. `category` (string, article category)
  3. `stage_name` (string)
  4. `stage_order` (int, defines order in workflow)
  5. `is_required` (enum): yes/no

- Example rows:
  ```
1|tutorial|Editor Review|1|yes
2|tutorial|Publisher Approval|2|yes
3|news|Editor Review|1|yes
4|announcement|Editor Review|1|yes
5|announcement|Publisher Approval|2|yes
  ```

---

### 6. comments.txt
- Format: Pipe-delimited
- Fields (in order):
  1. `comment_id` (int, unique)
  2. `article_id` (int)
  3. `version_id` (int)
  4. `user` (string, username)
  5. `comment_text` (string)
  6. `timestamp` (Datetime string)

- Example rows:
  ```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
  ```

---

### 7. analytics.txt
- Format: Pipe-delimited
- Fields (in order):
  1. `analytics_id` (int, unique)
  2. `article_id` (int)
  3. `date` (YYYY-MM-DD string)
  4. `views` (int)
  5. `unique_visitors` (int)
  6. `avg_time_seconds` (int)
  7. `shares` (int)

- Example rows:
  ```
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
  ```

---

This design specification provides full clarity on all backend Flask routes, the HTML template elements including exact element IDs, and the data file schemas with field order, types, and example data. This enables independent work for backend and frontend teams without ambiguity.
