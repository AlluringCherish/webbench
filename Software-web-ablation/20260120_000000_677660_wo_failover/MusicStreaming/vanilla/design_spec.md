# MusicStreaming Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                    | Function Name           | HTTP Method(s) | Template File          | Context Variables                                                                                                 |
|------------------------------|------------------------|----------------|------------------------|------------------------------------------------------------------------------------------------------------------|
| /                            | root_redirect           | GET            | N/A (redirect)          | None                                                                                                             |
| /dashboard                   | dashboard              | GET            | dashboard.html          | featured_songs: List[Dict] with keys (song_id:int, title:str, artist_name:str, duration:int), trending_artists: List[Dict] with keys (artist_id:int, name:str) |
| /songs                      | song_catalog           | GET            | song_catalog.html       | songs: List[Dict] with keys (song_id:int, title:str, artist_name:str, album_name:str, genre:str, duration:int), genres: List[str]                         |
| /songs/<int:song_id>         | song_details           | GET            | song_details.html       | song: Dict with keys (song_id:int, title:str, artist_name:str, album_name:str, duration:int)                      |
| /playlists                  | playlists              | GET            | playlists.html          | playlists: List[Dict] with keys (playlist_id:int, title:str, description:str, total_songs:int)                    |
| /playlists/<int:playlist_id> | playlist_details       | GET            | playlist_details.html   | playlist: Dict with keys (playlist_id:int, title:str, description:str), songs: List[Dict] with keys (song_id:int, title:str, artist_name:str, duration:int)  |
| /playlists/create           | create_playlist        | GET, POST     | create_playlist.html    | GET: None; POST: form data handled internally, on success redirect                                            |
| /albums                    | albums                 | GET            | albums.html             | albums: List[Dict] with keys (album_id:int, title:str, artist_name:str, year:int)                                |
| /albums/<int:album_id>       | album_details          | GET            | album_details.html      | album: Dict with keys (album_id:int, title:str, artist_name:str, year:int), songs: List[Dict] with keys (song_id:int, title:str, duration:int)                 |
| /artists                   | artists                | GET            | artists.html            | artists: List[Dict] with keys (artist_id:int, name:str, genre:str, photo_url:str)                                |
| /artists/<int:artist_id>     | artist_profile         | GET            | artist_profile.html     | artist: Dict with keys (artist_id:int, name:str, genre:str, country:str, formation_year:int), songs: List[Dict] with keys (song_id:int, title:str, album_name:str, duration:int) |
| /genres                    | genres                 | GET            | genres.html             | genres: List[Dict] with keys (genre_id:int, genre_name:str, description:str), songs: List[Dict] with keys (song_id:int, title:str, artist_name:str), artists: List[Dict] with keys (artist_id:int, name:str) |

**Notes:**
- The root route `/` redirects to `/dashboard`.
- Dynamic routes include song_id, playlist_id, album_id, artist_id parameters.
- For POST on `/playlists/create`, form data for playlist creation is handled; no template variables returned on POST.

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. Dashboard Page
- Template File Path: templates/dashboard.html
- Page Title: <title>Music Streaming Dashboard</title>
- Page Header: <h1>Music Streaming Dashboard</h1>
- Required Element IDs:
  - Div: dashboard-page
  - Div: featured-songs
  - Button: browse-songs-button
  - Button: my-playlists-button
  - Button: trending-artists-button
- Context Variables:
  - featured_songs: List[Dict], each dict has song_id (int), title (str), artist_name (str), duration (int seconds)
  - trending_artists: List[Dict], each dict has artist_id (int), name (str)
- Navigation Mappings:
  - browse-songs-button -> song_catalog
  - my-playlists-button -> playlists
  - trending-artists-button -> artists

### 2. Song Catalog Page
- Template File Path: templates/song_catalog.html
- Page Title: <title>Song Catalog</title>
- Page Header: <h1>Song Catalog</h1>
- Required Element IDs:
  - Div: catalog-page
  - Input: search-input
  - Dropdown: genre-filter
  - Div: songs-grid
  - Button: add-to-playlist-button-{{ song.song_id }} (dynamic per song)
- Context Variables:
  - songs: List[Dict] with fields song_id (int), title (str), artist_name (str), album_name (str), genre (str), duration (int)
  - genres: List[str]
- Navigation Mappings:
  - add-to-playlist-button-{{ song_id }} -> Backend handler to add song to playlist (POST or AJAX handled)

