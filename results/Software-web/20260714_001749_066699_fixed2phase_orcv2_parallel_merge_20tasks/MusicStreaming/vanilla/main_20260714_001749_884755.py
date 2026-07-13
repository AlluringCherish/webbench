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
# 20260714_001749_884755/main_20260714_001749_884755.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create complementary backend and frontend design specifications capturing all required Flask routes, data interaction patterns, and HTML template structures with element IDs, then merge into a single consistent design_spec.md document.\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDesignArchitect designs detailed Flask route endpoints, data schemas, \"\n        \"and file interaction patterns producing backend_design.md. FrontendDesignArchitect \"\n        \"defines HTML templates, element IDs, UI components, navigation, and filtering mechanisms \"\n        \"producing frontend_design.md. DesignMerger consolidates these two documents into a \"\n        \"unified design_spec.md ensuring consistency and completeness without adding new features.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Python Flask backend development with local text file database interaction.\n\nYour goal is to specify the backend design including Flask routes, data access logic, and data schemas reflecting the MusicStreaming application requirements.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Independently create backend_design.md specifying all Flask endpoints, request methods, and data interaction patterns\n- Utilize the specified local text data files: songs.txt, artists.txt, albums.txt, genres.txt, playlists.txt, playlist_songs.txt\n- Exclude any dependency or assumptions on frontend_design.md\n\n**Section 1: Flask Route Specifications**\n- Define each route path, HTTP method(s), expected request parameters, and response data structure\n- Include routes for searching songs, managing playlists, browsing albums, exploring artists, filtering genres, and statistics pages\n- Specify JSON structures or context variables passed to templates where applicable\n\n**Section 2: Data File Schemas and Access**\n- Describe the exact parsing logic and schema for each local text file based on column definitions and delimiters\n- Detail how data is read, filtered, and aggregated from these files in the backend\n- Cover data models representing songs, artists, albums, genres, playlists, and playlist songs with example data rows\n\n**Section 3: API and Integration Details**\n- Define APIs for add/remove songs in playlists, play counts updates, and navigation handling\n- Describe any necessary query parameters for filtering and sorting on the backend\n\nCRITICAL SUCCESS CRITERIA:\n- BackendDeveloper can implement functional Flask routes and data access from backend_design.md alone\n- Data file schemas are accurate and directly correspond to user_task_description examples\n- Use write_text_file tool to output backend_design.md\n\nOutput: backend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ],\n        },\n        {\n            \"agent_name\": \"FrontendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in HTML and Jinja2 template design for Python web applications.\n\nYour goal is to specify frontend HTML templates with detailed element IDs and UI structure for all MusicStreaming web pages as described.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Independently create frontend_design.md detailing all required HTML template files and their element IDs\n- Cover each of the ten specified pages: Dashboard, Song Catalog, Song Details, Playlists, Playlist Details, Create Playlist, Album Browse, Album Details, Artist Profiles, and Genre Exploration\n- Specify UI components such as buttons, input fields, dropdowns, grids, tables, and navigation widgets\n- Do not depend on backend_design.md\n\n**Section 1: HTML Templates Overview**\n- For each page, specify template filenames and page titles\n- List element IDs with their HTML element types and roles\n- Define navigation button actions and filtering UI elements\n\n**Section 2: UI Components and Interactions**\n- Detail how search inputs, dropdown filters, and buttons interact within templates\n- Include dynamic elements needing context variables and loops (e.g., song cards, playlist grids)\n- Provide exact ID conventions for controls like add-to-playlist and remove-song buttons with placeholders\n\nCRITICAL SUCCESS CRITERIA:\n- FrontendDeveloper can implement all templates and UI elements from frontend_design.md alone\n- Element IDs and page structures comply strictly with user_task_description\n- Use write_text_file tool to output frontend_design.md\n\nOutput: frontend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ],\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a System Architect specializing in integrating backend and frontend design specifications for Flask web applications.\n\nYour goal is to merge backend_design.md and frontend_design.md into a unified, consistent design_spec.md without introducing new features beyond the user task.\n\nTask Details:\n- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT\n- Verify completeness and resolve any inconsistencies between backend routes, data schemas, and frontend template elements\n- Ensure naming conventions, element IDs, and route parameters align perfectly across designs\n- Consolidate all information into one canonical design_spec.md document\n\n**Section 1: Consistency Verification**\n- Cross-check that every frontend element requiring backend data has matching route/context variable definitions\n- Confirm all backend routes are supported by corresponding frontend templates or UI components\n\n**Section 2: Unified Design Specification**\n- Integrate backend routes, data schemas, and frontend templates with element IDs into coherent sections\n- Maintain clear separation with consistent formatting consistent for developer consumption\n\nCRITICAL SUCCESS CRITERIA:\n- Resulting design_spec.md enables developers to implement both backend Flask routes and frontend HTML templates with no contradictions\n- The artifact references ONLY declared input artifacts; no extra requirements added\n- Use write_text_file tool to output design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\", \"source\": \"BackendDesignArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\", \"source\": \"FrontendDesignArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ],\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify backend design completeness and correctness per user task and local file data handling.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"backend_design.md\"}]\n        },\n        {\n            \"source_agent\": \"FrontendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify frontend design completeness and correctness of HTML element IDs and page structures.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"frontend_design.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Implement the backend app.py and frontend templates/*.html based on design_spec.md and merge into a complete functional Python Flask app with HTML templates.\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements Flask app.py with routes, data loading, and processing per design_spec.md. \"\n        \"FrontendDeveloper implements all HTML templates with specified element IDs and UI features concurrently. \"\n        \"IntegrationMerger reconciles app.py and templates/*.html ensuring interface consistency and writes the final \"\n        \"app.py and all templates.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Python backend developer specializing in Flask web applications.\n\nYour goal is to implement a complete Flask backend application as specified in design_spec.md, focusing on data handling using local text files, request routing, and business logic for the MusicStreaming app.\n\nTask Details:\n- Read design_spec.md from CONTEXT for all backend route specifications, data schemas, and functional requirements.\n- Produce a fully functional app.py implementing Flask routes, data loading from text files, search operations, playlist management, filtering, and statistics.\n- Do not incorporate frontend template details other than render and context variable usage as specified.\n- Write app.py independently without reading frontend templates.\n\n**Implementation Requirements:**\n- Implement data loading functions to read all specified text files (songs.txt, artists.txt, albums.txt, genres.txt, playlists.txt, playlist_songs.txt) with correct parsing per schema.\n- Define Flask routes with route paths, HTTP methods, and handlers as documented in design_spec.md.\n- Include logic for search (songs, albums, artists), filtering (genres), playlist CRUD operations, album and artist detail retrieval, and statistics computations.\n- Render templates with correct context dictionaries matching design_spec.md variable contracts.\n\n**Code Quality and Structure:**\n- Use concise, modular functions with clear single-quote docstring documentation.\n- Handle errors gracefully, especially file I/O and data integrity issues.\n- Maintain code readability with consistent style and commenting.\n\nCRITICAL SUCCESS CRITERIA:\n- app.py must comply fully with design_spec.md requirements for routes, data access, and processing.\n- Must use write_text_file tool to save app.py.\n- Output only the declared artifact app.py without extraneous notes.\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ],\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a frontend developer specializing in HTML and Jinja2 templating for Flask applications.\n\nYour goal is to implement all HTML templates (*.html) for the MusicStreaming app using element IDs, page structures, and navigation flows as specified in design_spec.md.\n\nTask Details:\n- Read design_spec.md from CONTEXT to extract frontend template specifications including page layouts, element IDs, and UI components.\n- Independently create all required templates under templates/*.html with correct element IDs and content placeholders.\n- Ensure navigation buttons, links, and data bindings match design_spec.md specifications.\n- Do not read or depend on backend code files.\n\n**Template Implementation Guidelines:**\n- Follow the exact page titles and element IDs as defined.\n- Use Jinja2 syntax for dynamic content rendering consistent with context variables described in design_spec.md.\n- Include page containers, buttons, inputs, grids, tables, and other UI elements with proper semantic HTML structures.\n- Maintain consistent style and accessibility where applicable.\n\n**Navigation and Interaction:**\n- Implement all buttons with designated IDs linked to appropriate routes or JavaScript hooks per design_spec.md.\n- Ensure forms, dropdowns, and search inputs are properly named and integrated.\n\nCRITICAL SUCCESS CRITERIA:\n- All templates must fully conform to design_spec.md UI requirements and element ID mappings.\n- Must use write_text_file tool to write templates/*.html files.\n- Output only the declared artifact templates/*.html, no additional files or commentary.\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ],\n        },\n        {\n            \"agent_name\": \"IntegrationMerger\",\n            \"prompt\": \"\"\"You are a software integration engineer specializing in merging Flask backend and frontend templates for web applications.\n\nYour goal is to consolidate and reconcile the backend app.py and frontend templates/*.html into a consistent, functional MusicStreaming app aligned with design_spec.md.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT.\n- Verify that all routes in app.py have corresponding templates with matching element IDs and navigation controls.\n- Detect and correct interface inconsistencies between backend context variables and frontend template placeholders.\n- Adjust only integration-related issues without altering core logic or UI specifications.\n- Produce the final app.py and templates/*.html artifacts fully aligned and ready for deployment.\n\n**Integration Tasks:**\n- Confirm all page routes defined in design_spec.md are implemented in app.py and referenced by templates.\n- Ensure element IDs in templates correspond to context variables rendered by app.py routes.\n- Verify that navigation buttons and links work correctly between pages as defined.\n- Correct any mismatches in naming, missing elements, or broken bindings.\n\n**Quality Assurance:**\n- Adhere strictly to design_spec.md requirements without adding new features.\n- Provide clear consistency in naming conventions and data flow between backend and frontend.\n- Maintain proper formatting and code comments only where necessary for integration clarity.\n\nCRITICAL SUCCESS CRITERIA:\n- Final app.py and templates/*.html fully conform to design_spec.md and pass backend-frontend integration validation.\n- Use write_text_file tool to output final app.py and all templates/*.html.\n- Output only declared artifacts app.py and templates/*.html.\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ],\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Verify backend implementation correctness and conformance to design_spec.md.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"app.py\"}]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Verify frontend template correctness and conformance to design_spec.md.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"templates/*.html\"}]\n        }\n    ]\n): pass",
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
    "BackendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in Python Flask backend development with local text file database interaction.

