# ContentPublishingHub Backend Architecture Documentation

---

## Section 1: Backend System Design

### Flask Application Structure

The Flask application for ContentPublishingHub will be structured modularly to ensure clear separation of concerns, maintainability, and scalability. The main application directory will contain the following packages and modules:

```
/content_publishing_hub/
    app.py                  # Flask app creation and configuration
    /routes/
        __init__.py
        dashboard.py         # Routes and controllers for dashboard views
        article.py           # CRUD operations and article-related routes
        versioning.py        # Article version history and version comparison routes
        analytics.py         # Article analytics routes
        calendar.py          # Content calendar routes
        user_articles.py     # Routes for user's own articles
        published.py         # Published articles browsing routes
    /models/
        __init__.py
        article_model.py     # Data access for articles and article_versions
        approval_model.py    # Data access for approvals
        comment_model.py     # Data access for comments
        analytics_model.py   # Data access for analytics data
        workflow_model.py    # Workflow stages data
        user_model.py        # User data access
    /services/
        __init__.py
        article_service.py   # Business logic around articles, versions, approvals
        approval_service.py  # Approval process handling
        comment_service.py   # Comment management
        analytics_service.py # Analytics data aggregation and processing
        calendar_service.py  # Calendar view data and scheduling
    /utils/
        file_manager.py      # Utilities for reading/writing data/*.txt files
        validators.py        # Input validation helpers
        version_control.py   # Versioning helpers and logic
    /templates/              # Jinja2 HTML templates
    /static/                 # Static files (CSS, JS, images)

```

### Responsibilities of Modules

- **app.py:** Initializes Flask app, sets configuration parameters, registers Blueprints from the routes package, and configures session management.

