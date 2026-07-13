# Backend Design Document for MusicStreaming Application

---

## Section 1: Flask Route Specifications

### 1. Dashboard Page
- **Route:** `/dashboard`
- **Method:** GET
- **Description:** Serves the main dashboard page.
- **Response:** Render template `dashboard.html` with context:
  - `featured_songs`: List of top featured songs (based on play_count, or curated list).
  - `trending_artists`: List of artists trending (based on aggregate song play counts or a metric).

### 2. Song Catalog Page
- **Route:** `/songs`
- **Method:** GET
- **Query Parameters:**
  - `search` (optional): string to search by song title, artist name, or album title.
  - `genre` (optional): Filter songs by genre.
- **Description:** Display all available songs with optional search and genre filter.
- **Response:** Render template `songs_catalog.html` with context:
  - `songs`: List of song records matching search and filter.
  - `genres`: Full list of genres for the dropdown filter.

### 3. Song Details Page
- **Route:** `/songs/<int:song_id>`
- **Method:** GET
- **Description:** Show detailed info for a specific song.
- **Response:** Render template `song_details.html` with:
  - `song`: Song object (with artist, album, duration, etc).
  - `artist`: Artist object related to the song.
  - `album`: Album object related to the song.

### 4. Playlist Page (List of Playlists)
- **Route:** `/playlists`
- **Method:** GET
- **Description:** Show all user-created playlists.
- **Response:** Render template `playlists.html` with:
  - `playlists`: List of playlist objects.

### 5. Playlist Details Page
- **Route:** `/playlists/<int:playlist_id>`
- **Method:** GET
- **Description:** Display songs in a playlist and management options.
- **Response:** Render template `playlist_details.html` with:
  - `playlist`: Playlist object.
  - `songs`: List of songs in the playlist.

### 6. Create Playlist Page
- **Route:** `/playlists/create`
- **Methods:** GET, POST
- - **GET:** Return the create new playlist form.
- - **POST:** Receive `title`, `description`, create new playlist, and redirect to `/playlists`.

### 7. Album Browse Page
- **Route:** `/albums`
- **Method:** GET
- **Query Parameters:**
  - `search` (optional): Search by album title or artist name.
  - `sort` (optional): Sorting criteria - `title`, `artist`, or `year`.
- **Response:** Render template `albums.html` with:
  - `albums`: List of matched album objects.

### 8. Album Details Page
- **Route:** `/albums/<int:album_id>`
- **Method:** GET
- **Description:** Show all songs in the album.
- **Response:** Render template `album_details.html` with:
  - `album`: Album object.
  - `artist`: Artist object for album artist.
  - `songs`: List of songs in the album.

### 9. Artist Profile Page
- **Route:** `/artists`
- **Method:** GET
- **Query Parameters:**
  - `search` (optional): search artist by name.
  - `sort` (optional): sort artists `name` or `genre`.
- **Response:** Render template `artists.html` with:
  - `artists`: List of artist objects matching criteria.

### 10. Individual Artist Profile
- **Route:** `/artists/<int:artist_id>`
- **Method:** GET
- **Description:** Show artist profile details and songs.
- **Response:** Render template `artist_profile.html` with:
  - `artist`: Artist object.
  - `songs`: Songs by this artist.
  - `albums`: Albums by this artist.

### 11. Genre Exploration Page
- **Route:** `/genres`
- **Method:** GET
- **Query Parameters:**
  - `genre_id` (optional): Show details for selected genre.
- **Response:** Render template `genres.html` with:
  - `genres`: List of all genres.
  - If `genre_id` provided:
    - `genre`: Selected genre object.
    - `songs`: Songs filtered by genre.
    - `artists`: Artists filtered by genre.

### 12. API: Add Song to Playlist
- **Route:** `/playlists/<int:playlist_id>/add_song`
- **Method:** POST
- **Request Data (JSON):**
  - `song_id`: ID of the song to add
- **Response:** JSON with success status and updated playlist info.

### 13. API: Remove Song from Playlist
- **Route:** `/playlists/<int:playlist_id>/remove_song`
- **Method:** POST
- **Request Data (JSON):**
  - `song_id`: ID of song to remove
- **Response:** JSON success/fail and updated playlist info.

### 14. API: Delete Playlist
- **Route:** `/playlists/<int:playlist_id>/delete`
- **Method:** POST
- **Response:** JSON status of deletion success.