Your goal is to specify the backend design including Flask routes, data access logic, and data schemas reflecting the MusicStreaming application requirements.

Task Details:
- Read user_task_description from CONTEXT
- Independently create backend_design.md specifying all Flask endpoints, request methods, and data interaction patterns
- Utilize the specified local text data files: songs.txt, artists.txt, albums.txt, genres.txt, playlists.txt, playlist_songs.txt
- Exclude any dependency or assumptions on frontend_design.md

**Section 1: Flask Route Specifications**
- Define each route path, HTTP method(s), expected request parameters, and response data structure
- Include routes for searching songs, managing playlists, browsing albums, exploring artists, filtering genres, and statistics pages
- Specify JSON structures or context variables passed to templates where applicable

**Section 2: Data File Schemas and Access**
- Describe the exact parsing logic and schema for each local text file based on column definitions and delimiters
- Detail how data is read, filtered, and aggregated from these files in the backend
- Cover data models representing songs, artists, albums, genres, playlists, and playlist songs with example data rows

**Section 3: API and Integration Details**
- Define APIs for add/remove songs in playlists, play counts updates, and navigation handling
- Describe any necessary query parameters for filtering and sorting on the backend

CRITICAL SUCCESS CRITERIA:
- BackendDeveloper can implement functional Flask routes and data access from backend_design.md alone
- Data file schemas are accurate and directly correspond to user_task_description examples
- Use write_text_file tool to output backend_design.md

