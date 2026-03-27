# ContentPublishingHub Architecture Design Document

---

## 1. Backend System Design

### 1.1 Flask Application Structure

The Flask application is structured modularly with clear separation of concerns to handle routing, business logic, data management, and version control.

#### Directory and Module Organization

- `app/`
  - `__init__.py` : Flask app factory and app initialization.
  - `routes/`
    - `dashboard.py` : Handles `/dashboard` route.
    - `article.py` : Manages article-related routes including creation, editing, versions, and analytics.
    - `user_articles.py` : Handles routes concerning user’s own articles.
    - `published.py` : Dedicated route for published articles display.
    - `calendar.py` : Manages content calendar display.
  - `services/`
    - `article_service.py` : Business logic for articles, including creation, retrieval, updating, and version control.
    - `approval_service.py` : Logic for managing approvals and workflow stages.
    - `analytics_service.py` : Aggregation and retrieval of article analytics data.
    - `user_service.py` : User session and data handling.
  - `data_access/`
    - `file_manager.py` : Interfaces with data files stored in `data/` directory, read/write operations.
  - `models/`
    - Define data models or schemas reflecting the structure of data files, used for parsing and validation.

### 1.2 Data File Usage and Access

The backend uses flat text files under the `data/` folder as persistent storage with explicit formats:

- `users.txt` : User accounts and information.
- `articles.txt` : Article metadata.
- `article_versions.txt` : Version histories for articles.
- `approvals.txt` : Approval records per version.
- `workflow_stages.txt` : Definition of workflow steps per article category.
- `comments.txt` : Comments on article versions.
- `analytics.txt` : Article performance metrics.

Each service layer interacts with these files through the `file_manager.py` component ensuring data integrity, parsing, and proper locking where necessary.

### 1.3 Data Flow

- **Request Handling:** Flask routes receive HTTP requests, validate inputs, and call appropriate service methods.
- **Business Logic:** Service layer handles processing, including article creation, versioning updates, approval state management, analytics summary, and user data operations.
- **Data Persistence:** Services delegate file read/write operations to the data access layer that parses and serializes data files.
- **Template Rendering:** Processed data or context variables are passed to Jinja frontend templates.

This layered approach enables clear separation of concerns and easier unit testing.

---

## 2. Routing and API Endpoints

| Route                                 | Method(s)    | Controller Function        | Description & Inputs                                                                                       | Outputs / Template Context                                          |
|--------------------------------------|--------------|----------------------------|-----------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------|
| `/dashboard`                         | GET          | `dashboard`                | Session-based authentication to identify current user.                                                    | `username`: str, `quick_stats`: dict, `recent_activity`: list dict |
| `/article/create`                    | GET, POST    | `create_article`           | GET: no input; POST: article form data (title, content)                                                   | GET: render form; POST: `success_flag` bool, `errors` dict          |
| `/article/<article_id>/edit`        | GET, POST    | `edit_article`             | `article_id`: int from URL; POST accepts updated article data                                             | `article` dict, `errors` dict, `current_version` str                |
| `/article/<article_id>/versions`    | GET          | `article_version_history`  | `article_id`: int; fetch all versions and comparison data                                                 | `article_id`: int, `versions`: list of dicts, `comparison_data`: dict |
| `/articles/mine`                    | GET          | `my_articles`              | Session user identified; optional filter query parameter for status                                        | `articles`: list dict, `filter_status_options`: list str           |
| `/articles/published`               | GET          | `published_articles`       | Accepts optional query params for category and sorting                                                    | `published_articles`: list dict, `category_options`: list, `sort_options`: list |
| `/calendar`                        | GET          | `content_calendar`         | No direct inputs                                                                                           | `calendar_data`: dict/list, `view_options`: list                   |
| `/article/<article_id>/analytics`  | GET          | `article_analytics`        | `article_id`: int                                                                                        | `analytics_overview`: dict, `total_views`: int, `unique_visitors`: int |

### 2.1 Dynamic Route Handling

- Routes with ` <article_id> ` are parameterized to accept integer article identifiers.
- Controllers validate the existence and authorization on the article corresponding to `article_id`.

### 2.2 Session Management and Authentication

- Each route expects a logged-in user identified via session or token.
- Authorization checks occur especially on protected routes like article editing or viewing user-specific data.
- Session management is handled centrally in middleware or user service.

---

## 3. Version Control Design

### 3.1 Architecture Overview

- Article versioning enables tracking each change as a separate version with metadata.
- Versions are stored in `article_versions.txt` and linked by `article_id`.
- Each version includes author, timestamp, content snapshot, and change summary.

### 3.2 Approval Workflow

- Approval statuses (approved, rejected, revision_requested) for specific versions are recorded in `approvals.txt`.
- Multiple approvers may record sequential or parallel approvals.
- `workflow_stages.txt` defines the ordered stages per article category and if these are required.
- Approval workflow design coordinates stage transitions per version state.

### 3.3 Comments and Version Feedback

- Comment entries in `comments.txt` link to specific `article_id` and `version_id`.
- Comments can be added by any user with access and provide version-specific feedback.

### 3.4 Backend Interaction

- Backend services read and update files with the following logic:
  - When new versions are saved, append new record to `article_versions.txt` with incremental version number.
  - Upon approvals, update `approvals.txt` with approval records.
  - Comments are appended to `comments.txt` with metadata.
  - Workflow steps are referenced from `workflow_stages.txt` to check current status and required next steps.

---

## 4. Frontend Integration Points

### 4.1 Data Passing to Templates

- Backend routes render specified Jinja templates with explicit context variables as per design spec for each route.
- Context variables strictly follow types and naming conventions in the design spec for consistency.

### 4.2 Response Structures

- Context data structures (dicts, lists of dicts) are carefully formed in the backend services to fulfill frontend rendering needs:
  - Example: `versions` in `/article/<article_id>/versions` is a list of dicts with keys `version_id`, `version_number`, `author`, `created_date`, `change_summary`.
  - Analytics metrics aggregate from `analytics.txt` per article.

### 4.3 Integration Requirements

- Coordination with frontend is required to ensure element IDs as specified are present in HTML templates for proper UI behavior.
- Frontend relies on provided data to populate forms, tables, grids, and charts.
- Navigation workflows (e.g., buttons linking between pages) need to use correct URL routes.
- Error and success flags must be handled to provide responsive user feedback on POST operations.

---

This document provides a definitive guide for backend and frontend teams to independently develop the ContentPublishingHub system in alignment with the agreed design specification.