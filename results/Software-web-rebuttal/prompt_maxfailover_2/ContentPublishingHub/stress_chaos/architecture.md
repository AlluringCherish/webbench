# ContentPublishingHub Backend Architecture Design Document

---

## Section 1: Backend System Design

### 1. Application Structure

The Flask application for ContentPublishingHub will be organized into a modular package-based structure to separate concerns and maintain scalability:

```
/content_publishing_hub/
|
|-- app/
|   |-- __init__.py          # Application factory and app setup
|   |-- routes/
|   |   |-- __init__.py
|   |   |-- dashboard.py      # Dashboard related routes and logic
|   |   |-- articles.py       # Article CRUD, editing, creation routes
|   |   |-- versions.py       # Version history and version comparison routes
|   |   |-- analytics.py      # Article analytics routes
|   |   |-- calendar.py       # Content calendar routes
|   |
|   |-- services/
|   |   |-- __init__.py
|   |   |-- data_access.py    # Functions to read/write data files in data/*.txt
|   |   |-- business_logic.py # Core logic on articles, versions, approvals
|   |   |-- version_control.py # Versioning and approval workflow management
|   |
|   |-- models/
|   |   |-- __init__.py
|   |   |-- user.py           # User data models and session management
|   |   |-- article.py        # Article data model abstraction
|   |   |-- version.py        # Article version data model
|   |   |-- approval.py       # Approval data model
|   |   |-- comment.py        # Comment data model
|   |
|   |-- templates/
|   |   |-- *.html            # Frontend templates corresponding to routes
|   |
|   |-- static/
|       |-- img/              # Static image assets
|
|-- data/
|   |-- users.txt
|   |-- articles.txt
|   |-- article_versions.txt
|   |-- approvals.txt
|   |-- workflow_stages.txt
|   |-- comments.txt
|   |-- analytics.txt
|
|-- config.py
|-- run.py                   # Entry point for Flask app
```

### 2. Module Responsibilities

- **app/__init__.py**: Initializes Flask app, registers blueprints for route modules, sets config, and session management.

