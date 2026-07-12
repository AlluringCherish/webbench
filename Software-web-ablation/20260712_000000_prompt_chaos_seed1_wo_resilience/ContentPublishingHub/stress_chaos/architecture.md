# ContentPublishingHub Backend Architecture

---

## Section 1: Backend System Design

### Flask Application Structure

The Flask application is structured into modular packages and components to maintain clean separation of concerns and scalability:

- **app/**
  - `__init__.py`: Initializes Flask app, configures extensions, registers blueprints.
  - **routes/**: Contains modules defining route handlers (controllers) grouped by functionality.
    - `dashboard.py`
    - `articles.py` (handles article create, edit, versions, my_articles, published_articles)
    - `calendar.py`
    - `analytics.py`
  - **services/**: Business logic layer encapsulating core operations like article versioning, approval workflows, analytics computation.
  - **data_access/**: Modules responsible for reading/writing data files located in `data/*.txt`. Handles parsing and serializing of pipe-delimited text files.
  - **auth/** (optional): Handles user session and authentication if implemented later.
  - **utils/**: Utility functions such as date parsing, text processing, filtering helpers.

### Module Responsibilities

- **Routing Modules (`routes/`)**: Define Flask route decorators and controller functions. Fetch input from request, call service layer methods, and prepare data for templates.

- **Service Modules (`services/`)**: Implement business logic, such as article creation/editing, version control, approval processes, and analytics aggregation. Interact with data_access modules for persistent data.

- **Data Access Modules (`data_access/`)**: Handle all file operations with the following core files:
  - `users.txt`
  - `articles.txt`
  - `article_versions.txt`
  - `approvals.txt`
  - `workflow_stages.txt`
  - `comments.txt`
  - `analytics.txt`

  They provide functions like `get_articles()`, `save_article()`, `get_article_versions(article_id)`, etc., abstracting the pipe-delimited text parsing and serialization.

- **Version Control and Workflow (within `services/versioning.py`)**: Encapsulates logic to manage version histories, approval status, and comment threads per article version.

### Data File Access and Management

- Each data access module uses efficient read and write patterns to handle updates and queries.
- Files are loaded on demand; caching strategies can be introduced if necessary.
- Updates to data files involve overwriting or appending to maintain atomic changes and consistency.
- Cross-file consistency (e.g., ensuring article version IDs match those in approvals and comments) is maintained by synchronized service layer logic.

### Data Flow

1. **Client Request** received on a route triggers controller function.
2. **Controller Calls Services** to perform logic (create, read, update data).
3. **Services Interact with Data Access Layer** to read or persist data.
4. **Resulting Data** prepared as context variables.
5. **Controller Passes Context** to frontend templates for rendering.

---

## Section 2: Routing and API Endpoints

| Route                             | Methods   | Controller Function          | Input                        | Output (Template and Context)                                                                                                  |
|----------------------------------|-----------|------------------------------|------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| `/dashboard`                     | GET       | `dashboard()`                | session username             | `dashboard.html`: username (str), quick_stats (dict), recent_activity (list of dict)                                           |
| `/article/create`                | GET, POST | `create_article()`           | POST form: title, content    | GET renders blank form (`create_article.html`). POST saves article draft and redirects or re-renders form with messages.      |
| `/article/<article_id>/edit`    | GET, POST | `edit_article(article_id)`   | GET uses URL param; POST form: title, content | `edit_article.html`: article_id, title, content (latest content)                                                               |
| `/article/<article_id>/versions`| GET       | `article_version_history(article_id)` | URL param               | `version_history.html`: article_id, versions (list of dict), version_comparison (dict)                                         |
| `/articles/mine`                | GET       | `my_articles()`              | session username, optional status filter | `my_articles.html`: articles (list), status_filter_options, selected_status_filter                                              |
| `/articles/published`           | GET       | `published_articles()`       | optional category, sort filters | `published_articles.html`: articles (published), category_filter_options, selected_category, sort_options, selected_sort       |
| `/calendar`                    | GET       | `content_calendar()`         | optional selected_view       | `content_calendar.html`: calendar_views, selected_view, schedule_items                                                        |
| `/article/<article_id>/analytics`| GET     | `article_analytics(article_id)` | URL param                  | `article_analytics.html`: article_id, analytics_overview (dict with metrics)                                                  |

### Dynamic Routes

- Routes with `<article_id>` parameters accept integer article_id values.
- Controller functions validate that `article_id` exists and return 404 or error handling if not.

### User Sessions and Authentication

- Assumes session management setup with Flask sessions/cookies to track logged-in user.
- User information (`username`) is extracted from session for personalization and data filtering.
- Authentication is not explicitly defined in design but can be integrated with login-required decorators on endpoints.

---

## Section 3: Version Control Design

### Article Versioning Architecture

- Each article has multiple versions tracked in `article_versions.txt`, uniquely identified by `version_id` and associated with `article_id`.
- Versions store content, author, timestamp, and a brief change summary.
- Version numbers are sequential per article, maintained during each save operation.

### Approval Workflow

- Approvals are managed via `approvals.txt`, linking each approval record to a specific article version.
- Approvals include status (approved, rejected, revision_requested), approver username, comments, and timestamp.
- Workflow stages from `workflow_stages.txt` determine the progression order for reviews and approvals by category.

### Comments Relation

- Comments tracked in `comments.txt` associate user feedback with specific article versions.
- Comments include commenter username, text, timestamp.

### Storage Interaction

- Version creation or update writes new lines to `article_versions.txt`.
- Approval actions append to `approvals.txt` with current review status.
- Comment submissions append to `comments.txt`.
- Service layer guarantees integrity across these files when processing version updates and approvals.

---

## Section 4: Frontend Integration Points

### Data Passing to Frontend Templates

- Controllers render templates using Flask's `render_template()` passing context variables per design specification.
- Context variables match expected types and structures strictly (dicts, lists of dicts, strings).
- Dynamic elements such as article lists, version histories, and analytics data structured to immediately populate UI components.

### Endpoint Response Patterns

- GET routes return rendered html templates with prefilled context data.
- POST routes typically redirect after processing to adhere to PRG (Post-Redirect-Get) pattern, except for form re-renders with validation errors.

### Coordination Areas

- Strict adherence to the keys and data structures in context variables ensures frontend elements can correctly bind and display data.
- IDs and element references (e.g., `#articles-table`, `#filter-article-status`) are linked to backend supplied data.
- Special frontend actions such as version comparisons or filtering depend on backend supplying comprehensive and well-structured context.

---

This architecture document serves as a guiding blueprint for independent backend and frontend development teams to implement the ContentPublishingHub system with clear interfaces, consistent data handling, and modular design.