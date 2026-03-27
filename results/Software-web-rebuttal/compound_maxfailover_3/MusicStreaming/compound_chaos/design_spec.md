# MusicStreaming Application Design Specification

---

## Section 1: Flask Routes Specification (Backend Developer Focus)

| Route Path                    | Function Name             | HTTP Method(s) | Template File              | Context Variables                                                                                                           |
|------------------------------|---------------------------|----------------|----------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| /                            | root_redirect             | GET            | None (redirect to dashboard) | None                                                                                                                        |
| /dashboard                   | dashboard_page            | GET            | dashboard.html             | featured_songs: List[Dict{song_id: int, title: str, artist_name: str, album_name: str, genre: str, duration: int}], trending_artists: List[Dict{artist_id: int, name: str, genre: str}] |
| /songs                      | song_catalog              | GET            | song_catalog.html          | songs: List[Dict{song_id: int, title: str, artist_name: str, album_name: str, genre: str, duration: int}], genres: List[str]  |
| /songs/search                | search_songs             | POST           | song_catalog.html          | songs: List[Dict{song_id: int, title: str, artist_name: str, album_name: str, genre: str, duration: int}], genres: List[str]  |
| /song/<int:song_id>          | song_details             | GET            | song_details.html          | song: Dict{song_id: int, title: str, artist_name: str, album_name: str, genre: str, duration: int, release_date: str}          |
| /playlists                  | playlists_page           | GET            | playlists.html             | playlists: List[Dict{playlist_id: int, title: str, description: str, total_songs: int}]                                      |
| /playlist/<int:playlist_id>  | playlist_details         | GET            | playlist_details.html      | playlist: Dict{playlist_id: int, title: str, description: str}, songs: List[Dict{song_id: int, title: str, artist_name: str, duration: int}] |
| /playlist/create             | create_playlist          | GET            | create_playlist.html       | None                                                                                                                        |
| /playlist/save               | save_playlist            | POST           | playlists.html (redirect after save) | None                                                                                                                        |
| /albums                     | albums_page              | GET            | albums.html                | albums: List[Dict{album_id: int, title: str, artist_name: str, release_year: int, genre: str}]                               |
| /album/<int:album_id>        | album_details            | GET            | album_details.html         | album: Dict{album_id: int, title: str, artist_name: str, release_year: int}, songs: List[Dict{song_id: int, title: str, duration: int}] |
| /artists                    | artists_page             | GET            | artists.html               | artists: List[Dict{artist_id: int, name: str, genre: str, country: str}]                                                     |
| /artist/<int:artist_id>      | artist_profile           | GET            | artist_profile.html        | artist: Dict{artist_id: int, name: str, genre: str, country: str, formation_year: int}, songs: List[Dict{song_id: int, title: str}] |
| /genres                     | genres_page              | GET            | genres.html                | genres: List[Dict{genre_id: int, genre_name: str, description: str}], featured_songs: List[Dict{song_id: int, title: str}], featured_artists: List[Dict{artist_id: int, name: str}] |

Notes:
- Root route '/' redirects (HTTP 302) to '/dashboard'.
- Function names use snake_case matching UI navigation and elements IDs exactly as per requirements.

---

## Section 2: HTML Template Specifications (Frontend Developer Focus)

### 1. dashboard.html
- Template File Path: templates/dashboard.html
- Page Title: Music Streaming Dashboard
- Element IDs & Types:
  - dashboard-page (Div)
  - featured-songs (Div)
  - browse-songs-button (Button)
  - my-playlists-button (Button)
  - trending-artists-button (Button)
- Context Variables:
  - featured_songs: List of featured song dictionaries with keys (song_id: int, title: str, artist_name: str, album_name: str, genre: str, duration: int)
  - trending_artists: List of trending artist dictionaries with keys (artist_id: int, name: str, genre: str)
- Navigation Mappings:
  - browse-songs-button -> song_catalog
  - my-playlists-button -> playlists_page
  - trending-artists-button -> artists_page

### 2. song_catalog.html
- Template File Path: templates/song_catalog.html
- Page Title: Song Catalog
- Element IDs & Types:
  - catalog-page (Div)
  - search-input (Input)
  - genre-filter (Dropdown)
  - songs-grid (Div)
  - add-to-playlist-button-{{ song.song_id }} (Button) [dynamic per song]
- Context Variables:
  - songs: List of song dictionaries with keys (song_id: int, title: str, artist_name: str, album_name: str, genre: str, duration: int)
  - genres: List of strings (genre names)
- Navigation Mappings:
  - add-to-playlist-button-{{ song.song_id }} -> playlist_details (to add song to playlist, implementation via POST or JS)

