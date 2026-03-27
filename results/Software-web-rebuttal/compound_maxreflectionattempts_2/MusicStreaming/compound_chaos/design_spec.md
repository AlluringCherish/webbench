# MusicStreaming Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path               | Function Name           | HTTP Method(s) | Template File             | Context Variables                                           |
|--------------------------|-------------------------|----------------|---------------------------|-------------------------------------------------------------|
| /                        | redirect_to_dashboard    | GET            | -                         | - (Redirects to /dashboard)                                 |
| /dashboard               | dashboard_page          | GET            | dashboard.html            | featured_songs: list of dict {song_id:int, title:str, artist_name:str, duration:int}
<trending_artists: list of dict {artist_id:int, name:str}>                        |
| /songs                   | song_catalog            | GET            | song_catalog.html         | songs: list of dict {song_id:int, title:str, artist_name:str, album_name:str, genre:str, duration:int}
genres: list of str                                                         |
| /songs/<int:song_id>     | song_details            | GET            | song_details.html         | song: dict {song_id:int, title:str, artist_id:int, artist_name:str, album_id:int, album_name:str, genre:str, duration:int}
                                    |
| /playlists               | playlists_page          | GET            | playlists.html            | playlists: list of dict {playlist_id:int, title:str, description:str, total_songs:int}                           |
| /playlists/<int:playlist_id> | playlist_details     | GET            | playlist_details.html     | playlist: dict {playlist_id:int, title:str, description:str}
songs: list of dict {song_id:int, title:str, artist_name:str, duration:int}           |
| /playlists/create        | create_playlist         | GET            | create_playlist.html      | -                                                               |
| /playlists/create        | create_playlist_post    | POST           | -                         | Form data processing (playlist_name:str, playlist_description:str)                 |
| /albums                  | albums_page             | GET            | albums.html               | albums: list of dict {album_id:int, title:str, artist_name:str, release_year:int}                           |
| /albums/<int:album_id>   | album_details           | GET            | album_details.html        | album: dict {album_id:int, title:str, artist_id:int, artist_name:str, release_year:int}
songs: list of dict {song_id:int, title:str, duration:int}                              |
| /artists                 | artists_page            | GET            | artists.html              | artists: list of dict {artist_id:int, name:str, genre:str, country:str}
                             |
| /artists/<int:artist_id> | artist_profile          | GET            | artist_profile.html       | artist: dict {artist_id:int, name:str, genre:str, country:str, formation_year:int}
songs: list of dict {song_id:int, title:str, album_name:str, duration:int}           |
| /genres                  | genres_page             | GET            | genres.html               | genres: list of dict {genre_id:int, genre_name:str, description:str}
selected_genre: dict {genre_id:int, genre_name:str, description:str} or None
songs: list of dict {song_id:int, title:str, artist_name:str, duration:int}
artists: list of dict {artist_id:int, name:str, genre:str}                            |

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. Dashboard Page
- Template File Path: templates/dashboard.html
- Page Title: Music Streaming Dashboard
- Elements:
  - Div: dashboard-page
  - Div: featured-songs
  - Button: browse-songs-button
  - Button: my-playlists-button
  - Button: trending-artists-button
- Context Variables:
  - featured_songs: list of dict {song_id:int, title:str, artist_name:str, duration:int}
  - trending_artists: list of dict {artist_id:int, name:str}
- Navigation Mappings:
  - browse-songs-button -> song_catalog
  - my-playlists-button -> playlists_page
  - trending-artists-button -> artists_page

### 2. Song Catalog Page
- Template File Path: templates/song_catalog.html
- Page Title: Song Catalog
- Elements:
  - Div: catalog-page
  - Input: search-input
  - Dropdown: genre-filter
  - Div: songs-grid
  - Button: add-to-playlist-button-{{song.song_id}} (Dynamic per song)
- Context Variables:
  - songs: list of dict {song_id:int, title:str, artist_name:str, album_name:str, genre:str, duration:int}
  - genres: list of str
- Navigation Mappings:
  - Buttons add-to-playlist-button-{{song.song_id}} -> (Typically triggers playlist addition action, may link to playlist views)

