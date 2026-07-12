# MusicStreaming Application - Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                    | Function Name          | HTTP Method(s) | Template File           | Context Variables                                                                                                                  |
|-------------------------------|-----------------------|----------------|-------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| /                             | root_redirect          | GET            | None (redirect to /dashboard) | None                                                                                                                      |
| /dashboard                   | dashboard_page         | GET            | dashboard.html           | featured_songs: list of dict {song_id: int, title: str, artist_name: str, duration: int}
trending_artists: list of dict {artist_id: int, name: str}
 |
| /songs                       | song_catalog_page      | GET, POST      | song_catalog.html        | songs: list of dict {song_id: int, title: str, artist_name: str, album_name: str, genre: str, duration: int}
filter_genre: str or None (selected genre filter)
search_query: str or None (search input text)
 |
| /songs/<int:song_id>         | song_details_page      | GET            | song_details.html        | song: dict {
  song_id: int,
  title: str,
  artist_id: int,
  artist_name: str,
  album_id: int,
  album_name: str,
  genre: str,
  duration: int
}
|
| /playlists                   | playlists_page         | GET            | playlists.html           | playlists: list of dict {playlist_id: int, title: str, song_count:int}
|
| /playlists/create            | create_playlist_page   | GET, POST      | create_playlist.html     | None on GET
Form POST data processed on POST
|
| /playlists/<int:playlist_id> | playlist_details_page  | GET            | playlist_details.html    | playlist: dict {playlist_id: int, title: str, description: str}
songs_in_playlist: list of dict {song_id: int, title: str, artist_name: str, duration: int}
|
| /albums                     | albums_page            | GET            | albums.html              | albums: list of dict {album_id: int, title: str, artist_name: str, year: int}
|
| /albums/<int:album_id>       | album_details_page     | GET            | album_details.html       | album: dict {album_id: int, title: str, artist_name: str, year: int}
songs_in_album: list of dict {song_id: int, title: str, duration: int}
|
| /artists                    | artists_page           | GET            | artists.html             | artists: list of dict {artist_id: int, name: str, genre: str}
|
| /artists/<int:artist_id>     | artist_profile_page    | GET            | artist_profile.html      | artist: dict {artist_id: int, name: str, genre: str, country: str, formation_year: int}
artist_songs: list of dict {song_id: int, title: str, album_name: str}
|
| /genres                     | genre_exploration_page | GET            | genres.html              | genres: list of dict {genre_id: int, genre_name: str, description: str}
selected_genre: str or None (selected genre name)
genre_songs: list of dict {song_id: int, title: str, artist_name: str}
genre_artists: list of dict {artist_id: int, name: str}
|

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. Dashboard Page
- Template File Path: templates/dashboard.html
- Page Title: "Music Streaming Dashboard"
- Required Element IDs:
  - dashboard-page (Div)
  - featured-songs (Div)
  - browse-songs-button (Button)
  - my-playlists-button (Button)
  - trending-artists-button (Button)
- Context Variables:
  - featured_songs: list of dict {song_id, title, artist_name, duration}
  - trending_artists: list of dict {artist_id, name}
- Navigation Mappings:
  - browse-songs-button => song_catalog_page
  - my-playlists-button => playlists_page
  - trending-artists-button => artists_page

### 2. Song Catalog Page
- Template File Path: templates/song_catalog.html
- Page Title: "Song Catalog"
- Required Element IDs:
  - catalog-page (Div)
  - search-input (Input)
  - genre-filter (Dropdown)
  - songs-grid (Div)
  - add-to-playlist-button-{{ song.song_id }} (Button) — repeat per song card
- Context Variables:
  - songs: list of dict {song_id, title, artist_name, album_name, genre, duration}
  - filter_genre: str or None
  - search_query: str or None
- Navigation Mappings:
  - Clicking add-to-playlist-button-{song_id} triggers backend playlist adding

