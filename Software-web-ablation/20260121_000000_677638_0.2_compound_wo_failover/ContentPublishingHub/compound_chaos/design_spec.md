# Design Specification for Content Publishing Hub

## Article and Versioning
- Each article identified by `article_id`.
- Multiple versions exist per article with fields: version_id, version_number, creation_date, stage (draft, review, approved, rejected), author, comments.
- Version data stored in `article_versions.txt`.
- Approval stages tracked in `approvals.txt` associated with version_id.
- Status filtering supported on frontend and backend.

## API Endpoints
- `GET /articles`: return filtered list based on status and category.
- `POST /article/create`: accepts article data and creates initial version.
- `POST /article/<article_id>/edit`: submit edits; creates new version.
- `GET /article/<article_id>/versions`: return version history.
- `POST /article/<article_id>/version/<version_id>/restore`: revert.
- `GET /article/<article_id>/analytics`: returns views, visitors, average time.

## Frontend Components
- Filter inputs: Dropdowns for category, status; text inputs for search.
- Buttons to save draft, submit for approval, publish.
- Textareas for content editing identified by IDs for state management.
- Analytics page shows numeric data and charts.
- Version comparison UI for side-by-side view.

## Data structures
- Articles: title, category, content (current version), author, created_date, publish_date, tags, featured_image.
- Versions: version_number, author, create_date, stage, comment.
- Analytics: article_id, date, views, unique_visitors, avg_read_time.
- Approvals: approval_id, version_id, status (approved, rejected, under_review), approver, date.

## Workflow
- Users can create, edit, and save drafts.
- Version history accessible with restoration capability.
- Approvals require admin/editor roles.
- Analytics updated in near real-time.
- Published articles filtered and sorted via frontend controls.

## Routing
- Consistent RESTful routes with clear naming conventions.
- Frontend templates fetch data asynchronously or use server-side rendering.

## Authentication
- Login system tied to users file.
- Role-based access control to restrict actions.

## Notes
- Storage is flat-file based; consider database migration for scalability.
- Keep frontend modular; separate JS scripts per page.
- Ensure error handling and user feedback mechanisms.
