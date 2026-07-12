# ContentPublishingHub Backend Architecture Document

---

## Section 1: Backend System Design

### Flask Application Structure

The Flask application for ContentPublishingHub will be structured in a modular and package-oriented fashion to ensure separation of concerns and maintainability.

#### Directory and Module Layout

- **app/** (Main application package)
  - __init__.py: Initializes the Flask app, registers blueprints, setup configurations, session management.
  - routes/
    - __init__.py: Initializes the routes package
    - dashboard_routes.py: Routes related to dashboard views.
    - article_routes.py: Routes handling article creation, editing, version history, analytics.
    - user_routes.py (optional): For user session/auth management if needed.
  - models/
    - __init__.py: Initialize models
    - article_model.py: Data access for articles and versions.
    - user_model.py: Data access for user-related information.
    - approval_model.py: Data access for approvals and workflow.
    - comments_model.py: Data access for comments.
    - analytics_model.py: Access analytics data.
    - workflow_model.py: Access workflow stage definitions.
  - services/
    - __init__.py
    - article_service.py: Contains business logic for article management including versioning, approval workflows.
    - analytics_service.py: Business logic for analytics aggregation.
  - utils/
    - file_handler.py: Helper functions to read/write the pipe-delimited text data files in data/ directory.
  - templates/: HTML frontend templates (served with Flask's render_template function).
  - static/: Static assets like images, CSS, JS.

### Module Responsibilities

- **routes/**: Handle HTTP requests, call appropriate services, pass data to templates, and manage responses.
- **models/**: Encapsulate all data access and parsing logic for text files storing user, article, version, approval, comment, and analytics data.
- **services/**: Contain business logic like creating article versions, processing approvals, enforcing workflow rules.
- **utils/file_handler.py**: Abstracts low-level file operations including reading and writing pipe-delimited files while ensuring concurrency and data integrity.

### Data File Management

All persistent data is stored in the `data/*.txt` files, accessed only via model layer utilizing utility functions to parse and serialize pipe-delimited text. Data files include users.txt, articles.txt, article_versions.txt, approvals.txt, comments.txt, workflow_stages.txt, analytics.txt.

Reading operations parse text files into Python data structures (lists/dicts), and writing operations overwrite files atomically to maintain consistency. Moreover, secondary indices or in-memory caches could be considered for performance optimizations.

### Data Flow Between Components

1. **Incoming Request** hits route handler in `routes/`.
2. Route calls relevant **service layer** for business logic.
3. Service layer uses **models** to retrieve or persist data from/to `data/*.txt` via `utils/file_handler.py`.
4. Service returns processed data back to route.
5. Route passes data as context variables into template for rendering.
6. Response sent back to client.

This layered approach ensures clear separation of HTTP handling, business rules, and data persistence.


## Section 2: Routing and API Endpoints

| Route                                    | Methods   | Controller Function       | Description / Input-Output                         |
|------------------------------------------|-----------|---------------------------|--------------------------------------------------|
| /dashboard                               | GET       | dashboard                 | Renders dashboard with username, stats, activities|
| /article/create                          | GET, POST | create_article            | GET: empty form; POST: create draft article      |
| /article/<int:article_id>/edit           | GET, POST | edit_article              | GET: Load article edition; POST: save new version|
| /article/<int:article_id>/versions       | GET       | article_version_history   | Show version history and optional comparisons    |
| /articles/mine                           | GET       | my_articles               | List articles owned by current user, filtering   |
| /articles/published                      | GET       | published_articles        | List all published articles with filtering/sorting|
| /calendar                               | GET       | content_calendar          | Show content schedule with view options          |
| /article/<int:article_id>/analytics      | GET       | article_analytics         | Show analytics overview for article               |

- **Dynamic Routes**: article_id is an integer URL parameter identifying specific articles.

- **Input Handling**:
  - POST routes (`/article/create`, `/article/<article_id>/edit`) accept form data for creating/saving articles.

- **Output**:
  - Routes return rendered HTML templates with context data.

- **Session and Authentication Considerations**:
  - Although user authentication is not detailed explicitly, session management should track logged-in user to provide username context.
  - Routes that modify data require verification of logged-in user ownership or permissions.
  - Access control middleware or decorators can be implemented for secure access.


## Section 3: Version Control Design

### Article Versioning and Workflow Architecture

- **Versioning**:
  - Each article maintains multiple versions stored in `article_versions.txt`.
  - Versions have a unique version_id, sequential version_number per article, content, author, timestamp, and change summary.
  - When an article is edited and saved, a new version entry is appended.

- **Approval Workflow**:
  - Approval steps tracked in `approvals.txt` with approval_id, article_id, version_id, approver, status, comments, timestamp.
  - The workflow stages defined by article category are read from `workflow_stages.txt`.
  - The system enforces that an article proceeds sequentially through required stages: for example, Editor Review followed by Publisher Approval.

- **Comments**:
  - Comments related to specific article versions are stored in `comments.txt` with identifiers linking comments to articles and versions.

- **Data Interaction**:
  - Models provide methods to query all versions tied to an article.
  - Approvals and comments are queried by article_id and version_id to build approval history and discussion threads.

- **Version History Presentation**:
  - The `/article/<article_id>/versions` route aggregates version details, approvals, and optionally comparison data.

- **State Transitions**:
  - Article status fields in `articles.txt` reflect overall state based on approvals (e.g., draft, pending_review, approved, published).


## Section 4: Frontend Integration Points

- Templates receive data through Flask's `render_template` function with context variables as specified in the design spec.

- Each route provides structured Python dicts and lists keyed by semantic names matching frontend expectation:
  - Example: `{ "username": username, "quick_stats": { ... }, "recent_activities": [...] }`

- Filtering and sorting options are passed as lists for frontend dropdowns.

- Dynamic page elements (article lists, version lists, analytics metrics) are passed as list of dicts with fields labeled in alignment with frontend naming conventions.

- For POST routes, the backend returns redirects or renders with validation error contexts to enable form interaction.

- Coordination Notes:
  - Frontend developers must implement forms with fields and buttons having specific IDs as per spec to ensure JavaScript interaction.
  - Backend APIs must supply data in predictable formats to enable UI rendering (e.g., version comparison data as dict).
  - Navigation buttons in templates depend on consistent route URLs and correct route naming in backend.

- Session-generated variables like current username must be injected into most templates to support personalized UI.


---

This architecture document provides detailed guidance for both backend and frontend teams to implement ContentPublishingHub with clear module responsibilities, route handling, version control, and frontend integration.

All backend code should strictly follow this model to maintain uniformity, testability, and scalability.

End of Document.
