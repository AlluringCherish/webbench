# MusicStreaming Application Requirements Analysis

## Overview
The MusicStreaming web application is developed using Python, with data storage in local text files. The application comprises 10 distinct pages starting at the Dashboard page. Key features include music search, playlist management, album and artist browsing, genre exploration, and statistics.

---

## Pages and UI Elements

### 1. Dashboard Page
- **Page Title**: Music Streaming Dashboard
- **Purpose**: Main hub displaying featured songs, trending artists, and quick navigation to functionalities.
- **Elements:**
  - `dashboard-page` (Div) - Container for the dashboard page
  - `featured-songs` (Div) - Featured song recommendations
  - `browse-songs-button` (Button) - Navigate to Song Catalog Page
  - `my-playlists-button` (Button) - Navigate to My Playlists Page
  - `trending-artists-button` (Button) - Navigate to Trending Artists Page

---

### 2. Song Catalog Page
- **Page Title**: Song Catalog
- **Purpose**: Display all available songs with search and filter.
- **Elements:**
  - `catalog-page` (Div) - Container
  - `search-input` (Input) - Search songs by title, artist, or album
  - `genre-filter` (Dropdown) - Filter by genre
  - `songs-grid` (Div) - Grid of song cards
  - `add-to-playlist-button-{song_id}` (Button) - Add song to playlist (per song)

---

### 3. Song Details Page
- **Page Title**: Song Details
- **Purpose**: Display detailed info about a specific song.
- **Elements:**
  - `song-details-page` (Div) - Container
  - `song-title` (H1) - Song title
  - `artist-name` (Div) - Artist name with link to artist profile
  - `album-name` (Div) - Album name
  - `duration-display` (Div) - Song duration
  - `play-button` (Button) - Play the song

---

### 4. Playlist Page
- **Page Title**: My Playlists
- **Purpose**: Display all user-created playlists.
- **Elements:**
  - `playlists-page` (Div) - Container
  - `playlists-grid` (Div) - Grid showing playlist cards
  - `create-playlist-button` (Button) - Create new playlist
  - `view-playlist-button-{playlist_id}` (Button) - View playlist details (per playlist)
  - `back-to-dashboard` (Button) - Navigate back to Dashboard

---

### 5. Playlist Details Page
- **Page Title**: Playlist Details
- **Purpose**: Display songs in a playlist with management options.
- **Elements:**
  - `playlist-details-page` (Div) - Container
  - `playlist-title` (H1) - Playlist title
  - `playlist-description` (Div) - Playlist description
  - `songs-in-playlist` (Table) - Table of songs (title, artist, duration, remove option)
  - `remove-song-button-{song_id}` (Button) - Remove song (per song)
  - `delete-playlist-button` (Button) - Delete entire playlist

---

### 6. Create Playlist Page
- **Page Title**: Create New Playlist
- **Purpose**: Create a new playlist with title and description.
- **Elements:**
  - `create-playlist-page` (Div) - Container
  - `playlist-name-input` (Input) - Playlist name input
  - `playlist-description-input` (Textarea) - Description input
  - `save-playlist-button` (Button) - Save new playlist
  - `cancel-create-button` (Button) - Cancel and go back

---

### 7. Album Browse Page
- **Page Title**: Albums
- **Purpose**: Browse all available albums.
- **Elements:**
  - `albums-page` (Div) - Container
  - `albums-grid` (Div) - Grid of album cards
  - `search-albums` (Input) - Search albums
  - `sort-albums` (Dropdown) - Sort albums (Title, Artist, Year)
  - `view-album-button-{album_id}` (Button) - View album details (per album)

---

### 8. Album Details Page
- **Page Title**: Album Details
- **Purpose**: View songs in a specific album.
- **Elements:**
  - `album-details-page` (Div) - Container
  - `album-title` (H1) - Album title
  - `album-artist` (Div) - Album artist
  - `album-year` (Div) - Release year
  - `album-songs-list` (Div) - List of songs in album
  - `add-album-to-playlist-button` (Button) - Add all album songs to playlist

---

### 9. Artist Profile Page
- **Page Title**: Artist Profiles
- **Purpose**: Display artists and their info.
- **Elements:**
  - `artists-page` (Div) - Container
  - `artists-grid` (Div) - Grid of artist cards
  - `search-artists` (Input) - Search artists
  - `artists-sort` (Dropdown) - Sort artists (Name, Genre)
  - `view-artist-button-{artist_id}` (Button) - View artist profile (per artist)

