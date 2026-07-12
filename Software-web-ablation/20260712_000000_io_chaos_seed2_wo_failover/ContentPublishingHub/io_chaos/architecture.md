# ContentPublishingHub Backend Architectural Design Document

---

## Section 1: Backend System Design

### 1. Flask Application Structure

The Flask backend application will be organized into a modular package-based structure as follows:

```
/content_publishing_hub/
|-- app.py                    # Main Flask app instance and entry point
|-- controllers/              # Flask route handlers and request controllers
|   |-- dashboard.py
|   |-- article.py
|   |-- versions.py
|   |-- analytics.py
|   |-- calendar.py
|-- services/                 # Business logic layer, versioning, approval workflow
|   |-- article_service.py
|   |-- version_service.py
|   |-- approval_service.py
|   |-- analytics_service.py
|   |-- user_service.py
|-- data_access/              # Data access and management of .txt data files
|   |-- article_dao.py
|   |-- user_dao.py
|   |-- version_dao.py
|   |-- approval_dao.py
|   |-- comment_dao.py
|   |-- analytics_dao.py
|-- utils/                    # Utility modules (e.g., parsing, validation)
|   |-- file_utils.py
|   |-- auth_utils.py
|-- templates/                # Frontend templates (Jinja2 HTML files)
|-- static/                   # Static assets (css/js/img)
|-- config.py                 # Configuration and constants
|-- requirements.txt
|-- README.md
```

### 2. Module Responsibilities

- **app.py:** Creates and configures the Flask app. Initializes extensions if needed.
- **controllers/**: Defines Flask route handlers. Handles HTTP input parsing, session management, invokes business logic, and prepares data/context for rendering templates.
- **services/**: Implements core business logic separated from HTTP concerns. Handles article management, versioning workflows, approval process, analytics aggregation.
- **data_access/**: Encapsulates reading/writing logic for all data files in `data/*.txt`. Provides CRUD operations abstracted from file formats.
- **utils/**: Helper functions for file parsing, validation, and optionally session/authentication utilities.
- **templates/**: Holds Jinja2 templates matching frontend page designs.

### 3. Data File Management

- All persistent data is stored in pipe-delimited text files under a dedicated `data/` directory.
- Each DAO (Data Access Object) module is responsible for safely reading and writing to its corresponding file, implementing:
  - Parsing lines into Python data structures
  - Writing updates atomically (e.g., write temp then rename)
  - Searching and filtering records by keys such as `article_id` or `version_id`
- File paths are configurable via `config.py`.
- Concurrency considerations can be handled by file locks or point-in-time snapshots if needed.

### 4. Data Flow

- HTTP requests arrive at the Flask routes (controllers).
- Controllers validate and parse input, then delegate to services.
- Services coordinate operations, aggregating data from DAOs.
- Services return business data or operation results to controllers.
- Controllers prepare context variables and render templates, or return JSON as needed.

---

## Section 2: Routing and API Endpoints

The application exposes the following Flask routes described with HTTP method, controller function, and input/output details:

| Route                              | HTTP Method(s) | Controller Function    | Inputs                         | Outputs / Rendered Template        |
|-----------------------------------|----------------|-----------------------|--------------------------------|-----------------------------------|
| /dashboard                        | GET            | dashboard             | Session: username              | Render `dashboard.html` with username context
| /article/create                   | GET, POST      | create_article        | (GET) None                    | (GET) Render `create_article.html`
|                                   |                |                       | (POST) form data (title, content, etc.) | Process, save draft/new article, reload or redirect
| /article/<article_id>/edit        | GET, POST      | edit_article          | URL param: article_id; (POST) form data | Fetch article data (GET), update version (POST), render `edit_article.html`
| /article/<article_id>/versions    | GET            | version_history       | URL param: article_id          | Fetch version list; Render `version_history.html`
| /articles/mine                   | GET            | my_articles           | Session user info               | List user's articles; Render `my_articles.html`
| /articles/published              | GET            | published_articles    | None                          | List published articles; Render `published_articles.html`
| /calendar                       | GET            | content_calendar      | None                          | Fetch scheduled publication data; Render `content_calendar.html`
| /article/<article_id>/analytics   | GET            | article_analytics     | URL param: article_id          | Fetch analytics data; Render `article_analytics.html`

### Dynamic Route Patterns
- `<article_id>` is always a string or int representing IDs parsed from URLs.
- Controller functions validate existence and permissions before processing.

### User Sessions and Authentication
- Basic session handling assumed to track logged-in username.
- Authentication and authorization checks (e.g., author vs viewer) handled at controller/service layer.
- Secure endpoints require session user; redirects or errors if unauthorized.

---

## Section 3: Version Control Design

### Architecture for Article Versioning and Approval Workflow

- Article versions are stored in `article_versions.txt` with unique `version_id` and linked to `article_id`.
- Each version has metadata: version number, content, author, timestamp, and change summary.
- Multiple versions can exist per article; newest version corresponds with draft or published content.

### Version History and Comments
- Version history endpoint fetches all versions for an article from `article_versions.txt`.
- Restore operations revert an article to content from a selected version.
- Comments on individual versions stored in `comments.txt`, linked by `article_id` and `version_id`.
- Comments provide collaborative feedback during review.

### Approval Workflow
- Approvals recorded in `approvals.txt` referencing `article_id` and `version_id`.
- Status values: approved, rejected, revision_requested.
- Each approval includes approver username, comments, and timestamp.
- Workflow stages in `workflow_stages.txt` define per-category review steps (e.g., Editor Review, Publisher Approval).
- Services enforce workflows by checking stage requirements and approval statuses.

### Storage Interaction
- DAOs read/write to respective txt files to query and persist version and approval data.
- Updates on versions or approvals trigger updates in articles status (e.g., draft -> approved).

---

## Section 4: Frontend Integration Points

### Data Provision to Templates
- Controller functions pass carefully structured context variables matching the design_spec mandates.
- For example, article dicts include expected fields (title, content, author, status, etc.).
- Lists of articles or versions are passed as lists of dict objects with consistent keys.

### Endpoint Responses
- All routes that render HTML respond with Jinja2 rendered templates.
- POST routes that alter state may return redirect responses or reload templates with form feedback.
- JSON responses could be added optionally for asynchronous data fetching but are not specified.

### Coordination Points with Frontend
- IDs in frontend elements correspond to data passed, e.g., article IDs used in URLs and button IDs.
- The structure of article, version, and analytics data objects must align exactly for seamless rendering.
- Form field names and buttons in frontend templates must match backend expected POST parameters.
- Session username and authentication state must be reflected in rendered templates for personalized content.

---

**This architectural design ensures modular, maintainable backend implementation that cleanly separates concerns and supports precise frontend integration for ContentPublishingHub.**

---
