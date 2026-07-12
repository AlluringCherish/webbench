# ContentPublishingHub Backend Architecture Documentation

---

## Section 1: Backend System Design

### 1. Flask Application Structure

The Flask application for ContentPublishingHub is organized into coherent modules and packages to separate concerns and facilitate maintenance and scalability.

**Suggested Directory Layout:**
```
/content_publishing_hub
|-- app.py
|-- config.py
|-- /data
|   |-- users.txt
|   |-- articles.txt
|   |-- article_versions.txt
|   |-- approvals.txt
|   |-- workflow_stages.txt
|   |-- comments.txt
|   |-- analytics.txt
|-- /modules
|   |-- __init__.py
|   |-- routes.py
|   |-- models.py
|   |-- services.py
|   |-- version_control.py
|   |-- utils.py
|-- /templates
|-- /static
```

### Module Roles and Responsibilities

- `app.py`:
  - Initializes the Flask app instance
  - Configures app settings (e.g., secret keys, upload folders)
  - Registers blueprints or routes
  - Handles app-wide middleware and error handlers

- `modules/routes.py`:
  - Defines all Flask routes as per design_spec.md
  - Each route maps to a controller function handling request parsing, validation, and response
  - Coordinates with services for business logic

- `modules/models.py`:
  - Data abstraction layer representing entities such as User, Article, ArticleVersion, Approval, Comment, Analytics.
  - Encapsulates logic for reading from and writing to the `data/*.txt` files.
  - Provides helper functions for parsing and serializing data line formats.

- `modules/services.py`:
  - Implements core business logic for features such as article creation, editing, filtering, scheduling.
  - Encapsulates workflows such as filtering user articles, scheduling content, and fetching analytic summaries.
  - Handles input validation and transformation.

- `modules/version_control.py`:
  - Manages article versioning lifecycle.
  - Retrieves version history, compares versions, manages approvals and comments.
  - Implements approval workflow enforcement based on `workflow_stages.txt`.

- `modules/utils.py`:
  - Utility functions for common tasks such as datetime parsing, ID generation, file locking for concurrent access, diff generation, and error handling.

### Data File Access and Management

- Data files are stored in the `/data` directory.
- All data access is abstracted via `models.py` with caching or indexing where appropriate.
- File reading happens with context management to ensure proper closure.
- Writes are synchronized using file locks or atomic write operations to avoid race conditions.
- Data parsed into Python dictionaries or objects for internal manipulation.

### Data Flow Between Components

1. A request hits a Flask route defined in `routes.py`.
2. The route controller parses input parameters (URL, form data, session info).
3. Controller calls appropriate `services.py` function(s) to trigger business logic.
4. Services interact with `models.py` to fetch or update data.
5. For article versioning and approval-related features, `version_control.py` is called to handle the specialized logic.
6. Results and context variables are assembled by the controller and passed to Flask's template rendering engine.
7. Response is sent back to the frontend.


## Section 2: Routing and API Endpoints

| Route Pattern                       | HTTP Method(s) | Controller Function       | Expected Input                       | Output / Response Context Variables               |
|-----------------------------------|----------------|--------------------------|------------------------------------|---------------------------------------------------|
| `/dashboard`                      | GET            | `dashboard`              | Session user info (username)       | `username` (str)                                  |
| `/article/create`                 | GET, POST      | `create_article`         | GET: none; POST: form data (title, content, etc) | GET: none; POST: errors (dict), form data for re-display |
| `/article/<int:article_id>/edit` | GET, POST      | `edit_article`           | Path: article_id; POST: form data, version changes| `article_id` (int), `article` (dict), `current_version` (dict), `errors` (POST) |
| `/article/<int:article_id>/versions` | GET         | `version_history`        | Path: article_id                    | `article_id` (int), `versions` (list of dicts), optional `selected_version`, optional `comparison_result` |
| `/articles/mine`                 | GET            | `my_articles`            | Session user info (username), optional status filter (query parameter) | `username` (str), `articles` (list of dicts), `status_filter` (str) |
| `/articles/published`            | GET            | `published_articles`     | Optional filters (category, sort) query params  | `articles` (list of dicts), `category_filter` (str), `sort_option` (str) |
| `/calendar`                     | GET, POST      | `content_calendar`       | GET: none or view filter; POST: scheduling data | `scheduled_articles` (list of dicts), `calendar_view` (str), schedule data (POST) |
| `/article/<int:article_id>/analytics` | GET        | `article_analytics`      | Path: article_id                    | `article_id` (int), `analytics` (dict)           |

### Routing Details:

- Dynamic route parts use Flask converters (`<int:article_id>`) to validate input.
- POST routes accept form data, validate, and then update data files.
- Query parameters support filtering (e.g., status filter for `/articles/mine`).
- All GET routes render corresponding HTML templates with proper context.

### User Session & Authentication

- User session management handled via Flask-Login or equivalent.
- All routes accessing user-specific data validate session presence.
- Username fetched from session or login context and passed as needed.
- Access control: Authors can only edit their own articles; approval users verified before approval actions.


## Section 3: Version Control Design

### Article Versioning

- Each article can have multiple versions stored in `article_versions.txt`.
- Each version has a unique `version_id`, associated `article_id`, incrementing `version_number`, `content`, `author`, and timestamp.
- New versions created on article edits.
- The `version_control.py` module provides functions to:
  - Retrieve all versions by article_id
  - Fetch the latest current version
  - Save new version entries
  - Generate diffs between versions for comparison

### Approval Workflow

- Approvals are tracked in `approvals.txt`.
- Approval records link an approval to a particular article version, stating approver username, status, comments, and timestamp.
- Approval workflow stages are determined from `workflow_stages.txt` based on article category.
- Business logic checks stage order and mandatory approvals before allowing transition of article status.
- Status like `pending_review`, `under_review`, `approved`, `rejected` are managed here.

### Comments

- Comments on article versions are stored in `comments.txt`.
- Comments include the user, timestamp, version context, and comment text.
- These are fetched and displayed in relevant views (e.g., version history, edit pages) for collaboration.

### Data Storage Interaction

- Data models parse and serialize records line-by-line adhering to pipe-delimited format.
- On version save, append new record to `article_versions.txt`.
- Approval actions append records to `approvals.txt` with timestamps.
- Comments similarly appended to `comments.txt`.
- Concurrency control ensured on write with locks or transaction-like mechanisms.


## Section 4: Frontend Integration Points

### Data Passing to Templates

- Backend controllers pass explicit context variables as described in design_spec.md.
- Data passed as Python primitives:
  - Strings (`username`, `status_filter`)
  - Lists of dictionaries (`articles`, `versions`, `scheduled_articles`)
  - Dictionaries (`article`, `current_version`, `analytics`, `comparison_result`)
- Templates expect specific IDs on page containers and UI elements, enabling frontend JavaScript hooks.

### Endpoint Responses

- Mostly HTML content via `render_template` with context.
- POST routes redirect on success or re-render with errors on failure.
- For version comparison, diff data or comparison results are passed to template context.

### Coordination Points with Frontend

- Data structures handed off must match templates expected keys, e.g., article dict fields matching `articles.txt` schema.
- Validation errors from POST routes must be mapable to form fields for error display.
- Dynamic content like version lists, analytics summaries, scheduled events require consistent format and ordering to render UI correctly.
- IDs defined for elements in design_spec.md must match for frontend event handling.

---

This document provides comprehensive guidance for backend developers to implement the Flask backend and for frontend teams to correctly interface with the backend routes and data structures, enabling seamless independent development and integration efforts.
