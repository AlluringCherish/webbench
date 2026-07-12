# Architecture Document for Content Publishing Hub

---

## 1. Backend System Design

### 1.1 Overview of Flask Application Structure

The backend is structured as a Flask application with a modular package design to separate concerns clearly. The main components are organized as follows:

- `app/`
  - `__init__.py`: Initializes Flask app and registers blueprints.
  - `routes.py`: Contains route definitions mapped to controller functions.
  - `controllers/`
    - `dashboard.py`: Business logic for dashboard-related functionality.
    - `articles.py`: Business logic and data processing for article creation, editing, versioning, and analytics.
    - `analytics.py`: Handles analytics data retrieval and processing.
    - `calendar.py`: Handles article scheduling and calendar view-related operations.
  - `models/`
    - `article.py`: Data access objects & helpers related to articles and versions.
    - `approval.py`: Data management for approval workflow.
    - `comments.py`: Handling comments data.
    - `analytics.py`: Data access for article analytics.
  - `services/`
    - `file_access.py`: Abstracts reading and writing operations from/to the data/*.txt files.
    - `version_control.py`: Encapsulates article versioning and approval logic.
    - `session_management.py`: (If authentication is included) manages sessions and user state.
  - `utils.py`: General utility functions (e.g., date/time conversions).
  - `config.py`: Configuration parameters.

### 1.2 Module Responsibilities

- **Routing (`routes.py`)**: Defines URL endpoints and their HTTP methods, delegates processing to controller functions.
- **Controllers (`controllers/`)**: Handle the orchestration of data retrieval, business logic, and preparation of data for the frontend.
- **Models (`models/`)**: Responsible for accessing data from the storage layer. Translates raw text file data (CSV/pipe-delimited) into Python objects/dictionaries.
- **Services (`services/`)**: Provide reusable functions for accessing and manipulating data files.
- **Version Control (`services/version_control.py`)**: Manages saving, restoring, and approving article versions, interaction with version history, approvals, and comments files.
- **Session Management**: If user login and authentication are implemented (implied by user data in users.txt and presence of admin and users), this module will handle session cookies and authentication checks.

### 1.3 Data File Management Strategy

- All primary data is stored in text files in the `data/` directory.
- File formats are pipe-delimited text files ("|" separator), including:
  - `articles.txt`: Core article metadata.
  - `article_versions.txt`: Stores the version history for each article.
  - `approvals.txt`: Approval states and workflow data for versions.
  - `comments.txt`: Comments on article versions.
  - `analytics.txt`: Article viewing and engagement metrics.
  - `users.txt`: User information.
  - `workflow_stages.txt`: Defines stages in the approval workflow.

- File access is handled by the service layer (`services/file_access.py`) which provides read and write utilities converting between delimited lines and structured Python objects.
- Changes are synchronized carefully to prevent inconsistency; file locking or transaction-like patterns might be employed to avoid race conditions (implementation detail subject to environment).

### 1.4 Data Flow Between Components

- **Client Request -> Routing Layer**: Incoming HTTP requests are matched to routes in `routes.py`.
- **Routing -> Controller**: Route handlers invoke controller functions passing request parameters.
- **Controller -> Model/Service**: Controllers use models and services to retrieve or persist data.
- **Model -> Data Files**: Models interact with the `services/file_access.py` to read/write data files.
- **Controller -> Frontend**: Processed data sent to frontend templates via rendering context or JSON responses.

This layered approach ensures separation of concerns, maintainability, and scalability.

---

## 2. Routing and API Endpoints

### 2.1 Route Overview

| Route                              | HTTP Method(s) | Controller Function             | Description                                    |
|----------------------------------|----------------|-------------------------------|------------------------------------------------|
| `/dashboard`                     | GET            | `dashboard.get_dashboard()`    | Renders main dashboard with article summaries and recent activities.
| `/articles/mine`                 | GET            | `articles.get_user_articles()` | Lists articles authored by logged-in user.
| `/articles/published`            | GET            | `articles.get_published_articles()` | Lists all published articles.
| `/article/create`                | GET, POST      | `articles.create_article()`    | GET presents article creation form; POST processes new article submission.
| `/article/<article_id>/edit`    | GET, POST      | `articles.edit_article(article_id)` | GET shows article edit form; POST updates article details.
| `/article/<article_id>/versions`| GET            | `articles.get_article_versions(article_id)` | Lists version history for article.
| `/article/<article_id>/versions/<version_id>/restore`| POST | `version_control.restore_version(article_id, version_id)` | Restores content to specified version.
| `/article/<article_id>/analytics`| GET           | `analytics.get_article_analytics(article_id)` | Displays analytics for an article.
| `/calendar`                     | GET            | `calendar.get_schedule()`      | Shows article publishing calendar view.
| `/article/<article_id>/comments` | GET, POST      | `comments.manage_comments(article_id)` | GET gets comments for article version; POST adds new comment.


### 2.2 Route Details

- **Dynamic Routes**: Routes with `<article_id>` and `<version_id>` parse the parameter from the URL and validate them prior to invoking logic.
- **HTTP Methods:**
  - GET requests serve page views or return data.
  - POST requests accept form data or JSON payloads to persist changes.

### 2.3 Session and Authentication Handling

- Authentication is presumed based on presence of users data; this may include login/logout routes (not in spec).
- Protected routes (e.g., create/edit article, approve versions) require user session validation.
- Sessions handled via Flask session cookies; middleware or decorators enforce authorization.

---

## 3. Version Control Design

### 3.1 Architecture Supporting Versioning and Approval

- Each article has multiple versions stored in `article_versions.txt` with fields including `version_id`, `article_id`, `version_number`, `content`, `author`, `created_date`, and `change_summary`.
- Versioning workflow stages are defined in `workflow_stages.txt`.
- Approvals are recorded in `approvals.txt` linking `approval_id` to `article_id`, `version_id`, `approver`, `status` (e.g. approved, rejected), `comments` and timestamp.
- Comment threads on versions stored in `comments.txt` attached to `article_id` and `version_id`.

### 3.2 Data Relations

- Versions belong to one article.
- Approvals relate to specific article versions.
- Comments belong to specific article versions.

### 3.3 Workflow

- Authors create new article versions.
- Versions are submitted for approval, recorded in `approvals.txt`.
- Approvers can approve or reject with feedback via comments.
- Approved versions are eligible for publishing.
- System allows restoring prior versions by re-saving selected version content as latest.

### 3.4 Backend Interaction With Storage Files

- `article_versions.txt`: Read and write operations for adding or retrieving version records.
- `approvals.txt`: Updates when approval status changes.
- `comments.txt`: Reading and writing comments linked to versions.

Service layer methods in `version_control.py` encapsulate these operations to maintain data integrity.

---

## 4. Frontend Integration Points

### 4.1 Passing Data to Templates

- Backend renders Jinja2 templates passing context dictionaries containing data structures such as lists of article dicts, single article dicts, version lists, analytics metrics, calendar entries.
- Examples:
  - Dashboard: passes `articles`, `recent_activities`, `filters`.
  - Article Edit: passes `article`, `current_version`.
  - Version History: passes list of versions with metadata.
  - Analytics page: metrics grouped by date, views, shares, visitors.

### 4.2 Endpoint Responses

- HTML pages: Most GET routes render templates with appropriate data.
- POST routes redirect to corresponding GET routes after update to refresh page state.
- Certain API-like endpoints may return JSON data for asynchronously loaded frontend components (e.g., calendar data).

### 4.3 Critical Backend/Frontend Coordination

- Data format for articles includes fields such as title, content, status, publish_date, category, tags, featured_image, meta_description, and author’s name.
- Versions include version number, created date, author, and change summary; frontend expects consistent keys.
- Approval status and comments structure must align so frontend can display threaded comments and status messages accurately.
- Filters and sorting options are passed via URL query arguments and must be supported consistently on backend and frontend.

---

# End of Architecture Document
