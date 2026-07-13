# MusicStreaming Web Application Detailed Design Specification

## Section 1: Page and UI Element Specifications

The MusicStreaming web application consists of the following 10 pages. Each page’s main container div has a unique ID and includes the specified UI elements with unique IDs where applicable. Navigation buttons and their target pages are also detailed, starting from the Dashboard page.

---

### 1. Dashboard Page
- **Page Title**: Music Streaming Dashboard
- **Container Div ID**: dashboard-page
- **Overview**: Main hub showing featured songs, trending artists, and navigation to core functionalities.
- **UI Elements:**
  - Div: featured-songs
  - Button: browse-songs-button (navigates to Song Catalog page)
  - Button: my-playlists-button (navigates to Playlist page)
  - Button: trending-artists-button (navigates to Artist Profile page)
  - Button: genres-exploration-button (navigates to Genre Exploration page)  

---

### 2. Song Catalog Page
- **Page Title**: Song Catalog
- **Container Div ID**: catalog-page
- **Overview**: Displays all available songs with search and genre filter options.
- **UI Elements:**
  - Input: search-input (search songs by title, artist, album)
  - Dropdown: genre-filter (genres e.g., Pop, Rock, Hip-Hop, Jazz, Classical)
  - Div (grid): songs-grid (song cards with cover art, title, artist, and duration)
  - Button: add-to-playlist-button-{song_id} (each song card has this for adding song to playlists)
  - Button: back-to-dashboard (returns to Dashboard page)

---

### 3. Song Details Page
- **Page Title**: Song Details
- **Container Div ID**: song-details-page
- **Overview**: Detailed information about a selected song.
- **UI Elements:**
  - H1: song-title
  - Div: artist-name (clickable link navigating to Artist Profile page)
  - Div: album-name
  - Div: duration-display
  - Button: play-button (to play the song)
  - Button: back-to-catalog (returns to Song Catalog page)

---

### 4. Playlist Page
- **Page Title**: My Playlists
- **Container Div ID**: playlists-page
- **Overview**: Displays all user-created playlists.
- **UI Elements:**
  - Div (grid): playlists-grid (playlist cards showing cover, title, song count)
  - Button: create-playlist-button (navigates to Create Playlist page)
  - Button: view-playlist-button-{playlist_id} (view details of specific playlist)
  - Button: back-to-dashboard (returns to Dashboard page)

---

### 5. Playlist Details Page
- **Page Title**: Playlist Details
- **Container Div ID**: playlist-details-page
- **Overview**: Displays songs within a selected playlist and options to manage it.
- **UI Elements:**
  - H1: playlist-title
  - Div: playlist-description
  - Table: songs-in-playlist (columns: title, artist, duration, remove button)
  - Button: remove-song-button-{song_id} (removes song from playlist)
  - Button: delete-playlist-button (deletes the playlist)
  - Button: back-to-playlists (returns to Playlist page)

---

### 6. Create Playlist Page
- **Page Title**: Create New Playlist
- **Container Div ID**: create-playlist-page
- **Overview**: Form for creating a new playlist.
- **UI Elements:**
  - Input: playlist-name-input
  - Textarea: playlist-description-input
  - Button: save-playlist-button (saves and creates playlist)
  - Button: cancel-create-button (cancels and returns to Playlist page)

---

### 7. Album Browse Page
- **Page Title**: Albums
- **Container Div ID**: albums-page
- **Overview**: Displays all available albums with browsing, searching, and sorting.
- **UI Elements:**
  - Input: search-albums (search albums by title or artist)
  - Dropdown: sort-albums (by Title, by Artist, by Year)
  - Div (grid): albums-grid (album cards with cover, title, artist, year)
  - Button: view-album-button-{album_id} (view album details)
  - Button: back-to-dashboard (returns to Dashboard page)

---

### 8. Album Details Page
- **Page Title**: Album Details
- **Container Div ID**: album-details-page
- **Overview**: Shows details and songs of a specific album.
- **UI Elements:**
  - H1: album-title
  - Div: album-artist
  - Div: album-year
  - Div: album-songs-list (list of songs in album)
  - Button: add-album-to-playlist-button (adds all album songs to a playlist)
  - Button: back-to-albums (returns to Album Browse page)

---

### 9. Artist Profile Page
- **Page Title**: Artist Profiles
- **Container Div ID**: artists-page
- **Overview**: Displays artists with search and sorting capabilities.
- **UI Elements:**
  - Input: search-artists (search artists by name)
  - Dropdown: artists-sort (by Name, by Genre)
  - Div (grid): artists-grid (artist cards with photo, name, genre)
  - Button: view-artist-button-{artist_id} (view artist profile)
  - Button: back-to-dashboard (returns to Dashboard page)

---

### 10. Genre Exploration Page
- **Page Title**: Genre Exploration
- **Container Div ID**: genres-page
- **Overview**: Explore music by genres including featured songs and artists.
- **UI Elements:**
  - Div: genres-list (list of all genres)
  - Dropdown: select-genre (select specific genre to view)
  - Div: genre-songs (songs under selected genre)
  - Div: genre-artists (artists under selected genre)
  - Button: back-to-dashboard (returns to Dashboard page)

---

## Navigation Flow

- The starting page is always the Dashboard Page.
- From Dashboard, users navigate to Song Catalog, Playlists, Artist Profiles, or Genre Exploration.
- From Song Catalog, users can view Song Details or return to Dashboard.
- From Song Details, users return to Song Catalog.
- From Playlists, users create or view Playlist Details or return to Dashboard.
- From Playlist Details, users return to Playlist Page.
- From Create Playlist, users return to Playlist Page.
- From Album Browse, users view Album Details or return to Dashboard.
- From Album Details, users return to Album Browse.
- From Artist Profiles, users view specific Artist details or return to Dashboard.
- From Genre Exploration, users return to Dashboard.


## Section 2: Data Storage Formats

Data is stored locally within the "data" directory in plain text files, format described here:

---

### 1. Songs Data (`songs.txt`)
- Fields (pipe `|` separated):
  - song_id
  - title
  - artist_id
  - album_id
  - genre
  - duration (in seconds)
  - release_date (YYYY-MM-DD)
  - play_count
- Example row:
  `1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000`

---

### 2. Artists Data (`artists.txt`)
- Fields:
  - artist_id
  - name
  - genre
  - country
  - formation_year
- Example row:
  `1|Queen|Rock|United Kingdom|1970`

---

### 3. Albums Data (`albums.txt`)
- Fields:
  - album_id
  - title
  - artist_id
  - release_year
  - total_songs
  - genre
- Example row:
  `1|A Night at the Opera|1|1975|11|Rock`

---

### 4. Genres Data (`genres.txt`)
- Fields:
  - genre_id
  - genre_name
  - description
- Example row:
  `1|Rock|Guitar-driven music with strong beats and vocals`

---

### 5. Playlists Data (`playlists.txt`)
- Fields:
  - playlist_id
  - title
  - description
  - creation_date (YYYY-MM-DD)
  - total_songs
- Example row:
  `1|Workout Mix|High energy songs for the gym|2025-01-15|25`

---

### 6. Playlist Songs Data (`playlist_songs.txt`)
- Fields:
  - playlist_song_id
  - playlist_id
  - song_id
  - added_date (YYYY-MM-DD)
- Example row:
  `1|1|2|2025-01-15`

---

## End of Specification
