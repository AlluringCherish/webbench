# ContentPublishingHub Backend Architecture Documentation

---

## Section 1: Backend System Design

### 1. Flask Application Structure

The Flask application for ContentPublishingHub is structured into the following main modules and packages:

- `app.py` (entry point)
- `routes/` (package containing route controllers for different URL endpoints)
- `models/` (package for data access and manipulation layer)
- `services/` (business logic and version control management)
- `utils/` (utility functions such as file I/O, validation, session management)
- `data/` (directory containing the pipe-delimited text data files)

#### Module Responsibilities:

- **app.py**
  - Initialize Flask app instance.
  - Register blueprints from `routes/`.
  - Setup session configuration and error handlers.

- **routes/**
  - Define route handlers (controller functions) mapped to HTTP routes.
  - Handle request input (GET/POST data).
  - Coordinate calls to `services` and `models` modules.
  - Render templates with provided context variables.

- **models/**
  - Encapsulate reading/writing to the data text files (`users.txt`, `articles.txt`, etc.).
  - Each data file has a corresponding model module class or functions to parse, update, and save records.
  - Provide methods to query/filter data for listing and retrieval by ID.
  - Handle concurrency by file locking if needed during writes.

- **services/**
  - Implement business logic including article creation, editing, versioning, approval workflow.
  - Coordinate multi-model interactions (e.g., saving an article update alongside creating a version record).
  - Handle validation logic for input data.
  - Manage approval workflows and version history data aggregation for display.

- **utils/**
  - Contain helpers for parsing date/time, generating IDs for new records.
  - Provide session helpers and authentication stubs.
  - File-based utilities for safe read/write of pipe-delimited data.

- **data/**
  - Storage location for all app data text files.
  - These files are accessed only via `models/` to enforce encapsulation.

### Data Flow Between Components

1. **Incoming HTTP request** reaches a route defined in `routes/`.
2. Route handler extracts input from request (URL params, form data).
3. For data retrieval or updates, route calls `services/` for business logic.
4. `services/` interacts with one or more `models/` modules to fetch/update data files.
5. Validation and version control logic applies in `services/`.
6. Aggregated data is returned to the route, which then renders a template passing context.

This layered design creates clear separation between routing, business logic, and data access.

---

## Section 2: Routing and API Endpoints

Below is the detailed list of Flask routes derived from design_spec.md with methods, functions, and input/output.

| Route Pattern                     | HTTP Method(s) | Controller Function      | Input/Output Description                                    |
|---------------------------------|----------------|-------------------------|------------------------------------------------------------|
| `/dashboard`                    | GET            | `dashboard()`           | Input: session user
Output: renders `dashboard.html` with `username` (str). |
| `/article/create`               | GET, POST      | `create_article()`      | GET: No input, displays form.
POST: Form data for new article draft.
Output: on success redirect; on error, render with validation errors. |
| `/article/<int:article_id>/edit`| GET, POST      | `edit_article(article_id)`| GET: loads article data and versions.
POST: updated article data for new version.
Output: render `edit_article.html` with `article` dict and `version_history` list or errors. |
| `/article/<int:article_id>/versions`| GET         | `version_history(article_id)`| Input: `article_id` to fetch versions.
Output: renders `version_history.html` with versions list and optional comparison data. |
| `/articles/mine`                | GET            | `my_articles()`         | Input: current user session.
Output: list of user's articles and filter status. |
| `/articles/published`           | GET            | `published_articles()`  | Input: optional query params for category filter and sort order.
Output: list of published articles. |
| `/calendar`                    | GET, POST      | `content_calendar()`    | GET: render with publication schedule data and view selector.
POST: receives scheduling data.
Output: updated schedule or errors. |
| `/article/<int:article_id>/analytics`| GET        | `article_analytics(article_id)`| Input: `article_id` to fetch analytics.
Output: renders analytics data structured for display. |

### Route Input & Output Details

- Routes supporting POST will handle JSON/form submissions with validation. Validation errors are passed back to templates as context.
- Dynamic routes use `<int:article_id>` capturing article identifiers directly as integers.
- User session management (e.g. current username) is consistently obtained from Flask session.
- Authentication is presumed to be handled externally or in middleware; session correctness assumed.

---

## Section 3: Version Control Design

### Architecture for Article Versioning and Approval Workflow

- **Article Versions:**
  - Stored in `article_versions.txt`, each row represents a version with fields:
    - `version_id` (unique),
    - `article_id` link,
    - `version_number` (incremented per article),
    - `content` (full textual content),
    - `author` username,
    - `created_date` timestamp,
    - `change_summary` (one-line description).
  - New versions created on edits.

- **Approval Workflow:**
  - Approvals stored in `approvals.txt` linking to specific article versions.
  - Each approval entry:
    - `approval_id` unique,
    - `article_id`,
    - `version_id`,
    - `approver` username,
    - `status` (approved, rejected, revision_requested),
    - `comments` text,
    - `timestamp`.
  - Multiple approvers may act on same version.

- **Comments:**
  - Comments linked to specific versions in `comments.txt`.

- **Workflow Stages:**
  - Defined per category in `workflow_stages.txt`.
  - Used to guide or validate article progress through editorial process.

### Interaction with Storage

- On article edit:
  - `services` creates a new version_id with incremented version_number.
  - Saves content and metadata to `article_versions.txt`.

- On approval action:
  - Approval records appended to `approvals.txt`.

- Fetching version history combines data from `article_versions.txt` and related approvals/comments.

- Version comparison data computed in business logic layer by loading relevant versions.

---

## Section 4: Frontend Integration Points

- Backend renders templates specifying exact context variables as per page requirements.
- Context variables include:
  - Simple types (str, int) e.g., `username`, `article_id`.
  - Collections (list of dicts) e.g., lists of articles, versions, analytics data.
  - Complex dict structures representing article data, version details, and analytics.

- JSON-serializable data is passed embedded in templates to enable frontend JS consumption.

- Backend ensures data consistency and necessary pre-processing (like date formatting) before passing.

- Coordination Points with Frontend Team:
  - Naming and structure of context variables must match frontend expectations (keys in dicts, field names).
  - Data structures for version histories must support rendering versions list and diffs.
  - Error message structures on form POSTs must be standardized for frontend display.
  - Pagination or filtering parameters should be planned between backend query handling and frontend controls.

- Navigation elements delegate routing to backend URLs; frontend triggers GET or POST requests accordingly.

- Templates rely on backend for initial data load; frontend may leverage embedded JSON for dynamic components.

---

This architecture documentation provides the backend design foundation covering the Flask application structure, detailed routing, version control management, and frontend integration approach needed to implement and coordinate development of the ContentPublishingHub application.

All implementation should adhere strictly to the version-controlled flat-file storage conventions and template data contracts defined here.
