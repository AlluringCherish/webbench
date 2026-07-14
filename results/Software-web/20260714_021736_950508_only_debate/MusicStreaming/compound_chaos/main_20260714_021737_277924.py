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
# 20260714_021737_277924/main_20260714_021737_277924.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Debate the adaptive design of the MusicStreaming Flask web app with exact page routes, elements, data formats, and no-authentication contract; deliver design_spec.md.\",\n    collab_pattern_name: str = \"Multi-Agent Debate\",\n    collab_pattern_description: str = (\n        \"DesignDebaterA and DesignDebaterB independently draft design_debate_a.md and design_debate_b.md respectively \"\n        \"in round 1, revising once in round 2 informed by each other's artifacts. DesignJudge adjudicates and writes \"\n        \"design_spec.md consolidating exact Flask routes, HTTP methods, templates with specified element IDs, form fields, \"\n        \"actions, and local-text persistence behavior compliant with the adaptive Web contract.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignDebaterA\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Python Flask web application design specifications.\n\nYour goal is to create and improve a complete and precise design specification file (design_debate_a.md) for the MusicStreaming app, capturing all page routes, element IDs, HTTP methods, templates, and local text file data management consistent with the highest Web contract standards for no-authentication applications.\n\nTask Details:\n- Read the entire user_task_description for MusicStreaming to understand page and data requirements\n- In round 1, author a full design_debate_a.md specifying Flask routes using exact paths, HTTP methods, and template names\n- Detail required HTML element IDs including dynamic IDs (e.g., add-to-playlist-button-{song_id}) for every page\n- Specify all form field names, method, and action attributes explicitly\n- Define data file schemas with precise field order, separators, and example rows matching local text files\n- Overwrite design_debate_a.md every round, revising based on peer design_debate_b.md only if consistent with user task\n\n**Section 1: Flask Routes and Views Specification**\n- State route path strings exactly as declared by the user (e.g., '/', '/dashboard', '/songs', '/playlist/<playlist_id>')\n- Specify HTTP methods (GET, POST, etc.)\n- Specify template file names for rendering each route\n- Define context variables passed to templates precisely by name and type\n\n**Section 2: HTML Template Element IDs and Interactions**\n- Enumerate exact HTML element IDs and dynamic ID patterns per page\n- Specify purpose/type of each element (Div, Button, Input, Dropdown, Table, etc.)\n- Document navigation button targets and form submission behaviors\n- Include all buttons' form methods and action attributes exactly\n\n**Section 3: Data File Schemas and Data Flow**\n- List all local text data files with full exact path 'data/<filename>.txt'\n- Specify each file's field separator as '|' and exact field order and names\n- Include example data lines verbatim from user\n- Specify data access patterns matching UI functionality (e.g., playlist song additions tracked via playlist_songs.txt)\n- Maintain data schema immutability and no extra fields\n\nCRITICAL SUCCESS CRITERIA:\n- Two total debate rounds: independent round 1 then peer-informed round 2 revising design_debate_a.md\n- Output must be a valid markdown file fully sufficient to implement the described Flask app compliant with the adaptive Web contract without adding requirements\n- Preserve exact route, template, form and element ID fidelity\n- Use write_text_file tool to save output as design_debate_a.md\n\nOutput: design_debate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_a.md\", \"source\": \"DesignDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_b.md\", \"source\": \"DesignDebaterB\"},\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_debate_a.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignDebaterB\",\n            \"prompt\": \"\"\"You are a System Architect specialized in Flask web application design and data flow specifications.\n\nYour goal is to author and refine a detailed design specification (design_debate_b.md) for the MusicStreaming web application capturing mandatory page routing, element ID contracts, HTTP form behaviors, and data persistence strictly using local text files consistent with the highest Web workflow standards.\n\nTask Details:\n- Analyze user_task_description to understand each page's UI elements and data dependencies\n- Draft complete Flask route definitions with exact HTTP methods, template files, and context data\n- Enumerate all page element IDs including dynamic patterned IDs (e.g., view-playlist-button-{playlist_id}) ensuring exact match to user descriptions\n- Specify form field names, methods, and action URL attributes without deviations\n- Document exact local text data file names and field structures supporting data flow for playlist, song, artist, album, genre, and statistics features\n- Overwrite design_debate_b.md after each round; incorporate peer suggestions only if aligned with user specs\n\n**Section 1: Page Routes and Navigation Flow**\n- Declare all routes starting from '/' rendering the Dashboard page by default\n- Define exact routes for all 10 pages described including parameters (e.g., song_id, album_id)\n- Specify navigational flows triggered by buttons with exact target routes\n\n**Section 2: HTML Elements, IDs, and Form Contracts**\n- Specify element types and exact ID strings for each page\n- Define dynamic IDs using brace notation for variables\n- Specify form method (GET or POST), action URLs, and input field names exactly\n- Include buttons for playlist management, song addition/removal with proper form definitions\n\n**Section 3: Local Text File Data Schema and Access**\n- List all data files in 'data' directory with exact filenames and schema delimiter '|'\n- Specify each file’s field order and example records as given\n- Correlate UI features (e.g., filters, searches) to read operations on local files\n- Ensure no authentication or user session data modifies storage logic\n\nCRITICAL SUCCESS CRITERIA:\n- Produce a deployable design document matching user specs exactly\n- Maintain strict adherence to declared routes, IDs, forms, and local text data handling\n- Use write_text_file tool to output design_debate_b.md\n\nOutput: design_debate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_b.md\", \"source\": \"DesignDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_a.md\", \"source\": \"DesignDebaterA\"},\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_debate_b.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignJudge\",\n            \"prompt\": \"\"\"You are a Senior System Architect responsible for adjudicating competing Flask web app design specifications.\n\nYour goal is to produce one canonical design_spec.md that consolidates and validates all accurate page routes, element IDs, HTTP methods, form fields, navigation targets, template usages, and local text file data schema for the MusicStreaming web app, fully conforming to the no-authentication adaptive Web contract.\n\nTask Details:\n- Read user_task_description plus final design_debate_a.md and design_debate_b.md after round 2\n- Cross-verify all routes start from '/' rendering dashboard or redirecting accordingly\n- Validate exact match of all HTML element IDs and dynamic IDs\n- Verify form action URLs, methods, and field names for all interactive pages\n- Confirm local data file names, delimiter usage, field orders, and example lines match authoritative user spec\n- Ensure no additional requirements or unsupported routes/forms/data beyond input artifacts\n- Combine both debater inputs into one singular, consistent, comprehensive design_spec.md\n\n**Verification Checklist:**\n- Route paths and HTTP methods exactly correct and consistent\n- Template file names and context variables precise and complete\n- HTML element IDs including dynamic per-item IDs correct without modification\n- Forms use declared methods, action URLs, and include all required inputs\n- Local text file data schema fully detailed and reflects user examples\n- Navigation button targets and back-to-dashboard routes included\n\nCRITICAL SUCCESS CRITERIA:\n- Output a fully usable design_spec.md enabling flawless Flask app implementation\n- Preserve exact user-declared routes, parameters, and all element IDs\n- Use write_text_file tool to save design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_a.md\", \"source\": \"DesignDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_b.md\", \"source\": \"DesignDebaterB\"},\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignDebaterA\",\n            \"reviewer_agent\": \"DesignJudge\",\n            \"review_criteria\": (\n                \"Approve when design_debate_a.md exists, is non-empty, readable, relevant, and has no catastrophic format errors; \"\n                \"partial completeness acceptable.\"\n            ),\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_debate_a.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignDebaterB\",\n            \"reviewer_agent\": \"DesignJudge\",\n            \"review_criteria\": (\n                \"Approve when design_debate_b.md exists, is non-empty, readable, relevant, and has no catastrophic format errors; \"\n                \"partial completeness acceptable.\"\n            ),\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_debate_b.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignJudge\",\n            \"reviewer_agent\": \"DesignDebaterA\",\n            \"review_criteria\": (\n                \"Approve when design_spec.md exists, is non-empty, readable, broadly usable, and satisfies the adaptive Web contract for \"\n                \"MusicStreaming app; minor omissions and polish allowed.\"\n            ),\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Debate complete, valid Flask app implementation and templates for MusicStreaming web app with local-text persistence and exact UI contract; deliver app.py and templates/*.html.\",\n    collab_pattern_name: str = \"Multi-Agent Debate\",\n    collab_pattern_description: str = (\n        \"ImplementationDebaterA and ImplementationDebaterB independently implement full Flask app.py and templates sets (templates_debate_a and templates_debate_b) \"\n        \"in round 1, revise once in round 2 informed by peer artifacts; ImplementationJudge adjudicates and writes canonical app.py and templates/*.html with strict conformance.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationDebaterA\",\n            \"prompt\": \"\"\"You are a Python Flask developer specializing in full-stack web application implementation with local text file persistence.\n\nYour goal is to implement a complete MusicStreaming Flask backend (app.py) and frontend templates_debate_a/*.html based on design_spec.md with exact compliance.\n\nTask Details:\n- Read design_spec.md, app_debate_a.py, app_debate_b.py, templates_debate_a/*.html, and templates_debate_b/*.html from CONTEXT\n- Independently write and revise app_debate_a.py and templates_debate_a/*.html across exactly two debate rounds\n- Deliver a Flask app.py implementing all declared routes (including '/'), HTTP methods, and local-text persistence\n- Deliver frontend HTML templates with exact element IDs, form field names, POST actions, and navigation flows per UI contract\n\n**Section 1: Backend Implementation Requirements**\n- Implement Flask routes for all specified pages with exact route paths and methods, preserving the DASHBOARD as root route ('/')\n- Implement all POST actions with persistent local text file updates in data directory exactly as per spec\n- Ensure no authentication is required; all features accessed directly\n- Follow proper file reads/writes matching data file schema and formats specified in design_spec.md\n\n**Section 2: Frontend Templates Requirements**\n- Render templates_debate_a/*.html matching all pages from design_spec.md including exact page titles and all required UI elements with exact IDs\n- Preserve dynamic button IDs (e.g., 'add-to-playlist-button-{song_id}') as specified, ensuring ability to handle multiple instances\n- Bind form field names, methods, and POST actions precisely to support backend routes with local persistence\n\n**Section 3: Collaboration and Revision**\n- In round 2, revise code and templates informed by peer artifacts (app_debate_b.py and templates_debate_b/*.html)\n- Maintain exact adherence to design_spec.md without adding new functionality or routes beyond specification\n\nCRITICAL SUCCESS CRITERIA:\n- Must use write_text_file tool to save app_debate_a.py and templates_debate_a/*.html during each round\n- Preserve exact filenames and file paths for all outputs\n- Implement root route '/' as the main Dashboard per authoritative web profile\n- Preserve all declared element IDs, dynamic IDs, form field names, methods, and local persistence behavior strictly\n- Write only the declared output artifacts; do not append refinement markers or extra files\n\nOutput: app_debate_a.py, templates_debate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignJudge\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\", \"source\": \"ImplementationDebaterB\"},\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\"},\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationDebaterB\",\n            \"prompt\": \"\"\"You are a Python Flask developer specializing in full-stack web application implementation with local text file persistence.\n\nYour goal is to implement a complete MusicStreaming Flask backend (app.py) and frontend templates_debate_b/*.html strictly following design_spec.md.\n\nTask Details:\n- Read design_spec.md, app_debate_b.py, app_debate_a.py, templates_debate_b/*.html, and templates_debate_a/*.html from CONTEXT\n- Independently write and revise app_debate_b.py and templates_debate_b/*.html through exactly two debate rounds\n- Implement all declared routes including root '/', HTTP methods, and local text file persistence per spec\n- Create frontend templates with all pages, page titles, UI elements, and exact IDs as required\n- Correctly implement dynamic elements such as buttons with IDs including identifiers (e.g., 'add-to-playlist-button-{song_id}')\n\n**Section 1: Backend Implementation Requirements**\n- Ensure proper Flask route definitions and JSON/text data file operations exactly matching design_spec.md data schemas\n- Implement POST methods for modifications with local text file persistence maintaining data consistency\n- No authentication; all UI access is direct and open\n\n**Section 2: Frontend Templates Requirements**\n- Render templates_debate_b/*.html with exact UI elements and navigation flows conforming to design_spec.md\n- Maintain consistent form field names, methods, POST action URLs, and element IDs dynamically when applicable\n\n**Section 3: Collaboration and Revision**\n- In round 2, revise implementation informed by peer artifacts (app_debate_a.py, templates_debate_a/*.html)\n- Reject additions not supported by design_spec.md or which alter the defined contract\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to output app_debate_b.py and templates_debate_b/*.html\n- Preserve exact filenames and paths for all outputs\n- Implement root route '/' as the dashboard page entry point exactly\n- Preserve all element IDs, dynamic IDs, form mapping, HTTP methods, and local persistence strictly\n- Produce only the declared output artifacts, without extra markings or refinements\n\nOutput: app_debate_b.py, templates_debate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignJudge\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\", \"source\": \"ImplementationDebaterA\"},\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\"},\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationJudge\",\n            \"prompt\": \"\"\"You are a Senior Python Flask developer and implementation adjudicator specializing in verifying full-stack web applications with local text file persistence.\n\nYour goal is to review and adjudicate candidate Flask backend implementations (app_debate_a.py, app_debate_b.py) and frontend template sets against design_spec.md; write one canonical app.py and templates/*.html set.\n\nTask Details:\n- Read design_spec.md, app_debate_a.py, templates_debate_a/*.html, app_debate_b.py, templates_debate_b/*.html from CONTEXT\n- Thoroughly compare both candidate implementations requirement by requirement for full compliance\n- Ensure root route '/' serves the Dashboard page exactly, and all page routes, methods, element IDs, form field names, and local persistences are strictly adhered to\n- Resolve conflicts favoring strictest interpretation of design_spec.md without adding features or changing UI contract\n- Produce one complete and internally consistent app.py implementing all routes and local-text persistence correctly\n- Produce a canonical templates/*.html set with exact titles, element IDs, navigation flows, dynamic IDs, and form actions matching design_spec.md\n\n**Section 1: Compliance Verification**\n- Verify each route exists with exact HTTP methods and local file read/write persistence as per data schema\n- Verify templates have all required UI elements with exact IDs, including dynamic IDs such as 'add-to-playlist-button-{song_id}'\n- Verify navigation and forms maintain strict conformance with declared behavior and no authentication\n\n**Section 2: Artifact Generation**\n- Generate final app.py ready for deployment with no unfinished or placeholder code\n- Generate final templates/*.html set consistent, complete, and syntactically valid\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to output canonical app.py and templates/*.html\n- Output must adhere strictly to the UI and backend contract; no unsupported features or routes\n- Output must be clean, syntactically correct, and deployable per design_spec.md\n- Write only the declared output artifacts with no extra commentary or unfinished code\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignJudge\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\", \"source\": \"ImplementationDebaterB\"},\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationDebaterA\",\n            \"reviewer_agent\": \"ImplementationJudge\",\n            \"review_criteria\": (\n                \"Approve when app_debate_a.py and templates_debate_a/*.html exist, readable, relevant, syntactically valid, and broadly conforming \"\n                \"to design_spec.md; minor incompleteness allowed.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\"},\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationDebaterB\",\n            \"reviewer_agent\": \"ImplementationJudge\",\n            \"review_criteria\": (\n                \"Approve when app_debate_b.py and templates_debate_b/*.html exist, readable, relevant, syntactically valid, and broadly conforming \"\n                \"to design_spec.md; minor incompleteness allowed.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\"},\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationJudge\",\n            \"reviewer_agent\": \"ImplementationDebaterA\",\n            \"review_criteria\": (\n                \"Approve when final app.py and templates/*.html exist, are readable, syntactically correct, and usable to run MusicStreaming app per spec.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n            ]\n        }\n    ]\n): pass",
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
    "DesignDebaterA": {
        "prompt": (
            """You are a System Architect specializing in Python Flask web application design specifications.

Your goal is to create and improve a complete and precise design specification file (design_debate_a.md) for the MusicStreaming app, capturing all page routes, element IDs, HTTP methods, templates, and local text file data management consistent with the highest Web contract standards for no-authentication applications.

Task Details:
- Read the entire user_task_description for MusicStreaming to understand page and data requirements
- In round 1, author a full design_debate_a.md specifying Flask routes using exact paths, HTTP methods, and template names
- Detail required HTML element IDs including dynamic IDs (e.g., add-to-playlist-button-{song_id}) for every page
- Specify all form field names, method, and action attributes explicitly
- Define data file schemas with precise field order, separators, and example rows matching local text files
- Overwrite design_debate_a.md every round, revising based on peer design_debate_b.md only if consistent with user task

**Section 1: Flask Routes and Views Specification**
- State route path strings exactly as declared by the user (e.g., '/', '/dashboard', '/songs', '/playlist/<playlist_id>')
- Specify HTTP methods (GET, POST, etc.)
- Specify template file names for rendering each route
- Define context variables passed to templates precisely by name and type

**Section 2: HTML Template Element IDs and Interactions**
- Enumerate exact HTML element IDs and dynamic ID patterns per page
- Specify purpose/type of each element (Div, Button, Input, Dropdown, Table, etc.)
- Document navigation button targets and form submission behaviors
- Include all buttons' form methods and action attributes exactly

**Section 3: Data File Schemas and Data Flow**
- List all local text data files with full exact path 'data/<filename>.txt'
- Specify each file's field separator as '|' and exact field order and names
- Include example data lines verbatim from user
- Specify data access patterns matching UI functionality (e.g., playlist song additions tracked via playlist_songs.txt)
- Maintain data schema immutability and no extra fields

CRITICAL SUCCESS CRITERIA:
- Two total debate rounds: independent round 1 then peer-informed round 2 revising design_debate_a.md
- Output must be a valid markdown file fully sufficient to implement the described Flask app compliant with the adaptive Web contract without adding requirements
- Preserve exact route, template, form and element ID fidelity
- Use write_text_file tool to save output as design_debate_a.md

Output: design_debate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_debate_a.md'}],

    },

    "DesignDebaterB": {
        "prompt": (
            """You are a System Architect specialized in Flask web application design and data flow specifications.

Your goal is to author and refine a detailed design specification (design_debate_b.md) for the MusicStreaming web application capturing mandatory page routing, element ID contracts, HTTP form behaviors, and data persistence strictly using local text files consistent with the highest Web workflow standards.

Task Details:
- Analyze user_task_description to understand each page's UI elements and data dependencies
- Draft complete Flask route definitions with exact HTTP methods, template files, and context data
- Enumerate all page element IDs including dynamic patterned IDs (e.g., view-playlist-button-{playlist_id}) ensuring exact match to user descriptions
- Specify form field names, methods, and action URL attributes without deviations
- Document exact local text data file names and field structures supporting data flow for playlist, song, artist, album, genre, and statistics features
- Overwrite design_debate_b.md after each round; incorporate peer suggestions only if aligned with user specs

**Section 1: Page Routes and Navigation Flow**
- Declare all routes starting from '/' rendering the Dashboard page by default
- Define exact routes for all 10 pages described including parameters (e.g., song_id, album_id)
- Specify navigational flows triggered by buttons with exact target routes

**Section 2: HTML Elements, IDs, and Form Contracts**
- Specify element types and exact ID strings for each page
- Define dynamic IDs using brace notation for variables
- Specify form method (GET or POST), action URLs, and input field names exactly
- Include buttons for playlist management, song addition/removal with proper form definitions

**Section 3: Local Text File Data Schema and Access**
- List all data files in 'data' directory with exact filenames and schema delimiter '|'
- Specify each file’s field order and example records as given
- Correlate UI features (e.g., filters, searches) to read operations on local files
- Ensure no authentication or user session data modifies storage logic

CRITICAL SUCCESS CRITERIA:
- Produce a deployable design document matching user specs exactly
- Maintain strict adherence to declared routes, IDs, forms, and local text data handling
- Use write_text_file tool to output design_debate_b.md

Output: design_debate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_debate_b.md'}],

    },

    "DesignJudge": {
        "prompt": (
            """You are a Senior System Architect responsible for adjudicating competing Flask web app design specifications.

Your goal is to produce one canonical design_spec.md that consolidates and validates all accurate page routes, element IDs, HTTP methods, form fields, navigation targets, template usages, and local text file data schema for the MusicStreaming web app, fully conforming to the no-authentication adaptive Web contract.

Task Details:
- Read user_task_description plus final design_debate_a.md and design_debate_b.md after round 2
- Cross-verify all routes start from '/' rendering dashboard or redirecting accordingly
- Validate exact match of all HTML element IDs and dynamic IDs
- Verify form action URLs, methods, and field names for all interactive pages
- Confirm local data file names, delimiter usage, field orders, and example lines match authoritative user spec
- Ensure no additional requirements or unsupported routes/forms/data beyond input artifacts
- Combine both debater inputs into one singular, consistent, comprehensive design_spec.md

**Verification Checklist:**
- Route paths and HTTP methods exactly correct and consistent
- Template file names and context variables precise and complete
- HTML element IDs including dynamic per-item IDs correct without modification
- Forms use declared methods, action URLs, and include all required inputs
- Local text file data schema fully detailed and reflects user examples
- Navigation button targets and back-to-dashboard routes included

CRITICAL SUCCESS CRITERIA:
- Output a fully usable design_spec.md enabling flawless Flask app implementation
- Preserve exact user-declared routes, parameters, and all element IDs
- Use write_text_file tool to save design_spec.md

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationDebaterA": {
        "prompt": (
            """You are a Python Flask developer specializing in full-stack web application implementation with local text file persistence.

Your goal is to implement a complete MusicStreaming Flask backend (app.py) and frontend templates_debate_a/*.html based on design_spec.md with exact compliance.

Task Details:
- Read design_spec.md, app_debate_a.py, app_debate_b.py, templates_debate_a/*.html, and templates_debate_b/*.html from CONTEXT
- Independently write and revise app_debate_a.py and templates_debate_a/*.html across exactly two debate rounds
- Deliver a Flask app.py implementing all declared routes (including '/'), HTTP methods, and local-text persistence
- Deliver frontend HTML templates with exact element IDs, form field names, POST actions, and navigation flows per UI contract

**Section 1: Backend Implementation Requirements**
- Implement Flask routes for all specified pages with exact route paths and methods, preserving the DASHBOARD as root route ('/')
- Implement all POST actions with persistent local text file updates in data directory exactly as per spec
- Ensure no authentication is required; all features accessed directly
- Follow proper file reads/writes matching data file schema and formats specified in design_spec.md

**Section 2: Frontend Templates Requirements**
- Render templates_debate_a/*.html matching all pages from design_spec.md including exact page titles and all required UI elements with exact IDs
- Preserve dynamic button IDs (e.g., 'add-to-playlist-button-{song_id}') as specified, ensuring ability to handle multiple instances
- Bind form field names, methods, and POST actions precisely to support backend routes with local persistence

**Section 3: Collaboration and Revision**
- In round 2, revise code and templates informed by peer artifacts (app_debate_b.py and templates_debate_b/*.html)
- Maintain exact adherence to design_spec.md without adding new functionality or routes beyond specification

CRITICAL SUCCESS CRITERIA:
- Must use write_text_file tool to save app_debate_a.py and templates_debate_a/*.html during each round
- Preserve exact filenames and file paths for all outputs
- Implement root route '/' as the main Dashboard per authoritative web profile
- Preserve all declared element IDs, dynamic IDs, form field names, methods, and local persistence behavior strictly
- Write only the declared output artifacts; do not append refinement markers or extra files

Output: app_debate_a.py, templates_debate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [],
        "output_artifacts": [],

    },

    "ImplementationDebaterB": {
        "prompt": (
            """You are a Python Flask developer specializing in full-stack web application implementation with local text file persistence.

Your goal is to implement a complete MusicStreaming Flask backend (app.py) and frontend templates_debate_b/*.html strictly following design_spec.md.

Task Details:
- Read design_spec.md, app_debate_b.py, app_debate_a.py, templates_debate_b/*.html, and templates_debate_a/*.html from CONTEXT
- Independently write and revise app_debate_b.py and templates_debate_b/*.html through exactly two debate rounds
- Implement all declared routes including root '/', HTTP methods, and local text file persistence per spec
- Create frontend templates with all pages, page titles, UI elements, and exact IDs as required
- Correctly implement dynamic elements such as buttons with IDs including identifiers (e.g., 'add-to-playlist-button-{song_id}')

**Section 1: Backend Implementation Requirements**
- Ensure proper Flask route definitions and JSON/text data file operations exactly matching design_spec.md data schemas
- Implement POST methods for modifications with local text file persistence maintaining data consistency
- No authentication; all UI access is direct and open

**Section 2: Frontend Templates Requirements**
- Render templates_debate_b/*.html with exact UI elements and navigation flows conforming to design_spec.md
- Maintain consistent form field names, methods, POST action URLs, and element IDs dynamically when applicable

**Section 3: Collaboration and Revision**
- In round 2, revise implementation informed by peer artifacts (app_debate_a.py, templates_debate_a/*.html)
- Reject additions not supported by design_spec.md or which alter the defined contract

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output app_debate_b.py and templates_debate_b/*.html
- Preserve exact filenames and paths for all outputs
- Implement root route '/' as the dashboard page entry point exactly
- Preserve all element IDs, dynamic IDs, form mapping, HTTP methods, and local persistence strictly
- Produce only the declared output artifacts, without extra markings or refinements

Output: app_debate_b.py, templates_debate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [],
        "output_artifacts": [],

    },

    "ImplementationJudge": {
        "prompt": (
            """You are a Senior Python Flask developer and implementation adjudicator specializing in verifying full-stack web applications with local text file persistence.

Your goal is to review and adjudicate candidate Flask backend implementations (app_debate_a.py, app_debate_b.py) and frontend template sets against design_spec.md; write one canonical app.py and templates/*.html set.

Task Details:
- Read design_spec.md, app_debate_a.py, templates_debate_a/*.html, app_debate_b.py, templates_debate_b/*.html from CONTEXT
- Thoroughly compare both candidate implementations requirement by requirement for full compliance
- Ensure root route '/' serves the Dashboard page exactly, and all page routes, methods, element IDs, form field names, and local persistences are strictly adhered to
- Resolve conflicts favoring strictest interpretation of design_spec.md without adding features or changing UI contract
- Produce one complete and internally consistent app.py implementing all routes and local-text persistence correctly
- Produce a canonical templates/*.html set with exact titles, element IDs, navigation flows, dynamic IDs, and form actions matching design_spec.md

**Section 1: Compliance Verification**
- Verify each route exists with exact HTTP methods and local file read/write persistence as per data schema
- Verify templates have all required UI elements with exact IDs, including dynamic IDs such as 'add-to-playlist-button-{song_id}'
- Verify navigation and forms maintain strict conformance with declared behavior and no authentication

**Section 2: Artifact Generation**
- Generate final app.py ready for deployment with no unfinished or placeholder code
- Generate final templates/*.html set consistent, complete, and syntactically valid

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output canonical app.py and templates/*.html
- Output must adhere strictly to the UI and backend contract; no unsupported features or routes
- Output must be clean, syntactically correct, and deployable per design_spec.md
- Write only the declared output artifacts with no extra commentary or unfinished code

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [],
        "output_artifacts": [],

    }

}

REVIEW_PROFILES = {
    'DesignDebaterA': [
        ("DesignJudge", """Approve when design_debate_a.md exists, is non-empty, readable, relevant, and has no catastrophic format errors; "
                "partial completeness acceptable.""", [{'type': 'text_file', 'name': 'design_debate_a.md'}])
    ],

    'DesignDebaterB': [
        ("DesignJudge", """Approve when design_debate_b.md exists, is non-empty, readable, relevant, and has no catastrophic format errors; "
                "partial completeness acceptable.""", [{'type': 'text_file', 'name': 'design_debate_b.md'}])
    ],

    'DesignJudge': [
        ("DesignDebaterA", """Approve when design_spec.md exists, is non-empty, readable, broadly usable, and satisfies the adaptive Web contract for "
                "MusicStreaming app; minor omissions and polish allowed.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationDebaterA': [
        ("ImplementationJudge", """Approve when app_debate_a.py and templates_debate_a/*.html exist, readable, relevant, syntactically valid, and broadly conforming "
                "to design_spec.md; minor incompleteness allowed.""", [{'type': 'text_file', 'name': 'app_debate_a.py'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html'}])
    ],

    'ImplementationDebaterB': [
        ("ImplementationJudge", """Approve when app_debate_b.py and templates_debate_b/*.html exist, readable, relevant, syntactically valid, and broadly conforming "
                "to design_spec.md; minor incompleteness allowed.""", [{'type': 'text_file', 'name': 'app_debate_b.py'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html'}])
    ],

    'ImplementationJudge': [
        ("ImplementationDebaterA", """Approve when final app.py and templates/*.html exist, are readable, syntactically correct, and usable to run MusicStreaming app per spec.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
    DesignDebaterA = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignDebaterA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=320,
        failure_threshold=1,
        recovery_time=40
    )
    DesignDebaterB = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignDebaterB",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=320,
        failure_threshold=1,
        recovery_time=40
    )
    DesignJudge = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignJudge",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )

    # Multi-Agent Debate: exactly 2 total rounds (1=initial, 2=one peer-informed revision)
    for round_num in range(1, 3):
        design_a, design_b = "", ""
        if round_num > 1:
            try:
                design_a = open("design_debate_a.md", "r", encoding="utf-8").read()
            except OSError:
                design_a = ""
            try:
                design_b = open("design_debate_b.md", "r", encoding="utf-8").read()
            except OSError:
                design_b = ""

        if round_num == 1:
            msg_a = "(No peer design yet - this is the initial round)"
            msg_b = "(No peer design yet - this is the initial round)"
        else:
            msg_a = f"Peer design_debate_b.md content to consider:\n\n{design_b}"
            msg_b = f"Peer design_debate_a.md content to consider:\n\n{design_a}"

        await asyncio.gather(
            execute(DesignDebaterA, msg_a),
            execute(DesignDebaterB, msg_b)
        )

    # Final: DesignJudge consolidates both final designs
    final_design_a, final_design_b = "", ""
    try:
        final_design_a = open("design_debate_a.md", "r", encoding="utf-8").read()
    except OSError:
        final_design_a = ""
    try:
        final_design_b = open("design_debate_b.md", "r", encoding="utf-8").read()
    except OSError:
        final_design_b = ""

    await execute(
        DesignJudge,
        f"Adjudicate and consolidate the final design documents into design_spec.md.\n\n"
        f"=== design_debate_a.md ===\n{final_design_a}\n\n"
        f"=== design_debate_b.md ===\n{final_design_b}"
    )
# Phase1_End
# Phase2_Start
import asyncio
import glob

async def implementation_and_verification_phase():
    ImplementationDebaterA = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationDebaterA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=30
    )
    ImplementationDebaterB = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationDebaterB",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=30
    )
    ImplementationJudge = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationJudge",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=30
    )

    # Multi-Agent Debate: exactly 2 total rounds (round 1 = initial independent drafts, round 2 = peer-informed revision)
    for round_num in range(1, 3):
        app_a, app_b = "", ""
        templates_a, templates_b = "", ""

        if round_num > 1:
            try:
                app_a = open("app_debate_a.py", "r", encoding="utf-8").read()
            except OSError:
                app_a = ""
            try:
                app_b = open("app_debate_b.py", "r", encoding="utf-8").read()
            except OSError:
                app_b = ""

            templates_a_parts = []
            for path in sorted(glob.glob("templates_debate_a/*.html")):
                try:
                    templates_a_parts.append("=== " + path + " ===\n" + open(path, "r", encoding="utf-8").read())
                except OSError:
                    pass
            templates_a = "\n\n".join(templates_a_parts)

            templates_b_parts = []
            for path in sorted(glob.glob("templates_debate_b/*.html")):
                try:
                    templates_b_parts.append("=== " + path + " ===\n" + open(path, "r", encoding="utf-8").read())
                except OSError:
                    pass
            templates_b = "\n\n".join(templates_b_parts)

        if round_num == 1:
            msg_a = "(No peer artifacts yet; this is round 1 initial implementation.)"
            msg_b = "(No peer artifacts yet; this is round 1 initial implementation.)"
        else:
            msg_a = (
                "Round 2: revise your implementation informed by the peer's artifacts below.\n\n"
                "=== Peer app_debate_b.py ===\n" + app_b + "\n\n"
                "=== Peer templates_debate_b/*.html ===\n" + templates_b
            )
            msg_b = (
                "Round 2: revise your implementation informed by the peer's artifacts below.\n\n"
                "=== Peer app_debate_a.py ===\n" + app_a + "\n\n"
                "=== Peer templates_debate_a/*.html ===\n" + templates_a
            )

        await asyncio.gather(
            execute(ImplementationDebaterA, msg_a),
            execute(ImplementationDebaterB, msg_b)
        )

    # After two rounds, read all final artifacts for adjudication
    try:
        app_a = open("app_debate_a.py", "r", encoding="utf-8").read()
    except OSError:
        app_a = ""
    try:
        app_b = open("app_debate_b.py", "r", encoding="utf-8").read()
    except OSError:
        app_b = ""

    templates_a_parts = []
    for path in sorted(glob.glob("templates_debate_a/*.html")):
        try:
            templates_a_parts.append("=== " + path + " ===\n" + open(path, "r", encoding="utf-8").read())
        except OSError:
            pass
    templates_a = "\n\n".join(templates_a_parts)

    templates_b_parts = []
    for path in sorted(glob.glob("templates_debate_b/*.html")):
        try:
            templates_b_parts.append("=== " + path + " ===\n" + open(path, "r", encoding="utf-8").read())
        except OSError:
            pass
    templates_b = "\n\n".join(templates_b_parts)

    # Execute ImplementationJudge to adjudicate and produce canonical app.py and templates/*.html
    await execute(
        ImplementationJudge,
        "Compare and adjudicate the two final candidate implementations. Produce final canonical app.py and templates/*.html.\n\n"
        "=== Candidate ImplementationDebaterA app_debate_a.py ===\n" + app_a + "\n\n"
        "=== Candidate ImplementationDebaterA templates_debate_a/*.html ===\n" + templates_a + "\n\n"
        "=== Candidate ImplementationDebaterB app_debate_b.py ===\n" + app_b + "\n\n"
        "=== Candidate ImplementationDebaterB templates_debate_b/*.html ===\n" + templates_b
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