### 3. Song Details Page
- Template File Path: templates/song_details.html
- Page Title: Song Details
- Elements:
  - Div: song-details-page
  - H1: song-title
  - Div: artist-name
  - Div: album-name
  - Div: duration-display
  - Button: play-button
- Context Variables:
  - song: dict {song_id:int, title:str, artist_id:int, artist_name:str, album_id:int, album_name:str, genre:str, duration:int}
- Navigation Mappings:
  - artist-name (as link) -> artist_profile
  - play-button (Triggers playback)

### 4. Playlist Page
- Template File Path: templates/playlists.html
- Page Title: My Playlists
- Elements:
  - Div: playlists-page
  - Div: playlists-grid
  - Button: create-playlist-button
  - Button: view-playlist-button-{{playlist.playlist_id}} (Dynamic)
  - Button: back-to-dashboard
- Context Variables:
  - playlists: list of dict {playlist_id:int, title:str, description:str, total_songs:int}
- Navigation Mappings:
  - create-playlist-button -> create_playlist
  - back-to-dashboard -> dashboard_page
  - view-playlist-button-{{playlist.playlist_id}} -> playlist_details

### 5. Playlist Details Page
- Template File Path: templates/playlist_details.html
- Page Title: Playlist Details
- Elements:
  - Div: playlist-details-page
  - H1: playlist-title
  - Div: playlist-description
  - Table: songs-in-playlist
  - Button: remove-song-button-{{song.song_id}} (Dynamic)
  - Button: delete-playlist-button
- Context Variables:
  - playlist: dict {playlist_id:int, title:str, description:str}
  - songs: list of dict {song_id:int, title:str, artist_name:str, duration:int}
- Navigation Mappings:
  - remove-song-button-{{song.song_id}} -> remove_song_from_playlist
  - delete-playlist-button -> delete_playlist

### 6. Create Playlist Page
- Template File Path: templates/create_playlist.html
- Page Title: Create New Playlist
- Elements:
  - Div: create-playlist-page
  - Input: playlist-name-input
  - Textarea: playlist-description-input
  - Button: save-playlist-button
  - Button: cancel-create-button
- Context Variables: None
- Navigation Mappings:
  - save-playlist-button -> create_playlist_post
  - cancel-create-button -> playlists_page

### 7. Album Browse Page
- Template File Path: templates/albums.html
- Page Title: Albums
- Elements:
  - Div: albums-page
  - Div: albums-grid
  - Input: search-albums
  - Dropdown: sort-albums
  - Button: view-album-button-{{album.album_id}} (Dynamic)
- Context Variables:
  - albums: list of dict {album_id:int, title:str, artist_name:str, release_year:int}
- Navigation Mappings:
  - view-album-button-{{album.album_id}} -> album_details

### 8. Album Details Page
- Template File Path: templates/album_details.html
- Page Title: Album Details
- Elements:
  - Div: album-details-page
  - H1: album-title
  - Div: album-artist
  - Div: album-year
  - Div: album-songs-list
  - Button: add-album-to-playlist-button
- Context Variables:
  - album: dict {album_id:int, title:str, artist_id:int, artist_name:str, release_year:int}
  - songs: list of dict {song_id:int, title:str, duration:int}
- Navigation Mappings:
  - add-album-to-playlist-button -> add_album_songs_to_playlist

### 9. Artist Profile Page
- Template File Path: templates/artists.html
- Page Title: Artist Profiles
- Elements:
  - Div: artists-page
  - Div: artists-grid
  - Input: search-artists
  - Dropdown: artists-sort
  - Button: view-artist-button-{{artist.artist_id}} (Dynamic)
- Context Variables:
  - artists: list of dict {artist_id:int, name:str, genre:str, country:str}
- Navigation Mappings:
  - view-artist-button-{{artist.artist_id}} -> artist_profile

### 10. Genre Exploration Page
- Template File Path: templates/genres.html
- Page Title: Genre Exploration
- Elements:
  - Div: genres-page
  - Div: genres-list
  - Dropdown: select-genre
  - Div: genre-songs
  - Div: genre-artists
  - Button: back-to-dashboard
