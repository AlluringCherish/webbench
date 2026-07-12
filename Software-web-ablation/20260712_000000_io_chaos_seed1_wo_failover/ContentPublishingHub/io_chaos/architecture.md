# ContentPublishingHub Backend Architecture Design Document

---

## Section 1: Backend System Design

### Flask Application Structure

The Flask application is organized into the following core modules and packages:

- **app/** 
  - `__init__.py`: Initializes the Flask app instance, loads configuration, and registers blueprints.
  - `routes.py`: Contains route definitions and controller functions for handling HTTP requests.
  - `models.py`: Defines data access objects (DAOs) or service classes for interacting with the data files.
  - `services/` 
    - Contains business logic modules such as article management, version control, approvals, comments, and analytics.
  - `utils.py`: Utility functions for common tasks such as parsing and writing data files.
  - `auth.py`: (Optional) Manages user session, authentication, and authorization logic.

### Module Responsibilities

- **routes.py**
  - Define all Flask routes as per the design_spec.md.
  - Map routes to controller functions that handle input, invoke service logic, and return template rendering or JSON.

- **models.py**
  - Abstracts read/write operations to text data files in `data/` directory.
  - Provides CRUD methods for users, articles, article versions, approvals, comments, analytics, and workflow stages.

- **services/**
  - Encapsulates business-specific logic like article version workflows, approval mechanisms, comment threading.
  - Implements data validation, version incrementing, approval state changes, and analytics aggregation.

- **utils.py**
  - Contains helper functions for parsing pipe-delimited text files, date/time formatting, and file locking to manage concurrent writes.

- **auth.py**
  - Handles user login sessions; for now assumes simple session management without OAuth or advanced security as not specified.

### Data File Access and Management

- All application data is stored in plain text files located in the `data/` directory relative to the app root.
- Each data file (`users.txt`, `articles.txt`, `article_versions.txt`, `approvals.txt`, `comments.txt`, `workflow_stages.txt`, `analytics.txt`) follows the specified pipe (`|`) delimited schema.
- Models layer will open files in read or append mode with appropriate locking to prevent data corruption.
- When updates are necessary, files will be rewritten fully or updated carefully depending on operation.
- The system will load data on demand and cache where feasible for performance.

### Data Flow

- HTTP requests arrive at `routes.py` endpoints.
- Routes parse request parameters (query, form, URL).
- Relevant service layer modules are called to perform business operations.
- Services call model functions to read or update the underlying text files.
- Data retrieved is assembled into Python data structures (dict, list) and passed back up.
- Routes render HTML templates, passing context variables needed for frontend rendering.


## Section 2: Routing and API Endpoints

| Route Pattern                      | HTTP Methods | Controller Function       | Input                          | Output (Data Passed to Template)                          |
|----------------------------------|--------------|---------------------------|--------------------------------|-----------------------------------------------------------|
| `/dashboard`                     | GET          | `dashboard()`             | Session username               | `username` (str), `quick_stats` (dict), `recent_activity` (list) |
| `/article/create`                | GET, POST    | `create_article()`        | POST form: `title` (str), `content` (str)                 | On GET: none; On POST: redirects or shows form errors      |
| `/article/<int:article_id>/edit` | GET, POST    | `edit_article(article_id)`| GET retrieves `article_id`; POST with updated `title`, `content` | GET: article details; POST: success redirect or errors    |
| `/article/<int:article_id>/versions` | GET      | `article_version_history(article_id)` | URL param `article_id` | `article_id` (int), `versions` (list of dicts)              |
| `/articles/mine`                | GET          | `my_articles()`           | Session username, optional filters                          | `username` (str), `articles` (list of dicts), `filter_status` (str) |
| `/articles/published`           | GET          | `published_articles()`    | Query params: optional category filters, sort order         | `articles` (list of dicts), `filter_category` (str), `sort_order` (str) |
| `/calendar`                    | GET          | `content_calendar()`      | Query param for calendar view mode                           | `calendar_view` (str), `scheduled_items` (list of dicts)  |
| `/article/<int:article_id>/analytics` | GET     | `article_analytics(article_id)` | URL param `article_id`                                  | `article_id` (int), `analytics_overview` (dict)            |

### Dynamic Route Patterns

- Routes with `<int:article_id>` parameter retrieve and operate on specific articles.
- Strict type enforcement for URL parameters to ensure data integrity.

### User Sessions and Authentication

- Session management handled to identify logged-in user (`username`).
- Routes dependent on user identity (e.g., `/articles/mine`, `/article/create`) use session check.
- Authentication logic modularized in `auth.py`, though specifics are outside current spec scope.


## Section 3: Version Control Design

### Versioning and Approval Workflow Architecture

- Each article can have multiple versions stored in `article_versions.txt`.
- Version records include `version_id`, `article_id`, `version_number`, `content`, `author`, `created_date`, and `change_summary`.
- Workflow stages defined per article category in `workflow_stages.txt` establish the approval process.

### Version History Management

- The backend loads all versions for an article and presents them in `version_history.html`.
- User can view, compare, and restore previous versions.
- New versions created by incrementing the latest `version_number`.

### Approval Records

- Approvals stored in `approvals.txt` link to an `article_id` and specific `version_id`.
- Each approval has an `approver`, `status` (approved, rejected, revision_requested), `comments`, and a timestamp.
- Approval changes update the article status accordingly (e.g., from pending_review to approved).

### Comments Tracking

- Comments linked to article versions are stored in `comments.txt`.
- Comment records include `comment_id`, `article_id`, `version_id`, `user`, `comment_text`, and timestamp.
- Comments assist reviewers and authors during the approval process.

### Storage Interaction

- All version control and approval data access abstracted via models/services for reading and writing to 
  `article_versions.txt`, `approvals.txt`, and `comments.txt`.
- Concurrency managed via file locks.


## Section 4: Frontend Integration Points

### Data and Context Passing

- Backend routes render Jinja2 templates, passing explicit context variables as specified in design_spec.md.
- Context variables match the template element IDs and expected data structures (strings, dicts, lists).
- Data structures are designed to directly support frontend UI components like tables, dropdowns, and lists.

### Endpoint Response Structure

- All GET routes return rendered HTML templates with data context.
- POST routes either redirect on success or rerender pages with error messages in context.
- For dynamic pages (e.g., article edit, version history), relevant entity ID and loaded data are passed to facilitate frontend display.

### Coordination with Frontend

- Backend must closely coordinate with frontend developers on data structure formats to match template requirements.
- Templates rely on backend to provide data such as:
  - User session information (username)
  - Filter and sorting selections to maintain UI state
  - Lists of articles, versions, comments conforming to schema
  - Approval statuses and workflow stages
  - Analytics metrics formatted for direct consumption

---

This architecture document provides the required detail to develop the backend Flask application and integrate effectively with frontend components for ContentPublishingHub.

Any further extension or refinement should maintain modular separation and clear data contract boundaries.