- **app/routes/**
  - `dashboard.py`: Handles `/dashboard` endpoint and prepares data for the dashboard view.
  - `articles.py`: Covers article creation, editing, and listing user/published articles.
  - `versions.py`: Manages article versions, history, comparison, and restoration.
  - `analytics.py`: Fetches article analytics data for display.
  - `calendar.py`: Provides routes for content calendar GUI.

- **app/services/data_access.py**
  - Central APIs to read, parse, write, and update the various data files in `data/` (e.g., users.txt, articles.txt).
  - Provides abstractions to return data as Python dictionaries or objects.
  - Ensures thread-safe file handling with locks or atomic writes for concurrent access.

- **app/services/business_logic.py**
  - Implements core logic operations such as filtering articles by status, retrieving user-related articles, sorting, etc.
  - Encapsulates validations and business rules.

- **app/services/version_control.py**
  - Manages version creation, version comparison, approval status retrieval, and workflow stage evaluations.
  - Interfaces with `article_versions.txt`, `approvals.txt`, and `comments.txt`.

- **app/models/**
  - Defines data structures and related helper methods for users, articles, versions, approvals, and comments.
  - Provides serialization to and from file formats.

- **Templates and Static**
  - While templates and frontend code are maintained separately, backend passes data contexts to templates as per specification.

### 3. Data File Access and Management

- Files are stored in `data/` as pipe-delimited text files.
- `data_access.py` handles all reading and writing.
- Load files into memory as lists of dicts keyed by the schema fields.
- On update, transactions will re-write the entire file or append where appropriate.
- Appropriate locking (file locks or threading.Lock) will be used during writes to avoid race conditions.
- Data files accessed:
  - `users.txt` - user account information
  - `articles.txt` - main articles metadata
  - `article_versions.txt` - content versions
  - `approvals.txt` - approval records
  - `workflow_stages.txt` - workflow configurations
  - `comments.txt` - comments on versions
  - `analytics.txt` - daily article analytics

### 4. Data Flow

- Incoming HTTP Requests → Route Controller:
  - Parse inputs (e.g., form data, route params)
  - Invoke business logic and data access services
  - Update data files if POST or changes needed
  - Load refreshed data context for views
- Route Controller → Template Rendering:
  - Pass context variables (dicts, lists) according to spec
  - Handle errors and provide messages as appropriate
- Business Logic relies on models and data access abstractions
- Version control module mediates version and approval processes, keeping version histories consistent

---

## Section 2: Routing and API Endpoints

| Route Pattern                        | Methods  | Controller Function         | Inputs                       | Outputs / Response                      |
|------------------------------------|----------|-----------------------------|------------------------------|---------------------------------------|
| `/dashboard`                       | GET      | dashboard()                 | Session user info            | Render `dashboard.html` with `username`, `quick_stats`, `recent_activity`|
| `/article/create`                  | GET, POST| create_article()            | POST: Form data (title, content)     | GET: Render `create_article.html`
| POST: Validation results, status messages, redirect on success|
| `/article/<int:article_id>/edit`  | GET, POST| edit_article(article_id)    | GET: article_id param
POST: form data for update | GET: Article dict context
POST: validation messages, status|
| `/article/<int:article_id>/versions` | GET    | article_version_history(article_id)| article_id param         | Render `version_history.html` with versions list, optional comparison data|
| `/articles/mine`                  | GET      | my_articles()               | Session user info            | Render `my_articles.html` with user’s articles, filter info|
| `/articles/published`             | GET      | published_articles()        | Optional query params for filters and sorting| Render `published_articles.html` with filtered/sorted articles|
| `/calendar`                      | GET      | content_calendar()          | Optional query params           | Render `content_calendar.html` with calendar view and event data|
| `/article/<int:article_id>/analytics` | GET  | article_analytics(article_id)| article_id param           | Render `article_analytics.html` with aggregation metrics|

### Routing Details:

- Dynamic routes use `<int:article_id>` to identify specific articles.
- POST routes validate inputs before committing changes.
- Session or request context will be used to identify logged-in user (e.g., via Flask-Login or custom session mechanism).
- Authentication and authorization checks (for editing, viewing own articles) will be incorporated where relevant.
- Redirects will be used post-POST to prevent form resubmission.

---

## Section 3: Version Control Design

### Architecture Overview

- Article versioning is supported with incremental version numbers linked to each article.
- Each version is stored in `article_versions.txt`.
- Approvals for each version are tracked in `approvals.txt` with status and comments.
- Comments linked to versions are stored in `comments.txt`.
- Workflow stages (via `workflow_stages.txt`) define approval steps depending on article category.

### Data Relationships

- **article_versions.txt:** connects `version_id` to an article and version number.
- **approvals.txt:** references specific `version_id` and records approval status and comments from approvers.
- **comments.txt:** linked to `version_id` to hold discussion notes.

### Workflow

- On creating or saving a new version, a new record is appended with incremented version_number.
- Approval workflow stages are retrieved based on article category.
- Approval statuses are checked to determine if an article version is ready for publishing or requires revision.
- Comments provide context and are accessible to users viewing version history.

### Storage Interaction

- The `version_control.py` service manages reads and writes to versioning-related files.
- To restore a version, relevant `article_versions.txt` entry content is used to update the current article draft.
- Approvals and comments are loaded with versions for display.

---

## Section 4: Frontend Integration Points

### Data Passing

- Backend routes prepare context dictionaries with variables directly mapping to template placeholders as per design_spec.md.
- All template rendering calls will use Flask's `render_template` with named variables (e.g., `render_template('dashboard.html', username=user, quick_stats=stats, recent_activity=activities)`).

### Expected Data Structures

- Lists of dicts for articles, versions, recent activity, and calendar events.
- Dicts for user info, quick stats, analytics overview, and comparison data.
- Form validation messages and status messages as strings or structured error dictionaries.

### Coordination Points

- The structure of article dicts must include all fields as defined in `articles.txt` schema.
- Version dicts include detailed content and metadata matching `article_versions.txt`.
- Status, filters, and sorting options need to be consistent with frontend dropdown and selection controls.
- For dynamic element IDs (e.g., restore button related to version_id), backend sends version_id to allow rendering unique ids.

---

This architecture design document equips both backend and frontend teams with a clear understanding of system components, route behaviors, data handling patterns, versioning logic, and integration methodology to deliver the ContentPublishingHub application as described in design_spec.md.