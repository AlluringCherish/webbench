# ContentPublishingHub Backend Architecture Design Document

---

## Section 1: Backend System Design

### 1. Flask Application Structure

The Flask application for ContentPublishingHub will be organized into modular packages and modules to isolate responsibilities, facilitate maintenance, and support scalability:

- **app/**
  - `__init__.py`: Initializes Flask app instance, configures extensions and registers blueprints.
  - **routes/** (package): Contains route handler modules mapped to major functional areas.
    - `dashboard.py`: Handles routes under `/dashboard`.
    - `articles.py`: Routes for article create, edit, listing, versions.
    - `calendar.py`: Routes for content calendar views.
    - `analytics.py`: Routes for article analytics.
  - **models/** (package): Data access and domain logic modules responsible for reading/writing the text data files.
    - `user_model.py`: Encapsulates user data interaction with `users.txt`.
    - `article_model.py`: Handles articles and metadata from `articles.txt`.
    - `version_model.py`: Manages article versions from `article_versions.txt`.
    - `approval_model.py`: Manages approval workflows from `approvals.txt`.
    - `comment_model.py`: Handles comments from `comments.txt`.
    - `workflow_model.py`: Workflow stages from `workflow_stages.txt`.
    - `analytics_model.py`: Analytics data access for `analytics.txt`.
  - **services/** (package): Business logic layer that orchestrates data operations for features.
    - `article_service.py`: Implements article creation, editing, versioning, approval workflows.
    - `analytics_service.py`: Aggregates analytics metrics.
    - `calendar_service.py`: Builds scheduled content views.
  - **utils/** (package): Utility modules for common tasks such as date parsing, data validation.
  - `auth.py` (optional): Handles user session and authentication if implemented.

### 2. Responsibilities of Each Module

- **Route modules** define Flask routes, handle input request data, invoke service layer, and return rendering context or JSON.
- **Model modules** isolate file I/O with the flat text files, provide read/write/manipulate operations returning domain objects/dicts.
- **Services** contain business rules such as version number increments, approval status transition rules.
- **Utils** provide helpers like parsing dates, formatting data, common validations.
- **Auth module** (if added) manages user session state, enforcing route access controls.

### 3. Data File Access and Management

- The application uses plain text files stored in `data/` folder to store persistent data.
- Models encapsulate file reading/writing ensuring data consistency.
- To read data, models parse lines into domain objects (dicts) for usage in services and routes.
- To write data, models serialize domain objects back to the respective text file.
- Concurrent write operations should be synchronized via file locks or atomic write patterns to prevent data corruption.

### 4. Data Flow

User actions (via frontend) invoke HTTP requests which reach corresponding Flask route functions. Route functions:
- Validate/parse incoming data.
- Call service layer methods to execute business logic, which utilize the models for data access.
- Models read/write the data files, return domain data.
- Service packages compose the data and prepare output context.
- Routes send context to frontend templates for rendering or redirect based on result.

This layered flow promotes separation of concerns and testability.

---

## Section 2: Routing and API Endpoints

Below are the endpoints derived from design_spec.md with HTTP methods, controller mappings, and I/O descriptions:

| Route Pattern                              | Methods   | Controller (Function)          | Input                                      | Output / Template              |
|--------------------------------------------|-----------|-------------------------------|--------------------------------------------|-------------------------------|
| /dashboard                                 | GET       | dashboard()                   | Session user info                          | Render `dashboard.html` with username, quick_stats, recent_activity context|
| /article/create                            | GET, POST | create_article()              | (GET) None
(POST) form data (title, content)         | (GET) Render `create_article.html`
(POST) Redirect or re-render with errors|
| /article/<int:article_id>/edit             | GET, POST | edit_article(article_id)      | (GET) None
(POST) form data for new version content| (GET) Render `edit_article.html` with article data
(POST) Save version, redirect or re-render|
| /article/<int:article_id>/versions         | GET       | article_version_history(article_id) | None                                     | Render `version_history.html` with versions_list, optional comparison_data|
| /articles/mine                             | GET       | my_articles()                 | Optional query filter for status?           | Render `my_articles.html` with user's articles and filter_status|
| /articles/published                        | GET       | published_articles()          | Optional query params for filter_category, sort_by| Render `published_articles.html`|
| /calendar                                  | GET       | content_calendar()            | Optional calendar_view (month, week, day) | Render `content_calendar.html` with calendar_view and scheduled_articles|
| /article/<int:article_id>/analytics        | GET       | article_analytics(article_id) | None                                        | Render `article_analytics.html` with analytics_overview|

### Dynamic Routes
- Routes using `<int:article_id>` refer to specific articles.
- The article_id parameter is validated and passed to controller functions.

### User Sessions and Authentication
- The routes assume a user session mechanism (e.g., Flask-Login or custom session). Username is retrieved from session.
- Protected routes (creating/editing articles) require authentication.
- Route functions check user identity and authorization.
- Error or redirect occurs for unauthorized access.

---

## Section 3: Version Control Design

### Article Versioning and Approval Workflow

- Each article can have multiple versions tracked in `article_versions.txt` with version_id and version_number.
- New versions are created on edits via the `edit_article` POST route, incrementing version_number.
- The approval records for each version are stored in `approvals.txt`, linking approver decisions and comments to article versions.
- Approval statuses: approved, rejected, revision_requested.
- Workflow stages defined in `workflow_stages.txt` guide the required approval process per article category.

### Relationships
- **Versions** link to articles by article_id.
- **Approvals** link to versions and articles.
- **Comments** for a version stored in `comments.txt`, linked by article_id and version_id.

### Storage Interaction
- Models for versioning read/write `article_versions.txt` to fetch or save versions.
- Approval model manages status transitions and comments results stored in `approvals.txt`.
- Comments model enables users or approvers to add remarks per version.
- Workflow model enforces the approval steps sequence defined in `workflow_stages.txt`.

---

## Section 4: Frontend Integration Points

### Data Passing and Context Variables
- For each route rendering templates, the backend passes context variables as defined in design_spec.md, for example:
  - `dashboard`: username, quick_stats dictionary, recent_activity list.
  - `edit_article`: article_id, article_title, article_content.
  - `version_history`: versions_list, comparison_data.

- Context data structures follow the schema detailed in design_spec.md to match frontend expectations for page rendering.

### Endpoint Responses
- GET routes return rendered HTML pages with the appropriate context.
- POST routes handle form submissions, perform business logic, then redirect or re-render with error messages.
- Redirects ensure users see updated state or are returned to the listing/dashboard pages.

### Coordination Areas with Frontend
- Data structures such as lists of dicts for articles, versions, and analytics must match the frontend element requirements (e.g., ID mappings, field names).
- Pagination, filtering choices, and sort options exposed in frontend must be supported by backend parameters and data queries.
- Form input field names in frontend must correspond to backend expected POST keys.
- Error messages or validation feedback sent by backend must be rendered clearly by frontend.

---

# Summary

This architecture enforces clean separation between routing, data access, business logic, and presentation layers, enabling independent backend and frontend development. The text-file-based data model is encapsulated in durable models with safe read/write access patterns. The version and approval workflows ensure strong content control before publication. The clearly defined context variables and route responses help the frontend team accurately render the complex UI outlined in design_spec.md.

This design document is intended as a comprehensive guide for implementing the ContentPublishingHub backend aligned tightly with the frontend designs.

---
