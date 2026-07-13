# MusicStreaming Application - Unified Design Specification

---

## 1. URL Routing and Navigation

| Route                                      | HTTP Method | Template               | Description / Notes                                   |
|--------------------------------------------|-------------|------------------------|-----------------------------------------------------|
| `/`                                        | GET         | `dashboard.html`       | Dashboard page, app entry point.                     |
| `/dashboard`                               | GET         | `dashboard.html`       | Alias route for dashboard (recommended to redirect to `/`). |
| `/songs`                                   | GET         | `song_catalog.html`    | Song Catalog with filtering and search.             |
| `/songs/<int:song_id>`                     | GET         | `song_details.html`    | Song Details page.                                   |
| `/playlists`                               | GET         | `playlists.html`       | My Playlists page.                                   |
| `/playlists/create`                        | GET, POST   | `create_playlist.html` | Create Playlist page (POST creates playlist).       |
| `/playlists/<int:playlist_id>`             | GET         | `playlist_details.html`| Playlist Details page.                               |
| `/playlists/<int:playlist_id>/delete`     | POST        | N/A                    | Delete playlist action triggered by button.         |
| `/playlists/<int:playlist_id>/remove_song/<int:song_id>` | POST | N/A                  | Remove song from playlist action triggered by button.
|
| `/albums`                                  | GET         | `albums.html`          | Album Browse page with filtering and sorting.       |
| `/albums/<int:album_id>`                   | GET         | `album_details.html`   | Album Details page.                                 |
| `/artists`                                 | GET         | `artists.html`         | Artist Profile page (list of artists).               |
| `/artists/<int:artist_id>`                 | GET         | TBD (not specified)    | Specific Artist Profile page (optional extension).  |
| `/genres`                                  | GET         | `genres.html`          | Genre Exploration page.                              |


### Navigation Button Mappings

- Dashboard (`/`):
  - `browse-songs-button` -> `/songs`
  - `my-playlists-button` -> `/playlists`
  - `trending-artists-button` -> `/artists`

- Song Catalog (`/songs`):
  - `add-to-playlist-button-{song_id}`: Opens modal or inline UI to select playlist.
  - Clicking song title navigates to `/songs/<song_id>`.
  - Clicking artist name navigates to `/artists` or `/artists/<artist_id>` if extended.

- Playlists (`/playlists`):
  - `create-playlist-button` -> `/playlists/create`
  - `view-playlist-button-{playlist_id}` -> `/playlists/<playlist_id>`
  - `back-to-dashboard` -> `/`

- Playlist Details (`/playlists/<playlist_id>`):
  - `remove-song-button-{song_id}` posts to `/playlists/<playlist_id>/remove_song/<song_id>` to remove song.
  - `delete-playlist-button` posts to `/playlists/<playlist_id>/delete` to delete playlist.

- Create Playlist (`/playlists/create`):
  - `save-playlist-button` posts form to `/playlists/create`.
  - `cancel-create-button` redirects to `/playlists`.

- Albums (`/albums`):
  - `view-album-button-{album_id}` -> `/albums/<album_id>`

- Album Details (`/albums/<album_id>`):
  - `add-album-to-playlist-button` triggers add all album songs to playlist action.

- Artists (`/artists`):
  - `view-artist-button-{artist_id}` -> `/artists/<artist_id>` (if implemented).

- Genre Exploration (`/genres`):
  - `select-genre` dropdown filters `genre-songs` and `genre-artists`.
  - `back-to-dashboard` button -> `/`

---

## 2. Detailed Page Specifications and Element IDs

---

### 1. Dashboard Page (`/`)
- **Page Title:** Music Streaming Dashboard
- **Container:** `dashboard-page` (Div)

**UI Elements:**
- `featured-songs` (Div): Displays featured songs from `songs.txt` filtered by top play counts.
- Buttons:
  - `browse-songs-button` (Button): Navigate to `/songs`.
  - `my-playlists-button` (Button): Navigate to `/playlists`.
  - `trending-artists-button` (Button): Navigate to `/artists` with trending artists.

---

### 2. Song Catalog Page (`/songs`)
- **Page Title:** Song Catalog
- **Container:** `catalog-page` (Div)

**UI Elements:**
- `search-input` (Input): Text input for searching songs by title, artist, or album.
- `genre-filter` (Dropdown): Populate from `genres.txt` for genre filter.
- `songs-grid` (Div): Grid of song cards.
  - Each card shows cover art (from album or default), title, artist name, duration.
  - `add-to-playlist-button-{song_id}` (Button): Add song to playlist.

**Interactions:**
- Search or select genre filters songs.
- `add-to-playlist-button-{song_id}` triggers playlist selection modal inline (UI not detailed).

**Data Access:**
- Reads `songs.txt`, `artists.txt`, `albums.txt`, `genres.txt`.

---

### 3. Song Details Page (`/songs/<int:song_id>`)
- **Page Title:** Song Details
- **Container:** `song-details-page` (Div)

**UI Elements:**
- `song-title` (H1): Song title
- `artist-name` (Div): Artist name, clickable to `/artists` or `/artists/<artist_id>` (extended)
- `album-name` (Div): Album name
- `duration-display` (Div): Duration formatted mm:ss
- `play-button` (Button): Plays song (frontend only)

**Data Access:**
- Reads `songs.txt`, `artists.txt`, `albums.txt` filtering by song_id.

---

