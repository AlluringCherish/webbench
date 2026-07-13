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
# 20260714_001749_829389/main_20260714_001749_829389.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Refine the adaptive design specification for the MusicStreaming web app, producing design_spec.md and gated design_feedback.md\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"DesignGenerator writes design_spec.md describing all pages, navigation, UI elements, and data storage format; DesignCritic reviews design_spec.md and produces design_feedback.md with either [APPROVED] or NEED_MODIFY, iterating at most twice.\",\n    team: list = [\n        {\n            \"agent_name\": \"DesignGenerator\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Python web application design specifications.\n\nYour goal is to generate or revise a comprehensive design_spec.md for a music streaming web application that includes detailed page structures, navigation flows, UI element specifications, and local text file data formats, refined through at most two iterations based on critic feedback.\n\nTask Details:\n- Read user_task_description, previous design_spec.md, and design_feedback.md from CONTEXT\n- On first iteration, create a full design_spec.md covering all ten pages, element IDs, navigation starting from the dashboard, and data formats\n- On feedback starting with NEED_MODIFY, incorporate all corrections and fully rewrite design_spec.md accordingly\n- Stop after a maximum of two iterations or upon receiving [APPROVED] feedback\n- Output design_spec.md with full specification text\n\n**Section 1: Page and UI Element Specifications**\n- Detail all ten pages with exact page titles, container div IDs, and all UI elements including buttons, inputs, dropdowns, tables, and grids with correct element IDs\n- Include navigation button IDs and define navigation flow starting from the Dashboard page\n- Specify page overviews and ensure element types are clear\n\n**Section 2: Data Storage Formats**\n- Specify local text file data storage formats with precise file names, field orders, separators, and example rows for songs, artists, albums, genres, playlists, and playlist songs\n- Preserve the exact text file format and data field definitions as described in the user task\n\n**Section 3: Iterative Refinement**\n- Apply all critic feedback marked NEED_MODIFY fully in revisions\n- Avoid adding new requirements beyond user_task_description\n- Maintain clarity and consistency across pages, navigation, UI elements, and data schema\n\nCRITICAL SUCCESS CRITERIA:\n- Run at most two Generator/Critic refinement iterations\n- Fully implement all corrections requested by DesignCritic in NEED_MODIFY feedback\n- Write output using write_text_file tool to save design_spec.md\n- Do not include authentication since the app is accessible without login\n- Output file must be named design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\", \"source\": \"DesignCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignCritic\",\n            \"prompt\": \"\"\"You are a Design Review Engineer specializing in Python music streaming web application design reviews.\n\nYour goal is to review the submitted design_spec.md for completeness, correctness, and conformance with the user_task_description, and produce clear gated feedback with either [APPROVED] or NEED_MODIFY for at most two iterations.\n\nTask Details:\n- Read user_task_description and design_spec.md from CONTEXT\n- Check that design_spec.md includes all ten pages with exact element IDs and detailed UI components as per requirements\n- Verify navigation flow starts at the Dashboard page and all navigation buttons and links are coherent\n- Confirm local text file data formats exactly match the specified schemas, field orders, separators, and example data\n- Ensure no authentication or login elements are specified, confirming feature accessibility\n- Write design_feedback.md starting strictly with either [APPROVED] or NEED_MODIFY followed by itemized concrete corrections if applicable\n\nReview Criteria:\n1. All pages and their elements are fully specified matching user requirements\n2. Navigation flow and button IDs are accurately described\n3. Data file formats comply precisely with user specification\n4. No extra requirements or features absent from user_task_description are introduced\n5. Feedback begins exactly with [APPROVED] or NEED_MODIFY and contains clear actionable items if NEED_MODIFY\n\nCRITICAL REQUIREMENTS:\n- Provide gated feedback with exact initial marker [APPROVED] or NEED_MODIFY\n- Use write_text_file tool to persist design_feedback.md\n- Feedback must focus strictly on completeness, correctness, and adherence to user task\n- Stop after two review iterations or once [APPROVED] is given\n\nOutput: design_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignGenerator\",\n            \"reviewer_agent\": \"DesignCritic\",\n            \"review_criteria\": \"Check design_spec.md for adherence to all specified pages, elements, navigation starting at dashboard, data format, and absence of authentication\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Refine the combined backend and frontend implementation of the MusicStreaming app with app.py and templates/*.html, gated by code_feedback.md\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"AppGenerator writes or revises app.py and all HTML templates per design_spec.md and code_feedback.md; CodeCritic reviews all produced files for functionality, page elements and IDs, data handling from text files, and produces code_feedback.md with [APPROVED] or NEED_MODIFY at most twice.\",\n    team: list = [\n        {\n            \"agent_name\": \"AppGenerator\",\n            \"prompt\": \"\"\"You are a Python Web Application Developer specializing in full-stack implementation using local text file data management.\n\nYour goal is to implement or revise a complete app.py backend and all HTML templates (*.html) for the MusicStreaming app, fully realizing features, navigation, exact page element IDs, and local data file handling as specified in design_spec.md. You will perform at most two iterations based on code_feedback.md.\n\nTask Details:\n- Read design_spec.md, current app.py, templates/*.html, and code_feedback.md from CONTEXT\n- On first iteration, create or revise app.py and all required HTML templates (*.html) per design_spec.md\n- On feedback beginning with NEED_MODIFY, apply all required corrections and fully rewrite the affected artifacts\n- When feedback is [APPROVED], preserve the approved implementation\n\n**Section 1: Backend Implementation (app.py)**\n- Implement all required HTTP routes covering the 10 specified pages starting from Dashboard\n- Manage data loading, querying, and updates exclusively from local text files in the 'data' directory\n- Include route handlers reflecting exact element IDs and navigation flows per design_spec.md\n- Use clear modular functions to load and save data files with exact formats given\n- Provide song search, filter, playlist management, album and artist browsing as per spec\n\n**Section 2: Frontend Implementation (templates/*.html)**\n- Create individual HTML templates for each page with exact page titles and specified element IDs\n- Follow the structure and element types precisely (div, button, input, dropdown, table, etc.)\n- Ensure all dynamic content placeholders match backend context variables\n- Include buttons with correct IDs, especially those with dynamic suffixes ({song_id}, {playlist_id}, etc.)\n- Navigation buttons and links must support smooth user flow as per requirements\n\n**Section 3: Data File Conventions**\n- Do not invent or alter data file names or formats beyond what design_spec.md specifies\n- Ensure all data reads and writes conform strictly to the delimiter and field order conventions\n- Data integrity must be preserved when modifying playlists or counts\n\nCRITICAL REQUIREMENTS:\n- Run at most two iterations responding to NEED_MODIFY feedback, stopping immediately on [APPROVED]\n- ALWAYS use write_text_file tool to save complete app.py and templates/*.html files\n- Do not add new data files or endpoints outside specification\n- Preserve exact element IDs and data handling as described\n- Maintain filename conventions exactly: app.py and templates/*.html files as output\n\nOutput: app.py and templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\", \"source\": \"CodeCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"CodeCritic\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Python web application verification and HTML template validation.\n\nYour goal is to review the app.py backend and all HTML templates (*.html) to verify correctness, completeness, and conformance to design_spec.md. Provide gated feedback in code_feedback.md beginning with [APPROVED] or NEED_MODIFY, running at most two iterations.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Validate that app.py implements all specified routes, data file interactions, and navigation from design_spec.md\n- Verify templates/*.html contain the exact page titles, element tags, and specified exact element IDs for each page and dynamic elements\n- Check that dynamic element IDs (e.g. add-to-playlist-button-{song_id}) are present and correctly named\n- Confirm data access aligns exactly with specified text file formats and fields for songs, artists, albums, genres, playlists, and playlist_songs\n\nReview Checklist:\n1. All 10 pages are implemented with correct titles and containers per design_spec.md\n2. All functional buttons, inputs, dropdowns, tables have exact IDs as specified, including dynamic ones\n3. Backend routes load and save data only via specified local text files with correct format, delimiter, and field order\n4. Navigation buttons link to proper routes matching page flows\n5. Error handling and edge cases are addressed without inventing new features\n\nCRITICAL REQUIREMENTS:\n- The first bytes of code_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY\n- No prefixes, whitespace, or extra characters before these markers\n- Use both write_text_file and validate_python_file tools for comprehensive verification\n- Provide concrete, specific modification instructions if feedback is NEED_MODIFY\n- Stop the refinement loop immediately after [APPROVED]\n\nOutput: code_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\", \"validate_python_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"AppGenerator\",\n            \"reviewer_agent\": \"CodeCritic\",\n            \"review_criteria\": \"Gate app.py and templates/*.html for conformance to design_spec.md including page elements, navigation, data file usage, and required exact element IDs\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "DesignGenerator": {
        "prompt": (
            """You are a Software Architect specializing in Python web application design specifications.

Your goal is to generate or revise a comprehensive design_spec.md for a music streaming web application that includes detailed page structures, navigation flows, UI element specifications, and local text file data formats, refined through at most two iterations based on critic feedback.

Task Details:
- Read user_task_description, previous design_spec.md, and design_feedback.md from CONTEXT
- On first iteration, create a full design_spec.md covering all ten pages, element IDs, navigation starting from the dashboard, and data formats
- On feedback starting with NEED_MODIFY, incorporate all corrections and fully rewrite design_spec.md accordingly
- Stop after a maximum of two iterations or upon receiving [APPROVED] feedback
- Output design_spec.md with full specification text

**Section 1: Page and UI Element Specifications**
- Detail all ten pages with exact page titles, container div IDs, and all UI elements including buttons, inputs, dropdowns, tables, and grids with correct element IDs
- Include navigation button IDs and define navigation flow starting from the Dashboard page
- Specify page overviews and ensure element types are clear

**Section 2: Data Storage Formats**
- Specify local text file data storage formats with precise file names, field orders, separators, and example rows for songs, artists, albums, genres, playlists, and playlist songs
- Preserve the exact text file format and data field definitions as described in the user task

**Section 3: Iterative Refinement**
- Apply all critic feedback marked NEED_MODIFY fully in revisions
- Avoid adding new requirements beyond user_task_description
- Maintain clarity and consistency across pages, navigation, UI elements, and data schema

CRITICAL SUCCESS CRITERIA:
- Run at most two Generator/Critic refinement iterations
- Fully implement all corrections requested by DesignCritic in NEED_MODIFY feedback
- Write output using write_text_file tool to save design_spec.md
- Do not include authentication since the app is accessible without login
- Output file must be named design_spec.md

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'design_feedback.md', 'source': 'DesignCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DesignCritic": {
        "prompt": (
            """You are a Design Review Engineer specializing in Python music streaming web application design reviews.

Your goal is to review the submitted design_spec.md for completeness, correctness, and conformance with the user_task_description, and produce clear gated feedback with either [APPROVED] or NEED_MODIFY for at most two iterations.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT
- Check that design_spec.md includes all ten pages with exact element IDs and detailed UI components as per requirements
- Verify navigation flow starts at the Dashboard page and all navigation buttons and links are coherent
- Confirm local text file data formats exactly match the specified schemas, field orders, separators, and example data
- Ensure no authentication or login elements are specified, confirming feature accessibility
- Write design_feedback.md starting strictly with either [APPROVED] or NEED_MODIFY followed by itemized concrete corrections if applicable

Review Criteria:
1. All pages and their elements are fully specified matching user requirements
2. Navigation flow and button IDs are accurately described
3. Data file formats comply precisely with user specification
4. No extra requirements or features absent from user_task_description are introduced
5. Feedback begins exactly with [APPROVED] or NEED_MODIFY and contains clear actionable items if NEED_MODIFY

CRITICAL REQUIREMENTS:
- Provide gated feedback with exact initial marker [APPROVED] or NEED_MODIFY
- Use write_text_file tool to persist design_feedback.md
- Feedback must focus strictly on completeness, correctness, and adherence to user task
- Stop after two review iterations or once [APPROVED] is given

Output: design_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_feedback.md'}],

    },

    "AppGenerator": {
        "prompt": (
            """You are a Python Web Application Developer specializing in full-stack implementation using local text file data management.

Your goal is to implement or revise a complete app.py backend and all HTML templates (*.html) for the MusicStreaming app, fully realizing features, navigation, exact page element IDs, and local data file handling as specified in design_spec.md. You will perform at most two iterations based on code_feedback.md.

Task Details:
- Read design_spec.md, current app.py, templates/*.html, and code_feedback.md from CONTEXT
- On first iteration, create or revise app.py and all required HTML templates (*.html) per design_spec.md
- On feedback beginning with NEED_MODIFY, apply all required corrections and fully rewrite the affected artifacts
- When feedback is [APPROVED], preserve the approved implementation

**Section 1: Backend Implementation (app.py)**
- Implement all required HTTP routes covering the 10 specified pages starting from Dashboard
- Manage data loading, querying, and updates exclusively from local text files in the 'data' directory
- Include route handlers reflecting exact element IDs and navigation flows per design_spec.md
- Use clear modular functions to load and save data files with exact formats given
- Provide song search, filter, playlist management, album and artist browsing as per spec

**Section 2: Frontend Implementation (templates/*.html)**
- Create individual HTML templates for each page with exact page titles and specified element IDs
- Follow the structure and element types precisely (div, button, input, dropdown, table, etc.)
- Ensure all dynamic content placeholders match backend context variables
- Include buttons with correct IDs, especially those with dynamic suffixes ({song_id}, {playlist_id}, etc.)
- Navigation buttons and links must support smooth user flow as per requirements

**Section 3: Data File Conventions**
- Do not invent or alter data file names or formats beyond what design_spec.md specifies
- Ensure all data reads and writes conform strictly to the delimiter and field order conventions
- Data integrity must be preserved when modifying playlists or counts

CRITICAL REQUIREMENTS:
- Run at most two iterations responding to NEED_MODIFY feedback, stopping immediately on [APPROVED]
- ALWAYS use write_text_file tool to save complete app.py and templates/*.html files
- Do not add new data files or endpoints outside specification
- Preserve exact element IDs and data handling as described
- Maintain filename conventions exactly: app.py and templates/*.html files as output

Output: app.py and templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'code_feedback.md', 'source': 'CodeCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "CodeCritic": {
        "prompt": (
            """You are a Software Test Engineer specializing in Python web application verification and HTML template validation.

Your goal is to review the app.py backend and all HTML templates (*.html) to verify correctness, completeness, and conformance to design_spec.md. Provide gated feedback in code_feedback.md beginning with [APPROVED] or NEED_MODIFY, running at most two iterations.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Validate that app.py implements all specified routes, data file interactions, and navigation from design_spec.md
- Verify templates/*.html contain the exact page titles, element tags, and specified exact element IDs for each page and dynamic elements
- Check that dynamic element IDs (e.g. add-to-playlist-button-{song_id}) are present and correctly named
- Confirm data access aligns exactly with specified text file formats and fields for songs, artists, albums, genres, playlists, and playlist_songs

Review Checklist:
1. All 10 pages are implemented with correct titles and containers per design_spec.md
2. All functional buttons, inputs, dropdowns, tables have exact IDs as specified, including dynamic ones
3. Backend routes load and save data only via specified local text files with correct format, delimiter, and field order
4. Navigation buttons link to proper routes matching page flows
5. Error handling and edge cases are addressed without inventing new features

CRITICAL REQUIREMENTS:
- The first bytes of code_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY
- No prefixes, whitespace, or extra characters before these markers
- Use both write_text_file and validate_python_file tools for comprehensive verification
- Provide concrete, specific modification instructions if feedback is NEED_MODIFY
- Stop the refinement loop immediately after [APPROVED]

Output: code_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'validate_python_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'code_feedback.md'}],

    }

}

REVIEW_PROFILES = {
    'DesignGenerator': [
        ("DesignCritic", """Check design_spec.md for adherence to all specified pages, elements, navigation starting at dashboard, data format, and absence of authentication""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'AppGenerator': [
        ("CodeCritic", """Gate app.py and templates/*.html for conformance to design_spec.md including page elements, navigation, data file usage, and required exact element IDs""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    DesignGenerator = build_resilient_agent(
        agent_name="DesignGenerator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )
    DesignCritic = build_resilient_agent(
        agent_name="DesignCritic",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    MAX_ITERATIONS = 2
    for iteration in range(MAX_ITERATIONS):
        current_design = ""
        feedback_content = ""
        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            current_design = ""
        if iteration > 0:
            try:
                feedback_content = open("design_feedback.md").read()
            except FileNotFoundError:
                feedback_content = ""

        await execute(
            DesignGenerator,
            "Generate or revise design_spec.md for the MusicStreaming web app.\n"
            "Incorporate all corrections from feedback marked NEED_MODIFY if any.\n\n"
            f"=== Current design_spec.md ===\n{current_design}\n\n"
            f"=== DesignCritic Feedback ===\n{feedback_content}"
        )

        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            current_design = ""

        await execute(
            DesignCritic,
            "Review the latest design_spec.md for completeness, correctness, and adherence to user task.\n"
            "Write design_feedback.md starting exactly with [APPROVED] or NEED_MODIFY.\n\n"
            f"=== Latest design_spec.md ===\n{current_design}"
        )

        try:
            feedback_content = open("design_feedback.md").read()
        except FileNotFoundError:
            feedback_content = ""
        if feedback_content.startswith("[APPROVED]"):
            break
# Phase1_End
# Phase2_Start
import glob

async def implementation_and_verification_phase():
    AppGenerator = build_resilient_agent(
        agent_name="AppGenerator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=30
    )
    CodeCritic = build_resilient_agent(
        agent_name="CodeCritic",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=30
    )

    MAX_ITERATIONS = 2
    for iteration in range(MAX_ITERATIONS):
        app_content = ""
        templates_content = ""
        feedback_content = ""
        try:
            app_content = open("app.py").read()
        except FileNotFoundError:
            pass
        for template_path in sorted(glob.glob("templates/*.html")):
            try:
                templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
            except OSError:
                pass
        if iteration > 0:
            try:
                feedback_content = open("code_feedback.md").read()
            except FileNotFoundError:
                pass

        await execute(
            AppGenerator,
            "Create or revise the complete app.py and templates/*.html per design_spec.md and code_feedback.md.\n\n"
            f"=== Current app.py ===\n{app_content}\n\n"
            f"=== Current Templates ===\n{templates_content}\n\n"
            f"=== CodeCritic Feedback ===\n{feedback_content}"
        )

        try:
            app_content = open("app.py").read()
        except FileNotFoundError:
            app_content = ""
        templates_content = ""
        for template_path in sorted(glob.glob("templates/*.html")):
            try:
                templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
            except OSError:
                pass

        await execute(
            CodeCritic,
            "Review the latest app.py and templates/*.html against design_spec.md. "
            "Write code_feedback.md starting exactly with [APPROVED] or NEED_MODIFY including detailed evaluation of routes, navigation, element IDs, and data handling.\n\n"
            f"=== Latest app.py ===\n{app_content}\n\n"
            f"=== Latest Templates ===\n{templates_content}"
        )

        try:
            feedback_content = open("code_feedback.md").read()
        except FileNotFoundError:
            feedback_content = ""
        if feedback_content.startswith("[APPROVED]"):
            break
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
