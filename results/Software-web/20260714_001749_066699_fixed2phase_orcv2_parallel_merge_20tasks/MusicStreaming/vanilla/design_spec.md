# Unified Design Specification for MusicStreaming Web Application

---

## Section 1: Flask Route Specifications and Corresponding Frontend Templates

### 1. Dashboard Page
- **Route:** `/dashboard`
- **Method:** GET
- **Description:** Main hub displaying featured songs and trending artists.
- **Response:** Render template `dashboard.html` with context:
  - `featured_songs`: List of featured songs.
  - `trending_artists`: List of trending artists.

- **Frontend (dashboard.html):**
  - Container Div ID: `dashboard-page`
  - Div ID `featured-songs`: displays featured song recommendations.
  - Buttons:
    - `browse-songs-button` navigates to Song Catalog page.
    - `my-playlists-button` navigates to Playlists page.
    - `trending-artists-button` navigates to Trending Artists page.

---

### 2. Song Catalog Page
- **Route:** `/songs`
- **Method:** GET
- **Query Parameters:** Optional `search` (string), `genre` (string).
- **Description:** List all songs with search and genre filtering.
- **Response:** Render template `catalog.html` (note: original backend call named `songs_catalog.html`, aligned to frontend) with:
  - `songs`: list of song records.
  - `genres`: list of all genres.

- **Frontend (catalog.html):**
  - Container Div ID: `catalog-page`
  - Search input ID: `search-input`
  - Dropdown filter ID: `genre-filter` filled from `genres`
  - Div ID `songs-grid`: grid to display songs
  - Each song card includes a button with ID format `add-to-playlist-button-{song_id}` for adding song to playlist

---

### 3. Song Details Page
- **Route:** `/songs/<int:song_id>`
- **Method:** GET
- **Description:** Show details of a song.
- **Response:** Render template `song_details.html` with:
  - `song`: song object
  - `artist`: artist object related to song
  - `album`: album object related to song

- **Frontend (song_details.html):**
  - Container Div ID: `song-details-page`
  - H1 ID: `song-title`
  - Div ID: `artist-name` (with link to artist profile)
  - Div ID: `album-name`
  - Div ID: `duration-display`
  - Button ID: `play-button`

---

### 4. Playlists Page (All Playlists)
- **Route:** `/playlists`
- **Method:** GET
- **Description:** Display all user playlists.
- **Response:** Render template `playlists.html` with:
  - `playlists`: list of playlists

- **Frontend (playlists.html):**
  - Container Div ID: `playlists-page`
  - Div ID: `playlists-grid` showing playlist cards
  - Button ID: `create-playlist-button` navigates to create playlist page
  - Each playlist card includes button `view-playlist-button-{playlist_id}`
  - Button ID: `back-to-dashboard` for navigation

---

### 5. Playlist Details Page
- **Route:** `/playlists/<int:playlist_id>`
- **Method:** GET
- **Description:** Show songs in a playlist with management options.
- **Response:** Render template `playlist_details.html` with:
  - `playlist`: playlist object
  - `songs`: list of songs in playlist

- **Frontend (playlist_details.html):**
  - Container Div ID: `playlist-details-page`
  - H1 ID: `playlist-title`
  - Div ID: `playlist-description`
  - Table ID: `songs-in-playlist` listing songs with columns title, artist, duration, with removal action
  - Remove button per song: `remove-song-button-{song_id}`
  - Button ID: `delete-playlist-button` for playlist deletion

---

### 6. Create Playlist Page
- **Route:** `/playlists/create`
- **Methods:** GET, POST
  - GET returns create playlist form
  - POST accepts `title` and `description`, creates playlist, redirects to `/playlists`

- **Frontend (create_playlist.html):**
  - Container Div ID: `create-playlist-page`
  - Input ID: `playlist-name-input`
  - Textarea ID: `playlist-description-input`
  - Button ID: `save-playlist-button` to save playlist
  - Button ID: `cancel-create-button` to cancel and navigate back

---

### 7. Album Browse Page
- **Route:** `/albums`
- **Method:** GET
- **Query Parameters:** Optional `search` (album title or artist), `sort` (criteria: title, artist, year)
- **Response:** Render template `albums.html` with:
  - `albums`: list of albums

- **Frontend (albums.html):**
  - Container Div ID: `albums-page`
  - Div ID: `albums-grid` shows album cards
  - Input ID: `search-albums` for searching albums
  - Dropdown ID: `sort-albums` for sorting
  - Each album card has button `view-album-button-{album_id}`

---

### 8. Album Details Page
- **Route:** `/albums/<int:album_id>`
- **Method:** GET
- **Description:** Show album details and songs.
- **Response:** Render template `album_details.html` with:
  - `album`: album object
  - `artist`: artist object for album
  - `songs`: list of songs in the album