### 15. API: Increment Play Count
- **Route:** `/songs/<int:song_id>/play`
- **Method:** POST
- **Query:** Increment the play count of a song.
- **Response:** JSON with new play_count.

---

## Section 2: Data File Schemas and Access

### 1. Songs Data (`data/songs.txt`)
- **Schema:**
  ```
  song_id|title|artist_id|album_id|genre|duration|release_date|play_count
  ```
- **Parsing:**
  - Split each line by `|`.
  - Cast `song_id`, `artist_id`, `album_id`, and `play_count` to int.
  - `duration` as int (seconds).
  - `release_date` as string (YYYY-MM-DD).
- **Example Row:**
  `1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000`

- **Usage:**
  - Filtering songs by genre or search by title/artist/album implemented by cross-referencing artist and album files.
  - Aggregation of play_count for trending.

### 2. Artists Data (`data/artists.txt`)
- **Schema:**
  ```
  artist_id|name|genre|country|formation_year
  ```
- **Parsing:**
  - `artist_id`, `formation_year` as int.
  - Others as strings.
- **Example:**
  `1|Queen|Rock|United Kingdom|1970`

### 3. Albums Data (`data/albums.txt`)
- **Schema:**
  ```
  album_id|title|artist_id|release_year|total_songs|genre
  ```
- **Parsing:**
  - `album_id`, `artist_id`, `release_year`, `total_songs` as int.
  - Others strings.
- **Example:**
  `1|A Night at the Opera|1|1975|11|Rock`

### 4. Genres Data (`data/genres.txt`)
- **Schema:**
  ```
  genre_id|genre_name|description
  ```
- **Parsing:**
  - `genre_id` as int.
  - Others as string.
- **Example:**
  `1|Rock|Guitar-driven music with strong beats and vocals`

### 5. Playlists Data (`data/playlists.txt`)
- **Schema:**
  ```
  playlist_id|title|description|creation_date|total_songs
  ```
- **Parsing:**
  - `playlist_id`, `total_songs` as int.
  - Date as string (YYYY-MM-DD).
- **Example:**
  `1|Workout Mix|High energy songs for the gym|2025-01-15|25`

### 6. Playlist Songs Data (`data/playlist_songs.txt`)
- **Schema:**
  ```
  playlist_song_id|playlist_id|song_id|added_date
  ```
- **Parsing:**
  - `playlist_song_id`, `playlist_id`, `song_id` as int.
  - Date as string.
- **Example:**
  `1|1|2|2025-01-15`

---

### Data Access Patterns
- Use Python file IO to read the text files.
- Parse each file to list of dictionaries keyed by field names.
- Relations like artist_id or album_id used to join data across different files.
- Searching requires:
  - Loading songs, artists, albums.
  - Filtering on song title, artist name, or album title.
- Filtering genres uses the genre field in songs.
- Playlist management involves updating and writing back `playlists.txt` and `playlist_songs.txt`.
- Play count increments update the line for the song in `songs.txt`.

---

## Section 3: API and Integration Details

### Add Song to Playlist
- Read current `playlists.txt` and `playlist_songs.txt`.
- Generate a new `playlist_song_id` (max existing +1).
- Append new entry in `playlist_songs.txt`.
- Increment `total_songs` in `playlists.txt` for that playlist.
- Return success JSON.

### Remove Song from Playlist
- Read and filter out the song entry in `playlist_songs.txt`.
- Decrement `total_songs` in `playlists.txt`.
- Save changes to files.
- Return JSON status.

### Delete Playlist
- Remove playlist entry from `playlists.txt`.
- Remove all entries belonging to playlist from `playlist_songs.txt`.
- Save files.
- Return success JSON.

### Increment Song Play Count
- Locate song by `song_id` in `songs.txt`.
- Increment play_count by 1.
- Write back updated line.
- Return updated play_count as JSON.

### Navigation Handling
- Routing handled by Flask.
- Query parameters used for search/filter sorting.

### Sorting & Filtering Parameters
- Sorting albums by `title`, `artist`, or `year`.
- Sorting artists by `name` or `genre`.
- Filtering songs by `genre`.
- Searching via substring case-insensitive match.

---

This document provides backend functional details and data schema needed for a Flask backend developer to implement the MusicStreaming application from local text files.

