import asyncio
import sys
import os
import time
import asyncio
from typing import List, Dict, Any
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from essential_modules import build_resilient_agent, execute, aggregate_task_metrics
from chaos import ChaosController

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create comprehensive design specification enabling independent backend/frontend development with detailed page elements and data schema definitions\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"SystemArchitect creates design_spec.md with 3 sections (Flask Routes, HTML Templates, Data Schemas) \"\n        \"covering all MusicStreaming pages, UI elements with IDs, and data file formats.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"SystemArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications.\n\nYour goal is to create comprehensive design specifications that enable Backend and Frontend developers to implement the MusicStreaming application independently with clear deliverables.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Create design_spec.md containing three main sections: Flask Routes, HTML Templates with element IDs, and Data Schemas\n- Ensure all MusicStreaming pages and their UI elements with exact IDs are fully specified\n- Include all data file formats with exact fields and example data as defined\n- Do NOT include implementation details or presume backend/frontend internal code\n\n**Section 1: Flask Routes Specification (For Backend Developer)**\n\nProvide a detailed route table with the following columns:\n- Route Path: URL pattern (e.g., /dashboard, /songs/<int:song_id>)\n- Function Name: Flask function name (snake_case)\n- HTTP Method(s): GET or POST as applicable\n- Template File: Template filename to render\n- Context Variables: All variables passed, including their data types and structures\n\nRequirements:\n- Include all pages as routes with explicit function names matching page purposes\n- Root route '/' must redirect to dashboard page route\n- Clearly define dynamic routes with parameters (e.g., song_id, playlist_id)\n- Context variables must specify exact types (str, int, list, dict) and structures, including nested fields\n- Ensure all routes are consistent with UI element navigation mappings\n\n**Section 2: HTML Template Specifications (For Frontend Developer)**\n\nFor each page template, provide:\n- Template File Path: templates/{template_name}.html\n- Page Title: Exact <title> and <h1> content\n- Required Element IDs: Complete list with exact IDs and element types (Div, Button, Input, Dropdown, Table, etc.)\n- Context Variables: Detailed description of all variables available in the template with their structure\n- Navigation Mappings: Button and link element IDs mapped to Flask route function names; include dynamic id patterns\n\nRequirements:\n- All element IDs must exactly match those specified in the user task document\n- Context variables must correspond exactly to those in Section 1\n- Navigation targets and function names must align with Section 1 routes\n- Include notes on dynamic element ID patterns using Jinja2 syntax for rendering\n\n**Section 3: Data File Schemas (For Backend Developer)**\n\nFor each data text file in the data directory, provide:\n- Filename and exact relative path (e.g., data/songs.txt)\n- File format: pipe-delimited (|)\n- Exact field order with clear descriptive field names\n- Field data types and brief description for each field\n- 2-3 realistic example rows as per user task examples\n\nRequirements:\n- Ensure strict adherence to field order and delimiter format as backend depends on it\n- Example data must reflect realistic sample content for validation\n- Describe any relationships or foreign keys between files (e.g., artist_id references)\n\nCRITICAL SUCCESS CRITERIA:\n- Backend developer can implement app routes and data loading based solely on Section 1 and Section 3\n- Frontend developer can create all templates with exact IDs and navigation using Section 2 only\n- All element IDs, context variable names, and data schemas exactly match user requirements\n- Use write_text_file tool to save design_spec.md without interactive code snippets or partial outputs\n- Do NOT add assumptions beyond provided user task and data specifications\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Check design_spec.md backend sections for completeness: all Flask routes with function names, parameters, HTTP methods; data schema definitions for text files with exact fields and formats.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": (\n                \"Check design_spec.md frontend sections for completeness: all HTML templates with exact element IDs, page layouts, reference to navigation flow and context variables.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def parallel_implementation_phase(\n    goal: str = \"Implement backend logic and frontend templates in parallel according to design specification\",\n    collab_pattern_name: str = \"Parallel Flow\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py with all defined Flask routes and data loading/saving logic from design_spec.md. \"\n        \"FrontendDeveloper implements HTML templates with specified element IDs and navigation as per design_spec.md.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to implement a complete Flask backend that fully realizes all routes, data management, and business logic as specified in the design specification.\n\nTask Details:\n- Read design_spec.md from CONTEXT, focusing on Flask route definitions, expected HTTP methods, context variables, and data file schemas\n- Implement app.py with ALL Flask routes following exact route names, function names, and data handling requirements\n- Load and save data from/to data/*.txt files using pipe-delimited formats as specified\n- Do NOT read or modify frontend templates; do NOT assume unspecified features outside design_spec.md\n\nImplementation Requirements:\n1. **Flask Application Setup**\n   - Initialize Flask app with appropriate configurations\n   - Implement root '/' route that redirects to Dashboard page per specification\n\n2. **Data Loading and Saving**\n   - Parse data files from data directory using exact schema from design_spec.md\n   - Use robust file reading with pipe-delimited parsing (e.g., line.strip().split('|'))\n   - Map data fields precisely as defined for each entity (songs, artists, albums, genres, playlists, playlist_songs)\n   - Implement data writing functions if necessary for playlist creation or update\n\n3. **Route and Business Logic Implementation**\n   - Implement all routes with exact function names and HTTP method handlers (GET, POST) defined in design_spec.md\n   - Pass correct context variables to templates matching design_spec.md names and types\n   - Handle form submissions and update data files accordingly (e.g., creating playlists, adding/removing songs)\n   - Implement error handling for missing or malformed data gracefully\n\n4. **Best Practices**\n   - Use url_for for all redirects\n   - Ensure data consistency across routes\n   - Include \"__main__\" guard to run app in debug mode on port 5000\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save your completed app.py\n- Follow design_spec.md content EXACTLY for routes, data schema, and logic\n- Do NOT invent features or deviate from provided specification\n- Do NOT output code in chat messages only—always save via write_text_file\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask applications.\n\nYour goal is to implement complete frontend HTML templates that fulfill all page designs, contain the specified element IDs, and follow navigation flows exactly as described in the design specification.\n\nTask Details:\n- Read design_spec.md from CONTEXT, focusing on template specifications including element IDs, page titles, context variables, and navigation routes\n- Implement all frontend templates (*.html) corresponding to each application page\n- Ensure all static and dynamic element IDs are implemented exactly as specified, including Jinja2 syntax for dynamic IDs\n- DO NOT read or modify backend code or logic; do NOT assume additional features outside design_spec.md\n\nImplementation Requirements:\n1. **Template Structure**\n   - Use standard HTML5 with Jinja2 syntax for templating\n   - Include correct <title> and <h1> tags with exact page titles from specification\n   - Wrap page content using main container div with specified IDs\n\n2. **Element IDs and Dynamics**\n   - Implement ALL static IDs exactly as named\n   - For dynamic elements (e.g., add-to-playlist-button-{song_id}), use proper Jinja2 templating:\n     ```html\n     id=\"add-to-playlist-button-{{ song.song_id }}\"\n     ```\n   - Ensure dynamic IDs match naming patterns from specification exactly\n\n3. **Navigation and Links**\n   - Implement navigation buttons and links using url_for with exact route function names as provided\n   - Static buttons:\n     ```html\n     <a href=\"{{ url_for('function_name') }}\"><button id=\"element-id\">Text</button></a>\n     ```\n   - Dynamic links with parameters:\n     ```html\n     <a href=\"{{ url_for('function_name', id=item.id) }}\">\n       <button id=\"button-id-{{ item.id }}\">View</button>\n     </a>\n     ```\n\n4. **Forms (for POST actions)**\n   - Implement HTML forms for creating playlists, adding/removing songs, with method=\"POST\" and correct action URLs\n   - Use input elements with specified IDs and names\n\n5. **Context Variables**\n   - Access context variables as specified with correct field access (e.g., {{ song.title }}, {{ artist.name }})\n   - Use loops and conditionals as needed to render lists and tables\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save all template files in templates/ directory\n- ALL element IDs must be exact and case-sensitive as specified\n- Page titles and navigation must match design_spec.md precisely\n- Do NOT add extra templates or IDs beyond the specification\n- Do NOT output code in chat messages only—always save via write_text_file\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Validate app.py implements all Flask routes correctly according to design_spec.md including route names, HTTP methods, required data handling, and that root route redirects to the Dashboard page.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify templates/*.html implement all page elements with correct IDs, context variable usage, navigation flows, and page titles matching design_spec.md.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def testing_and_validation_phase(\n    goal: str = \"Perform comprehensive testing and validation of backend and frontend implementations; correct any issues found\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"Tester tests both app.py and templates/*.html functionality against user requirements and design_spec.md; produces feedback. \"\n        \"BackendDeveloper and FrontendDeveloper iteratively fix issues based on Tester feedback until approval.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"Tester\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in functional and UI testing of Python-based web applications with Flask backend and HTML frontend.\n\nYour goal is to perform comprehensive testing and validation of both backend and frontend implementations to verify that all user features work correctly, identifying issues and producing detailed feedback with approval status.\n\nTask Details:\n- Read app.py and templates/*.html from CONTEXT as current implementation artifacts\n- Read design_spec.md and user_task_description to understand all required features and expected behaviors\n- Test ALL user requirements for functionality and UI correctness across pages and features\n- Write detailed tester_feedback.txt including issue descriptions and overall approval status with [APPROVED] or NEED_MODIFY\n- Focus only on implemented features; do NOT propose new features\n\nTesting Requirements:\n1. **Functional Testing**:\n   - Verify all Flask routes respond correctly as per design_spec.md\n   - Test dynamic functionality such as search, filters, playlist creation, song playback buttons\n   - Validate data display correctness against data schemas and user requirements\n   - Confirm backend handles error cases gracefully\n\n2. **UI Testing**:\n   - Check presence and correctness of all required element IDs across pages\n   - Validate page titles and navigation flows correspond exactly to specifications\n   - Ensure buttons, forms, inputs function as expected\n   - Confirm responsive behavior and consistent styling (where applicable)\n\n3. **Feedback Format**:\n   - Use clear sections for Backend Issues, Frontend Issues, and Summary\n   - Provide exact file names and element IDs or routes where issues occur\n   - End feedback file with either [APPROVED] if no issues, or NEED_MODIFY if fixes are needed\n\nCRITICAL REQUIREMENTS:\n- Use execute_python_code to run backend tests and simulate requests\n- Use read_binary_file if visual/UI binary artifacts need analysis\n- Use write_text_file to save tester_feedback.txt with detailed findings and status marker\n- Do NOT modify any implementation files directly\n\nOutput: tester_feedback.txt\"\"\",\n            \"tools\": [\"execute_python_code\", \"read_binary_file\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"tester_feedback.txt\"}\n            ]\n        },\n        {\n            \"agent_name\": \"BackendDeveloper_Fix\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to fix backend code based on Tester feedback until the backend implementation is fully approved.\n\nTask Details:\n- Read tester_feedback.txt to identify backend issues and approval status\n- Read current app.py from CONTEXT to update\n- Fix all reported backend functionality issues, ensuring full compliance with design_spec.md and user_task_description\n- Do NOT modify frontend templates or unrelated files\n- Iteratively improve backend until Tester feedback file contains [APPROVED]\n\nImplementation Guidance:\n1. Carefully analyze each backend issue reported, reproducing test scenarios if needed\n2. Modify app.py to correct route implementations, data handling, and business logic\n3. Preserve consistent naming and structure from design_spec.md\n4. Maintain code readability and Flask best practices\n5. Use write_text_file to save updated app.py after each iteration\n\nCRITICAL REQUIREMENTS:\n- Do NOT introduce frontend or UI changes\n- Thoroughly address all backend concerns raised by Tester\n- Stop only when Tester feedback marks backend as [APPROVED]\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"tester_feedback.txt\", \"source\": \"Tester\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper_Fix\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper_Fix\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML/Jinja2 templating for Flask web applications.\n\nYour goal is to fix frontend templates based on Tester feedback until the frontend implementation is fully approved.\n\nTask Details:\n- Read tester_feedback.txt to identify frontend UI/UX issues and approval status\n- Read current templates/*.html files from CONTEXT to update\n- Fix all frontend issues including element IDs, navigation, page titles, layout, and interaction compliance with design_spec.md and user_task_description\n- Do NOT modify backend code or unrelated files\n- Iteratively improve frontend until Tester feedback file contains [APPROVED]\n\nImplementation Guidance:\n1. Verify all required element IDs are present and correctly named per specification\n2. Correct page titles and navigation links to match exact requirements\n3. Fix UI behavior issues, including buttons, forms, and dynamic content display\n4. Ensure template syntax is correct and consistent\n5. Use write_text_file to save updated templates/*.html files after each iteration\n\nCRITICAL REQUIREMENTS:\n- Do NOT introduce backend or business logic changes\n- Address all UI/UX concerns identified by Tester thoroughly\n- Stop only when Tester feedback indicates frontend is [APPROVED]\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"tester_feedback.txt\", \"source\": \"Tester\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper_Fix\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"Tester\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"SystemArchitect reviews tester_feedback.txt for coverage of all user requirements and accuracy of test procedures.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"tester_feedback.txt\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\"}\n            ]\n        },\n        {\n            \"source_agent\": \"Tester\",\n            \"reviewer_agent\": \"BackendDeveloper_Fix\",\n            \"review_criteria\": (\n                \"Tester ensures backend fixes address all functional issues, and confirms when backend functionality is fully approved.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"tester_feedback.txt\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"Tester\",\n            \"reviewer_agent\": \"FrontendDeveloper_Fix\",\n            \"review_criteria\": (\n                \"Tester ensures frontend fixes address all UI/UX issues, and confirms when frontend implementation is fully approved.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"tester_feedback.txt\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'MusicStreaming' Web Application

## 1. Objective
Develop a comprehensive web application named 'MusicStreaming' using Python, with data managed through local text files. The application enables users to search for songs, create and manage playlists, browse albums, explore artist profiles, filter by genres, and view song/artist statistics. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'MusicStreaming' application is Python.

## 3. Page Design

The 'MusicStreaming' web application will consist of the following ten pages:

### 1. Dashboard Page
- **Page Title**: Music Streaming Dashboard
- **Overview**: The main hub displaying featured songs, trending artists, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-songs** - Type: Div - Display of featured song recommendations.
  - **ID: browse-songs-button** - Type: Button - Button to navigate to song catalog page.
  - **ID: my-playlists-button** - Type: Button - Button to navigate to my playlists page.
  - **ID: trending-artists-button** - Type: Button - Button to navigate to trending artists page.

### 2. Song Catalog Page
- **Page Title**: Song Catalog
- **Overview**: A page displaying all available songs with search and filter capabilities.
- **Elements**:
  - **ID: catalog-page** - Type: Div - Container for the catalog page.
  - **ID: search-input** - Type: Input - Field to search songs by title, artist, or album.
  - **ID: genre-filter** - Type: Dropdown - Dropdown to filter by genre (Pop, Rock, Hip-Hop, Jazz, Classical, etc.).
  - **ID: songs-grid** - Type: Div - Grid displaying song cards with cover art, title, artist, and duration.
  - **ID: add-to-playlist-button-{song_id}** - Type: Button - Button to add song to playlist (each song card has this).

### 3. Song Details Page
- **Page Title**: Song Details
- **Overview**: A page displaying detailed information about a specific song.
- **Elements**:
  - **ID: song-details-page** - Type: Div - Container for the song details page.
  - **ID: song-title** - Type: H1 - Display song title.
  - **ID: artist-name** - Type: Div - Display artist name with link to artist profile.
  - **ID: album-name** - Type: Div - Display album name.
  - **ID: duration-display** - Type: Div - Display song duration.
  - **ID: play-button** - Type: Button - Button to play the song.

### 4. Playlist Page
- **Page Title**: My Playlists
- **Overview**: A page displaying all user-created playlists.
- **Elements**:
  - **ID: playlists-page** - Type: Div - Container for the playlists page.
  - **ID: playlists-grid** - Type: Div - Grid displaying playlist cards with cover, title, and song count.
  - **ID: create-playlist-button** - Type: Button - Button to create a new playlist.
  - **ID: view-playlist-button-{playlist_id}** - Type: Button - Button to view playlist details (each playlist has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 5. Playlist Details Page
- **Page Title**: Playlist Details
- **Overview**: A page displaying songs in a specific playlist with management options.
- **Elements**:
  - **ID: playlist-details-page** - Type: Div - Container for the playlist details page.
  - **ID: playlist-title** - Type: H1 - Display playlist title.
  - **ID: playlist-description** - Type: Div - Display playlist description.
  - **ID: songs-in-playlist** - Type: Table - Table displaying songs with title, artist, duration, and remove option.
  - **ID: remove-song-button-{song_id}** - Type: Button - Button to remove song from playlist (each song has this).
  - **ID: delete-playlist-button** - Type: Button - Button to delete the entire playlist.

### 6. Create Playlist Page
- **Page Title**: Create New Playlist
- **Overview**: A page for users to create a new playlist with title and description.
- **Elements**:
  - **ID: create-playlist-page** - Type: Div - Container for the create playlist page.
  - **ID: playlist-name-input** - Type: Input - Field to input playlist name.
  - **ID: playlist-description-input** - Type: Textarea - Field to input playlist description.
  - **ID: save-playlist-button** - Type: Button - Button to save and create the new playlist.
  - **ID: cancel-create-button** - Type: Button - Button to cancel and go back.

### 7. Album Browse Page
- **Page Title**: Albums
- **Overview**: A page displaying all available albums with browsing and filtering options.
- **Elements**:
  - **ID: albums-page** - Type: Div - Container for the albums page.
  - **ID: albums-grid** - Type: Div - Grid displaying album cards with cover art, title, artist, and year.
  - **ID: search-albums** - Type: Input - Field to search albums by title or artist.
  - **ID: sort-albums** - Type: Dropdown - Dropdown to sort albums (By Title, By Artist, By Year).
  - **ID: view-album-button-{album_id}** - Type: Button - Button to view album details (each album has this).

### 8. Album Details Page
- **Page Title**: Album Details
- **Overview**: A page displaying all songs in a specific album.
- **Elements**:
  - **ID: album-details-page** - Type: Div - Container for the album details page.
  - **ID: album-title** - Type: H1 - Display album title.
  - **ID: album-artist** - Type: Div - Display album artist.
  - **ID: album-year** - Type: Div - Display album release year.
  - **ID: album-songs-list** - Type: Div - List of songs in the album.
  - **ID: add-album-to-playlist-button** - Type: Button - Button to add all songs from album to playlist.

### 9. Artist Profile Page
- **Page Title**: Artist Profiles
- **Overview**: A page displaying all artists and their information.
- **Elements**:
  - **ID: artists-page** - Type: Div - Container for the artists page.
  - **ID: artists-grid** - Type: Div - Grid displaying artist cards with photo, name, and genre.
  - **ID: search-artists** - Type: Input - Field to search artists by name.
  - **ID: artists-sort** - Type: Dropdown - Dropdown to sort artists (By Name, By Genre).
  - **ID: view-artist-button-{artist_id}** - Type: Button - Button to view artist profile (each artist has this).

### 10. Genre Exploration Page
- **Page Title**: Genre Exploration
- **Overview**: A page for exploring music by genres with featured songs and artists per genre.
- **Elements**:
  - **ID: genres-page** - Type: Div - Container for the genres page.
  - **ID: genres-list** - Type: Div - List of all available genres.
  - **ID: select-genre** - Type: Dropdown - Dropdown to select and view a specific genre.
  - **ID: genre-songs** - Type: Div - Display songs for selected genre.
  - **ID: genre-artists** - Type: Div - Display artists for selected genre.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'MusicStreaming' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Songs Data
- **File Name**: `songs.txt`
- **Data Format**:
  ```
  song_id|title|artist_id|album_id|genre|duration|release_date|play_count
  ```
- **Example Data**:
  ```
  1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
  2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
  3|Shape of You|3|3|Pop|233|2017-01-06|4200000
  ```

### 2. Artists Data
- **File Name**: `artists.txt`
- **Data Format**:
  ```
  artist_id|name|genre|country|formation_year
  ```
- **Example Data**:
  ```
  1|Queen|Rock|United Kingdom|1970
  2|The Weeknd|Synth-Pop|Canada|2010
  3|Ed Sheeran|Pop|United Kingdom|2005
  ```

### 3. Albums Data
- **File Name**: `albums.txt`
- **Data Format**:
  ```
  album_id|title|artist_id|release_year|total_songs|genre
  ```
- **Example Data**:
  ```
  1|A Night at the Opera|1|1975|11|Rock
  2|After Hours|2|2019|14|Synth-Pop
  3|Divide|3|2017|12|Pop
  ```

### 4. Genres Data
- **File Name**: `genres.txt`
- **Data Format**:
  ```
  genre_id|genre_name|description
  ```
- **Example Data**:
  ```
  1|Rock|Guitar-driven music with strong beats and vocals
  2|Pop|Catchy mainstream music with broad appeal
  3|Hip-Hop|Rhythmic music with rap vocals and beat production
  ```

### 5. Playlists Data
- **File Name**: `playlists.txt`
- **Data Format**:
  ```
  playlist_id|title|description|creation_date|total_songs
  ```
- **Example Data**:
  ```
  1|Workout Mix|High energy songs for the gym|2025-01-15|25
  2|Chill Vibes|Relaxing music for study|2025-01-16|18
  3|Party Hits|Latest party tracks|2025-01-17|32
  ```

### 6. Playlist Songs Data
- **File Name**: `playlist_songs.txt`
- **Data Format**:
  ```
  playlist_song_id|playlist_id|song_id|added_date
  ```
- **Example Data**:
  ```
  1|1|2|2025-01-15
  2|1|3|2025-01-15
  3|2|1|2025-01-16
  ```
"""

CONTEXT = {
    "_metrics": {},  # Metrics tracking for all agents
    "user_task_description": [{
        "timestamp": time.time(),
        "agent_name": "user",
        "content": user_task
    }]
}

AGENT_PROFILES = {
    "SystemArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications.

Your goal is to create comprehensive design specifications that enable Backend and Frontend developers to implement the MusicStreaming application independently with clear deliverables.

Task Details:
- Read user_task_description from CONTEXT
- Create design_spec.md containing three main sections: Flask Routes, HTML Templates with element IDs, and Data Schemas
- Ensure all MusicStreaming pages and their UI elements with exact IDs are fully specified
- Include all data file formats with exact fields and example data as defined
- Do NOT include implementation details or presume backend/frontend internal code

**Section 1: Flask Routes Specification (For Backend Developer)**

Provide a detailed route table with the following columns:
- Route Path: URL pattern (e.g., /dashboard, /songs/<int:song_id>)
- Function Name: Flask function name (snake_case)
- HTTP Method(s): GET or POST as applicable
- Template File: Template filename to render
- Context Variables: All variables passed, including their data types and structures

Requirements:
- Include all pages as routes with explicit function names matching page purposes
- Root route '/' must redirect to dashboard page route
- Clearly define dynamic routes with parameters (e.g., song_id, playlist_id)
- Context variables must specify exact types (str, int, list, dict) and structures, including nested fields
- Ensure all routes are consistent with UI element navigation mappings

**Section 2: HTML Template Specifications (For Frontend Developer)**

For each page template, provide:
- Template File Path: templates/{template_name}.html
- Page Title: Exact <title> and <h1> content
- Required Element IDs: Complete list with exact IDs and element types (Div, Button, Input, Dropdown, Table, etc.)
- Context Variables: Detailed description of all variables available in the template with their structure
- Navigation Mappings: Button and link element IDs mapped to Flask route function names; include dynamic id patterns

Requirements:
- All element IDs must exactly match those specified in the user task document
- Context variables must correspond exactly to those in Section 1
- Navigation targets and function names must align with Section 1 routes
- Include notes on dynamic element ID patterns using Jinja2 syntax for rendering

**Section 3: Data File Schemas (For Backend Developer)**

For each data text file in the data directory, provide:
- Filename and exact relative path (e.g., data/songs.txt)
- File format: pipe-delimited (|)
- Exact field order with clear descriptive field names
- Field data types and brief description for each field
- 2-3 realistic example rows as per user task examples

Requirements:
- Ensure strict adherence to field order and delimiter format as backend depends on it
- Example data must reflect realistic sample content for validation
- Describe any relationships or foreign keys between files (e.g., artist_id references)

CRITICAL SUCCESS CRITERIA:
- Backend developer can implement app routes and data loading based solely on Section 1 and Section 3
- Frontend developer can create all templates with exact IDs and navigation using Section 2 only
- All element IDs, context variable names, and data schemas exactly match user requirements
- Use write_text_file tool to save design_spec.md without interactive code snippets or partial outputs
- Do NOT add assumptions beyond provided user task and data specifications

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],
    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications.

Your goal is to implement a complete Flask backend that fully realizes all routes, data management, and business logic as specified in the design specification.

Task Details:
- Read design_spec.md from CONTEXT, focusing on Flask route definitions, expected HTTP methods, context variables, and data file schemas
- Implement app.py with ALL Flask routes following exact route names, function names, and data handling requirements
- Load and save data from/to data/*.txt files using pipe-delimited formats as specified
- Do NOT read or modify frontend templates; do NOT assume unspecified features outside design_spec.md

Implementation Requirements:
1. **Flask Application Setup**
   - Initialize Flask app with appropriate configurations
   - Implement root '/' route that redirects to Dashboard page per specification

2. **Data Loading and Saving**
   - Parse data files from data directory using exact schema from design_spec.md
   - Use robust file reading with pipe-delimited parsing (e.g., line.strip().split('|'))
   - Map data fields precisely as defined for each entity (songs, artists, albums, genres, playlists, playlist_songs)
   - Implement data writing functions if necessary for playlist creation or update

3. **Route and Business Logic Implementation**
   - Implement all routes with exact function names and HTTP method handlers (GET, POST) defined in design_spec.md
   - Pass correct context variables to templates matching design_spec.md names and types
   - Handle form submissions and update data files accordingly (e.g., creating playlists, adding/removing songs)
   - Implement error handling for missing or malformed data gracefully

4. **Best Practices**
   - Use url_for for all redirects
   - Ensure data consistency across routes
   - Include "__main__" guard to run app in debug mode on port 5000

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save your completed app.py
- Follow design_spec.md content EXACTLY for routes, data schema, and logic
- Do NOT invent features or deviate from provided specification
- Do NOT output code in chat messages only—always save via write_text_file

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],
    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask applications.

Your goal is to implement complete frontend HTML templates that fulfill all page designs, contain the specified element IDs, and follow navigation flows exactly as described in the design specification.

Task Details:
- Read design_spec.md from CONTEXT, focusing on template specifications including element IDs, page titles, context variables, and navigation routes
- Implement all frontend templates (*.html) corresponding to each application page
- Ensure all static and dynamic element IDs are implemented exactly as specified, including Jinja2 syntax for dynamic IDs
- DO NOT read or modify backend code or logic; do NOT assume additional features outside design_spec.md

Implementation Requirements:
1. **Template Structure**
   - Use standard HTML5 with Jinja2 syntax for templating
   - Include correct <title> and <h1> tags with exact page titles from specification
   - Wrap page content using main container div with specified IDs

2. **Element IDs and Dynamics**
   - Implement ALL static IDs exactly as named
   - For dynamic elements (e.g., add-to-playlist-button-{song_id}), use proper Jinja2 templating:
     ```html
     id="add-to-playlist-button-{{ song.song_id }}"
     ```
   - Ensure dynamic IDs match naming patterns from specification exactly

3. **Navigation and Links**
   - Implement navigation buttons and links using url_for with exact route function names as provided
   - Static buttons:
     ```html
     <a href="{{ url_for('function_name') }}"><button id="element-id">Text</button></a>
     ```
   - Dynamic links with parameters:
     ```html
     <a href="{{ url_for('function_name', id=item.id) }}">
       <button id="button-id-{{ item.id }}">View</button>
     </a>
     ```

4. **Forms (for POST actions)**
   - Implement HTML forms for creating playlists, adding/removing songs, with method="POST" and correct action URLs
   - Use input elements with specified IDs and names

5. **Context Variables**
   - Access context variables as specified with correct field access (e.g., {{ song.title }}, {{ artist.name }})
   - Use loops and conditionals as needed to render lists and tables

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save all template files in templates/ directory
- ALL element IDs must be exact and case-sensitive as specified
- Page titles and navigation must match design_spec.md precisely
- Do NOT add extra templates or IDs beyond the specification
- Do NOT output code in chat messages only—always save via write_text_file

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],
    },

    "Tester": {
        "prompt": (
            """You are a Software Test Engineer specializing in functional and UI testing of Python-based web applications with Flask backend and HTML frontend.

Your goal is to perform comprehensive testing and validation of both backend and frontend implementations to verify that all user features work correctly, identifying issues and producing detailed feedback with approval status.

Task Details:
- Read app.py and templates/*.html from CONTEXT as current implementation artifacts
- Read design_spec.md and user_task_description to understand all required features and expected behaviors
- Test ALL user requirements for functionality and UI correctness across pages and features
- Write detailed tester_feedback.txt including issue descriptions and overall approval status with [APPROVED] or NEED_MODIFY
- Focus only on implemented features; do NOT propose new features

Testing Requirements:
1. **Functional Testing**:
   - Verify all Flask routes respond correctly as per design_spec.md
   - Test dynamic functionality such as search, filters, playlist creation, song playback buttons
   - Validate data display correctness against data schemas and user requirements
   - Confirm backend handles error cases gracefully

2. **UI Testing**:
   - Check presence and correctness of all required element IDs across pages
   - Validate page titles and navigation flows correspond exactly to specifications
   - Ensure buttons, forms, inputs function as expected
   - Confirm responsive behavior and consistent styling (where applicable)

3. **Feedback Format**:
   - Use clear sections for Backend Issues, Frontend Issues, and Summary
   - Provide exact file names and element IDs or routes where issues occur
   - End feedback file with either [APPROVED] if no issues, or NEED_MODIFY if fixes are needed

CRITICAL REQUIREMENTS:
- Use execute_python_code to run backend tests and simulate requests
- Use read_binary_file if visual/UI binary artifacts need analysis
- Use write_text_file to save tester_feedback.txt with detailed findings and status marker
- Do NOT modify any implementation files directly

Output: tester_feedback.txt"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['execute_python_code', 'read_binary_file', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'tester_feedback.txt'}],
    },

    "BackendDeveloper_Fix": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications.

Your goal is to fix backend code based on Tester feedback until the backend implementation is fully approved.

Task Details:
- Read tester_feedback.txt to identify backend issues and approval status
- Read current app.py from CONTEXT to update
- Fix all reported backend functionality issues, ensuring full compliance with design_spec.md and user_task_description
- Do NOT modify frontend templates or unrelated files
- Iteratively improve backend until Tester feedback file contains [APPROVED]

Implementation Guidance:
1. Carefully analyze each backend issue reported, reproducing test scenarios if needed
2. Modify app.py to correct route implementations, data handling, and business logic
3. Preserve consistent naming and structure from design_spec.md
4. Maintain code readability and Flask best practices
5. Use write_text_file to save updated app.py after each iteration

CRITICAL REQUIREMENTS:
- Do NOT introduce frontend or UI changes
- Thoroughly address all backend concerns raised by Tester
- Stop only when Tester feedback marks backend as [APPROVED]

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'tester_feedback.txt', 'source': 'Tester'}, {'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper_Fix'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],
    },

    "FrontendDeveloper_Fix": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML/Jinja2 templating for Flask web applications.

Your goal is to fix frontend templates based on Tester feedback until the frontend implementation is fully approved.

Task Details:
- Read tester_feedback.txt to identify frontend UI/UX issues and approval status
- Read current templates/*.html files from CONTEXT to update
- Fix all frontend issues including element IDs, navigation, page titles, layout, and interaction compliance with design_spec.md and user_task_description
- Do NOT modify backend code or unrelated files
- Iteratively improve frontend until Tester feedback file contains [APPROVED]

Implementation Guidance:
1. Verify all required element IDs are present and correctly named per specification
2. Correct page titles and navigation links to match exact requirements
3. Fix UI behavior issues, including buttons, forms, and dynamic content display
4. Ensure template syntax is correct and consistent
5. Use write_text_file to save updated templates/*.html files after each iteration

CRITICAL REQUIREMENTS:
- Do NOT introduce backend or business logic changes
- Address all UI/UX concerns identified by Tester thoroughly
- Stop only when Tester feedback indicates frontend is [APPROVED]

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'tester_feedback.txt', 'source': 'Tester'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper_Fix'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],
    }

}

REVIEW_PROFILES = {
    'SystemArchitect': [
        ("BackendDeveloper", """Check design_spec.md backend sections for completeness: all Flask routes with function names, parameters, HTTP methods; data schema definitions for text files with exact fields and formats.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
        ("FrontendDeveloper", """Check design_spec.md frontend sections for completeness: all HTML templates with exact element IDs, page layouts, reference to navigation flow and context variables.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'BackendDeveloper': [
        ("SystemArchitect", """Validate app.py implements all Flask routes correctly according to design_spec.md including route names, HTTP methods, required data handling, and that root route redirects to the Dashboard page.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("SystemArchitect", """Verify templates/*.html implement all page elements with correct IDs, context variable usage, navigation flows, and page titles matching design_spec.md.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'Tester': [
        ("SystemArchitect", """SystemArchitect reviews tester_feedback.txt for coverage of all user requirements and accuracy of test procedures.""", [{'type': 'text_file', 'name': 'tester_feedback.txt'}, {'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'user', 'name': 'user_task_description'}]),
        ("BackendDeveloper_Fix", """Tester ensures backend fixes address all functional issues, and confirms when backend functionality is fully approved.""", [{'type': 'text_file', 'name': 'tester_feedback.txt'}, {'type': 'text_file', 'name': 'app.py'}]),
        ("FrontendDeveloper_Fix", """Tester ensures frontend fixes address all UI/UX issues, and confirms when frontend implementation is fully approved.""", [{'type': 'text_file', 'name': 'tester_feedback.txt'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}




# ==================== Compound Chaos Controller Setup ====================
import random
from chaos.injectors import ChaosMode

# Compound Chaos: Per-task sampling
COMPOUND_CONFIG = {
    "agent_intensity": random.choice([0.2, 0.3, 0.4, 0.5, 0.6]),
    "prompt_method": random.choice(["WORD_SHUFFLE", "WORD_DELETION", "WORD_REPLACEMENT"]),
    "io_method": random.choice(["WORD_SHUFFLE", "WORD_DELETION", "WORD_REPLACEMENT"]),
    "prompt_probability": 0.2,
    "io_probability": 0.2
}

# ChaosMode mapping
MODE_MAP = {
    "WORD_SHUFFLE": ChaosMode.WORD_SHUFFLE,
    "WORD_DELETION": ChaosMode.WORD_DELETION,
    "WORD_REPLACEMENT": ChaosMode.WORD_REPLACEMENT,
}

chaos_controller = ChaosController(
    agent_chaos_enabled=True,
    stress_chaos_enabled=True,
    stress_chaos_mode=MODE_MAP[COMPOUND_CONFIG["prompt_method"]],
    io_chaos_enabled=True,
    io_chaos_mode=MODE_MAP[COMPOUND_CONFIG["io_method"]],
    target_agent_names=list(AGENT_PROFILES.keys())
)

# Agent chaos is sampled with intensity
chaos_controller.start_experiment(
    running_agents=list(AGENT_PROFILES.keys()),
    agent_profiles=AGENT_PROFILES,
    probability=COMPOUND_CONFIG["agent_intensity"]
)

# Prompt/IO separately sampled at 0.2 probability (reset)
all_agents = list(AGENT_PROFILES.keys())
chaos_controller.stress_chaos_targets = [a for a in all_agents if random.random() < COMPOUND_CONFIG["prompt_probability"]]
chaos_controller.io_chaos_targets = [a for a in all_agents if random.random() < COMPOUND_CONFIG["io_probability"]]

# Guarantee at least 1
if not chaos_controller.stress_chaos_targets:
    chaos_controller.stress_chaos_targets = [random.choice(all_agents)]
if not chaos_controller.io_chaos_targets:
    chaos_controller.io_chaos_targets = [random.choice(all_agents)]

# Save chaos configuration to file for debugging
from datetime import datetime
import json

chaos_config_data = {
    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "scenario": "compound_chaos",
    "compound_config": COMPOUND_CONFIG,
    "enabled_chaos_types": {
        "agent_chaos": chaos_controller.agent_chaos.enabled,
        "stress_chaos": chaos_controller.stress_chaos.enabled,
        "io_chaos": chaos_controller.io_chaos.enabled
    },
    "targets": {
        "agent_chaos_targets": chaos_controller.agent_chaos_targets,
        "stress_chaos_targets": chaos_controller.stress_chaos_targets,
        "io_chaos_targets": chaos_controller.io_chaos_targets
    },
    "registered_files": dict(chaos_controller.agent_file_registry)
}

with open("chaos_config.json", "w") as f:
    json.dump(chaos_config_data, f, indent=2)

print(f"Compound Chaos activated: Agent={COMPOUND_CONFIG['agent_intensity']}, Prompt={COMPOUND_CONFIG['prompt_method']}, IO={COMPOUND_CONFIG['io_method']}")
print(f"Chaos configuration saved to: chaos_config.json")
# ================================================================

# Orchestration Functions
async def design_specification_phase():
    # Create SystemArchitect agent
    SystemArchitect = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="SystemArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    # Execute SystemArchitect to create design_spec.md with full design spec sections
    await execute(SystemArchitect, "Create design_spec.md with Flask Routes, HTML Templates with element IDs, and Data Schemas for MusicStreaming app based on user_task_description")
# Phase1_End

# Phase2_Start
import asyncio

async def parallel_implementation_phase():
    # Create BackendDeveloper agent
    BackendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )
    # Create FrontendDeveloper agent
    FrontendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )

    # Execute both agents in parallel
    await asyncio.gather(
        execute(BackendDeveloper, "Implement app.py with all Flask routes and data logic according to design_spec.md"),
        execute(FrontendDeveloper, "Implement all HTML templates with specified element IDs and navigation as per design_spec.md")
    )
# Phase2_End

# Phase3_Start

async def testing_and_validation_phase():
    # Create agents
    Tester = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="Tester",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )
    BackendDeveloper_Fix = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloper_Fix",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )
    FrontendDeveloper_Fix = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDeveloper_Fix",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    MAX_ITERATIONS = 3
    for iteration in range(MAX_ITERATIONS):
        # Execute Tester to test current implementation and write tester_feedback.txt
        await execute(Tester, "Perform comprehensive functional and UI tests on app.py and templates/*.html; write tester_feedback.txt")

        # Read tester_feedback.txt to check approval status
        try:
            with open("tester_feedback.txt", "r") as f:
                feedback_content = f.read()
        except FileNotFoundError:
            # If no feedback file found, stop the loop
            break

        if "[APPROVED]" in feedback_content:
            # Check if backend and frontend are approved, then break the loop
            break

        # Execute BackendDeveloper_Fix to fix backend issues if any
        await execute(BackendDeveloper_Fix, f"Fix backend issues as per tester_feedback.txt\n{feedback_content}")

        # Execute FrontendDeveloper_Fix to fix frontend issues if any
        await execute(FrontendDeveloper_Fix, f"Fix frontend UI/UX issues as per tester_feedback.txt\n{feedback_content}")

        # After fixes, the loop will run Tester again to validate fixes

# Phase3_End

# Orchestrate_Start

async def orchestrate():
    """Execute the complete multi-agent workflow in steps."""
    import time
    import json
    from pathlib import Path
    from essential_modules import aggregate_task_metrics
    orchestrate_start_time = time.time()

    step1 = [
        design_specification_phase()
    ]
    step2 = [
        parallel_implementation_phase()
    ]
    step3 = [
        testing_and_validation_phase()
    ]

    await asyncio.gather(*step1)
    await asyncio.gather(*step2)
    await asyncio.gather(*step3)

    # Record task duration
    orchestrate_end_time = time.time()
    CONTEXT["_task_duration"] = orchestrate_end_time - orchestrate_start_time

    # Print chaos engineering report (if enabled)
    if 'chaos_controller' in globals():
        print("\n" + "="*80)
        print("Chaos Engineering Report")
        print("="*80)
        chaos_controller.print_report(context=CONTEXT)

    # Save metrics to JSON
    task_metrics = aggregate_task_metrics(CONTEXT)
    metrics_path = Path("metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(task_metrics, f, indent=2)
    print(f" Metrics saved to: {{metrics_path.resolve()}}")
# Orchestrate_End

if __name__ == "__main__":
    import sys
    import signal
    from datetime import datetime
    from pathlib import Path
    import json

    # Signal handler for graceful shutdown on timeout
    def save_metrics_on_signal(signum, frame):
        print(f"\n  Received signal {signum}, saving metrics before exit...")
        try:
            task_metrics = aggregate_task_metrics(CONTEXT)
            metrics_path = Path("metrics.json")
            with open(metrics_path, "w") as f:
                json.dump(task_metrics, f, indent=2)
            print(f"Metrics saved to: {metrics_path.resolve()}")
        except Exception as e:
            print(f"Error saving metrics: {e}")
        sys.exit(1)

    # Register signal handlers
    signal.signal(signal.SIGTERM, save_metrics_on_signal)
    signal.signal(signal.SIGINT, save_metrics_on_signal)

    # Open log file for real-time stdout/stderr capture
    log_file = open("execution_log.txt", "w", encoding="utf-8")

    # Write header
    log_file.write("=== Execution Log ===\n")
    log_file.write(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log_file.write("\n=== OUTPUT ===\n")
    log_file.flush()

    # Create a Tee class to write to both stdout and file
    class Tee:
        def __init__(self, *files):
            self.files = files
        def write(self, data):
            for f in self.files:
                f.write(data)
                f.flush()
        def flush(self):
            for f in self.files:
                f.flush()

    # Redirect stdout and stderr to both console and log file
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    sys.stdout = Tee(original_stdout, log_file)
    sys.stderr = Tee(original_stderr, log_file)

    try:
        # Run orchestration
        asyncio.run(orchestrate())
    finally:
        # Restore original stdout/stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr

        # Write summary
        log_file.write(f"\n\n=== Summary ===\n")
        log_file.write(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.close()
