# ContentPublishingHub Backend Architecture Document

---

## Section 1: Backend System Design

### Flask Application Structure

The backend is designed as a modular Flask application with logically separated packages and modules to ensure maintainability, scalability, and clear responsibility boundaries.

**Proposed directory structure:**

```
/content_publishing_hub/
  /app/
    __init__.py              # Flask app factory and app initialization
    /routes/
      __init__.py
      dashboard.py           # Routes and controllers for dashboard
      article.py             # Routes and controllers for article CRUD and versions
      calendar.py            # Routes and controllers for calendar
      analytics.py           # Routes and controllers for article analytics
    /services/
      __init__.py
      data_access.py         # Data access layer for reading/writing data files
      article_service.py     # Business logic related to articles and versions
      approval_service.py    # Handling approvals and workflow
      analytics_service.py   # Analytics computations and data
    /models/
      __init__.py
      entities.py            # Data classes or schemas representing domain objects
    /utils/
      __init__.py
      helpers.py             # Utility functions (e.g., date parsing, validation)
    /version_control/
      __init__.py
      version_manager.py     # Logic for managing article versions, approvals, comments
  /data/
    users.txt
    articles.txt
    article_versions.txt
    approvals.txt
    workflow_stages.txt
    comments.txt
    analytics.txt
  /templates/
    # HTML templates as per design_spec.md
  /static/
    # CSS, JS, images, assets
  config.py                 # Configuration settings
  run.py                    # Entry point to run the Flask app

### Module Responsibilities

- **routes/**: Defines Flask routes, handles HTTP request/response lifecycle, calls service layer
- **services/**: Implements business logic, interacts with data_access to retrieve or persist data
- **models/**: Defines data structures reflecting entities such as Article, User, Version, Approval
- **utils/**: Provides helper functions like parsing dates, input validation
- **version_control/**: Specialized logic for versioning articles, managing approvals and comments
- **data/**: Stores flat text files acting as the persistent data source for the application

### Data File Access and Management

- The data_access.py module centralizes reading and writing operations to `data/*.txt` files.
- It will parse files into appropriate models or data structures and serialize changes back to files.
- Concurrency control (file locking or atomic writes) should be considered to avoid corruption.
- Reading operations produce model instances or dictionaries for upper layers.
- Writing operations receive updated or new entities and update the corresponding files.

### Data Flow Between Components

- **Request received** at Flask route in `routes/` modules.
- Route handler calls relevant method in `services/` to process business logic.
- Service uses `data_access.py` to fetch or update records in data files.
- For article-related actions, `version_control/version_manager.py` provides version handling, approval and comment operations.
- The service returns domain data or status to the route.
- Route renders template with context variables or returns JSON responses.


---

## Section 2: Routing and API Endpoints

| Route                                 | HTTP Methods | Controller Function        | Description                                                                                       |
|--------------------------------------|--------------|----------------------------|-------------------------------------------------------------------------------------------------|
| /dashboard                           | GET          | dashboard()               | Displays user dashboard, quick stats, recent activity.                                         |
| /article/create                     | GET, POST    | create_article()          | GET displays form; POST handles article creation form submission.                              |
| /article/<article_id>/edit          | GET, POST    | edit_article(article_id)  | Edit article information and add new versions; GET shows edit form, POST saves.                |
| /article/<article_id>/versions      | GET          | article_version_history(article_id) | Show version history and allow comparisons, restoration.                             |
| /articles/mine                     | GET          | my_articles()             | List articles authored by logged-in user, with optional status filtering.                      |
| /articles/published                | GET          | published_articles()      | Show all published articles, filtered and sorted.                                             |
| /calendar                          | GET          | content_calendar()        | Display content publishing calendar and scheduled events.                                     |
| /article/<article_id>/analytics     | GET          | article_analytics(article_id) | Display article analytics data (views, visitors, shares).                              |

### Route Details

- Dynamic routing for article-specific pages uses `<article_id>` as an integer path parameter.
- All GET routes serve HTML templates with necessary context variables.
- POST routes handle form submissions (create/edit article).

### User Sessions and Authentication

- Although not explicitly defined in the spec, session and authentication handling should be considered.
- Possible integration points:
  - Access control for routes like `/article/<article_id>/edit`, `/articles/mine` to ensure only authorized users (authors or admins).
  - Session management for user identity retrieval to pass `username` in context.
- For initial implementation, consider a simple session state storing username, expanded in future scope.


---

## Section 3: Version Control Design

### Architecture Overview

- Article versioning is handled by the `version_control/version_manager.py` module in coordination with the `article_versions.txt`, `approvals.txt`, and `comments.txt` files.
- Each article can have multiple sequential versions identified by `version_number` and `version_id`.
- Approval workflow is tracked in `approvals.txt` with status per approver.
- Comments related to versions are stored in `comments.txt`.
- Workflow stages per category are defined in `workflow_stages.txt` for integration with approvals.

### Version History and Approval Workflow

- When a new version is saved:
  - A new record is added to `article_versions.txt` with metadata (author, timestamp, change summary).
  - The version starts at the initial workflow stage for that article category.

- Approval actions:
  - Each approval or rejection is recorded with status, approver, comments, timestamp.
  - The current approval status of a version can be derived by aggregating records for that version.
  - Workflow stages guide required approvals before publishing.

- Comments:
  - Linked to specific article versions.
  - Enable collaboration and feedback through the authoring and approval process.

### Storage Interaction

- Updates to a version or approval involve appending or modifying lines in the respective text files.
- Reads parse all relevant approvals/comments when loading version history.

---

## Section 4: Frontend Integration Points

### Passing Data to Templates

- Backend renders HTML templates using Flask's `render_template()` method, supplying context variables as specified per route in design_spec.md.
- Example: `/dashboard` renders `dashboard.html` with `username`, `quick_stats`, and `recent_activity`.
- Dynamic data like article details, versions, analytics are passed as dictionaries or lists of dicts.

### Endpoint Responses

- All GET routes respond with fully rendered HTML pages.
- POST routes handling form submissions redirect back to relevant pages or return status messages embedded in templates.
- APIs for version comparisons or analytics data are embedded as context data in page renders.

### Coordination with Frontend Design

- Backend must strictly adhere to data structures expected by frontend templates:
  - For lists of articles or versions, ensure dict elements contain all required keys as per design specification.
  - Date/time fields should be formatted consistently to ISO 8601 or the expected display format.
- ID attributes in templates correlate with backend data to enable dynamic operations (e.g., restore button linked to specific version_id).
- Any changes to backend data format must be coordinated with frontend to update rendering logic or JavaScript handling.

---

This architecture document provides a comprehensive framework for backend and frontend teams to independently implement their respective components with clear interface boundaries and data contracts.

---

*Document autogenerated based on ContentPublishingHub design_spec.md*  