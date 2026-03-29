# ContentPublishingHub Backend Architecture Design Document

---

## Section 1: Backend System Design

### 1. Flask Application Structure

The Flask application is structured into modular packages and submodules to separate concerns, enable scalability, and facilitate testing and maintenance. The proposed structure is:

```
/content_publishing_hub
|-- app.py                # Flask app factory and initialization
|-- config.py             # Configurations (env, file paths, secret keys, etc.)
|-- /routes               # Routing and controller functions
|   |-- __init__.py
|   |-- dashboard.py
|   |-- article.py
|   |-- analytics.py
|   |-- calendar.py
|-- /services             # Business logic and data manipulation
|   |-- __init__.py
|   |-- article_service.py
|   |-- user_service.py
|   |-- version_control_service.py
|   |-- analytics_service.py
|-- /data_access          # Data access layer - file I/O abstraction
|   |-- __init__.py
|   |-- articles_dao.py
|   |-- users_dao.py
|   |-- versions_dao.py
|   |-- approvals_dao.py
|   |-- comments_dao.py
|   |-- analytics_dao.py
|-- /utils                # Utility functions
|   |-- __init__.py
|   |-- file_io.py        # Read/write helper functions using pipe-delimited format
|   |-- validators.py
|-- /templates            # Jinja2 templates for frontend
|-- /static               # Static assets
|-- requirements.txt
|-- README.md
```

### 2. Module Responsibilities

- **app.py**: Application factory to create the Flask app instance, register Blueprints (routes), and initialize middleware if needed (e.g., session handling, authentication, error handlers).

- **routes/**: Contains Blueprints for grouping related routes and controller functions by feature (e.g., dashboard, article management, analytics).
  - Handles HTTP requests and responses, input validation at the endpoint level,
  - Parses URL parameters and form data,
  - Calls appropriate services,
  - Passes context data to template rendering.

- **services/**: Implements core business logic and workflows.
  - Article management including create/edit, versioning coordination, approval workflow logic.
  - User-related operations.
  - Analytics aggregation and computation.

- **data_access/**: Abstracts file reading and writing operations.
  - Provides functions to fetch, parse, update, and save data in the pipe-delimited text file formats.
  - Ensures thread-safe read/write to data files to prevent data corruption.

- **utils/**:
  - Common helper functions for file I/O, pipe-delimited parsing and serialization,
  - Input validation.

### 3. Data File Access and Management

All persistent data is stored in pipe-delimited text files under a data directory (`data/*.txt`). Data access layer functions:

- Load data into application objects or dictionaries on demand (lazy loading for performance).
- Support CRUD operations conceptually — reading full datasets to modify and write back, or appending for new records.
- Each DAO module corresponds to one or more data files, parsing them into relevant data structures.
- Version controlled files like `article_versions.txt`, `approvals.txt`, and `comments.txt` are accessed in a way to preserve integrity.
- Timestamp and ID generation managed via services or utility modules to avoid collisions.

### 4. Data Flow Between Components

1. User sends HTTP request to Flask endpoint in routes module.
2. Route function extracts input (URL params, form fields), validates data.
3. Route invokes service function passing inputs.
4. Service uses DAOs to read or update data files as needed.
5. Service returns processed data or status to route.
6. Route renders appropriate Jinja2 template, passing context data.
7. Client receives rendered HTML page.

This layered approach enforces separation of concerns and easy unit testing.

---

## Section 2: Routing and API Endpoints

| Route URL                                | HTTP Methods | Function Handler    | Input                               | Output                                   | Notes/Details                                      |
|------------------------------------------|--------------|--------------------|-----------------------------------|------------------------------------------|----------------------------------------------------|
| `/dashboard`                             | GET          | `dashboard`         | Session user info (username)      | Render `dashboard.html` with: `username`, `quick_stats`, `recent_activity` |
| `/article/create`                        | GET, POST    | `create_article`    | GET: none (empty form)             | GET: blank form rendered                       |
|                                          |              |                    | POST: form data (title, content) | POST: validation errors or success messages     |
| `/article/<int:article_id>/edit`         | GET, POST    | `edit_article`       | GET: article_id URL param          | `edit_article.html` with `article` dict            |
|                                          |              |                    | POST: update form data             | validation errors or success messages             |
| `/article/<int:article_id>/versions`     | GET          | `version_history`    | article_id URL param               | `version_history.html` with list of versions and current version id |
| `/articles/mine`                         | GET          | `my_articles`       | Session user info, optional filter parameter (status) | `my_articles.html` with filtered articles list and filter status |
| `/articles/published`                    | GET          | `published_articles` | Optional category and sort filter query params  | `published_articles.html` with filtered and sorted articles |
| `/calendar`                             | GET          | `content_calendar`  | Optional calendar view selection  | `content_calendar.html` with calendar view and scheduled articles |
| `/article/<int:article_id>/analytics`   | GET          | `article_analytics`  | article_id URL param               | `article_analytics.html` with `analytics_data` dict |

### Dynamic Routes Pattern
- Use `<int:article_id>` for articles.
- Article version specific routes embed `<article_id>` but could be extended for `<version_id>` if needed.

### Session and Authentication
- Current user session stored via Flask session or equivalent, including `username`.
- User authentication middleware integrated but not detailed here.
- Endpoints assume session-based access; future token-based API extensions possible.

---

## Section 3: Version Control Design

### Versioning Workflow Architecture

- Each article can have multiple versions tracked in `article_versions.txt`.
- Version entry includes version number, content, author, timestamp, and change summary.
- Version numbers auto-increment per article.

### Approval Workflow

- Approvals tied to particular article versions stored in `approvals.txt`.
- Each approval includes approver username, status (`approved`, `rejected`, `revision_requested`), comment, and timestamp.
- Workflow stages from `workflow_stages.txt` provide sequence and requirement flags per article category.
- Business logic enforces that an article version must pass all required stages before final publication.

### Comments on Versions

- Comments linked to article version via `comments.txt`.
- Multiple users can leave comments, facilitating review discussions.

### Storage Interaction

- Services read/write the version-related files via DAOs ensuring atomic updates.
- New version creation triggers appending to `article_versions.txt`.
- Approval status updates and comments are appended to their respective files.
- Version history queries aggregate versions, approvals, and comments to display coherent version metadata.

---

## Section 4: Frontend Integration Points

### Data Passing to Templates

- Context variables listed in design_spec.md for each route are populated by backend via `render_template` calls.
- Backend ensures correct data types and structures:
  - Primitive types (strings, ints) are passed directly.
  - Lists and dicts are passed as JSON-friendly structures for ease of client rendering.

### Endpoint Responses

- All routes render full HTML templates as described, not JSON APIs, supporting server-side rendering.
- For POST requests (e.g., create/edit article), response includes validation feedback within the same template.

### Coordination Points with Frontend

- Element IDs in templates (e.g., `create-article-button`, `versions-list`) are expected by frontend JS and styling.
- Data structures such as list of articles, versions, analytics data must align with frontend expectations (e.g., keys, nested fields).
- Pagination or filtering parameters passed as query parameters need consistent handling.

---

This design document provides a comprehensive blueprint for backend and frontend teams to implement the ContentPublishingHub application effectively and independently.

---

_End of document_