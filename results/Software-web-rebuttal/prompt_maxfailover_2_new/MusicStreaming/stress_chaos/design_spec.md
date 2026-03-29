# MusicStreaming Application Design Specification

---

## 1. Flask Routes Specification

| Route Path                  | Function Name          | HTTP Method(s) | Template File          | Context Variables                                                                                                        |
|-----------------------------|------------------------|----------------|------------------------|--------------------------------------------------------------------------------------------------------------------------|
| /                           | redirect_to_dashboard   | GET            | N/A (redirect)          | None                                                                                                                     |
| /dashboard                  | dashboard              | GET            | dashboard.html          | featured_songs: List[Dict[str, any]], featured_playlists: List[Dict[str, any]], trending_artists: List[Dict[str, any]]    |
| /songs                     | song_catalog           | GET            | songs.html              | songs: List[Dict[str, any]], genres: List[Dict[str, any]], search_query: str, genre_filter: int or None                   |
| /songs/<int:song_id>        | song_details           | GET            | song_detail.html        | song: Dict[str, any]                                                                                                      |
| /playlists                 | playlists              | GET            | playlists.html          | playlists: List[Dict[str, any]]                                                                                           |
| /playlists/<int:playlist_id>| playlist_details       | GET            | playlist_detail.html    | playlist: Dict[str, any], songs: List[Dict[str, any]]                                                                     |
| /playlists/create           | create_playlist        | GET, POST      | create_playlist.html    | (GET) None                                                                                                                |
| /albums                    | albums_list            | GET            | albums.html             | albums: List[Dict[str, any]], search_query: str, sort_option: str                                                        |
| /albums/<int:album_id>      | album_details          | GET            | album_detail.html       | album: Dict[str, any], songs: List[Dict[str, any]]                                                                       |
| /artists                   | artists_list           | GET            | artists.html            | artists: List[Dict[str, any]], search_query: str, sort_option: str                                                       |
| /artists/<int:artist_id>    | artist_profile         | GET            | artist_profile.html     | artist: Dict[str, any], albums: List[Dict[str, any]], songs: List[Dict[str, any]]                                         |
| /genres                    | genres_page            | GET            | genres.html             | genres: List[Dict[str, any]]                                                                                              |
| /genres/<int:genre_id>      | genre_details          | GET            | genre_detail.html       | genre: Dict[str, any], songs: List[Dict[str, any]], artists: List[Dict[str, any]]                                         |

---

## 2. HTML Templates Specification

### dashboard.html
- Template Path: templates/dashboard.html
- Page Title: "Music Streaming Dashboard"
- Main Container ID: `dashboard-page` (Div)
- IDs and Elements:
  - featured-songs (Div)
  - browse-songs-button (Button)
  - my-playlists-button (Button)
  - trending-artists-button (Button)
- Context Variables:
  - featured_songs: List of song dicts with id, title, artist_name, duration
  - featured_playlists: List of playlist dicts with id, title, total_songs
  - trending_artists: List of artist dicts with id, name
- Navigation Mapping:
  - `browse-songs-button` &rarr; `song_catalog`
  - `my-playlists-button` &rarr; `playlists`
  - `trending-artists-button` &rarr; custom route / trending artists (not explicitly specified but should be `/artists?filter=trending` or similar)

### songs.html
- Template Path: templates/songs.html
- Page Title: "Song Catalog"
- Main Container ID: `catalog-page` (Div)
- IDs and Elements:
  - search-input (Input)
  - genre-filter (Dropdown)
  - songs-grid (Div)
  - add-to-playlist-button-{song_id} (Button)
- Context Variables:
  - songs: List of song dicts (id, title, artist_name, album_name, duration, genre)
  - genres: List of genre dicts (id, genre_name)
  - search_query: str
  - genre_filter: int or None
- Navigation Mapping:
  - Buttons `add-to-playlist-button-{song_id}`: Trigger adding song to playlist (AJAX or form post to backend)

### song_detail.html
- Template Path: templates/song_detail.html
- Page Title: "Song Details"
- Main Container ID: `song-details-page` (Div)
- IDs and Elements:
  - song-title (H1)
  - artist-name (Div) - clickable link to artist profile `/artists/<artist_id>`
  - album-name (Div)
  - duration-display (Div)
  - play-button (Button)
- Context Variables:
  - song: dict with all detailed song info including artist_id, album_id
- Navigation Mapping:
  - artist-name click navigates to `artist_profile` route
  - play-button triggers play (frontend behavior)

### playlists.html
- Template Path: templates/playlists.html
- Page Title: "My Playlists"
- Main Container ID: `playlists-page` (Div)
- IDs and Elements:
  - playlists-grid (Div)
  - create-playlist-button (Button)
  - back-to-dashboard (Button)
  - view-playlist-button-{playlist_id} (Button)
- Context Variables:
  - playlists: List of playlist dicts (id, title, description, total_songs)
- Navigation Mapping:
  - create-playlist-button &rarr; `create_playlist`
  - back-to-dashboard &rarr; `dashboard`
  - view-playlist-button-{playlist_id} &rarr; `playlist_details`

### playlist_detail.html
- Template Path: templates/playlist_detail.html
- Page Title: "Playlist Details"
- Main Container ID: `playlist-details-page` (Div)
- IDs and Elements:
  - playlist-title (H1)
  - playlist-description (Div)
  - songs-in-playlist (Table)
  - remove-song-button-{song_id} (Button)
  - delete-playlist-button (Button)
- Context Variables:
  - playlist: dict with id, title, description
  - songs: list of song dicts in the playlist
- Navigation Mapping:
  - remove-song-button-{song_id}: POST to remove song from playlist
  - delete-playlist-button: POST to delete playlist

