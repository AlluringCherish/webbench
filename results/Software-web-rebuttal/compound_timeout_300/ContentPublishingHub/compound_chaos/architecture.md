# Backend Architecture Design Document

## 1. Overview
This architectural document outlines the backend design for the Flask-based web application described in `design_spec.md`. It serves as a comprehensive guide for backend developers and system architects to implement the version control, approval workflows, and integration points, ensuring seamless coordination with the frontend components.

---

## 2. Application Structure and Components

### 2.1 Application Structure
- **App Initialization (`app/__init__.py`)**: Initializes the Flask app, configures extensions (like database ORM, migration tools), and registers Blueprints for modular routes.
- **Blueprints**:
  - `articles`: Handles article management, including creation, editing, and versioning.
  - `users`: Manages user authentication and profile.
  - `approvals`: Manages approval workflows for article versions.
  - `analytics`: Provides analytics endpoints related to article usage.
- **Models (`app/models.py`)**: Defines ORM models for `User`, `Article`, `Version`, `Approval`, `Comment`, `WorkflowStage`, and `Analytics` reflecting the schemas specified in the file schema section.
- **Services Layer (`app/services/`)**: Contains business logic implementing version control, state transitions, approval processes, and integration handling.
- **Database**: A relational database (e.g., PostgreSQL) used for persistent storage. Tables correspond to provided schemas in `users.txt`, `articles.txt`, etc.
- **Configuration (`config.py`)**: Configures environment-specific settings, including integration endpoints and credentials.

### 2.2 Version Control and State Management
- **Versioning Model**:
  - Each article can have multiple versions identified by `version_id`.
  - `version_number` tracks incrementing versions per article.
  - Content changes, author, timestamp, and change summaries are stored.
- **State Machine**:
  - Article versions move through workflow stages (`workflow_stages.txt`).
  - Stages include Draft, Editor Review, Approval, Published, Archived.
  - Each stage has a defined order and permissions.
  - Transitions managed via service layer.
- **Approval Workflow**:
  - Approval entries record approver, status, comments, and timestamp.
  - Only after required approvals will a version move to "Published" status.
  - Comments linked to articles and versions support review collaboration.

### 2.3 File Management and Formats
- Text-based storage (e.g., Markdown or HTML) for article content and versions.
- Files are managed via the database with references to assets (images, tags).
- Approvals and comments stored with timestamps for auditing.

### 2.4 Interactions between Backend Components
- The service layer mediates between the Flask views and the ORM models.
- Robust validation ensures data integrity during status transitions.
- Notification services can be integrated here for informing users.

---

## 3. Flask API Endpoint Design

| Route                             | Methods | Endpoint Name           | Description                                | Input                      | Output                                |
|----------------------------------|---------|------------------------|--------------------------------------------|----------------------------|-------------------------------------|
| `/dashboard`                     | GET     | `dashboard`            | Get quick stats and dashboard info         | None                       | Dashboard data (stats, summaries)   |
| `/articles/create`               | GET, POST | `create_article`    | Form display and submit new article         | POST data: Title, Content   | Success/error message                |
| `/articles/edit/<article_id>`   | GET, POST | `edit_article`     | Edit an existing article                     | POST data: Content edits    | Updated version or error             |
| `/article/<article_id>/versions`| GET     | `article_versions`     | Get list of all article versions             | None                       | List of versions                    |
| `/articles/mine`                | GET     | `my_articles`          | List articles owned by current user         | None                       | List of articles                   |
| `/articles/published`           | GET     | `published_articles`    | List all published articles filtered/sorted| Query params: category, sort order| Filtered articles list            |
| `/calendar`                    | GET     | `calendar`              | View article publishing calendar             | None                       | Calendar data                      |
| `/analytics/article/<article_id>`| GET    | `article_analytics`     | Article analytics data                        | None                       | Analytics summary                  |

### Endpoint Logic and Input/Output
- Dynamic routes such as `/edit/<article_id>` accept and validate UUID params.
- GET methods primarily serve data and templates.
- POST methods handle data submission with validation and error messaging.
- Input data structures as per front-end forms include fields for article content, status filters, categories, comments.

---

## 4. Integration

- The backend includes API contracts compatible with the frontend's specified element IDs and expected JSON responses.
- Integration adheres strictly to the frontend element IDs such as `create-article-button`, `versions-list`, `filter-article-status`, and others for effective DOM manipulation.
- Integration with external services (e.g., email notifications, analytics) can be configured via environment variables.
- The approval process files (`approvals.txt`) and comments management are integrated into database services accessed via APIs.

---

## 5. Frontend Connection Points

- Backend endpoints correspond directly to pages/templates with element IDs matching frontend specs.
- API responses are in JSON for AJAX queries manipulating frontend components like lists and filters.
- Areas requiring close frontend-backend sync include article versioning workflows, approval status updates, comment posting and retrieval.
- Backend implements access control and data validation critical for frontend state representation accuracy.

---

## 6. Artifact Naming and Code Guidelines

- Artifacts follow strict naming conventions matching `design_spec.md` for consistency.
- Detailed inline commenting in the codebase aligns with this document.
- Only backend logic is covered; frontend implementation relies on this document for integration.

---

This document serves as the single source of truth for backend development ensuring clean separation of concerns, robust version control, and seamless integration with the specified frontend.