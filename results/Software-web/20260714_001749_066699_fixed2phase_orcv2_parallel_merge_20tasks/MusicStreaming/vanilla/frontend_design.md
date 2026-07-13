# Frontend Design Specification for MusicStreaming Web Application

---

## Section 1: HTML Templates Overview

### 1. Dashboard Page
- Filename: `dashboard.html`
- Page Title: Music Streaming Dashboard
- Elements:
  - `dashboard-page` (Div) - Container for the main dashboard page.
  - `featured-songs` (Div) - Displays featured song recommendations.
  - `browse-songs-button` (Button) - Navigates to Song Catalog page.
  - `my-playlists-button` (Button) - Navigates to My Playlists page.
  - `trending-artists-button` (Button) - Navigates to Trending Artists page.

### 2. Song Catalog Page
- Filename: `catalog.html`
- Page Title: Song Catalog
- Elements:
  - `catalog-page` (Div) - Container for the song catalog page.
  - `search-input` (Input) - Text input to search songs by title, artist, or album.
  - `genre-filter` (Dropdown) - Dropdown for filtering songs by genre (e.g., Pop, Rock, Jazz).
  - `songs-grid` (Div) - Grid displaying song cards.
  - `add-to-playlist-button-{song_id}` (Button) - Button on each song card to add song to playlist. `{song_id}` placeholder to be replaced dynamically.

### 3. Song Details Page
- Filename: `song_details.html`
- Page Title: Song Details
- Elements:
  - `song-details-page` (Div) - Container for song detail page.
  - `song-title` (H1) - Displays the song title.
  - `artist-name` (Div) - Displays artist name with link to artist profile.
  - `album-name` (Div) - Displays album name.
  - `duration-display` (Div) - Displays song duration.
  - `play-button` (Button) - Button to play the song.

### 4. Playlist Page
- Filename: `playlists.html`
- Page Title: My Playlists
- Elements:
  - `playlists-page` (Div) - Container for playlists page.
  - `playlists-grid` (Div) - Grid displaying playlist cards.
  - `create-playlist-button` (Button) - Button to create a new playlist.
  - `view-playlist-button-{playlist_id}` (Button) - Button on each playlist card to view playlist details.
  - `back-to-dashboard` (Button) - Button to navigate back to Dashboard page.

### 5. Playlist Details Page
- Filename: `playlist_details.html`
- Page Title: Playlist Details
- Elements:
  - `playlist-details-page` (Div) - Container for playlist details.
  - `playlist-title` (H1) - Displays playlist title.
  - `playlist-description` (Div) - Displays playlist description.
  - `songs-in-playlist` (Table) - Table displaying songs with title, artist, duration, and remove option.
  - `remove-song-button-{song_id}` (Button) - Button to remove a specific song from playlist.
  - `delete-playlist-button` (Button) - Button to delete the entire playlist.

### 6. Create Playlist Page
- Filename: `create_playlist.html`
- Page Title: Create New Playlist
- Elements:
  - `create-playlist-page` (Div) - Container for create playlist page.
  - `playlist-name-input` (Input) - Input field for playlist name.
  - `playlist-description-input` (Textarea) - Textarea for playlist description.
  - `save-playlist-button` (Button) - Button to save and create the playlist.
  - `cancel-create-button` (Button) - Button to cancel creation and navigate back.

### 7. Album Browse Page
- Filename: `albums.html`
- Page Title: Albums
- Elements:
  - `albums-page` (Div) - Container for album browse page.
  - `albums-grid` (Div) - Grid displaying album cards.
  - `search-albums` (Input) - Input to search albums by title or artist.
  - `sort-albums` (Dropdown) - Dropdown for sorting albums (By Title, By Artist, By Year).
  - `view-album-button-{album_id}` (Button) - Button on each album card to view album details.

### 8. Album Details Page
- Filename: `album_details.html`
- Page Title: Album Details
- Elements:
  - `album-details-page` (Div) - Container for album details.
  - `album-title` (H1) - Displays album title.
  - `album-artist` (Div) - Displays album artist.
  - `album-year` (Div) - Displays album release year.
  - `album-songs-list` (Div) - List of songs in album.
  - `add-album-to-playlist-button` (Button) - Button to add all album songs to a playlist.

