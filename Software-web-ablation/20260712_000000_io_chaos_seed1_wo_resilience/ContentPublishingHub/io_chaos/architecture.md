# ContentPublishingHub - Backend Architecture Design Document

---

## Section 1: Backend System Design

### 1. Flask Application Structure

The ContentPublishingHub backend will follow a modular Flask application architecture structured into packages and modules:

- **app/** (main package)
  - **__init__.py**: Creates and configures the Flask app instance. Initializes data layers, registers blueprints, and sets up common extensions (e.g., session management).
  - **routes/** (package): Contains route modules, each responsible for logically grouped routes.
    - dashboard.py: Handles `/dashboard` route logic.
    - article.py: Manages `/article/*` routes including create, edit, versions, analytics.
    - articles.py: Manages `/articles/mine` and `/articles/published` routes.
    - calendar.py: Handles `/calendar` route.
  - **models/** (package): Responsible for data access and domain logic related to core entities.
    - article_model.py: Methods to read/write articles, versions, comments, approvals from/to data files.
    - user_model.py: Methods for user data access.
    - analytics_model.py: Handles analytics data retrieval.
    - workflow_model.py: Manages workflow stages and approval processes.
  - **services/** (package): Contains business logic and validation rules.
    - article_service.py: Implements article lifecycle, versioning, approval workflows, applying business rules.
    - user_service.py: User authentication, session handling (if relevant).
    - analytics_service.py: Processes raw analytics into report data.
  - **utils/** (package): Utility modules for common functions (file I/O abstraction, date parsing, logging, etc.)
  - **static/**: Static assets (CSS, JS, images).
  - **templates/**: Jinja2 template files structured per frontend design.

### 2. Responsibilities of Each Module

- **Routing Modules:** Receive HTTP requests, validate inputs, call services, prepare data for rendering templates or return JSON responses.
- **Models:** Abstract data storage mechanics; responsible for reading and writing to text files located in `data/*.txt`. Implement caching or locking as needed for concurrency.
- **Services:** Contain core business logic, for example, enforcing version approval workflows, validating article state transitions, or formatting analytics.
- **Utils:** Helper functions used across layers, including centralized file management to ensure consistent and safe file access.

### 3. Data Files Access and Management

- All persistent data is stored in text files under the `data/` directory.
- File access is encapsulated through model classes/functions to abstract parsing (e.g., split by `|`), loading into memory-friendly structures (dicts, lists), and writing back safely.
- Write operations always ensure data consistency and avoid corrupting files (e.g., using atomic writes).
- Reads cache filepath constants to avoid path hardcoding.

### 4. Data Flow Between Components

- Incoming HTTP requests are routed to appropriate controller functions in `routes/`.
- Routes validate and parse inputs, then call service layer functions to process requests.
- Services interact with models to fetch or update data in files.
- Results (data or status) are returned to routes.
- Routes then prepare context variables and invoke template rendering or JSON responses.

---

## Section 2: Routing and API Endpoints

### 1. Flask Routes Overview

| Route                           | HTTP Methods | Controller Function        | Description                          |
|--------------------------------|--------------|----------------------------|------------------------------------|
| /dashboard                     | GET          | dashboard                 | Render dashboard with user stats   |
| /article/create                | GET, POST    | create_article            | Show create form, handle submissions|
| /article/<article_id>/edit     | GET, POST    | edit_article              | Edit article form and updates      |
| /article/<article_id>/versions | GET          | article_version_history   | Display version history for article|
| /articles/mine                 | GET          | my_articles               | List user's articles with filters  |
| /articles/published            | GET          | published_articles        | List published articles with categories|
| /calendar                     | GET          | content_calendar          | Show publishing calendar           |
| /article/<article_id>/analytics| GET          | article_analytics         | Show analytics data for an article |

### 2. Controller Function Inputs and Outputs

- **dashboard (GET)**
  - Input: session to obtain logged-in username
  - Output: Renders `dashboard.html` with username, quick_stats dict, recent_activities list

- **create_article (GET, POST)**
  - GET: Renders `create_article.html` with empty form
  - POST: Processes form data, validates, creates new article entry, redirects or shows errors

- **edit_article (GET, POST)**
  - GET: Loads article data by article_id, passes to `edit_article.html`
  - POST: Validates and saves new version or updates, then redirects or shows validation errors

- **article_version_history (GET)**
  - Input: article_id from route
  - Output: List of versions retrieved and passed to `version_history.html`

- **my_articles (GET)**
  - Input: Optional filters from query params
  - Output: Filtered list of articles by current user in `my_articles.html`

- **published_articles (GET)**
  - Input: Optional category filter and sort options
  - Output: Articles and categories for rendering `published_articles.html`

- **content_calendar (GET)**
  - Output: Scheduled publications data for `content_calendar.html`

- **article_analytics (GET)**
  - Input: article_id
  - Output: Analytics summary data for the article in `article_analytics.html`

### 3. Dynamic Route Patterns

- Article-specific routes use `<article_id>` as an integer path parameter.
- Route functions must validate existence and permissions for article_id.

### 4. Session and Authentication Handling

- User session management is assumed for login and authorization.
- Backend checks user identity via session to filter articles (`my_articles`) and authorize edits.
- Authentication integration points are provided in user_service but actual mechanism (OAuth, JWT, etc.) is out of scope.

---

## Section 3: Version Control Design

### 1. Article Versioning and Approval Workflow Architecture

- Versions of articles are tracked in `article_versions.txt`, each version identified uniquely and linked to an article_id.
- Every article edit creates a version with incremented version_number, author, content, timestamp, and change summary.
- Approval workflow managed via `approvals.txt` tracking approval ids, linked to article version, approver, status, comments, and timestamp.
- Workflow stages for different categories are described in `workflow_stages.txt` and used by the service layer to enforce approval steps.

### 2. Relationships

- Articles have many versions.
- Each version may have multiple approvals representing review status.
- Comments stored in `comments.txt` can be associated with specific article versions for feedback.

### 3. Storage Interaction

- Reading article_versions.txt returns all versions for an article.
- Reading approvals.txt returns approval history per article version.
- Comments are read per version for display in UI.
- On saving a new version or approval status, corresponding files are updated atomically.

### 4. Workflow Enforcement

- The service layer consults workflow_stages.txt to ensure correct progression before publishing.
- Updates to approval status and version content trigger state changes in articles.txt status field.

---

## Section 4: Frontend Integration Points

### 1. Passing Context Variables

- Each route provides context variables as specified in the design_spec to templates via `render_template`.
- Data structures (dicts, lists) correspond directly to frontend element needs (e.g., quick_stats dict, articles list).

### 2. Endpoint Responses

- All GET routes return full HTML pages rendered with Jinja2 templates, including user data required for interface.
- POST routes that mutate data redirect on success; in case of errors, re-render forms with validation messages.

### 3. Coordination Areas

- Particular attention on data shapes expected by frontend, such as:
  - Article dictionaries including all fields from articles.txt plus computed properties.
  - Version lists maintaining order and version metadata.
  - Approval comments and statuses displayed alongside versions.
  - Analytics data structured to facilitate display in charts and statistics sections.
- Route handlers must ensure that data passed matches frontend expectations (e.g., keys, IDs, formatting).

### 4. Integration Points With Frontend Components

- Templates rely on specific IDs for page elements as specified (e.g., `dashboard-page`, `article-title`). Backend must supply context fully to prevent frontend errors.
- Any dynamic JSON data for frontend scripting can be exposed through additional API endpoints or embedded scripts rendered by Flask.

---

This architectural design document provides a comprehensive backend blueprint enabling clear separation of concerns and independent frontend implementation based on published templates and backend APIs.
