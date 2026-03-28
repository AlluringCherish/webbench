# ContentPublishingHub Backend Architecture Design

---

## Section 1: Backend System Design

### Flask Application Structure

```plaintext
content_publishing_hub/
│
├── app.py                    # Flask application factory and entry point
├── config.py                 # Configuration settings (e.g., file paths, secrets)
├── requirements.txt          # Python dependencies
├── data/                     # Data files storage folder
│   ├── users.txt
│   ├── articles.txt
│   ├── article_versions.txt
│   ├── approvals.txt
│   ├── workflow_stages.txt
│   ├── comments.txt
│   ├── analytics.txt
│   └── ...
├── modules/                  # Core backend modules
│   ├── __init__.py
│   ├── routes.py             # All route definitions and view functions
│   ├── models.py             # Data models and data access layer
│   ├── services.py           # Business logic and orchestration
│   ├── version_control.py    # Article versioning and approval workflow logic
│   ├── utils.py              # Helper utilities (e.g., file ops, validation)
│   ├── auth.py               # User session management & authentication (stub/placeholder)
│   └── data_access.py        # File read/write operations encapsulated
└── templates/                # Frontend template files (not implemented here)

```

### Module Responsibilities

- **app.py:** Initializes Flask app, registers blueprints or routes from `modules.routes`, sets up configuration.
- **modules/routes.py:** Defines all Flask routes mapping to controller functions handling requests, validation, and responses.
- **modules/models.py:** Defines Python classes or dict schemas that represent entities like User, Article, Version, Approval, Comment, Analytics for structured data access.
- **modules/services.py:** Contains business logic — e.g., fetching articles, applying filters, computing quick stats, preparing data for templates.
- **modules/version_control.py:** Handles version creation, retrieval, approval workflow management, comparisons, restore operations.
- **modules/utils.py:** Utility functions for common operations such as parsing date strings, validation, data formatting.
- **modules/auth.py:** Manages user sessions; authentication to be stubbed or expanded depending on future requirement.
- **modules/data_access.py:** Encapsulates file I/O operations (read/write of all .txt data files) with locking or synchronization protections if concurrency is expected.

### Data File Access and Management

- All data persists in plain text files under `data/` folder with pipe-delimited formats.
- `data_access.py` module provides read and write abstractions for each data file.
- On read, the content is parsed into appropriate Python data structures (list of dicts, etc.)
- On write, updated data replaces the file contents ensuring atomic file updates (e.g., temp write-rename pattern).
- For operations that change state (e.g., creating version, approving article), relevant files are updated accordingly.
- Concurrency handling may be implemented via file locks or by queuing writes if needed in later scaling.

### Data Flow Between Components

1. **Request Handling:** Client interacts via HTTP routes defined in `routes.py`.
2. **Controller Logic:** Route functions validate inputs, invoke business logic in `services.py`/`version_control.py`.
3. **Data Access:** Services layer uses `models.py` classes and `data_access.py` to query or update files.
4. **Business Rules:** Services enforce workflow rules, article status transitions, versioning using `version_control.py`.
5. **Template Context:** Prepared data is passed as context dict to rendering templates.
6. **Response:** Rendered HTML (via templates) or JSON responses returned to client.

---

## Section 2: Routing and API Endpoints

