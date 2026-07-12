# ContentPublishingHub Architecture Design Document

---

## Section 1: Backend System Design

### Flask Application Structure

The Flask application will be structured into modular packages and modules to separate concerns and enable maintainable, scalable development:

- **app/** (main application package)
  - `__init__.py`: Initializes the Flask app instance, sets configuration, and registers blueprints
  - **routes/**: Contains route handler modules organized by functional areas
    - `dashboard.py`: Routes and logic for dashboard page
    - `article.py`: Routes managing article creation, editing, versions, and analytics
    - `articles_listing.py`: Routes for listing user's articles and published articles
    - `calendar.py`: Routes for content calendar page
  - **services/**: Business logic layer handling data processing, validation, and coordination
    - `article_service.py`: Article management, version control, approval workflows
    - `analytics_service.py`: Analytics data aggregation and retrieval
    - `user_service.py`: User-related operations and session management
  - **data_access/**: Data Access Layer (DAL) managing reading and writing data from/to text files
    - `file_repository.py`: Abstracts file I/O operations for all data files (`users.txt`, `articles.txt`, etc.)
  - **utils/**: Utility functions (e.g., date parsing, common helpers)
  - **auth/**: Optional module for session and authentication management (not fully specified but prepared for future)

### Module Responsibilities

- **Routes Modules**: Responsible purely for receiving HTTP requests, extracting parameters, invoking corresponding service functions, and returning rendered templates or redirects.

- **Services Modules**: Contain core logic for managing articles, versions, approvals, comments, analytics, and user-related functions. Implements workflows and business rules.

- **Data Access Layer**: Provides consistent, thread-safe file read/write interfaces to the underlying `.txt` data files. Facilitates loading and saving structured data as Python dictionaries or objects.

- **Utilities**: Provide helper methods for formatting, date conversions, file path handling, etc.

### Data File Access and Management

- Data files located under `data/` directory (e.g., `data/articles.txt`, `data/article_versions.txt`) will be opened in read or append/write mode as needed.

- All file accesses will be encapsulated by `file_repository.py` to handle parsing lines into structured dicts, searching by keys (e.g., `article_id`), and writing back updates safely.

- For concurrency control, simple file locks or synchronized write operations will be applied if necessary.

### Data Flow

Example flow for editing an article:
1. User requests `/article/<article_id>/edit` (GET).
2. Route handler loads article metadata and latest version content using the service layer.
3. Service layer calls data access to retrieve `articles.txt` and latest version in `article_versions.txt`.
4. Data sent as context variables to template `edit_article.html`.
5. On POST to same route, form data captured, validated, and service layer creates a new version entry.
6. Data access writes updated version to `article_versions.txt`.
7. User redirected to appropriate page.

This modular approach ensures separation between presentation (routes/templates), business logic (services), and data persistence (data access).

---

## Section 2: Routing and API Endpoints

### Defined Flask Routes

| Route URL Pattern                | HTTP Method(s) | Controller Function     | Input                     | Output (Template & Context)                                                  |
|--------------------------------|----------------|------------------------|---------------------------|------------------------------------------------------------------------------|
| `/dashboard`                   | GET            | `dashboard`            | session user info          | `dashboard.html` with username, quick_stats, recent_activity                  |
| `/article/create`              | GET, POST      | `create_article`       | (GET: none), (POST: form data title, content) | `create_article.html` (GET), redirect after POST                             |
| `/article/<int:article_id>/edit` | GET, POST  | `edit_article`         | article_id (URL), (POST form data version content) | `edit_article.html` with article info, redirect after POST                   |
| `/article/<int:article_id>/versions` | GET, POST | `version_history`     | article_id (URL), (POST: version comparison/restore actions) | `version_history.html` with versions_list and comparison                      |
| `/articles/mine`               | GET            | `my_articles`          | session user info          | `my_articles.html` with user's articles, filter options                      |
| `/articles/published`          | GET            | `published_articles`   | query params (optional sorting/filtering) | `published_articles.html` with articles grid, filters, sorting options       |
| `/calendar`                   | GET            | `content_calendar`     | none                      | `content_calendar.html` with calendar views and events                      |
| `/article/<int:article_id>/analytics` | GET      | `article_analytics`    | article_id (URL)           | `article_analytics.html` with analytics data                                 |

### Dynamic Route Patterns

- Routes accepting `article_id` parameters enforce integer type and load respective article data.
- Version history route manages article versions dynamically.

### User Sessions and Authentication

- User identity assumed managed via session, with `username` stored on login.
- Certain routes like `/articles/mine` rely on session to display personalized data.
- Authentication middleware or decorators to be integrated as needed (not specified here).

---

## Section 3: Version Control Design

### Article Versioning and Workflow

- Each article maintains multiple versions stored in `article_versions.txt` with sequential version numbers.
- New versions are created on edits.
- Approval workflow stages defined per category in `workflow_stages.txt`.
- Each version can have multiple approval records in `approvals.txt` representing different approvers and their decisions.
- Comments linked to specific versions stored in `comments.txt`.

### Relationships

- `article_versions.txt` entries relate to `articles.txt` by article_id.
- `approvals.txt` entries link to article_id and version_id, representing approval status and remarks.
- `comments.txt` connect users' feedback to article versions.

### Storage Interaction

- Version creation appends new entries to `article_versions.txt`.
- Approval decisions update `approvals.txt` with timestamped records.
- Commenting appends to `comments.txt`.
- Services layer abstracts logic retrieving version history, current approval state, comments.

- Restore version action (from `/article/<article_id>/versions`) sets current working content to selected version, typically by creating a new version copying restored content.

---

## Section 4: Frontend Integration Points

### Data Passing and Template Rendering

- Routes return `render_template()` calls providing explicitly named context variables as per design specs to frontend templates.
- Context variables match expected frontend IDs and data structures (e.g., lists of dicts, strings, integers) for dynamic rendering.

### Endpoint Response Expectations

- GET routes deliver initial page contexts to enable fully populated views.
- POST routes generally perform state changes then redirect to prevent double form submissions.

### Coordination with Frontend Design

- Context variable naming and data structures must be consistent with frontend element IDs and expected data types:
  - e.g., `dashboard` passes `username` string matching `welcome-message` element.
  - `version_history` passes lists and dicts for rendering versions and comparison sections.

- Certain elements like buttons, dropdowns require backend to supply options (e.g., filter status, sort options).

- Version comparison and restoration require structured data returned that frontend can render clearly.

- Analytics views require aggregated metrics passed as dictionaries and counts matching frontend display elements.

---

This architecture document enables the backend and frontend implementation teams to develop independently while maintaining consistency and integration alignment based on well-defined modules, routes, workflows, data management, and templating contracts.

---

*End of Document*
