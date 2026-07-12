# MusicStreaming Web Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                     | Function Name             | HTTP Method(s) | Template File             | Context Variables                                                                                                                      |
|-------------------------------|---------------------------|----------------|---------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| /                             | root_redirect              | GET            | None (Redirect)           | None                                                                                                                                    |
| /dashboard                    | dashboard_page             | GET            | dashboard.html            | featured_songs: list of dict {song_id: int, title: str, artist_name: str, duration: int}
trending_artists: list of dict {artist_id: int, name: str, genre: str}                 |
| /songs                       | song_catalog_page          | GET            | song_catalog.html         | songs: list of dict {song_id: int, title: str, artist_name: str, album_name: str, genre: str, duration: int}
genres: list of str                                                                 |
| /songs/search                 | song_search                | POST           | song_catalog.html         | songs: list of dict (same structure as above)
genres: list of str
search_query: str
selected_genre: str or None                                                        |
| /songs/<int:song_id>          | song_details_page          | GET            | song_details.html         | song: dict {song_id: int, title: str, artist_id: int, artist_name: str, album_name: str, duration: int}
                                   |
| /playlists                   | playlists_page             | GET            | playlists.html            | playlists: list of dict {playlist_id: int, title: str, description: str, total_songs: int}                                              |
| /playlists/create             | create_playlist_page       | GET, POST      | create_playlist.html      | On GET: None
On POST: success_message: str (optional), error_message: str (optional)                                                      |
| /playlists/<int:playlist_id>  | playlist_details_page      | GET            | playlist_details.html     | playlist: dict {playlist_id: int, title: str, description: str}
songs_in_playlist: list of dict {song_id: int, title: str, artist_name: str, duration: int}|
| /playlists/<int:playlist_id>/delete | delete_playlist          | POST           | None (Redirect)           | None                                                                                                                                    |
| /playlists/<int:playlist_id>/songs/<int:song_id>/remove | remove_song_from_playlist | POST           | None (Redirect)           | None                                                                                                                                    |
| /albums                      | album_browse_page          | GET            | album_browse.html         | albums: list of dict {album_id: int, title: str, artist_name: str, release_year: int}                                                   |
| /albums/search                | album_search               | POST           | album_browse.html         | albums: list of dict (same structure as above)
search_query: str
sort_option: str ("By Title", "By Artist", "By Year")           |
| /albums/<int:album_id>        | album_details_page         | GET            | album_details.html        | album: dict {album_id: int, title: str, artist_name: str, release_year: int}
songs_in_album: list of dict {song_id: int, title: str, duration: int}            |
| /albums/<int:album_id>/add_to_playlist | add_album_to_playlist    | POST           | None (Redirect)           | None                                                                                                                                    |
| /artists                     | artist_profile_page        | GET            | artist_profile.html       | artists: list of dict {artist_id: int, name: str, genre: str, country: str}
                                                                 |
| /artists/search               | artist_search              | POST           | artist_profile.html       | artists: list of dict (same structure as above)
search_query: str
sort_option: str ("By Name", "By Genre")                          |
| /artists/<int:artist_id>      | artist_details_page        | GET            | artist_details.html       | artist: dict {artist_id: int, name: str, genre: str, country: str, formation_year: int}
songs_by_artist: list of dict {song_id: int, title: str, album_name: str, duration: int}|
| /genres                      | genre_exploration_page     | GET            | genre_exploration.html    | genres: list of dict {genre_id: int, genre_name: str, description: str}
selected_genre: str or None
songs_in_genre: list of dict {song_id: int, title: str, artist_name: str, duration: int}
artists_in_genre: list of dict {artist_id: int, name: str, genre: str}            |
| /genres/filter                | genre_filter               | POST           | genre_exploration.html    | genres: list of dict (same structure as above)
selected_genre: str
songs_in_genre: list of dict (same as above)
artists_in_genre: list of dict (same as above)|

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### Overall Notes:
- All templates are located under `templates/` directory.
- Dynamic IDs for buttons involving entities append the entity's id e.g. `add-to-playlist-button-{{ song_id }}`.
- Navigation buttons link to routes described in Section 1.

