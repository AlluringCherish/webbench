# ContentPublishingHub Backend Architectural Design

---

## Section 1: Backend System Design

### 1. Flask Application Structure

The Flask application for ContentPublishingHub will be organized into a modular and layered structure for maintainability, scalability, and clear separation of concerns:

```
/content_publishing_hub/
|-- app.py                     # Flask application factory and app initialization
|-- config.py                  # Configuration settings (environment, paths, etc.)
|-- /controllers/              # Request handling and routing logic
|    |-- dashboard.py
|    |-- articles.py
|    |-- calendar.py
|    |-- analytics.py
|    |-- __init__.py
|-- /models/                   # Data access layer interacting with data/*.txt files
|    |-- user_model.py
|    |-- article_model.py
|    |-- version_model.py
|    |-- approval_model.py
|    |-- comment_model.py
|    |-- workflow_model.py
|    |-- analytics_model.py
|    |-- __init__.py
|-- /services/                 # Business logic layer handling workflows, validation, versioning
|    |-- article_service.py
|    |-- versioning_service.py
|    |-- approval_service.py
|    |-- analytics_service.py
|    |-- __init__.py
|-- /utils/                    # Utility modules (file operations, version control management, helpers)
|    |-- file_io.py            # Read/write for data/*.txt files
|    |-- version_control.py    # Versioning logic (diff generation, history management)
|    |-- validation.py
|    |-- __init__.py
|-- /templates/                # Frontend HTML templates (as per design_spec.md)
|-- /static/                   # Static files: CSS, JS, Images
|-- requirements.txt
|-- README.md

```

### 2. Module Responsibilities