### 4. Playlist Page (`/playlists`)
- **Page Title:** My Playlists
- **Container:** `playlists-page` (Div)

**UI Elements:**
- `playlists-grid` (Div): Displays playlists cards with cover (optional), title, song count.
- Buttons:
  - `create-playlist-button` (Button): Navigates to `/playlists/create`.
  - `view-playlist-button-{playlist_id}` (Button): Navigates to `/playlists/<playlist_id>`.
  - `back-to-dashboard` (Button): Navigates to `/`.

**Data Access:**
- Reads `playlists.txt` and `playlist_songs.txt`.

---

### 5. Playlist Details Page (`/playlists/<int:playlist_id>`)
- **Page Title:** Playlist Details
- **Container:** `playlist-details-page` (Div)

**UI Elements:**
- `playlist-title` (H1): Playlist title
- `playlist-description` (Div): Playlist description
- `songs-in-playlist` (Table): Columns for song title, artist, duration, with remove button
- `remove-song-button-{song_id}` (Button): Removes song
- `delete-playlist-button` (Button): Deletes playlist

**Interactions:**
- Remove song and delete playlist actions via POST requests to respective routes.

**Data Access:**
- Reads `playlists.txt`, `playlist_songs.txt`, `songs.txt`, `artists.txt`.

---

### 6. Create Playlist Page (`/playlists/create`)
- **Page Title:** Create New Playlist
- **Container:** `create-playlist-page` (Div)

**UI Elements:**
- `playlist-name-input` (Input): Playlist name
- `playlist-description-input` (Textarea): Playlist description
- `save-playlist-button` (Button): Submit create playlist
- `cancel-create-button` (Button): Cancel creation and navigate back

**Interactions:**
- POSTs to create playlist on save; cancel navigates back.

---

### 7. Album Browse Page (`/albums`)
- **Page Title:** Albums
- **Container:** `albums-page` (Div)

**UI Elements:**
- `albums-grid` (Div): Album cards with cover, title, artist, year
- `search-albums` (Input): Search albums
- `sort-albums` (Dropdown): Sort by Title, Artist, Year
- `view-album-button-{album_id}` (Button): View album details

**Data Access:**
- Reads `albums.txt`, `artists.txt`.

---

### 8. Album Details Page (`/albums/<int:album_id>`)
- **Page Title:** Album Details
- **Container:** `album-details-page` (Div)

**UI Elements:**
- `album-title` (H1)
- `album-artist` (Div)
- `album-year` (Div)
- `album-songs-list` (Div): List songs with titles and durations
- `add-album-to-playlist-button` (Button): Add all album songs to playlist

**Data Access:**
- Reads `albums.txt`, `songs.txt` (filtered by album_id), `artists.txt`.

---

### 9. Artist Profile Page (`/artists`)
- **Page Title:** Artist Profiles
- **Container:** `artists-page` (Div)

**UI Elements:**
- `artists-grid` (Div): Artist cards with photo (optional), name, genre
- `search-artists` (Input): Search by artist name
- `artists-sort` (Dropdown): Sort by Name, Genre
- `view-artist-button-{artist_id}` (Button): View artist profile (optional `/artists/<artist_id>`)

**Data Access:**
- Reads `artists.txt`.

---

### 10. Genre Exploration Page (`/genres`)
- **Page Title:** Genre Exploration
- **Container:** `genres-page` (Div)

**UI Elements:**
- `genres-list` (Div): Lists genre names from `genres.txt`
- `select-genre` (Dropdown): Select genre triggers filtered views
- `genre-songs` (Div): Shows songs filtered by genre
- `genre-artists` (Div): Shows artists filtered by genre
- `back-to-dashboard` (Button): Navigate to `/`

**Data Access:**
- Reads `genres.txt`, `songs.txt`, `artists.txt` filtered by genre.

---

## 3. Data Storage and File Handling

### Data Folder: `data/`

### Data Files and Formats

| File               | Description                                 | Format / Fields
|--------------------|---------------------------------------------|-----------------------------|
| `songs.txt`        | Songs metadata                              | song_id|title|artist_id|album_id|genre|duration|release_date|play_count |
| `artists.txt`      | Artist metadata                             | artist_id|name|genre|country|formation_year |
| `albums.txt`       | Album metadata                              | album_id|title|artist_id|release_year|total_songs|genre |
| `genres.txt`       | Genres list and info                        | genre_id|genre_name|description |
| `playlists.txt`    | Playlists metadata                          | playlist_id|title|description|creation_date|total_songs |
| `playlist_songs.txt`| Playlist to songs mapping                   | playlist_song_id|playlist_id|song_id|added_date |

### Data Access Notes
- All pages that display song info use `songs.txt` 
- Artist and album info resolved via `artists.txt` and `albums.txt`
- Filtering by genre or search is handled by UI controls and backend
- Creating, updating, removing playlists and songs updates `playlists.txt` and `playlist_songs.txt`

---

# Appendix: Element ID Naming Conventions

- Use exact IDs as specified for buttons and containers.
- Entity-specific buttons include unique ids: e.g., `add-to-playlist-button-{song_id}`, `view-playlist-button-{playlist_id}`, `remove-song-button-{song_id}`.
- Inputs and selectors have descriptive IDs like `search-input`, `genre-filter`, `select-genre`.

---

This unified design specification fully satisfies the MusicStreaming application's requirements, ensuring clarity and completeness in UI element definitions, navigation flows, backend routes, and local file data management.