- Context Variables:
  - genres: list of dict {genre_id:int, genre_name:str, description:str}
  - selected_genre: dict or None
  - songs: list of dict {song_id:int, title:str, artist_name:str, duration:int}
  - artists: list of dict {artist_id:int, name:str, genre:str}
- Navigation Mappings:
  - back-to-dashboard -> dashboard_page

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. Songs Data
- Filename and Path: data/songs.txt
- File Format: pipe-delimited (`|`)
- Fields:
  1. song_id (int): Unique identifier for a song
  2. title (str): Title of the song
  3. artist_id (int): Unique identifier of the artist
  4. album_id (int): Unique identifier of the album
  5. genre (str): Genre of the song
  6. duration (int): Duration of the song in seconds
  7. release_date (str): Release date in YYYY-MM-DD format
  8. play_count (int): Number of times the song has been played
- Examples:
  ```
  1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
  2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
  3|Shape of You|3|3|Pop|233|2017-01-06|4200000
  ```
- Notes:
  - artist_id references artists.txt's artist_id
  - album_id references albums.txt's album_id

### 2. Artists Data
- Filename and Path: data/artists.txt
- File Format: pipe-delimited (`|`)
- Fields:
  1. artist_id (int): Unique identifier for an artist
  2. name (str): Artist name
  3. genre (str): Artist's primary genre
  4. country (str): Country of origin
  5. formation_year (int): Year the artist was formed
- Examples:
  ```
  1|Queen|Rock|United Kingdom|1970
  2|The Weeknd|Synth-Pop|Canada|2010
  3|Ed Sheeran|Pop|United Kingdom|2005
  ```

### 3. Albums Data
- Filename and Path: data/albums.txt
- File Format: pipe-delimited (`|`)
- Fields:
  1. album_id (int): Unique identifier for an album
  2. title (str): Album title
  3. artist_id (int): Artist who released the album
  4. release_year (int): Year of release
  5. total_songs (int): Number of songs in album
  6. genre (str): Album genre
- Examples:
  ```
  1|A Night at the Opera|1|1975|11|Rock
  2|After Hours|2|2019|14|Synth-Pop
  3|Divide|3|2017|12|Pop
  ```

### 4. Genres Data
- Filename and Path: data/genres.txt
- File Format: pipe-delimited (`|`)
- Fields:
  1. genre_id (int): Unique identifier for genre
  2. genre_name (str): Name of the genre
  3. description (str): Description of the genre
- Examples:
  ```
  1|Rock|Guitar-driven music with strong beats and vocals
  2|Pop|Catchy mainstream music with broad appeal
  3|Hip-Hop|Rhythmic music with rap vocals and beat production
  ```

### 5. Playlists Data
- Filename and Path: data/playlists.txt
- File Format: pipe-delimited (`|`)
- Fields:
  1. playlist_id (int): Unique playlist identifier
  2. title (str): Playlist title
  3. description (str): Description of playlist
  4. creation_date (str): Date playlist created (YYYY-MM-DD)
  5. total_songs (int): Number of songs in the playlist
- Examples:
  ```
  1|Workout Mix|High energy songs for the gym|2025-01-15|25
  2|Chill Vibes|Relaxing music for study|2025-01-16|18
  3|Party Hits|Latest party tracks|2025-01-17|32
  ```

### 6. Playlist Songs Data
- Filename and Path: data/playlist_songs.txt
- File Format: pipe-delimited (`|`)
- Fields:
  1. playlist_song_id (int): Unique id for playlist-song link
  2. playlist_id (int): Playlist identifier (foreign key to playlists.txt)
  3. song_id (int): Song identifier (foreign key to songs.txt)
  4. added_date (str): Date song was added (YYYY-MM-DD)
- Examples:
  ```
  1|1|2|2025-01-15
  2|1|3|2025-01-15
  3|2|1|2025-01-16
  ```

---

Design specification complete. Backend and Frontend developers can independently implement MusicStreaming based on this document exclusively.