### 1. Dashboard Page
- Template File Path: templates/dashboard.html
- Page Title:
  - &lt;title&gt;Music Streaming Dashboard&lt;/title&gt;
  - &lt;h1 id="dashboard-title"&gt;Music Streaming Dashboard&lt;/h1&gt;
- Required Element IDs:
  - dashboard-page (Div)
  - featured-songs (Div)
  - browse-songs-button (Button)
  - my-playlists-button (Button)
  - trending-artists-button (Button)
- Context Variables:
  - featured_songs: list of dict with keys song_id (int), title (str), artist_name (str), duration (int seconds)
  - trending_artists: list of dict with keys artist_id (int), name (str), genre (str)
- Navigation Mappings:
  - browse-songs-button &rarr; song_catalog_page
  - my-playlists-button &rarr; playlists_page
  - trending-artists-button &rarr; artist_profile_page

### 2. Song Catalog Page
- Template File Path: templates/song_catalog.html
- Page Title:
  - &lt;title&gt;Song Catalog&lt;/title&gt;
  - &lt;h1 id="catalog-title"&gt;Song Catalog&lt;/h1&gt;
- Required Element IDs:
  - catalog-page (Div)
  - search-input (Input)
  - genre-filter (Dropdown)
  - songs-grid (Div)
  - add-to-playlist-button-{{ song_id }} (Button) for each song card
- Context Variables:
  - songs: list of dict with keys song_id (int), title (str), artist_name (str), album_name (str), genre (str), duration (int seconds)
  - genres: list of genre names (str)
  - search_query: str (optional, for POST requests)
  - selected_genre: str or None
- Navigation Mappings:
  - add-to-playlist-button-{{ song_id }} &rarr; add song to playlist action (POST backend route)

### 3. Song Details Page
- Template File Path: templates/song_details.html
- Page Title:
  - &lt;title&gt;Song Details&lt;/title&gt;
  - &lt;h1 id="song-title"&gt;{{ song.title }}&lt;/h1&gt;
- Required Element IDs:
  - song-details-page (Div)
  - song-title (H1)
  - artist-name (Div) - this should be a clickable link to artist profile page
  - album-name (Div)
  - duration-display (Div)
  - play-button (Button)
- Context Variables:
  - song: dict with keys song_id (int), title (str), artist_id (int), artist_name (str), album_name (str), duration (int seconds)
- Navigation Mappings:
  - artist-name (Div link) &rarr; artist_details_page with artist_id
  - play-button &rarr; play song action (may be client-side)

### 4. Playlist Page
- Template File Path: templates/playlists.html
- Page Title:
  - &lt;title&gt;My Playlists&lt;/title&gt;
  - &lt;h1 id="playlists-title"&gt;My Playlists&lt;/h1&gt;
- Required Element IDs:
  - playlists-page (Div)
  - playlists-grid (Div)
  - create-playlist-button (Button)
  - view-playlist-button-{{ playlist_id }} (Button) for each playlist card
  - back-to-dashboard (Button)
- Context Variables:
  - playlists: list of dict with keys playlist_id (int), title (str), description (str), total_songs (int)
- Navigation Mappings:
  - create-playlist-button &rarr; create_playlist_page
  - view-playlist-button-{{ playlist_id }} &rarr; playlist_details_page with playlist_id
  - back-to-dashboard &rarr; dashboard_page

### 5. Playlist Details Page
- Template File Path: templates/playlist_details.html
- Page Title:
  - &lt;title&gt;Playlist Details&lt;/title&gt;
  - &lt;h1 id="playlist-title"&gt;{{ playlist.title }}&lt;/h1&gt;
- Required Element IDs:
  - playlist-details-page (Div)
  - playlist-title (H1)
  - playlist-description (Div)
  - songs-in-playlist (Table)
  - remove-song-button-{{ song_id }} (Button) for each song in playlist
  - delete-playlist-button (Button)
