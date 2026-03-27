# ContentPublishingHub Backend Architecture Document

---

## Section 1: Backend System Design

### 1.1 Flask Application Structure

The application will follow a modular Flask architecture with the following key Python packages and modules:

- `/app`
  - `__init__.py` : Initializes the Flask app, configures extensions and registers blueprints.
  - `/routes/` : Contains route modules, each managing endpoints related to specific features.
    - `dashboard_routes.py`
    - `article_routes.py`
    - `analytics_routes.py`
    - `calendar_routes.py`
  - `/models/` : Contains data access and business logic abstractions responsible for reading from and writing to the flat text data stores.
    - `user_model.py` : Manages user data from `data/users.txt`.
    - `article_model.py` : Manages articles data from `data/articles.txt`.
    - `version_model.py` : Manages article versions in `data/article_versions.txt`.
    - `approval_model.py` : Handles approval workflow data from `data/approvals.txt`.
    - `comment_model.py` : Handles comments data from `data/comments.txt`.
    - `workflow_model.py` : Manages workflow stages from `data/workflow_stages.txt`.
    - `analytics_model.py` : Handles analytics data from `data/analytics.txt`.
  - `/services/` : Contains business logic services that orchestrate complex operations involving multiple models or validations.
    - `article_service.py` : Handles creation, editing, versioning, submission for approval.
    - `analytics_service.py` : Aggregates and computes analytics metrics.
    - `approval_service.py` : Coordinates approval processes and status updates.
  - `/utils/`
    - `file_io.py` : Utility module encapsulating file reading and writing logic leveraging encoding and concurrency safety.

### 1.2 Responsibilities per Module

- **Routes Modules**: Handle HTTP request/response cycle, extract inputs from request, call appropriate services, and render templates with context variables.
- **Models**: Provide abstraction layer for persistent data, implement parsing of flat files (`.txt`), serialization, and in-memory representation.
- **Services**: Contain core business rules such as article version handling, approval workflows, analytics aggregation.
- **Utils**: Handle cross-cutting concerns such as file access, logging, configuration.

### 1.3 Data File Access and Management

All data files reside in `data/` directory with `.txt` flat files formatted using pipe (`|`) delimiters.

- Reading: Lines from the files will be read using `file_io.py` with parsing logic to split fields into dictionaries or objects.
- Writing: Updates will be serialized back to files ensuring atomic operations to prevent data corruption, and appropriate backups/version controls applied.
- Concurrency & Locking: Since files are shared resources, locking mechanisms or transactional write patterns will be implemented to avoid race conditions.
- Caching: In-memory caching strategies can be optionally implemented for read-heavy data like workflow stages, user info to optimize performance.

### 1.4 Data Flow Between Components

- Client requests (GET or POST) arrive at Flask route handlers.
- Route handlers validate and parse input, then invoke the relevant service layer functions.
- Service layer queries and updates models, performing business logic.
- Models interact with text files for persistent storage access.
- Results and data are returned to route handlers, which render frontend templates passing context variables for display.


## Section 2: Routing and API Endpoints

| Route | Methods | Function | Description | Input | Output/Template |
|-------|---------|----------|-------------|-------|-----------------|
| `/dashboard` | GET | `dashboard` | Displays user dashboard with stats and activity | Query params: none; session for username | Renders `dashboard.html` with `username`, `quick_stats`, `recent_activity` |
| `/article/create` | GET, POST | `create_article` | Creates new article; GET renders form, POST processes creation | POST form data: article fields | GET renders `create_article.html`; POST redirects or shows errors |
| `/article/<article_id>/edit` | GET, POST | `edit_article` | Edit existing article and save new version | Path param: `article_id`; POST form data: updated title/content | GET renders `edit_article.html` with article data; POST updates and redirects |
| `/article/<article_id>/versions` | GET | `article_version_history` | Show version history and comparison for an article | Path param: `article_id` | Renders `version_history.html` with versions list and comparison data |
| `/articles/mine` | GET | `my_articles` | Shows list of user’s articles with filtering | Query params: filter status | Renders `my_articles.html` with filtered articles, filter options |
| `/articles/published` | GET | `published_articles` | Shows all published articles with category filter and sort | Query params: category, sort | Renders `published_articles.html` with articles, categories, sort options |
| `/calendar` | GET | `content_calendar` | Displays content scheduling calendar | Query params: view mode | Renders `content_calendar.html` with calendar views and scheduled events |
| `/article/<article_id>/analytics` | GET | `article_analytics` | Shows analytics for a specified article | Path param: `article_id` | Renders `article_analytics.html` with analytics overview, views, visitors |

### Routing Details

- Dynamic routes use Flask style URL patterns with converters, e.g., `<int:article_id>` or `<string:article_id>`.
- HTTP methods aligned with form or data interaction: GET for rendering, POST for updates/creation.
- Input validation and sanitization performed at route or service layer.
- User authentication and session management (e.g., via Flask-Login) will be integrated at the app level to identify current user and enforce authorization; middleware decorators can restrict access to routes like create/edit.


## Section 3: Version Control Design

### 3.1 Article Versioning and Workflow

- Each article has one or more versions stored in `article_versions.txt`.
- Version identified uniquely by `version_id` and linked to `article_id` with version increment `version_number`.
- New edits create a new version row, preserving previous versions.

### 3.2 Approval Workflow

- Approval records stored in `approvals.txt` track `approver` decisions per version.
- Statuses: `approved`, `rejected`, `revision_requested`.
- Multiple approvers possible; aggregate to determine article status (e.g., all approvers must approve to move to `approved` status).
- `workflow_stages.txt` defines category-specific workflow stages to enforce review steps.
- Comments associated with versions stored in `comments.txt` facilitate review feedback.

### 3.3 Storage Interaction

- On new version save: Append to `article_versions.txt`.
- On approval decision: Append to `approvals.txt`.
- Comments saved into `comments.txt` linked by `article_id` and `version_id`.
- Article status updates reflected in `articles.txt` to reflect current state (draft, approved, published, etc.).


## Section 4: Frontend Integration Points

### 4.1 Passing Data to Templates

- Data context passed from route controllers to Jinja2 templates aligns with specified context variables per route in the design spec.
- Variables such as `username`, `articles`, `versions`, `analytics_overview` are passed as dictionaries, lists, or primitives matching frontend expectations.
- Date and datetime fields are formatted server-side to ISO strings or human-readable formats prior to template context.

### 4.2 Endpoint Responses for Rendering

- All GET endpoints render HTML templates with required data.
- POST endpoints typically perform action then redirect (Post/Redirect/Get pattern) to avoid duplicate submissions.
- JSON responses can be added for API endpoints if frontend requires asynchronous data fetch (not currently specified).

### 4.3 Coordination Points with Frontend

- Data structures for lists (e.g., articles, versions) must include all displayed attributes needed for UI components such as filters and tables.
- Dropdown options (statuses, categories, sort options) must be passed dynamically to templates.
- Navigation URLs embedded in templates must correspond exactly to Flask routes.
- Buttons and form inputs need backend support to handle submitted data fields with matching keys.
- Date and time format consistency must be agreed for display.

---

This architecture document provides the backend design blueprint and integration details needed for independent backend and frontend implementation teams to proceed concurrently while ensuring alignment on data flow, routing, version handling, and user interface context.

---

End of Document