### 9. Artist Profile Page
- Filename: `artists.html`
- Page Title: Artist Profiles
- Elements:
  - `artists-page` (Div) - Container for artists page.
  - `artists-grid` (Div) - Grid displaying artist cards.
  - `search-artists` (Input) - Input to search artists by name.
  - `artists-sort` (Dropdown) - Dropdown to sort artists (By Name, By Genre).
  - `view-artist-button-{artist_id}` (Button) - Button on artist card to view artist profile.

### 10. Genre Exploration Page
- Filename: `genres.html`
- Page Title: Genre Exploration
- Elements:
  - `genres-page` (Div) - Container for genre exploration page.
  - `genres-list` (Div) - List of all available genres.
  - `select-genre` (Dropdown) - Dropdown to select a genre.
  - `genre-songs` (Div) - Display songs by selected genre.
  - `genre-artists` (Div) - Display artists by selected genre.
  - `back-to-dashboard` (Button) - Button to navigate back to Dashboard.

---

## Section 2: UI Components and Interactions

### Search Inputs
- `search-input` (catalog.html): Typing here filters songs dynamically by title, artist, or album.
- `search-albums` (albums.html): Filters albums by title or artist name.
- `search-artists` (artists.html): Filters artist cards by name.

### Dropdown Filters
- `genre-filter` (catalog.html): On selection, filters the displayed songs grid by the chosen genre.
- `sort-albums` (albums.html): Sorts albums grid by selected criteria (title, artist, or year).
- `artists-sort` (artists.html): Sorts artist cards by name or genre.
- `select-genre` (genres.html): Changes the content in `genre-songs` and `genre-artists` to correspond to selected genre.

### Buttons and Actions
- Navigation buttons (`browse-songs-button`, `my-playlists-button`, `trending-artists-button`, `back-to-dashboard`, etc.) trigger page navigation.
- Each `add-to-playlist-button-{song_id}` (catalog.html) opens a UI or triggers an action to add that specific song to a playlist.
- `create-playlist-button` (playlists.html) leads to `create_playlist.html`.
- `view-playlist-button-{playlist_id}` navigates to that playlist's details page.
- `remove-song-button-{song_id}` removes the song from the playlist in playlist_details.html.
- `delete-playlist-button` deletes the full playlist.
- `save-playlist-button` saves new playlist and redirects to playlists page.
- `cancel-create-button` navigates back from create playlist.
- `view-album-button-{album_id}` navigates to album_details.html.
- `add-album-to-playlist-button` allows adding all album songs to a playlist.
- `view-artist-button-{artist_id}` opens artist profile page.

### Dynamic Elements and Jinja2 Loops
- In `songs-grid` (catalog.html), loop over songs,
  - Each song card has IDs with `{song_id}` for unique controls.
- `playlists-grid` (playlists.html), loop over playlists,
  - IDs include `{playlist_id}` for individual cards and buttons.
- `songs-in-playlist` (playlist_details.html) table rows loop songs,
  - Each remove button uses `remove-song-button-{song_id}`.
- `albums-grid` (albums.html), loop albums,
  - Buttons include `view-album-button-{album_id}`.
- `album-songs-list` (album_details.html) lists songs dynamically.
- `artists-grid` (artists.html) loops artists,
  - Buttons `view-artist-button-{artist_id}`.
- `genres-list` (genres.html) lists all genres,
  - `select-genre` dropdown triggers genre-specific song and artist display.

### ID Conventions Summary
- Use hyphenated lowercase with descriptive names.
- For dynamic buttons, use format `base-id-{entity_id}` to uniquely identify elements.
  Example: `add-to-playlist-button-42` for song with ID 42.
- Container divs have simple IDs named after page or content.

---

This comprehensive frontend design allows the FrontendDeveloper to implement the entire UI with clarity on each element and interaction based solely on this document.