| Route Pattern                      | Methods  | Controller Function         | Input Parameters                      | Output Context / Response                                  |
|----------------------------------|----------|-----------------------------|-------------------------------------|------------------------------------------------------------|
| `/dashboard`                     | GET      | `dashboard()`               | session user info                    | `username`, `quick_stats`, `recent_activity` dicts          |
| `/article/create`                | GET, POST| `create_article()`          | POST: form data (title, content, category, etc.)            | GET: render template; POST: validation result, status msg   |
| `/article/<int:article_id>/edit`| GET, POST| `edit_article(article_id)`  | article_id as int; POST: form data                          | article dict, validation errors, status messages            |
| `/article/<int:article_id>/versions`| GET  | `article_version_history(article_id)` | article_id as int                        | versions list, optional comparison dict, article_id         |
| `/articles/mine`                | GET      | `my_articles()`             | session user info, optional query filters                  | articles list, filter status, user info                      |
| `/articles/published`           | GET      | `published_articles()`      | query params for filters (category, sort)                  | filtered/sorted articles list, filter_category, sort_by     |
| `/calendar`                    | GET, POST | `content_calendar()`        | POST: form data for scheduling or calendar view            | calendar_view, calendar_data, status messages                |
| `/article/<int:article_id>/analytics`| GET  | `article_analytics(article_id)` | article_id as int                   | analytics dict, article_id                                    |

### Dynamic Route Patterns

- `/article/<int:article_id>/edit`
- `/article/<int:article_id>/versions`
- `/article/<int:article_id>/analytics`

Each `article_id` parameter will be validated and used to load the corresponding article data.

### User Sessions and Authentication

- Sessions will store logged-in user identity (e.g., username).
- Authentication is planned as a stub module in `auth.py`, currently no enforced security.
- Routes will access current user from session for ownership (e.g., `/articles/mine`) or authorization.
- Login/logout endpoints are out of scope but should be integrated in future.

---

## Section 3: Version Control Design

### Article Versioning and Approval Workflow Architecture

- **Versioning:**
  - Every article edit that is saved as a new version results in an entry in `article_versions.txt`.
  - Each version has a unique `version_id` and incrementing `version_number` scoped per article.
  - Versions store `content`, `author`, `created_date`, and `change_summary`.

- **Approval Workflow:**
  - Each version can have zero or more approval records in `approvals.txt`.
  - Approvals have `approver`, `status` (approved, rejected, revision_requested), `comments`, and `timestamp`.
  - Stages for categories come from `workflow_stages.txt` to control order and requirements.
  - The system checks required approval stages before an article version can be promoted to approved or published status.

- **Comments and Collaboration:**
  - Comments are linked by `article_id` and `version_id` in `comments.txt`.
  - Comments store user remarks and timestamps.
  - Used in review phase for collaboration.

### Storage Interaction

- Reading versions queries `article_versions.txt` filtered by `article_id`.
- Approval status and history read from `approvals.txt` for a given `article_id` and `version_id`.
- Comments related to the version retrieved from `comments.txt`.
- Updates happen by appending or rewriting respective text files ensuring data integrity.

### Workflow Enforcement

- The backend enforces the required approval stages and transitions.
- On version save or approval action, status transitions checked and effected in `articles.txt` for the main article entry.

---

## Section 4: Frontend Integration Points

### Data Passing to Templates

- Each route returns data context required for its specific template as described in `design_spec.md`:
  - E.g., `dashboard()` returns `username`, `quick_stats`, `recent_activity`.
  - Context variables are explicitly prepared in the controller functions.

- Data structures (lists of dicts, dicts) align with frontend expectations (e.g., list of articles as dicts containing fields like `title`, `status`, etc.).

- Validation status messages and error messages returned to form handling templates (`create_article`, `edit_article`, `content_calendar`) on POST requests.

### Endpoint Response Characteristics

- GET requests typically render HTML pages using Flask's `render_template()` passing context.
- POST requests process forms and then render the same template with feedback or redirect as appropriate.
- No API JSON endpoints are specified; can be expanded in future as needed.

### Coordination Points with Frontend Team

- Confirm exact data structure fields and types for context variables to ensure template variables bindings work correctly.
- Agree on status message formats for validation feedback.
- Coordinate IDs usage in form inputs and buttons as specified in the templates section for event handling.
- Ensure URLs used in navigation elements and forms correspond exactly to backend routes.

---

This document provides a comprehensive blueprint for implementing the ContentPublishingHub backend using Flask, ensuring clear separation of concerns, maintainability, and smooth frontend integration.