### 3. song_details.html
- Template File Path: templates/song_details.html
- Page Title: Song Details
- Element IDs & Types:
  - song-details-page (Div)
  - song-title (H1)
  - artist-name (Div) - includes link to artist_profile
  - album-name (Div)
  - duration-display (Div)
  - play-button (Button)
- Context Variables:
  - song: Dict with keys (song_id: int, title: str, artist_name: str, album_name: str, genre: str, duration: int, release_date: str)
- Navigation Mappings:
  - artist-name (link) -> artist_profile (for artist_id)

### 4. playlists.html
- Template File Path: templates/playlists.html
- Page Title: My Playlists
- Element IDs & Types:
  - playlists-page (Div)
  - playlists-grid (Div)
  - create-playlist-button (Button)
  - view-playlist-button-{{ playlist.playlist_id }} (Button) [dynamic per playlist]
  - back-to-dashboard (Button)
- Context Variables:
  - playlists: List of playlist dictionaries with keys (playlist_id: int, title: str, description: str, total_songs: int)
- Navigation Mappings:
  - create-playlist-button -> create_playlist
  - view-playlist-button-{{ playlist.playlist_id }} -> playlist_details
  - back-to-dashboard -> dashboard_page

### 5. playlist_details.html
- Template File Path: templates/playlist_details.html
- Page Title: Playlist Details
- Element IDs & Types:
  - playlist-details-page (Div)
  - playlist-title (H1)
  - playlist-description (Div)
  - songs-in-playlist (Table)
  - remove-song-button-{{ song.song_id }} (Button) [dynamic per song]
  - delete-playlist-button (Button)
- Context Variables:
  - playlist: Dict with keys (playlist_id: int, title: str, description: str)
  - songs: List of song dictionaries with keys (song_id: int, title: str, artist_name: str, duration: int)
- Navigation Mappings:
  - remove-song-button-{{ song.song_id }} -> playlist_details (with removal action)
  - delete-playlist-button -> playlists_page

### 6. create_playlist.html
- Template File Path: templates/create_playlist.html
- Page Title: Create New Playlist
- Element IDs & Types:
  - create-playlist-page (Div)
  - playlist-name-input (Input)
  - playlist-description-input (Textarea)
  - save-playlist-button (Button)
  - cancel-create-button (Button)
- Context Variables:
  - None
- Navigation Mappings:
  - save-playlist-button -> save_playlist
  - cancel-create-button -> playlists_page

### 7. albums.html
- Template File Path: templates/albums.html
- Page Title: Albums
- Element IDs & Types:
  - albums-page (Div)
  - albums-grid (Div)
  - search-albums (Input)
  - sort-albums (Dropdown)
  - view-album-button-{{ album.album_id }} (Button) [dynamic per album]
- Context Variables:
  - albums: List of album dictionaries with keys (album_id: int, title: str, artist_name: str, release_year: int, genre: str)
- Navigation Mappings:
  - view-album-button-{{ album.album_id }} -> album_details

### 8. album_details.html
- Template File Path: templates/album_details.html
- Page Title: Album Details
- Element IDs & Types:
  - album-details-page (Div)
  - album-title (H1)
  - album-artist (Div)
  - album-year (Div)
  - album-songs-list (Div)
  - add-album-to-playlist-button (Button)
- Context Variables:
  - album: Dict with keys (album_id: int, title: str, artist_name: str, release_year: int)
  - songs: List of song dictionaries with keys (song_id: int, title: str, duration: int)
- Navigation Mappings:
  - add-album-to-playlist-button -> playlist_details

### 9. artists.html
- Template File Path: templates/artists.html
- Page Title: Artist Profiles
- Element IDs & Types:
  - artists-page (Div)
  - artists-grid (Div)
  - search-artists (Input)
  - artists-sort (Dropdown)
  - view-artist-button-{{ artist.artist_id }} (Button) [dynamic per artist]
- Context Variables:
  - artists: List of artist dictionaries with keys (artist_id: int, name: str, genre: str, country: str)
- Navigation Mappings:
  - view-artist-button-{{ artist.artist_id }} -> artist_profile

### 10. genres.html
- Template File Path: templates/genres.html
- Page Title: Genre Exploration
- Element IDs & Types:
  - genres-page (Div)
  - genres-list (Div)
  - select-genre (Dropdown)
  - genre-songs (Div)
  - genre-artists (Div)
  - back-to-dashboard (Button)
- Context Variables:
  - genres: List of genre dictionaries with keys (genre_id: int, genre_name: str, description: str)
  - featured_songs: List of featured song dictionaries (song_id: int, title: str)
  - featured_artists: List of featured artist dictionaries (artist_id: int, name: str)
