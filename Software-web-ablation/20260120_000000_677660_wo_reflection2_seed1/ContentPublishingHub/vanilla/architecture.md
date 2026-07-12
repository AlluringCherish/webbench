# ContentPublishingHub Backend Architecture

---

## Section 1: Backend System Design

### 1. Flask Application Structure

The Flask application will be organized as a modular package with a clear separation of concerns among routing, data access, business logic, and version control components.

```
content_publishing_hub/
│
├── app.py                  # Flask app instantiation and configuration
├── config.py               # Configuration settings (e.g., file paths, debug)
├── requirements.txt        # Python dependencies
├── routes/                 # Flask route handlers (controllers)
│   ├── __init__.py
│   ├── dashboard.py
│   ├── articles.py
│   ├── versions.py
│   ├── calendar.py
│   └── analytics.py
├── services/               # Business logic layer
│   ├── __init__.py
│   ├── article_service.py
│   ├── user_service.py
│   ├── version_service.py
│   ├── approval_service.py
│   ├── comment_service.py
│   └── analytics_service.py
├── data_access/            # Data access layer for file operations
│   ├── __init__.py
│   ├── user_dao.py
│   ├── article_dao.py
│   ├── version_dao.py
│   ├── approval_dao.py
│   ├── comment_dao.py
│   └── analytics_dao.py
├── models/                 # Data model definitions (schemas as classes/dicts)
│   ├── __init__.py
│   ├── user.py
│   ├── article.py
│   ├── version.py
│   ├── approval.py
│   ├── comment.py
│   └── analytics.py
├── utils/                  # Shared utilities (e.g., parsing, validation)
│   ├── __init__.py
│   └── file_utils.py       # Includes helpers for reading/writing text files
├── templates/              # Jinja2 templates for frontend
├── static/                 # Static assets (css, js, images)
└── data/                   # Data files (users.txt, articles.txt, etc.)

```

### 2. Module Responsibilities