### 3. Song Details Page
- Template File Path: templates/song_details.html
- Page Title: <title>Song Details</title>
- Page Header: <h1 id="song-title">{{ song.title }}</h1>
- Required Element IDs:
  - Div: song-details-page
  - H1: song-title
  - Div: artist-name (artist name as link to artist profile with route: artist_profile)
  - Div: album-name
  - Div: duration-display
  - Button: play-button
- Context Variables:
  - song: Dict with song_id (int), title (str), artist_name (str), album_name (str), duration (int)
- Navigation Mappings:
  - artist-name link -> artist_profile(song.artist_id)
  - play-button triggers play action (frontend)

### 4. Playlist Page
- Template File Path: templates/playlists.html
- Page Title: <title>My Playlists</title>
- Page Header: <h1>My Playlists</h1>
- Required Element IDs:
  - Div: playlists-page
  - Div: playlists-grid
  - Button: create-playlist-button
  - Button: view-playlist-button-{{ playlist.playlist_id }} (dynamic per playlist)
  - Button: back-to-dashboard
- Context Variables:
  - playlists: List[Dict] with playlist_id (int), title (str), description (str), total_songs (int)
- Navigation Mappings:
  - create-playlist-button -> create_playlist (GET)
  - view-playlist-button-{{ playlist_id }} -> playlist_details(playlist_id)
  - back-to-dashboard -> dashboard

### 5. Playlist Details Page
- Template File Path: templates/playlist_details.html
- Page Title: <title>Playlist Details</title>
- Page Header: <h1 id="playlist-title">{{ playlist.title }}</h1>
- Required Element IDs:
  - Div: playlist-details-page
  - H1: playlist-title
  - Div: playlist-description
  - Table: songs-in-playlist
  - Button: remove-song-button-{{ song.song_id }} (dynamic per song)
  - Button: delete-playlist-button
- Context Variables:
  - playlist: Dict with playlist_id (int), title (str), description (str)
  - songs: List[Dict] with song_id (int), title (str), artist_name (str), duration (int)
- Navigation Mappings:
  - remove-song-button-{{ song_id }} -> Backend action to remove song from playlist (POST)
  - delete-playlist-button -> Backend action to delete playlist (POST)

### 6. Create Playlist Page
- Template File Path: templates/create_playlist.html
- Page Title: <title>Create New Playlist</title>
- Page Header: <h1>Create New Playlist</h1>
- Required Element IDs:
  - Div: create-playlist-page
  - Input: playlist-name-input
  - Textarea: playlist-description-input
  - Button: save-playlist-button
  - Button: cancel-create-button
- Context Variables:
  - None (form inputs only)
- Navigation Mappings:
  - save-playlist-button -> form submission handled via POST
  - cancel-create-button -> playlists page

### 7. Albums Page
- Template File Path: templates/albums.html
- Page Title: <title>Albums</title>
- Page Header: <h1>Albums</h1>
- Required Element IDs:
  - Div: albums-page
  - Div: albums-grid
  - Input: search-albums
  - Dropdown: sort-albums
  - Button: view-album-button-{{ album.album_id }} (dynamic per album)
- Context Variables:
  - albums: List[Dict] with album_id (int), title (str), artist_name (str), year (int)
- Navigation Mappings:
  - view-album-button-{{ album_id }} -> album_details(album_id)

### 8. Album Details Page
- Template File Path: templates/album_details.html
- Page Title: <title>Album Details</title>
- Page Header: <h1 id="album-title">{{ album.title }}</h1>
- Required Element IDs:
  - Div: album-details-page
  - H1: album-title
  - Div: album-artist
  - Div: album-year
  - Div: album-songs-list
  - Button: add-album-to-playlist-button
- Context Variables:
  - album: Dict with album_id (int), title (str), artist_name (str), year (int)
  - songs: List[Dict] with song_id (int), title (str), duration (int)
- Navigation Mappings:
  - add-album-to-playlist-button -> Backend handler to add all songs in album to playlist

### 9. Artist Profile Page
- Template File Path: templates/artists.html
- Page Title: <title>Artist Profiles</title>
- Page Header: <h1>Artist Profiles</h1>
- Required Element IDs:
  - Div: artists-page
  - Div: artists-grid
  - Input: search-artists
  - Dropdown: artists-sort
  - Button: view-artist-button-{{ artist.artist_id }} (dynamic per artist)
