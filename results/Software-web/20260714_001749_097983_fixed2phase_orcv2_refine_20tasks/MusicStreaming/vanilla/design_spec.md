# MusicStreaming Web Application Design Specification

---

## Section 1: Page and UI Element Specifications

### 1. Dashboard Page
- **Page Title**: Music Streaming Dashboard
- **Container Div ID**: dashboard-page
- **UI Elements**:
  - featured-songs (Div): Display of featured song recommendations.
  - browse-songs-button (Button): Navigation to Song Catalog page.
  - my-playlists-button (Button): Navigation to My Playlists page.
  - trending-artists-button (Button): Navigation to Trending Artists page.

### 2. Song Catalog Page
- **Page Title**: Song Catalog
- **Container Div ID**: catalog-page
- **UI Elements**:
  - search-input (Input): Search songs by title, artist, or album.
  - genre-filter (Dropdown): Filter songs by genre (Pop, Rock, Hip-Hop, Jazz, Classical, etc.).
  - songs-grid (Div): Grid displaying song cards (cover art, title, artist, duration).
  - add-to-playlist-button-{song_id} (Button): Add song to playlist (individual per song).

### 3. Song Details Page
- **Page Title**: Song Details
- **Container Div ID**: song-details-page
- **UI Elements**:
  - song-title (H1): Song title display.
  - artist-name (Div): Artist name with link to artist profile.
  - album-name (Div): Album name display.
  - duration-display (Div): Song duration.
  - play-button (Button): Play the song.

### 4. Playlist Page
- **Page Title**: My Playlists
- **Container Div ID**: playlists-page
- **UI Elements**:
  - playlists-grid (Div): Grid of playlist cards with cover, title, song count.
  - create-playlist-button (Button): Create new playlist.
  - view-playlist-button-{playlist_id} (Button): View details of a playlist.
  - back-to-dashboard (Button): Return to Dashboard page.

### 5. Playlist Details Page
- **Page Title**: Playlist Details
- **Container Div ID**: playlist-details-page
- **UI Elements**:
  - playlist-title (H1): Playlist title.
  - playlist-description (Div): Playlist description.
  - songs-in-playlist (Table): Songs with columns (title, artist, duration, remove option).
  - remove-song-button-{song_id} (Button): Remove a song from playlist.
  - delete-playlist-button (Button): Delete the entire playlist.

### 6. Create Playlist Page
- **Page Title**: Create New Playlist
- **Container Div ID**: create-playlist-page
- **UI Elements**:
  - playlist-name-input (Input): Input field for playlist name.
  - playlist-description-input (Textarea): Input for playlist description.
  - save-playlist-button (Button): Save/Create new playlist.
  - cancel-create-button (Button): Cancel creation and go back.

### 7. Album Browse Page
- **Page Title**: Albums
- **Container Div ID**: albums-page
- **UI Elements**:
  - albums-grid (Div): Grid with album cards (cover art, title, artist, year).
  - search-albums (Input): Search albums by title or artist.
  - sort-albums (Dropdown): Sort albums by Title, Artist, or Year.
  - view-album-button-{album_id} (Button): View album details.

### 8. Album Details Page
- **Page Title**: Album Details
- **Container Div ID**: album-details-page
- **UI Elements**:
  - album-title (H1): Album title.
  - album-artist (Div): Album artist name.
  - album-year (Div): Album release year.
  - album-songs-list (Div): List of songs in the album.
  - add-album-to-playlist-button (Button): Add all album songs to playlist.

### 9. Artist Profile Page
- **Page Title**: Artist Profiles
- **Container Div ID**: artists-page
- **UI Elements**:
  - artists-grid (Div): Grid of artist cards with photo, name, genre.
  - search-artists (Input): Search artists by name.
  - artists-sort (Dropdown): Sort artists by Name or Genre.
  - view-artist-button-{artist_id} (Button): View artist profile.

### 10. Genre Exploration Page
- **Page Title**: Genre Exploration
- **Container Div ID**: genres-page
- **UI Elements**:
  - genres-list (Div): List all available genres.
  - select-genre (Dropdown): Select a genre to view details.
  - genre-songs (Div): Songs in the selected genre.
  - genre-artists (Div): Artists of the selected genre.
  - back-to-dashboard (Button): Navigate back to Dashboard.

---

## Navigation Flow (Starting from Dashboard)
- Dashboard (dashboard-page)
  - browse-songs-button -> Song Catalog (catalog-page)
  - my-playlists-button -> Playlist Page (playlists-page)
  - trending-artists-button -> Artist Profile Page (artists-page)
  - back-to-dashboard buttons (where applicable) return to Dashboard
  - From Catalog:
    - add-to-playlist-button on song cards to add songs
    - Clicking song navigates to Song Details (song-details-page)
  - From Playlist Page:
    - create-playlist-button -> Create Playlist Page (create-playlist-page)
    - view-playlist-button-{playlist_id} -> Playlist Details Page (playlist-details-page)
  - From Album Browse Page:
    - view-album-button-{album_id} -> Album Details Page (album-details-page)
  - From Artist Profile Page:
    - view-artist-button-{artist_id} -> Artist Details (not distinct page but similar view inside artists-page or song-details)
  - From Genre Exploration Page:
    - select-genre dropdown updates genre-songs and genre-artists
    - back-to-dashboard button -> Dashboard

---

## Section 2: Data Storage Formats

### 1. Songs Data
- **File**: songs.txt
- **Format**:
```
song_id|title|artist_id|album_id|genre|duration|release_date|play_count
```
- **Example:**
```
1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
3|Shape of You|3|3|Pop|233|2017-01-06|4200000
```

### 2. Artists Data
- **File**: artists.txt
- **Format**:
```
artist_id|name|genre|country|formation_year
```
- **Example:**
```
1|Queen|Rock|United Kingdom|1970
2|The Weeknd|Synth-Pop|Canada|2010
3|Ed Sheeran|Pop|United Kingdom|2005
```

### 3. Albums Data
- **File**: albums.txt
- **Format**:
```
album_id|title|artist_id|release_year|total_songs|genre
```
- **Example:**
```
1|A Night at the Opera|1|1975|11|Rock
2|After Hours|2|2019|14|Synth-Pop
3|Divide|3|2017|12|Pop
```

### 4. Genres Data
- **File**: genres.txt
- **Format**:
```
genre_id|genre_name|description
```
- **Example:**
```
1|Rock|Guitar-driven music with strong beats and vocals
2|Pop|Catchy mainstream music with broad appeal
3|Hip-Hop|Rhythmic music with rap vocals and beat production
```

### 5. Playlists Data
- **File**: playlists.txt
- **Format**:
```
playlist_id|title|description|creation_date|total_songs
```
- **Example:**
```
1|Workout Mix|High energy songs for the gym|2025-01-15|25
2|Chill Vibes|Relaxing music for study|2025-01-16|18
3|Party Hits|Latest party tracks|2025-01-17|32
```

### 6. Playlist Songs Data
- **File**: playlist_songs.txt
- **Format**:
```
playlist_song_id|playlist_id|song_id|added_date
```
- **Example:**
```
1|1|2|2025-01-15
2|1|3|2025-01-15
3|2|1|2025-01-16
```

---

This completes the comprehensive design specification for the MusicStreaming web application.