- **app.py:** Entry point creating Flask app, registering blueprints from controllers, setting up config.
- **controllers/**: Defines route handlers (e.g., dashboard, article creation/editing, version history, analytics).
  - Each file targets related routes and coordinates input parsing, session handling, calling services, and response rendering.
- **models/**: Manages reading/writing of raw persistent data stored in flat text files located under `data/` directory.
  - Implements file parsing, data representation (e.g., users, articles, versions).
  - Handles concurrency control if necessary when writing files.
- **services/**: Implements business rules, workflows, version control, approval processing.
  - Coordinates complex operations spanning multiple models.
- **utils/file_io.py:** Provides robust abstractions for file access to read/write lines, parse to dicts, write back, ensuring data consistency.
- **utils/version_control.py:** Manages version comparison, diff generation logic required for version history page.
- **templates/**: HTML templates rendered by controllers passing the context variables.

### 3. Data File Access and Management

- All application data is persisted in the `data` folder as flat text files with `|` delimited fields.
- Each model corresponds to a data file: `users.txt`, `articles.txt`, `article_versions.txt`, `approvals.txt`, `comments.txt`, `workflow_stages.txt`, `analytics.txt`.
- Models provide methods such as `get_all()`, `get_by_id()`, `create()`, `update()`, and `filter()`.
- On updating (e.g., adding new article version), models append new records to the respective files.
- Read operations on these files are optimized in-memory caching if needed (optional based on scale), but always ensure fresh read on critical operations.

### 4. Data Flow Between Components

1. **Request Received:** Controller receives HTTP request.
2. **Input Parsing:** Controller extracts parameters/query/form data.
3. **Business Logic:** Controller calls services for operations like article creation, version management, approvals.
4. **Data Access:** Services interact with models to read/write data files.
5. **Response Preparation:** Services return data or status to controller.
6. **Template Rendering:** Controller passes data context to frontend templates.
7. **Response Sent:** Flask sends the rendered HTML or JSON response back to client.

---

## Section 2: Routing and API Endpoints

The routing scheme aligns strictly with the design_spec.md routes and HTTP methods.

| Route Pattern                      | Methods  | Controller Function           | Input                                    | Output/Context Variables                               |
|----------------------------------|----------|------------------------------|-----------------------------------------|-------------------------------------------------------|
| `/dashboard`                     | GET      | dashboard()                  | Session user info                         | `username`, `quick_stats` (dict), `recent_activity` (list of dicts) |
| `/article/create`                | GET, POST| create_article()             | POST form: `article_title`, `article_content`         | On GET: None; On POST: success/error messages           |
| `/article/<int:article_id>/edit`| GET, POST| edit_article(article_id)     | URL param `article_id`, POST form: edited title & content | `article_id`, `title`, `content`                    |
| `/article/<int:article_id>/versions`| GET   | article_version_history(article_id) | URL param `article_id`                            | `article_id`, `versions` (list of dicts), `comparison` (dict), `current_version` (int) |
| `/articles/mine`                | GET      | my_articles()                | Session user info, optional query filter status        | `articles` (list of dicts), `filter_status`              |
| `/articles/published`           | GET      | published_articles()         | Optional query: `filter_category`, `sort_option`        | `articles` (list of dicts), `filter_category`, `sort_option`|
| `/calendar`                    | GET, POST | content_calendar()           | POST form: calendar events or schedules                 | `calendar_view` (str), `calendar_data` (list or dict)     |
| `/article/<int:article_id>/analytics`| GET  | article_analytics(article_id) | URL param `article_id`                            | `article_id`, `analytics` (dict)                         |

### Dynamic Routes

- Routes like `/article/<article_id>/edit`, `/article/<article_id>/versions`, and `/article/<article_id>/analytics` use integer `article_id` URL path parameters.

### User Sessions and Authentication

- The system expects an authentication mechanism (e.g., login sessions) to provide `username` and user role context.
- Controllers extract session user data to determine access rights (e.g., authors can edit their own articles).
- Session management (login/logout) is assumed implemented but outside the scope of this document.

---

## Section 3: Version Control Design

### 1. Article Versioning Model

- Each article can have multiple versions tracked in `article_versions.txt`.
- Version entries have `version_id`, `article_id`, `version_number`, `content`, `author`, `created_date`, and `change_summary`.
- Version numbers increment sequentially per article.

### 2. Version History and Comparison

- The architecture supports retrieving all versions for an article.
- Diff/Comparison logic implemented in `utils/version_control.py` generates changes summary for UI.
- Users can view version changes on the `/article/<article_id>/versions` page.

### 3. Approval Workflow

- Approvals are recorded in `approvals.txt` referencing article and version.
- Approval entries include status (approved, rejected, revision_requested), approver comments, and timestamp.
- The workflow stages from `workflow_stages.txt` define mandatory reviews per category.
- Services orchestrate moving articles through approval stages accordingly.

### 4. Comments on Versions

- Comments made by users on specific versions are saved in `comments.txt`.
- Comments include comment text, author, timestamp, and link to version and article.

### 5. Storage Interaction

- On article version save, a new record appends to `article_versions.txt`.
- Approval submissions append records to `approvals.txt`.
- Comments saved by appending to `comments.txt`.
- Version and approval lookup uses corresponding models parsing these files.

---

## Section 4: Frontend Integration Points

### 1. Data Passing to Frontend Templates

- Controllers pass data as context variables to templates using Flask's `render_template()`.
- Context variable keys correspond to those listed per route in design_spec.md to ensure consistent frontend data binding.
- E.g., `dashboard()` passes `username`, `quick_stats`, `recent_activity` variables.

### 2. Endpoint Responses

- Most routes respond to GET requests by rendering templates with populated context.
- POST routes handle form submissions and return the same template with success/error messages in context for display by frontend.
- For dynamic pages with data filtering or state change (e.g., calendar POST), updated context is passed for re-render.

### 3. Coordination Points with Frontend Team

- Frontend expects specific data structures:
  - Lists of dicts for articles and versions with specific keys matching data fields.
  - Dictionary structures for analytics and quick stats.
  - Strings or enums for filters and status values.
- Naming conventions of context variables must be consistent.
- Pagination, sorting, and filtering parameters passed from frontend must be supported in backend (via query params or POST forms).
- Backend must handle validation and provide meaningful error messages to be rendered by frontend UI elements.

---

This architecture.md serves as the definitive guide enabling backend and frontend teams to develop ContentPublishingHub independently yet consistently following this design blueprint.