- Context Variables:
  - playlist: dict with keys playlist_id (int), title (str), description (str)
  - songs_in_playlist: list of dict with keys song_id (int), title (str), artist_name (str), duration (int seconds)
- Navigation Mappings:
  - remove-song-button-{{ song_id }} &rarr; remove_song_from_playlist route with playlist_id and song_id (POST)
  - delete-playlist-button &rarr; delete_playlist route with playlist_id (POST)

### 6. Create Playlist Page
- Template File Path: templates/create_playlist.html
- Page Title:
  - &lt;title&gt;Create New Playlist&lt;/title&gt;
  - &lt;h1 id="create-playlist-title"&gt;Create New Playlist&lt;/h1&gt;
- Required Element IDs:
  - create-playlist-page (Div)
  - playlist-name-input (Input)
  - playlist-description-input (Textarea)
  - save-playlist-button (Button)
  - cancel-create-button (Button)
- Context Variables:
  - On GET: None
  - On POST: success_message (str, optional), error_message (str, optional)
- Navigation Mappings:
  - save-playlist-button &rarr; create_playlist_page POST handler
  - cancel-create-button &rarr; playlists_page

### 7. Album Browse Page
- Template File Path: templates/album_browse.html
- Page Title:
  - &lt;title&gt;Albums&lt;/title&gt;
  - &lt;h1 id="albums-title"&gt;Albums&lt;/h1&gt;
- Required Element IDs:
  - albums-page (Div)
  - albums-grid (Div)
  - search-albums (Input)
  - sort-albums (Dropdown)
  - view-album-button-{{ album_id }} (Button) for each album card
- Context Variables:
  - albums: list of dict with keys album_id (int), title (str), artist_name (str), release_year (int)
  - search_query: str (optional, for POST)
  - sort_option: str ("By Title", "By Artist", "By Year")
- Navigation Mappings:
  - view-album-button-{{ album_id }} &rarr; album_details_page with album_id

### 8. Album Details Page
- Template File Path: templates/album_details.html
- Page Title:
  - &lt;title&gt;Album Details&lt;/title&gt;
  - &lt;h1 id="album-title"&gt;{{ album.title }}&lt;/h1&gt;
- Required Element IDs:
  - album-details-page (Div)
  - album-title (H1)
  - album-artist (Div)
  - album-year (Div)
  - album-songs-list (Div)
  - add-album-to-playlist-button (Button)
- Context Variables:
  - album: dict with keys album_id (int), title (str), artist_name (str), release_year (int)
  - songs_in_album: list of dict with keys song_id (int), title (str), duration (int seconds)
- Navigation Mappings:
  - add-album-to-playlist-button &rarr; add_album_to_playlist POST route with album_id

### 9. Artist Profile Page
- Template File Path: templates/artist_profile.html
- Page Title:
  - &lt;title&gt;Artist Profiles&lt;/title&gt;
  - &lt;h1 id="artists-title"&gt;Artist Profiles&lt;/h1&gt;
- Required Element IDs:
  - artists-page (Div)
  - artists-grid (Div)
  - search-artists (Input)
  - artists-sort (Dropdown)
  - view-artist-button-{{ artist_id }} (Button) for each artist card
- Context Variables:
  - artists: list of dict with keys artist_id (int), name (str), genre (str), country (str)
  - search_query: str (optional)
  - sort_option: str ("By Name", "By Genre")
- Navigation Mappings:
  - view-artist-button-{{ artist_id }} &rarr; artist_details_page with artist_id

### 10. Genre Exploration Page
- Template File Path: templates/genre_exploration.html
- Page Title:
  - &lt;title&gt;Genre Exploration&lt;/title&gt;
  - &lt;h1 id="genres-title"&gt;Genre Exploration&lt;/h1&gt;
- Required Element IDs:
  - genres-page (Div)
  - genres-list (Div)
  - select-genre (Dropdown)
  - genre-songs (Div)
  - genre-artists (Div)
  - back-to-dashboard (Button)