- **Frontend (album_details.html):**
  - Container Div ID: `album-details-page`
  - H1 ID: `album-title`
  - Div IDs: `album-artist`, `album-year`
  - Div ID: `album-songs-list` for list of album songs
  - Button ID: `add-album-to-playlist-button` to add all album songs

---

### 9. Artist Listing Page
- **Route:** `/artists`
- **Method:** GET
- **Query Parameters:** Optional `search` (artist name), `sort` (name or genre)
- **Response:** Render template `artists.html` with:
  - `artists`: list of artist objects

- **Frontend (artists.html):**
  - Container Div ID: `artists-page`
  - Div ID: `artists-grid` shows artist cards
  - Input ID: `search-artists`
  - Dropdown ID: `artists-sort`
  - Buttons `view-artist-button-{artist_id}` on each artist card

---

### 10. Individual Artist Profile Page
- **Route:** `/artists/<int:artist_id>`
- **Method:** GET
- **Description:** Show artist profile, songs, and albums.
- **Response:** Render template `artist_profile.html` with:
  - `artist`: artist object
  - `songs`: songs by artist
  - `albums`: albums by artist

- **Frontend:** Template elements not explicitly detailed beyond route; assume consistent structure referencing `artist`, `songs`, and `albums` variables.

---

### 11. Genre Exploration Page
- **Route:** `/genres`
- **Method:** GET
- **Query Parameters:** Optional `genre_id`
- **Response:** Render template `genres.html` with:
  - `genres`: all genres
  - If `genre_id` provided:
    - `genre`: selected genre object
    - `songs`: songs filtered by genre
    - `artists`: artists filtered by genre

- **Frontend (genres.html):**
  - Container Div ID: `genres-page`
  - Div ID: `genres-list`
  - Dropdown ID: `select-genre` to pick genre
  - Div ID: `genre-songs` for songs in selected genre
  - Div ID: `genre-artists` for artists in selected genre
  - Button ID: `back-to-dashboard`

---

## Section 2: API Endpoints

### Add Song to Playlist
- **Route:** `/playlists/<int:playlist_id>/add_song`
- **Method:** POST
- **Request:** JSON with `song_id`
- **Response:** JSON success and updated playlist info

### Remove Song from Playlist
- **Route:** `/playlists/<int:playlist_id>/remove_song`
- **Method:** POST
- **Request:** JSON with `song_id`
- **Response:** JSON success/fail and updated playlist info

### Delete Playlist
- **Route:** `/playlists/<int:playlist_id>/delete`
- **Method:** POST
- **Response:** JSON deletion status

### Increment Song Play Count
- **Route:** `/songs/<int:song_id>/play`
- **Method:** POST
- **Response:** JSON with updated play_count

---

## Section 3: Data File Schemas

Data files are stored in directory `data/` with the following schemas:

### 1. Songs Data (`songs.txt`)
```
song_id|title|artist_id|album_id|genre|duration|release_date|play_count
```
- Example:
```
1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
```

### 2. Artists Data (`artists.txt`)
```
artist_id|name|genre|country|formation_year
```
- Example:
```
1|Queen|Rock|United Kingdom|1970
```

### 3. Albums Data (`albums.txt`)
```
album_id|title|artist_id|release_year|total_songs|genre
```
- Example:
```
1|A Night at the Opera|1|1975|11|Rock
```

### 4. Genres Data (`genres.txt`)
```
genre_id|genre_name|description
```
- Example:
```
1|Rock|Guitar-driven music with strong beats and vocals
```

### 5. Playlists Data (`playlists.txt`)
```
playlist_id|title|description|creation_date|total_songs
```
- Example:
```
1|Workout Mix|High energy songs for the gym|2025-01-15|25
```

### 6. Playlist Songs Data (`playlist_songs.txt`)
```
playlist_song_id|playlist_id|song_id|added_date
```
- Example:
```
1|1|2|2025-01-15
```

---

## Section 4: Data Access and Integration Notes

- Files read and parsed into list of dicts keyed by schema fields.
- Relationships managed by `artist_id`, `album_id`, `genre`, etc., to join data across files.
- Searches and filters are case-insensitive substring matches.
- Playlists are updated by modifying `playlists.txt` and `playlist_songs.txt`.
- Incrementing play count updates `songs.txt` directly.
- Pagination or caching not specified.

---

## Section 5: Frontend UI Elements and Interaction Summary

- UI elements have consistent IDs matching backend context variable uses and routes.
- Dynamic element IDs for items (songs, playlists, albums, artists) use format: `base-id-{entity_id}`.
- Search inputs, filters, and sorting dropdowns map to query parameters on backend routes.
- Buttons correspond to navigation or API calls as documented.

---

This unified design_spec.md document merges backend routes, data schemas, and frontend template specifications providing clear, consistent references for both backend Flask developers and frontend UI developers. Developers can implement the MusicStreaming application end-to-end without discrepancies or missing elements.