### create_playlist.html
- Template Path: templates/create_playlist.html
- Page Title: "Create New Playlist"
- Main Container ID: `create-playlist-page` (Div)
- IDs and Elements:
  - playlist-name-input (Input)
  - playlist-description-input (Textarea)
  - save-playlist-button (Button)
  - cancel-create-button (Button)
- Context Variables: None
- Navigation Mapping:
  - save-playlist-button: POST to create playlist
  - cancel-create-button: navigate back to `playlists`

### albums.html
- Template Path: templates/albums.html
- Page Title: "Albums"
- Main Container ID: `albums-page` (Div)
- IDs and Elements:
  - albums-grid (Div)
  - search-albums (Input)
  - sort-albums (Dropdown)
  - view-album-button-{album_id} (Button)
- Context Variables:
  - albums: list of album dicts
  - search_query: str
  - sort_option: str
- Navigation Mapping:
  - view-album-button-{album_id} &rarr; `album_details`

### album_detail.html
- Template Path: templates/album_detail.html
- Page Title: "Album Details"
- Main Container ID: `album-details-page` (Div)
- IDs and Elements:
  - album-title (H1)
  - album-artist (Div)
  - album-year (Div)
  - album-songs-list (Div)
  - add-album-to-playlist-button (Button)
- Context Variables:
  - album: dict
  - songs: list of songs
- Navigation Mapping:
  - add-album-to-playlist-button: adds all album songs to playlist

### artists.html
- Template Path: templates/artists.html
- Page Title: "Artist Profiles"
- Main Container ID: `artists-page` (Div)
- IDs and Elements:
  - artists-grid (Div)
  - search-artists (Input)
  - artists-sort (Dropdown)
  - view-artist-button-{artist_id} (Button)
- Context Variables:
  - artists: list of artist dicts
  - search_query: str
  - sort_option: str
- Navigation Mapping:
  - view-artist-button-{artist_id} &rarr; `artist_profile`

### genres.html
- Template Path: templates/genres.html
- Page Title: "Genre Exploration"
- Main Container ID: `genres-page` (Div)
- IDs and Elements:
  - genres-list (Div)
  - select-genre (Dropdown)
  - genre-songs (Div)
  - genre-artists (Div)
  - back-to-dashboard (Button)
- Context Variables:
  - genres: list of genre dicts
  - selected_genre_id: int or None
  - genre_songs: list of song dicts
  - genre_artists: list of artist dicts
- Navigation Mapping:
  - back-to-dashboard &rarr; `dashboard`


## 3. Data File Schemas

### data/songs.txt
- Format: Pipe-delimited (`|`)
- Fields:
  1. song_id: int - Unique ID for the song
  2. title: str - Song title
  3. artist_id: int - Foreign key referencing artists
  4. album_id: int - Foreign key referencing albums
  5. genre: str - Music genre
  6. duration: int - Duration in seconds
  7. release_date: date (YYYY-MM-DD) - Date song was released
  8. play_count: int - Number of plays
- Example rows:
  ```
  1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
  2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
  3|Shape of You|3|3|Pop|233|2017-01-06|4200000
  ```

### data/artists.txt
- Format: Pipe-delimited (`|`)
- Fields:
  1. artist_id: int - Unique artist ID
  2. name: str - Artist name
  3. genre: str - Primary genre
  4. country: str - Country of origin
  5. formation_year: int - Year formed
- Example rows:
  ```
  1|Queen|Rock|United Kingdom|1970
  2|The Weeknd|Synth-Pop|Canada|2010
  3|Ed Sheeran|Pop|United Kingdom|2005
  ```

### data/albums.txt
- Format: Pipe-delimited (`|`)
- Fields:
  1. album_id: int - Unique album ID
  2. title: str - Album title
  3. artist_id: int - Foreign key referencing artist
  4. release_year: int - Year released
  5. total_songs: int - Number of songs
  6. genre: str - Album genre
- Example rows:
  ```
  1|A Night at the Opera|1|1975|11|Rock
  2|After Hours|2|2019|14|Synth-Pop
  3|Divide|3|2017|12|Pop
  ```

### data/genres.txt
- Format: Pipe-delimited (`|`)
- Fields:
  1. genre_id: int - Unique genre ID
  2. genre_name: str - Name of genre
  3. description: str - Description
- Example rows:
  ```
  1|Rock|Guitar-driven music with strong beats and vocals
  2|Pop|Catchy mainstream music with broad appeal
  3|Hip-Hop|Rhythmic music with rap vocals and beat production
  ```

### data/playlists.txt
- Format: Pipe-delimited (`|`)
- Fields:
  1. playlist_id: int - Unique playlist ID
  2. title: str - Playlist title
  3. description: str - Playlist description
  4. creation_date: date (YYYY-MM-DD) - Date created
  5. total_songs: int - Number of songs in playlist
- Example rows:
  ```
  1|Workout Mix|High energy songs for the gym|2025-01-15|25
  2|Chill Vibes|Relaxing music for study|2025-01-16|18
  3|Party Hits|Latest party tracks|2025-01-17|32
  ```

### data/playlist_songs.txt
- Format: Pipe-delimited (`|`)
- Fields:
  1. playlist_song_id: int - Unique ID for playlist song mapping
  2. playlist_id: int - Foreign key referencing playlists
  3. song_id: int - Foreign key referencing songs
  4. added_date: date (YYYY-MM-DD) - Date added to playlist
- Example rows:
  ```
  1|1|2|2025-01-15
  2|1|3|2025-01-15
  3|2|1|2025-01-16
  ```

---

# End of Design Specification