Output: backend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'backend_design.md'}],

    },

    "FrontendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in HTML and Jinja2 template design for Python web applications.

Your goal is to specify frontend HTML templates with detailed element IDs and UI structure for all MusicStreaming web pages as described.

Task Details:
- Read user_task_description from CONTEXT
- Independently create frontend_design.md detailing all required HTML template files and their element IDs
- Cover each of the ten specified pages: Dashboard, Song Catalog, Song Details, Playlists, Playlist Details, Create Playlist, Album Browse, Album Details, Artist Profiles, and Genre Exploration
- Specify UI components such as buttons, input fields, dropdowns, grids, tables, and navigation widgets
- Do not depend on backend_design.md

**Section 1: HTML Templates Overview**
- For each page, specify template filenames and page titles
- List element IDs with their HTML element types and roles
- Define navigation button actions and filtering UI elements

**Section 2: UI Components and Interactions**
- Detail how search inputs, dropdown filters, and buttons interact within templates
- Include dynamic elements needing context variables and loops (e.g., song cards, playlist grids)
- Provide exact ID conventions for controls like add-to-playlist and remove-song buttons with placeholders

CRITICAL SUCCESS CRITERIA:
- FrontendDeveloper can implement all templates and UI elements from frontend_design.md alone
- Element IDs and page structures comply strictly with user_task_description
- Use write_text_file tool to output frontend_design.md

Output: frontend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_design.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a System Architect specializing in integrating backend and frontend design specifications for Flask web applications.

