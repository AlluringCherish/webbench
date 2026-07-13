import asyncio
import sys
import os
import time
import asyncio
from typing import List, Dict, Any
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import essential_modules
from essential_modules import build_resilient_agent, execute, aggregate_task_metrics
from chaos import ChaosController
# 20260713_204916_216755/main_20260713_204916_216755.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Analyze the 'MusicStreaming' requirements and produce a complete detailed design_spec.md covering all pages, routes, elements, and data handling.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"RequirementsAnalyst writes requirements_analysis.md extracting all detailed elements, pages, and user flows; then \"\n        \"WebArchitect reads requirements_analysis.md and writes design_spec.md specifying Flask routes, page titles, element IDs, \"\n        \"data contracts, and local file storage formats.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"RequirementsAnalyst\",\n            \"prompt\": \"\"\"You are a Requirements Analyst specializing in software requirements documentation for web applications.\n\nYour goal is to analyze user task descriptions and produce a comprehensive requirements_analysis.md document that details all pages, UI elements, data storage formats, and user interactions.\n\nTask Details:\n- Carefully read the user_task_description artifact for the entire MusicStreaming application requirements\n- Document all 10 pages with their titles and detailed UI elements including exact element IDs and types\n- Capture all user interaction flows, including navigation via buttons and starting page as Dashboard\n- Extract data storage formats from the requirements, listing all local text files and their field structures\n- Produce a clear, organized requirements_analysis.md text file capturing above details comprehensively\n\nRequirements:\n- Include page name, purpose, and elements with exact IDs and types\n- List navigation buttons and their target pages\n- Include data files names with exact field names and example data if available\n- Structure document for easy consumption by design and development teams\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to create requirements_analysis.md\n- Preserve all element IDs and data format details without modification\n- Focus only on information present in user_task_description provided\n- Document user navigation flow and dashboard starting point\n- Output only the requirements_analysis.md file as specified\n\nOutput: requirements_analysis.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"WebArchitect\",\n            \"prompt\": \"\"\"You are a Web Architect specializing in Flask web application architecture and design specification.\n\nYour goal is to transform requirements_analysis.md into a detailed design_spec.md that fully specifies the Flask routes, page titles, element IDs, navigation flow starting at Dashboard, and data handling contracts for local text files.\n\nTask Details:\n- Read user_task_description and requirements_analysis.md artifacts to understand full application scope\n- Define exact Flask routes for each of the 10 pages with route paths and function names\n- Specify page titles matching each page exactly\n- List all exact element IDs to appear on each page\n- Define navigation flows starting from Dashboard page with button mappings to routes\n- Specify data file names and exact pipe-delimited field sequences for local storage as per requirements\n- Produce a comprehensive design_spec.md text file that acts as a blueprint for implementation\n\nSpecifications:\n1. Flask Routes:\n   - Provide route path (e.g., /dashboard, /songs, /playlists/<int:id>)\n   - Provide function name (snake_case)\n   - HTTP methods if applicable (GET, POST)\n   - Template filename\n   - Context variables passed to templates with types\n\n2. Page Titles and Element IDs:\n   - Exact page titles\n   - List all element IDs per page as documented\n\n3. Navigation:\n   - Map buttons to route functions using url_for conventions\n   - Dashboard as root start page ('/')\n\n4. Data Handling:\n   - List all data files with exact field names and order\n   - Using pipe-delimited format without headers\n   - Include brief description of each data file's purpose\n\nCRITICAL SUCCESS CRITERIA:\n- design_spec.md fully supports independent backend and frontend implementation\n- All route names, element IDs, and data fields must be exact and consistent\n- Navigation flows must be clearly defined from Dashboard start point\n- Use write_text_file tool to output design_spec.md\n- Do not add features or pages beyond those specified in requirements\n- Ensure clarity and completeness for implementation engineers\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\", \"source\": \"RequirementsAnalyst\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"WebArchitect\",\n            \"review_criteria\": (\n                \"Verify that requirements_analysis.md fully captures all page designs, element IDs, buttons, data formats, and the dashboard \"\n                \"start requirement with no omissions or extraneous features.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"WebArchitect\",\n            \"reviewer_agent\": \"ImplementationEngineer\",\n            \"review_criteria\": (\n                \"Verify design_spec.md provides complete, unambiguous Flask routes, page titles, element IDs, and data file format contracts \"\n                \"necessary for implementation without gaps.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Implement the MusicStreaming web application as evaluator-compatible app.py and templates/*.html files per design_spec.md.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineer writes app_draft.py and templates_draft/*.html implementing all routes, pages, elements, and data handling as per design_spec.md; \"\n        \"IntegrationEngineer then integrates drafts into final app.py and templates/*.html ensuring runnable Flask app with all features, navigation, and data storage.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineer\",\n            \"prompt\": \"\"\"You are a Backend and Frontend Developer specializing in Flask web application development with Python.\n\nYour goal is to develop draft versions of the Flask backend and HTML templates implementing all routes, page logics, UI elements, and data handling strictly according to design specifications for a music streaming web application.\n\nTask Details:\n- Read full user_task_description and design_spec.md fully\n- Create app_draft.py implementing all Flask routes starting at Dashboard page\n- Implement page logic for song catalog, playlists, albums, artists, genres, and statistics\n- Render templates_draft/*.html with exact IDs and button elements as specified\n- Handle local text file data per specifications exactly\n- Produce drafts only; integration and final assembly done by IntegrationEngineer\n\nImplementation Requirements:\n1. **Flask Backend Draft (app_draft.py)**\n   - Set up Flask app with all routes defined in design_spec.md\n   - Each route should load and process data from local text files (data/*.txt) accurately\n   - Pass correct context variables to templates\n   - Do NOT implement final integration or deployment details\n\n2. **HTML Templates Draft (templates_draft/*.html)**\n   - Implement all templates with exact container IDs, buttons, inputs, dropdowns, and dynamic ID patterns\n   - Use correct Jinja2 templating syntax for dynamic content and loops\n   - Include buttons and navigation elements as specified\n   - Templates correspond exactly to pages defined in the specification\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_draft.py and all templates_draft/*.html files\n- Follow design_spec.md and user_task_description precisely to ensure feature completeness\n- Maintain exact casing and naming conventions for all UI element IDs\n- Restrict work to drafts; do not finalize integration or deployment code\n\nOutput: app_draft.py, templates_draft/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationEngineer\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in Flask web application final assembly.\n\nYour goal is to merge draft backend code and HTML templates into final production-ready app.py and templates/*.html files that form a fully runnable Flask application for music streaming, ensuring stable routes, correct navigation, UI element functionality, and proper local data access.\n\nTask Details:\n- Read full user_task_description, design_spec.md, and drafts app_draft.py and templates_draft/*.html\n- Merge and refactor app_draft.py into final app.py ensuring all routes and logic are stable and functional\n- Process templates_draft/*.html into final templates/*.html ensuring all button IDs, container IDs, and navigation elements adhere strictly to specification\n- Confirm all local data files (data/*.txt) are accessed correctly per specification within app.py\n- Resolve any draft file paths and template references appropriately for final deployment\n\nIntegration Requirements:\n1. **Backend Integration**\n   - Validate and refine all Flask routes from draft\n   - Ensure root route redirects to dashboard page\n   - Confirm data loading/parsing is correctly implemented per data schemas\n   - Clean up code for maintainability and error handling\n\n2. **Template Integration**\n   - Transfer draft templates to final templates directory\n   - Guarantee all specified element IDs and dynamic elements are preserved\n   - Ensure navigation between pages uses correct Flask url_for references\n   - Remove any placeholder references to draft files or paths\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save final app.py and templates/*.html files\n- Ensure final app.py is runnable as a Flask app with correct port and debug settings\n- Strictly follow design_spec.md for UI element IDs and routing consistency\n- Do not introduce new features beyond the scope of the drafts and specification\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\", \"source\": \"ImplementationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\", \"source\": \"ImplementationEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineer\",\n            \"reviewer_agent\": \"IntegrationEngineer\",\n            \"review_criteria\": (\n                \"Review app_draft.py and templates_draft/*.html against design_spec.md to confirm all required pages, routes, UI elements, button IDs, and data \"\n                \"file handling are correctly implemented.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"IntegrationEngineer\",\n            \"reviewer_agent\": \"ValidationEngineer\",\n            \"review_criteria\": (\n                \"Verify that the final app.py and templates/*.html form a runnable Flask application with all required routes and UI element IDs functioning \"\n                \"and adhering to the design_spec.md.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Validate and correct the final app.py and templates/*.html to ensure a fully functional and requirement-compliant MusicStreaming web app.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"ValidationEngineer tests and validates app.py with templates/*.html, writing validation_report.md identifying issues; \"\n        \"SequentialFixer applies corrections per validation_report.md and rewrites final app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidationEngineer\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in comprehensive validation of Flask web applications using Python.\n\nYour goal is to perform thorough validation testing to ensure the final app.py and templates/*.html fully conform to functional requirements and design specifications for a MusicStreaming web app, producing a detailed validation_report.md.\n\nTask Details:\n- Read user_task_description (overall requirements)\n- Read design_spec.md (for detailed design specs)\n- Read app.py and templates/*.html (final implemented code)\n- Create validation_report.md documenting all detected issues\n\nValidation Requirements:\n1. **Python Code Validation:**\n   - Use validate_python_file tool to check app.py for syntax and runtime errors\n   - Use execute_python_code tool to run or test critical functions as needed\n\n2. **Functional Testing:**\n   - Verify all Flask routes behave as specified in design_spec.md\n   - Check root route redirects to dashboard page\n   - Confirm form handling, GET/POST methods operate correctly\n\n3. **UI Validation:**\n   - Inspect templates/*.html to ensure presence and correctness of all specified element IDs\n   - Verify page titles match specifications\n   - Confirm navigation buttons/links work and IDs correspond accurately\n   - Check dynamic element IDs use correct patterns with variable substitutions\n\n4. **Data Interaction:**\n   - Confirm data files are read/updated in app.py according to specified formats and field orders\n   - Validate data-driven UI components show expected content references\n\n5. **Reporting:**\n   - Document each issue with clear description, affected artifact, and suggested correction in validation_report.md\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools appropriately for validation\n- Use write_text_file tool to output detailed validation_report.md\n- Report all issues aligned to design_spec.md and user requirements\n- Focus on correctness, completeness, and conformity without adding features\n\nOutput: validation_report.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"SequentialFixer\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in iterative refinement and correction of Flask web applications.\n\nYour goal is to apply all required fixes identified in validation_report.md to the existing app.py and templates/*.html so that the final outputs fully comply with design_spec.md and user requirements for the MusicStreaming web app.\n\nTask Details:\n- Read user_task_description (overall requirements)\n- Read design_spec.md (detailed design spec)\n- Read current app.py and templates/*.html (existing implementation)\n- Read validation_report.md (detailed validation feedback with issues and correction instructions)\n- Produce corrected app.py and templates/*.html files reflecting all fixes\n\nFix Implementation Requirements:\n1. **Address all reported syntax and runtime errors in app.py**\n2. **Correct all mismatches or missing Flask routes, ensuring behavior matches design_spec.md**\n3. **Implement all UI fixes in templates to ensure element IDs, page titles, dynamic IDs, and navigation match specifications**\n4. **Fix all data loading and saving logic to fully conform to data schema formats and interaction patterns**\n5. **Preserve coding best practices and project structure**\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save corrected app.py and all templates\n- Do not add functionality beyond what is required to fix reported issues\n- Fully resolve all validation_report.md points to ensure complete compliance\n- Focus on functional correctness, data integrity, and UI compliance strictly as per design_spec.md\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\", \"source\": \"ValidationEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidationEngineer\",\n            \"reviewer_agent\": \"SequentialFixer\",\n            \"review_criteria\": (\n                \"Ensure validation_report.md contains actionable, detailed findings aligned to design_spec.md covering all pages, routes, UI element IDs, and data file usage.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SequentialFixer\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": (\n                \"Verify the final app.py and templates/*.html fully resolve all validation issues and strictly implement the user requirements from validation_report.md.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "RequirementsAnalyst": {
        "prompt": (
            """You are a Requirements Analyst specializing in software requirements documentation for web applications.

Your goal is to analyze user task descriptions and produce a comprehensive requirements_analysis.md document that details all pages, UI elements, data storage formats, and user interactions.

Task Details:
- Carefully read the user_task_description artifact for the entire MusicStreaming application requirements
- Document all 10 pages with their titles and detailed UI elements including exact element IDs and types
- Capture all user interaction flows, including navigation via buttons and starting page as Dashboard
- Extract data storage formats from the requirements, listing all local text files and their field structures
- Produce a clear, organized requirements_analysis.md text file capturing above details comprehensively

Requirements:
- Include page name, purpose, and elements with exact IDs and types
- List navigation buttons and their target pages
- Include data files names with exact field names and example data if available
- Structure document for easy consumption by design and development teams

CRITICAL REQUIREMENTS:
- Use write_text_file tool to create requirements_analysis.md
- Preserve all element IDs and data format details without modification
- Focus only on information present in user_task_description provided
- Document user navigation flow and dashboard starting point
- Output only the requirements_analysis.md file as specified

Output: requirements_analysis.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md'}],

    },

    "WebArchitect": {
        "prompt": (
            """You are a Web Architect specializing in Flask web application architecture and design specification.

Your goal is to transform requirements_analysis.md into a detailed design_spec.md that fully specifies the Flask routes, page titles, element IDs, navigation flow starting at Dashboard, and data handling contracts for local text files.

Task Details:
- Read user_task_description and requirements_analysis.md artifacts to understand full application scope
- Define exact Flask routes for each of the 10 pages with route paths and function names
- Specify page titles matching each page exactly
- List all exact element IDs to appear on each page
- Define navigation flows starting from Dashboard page with button mappings to routes
- Specify data file names and exact pipe-delimited field sequences for local storage as per requirements
- Produce a comprehensive design_spec.md text file that acts as a blueprint for implementation

Specifications:
1. Flask Routes:
   - Provide route path (e.g., /dashboard, /songs, /playlists/<int:id>)
   - Provide function name (snake_case)
   - HTTP methods if applicable (GET, POST)
   - Template filename
   - Context variables passed to templates with types

2. Page Titles and Element IDs:
   - Exact page titles
   - List all element IDs per page as documented

3. Navigation:
   - Map buttons to route functions using url_for conventions
   - Dashboard as root start page ('/')

4. Data Handling:
   - List all data files with exact field names and order
   - Using pipe-delimited format without headers
   - Include brief description of each data file's purpose

CRITICAL SUCCESS CRITERIA:
- design_spec.md fully supports independent backend and frontend implementation
- All route names, element IDs, and data fields must be exact and consistent
- Navigation flows must be clearly defined from Dashboard start point
- Use write_text_file tool to output design_spec.md
- Do not add features or pages beyond those specified in requirements
- Ensure clarity and completeness for implementation engineers

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'requirements_analysis.md', 'source': 'RequirementsAnalyst'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineer": {
        "prompt": (
            """You are a Backend and Frontend Developer specializing in Flask web application development with Python.

Your goal is to develop draft versions of the Flask backend and HTML templates implementing all routes, page logics, UI elements, and data handling strictly according to design specifications for a music streaming web application.

Task Details:
- Read full user_task_description and design_spec.md fully
- Create app_draft.py implementing all Flask routes starting at Dashboard page
- Implement page logic for song catalog, playlists, albums, artists, genres, and statistics
- Render templates_draft/*.html with exact IDs and button elements as specified
- Handle local text file data per specifications exactly
- Produce drafts only; integration and final assembly done by IntegrationEngineer

Implementation Requirements:
1. **Flask Backend Draft (app_draft.py)**
   - Set up Flask app with all routes defined in design_spec.md
   - Each route should load and process data from local text files (data/*.txt) accurately
   - Pass correct context variables to templates
   - Do NOT implement final integration or deployment details

2. **HTML Templates Draft (templates_draft/*.html)**
   - Implement all templates with exact container IDs, buttons, inputs, dropdowns, and dynamic ID patterns
   - Use correct Jinja2 templating syntax for dynamic content and loops
   - Include buttons and navigation elements as specified
   - Templates correspond exactly to pages defined in the specification

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_draft.py and all templates_draft/*.html files
- Follow design_spec.md and user_task_description precisely to ensure feature completeness
- Maintain exact casing and naming conventions for all UI element IDs
- Restrict work to drafts; do not finalize integration or deployment code

Output: app_draft.py, templates_draft/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}],

    },

    "IntegrationEngineer": {
        "prompt": (
            """You are a Software Integration Engineer specializing in Flask web application final assembly.

Your goal is to merge draft backend code and HTML templates into final production-ready app.py and templates/*.html files that form a fully runnable Flask application for music streaming, ensuring stable routes, correct navigation, UI element functionality, and proper local data access.

Task Details:
- Read full user_task_description, design_spec.md, and drafts app_draft.py and templates_draft/*.html
- Merge and refactor app_draft.py into final app.py ensuring all routes and logic are stable and functional
- Process templates_draft/*.html into final templates/*.html ensuring all button IDs, container IDs, and navigation elements adhere strictly to specification
- Confirm all local data files (data/*.txt) are accessed correctly per specification within app.py
- Resolve any draft file paths and template references appropriately for final deployment

Integration Requirements:
1. **Backend Integration**
   - Validate and refine all Flask routes from draft
   - Ensure root route redirects to dashboard page
   - Confirm data loading/parsing is correctly implemented per data schemas
   - Clean up code for maintainability and error handling

2. **Template Integration**
   - Transfer draft templates to final templates directory
   - Guarantee all specified element IDs and dynamic elements are preserved
   - Ensure navigation between pages uses correct Flask url_for references
   - Remove any placeholder references to draft files or paths

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final app.py and templates/*.html files
- Ensure final app.py is runnable as a Flask app with correct port and debug settings
- Strictly follow design_spec.md for UI element IDs and routing consistency
- Do not introduce new features beyond the scope of the drafts and specification

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app_draft.py', 'source': 'ImplementationEngineer'}, {'type': 'text_file', 'name': 'templates_draft/*.html', 'source': 'ImplementationEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "ValidationEngineer": {
        "prompt": (
            """You are a Software Test Engineer specializing in comprehensive validation of Flask web applications using Python.

Your goal is to perform thorough validation testing to ensure the final app.py and templates/*.html fully conform to functional requirements and design specifications for a MusicStreaming web app, producing a detailed validation_report.md.

Task Details:
- Read user_task_description (overall requirements)
- Read design_spec.md (for detailed design specs)
- Read app.py and templates/*.html (final implemented code)
- Create validation_report.md documenting all detected issues

Validation Requirements:
1. **Python Code Validation:**
   - Use validate_python_file tool to check app.py for syntax and runtime errors
   - Use execute_python_code tool to run or test critical functions as needed

2. **Functional Testing:**
   - Verify all Flask routes behave as specified in design_spec.md
   - Check root route redirects to dashboard page
   - Confirm form handling, GET/POST methods operate correctly

3. **UI Validation:**
   - Inspect templates/*.html to ensure presence and correctness of all specified element IDs
   - Verify page titles match specifications
   - Confirm navigation buttons/links work and IDs correspond accurately
   - Check dynamic element IDs use correct patterns with variable substitutions

4. **Data Interaction:**
   - Confirm data files are read/updated in app.py according to specified formats and field orders
   - Validate data-driven UI components show expected content references

5. **Reporting:**
   - Document each issue with clear description, affected artifact, and suggested correction in validation_report.md

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools appropriately for validation
- Use write_text_file tool to output detailed validation_report.md
- Report all issues aligned to design_spec.md and user requirements
- Focus on correctness, completeness, and conformity without adding features

Output: validation_report.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_report.md'}],

    },

    "SequentialFixer": {
        "prompt": (
            """You are a Software Developer specializing in iterative refinement and correction of Flask web applications.

Your goal is to apply all required fixes identified in validation_report.md to the existing app.py and templates/*.html so that the final outputs fully comply with design_spec.md and user requirements for the MusicStreaming web app.

Task Details:
- Read user_task_description (overall requirements)
- Read design_spec.md (detailed design spec)
- Read current app.py and templates/*.html (existing implementation)
- Read validation_report.md (detailed validation feedback with issues and correction instructions)
- Produce corrected app.py and templates/*.html files reflecting all fixes

Fix Implementation Requirements:
1. **Address all reported syntax and runtime errors in app.py**
2. **Correct all mismatches or missing Flask routes, ensuring behavior matches design_spec.md**
3. **Implement all UI fixes in templates to ensure element IDs, page titles, dynamic IDs, and navigation match specifications**
4. **Fix all data loading and saving logic to fully conform to data schema formats and interaction patterns**
5. **Preserve coding best practices and project structure**

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save corrected app.py and all templates
- Do not add functionality beyond what is required to fix reported issues
- Fully resolve all validation_report.md points to ensure complete compliance
- Focus on functional correctness, data integrity, and UI compliance strictly as per design_spec.md

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'validation_report.md', 'source': 'ValidationEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'RequirementsAnalyst': [
        ("WebArchitect", """Verify that requirements_analysis.md fully captures all page designs, element IDs, buttons, data formats, and the dashboard "
                "start requirement with no omissions or extraneous features.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'requirements_analysis.md'}])
    ],

    'WebArchitect': [
        ("ImplementationEngineer", """Verify design_spec.md provides complete, unambiguous Flask routes, page titles, element IDs, and data file format contracts "
                "necessary for implementation without gaps.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationEngineer': [
        ("IntegrationEngineer", """Review app_draft.py and templates_draft/*.html against design_spec.md to confirm all required pages, routes, UI elements, button IDs, and data "
                "file handling are correctly implemented.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}])
    ],

    'IntegrationEngineer': [
        ("ValidationEngineer", """Verify that the final app.py and templates/*.html form a runnable Flask application with all required routes and UI element IDs functioning "
                "and adhering to the design_spec.md.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'ValidationEngineer': [
        ("SequentialFixer", """Ensure validation_report.md contains actionable, detailed findings aligned to design_spec.md covering all pages, routes, UI element IDs, and data file usage.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_report.md'}])
    ],

    'SequentialFixer': [
        ("RequirementsAnalyst", """Verify the final app.py and templates/*.html fully resolve all validation issues and strictly implement the user requirements from validation_report.md.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}





# ==================== Chaos Controller Setup ====================
import random
import os
from chaos.injectors import ChaosMode

COMPOUND_CONFIG = {
    "agent_intensity": random.choice([0.2, 0.3, 0.4, 0.5, 0.6]),
    "stress_method": random.choice(['WORD_SHUFFLE', 'WORD_DELETION', 'WORD_REPLACEMENT']),
    "io_method": random.choice(['WORD_SHUFFLE', 'WORD_DELETION', 'WORD_REPLACEMENT']),
    "stress_probability": 0.2,
    "io_probability": 0.2
}
if os.environ.get("CHAOS_AGENT_PROBABILITY_OVERRIDE"):
    COMPOUND_CONFIG["agent_intensity"] = float(os.environ["CHAOS_AGENT_PROBABILITY_OVERRIDE"])
if os.environ.get("CHAOS_STRESS_PROBABILITY_OVERRIDE"):
    COMPOUND_CONFIG["stress_probability"] = float(os.environ["CHAOS_STRESS_PROBABILITY_OVERRIDE"])
if os.environ.get("CHAOS_IO_PROBABILITY_OVERRIDE"):
    COMPOUND_CONFIG["io_probability"] = float(os.environ["CHAOS_IO_PROBABILITY_OVERRIDE"])

MODE_MAP = {
    "WORD_SHUFFLE": ChaosMode.WORD_SHUFFLE,
    "WORD_DELETION": ChaosMode.WORD_DELETION,
    "WORD_REPLACEMENT": ChaosMode.WORD_REPLACEMENT,
}

chaos_target_agent_names = [
    name.strip()
    for name in os.environ.get("CHAOS_TARGET_AGENT_NAMES", "").split(",")
    if name.strip()
] or list(AGENT_PROFILES.keys())

chaos_controller = ChaosController(
    agent_chaos_enabled=True,
    stress_chaos_enabled=True,
    stress_chaos_mode=MODE_MAP[COMPOUND_CONFIG["stress_method"]],
    io_chaos_enabled=True,
    io_chaos_mode=MODE_MAP[COMPOUND_CONFIG["io_method"]],
    target_agent_names=chaos_target_agent_names
)

# V2 probabilities: agent chaos uses random 0.2-0.6; stress/io use 0.2.
# V1 methods: one word-based Stress mode and one word-based IO mode per task.
chaos_controller.start_experiment(
    running_agents=list(AGENT_PROFILES.keys()),
    agent_profiles=AGENT_PROFILES,
    probability=COMPOUND_CONFIG["agent_intensity"]
)

all_agents = list(AGENT_PROFILES.keys())
chaos_controller.set_targets_by_probability(
    "stress",
    running_agents=all_agents,
    agent_profiles=AGENT_PROFILES,
    probability=COMPOUND_CONFIG["stress_probability"]
)
chaos_controller.set_targets_by_probability(
    "io",
    running_agents=all_agents,
    agent_profiles=AGENT_PROFILES,
    probability=COMPOUND_CONFIG["io_probability"]
)

# Save chaos configuration to file for debugging
from datetime import datetime
import json

chaos_config_data = {
    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "scenario": "compound_chaos",
    "probability": COMPOUND_CONFIG["agent_intensity"],
    "target_agent_names": chaos_target_agent_names,
    "probabilities": {
        "agent_chaos": COMPOUND_CONFIG["agent_intensity"],
        "stress_chaos": COMPOUND_CONFIG["stress_probability"],
        "io_chaos": COMPOUND_CONFIG["io_probability"]
    },
    "compound_config": COMPOUND_CONFIG,
    "enabled_chaos_types": {
        "agent_chaos": chaos_controller.agent_chaos.enabled,
        "stress_chaos": chaos_controller.stress_chaos.enabled,
        "io_chaos": chaos_controller.io_chaos.enabled
    },
    "logical_targets": {
        "agent_chaos_targets": chaos_controller.agent_chaos_logical_targets,
        "stress_chaos_targets": chaos_controller.stress_chaos_logical_targets,
        "io_chaos_targets": chaos_controller.io_chaos_logical_targets
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

print("[*] Chaos scenario 'compound_chaos' activated with compound probabilities")
print(f"[*] Compound config: {COMPOUND_CONFIG}")
print(f"[*] Chaos configuration saved to: chaos_config.json")
# ================================================================

# Orchestration Functions
async def design_specification_phase():
    # Create RequirementsAnalyst agent
    RequirementsAnalyst = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="RequirementsAnalyst",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )

    # Create WebArchitect agent
    WebArchitect = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="WebArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=320,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution: RequirementsAnalyst then WebArchitect

    # Step 1: RequirementsAnalyst analyzes user_task_description and outputs requirements_analysis.md
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description for MusicStreaming app and write comprehensive requirements_analysis.md including pages, UI elements with exact IDs, navigation flows starting at Dashboard, and data storage formats.")

    # Step 2: Read requirements_analysis.md content to pass to WebArchitect
    requirements_content = ""
    try:
        requirements_content = open("requirements_analysis.md").read()
    except Exception:
        requirements_content = ""

    # Step 3: WebArchitect reads user_task_description and requirements_analysis.md and writes design_spec.md
    await execute(WebArchitect,
                  f"Read user_task_description and requirements_analysis.md to create detailed design_spec.md specifying Flask routes, page titles, element IDs, navigation from Dashboard, and pipe-delimited data file contracts.\n\n"
                  f"=== requirements_analysis.md ===\n{requirements_content}\n")
# Phase1_End

# Phase2_Start
import asyncio

async def implementation_phase():
    # Create agents
    ImplementationEngineer = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    IntegrationEngineer = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="IntegrationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution for Sequential Flow pattern
    # 1. ImplementationEngineer produces drafts: app_draft.py and templates_draft/*.html
    await execute(ImplementationEngineer,
                  "Develop draft app_draft.py implementing all Flask routes and logic from design_spec.md for MusicStreaming app. "
                  "Create draft HTML templates in templates_draft/ with exact IDs and elements per design_spec.md.")

    # Read draft outputs for IntegrationEngineer
    app_draft_code, templates_draft_content = "", ""
    try:
        app_draft_code = open("app_draft.py").read()
    except Exception:
        pass
    try:
        import glob
        draft_files = glob.glob("templates_draft/*.html")
        templates_draft_content = ""
        for fpath in draft_files:
            try:
                templates_draft_content += f"=== {fpath} ===\n" + open(fpath).read() + "\n\n"
            except Exception:
                pass
    except Exception:
        pass

    # 2. IntegrationEngineer merges drafts and refines into final app.py and templates/*.html
    await execute(IntegrationEngineer,
                  f"Integrate and finalize app_draft.py and templates_draft/*.html into runnable app.py and templates/*.html as per design_spec.md. "
                  f"Ensure stable routes, proper navigation, and correct local data access.\n\n"
                  f"=== app_draft.py ===\n"
                  f"{app_draft_code}\n\n"
                  f"=== templates_draft/*.html ===\n"
                  f"{templates_draft_content}")
# Phase2_End

# Phase3_Start

async def verification_phase():
    # Create agents
    ValidationEngineer = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ValidationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )
    SequentialFixer = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="SequentialFixer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=480,
        failure_threshold=2,
        recovery_time=60
    )

    # Sequential execution
    await execute(ValidationEngineer,
                  "Validate app.py and all templates/*.html thoroughly using validate_python_file and execute_python_code tools. "
                  "Verify routes, UI elements, data interaction against design_spec.md and user_task_description. "
                  "Output detailed validation_report.md with all issues.")

    # Read validation_report.md content to inject into SequentialFixer
    validation_report_content = ""
    try:
        with open("validation_report.md", "r", encoding="utf-8") as f:
            validation_report_content = f.read()
    except Exception:
        pass

    # Correction by SequentialFixer based on validation_report.md
    await execute(SequentialFixer,
                  f"Apply all fixes listed in validation_report.md to app.py and templates/*.html to fully comply with design_spec.md and user requirements. "
                  "Preserve existing functionality and project structure. Output corrected app.py and templates/*.html.\n"
                  f"=== validation_report.md ===\n{validation_report_content}")
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
        implementation_phase()
    ]
    step3 = [
        verification_phase()
    ]

    await asyncio.gather(*step1)
    await asyncio.gather(*step2)
    await asyncio.gather(*step3)

    # Record task duration
    orchestrate_end_time = time.time()
    CONTEXT["_task_duration"] = orchestrate_end_time - orchestrate_start_time

    # Print chaos engineering report (if enabled)
    cc = None
    if 'chaos_controller' in globals():
        print("\n" + "="*80)
        print("Chaos Engineering Report")
        print("="*80)
        chaos_controller.print_report(context=CONTEXT)
        cc = chaos_controller

    # Print chaos engineering report
    print("\n" + "="*80)
    print("Chaos Engineering Report")
    print("="*80)
    chaos_controller.print_report(context=CONTEXT)


    # Save metrics to JSON (with resilience_metrics if chaos enabled)
    task_metrics = aggregate_task_metrics(CONTEXT, chaos_controller=cc)
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
        print(f"\n  Received signal {signum}, saving metrics and reports before exit...")

        # Save chaos reports if chaos_controller exists (chaos scenarios only)
        try:
            if 'chaos_controller' in globals():
                print("Generating chaos report on timeout...")
                chaos_controller.print_report(context=CONTEXT, save_to_file=True)
                print("Chaos reports saved successfully")
        except Exception as e:
            print(f"  Error saving chaos report: {e}")
            import traceback
            traceback.print_exc()

        # Save metrics (independent of chaos report success/failure)
        try:
            # Pass chaos_controller if available for resilience_metrics
            cc = chaos_controller if 'chaos_controller' in globals() else None
            task_metrics = aggregate_task_metrics(CONTEXT, chaos_controller=cc)
            metrics_path = Path("metrics.json")
            with open(metrics_path, "w") as f:
                json.dump(task_metrics, f, indent=2)
            print(f"Metrics saved to: {metrics_path.resolve()}")
        except Exception as e:
            print(f"Error saving metrics: {e}")
            import traceback
            traceback.print_exc()

        sys.exit(1)

    # Register signal handlers
    signal.signal(signal.SIGTERM, save_metrics_on_signal)
    signal.signal(signal.SIGINT, save_metrics_on_signal)

    # Open log file for real-time stdout/stderr capture
    log_file = open("execution_log.txt", "w", encoding="utf-8")
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

        log_file.close()