### 3. Song Details Page
- Template File Path: templates/song_details.html
- Page Title: "Song Details"
- Required Element IDs:
  - song-details-page (Div)
  - song-title (H1)
  - artist-name (Div) with link to artist_profile_page
  - album-name (Div)
  - duration-display (Div)
  - play-button (Button)
- Context Variables:
  - song: dict {song_id, title, artist_id, artist_name, album_id, album_name, genre, duration}
- Navigation Mappings:
  - artist-name link => artist_profile_page

### 4. Playlist Page
- Template File Path: templates/playlists.html
- Page Title: "My Playlists"
- Required Element IDs:
  - playlists-page (Div)
  - playlists-grid (Div)
  - create-playlist-button (Button)
  - view-playlist-button-{{ playlist.playlist_id }} (Button) — per playlist card
  - back-to-dashboard (Button)
- Context Variables:
  - playlists: list of dict {playlist_id, title, song_count}
- Navigation Mappings:
  - create-playlist-button => create_playlist_page
  - view-playlist-button-{playlist_id} => playlist_details_page(playlist_id)
  - back-to-dashboard => dashboard_page

### 5. Playlist Details Page
- Template File Path: templates/playlist_details.html
- Page Title: "Playlist Details"
- Required Element IDs:
  - playlist-details-page (Div)
  - playlist-title (H1)
  - playlist-description (Div)
  - songs-in-playlist (Table)
  - remove-song-button-{{ song.song_id }} (Button) — per song row
  - delete-playlist-button (Button)
- Context Variables:
  - playlist: dict {playlist_id, title, description}
  - songs_in_playlist: list of dict {song_id, title, artist_name, duration}
- Navigation Mappings:
  - remove-song-button-{song_id} triggers song removal
  - delete-playlist-button triggers playlist deletion

### 6. Create Playlist Page
- Template File Path: templates/create_playlist.html
- Page Title: "Create New Playlist"
- Required Element IDs:
  - create-playlist-page (Div)
  - playlist-name-input (Input)
  - playlist-description-input (Textarea)
  - save-playlist-button (Button)
  - cancel-create-button (Button)
- Context Variables:
  - None
- Navigation Mappings:
  - save-playlist-button triggers playlist creation POST
  - cancel-create-button navigates back (previous page or playlist page)

### 7. Album Browse Page
- Template File Path: templates/albums.html
- Page Title: "Albums"
- Required Element IDs:
  - albums-page (Div)
  - albums-grid (Div)
  - search-albums (Input)
  - sort-albums (Dropdown)
  - view-album-button-{{ album.album_id }} (Button) — per album card
- Context Variables:
  - albums: list of dict {album_id, title, artist_name, year}
- Navigation Mappings:
  - view-album-button-{album_id} => album_details_page(album_id)

### 8. Album Details Page
- Template File Path: templates/album_details.html
- Page Title: "Album Details"
- Required Element IDs:
  - album-details-page (Div)
  - album-title (H1)
  - album-artist (Div)
  - album-year (Div)
  - album-songs-list (Div)
  - add-album-to-playlist-button (Button)
- Context Variables:
  - album: dict {album_id, title, artist_name, year}
  - songs_in_album: list of dict {song_id, title, duration}
- Navigation Mappings:
  - add-album-to-playlist-button triggers batch add of album songs to playlist

### 9. Artist Profile Page
- Template File Path: templates/artists.html
- Page Title: "Artist Profiles"
- Required Element IDs:
  - artists-page (Div)
  - artists-grid (Div)
  - search-artists (Input)
  - artists-sort (Dropdown)
  - view-artist-button-{{ artist.artist_id }} (Button) — per artist card
- Context Variables:
  - artists: list of dict {artist_id, name, genre}
- Navigation Mappings:
  - view-artist-button-{artist_id} => artist_profile_page(artist_id)

### 10. Genre Exploration Page
- Template File Path: templates/genres.html
- Page Title: "Genre Exploration"
- Required Element IDs:
  - genres-page (Div)
  - genres-list (Div)
  - select-genre (Dropdown)
  - genre-songs (Div)
  - genre-artists (Div)
  - back-to-dashboard (Button)