Your goal is to merge backend_design.md and frontend_design.md into a unified, consistent design_spec.md without introducing new features beyond the user task.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Verify completeness and resolve any inconsistencies between backend routes, data schemas, and frontend template elements
- Ensure naming conventions, element IDs, and route parameters align perfectly across designs
- Consolidate all information into one canonical design_spec.md document

**Section 1: Consistency Verification**
- Cross-check that every frontend element requiring backend data has matching route/context variable definitions
- Confirm all backend routes are supported by corresponding frontend templates or UI components

**Section 2: Unified Design Specification**
- Integrate backend routes, data schemas, and frontend templates with element IDs into coherent sections
- Maintain clear separation with consistent formatting consistent for developer consumption

CRITICAL SUCCESS CRITERIA:
- Resulting design_spec.md enables developers to implement both backend Flask routes and frontend HTML templates with no contradictions
- The artifact references ONLY declared input artifacts; no extra requirements added
- Use write_text_file tool to output design_spec.md

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'backend_design.md', 'source': 'BackendDesignArchitect'}, {'type': 'text_file', 'name': 'frontend_design.md', 'source': 'FrontendDesignArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Python backend developer specializing in Flask web applications.

Your goal is to implement a complete Flask backend application as specified in design_spec.md, focusing on data handling using local text files, request routing, and business logic for the MusicStreaming app.

Task Details:
- Read design_spec.md from CONTEXT for all backend route specifications, data schemas, and functional requirements.
- Produce a fully functional app.py implementing Flask routes, data loading from text files, search operations, playlist management, filtering, and statistics.
- Do not incorporate frontend template details other than render and context variable usage as specified.
- Write app.py independently without reading frontend templates.

**Implementation Requirements:**
- Implement data loading functions to read all specified text files (songs.txt, artists.txt, albums.txt, genres.txt, playlists.txt, playlist_songs.txt) with correct parsing per schema.
- Define Flask routes with route paths, HTTP methods, and handlers as documented in design_spec.md.
- Include logic for search (songs, albums, artists), filtering (genres), playlist CRUD operations, album and artist detail retrieval, and statistics computations.
- Render templates with correct context dictionaries matching design_spec.md variable contracts.

**Code Quality and Structure:**
- Use concise, modular functions with clear single-quote docstring documentation.
- Handle errors gracefully, especially file I/O and data integrity issues.
- Maintain code readability with consistent style and commenting.

CRITICAL SUCCESS CRITERIA:
- app.py must comply fully with design_spec.md requirements for routes, data access, and processing.
- Must use write_text_file tool to save app.py.
- Output only the declared artifact app.py without extraneous notes.

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],

    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a frontend developer specializing in HTML and Jinja2 templating for Flask applications.

Your goal is to implement all HTML templates (*.html) for the MusicStreaming app using element IDs, page structures, and navigation flows as specified in design_spec.md.

