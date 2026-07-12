# ContentPublishingHub - Backend Architecture Design Document

---

## Section 1: Backend System Design

### 1. Flask Application Structure

The Flask backend will be organized into a modular package structure as follows:

```
content_publishing_hub/
├── app.py              # Flask app factory and application entry point
├── config.py           # Configuration settings
├── routes/             # Flask route handlers (controllers)
│   ├── dashboard.py
│   ├── articles.py
│   ├── calendar.py
│   ├── analytics.py
│   └── __init__.py
├── models/             # Data access and domain models
│   ├── user.py
│   ├── article.py
│   ├── versioning.py
│   ├── approval.py
│   ├── comment.py
│   ├── analytics.py
│   └── __init__.py
├── services/           # Business logic layer
│   ├── article_service.py
│   ├── version_service.py
│   ├── approval_service.py
│   ├── comment_service.py
│   ├── analytics_service.py
│   └── calendar_service.py
├── utils/              # Utility modules for file IO, parsing, validation
│   ├── file_manager.py # Reading/writing data/*.txt files
│   ├── validation.py
│   └── __init__.py
├── templates/          # Jinja2 templates (frontend integration)
├── static/             # Static files (CSS, JS, images)
└── tests/              # Unit and integration tests

```

### 2. Module Responsibilities

- **app.py**: Initializes the Flask app, applies configs, registers Blueprints for route modules.

- **routes/**: Contains all route/controller functions mapped to Flask routes. Each module groups related routes:
  - `dashboard.py`: dashboard route
  - `articles.py`: create, edit, version history, my articles, published articles routes
  - `calendar.py`: content calendar routes
  - `analytics.py`: article analytics route

- **models/**: Represent data entities and abstract file parsing and data loading:
  - Handling of loading, saving, and querying records from the respective data text files.
  - Model objects provide structured access (e.g., Article, Version, Approval, Comment).

- **services/**: Implements business logic and workflows using the models:
  - Version management (creating new version, retrieving history)
  - Approval workflow logic and validation
  - Analytics aggregation
  - Calendar scheduling

- **utils/file_manager.py**:
  - Centralized reading and writing of all data files (e.g., users.txt, articles.txt, article_versions.txt, approvals.txt, comments.txt, analytics.txt).
  - Performs pipe-delimited parsing, writing in predefined schemas.

- **utils/validation.py**:
  - Input validation on POST data for articles, scheduling, etc.


### 3. Data File Access and Management

All application data is stored in plain pipe-delimited text files under a `data/` directory. The system uses:

- **FileManager** (in utils/file_manager.py) to abstract:
  - Reading all records of a file as list of dicts
  - Appending new records safely
  - Updating or deleting records by rewriting files

- Each model class will interact with FileManager to load data on demand.
- Updates like creating articles, saving versions, approving, commenting will use service methods wrapping file operations.

This approach supports simple storage without database dependency.

### 4. Data Flow Between Components

1. **HTTP Request** 1 Controller 1 Service 1 Model 1 File
  - Routes parse inputs, call service layer.
  - Services validate, process business logic.
  - Models read/write data files as needed.

2. **Response Generation**
  - Route functions compile data into context dicts.
  - Render templates with passed context.

3. **Versioning & Approval**
  - Services manage article version creation and approval state transitions.

4. **Analytics Aggregation**
  - Analytics service summarizes daily metrics for display.

---

## Section 2: Routing and API Endpoints

| Route Pattern                     | HTTP Method(s) | Controller Function       | Input Parameters                 | Output / Template             |
|---------------------------------|----------------|---------------------------|---------------------------------|------------------------------|
| `/dashboard`                    | GET            | `dashboard`               | Session user info (username)     | Renders `dashboard.html` with username context |
| `/article/create`               | GET, POST      | `create_article`          | POST: article form data         | GET: render form, POST: validation errors or redirect|
| `/article/<int:article_id>/edit`| GET, POST     | `edit_article`            | `article_id`, POST form data   | Edit article page with article data and errors if any|
| `/article/<int:article_id>/versions` | GET       | `article_version_history` | `article_id`                   | Version history page with versions, optional comparison|
| `/articles/mine`                | GET            | `my_articles`             | Session username, optional filters| List of user's articles|
| `/articles/published`           | GET            | `published_articles`      | Query filter params (category, sort) | List of published articles|
| `/calendar`                    | GET, POST      | `content_calendar`        | POST: scheduling input        | Calendar view with scheduled items|
| `/article/<int:article_id>/analytics` | GET      | `article_analytics`       | `article_id`                  | Analytics data for article|

### 1. Dynamic Route Patterns

- `<int:article_id>` URL parameter will be converted to integer.
- These IDs are passed to controller functions to query relevant data.

### 2. Controller Function Input / Output

- GET methods typically retrieve data from models and services.
- POST methods accept form data, validate, update data files, and handle errors.
- Validation errors passed to templates as context dictionary keyed by field.

### 3. User Sessions and Authentication

- The design spec implies a logged-in user context is necessary.
- Session management handled centrally (not detailed in spec), assumed accessible via Flask `session` and `g`.
- Routes requiring user-specific data (e.g., `/dashboard`, `/articles/mine`) will extract username from session.
- Authentication considerations (login, logout) are out of scope but hooks can be added.

---

## Section 3: Version Control Design

### 1. Article Versioning and Workflow Architecture

- Each article can have multiple versions, tracked via `article_versions.txt`.
- Versions identified by `version_id` globally unique and `version_number` per article.
- Content and metadata stored per version (content, author, timestamp, change summary).

### 2. Approval Workflow

- Approvals stored in `approvals.txt` linking to article and version by IDs.
- Each approval tracks approver username, status (`approved`, `rejected`, `revision_requested`), comments, and timestamp.
- Workflow stages defined in `workflow_stages.txt` describe approval steps per article category.
- Approval status impacts article status (e.g., approved versions enable publishing).

### 3. Comments Linking

- Comments from `comments.txt` link to articles and specific versions.
- Allow reviewers and users to provide feedback associated with a version.

### 4. Storage Interaction

- Version creation appends new record in `article_versions.txt`.
- Approvals appended or updated in `approvals.txt` with each review status.
- Comments appended in `comments.txt`.
- Services coordinate file writes ensuring consistency.

---

## Section 4: Frontend Integration Points

### 1. Template Data Passing

- Route handlers provide context dictionaries with required variables matching design_spec.md.
- Context keys align exactly with frontend expectations for variable names and types.
- Examples:
  - `username` for user name display
  - `article`, `current_version`, `validation_errors` in edit/create pages
  - Lists of articles, versions, scheduled items as lists of dict objects

### 2. Endpoint Responses and Rendering

- All routes respond by rendering Jinja2 templates with context.
- POST actions typically redirect on success to avoid resubmissions, re-render form with errors on validation failure.

### 3. Coordination Points

- Frontend and backend teams must agree on:
  - Exact data structure formats for lists and dicts passed to templates
  - Field naming in validation error dictionaries
  - Expected element IDs and their usage from design_spec.md for JS bindings
  - Button actions triggering specific routes and methods

### 4. Static Assets

- Static resources such as CSS, JS, and images served from `/static` folder.

---

# Summary

This architecture specifies a clean separation of concerns between routing, business logic, data models, and file-based storage, facilitating scalable backend development. Clear routing and data context definitions enable straightforward frontend integration while the version control workflow supports complex content management requirements.

This document should allow independent backend and frontend teams to proceed confidently without ambiguity.

---

End of architecture.md
