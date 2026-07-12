# Content Publishing Hub Architecture and Versioning Documentation

---

## 1. Backend System Design

### 1.1 Modules and Data Management

- **Modules**: The backend is implemented as a Flask application with modular components:
  - `routes.py`: Defines all HTTP endpoints, organizing RESTful routes for articles, versions, approvals, analytics, and calendar.
  - `models.py`: Handles reading and writing from `.txt` files storing entities (articles, versions, approvals, comments, users, analytics).
  - `auth.py`: Manages user authentication and session control.
  - `workflow.py`: Contains logic for editorial workflow stages, status transitions, and validations.
  - `analytics.py`: Aggregates and processes article performance data.

- **File-based Storage**:
  - Uses structured pipe-delimited `*.txt` files stored under `data/` directory.
  - Entities are stored separately, e.g., `articles.txt`, `article_versions.txt`, `approvals.txt`, `comments.txt`, `analytics.txt`, `users.txt`, `workflow_stages.txt`, `calendar_data.txt`.
  - Reading and writing operations ensure data consistency with locking or transactional writes.

### 1.2 Versioning

- Article content is versioned, each saved as a separate entry in `article_versions.txt`.
- `version_id` uniquely identifies each version.
- Version metadata includes `article_id`, `version_number` (incremented per article), `content`, `author`, `created_date`, and a short `change_summary`.
- Backend routes support:
  - Listing all versions for an article.
  - Comparing two versions with textual diffs.
  - Restoring older versions (creating new version entries with restored content).

### 1.3 Approval Workflow

- Workflow stages configurable in `workflow_stages.txt` with fields:
  - `stage_id`, `category`, `stage_name`, `stage_order`, `is_required`.
- Approvals tracked in `approvals.txt` with unique `approval_id`, linked to a version, storing approver, status (`approved`/`rejected`/`revision_requested`), comments, and timestamp.
- Routes allow submitting approvals or rejection, with backend enforcing stage requirement logic.

---

## 2. Routing and API Endpoints

The following main endpoints define the system's HTTP interface:

### Article Management

| Route                             | Methods | Description                                  |
|----------------------------------|---------|----------------------------------------------|
| `/dashboard`                     | GET     | Displays overview dashboard with quick stats. |
| `/articles/mine`                 | GET     | List articles owned by the current user.     |
| `/articles/published`            | GET     | List and filter all published articles.      |
| `/article/create`                | GET,POST| Article creation page and submission.         |
| `/article/<article_id>/edit`    | GET,POST| Edit an article's content and save versions. |
| `/article/<article_id>/publish` | POST    | Publish the article if approved.              |
| `/article/<article_id>/submit`  | POST    | Submit article for approval workflow.         |

### Versioning

| Route                                           | Methods | Description                                    |
|------------------------------------------------|---------|------------------------------------------------|
| `/article/<article_id>/versions`                | GET     | List all versions for an article.               |
| `/article/<article_id>/versions/<version_id>`   | GET     | View specific version content and metadata.     |
| `/article/<article_id>/versions/<version_id>/compare/<other_version_id>` | GET | Compare two versions with diffs. |
| `/article/<article_id>/versions/<version_id>/restore` | POST   | Restore an older version to current state.       |

### Approval

| Route                                           | Methods | Description                                  |
|------------------------------------------------|---------|----------------------------------------------|
| `/article/<article_id>/approval`                 | GET     | View approval status and comments for article. |
| `/article/<article_id>/approval/submit`          | POST    | Submit an approval decision.                  |

### Analytics

| Route                                           | Methods | Description                                  |
|------------------------------------------------|---------|----------------------------------------------|
| `/article/<article_id>/analytics`                 | GET     | Display article analytics summary.           |
| `/article/<article_id>/analytics/data`            | GET     | Provide JSON analytics data for frontend.    |

### Calendar

| Route                                           | Methods | Description                                  |
|------------------------------------------------|---------|----------------------------------------------|
| `/calendar`                                      | GET     | View the content calendar with article schedules. |
| `/calendar/data`                                 | GET     | Serve calendar data as JSON for the frontend.   |
| `/calendar/save`                                 | POST    | Save calendar scheduling changes.            |

---

## 3. Version Control Design

- Versions tracked fully for each article with unique `version_id`.
- Versions stored incrementally in `article_versions.txt`.
- Backend facilitates:
  - Creating new versions on edits or restorations.
  - Comparing two versions showing textual differences.
  - Restoring any previous version as new current version.
- Version history visible to all users with edit rights.
- Version metadata is consistent and includes author and timestamp.

---

## 4. Frontend Integration Points

### Templates and Pages

- Implemented in Jinja2:
  - `dashboard.html`, `my_articles.html`, `create_article.html`, `edit_article.html`, `article_analytics.html`, `content_calendar.html`, `published_articles.html`, `version_history.html`.
- Includes interactive components:
  - Buttons: `create-article-button`, `save-draft-button`, `publish-button`, `cancel-button`, `schedule-button`, etc.
  - Pagination and sorting dropdowns.
  - Filters such as `filter_status_options`, `filter_published_category`.

### Data Flow

- Templates receive backend context variables corresponding to file data fields:
  - Articles: `article_id`, `title`, `author`, `category`, `status`, `tags`, `featured_image`, `meta_description`, `created_date`, `publish_date`.
  - Versions: `version_id`, `version_number`, `content`, `author`, `created_date`, `change_summary`.
  - Approvals: `approval_id`, `approver`, `status`, `comments`, `timestamp`.
  - Analytics: `views`, `unique_visitors`, `avg_time_seconds`, `shares`.

- Frontend sends GET/POST requests to backend routes for data updates and retrieval.
- Calendars load scheduling data asynchronously from `/calendar/data`.

### Authentication and Session

- Login required for all editorial, creation, approval routes.
- User data from `users.txt` manages roles (Author, Editor, Publisher, Admin).

### Interaction Flow

- Users navigate between pages using explicit buttons like:
  - `back-to-dashboard`, `back-to-article-analytics`, `back-to-dashboard-published`, etc.
- Version history supports side-by-side content comparison.
- Analytics pages show numeric stats and include charts (via JS) sourced from backend JSON.

---

# Summary

This design establishes clear boundaries and responsibilities across frontend and backend, adhering to RESTful principles and using text file storage for simplicity. It supports robust version control, approval workflows, analytics, and a calendar-driven content pipeline. The Flask app routes are logically grouped and designed for clean extension. Frontend templates and mechanisms align with backend data structures ensuring a cohesive system.