---

### 10. Genre Exploration Page
- **Page Title**: Genre Exploration
- **Purpose**: Explore music by genre.
- **Elements:**
  - `genres-page` (Div) - Container
  - `genres-list` (Div) - List all genres
  - `select-genre` (Dropdown) - Select genre
  - `genre-songs` (Div) - Songs in selected genre
  - `genre-artists` (Div) - Artists in selected genre
  - `back-to-dashboard` (Button) - Navigate back to Dashboard

---

## User Interaction and Navigation Flow
- Starting page: Dashboard Page (`dashboard-page` container).
- Navigation from Dashboard:
  - `browse-songs-button` → Song Catalog Page
  - `my-playlists-button` → Playlist Page
  - `trending-artists-button` → Artist Profile Page (assumed Trending Artists maps to Artist Profiles view)
- From Song Catalog:
  - Use search and `genre-filter` to find songs
  - `add-to-playlist-button-{song_id}` to add songs
  - Song selection navigates to Song Details Page
- From Playlist Page:
  - `create-playlist-button` to Create Playlist Page
  - `view-playlist-button-{playlist_id}` to Playlist Details Page
  - `back-to-dashboard` returns to Dashboard Page
- From Playlist Details Page:
  - `remove-song-button-{song_id}` removes song
  - `delete-playlist-button` deletes playlist
- From Create Playlist Page:
  - `save-playlist-button` saves and returns to Playlist Page (assumed)
  - `cancel-create-button` cancels and returns
- From Album Browse Page:
  - Search and sort albums
  - `view-album-button-{album_id}` to Album Details Page
- From Album Details Page:
  - `add-album-to-playlist-button` adds all album songs
- From Artist Profile Page:
  - `search-artists`, `artists-sort` for filtering
  - `view-artist-button-{artist_id}` to detailed artist profile
- From Genre Exploration Page:
  - `select-genre` to view genre songs and artists
  - `back-to-dashboard` returns to Dashboard


## Data Storage Formats
All data stored locally in 'data' directory in text files.

### 1. Songs Data - `songs.txt`
- Fields: `song_id`, `title`, `artist_id`, `album_id`, `genre`, `duration`, `release_date`, `play_count`
- Example:
  ```
  1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
  2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
  3|Shape of You|3|3|Pop|233|2017-01-06|4200000
  ```

### 2. Artists Data - `artists.txt`
- Fields: `artist_id`, `name`, `genre`, `country`, `formation_year`
- Example:
  ```
  1|Queen|Rock|United Kingdom|1970
  2|The Weeknd|Synth-Pop|Canada|2010
  3|Ed Sheeran|Pop|United Kingdom|2005
  ```

### 3. Albums Data - `albums.txt`
- Fields: `album_id`, `title`, `artist_id`, `release_year`, `total_songs`, `genre`
- Example:
  ```
  1|A Night at the Opera|1|1975|11|Rock
  2|After Hours|2|2019|14|Synth-Pop
  3|Divide|3|2017|12|Pop
  ```

### 4. Genres Data - `genres.txt`
- Fields: `genre_id`, `genre_name`, `description`
- Example:
  ```
  1|Rock|Guitar-driven music with strong beats and vocals
  2|Pop|Catchy mainstream music with broad appeal
  3|Hip-Hop|Rhythmic music with rap vocals and beat production
  ```

### 5. Playlists Data - `playlists.txt`
- Fields: `playlist_id`, `title`, `description`, `creation_date`, `total_songs`
- Example:
  ```
  1|Workout Mix|High energy songs for the gym|2025-01-15|25
  2|Chill Vibes|Relaxing music for study|2025-01-16|18
  3|Party Hits|Latest party tracks|2025-01-17|32
  ```

### 6. Playlist Songs Data - `playlist_songs.txt`
- Fields: `playlist_song_id`, `playlist_id`, `song_id`, `added_date`
- Example:
  ```
  1|1|2|2025-01-15
  2|1|3|2025-01-15
  3|2|1|2025-01-16
  ```

---

## Summary
This document captures a comprehensive view of the MusicStreaming application's page structures, UI elements with exact IDs, navigation flows with Dashboard as the starting page, and data storage formats as specified in local text files. It is intended to facilitate both design and development efforts.