- Context Variables:
  - genres: list of dict with keys genre_id (int), genre_name (str), description (str)
  - selected_genre: str or None
  - songs_in_genre: list of dict with keys song_id (int), title (str), artist_name (str), duration (int seconds)
  - artists_in_genre: list of dict with keys artist_id (int), name (str), genre (str)
- Navigation Mappings:
  - back-to-dashboard &rarr; dashboard_page

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. songs.txt
- File Path: data/songs.txt
- File Format: Pipe-delimited (|)
- Fields (in order):
  1. song_id (int): Unique numeric ID of song
  2. title (str): Song title
  3. artist_id (int): Numeric ID referencing artist in artists.txt
  4. album_id (int): Numeric ID referencing album in albums.txt
  5. genre (str): Genre name of the song
  6. duration (int): Duration in seconds
  7. release_date (str): Date in YYYY-MM-DD format
  8. play_count (int): Number of times song has been played
- Example Rows:
  ```
  1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
  2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
  3|Shape of You|3|3|Pop|233|2017-01-06|4200000
  ```
- Relationships:
  - artist_id refers to artists.txt artist_id
  - album_id refers to albums.txt album_id

### 2. artists.txt
- File Path: data/artists.txt
- File Format: Pipe-delimited (|)
- Fields (in order):
  1. artist_id (int): Unique numeric ID of artist
  2. name (str): Artist's name
  3. genre (str): Primary genre
  4. country (str): Country of origin
  5. formation_year (int): Year artist or band was formed
- Example Rows:
  ```
  1|Queen|Rock|United Kingdom|1970
  2|The Weeknd|Synth-Pop|Canada|2010
  3|Ed Sheeran|Pop|United Kingdom|2005
  ```

### 3. albums.txt
- File Path: data/albums.txt
- File Format: Pipe-delimited (|)
- Fields (in order):
  1. album_id (int): Unique numeric ID of album
  2. title (str): Album title
  3. artist_id (int): Numeric ID of artist who released the album
  4. release_year (int): Year album was released
  5. total_songs (int): Total number of songs in the album
  6. genre (str): Album genre
- Example Rows:
  ```
  1|A Night at the Opera|1|1975|11|Rock
  2|After Hours|2|2019|14|Synth-Pop
  3|Divide|3|2017|12|Pop
  ```
- Relationships:
  - artist_id refers to artists.txt artist_id

### 4. genres.txt
- File Path: data/genres.txt
- File Format: Pipe-delimited (|)
- Fields (in order):
  1. genre_id (int): Unique numeric ID of genre
  2. genre_name (str): Name of genre
  3. description (str): Description text of genre
- Example Rows:
  ```
  1|Rock|Guitar-driven music with strong beats and vocals
  2|Pop|Catchy mainstream music with broad appeal
  3|Hip-Hop|Rhythmic music with rap vocals and beat production
  ```

### 5. playlists.txt
- File Path: data/playlists.txt
- File Format: Pipe-delimited (|)
- Fields (in order):
  1. playlist_id (int): Unique numeric ID of playlist
  2. title (str): Playlist title
  3. description (str): Playlist description
  4. creation_date (str): Date playlist was created in YYYY-MM-DD format
  5. total_songs (int): Number of songs in playlist
- Example Rows:
  ```
  1|Workout Mix|High energy songs for the gym|2025-01-15|25
  2|Chill Vibes|Relaxing music for study|2025-01-16|18
  3|Party Hits|Latest party tracks|2025-01-17|32
  ```

### 6. playlist_songs.txt
- File Path: data/playlist_songs.txt
- File Format: Pipe-delimited (|)
- Fields (in order):
  1. playlist_song_id (int): Unique numeric ID for this record
  2. playlist_id (int): Numeric ID referencing playlists.txt
  3. song_id (int): Numeric ID referencing songs.txt
  4. added_date (str): Date song was added in YYYY-MM-DD format
- Example Rows:
  ```
  1|1|2|2025-01-15
  2|1|3|2025-01-15
  3|2|1|2025-01-16
  ```
- Relationships:
  - playlist_id references playlists.txt playlist_id
  - song_id references songs.txt song_id

---

*End of Design Specification Document*