Task Details:
- Read design_spec.md from CONTEXT to extract frontend template specifications including page layouts, element IDs, and UI components.
- Independently create all required templates under templates/*.html with correct element IDs and content placeholders.
- Ensure navigation buttons, links, and data bindings match design_spec.md specifications.
- Do not read or depend on backend code files.

**Template Implementation Guidelines:**
- Follow the exact page titles and element IDs as defined.
- Use Jinja2 syntax for dynamic content rendering consistent with context variables described in design_spec.md.
- Include page containers, buttons, inputs, grids, tables, and other UI elements with proper semantic HTML structures.
- Maintain consistent style and accessibility where applicable.

**Navigation and Interaction:**
- Implement all buttons with designated IDs linked to appropriate routes or JavaScript hooks per design_spec.md.
- Ensure forms, dropdowns, and search inputs are properly named and integrated.

CRITICAL SUCCESS CRITERIA:
- All templates must fully conform to design_spec.md UI requirements and element ID mappings.
- Must use write_text_file tool to write templates/*.html files.
- Output only the declared artifact templates/*.html, no additional files or commentary.

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "IntegrationMerger": {
        "prompt": (
            """You are a software integration engineer specializing in merging Flask backend and frontend templates for web applications.

Your goal is to consolidate and reconcile the backend app.py and frontend templates/*.html into a consistent, functional MusicStreaming app aligned with design_spec.md.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT.
- Verify that all routes in app.py have corresponding templates with matching element IDs and navigation controls.
- Detect and correct interface inconsistencies between backend context variables and frontend template placeholders.
- Adjust only integration-related issues without altering core logic or UI specifications.
- Produce the final app.py and templates/*.html artifacts fully aligned and ready for deployment.

**Integration Tasks:**
- Confirm all page routes defined in design_spec.md are implemented in app.py and referenced by templates.
- Ensure element IDs in templates correspond to context variables rendered by app.py routes.
- Verify that navigation buttons and links work correctly between pages as defined.
- Correct any mismatches in naming, missing elements, or broken bindings.

**Quality Assurance:**
- Adhere strictly to design_spec.md requirements without adding new features.
- Provide clear consistency in naming conventions and data flow between backend and frontend.
- Maintain proper formatting and code comments only where necessary for integration clarity.

CRITICAL SUCCESS CRITERIA:
- Final app.py and templates/*.html fully conform to design_spec.md and pass backend-frontend integration validation.
- Use write_text_file tool to output final app.py and all templates/*.html.
- Output only declared artifacts app.py and templates/*.html.

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'BackendDesignArchitect': [
        ("DesignMerger", """Verify backend design completeness and correctness per user task and local file data handling.""", [{'type': 'text_file', 'name': 'backend_design.md'}])
    ],

    'FrontendDesignArchitect': [
        ("DesignMerger", """Verify frontend design completeness and correctness of HTML element IDs and page structures.""", [{'type': 'text_file', 'name': 'frontend_design.md'}])
    ],

    'BackendDeveloper': [
        ("IntegrationMerger", """Verify backend implementation correctness and conformance to design_spec.md.""", [{'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("IntegrationMerger", """Verify frontend template correctness and conformance to design_spec.md.""", [{'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    BackendDesignArchitect = build_resilient_agent(
        agent_name="BackendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )
    FrontendDesignArchitect = build_resilient_agent(
        agent_name="FrontendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )
    DesignMerger = build_resilient_agent(
        agent_name="DesignMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    # Run BackendDesignArchitect and FrontendDesignArchitect in parallel
    await asyncio.gather(
        execute(BackendDesignArchitect, "Create backend_design.md specifying Flask routes, data schemas, and file interaction patterns based on user_task_description."),
        execute(FrontendDesignArchitect, "Create frontend_design.md specifying HTML templates, element IDs, UI components, and navigation based on user_task_description.")
    )

    # Read outputs for merger
    backend_content, frontend_content = "", ""
    try:
        backend_content = open("backend_design.md").read()
    except Exception:
        pass
    try:
        frontend_content = open("frontend_design.md").read()
    except Exception:
        pass

    # Merge backend and frontend designs into design_spec.md
    await execute(
        DesignMerger,
        f"Merge backend_design.md and frontend_design.md to create unified design_spec.md.\n\n"
        f"=== backend_design.md ===\n{backend_content}\n\n"
        f"=== frontend_design.md ===\n{frontend_content}"
    )
# Phase1_End
# Phase2_Start
import asyncio
import glob

async def implementation_and_verification_phase():
    BackendDeveloper = build_resilient_agent(
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=480,
        failure_threshold=2,
        recovery_time=60
    )
    FrontendDeveloper = build_resilient_agent(
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=480,
        failure_threshold=2,
        recovery_time=60
    )
    IntegrationMerger = build_resilient_agent(
        agent_name="IntegrationMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    # Run BackendDeveloper and FrontendDeveloper in parallel
    await asyncio.gather(
        execute(
            BackendDeveloper,
            "Implement app.py with routes, data loading, search, playlist management, and statistics as specified in design_spec.md. "
            "Save output to app.py."
        ),
        execute(
            FrontendDeveloper,
            "Implement all HTML templates (*.html) according to design_spec.md with exact element IDs, navigation, and UI features. "
            "Save output to templates/*.html."
        )
    )

    # Read latest outputs for IntegrationMerger
    app_content = ""
    templates_content = ""
    try:
        app_content = open("app.py").read()
    except FileNotFoundError:
        pass

    for template_path in sorted(glob.glob("templates/*.html")):
        try:
            templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
        except OSError:
            pass

    # Run IntegrationMerger to merge and verify full integration, output final app.py and templates
    await execute(
        IntegrationMerger,
        "Consolidate and reconcile backend app.py and frontend templates/*.html to ensure interface consistency and correctness "
        "per design_spec.md. Adjust only integration points, no new features. Output final app.py and templates/*.html.\n\n"
        f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md','')}\n\n"
        f"=== app.py ===\n{app_content}\n\n"
        f"=== templates/*.html ===\n{templates_content}"
    )
# Phase2_End
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
        implementation_and_verification_phase()
    ]

    await asyncio.gather(*step1)
    await asyncio.gather(*step2)

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