- Context Variables:
  - artists: List[Dict] with artist_id (int), name (str), genre (str), photo_url (str)
- Navigation Mappings:
  - view-artist-button-{{ artist_id }} -> artist_profile(artist_id)

### 10. Genre Exploration Page
- Template File Path: templates/genres.html
- Page Title: <title>Genre Exploration</title>
- Page Header: <h1>Genre Exploration</h1>
- Required Element IDs:
  - Div: genres-page
  - Div: genres-list
  - Dropdown: select-genre
  - Div: genre-songs
  - Div: genre-artists
  - Button: back-to-dashboard
- Context Variables:
  - genres: List[Dict] with genre_id (int), genre_name (str), description (str)
  - songs: List[Dict] with song_id (int), title (str), artist_name (str)
  - artists: List[Dict] with artist_id (int), name (str)
- Navigation Mappings:
  - back-to-dashboard -> dashboard

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. Songs Data
- Filename: data/songs.txt
- File Format: Pipe-delimited (|)
- Fields:
  1. song_id (int) - Unique ID for the song
  2. title (str) - Song title
  3. artist_id (int) - Foreign key reference to artists.txt artist_id
  4. album_id (int) - Foreign key reference to albums.txt album_id
  5. genre (str) - Song genre
  6. duration (int) - Duration in seconds
  7. release_date (str) - Release date in YYYY-MM-DD format
  8. play_count (int) - Number of times song played
- Example Rows:
  ```
  1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
  2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
  3|Shape of You|3|3|Pop|233|2017-01-06|4200000
  ```

### 2. Artists Data
- Filename: data/artists.txt
- File Format: Pipe-delimited (|)
- Fields:
  1. artist_id (int) - Unique ID
  2. name (str) - Artist name
  3. genre (str) - Primary genre
  4. country (str) - Country of origin
  5. formation_year (int) - Year artist/group formed
- Example Rows:
  ```
  1|Queen|Rock|United Kingdom|1970
  2|The Weeknd|Synth-Pop|Canada|2010
  3|Ed Sheeran|Pop|United Kingdom|2005
  ```

### 3. Albums Data
- Filename: data/albums.txt
- File Format: Pipe-delimited (|)
- Fields:
  1. album_id (int) - Unique ID
  2. title (str) - Album title
  3. artist_id (int) - Foreign key reference to artists.txt
  4. release_year (int) - Year of release
  5. total_songs (int) - Number of songs in album
  6. genre (str) - Album genre
- Example Rows:
  ```
  1|A Night at the Opera|1|1975|11|Rock
  2|After Hours|2|2019|14|Synth-Pop
  3|Divide|3|2017|12|Pop
  ```

### 4. Genres Data
- Filename: data/genres.txt
- File Format: Pipe-delimited (|)
- Fields:
  1. genre_id (int) - Unique ID
  2. genre_name (str) - Name of genre
  3. description (str) - Description of genre
- Example Rows:
  ```
  1|Rock|Guitar-driven music with strong beats and vocals
  2|Pop|Catchy mainstream music with broad appeal
  3|Hip-Hop|Rhythmic music with rap vocals and beat production
  ```

### 5. Playlists Data
- Filename: data/playlists.txt
- File Format: Pipe-delimited (|)
- Fields:
  1. playlist_id (int) - Unique ID
  2. title (str) - Playlist title
  3. description (str) - Playlist description
  4. creation_date (str) - Creation date (YYYY-MM-DD)
  5. total_songs (int) - Number of songs in playlist
- Example Rows:
  ```
  1|Workout Mix|High energy songs for the gym|2025-01-15|25
  2|Chill Vibes|Relaxing music for study|2025-01-16|18
  3|Party Hits|Latest party tracks|2025-01-17|32
  ```

### 6. Playlist Songs Data
- Filename: data/playlist_songs.txt
- File Format: Pipe-delimited (|)
- Fields:
  1. playlist_song_id (int) - Unique ID
  2. playlist_id (int) - Foreign key reference to playlists.txt
  3. song_id (int) - Foreign key reference to songs.txt
  4. added_date (str) - Date song added to playlist (YYYY-MM-DD)
- Example Rows:
  ```
  1|1|2|2025-01-15
  2|1|3|2025-01-15
  3|2|1|2025-01-16
  ```

---

*This design specification enables backend and frontend developers to implement the MusicStreaming application fully independently and consistently.*