- **app.py**: Initialize and configure Flask app, register blueprints for route modules.
- **routes/**: Define Flask route controllers mapped to URLs, handle HTTP methods,
  parse request data, and pass results to templates.

  - `dashboard.py`: Dashboard related routes.
  - `articles.py`: Article creation, editing, listing.
  - `versions.py`: Article version history and comparisons.
  - `calendar.py`: Content calendar viewing and scheduling.
  - `analytics.py`: Article analytics presentation.

- **services/**: Encapsulate business logic such as article versioning, approval workflow,
  validation rules, and operations combining multiple data sources.

- **data_access/**: Direct interaction with data files residing in `data/`. Responsible for:

  - Reading and parsing pipe-delimited `.txt` files into Python data structures.
  - Writing updates back to files ensuring data integrity.
  - Providing search, filter, and pagination functions as needed.

- **models/**: Define data schemas as classes or structured dicts, providing clarity on fields,
  types, and facilitating deserialization from raw file data.

- **utils/file_utils.py**: Implement the low-level `write_text_file` function, read helpers,
  and concurrency controls (e.g., locks) when updating files.

### 3. Data File Access and Management

- All persistent data is stored in the `data/` folder as pipe-delimited text files.
- Data Access Objects (DAOs) in the `data_access/` layer implement CRUD operations for each file.
- Updates to data files are done via atomic write operations using `write_text_file` utility.
- Reads parse entire file content into in-memory Python objects; writes serialize changes back.
- Versioning related files (`article_versions.txt`, `approvals.txt`, `comments.txt`) are consistently
  accessed and maintained to reflect current state.

### 4. Data Flow Between Components

- **Client Request** ➔ handled by `routes/` module ➔ invokes appropriate `services/` function
  ➔ which calls `data_access/` DAO for file operations

- **Data returned** from DAO ➔ processed/enriched by `services/` ➔ passed to `routes/`

- `routes/` renders Jinja2 templates with context variables (or JSON for APIs if needed)

- POST routes handle form data, validate via `services/`, persist changes, then redirect or re-render.

---

## Section 2: Routing and API Endpoints

| Route Pattern                      | HTTP Method(s) | Controller Function      | Input / Parameters                              | Output / Response                          |
|----------------------------------|----------------|-------------------------|------------------------------------------------|--------------------------------------------|
| `/dashboard`                     | GET            | dashboard               | User session (to identify username)             | Render `dashboard.html` with user context |
| `/article/create`                | GET, POST      | create_article          | GET: none; POST: form data for new article     | GET: render form; POST: validate, redirect or error context |
| `/article/<int:article_id>/edit` | GET, POST      | edit_article            | article_id from URL; POST: updated article data| Render edit form with article data and validation errors |
| `/article/<int:article_id>/versions` | GET          | article_version_history  | article_id from URL                            | Render version_history.html with versions list and optional comparison |
| `/articles/mine`                 | GET            | my_articles             | User session (username), optional filter params| Render my_articles.html with filtered articles list |
| `/articles/published`            | GET            | published_articles      | Optional query params: category filter, sort   | Render published_articles.html with articles grid |
| `/calendar`                     | GET, POST      | content_calendar        | GET: none; POST: calendar scheduling data       | GET: render calendar; POST: update result or errors  |
| `/article/<int:article_id>/analytics` | GET         | article_analytics       | article_id from URL                             | Render article_analytics.html with metrics |

### Session and Authentication

- Backend will manage logged-in user sessions via Flask session management.
- User identity from session used for personalization (e.g., username context).
- Routes requiring authentication will check session; redirect to login if unauthenticated.
- No explicit user login route detailed here; assumed to be handled externally or as a separate module.


---

## Section 3: Version Control Design

### 1. Article Versioning Architecture

- Every article edit that results in content changes creates a new version entry in `article_versions.txt`.
- Each version includes `version_id`, `article_id`, `version_number`, full `content`, `author`,
  `created_date`, and a short `change_summary` describing the update.

- The version number increments sequentially per `article_id`.

### 2. Approval Workflow

- Approval data stored in `approvals.txt` links to a specific `article_id` and `version_id`.
- Approval records include `approval_id`, approver username, status (`approved`, `rejected`, `revision_requested`),
  comments, and timestamp.

- Approval workflow stages (from `workflow_stages.txt`) define ordered steps per article category.
- The system can enforce progression through required stages before final publishing.

### 3. Comments on Versions

- Comments on article versions are stored in `comments.txt`, associating comments with
  `article_id` and `version_id`.
- Comments include `comment_id`, username of commenter, comment text, and timestamp.

### 4. Storage Interaction

- Data Access Objects for versions, approvals, and comments provide methods to:
  - Create/read version entries
  - Fetch approval history and current status
  - Add and retrieve comments

- Updates leverage `write_text_file` to persist changes reliably.

- Services layer consolidates data for presentation (e.g., version comparison, history view).

---

## Section 4: Frontend Integration Points

### 1. Template Data Passing

- Each route handler renders a Jinja2 template returning HTML.
- Context variables passed to templates are derived from design_spec.md Section 1 routes table.
- Data structures such as lists of dicts, single dicts, or optional context variables match expected front-end consumption.

Example:
- For `/dashboard`, template receives `username` (str) and additional statistics.
- For version history, list of versions includes fields required to populate the `<ul id="versions-list">`.

### 2. Endpoint Response Contracts

- GET routes typically render templates with full context variables.
- POST routes either redirect after successful updates or re-render the form with validation errors.
- AJAX or API JSON responses may be supported for future extensibility but are not specified here.

### 3. Frontend and Backend Coordination

- Frontend teams rely on backend documentation for variable names and types to bind data to UI elements.
- Critical template element IDs and expected context variables from design_spec.md ensure synchronization.
- Backend must ensure data consistency especially for dynamic pages like edit article, version history, and analytics.

---

# Summary

This architecture provides a clean, modular Flask backend structure with focused responsibilities and explicit data flows.
The version control and approval workflow are tightly integrated with file-based persistent storage via DAOs.
Routing and context variable contracts enable seamless frontend integration based on predefined templates.

The architecture.md document supports independent development of backend and frontend components with clear interfaces and data expectations.
