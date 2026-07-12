# ContentPublishingHub Backend Architecture Design Document

---

## Section 1: Backend System Design

### 1.1 Flask Application Structure

The Flask backend application will be organized into a modular package structure to separate concerns clearly and facilitate maintainability:

```
/content_publishing_hub
  /app
    /routes            # Route handlers (controllers) for each app area
    /services          # Business logic and processing services
    /models            # Data access and manipulation abstractions
    /utils             # Utility functions (file IO, helpers)
    /version_control   # Versioning and approval workflow logic
    /auth              # Authentication and session management if needed
    /templates         # HTML template files (frontend integration)
    __init__.py        # Initializes Flask app and registers blueprints
  /data                # Raw data text files (articles.txt, approvals.txt, etc.)
  config.py            # Configuration settings
  run.py               # Application entry point
  requirements.txt     # Python dependencies
```

### 1.2 Module Responsibilities

- **routes**: Defines all Flask route functions corresponding to URL endpoints. Routes handle HTTP requests, parse inputs, invoke service layer, and return rendered templates or JSON.

- **services**: Encapsulates core business logic such as article creation, editing, versioning, approval processing, and analytics summarization. Services operate on data models and help keep routes lean.

- **models**: Interacts directly with the underlying data files (e.g., articles.txt, comments.txt). Implements loading, parsing, querying, updating, and saving text file data with appropriate locking or synchronization.

- **utils**: Provides helper functions for file reading/writing, date formatting, data validation, and any other shared utility.

- **version_control**: Dedicated to managing article version history, approvals, comments, and workflow stages. Coordinates with models to persist versioning data.

- **auth**: Manages user session handling and authentication (extendable). Currently scoped for session management of logged-in users.

### 1.3 Data File Access and Management

- All persistent data stored as plain text files under `/data` directory.
- The `models` layer abstracts the file format specifics and offers programmatic access to data.
- Read/write methods use appropriate file locking or atomic writes to avoid data corruption.
- Loading data into memory for querying and saving back after modifications.
- Data integrity is critical, especially for articles and versioning; thus, service layer enforces validation and consistency.

### 1.4 Data Flow

- User requests hit Flask routes (controllers).
- Routes validate inputs and invoke corresponding service methods.
- Service methods utilize models to load and update data files.
- Version control service manages version and approval related workflows.
- Responses packaged with context variables and passed to frontend templates for rendering.
- For forms (POST), data flows from frontend to route, then service, and finally models to update files.
- For GET requests, data is gathered from models, processed by services, and sent to templates.

---

## Section 2: Routing and API Endpoints

| Route | Methods | Controller Function | Input Parameters | Output / Template | Notes |
|-----------------------------|---------|-----------------------|---------------------------|------------------------|--------|
| /dashboard | GET | dashboard | session user info | dashboard.html with user stats, activity | Displays personalized dashboard
| /article/create | GET, POST | create_article | POST: form data (title, content, etc.) | create_article.html or redirect | Creation form and submission
| /article/&lt;article_id&gt;/edit | GET, POST | edit_article | article_id (dynamic), POST form data | edit_article.html with article data | Edit article and save versions
| /article/&lt;article_id&gt;/versions | GET | article_version_history | article_id | version_history.html with version list | View article version history
| /articles/mine | GET | my_articles | session username, optional filters | my_articles.html with user articles | Filters by user and status
| /articles/published | GET | published_articles | optional filter_category, sort_by | published_articles.html with published list | List published articles
| /calendar | GET | content_calendar | optional view selector | content_calendar.html with schedule data | Content calendar view
| /article/&lt;article_id&gt;/analytics | GET | article_analytics | article_id | article_analytics.html with stats | Shows analytics summary

### Routing Details

- Dynamic parameters like `article_id` passed via URL segment and validated to int or string as needed.
- GET routes primarily fetch and display data.
- POST routes process form submissions for create/edit actions.
- Session data used to capture logged-in username for personalized data filtering.
- Authentication layers (if added) will guard sensitive routes.

---

## Section 3: Version Control Design

### 3.1 Architecture Overview

- Article versions are managed as sequential numbered versions linked to a core article ID.
- Each version stores full content, author, timestamp, and change summary.
- Approval records track reviewer decisions per version including status, comments, and timestamps.
- Comments are linked to article versions allowing contextual discussion.
- Workflow stages define required approvals per article category.

### 3.2 Data Relationships

- `article_versions.txt` links by `article_id` with multiple versions distinguished by `version_number`.
- `approvals.txt` references `article_id` and `version_id` to track approval status per version.
- `comments.txt` similarly linked per article and version for ongoing feedback.
- `workflow_stages.txt` defines pipeline stages per article category affecting approval requirements.

### 3.3 Versioning Workflow

- When an article is edited and saved as new version, a new version entry is appended with incremented version_number.
- Approvers can mark versions as approved, rejected, or request revisions via the approval workflow.
- Comments can be added during review for each version.
- Version history pages query and display all versions and their approval summary.
- Restoration of previous versions involves copying content from a selected version to create a new draft version.

### 3.4 Storage and Access

- Version control logic accesses respective data files through model abstractions.
- Updates to versions, approvals, and comments are persisted atomically to respective text files.

---

## Section 4: Frontend Integration Points

### 4.1 Data Passing to Templates

- Each route renders templates with context variables matching design_spec.md specifications.
- Data such as username, article lists, version details, analytics summaries are passed as dicts, lists, or scalar values.
- Variables follow clear naming conventions e.g., `article_id`, `versions`, `quick_stats`, `recent_activity`.

### 4.2 Endpoint Responses

- GET endpoints render full HTML pages populated with context data.
- POST endpoints typically redirect post-processing or return validation messages within templates.

### 4.3 Coordination with Frontend

- Frontend teams will consume context variables to populate page elements identified by specified IDs.
- Careful coordination on data structures, e.g., list of dicts for articles and versions, is necessary to ensure correct rendering.
- Navigation actions mapped to routes should be consistent with backend URL structure.

---

This architecture document provides the comprehensive backend design, routing logic, version control strategy, and frontend integration approach to enable independent development and integration of the ContentPublishingHub system.