- **routes/**: Contains Flask route handlers grouped by functional areas:
  - `dashboard.py`: Handles `/dashboard` route to provide stats and recent activity.
  - `article.py`: Manages article creation (`/article/create`), editing (`/article/<article_id>/edit`), and related POST/GET logic.
  - `versioning.py`: Manages `/article/<article_id>/versions` viewing and version comparison.
  - `analytics.py`: Handles `/article/<article_id>/analytics` for article engagement metrics.
  - `calendar.py`: Provides content calendar views and scheduling.
  - `user_articles.py`: Manages `/articles/mine` to display and filter user's own articles.
  - `published.py`: Handles `/articles/published` and filtering/sorting of published content.

- **models/**: Interfaces with data file storage. Each model abstracts read/write operations on specific data files located in `data/*.txt`. Models implement methods for parsing files, querying, updating, and saving data.

- **services/**: Contains business logic and workflows decoupled from route or data handling. These services perform operations such as validation, version generation, approval workflows, comment aggregation, analytics computation, and calendar data preparation.

- **utils/**: Utility functions including:
  - File I/O helper functions to safely read and write line-delimited `*.txt` files.
  - Data validation utilities for input fields.
  - Version control helpers for managing version increments, diffs, and restorations.

### Data File Access and Management

All data is persisted in plain text files located in a `data/` directory relative to the application root. These files include `users.txt`, `articles.txt`, `article_versions.txt`, `approvals.txt`, `comments.txt`, `workflow_stages.txt`, and `analytics.txt`.

- **Data Reading:** Models parse these text files into structured Python objects (e.g., dictionaries, lists). Parsing involves splitting lines by `|` and mapping fields to dictionary keys.

- **Data Writing:** Updates (new article versions, approvals, comments) are serialized and appended or rewritten to respective files using safe file operations from `utils/file_manager.py`.

- **Concurrency Handling:** To mitigate concurrency issues (e.g., race conditions on writes), the file manager will employ file locks or atomic file write techniques.

- **Caching:** Optionally, frequently accessed data such as workflow stages might be cached in-memory with reload on file change to optimize performance.

### Data Flow Between Components

1. **HTTP Request** → Routed by Flask Blueprints to appropriate route handlers in `routes/`.
2. **Route Handler** calls business logic in `services/` to process the request.
3. **Services** invoke methods from `models/` to read/update data files.
4. Data is returned as domain objects to service, which applies business rules.
5. Processed data is passed back to the route handler.
6. Route handler injects data as context variables into Jinja2 templates for frontend rendering or returns JSON responses.

This layered approach ensures separation of routing, business logic, and data persistence concerns.

---

## Section 2: Routing and API Endpoints

| Route Pattern                  | HTTP Method(s) | Handler Function        | Description / Input Output                                                                |
|-------------------------------|----------------|------------------------|------------------------------------------------------------------------------------------|
| `/dashboard`                  | GET            | `dashboard()`           | Returns dashboard page context with `username`, `quick_stats`, and `recent_activity`.
|
| `/article/create`             | GET, POST      | `create_article()`      | GET: Display article creation form.
POST: Accept form data (title, content, etc.), validate and save draft or new article.
Returns form with success or error states.
|
| `/article/<article_id>/edit` | GET, POST      | `edit_article(article_id)` | GET: Load article data to prefill form.
POST: Save new version/update article with validation.
Returns success/errors.
|
| `/article/<article_id>/versions` | GET        | `view_article_versions(article_id)` | Returns version history for given article, optional comparison data.
|
| `/articles/mine`             | GET            | `my_articles()`         | Returns user's own articles list and filter options.
|
| `/articles/published`        | GET            | `published_articles()`  | Returns list of published articles, with category and sort filters.
|
| `/calendar`                  | GET            | `content_calendar()`    | Returns calendar view options and schedule data.
|
| `/article/<article_id>/analytics` | GET        | `article_analytics(article_id)` | Returns analytics summary data for article.

### Dynamic Route Patterns

- `<article_id>` path variables are validated as integers.
- Input forms in POST methods are validated for correctness and sanitization.

### Session and Authentication Handling

- The application assumes user authentication is managed externally or via Flask session.
- Route handlers will access `session['username']` or similar to identify the logged-in user.
- Permission checks (e.g., editing own articles) are enforced in services layer.
- Unauthorized access returns 403 or redirects to login as appropriate.

---

## Section 3: Version Control Design

### Article Versioning and Approval Workflow Architecture

- Each article can have multiple versions stored in `article_versions.txt`.
- Versioning is managed using an incremental `version_number` for each article.
- When an article is edited and saved, a new version record is appended with the following:
  - `version_id`: unique identifier
  - `article_id`: link to base article
  - `version_number`: incremented from latest
  - `content`: full article content text
  - `author`: who made the change
  - `created_date`: timestamp of version creation
  - `change_summary`: brief description

- Approvals are managed separately in `approvals.txt` and link to article versions.
- An approval record includes:
  - `approval_id`, `article_id`, `version_id`, `approver`, `status` (approved, rejected, revision_requested), `comments`, and `timestamp`.

- Approval workflow stages are defined in `workflow_stages.txt` per article category with ordered steps.
- Approval service enforces progression through required workflow stages.

- Comments related to versions and articles are stored in `comments.txt` and are displayed in UI alongside versions.

### Storage Interaction

- Reads for version history combine data from `article_versions.txt` and `approvals.txt` to show status per version.
- When saving new versions or approvals, files are appended safely.
- Comment creation appends to `comments.txt`.

- Rollback/restore functionality updates the article's current content pointer to a selected version.

---

## Section 4: Frontend Integration Points

- All routes that render HTML templates use Flask's `render_template()` passing context variables as per specification in `design_spec.md`.

- Context variables are strictly matched to frontend expectations; for example:
  - `dashboard()` passes `{username, quick_stats, recent_activity}` matching dashboard.html element expectations.
  - Forms (`create_article`, `edit_article`) provide error messages or data dictionaries compatible with input fields.
  - Version history and analytics routes provide detailed dicts/arrays formatted to allow direct rendering with frontend elements.

- Back-end endpoints return rendered pages using context variables keyed with names matching frontend bindings (e.g., `article`, `versions`, `analytics`).

- Routes that handle POST forms will redirect or re-render forms including validation error data so frontend can update UI accordingly.

- Coordination points with frontend team:
  - Data structures for articles and versions must support fields needed by frontend input elements.
  - Dropdown options (filters, categories, sorting) are sent as lists for rendering select elements.
  - Analytics data must be summarized in expected format to allow direct insertion into template IDs.
  - Calendar data structure must align with frontend calendar grid rendering logic.

- Static assets and templates are organized under `/static` and `/templates` respectively to enable Flask's standard templating and static file serving.

---

This documentation equips both backend and frontend development teams to independently implement their parts cohesively with clear interface contracts and data flow.