- Context Variables:
  - genres: list of dict {genre_id, genre_name, description}
  - selected_genre: str or None
  - genre_songs: list of dict {song_id, title, artist_name}
  - genre_artists: list of dict {artist_id, name}
- Navigation Mappings:
  - back-to-dashboard => dashboard_page

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. Songs Data
- Filename and Path: data/songs.txt
- File Format: pipe-delimited (|)
- Fields:
  1. song_id (int) - Unique identifier for the song
  2. title (str) - Song title
  3. artist_id (int) - Foreign key referencing artists.txt
  4. album_id (int) - Foreign key referencing albums.txt
  5. genre (str) - Genre of the song
  6. duration (int) - Duration of the song in seconds
  7. release_date (str) - Release date in YYYY-MM-DD format
  8. play_count (int) - Number of plays
- Example Rows:
  ```
  1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
  2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
  3|Shape of You|3|3|Pop|233|2017-01-06|4200000
  ```

### 2. Artists Data
- Filename and Path: data/artists.txt
- File Format: pipe-delimited (|)
- Fields:
  1. artist_id (int) - Unique identifier for the artist
  2. name (str) - Artist name
  3. genre (str) - Primary genre
  4. country (str) - Country of origin
  5. formation_year (int) - Year artist or band was formed
- Example Rows:
  ```
  1|Queen|Rock|United Kingdom|1970
  2|The Weeknd|Synth-Pop|Canada|2010
  3|Ed Sheeran|Pop|United Kingdom|2005
  ```

### 3. Albums Data
- Filename and Path: data/albums.txt
- File Format: pipe-delimited (|)
- Fields:
  1. album_id (int) - Unique identifier for the album
  2. title (str) - Album title
  3. artist_id (int) - Foreign key referencing artists.txt
  4. release_year (int) - Year album was released
  5. total_songs (int) - Number of songs on album
  6. genre (str) - Album genre
- Example Rows:
  ```
  1|A Night at the Opera|1|1975|11|Rock
  2|After Hours|2|2019|14|Synth-Pop
  3|Divide|3|2017|12|Pop
  ```

### 4. Genres Data
- Filename and Path: data/genres.txt
- File Format: pipe-delimited (|)
- Fields:
  1. genre_id (int) - Unique identifier for genre
  2. genre_name (str) - Name of genre
  3. description (str) - Description of genre
- Example Rows:
  ```
  1|Rock|Guitar-driven music with strong beats and vocals
  2|Pop|Catchy mainstream music with broad appeal
  3|Hip-Hop|Rhythmic music with rap vocals and beat production
  ```

### 5. Playlists Data
- Filename and Path: data/playlists.txt
- File Format: pipe-delimited (|)
- Fields:
  1. playlist_id (int) - Unique identifier for playlist
  2. title (str) - Playlist title
  3. description (str) - Playlist description
  4. creation_date (str) - Creation date YYYY-MM-DD
  5. total_songs (int) - Number of songs in playlist
- Example Rows:
  ```
  1|Workout Mix|High energy songs for the gym|2025-01-15|25
  2|Chill Vibes|Relaxing music for study|2025-01-16|18
  3|Party Hits|Latest party tracks|2025-01-17|32
  ```

### 6. Playlist Songs Data
- Filename and Path: data/playlist_songs.txt
- File Format: pipe-delimited (|)
- Fields:
  1. playlist_song_id (int) - Unique identifier for playlist song entry
  2. playlist_id (int) - Foreign key referencing playlists.txt
  3. song_id (int) - Foreign key referencing songs.txt
  4. added_date (str) - Date song was added YYYY-MM-DD
- Example Rows:
  ```
  1|1|2|2025-01-15
  2|1|3|2025-01-15
  3|2|1|2025-01-16
  ```

---

**End of design specification document.**