- Navigation Mappings:
  - back-to-dashboard -> dashboard_page

---

## Section 3: Data File Schemas (Backend Developer Focus)

### 1. data/songs.txt
- File Format: Pipe-delimited (`|`)
- Fields (in order):
  1. song_id (int): Unique identifier for the song.
  2. title (str): Song title.
  3. artist_id (int): Foreign key referencing artists.txt's artist_id.
  4. album_id (int): Foreign key referencing albums.txt's album_id.
  5. genre (str): Genre name of the song.
  6. duration (int): Duration of the song in seconds.
  7. release_date (str): Release date in YYYY-MM-DD format.
  8. play_count (int): Number of times the song has been played.
- Example Rows:
  - `1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000`
  - `2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000`
  - `3|Shape of You|3|3|Pop|233|2017-01-06|4200000`
- Foreign Key Relationships:
  - `artist_id` references `artists.txt` `artist_id`
  - `album_id` references `albums.txt` `album_id`

### 2. data/artists.txt
- File Format: Pipe-delimited (`|`)
- Fields (in order):
  1. artist_id (int): Unique identifier for the artist.
  2. name (str): Artist name.
  3. genre (str): Main genre of the artist.
  4. country (str): Country of origin.
  5. formation_year (int): Year the artist or band was formed.
- Example Rows:
  - `1|Queen|Rock|United Kingdom|1970`
  - `2|The Weeknd|Synth-Pop|Canada|2010`
  - `3|Ed Sheeran|Pop|United Kingdom|2005`
- Foreign Key Relationships:
  - Referenced by `songs.txt` via `artist_id`
  - Referenced by `albums.txt` via `artist_id`

### 3. data/albums.txt
- File Format: Pipe-delimited (`|`)
- Fields (in order):
  1. album_id (int): Unique identifier for the album.
  2. title (str): Album title.
  3. artist_id (int): Foreign key referencing artists.txt's artist_id.
  4. release_year (int): Year album was released.
  5. total_songs (int): Number of songs on the album.
  6. genre (str): Genre of the album.
- Example Rows:
  - `1|A Night at the Opera|1|1975|11|Rock`
  - `2|After Hours|2|2019|14|Synth-Pop`
  - `3|Divide|3|2017|12|Pop`
- Foreign Key Relationships:
  - `artist_id` references `artists.txt` `artist_id`

### 4. data/genres.txt
- File Format: Pipe-delimited (`|`)
- Fields (in order):
  1. genre_id (int): Unique identifier for the genre.
  2. genre_name (str): Name of the genre.
  3. description (str): Description of the genre.
- Example Rows:
  - `1|Rock|Guitar-driven music with strong beats and vocals`
  - `2|Pop|Catchy mainstream music with broad appeal`
  - `3|Hip-Hop|Rhythmic music with rap vocals and beat production`
- Foreign Key Relationships:
  - Referenced by `songs.txt` and `albums.txt` via genre fields

### 5. data/playlists.txt
- File Format: Pipe-delimited (`|`)
- Fields (in order):
  1. playlist_id (int): Unique identifier for the playlist.
  2. title (str): Playlist title.
  3. description (str): Playlist description.
  4. creation_date (str): Date the playlist was created (YYYY-MM-DD).
  5. total_songs (int): Number of songs in the playlist.
- Example Rows:
  - `1|Workout Mix|High energy songs for the gym|2025-01-15|25`
  - `2|Chill Vibes|Relaxing music for study|2025-01-16|18`
  - `3|Party Hits|Latest party tracks|2025-01-17|32`
- Foreign Key Relationships:
  - Referenced by `playlist_songs.txt` via `playlist_id`

### 6. data/playlist_songs.txt
- File Format: Pipe-delimited (`|`)
- Fields (in order):
  1. playlist_song_id (int): Unique identifier for the entry.
  2. playlist_id (int): Foreign key referencing playlists.txt's playlist_id.
  3. song_id (int): Foreign key referencing songs.txt's song_id.
  4. added_date (str): Date the song was added to the playlist (YYYY-MM-DD).
- Example Rows:
  - `1|1|2|2025-01-15`
  - `2|1|3|2025-01-15`
  - `3|2|1|2025-01-16`
- Foreign Key Relationships:
  - `playlist_id` references `playlists.txt` `playlist_id`
  - `song_id` references `songs.txt` `song_id`

---

This comprehensive design specification will allow backend and frontend developers to work independently with full clarity on routes, UI templates, and data schema for the MusicStreaming application.
