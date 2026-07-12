# MusicStreaming Application Design Specifications

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                      | Function Name            | HTTP Method(s) | Template File           | Context Variables                                                                                                                          |
|--------------------------------|--------------------------|----------------|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| / (root)                       | root_redirect             | GET            | N/A                     | None (Redirects to /dashboard)                                                                                                            |
| /dashboard                    | dashboard_page            | GET            | dashboard.html          | featured_songs (list of dict{song_id:int, title:str, artist_name:str, duration:int}), trending_artists (list of dict{artist_id:int, name:str}), navigation_buttons (dict) |
| /songs                       | song_catalog_page         | GET            | song_catalog.html       | songs (list of dict{song_id:int, title:str, artist_name:str, album_name:str, genre:str, duration:int}), genres (list of str), search_query (str), selected_genre (str)             |
| /songs/<int:song_id>          | song_details_page         | GET            | song_details.html       | song (dict with keys: song_id:int, title:str, artist_id:int, artist_name:str, album_id:int, album_name:str, genre:str, duration:int),                                                         |
|                              |                          |                |                         | release_date:str, play_count:int), artist_profile_url (str)                                                                                |
| /playlists                   | playlists_page            | GET            | playlists.html          | playlists (list of dict{playlist_id:int, title:str, description:str, total_songs:int}), navigation_buttons (dict)                         |
| /playlists/create            | create_playlist_page      | GET            | create_playlist.html    | None                                                                                                                                      |
| /playlists/create            | create_playlist_submit    | POST           | N/A                     | Form Data: playlist_name (str), playlist_description (str)                                                                                |
| /playlists/<int:playlist_id> | playlist_details_page     | GET            | playlist_details.html   | playlist (dict{playlist_id:int, title:str, description:str}), songs (list of dict{song_id:int, title:str, artist_name:str, duration:int}),                                                    |
|                              |                          |                |                         | total_songs:int                                                                                                                           |
| /playlists/<int:playlist_id>/delete | delete_playlist          | POST           | N/A                     | playlist_id:int                                                                                                                           |
| /playlists/<int:playlist_id>/remove_song/<int:song_id> | remove_song_from_playlist | POST           | N/A                     | playlist_id:int, song_id:int                                                                                                              |
| /albums                      | albums_page               | GET            | albums.html             | albums (list of dict{album_id:int, title:str, artist_name:str, year:int}), search_query (str), sort_by (str)                              |
| /albums/<int:album_id>        | album_details_page        | GET            | album_details.html      | album (dict{album_id:int, title:str, artist_id:int, artist_name:str, release_year:int, total_songs:int, genre:str}), songs (list of dict{song_id:int, title:str, duration:int})            |
| /albums/<int:album_id>/add_to_playlist | add_album_to_playlist     | POST           | N/A                     | album_id:int, target_playlist_id:int (from form data)                                                                                     |
| /artists                     | artists_page              | GET            | artists.html            | artists (list of dict{artist_id:int, name:str, genre:str, country:str}), search_query (str), sort_by (str)                                 |
| /artists/<int:artist_id>      | artist_profile_page       | GET            | artist_profile.html     | artist (dict{artist_id:int, name:str, genre:str, country:str, formation_year:int}), songs (list of dict{song_id:int, title:str, album_name:str, duration:int})                              |
| /genres                      | genre_exploration_page    | GET            | genres.html             | genres (list of str), selected_genre (str), genre_songs (list of dict{song_id:int, title:str, artist_name:str, duration:int}), genre_artists (list of dict{artist_id:int, name:str})        |


---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. dashboard.html
- Template File Path: templates/dashboard.html
- Page Title: 
  - <title>Music Streaming Dashboard</title>
  - <h1 id="dashboard-header">Music Streaming Dashboard</h1>  (implied but not specified, the container div is given)
- Required Element IDs:
  - dashboard-page (Div)
  - featured-songs (Div)
  - browse-songs-button (Button)
  - my-playlists-button (Button)
  - trending-artists-button (Button)
- Context Variables:
  - featured_songs: list of dict with keys {song_id (int), title (str), artist_name (str), duration (int)}
  - trending_artists: list of dict with keys {artist_id (int), name (str)}
- Navigation Mappings:
  - browse-songs-button -> song_catalog_page
  - my-playlists-button -> playlists_page
  - trending-artists-button -> artists_page

### 2. song_catalog.html
- Template File Path: templates/song_catalog.html
- Page Title:
  - <title>Song Catalog</title>
  - (No explicit h1 specified)
- Required Element IDs:
  - catalog-page (Div)
  - search-input (Input)
  - genre-filter (Dropdown)
  - songs-grid (Div)  (contains multiple add-to-playlist-button-{song_id} Buttons dynamically)
  - add-to-playlist-button-{song_id} (Button) (dynamic ids per song)
- Context Variables:
  - songs: list of dict with keys {song_id (int), title (str), artist_name (str), album_name (str), genre (str), duration (int)}
  - genres: list of str
  - search_query: str
  - selected_genre: str
- Navigation Mappings:
  - add-to-playlist-button-{song_id} -> action to add that song to playlist (Form submit or AJAX, backend route not direct)

### 3. song_details.html
- Template File Path: templates/song_details.html
- Page Title:
  - <title>Song Details</title>
  - <h1 id="song-title">{{ song.title }}</h1>
- Required Element IDs:
  - song-details-page (Div)
  - song-title (H1)
  - artist-name (Div with link to artist profile)
  - album-name (Div)
  - duration-display (Div)
  - play-button (Button)
- Context Variables:
  - song: dict with keys {song_id (int), title (str), artist_id (int), artist_name (str), album_id (int), album_name (str), genre (str), duration (int), release_date (str), play_count (int)}
  - artist_profile_url: str
- Navigation Mappings:
  - artist-name (link) -> artist_profile_page with artist_id
  - play-button -> action to play the song (client-side interaction, no route)

### 4. playlists.html
- Template File Path: templates/playlists.html
- Page Title:
  - <title>My Playlists</title>
  - (No explicit h1 specified, but container div is playlists-page)
- Required Element IDs:
  - playlists-page (Div)
  - playlists-grid (Div) (contains multiple view-playlist-button-{playlist_id} Buttons dynamically)
  - create-playlist-button (Button)
  - back-to-dashboard (Button)
  - view-playlist-button-{playlist_id} (Button) dynamic ids
- Context Variables:
  - playlists: list of dict with keys {playlist_id (int), title (str), description (str), total_songs (int)}
- Navigation Mappings:
  - create-playlist-button -> create_playlist_page
  - back-to-dashboard -> dashboard_page
  - view-playlist-button-{playlist_id} -> playlist_details_page with playlist_id

### 5. playlist_details.html
- Template File Path: templates/playlist_details.html
- Page Title:
  - <title>Playlist Details</title>
  - <h1 id="playlist-title">{{ playlist.title }}</h1>
- Required Element IDs:
  - playlist-details-page (Div)
  - playlist-title (H1)
  - playlist-description (Div)
  - songs-in-playlist (Table) (rows with remove-song-button-{song_id} Buttons dynamically)
  - remove-song-button-{song_id} (Button) dynamic ids
  - delete-playlist-button (Button)
- Context Variables:
  - playlist: dict with keys {playlist_id (int), title (str), description (str)}
  - songs: list of dict with keys {song_id (int), title (str), artist_name (str), duration (int)}
  - total_songs: int
- Navigation Mappings:
  - remove-song-button-{song_id} -> remove_song_from_playlist route with playlist_id and song_id
  - delete-playlist-button -> delete_playlist route with playlist_id

### 6. create_playlist.html
- Template File Path: templates/create_playlist.html
- Page Title:
  - <title>Create New Playlist</title>
  - (No explicit h1 specified, container div id="create-playlist-page")
- Required Element IDs:
  - create-playlist-page (Div)
  - playlist-name-input (Input)
  - playlist-description-input (Textarea)
  - save-playlist-button (Button)
  - cancel-create-button (Button)
- Context Variables:
  - None
- Navigation Mappings:
  - save-playlist-button -> form submission to create_playlist_submit
  - cancel-create-button -> go back to playlists_page

### 7. albums.html
- Template File Path: templates/albums.html
- Page Title:
  - <title>Albums</title>
  - (No explicit h1 specified, container div id="albums-page")
- Required Element IDs:
  - albums-page (Div)
  - albums-grid (Div) (contains multiple view-album-button-{album_id} Buttons dynamically)
  - search-albums (Input)
  - sort-albums (Dropdown)
  - view-album-button-{album_id} (Button) dynamic ids
- Context Variables:
  - albums: list of dict with keys {album_id (int), title (str), artist_name (str), year (int)}
  - search_query: str
  - sort_by: str
- Navigation Mappings:
  - view-album-button-{album_id} -> album_details_page with album_id

### 8. album_details.html
- Template File Path: templates/album_details.html
- Page Title:
  - <title>Album Details</title>
  - <h1 id="album-title">{{ album.title }}</h1>
- Required Element IDs:
  - album-details-page (Div)
  - album-title (H1)
  - album-artist (Div)
  - album-year (Div)
  - album-songs-list (Div)
  - add-album-to-playlist-button (Button)
- Context Variables:
  - album: dict with keys {album_id (int), title (str), artist_id (int), artist_name (str), release_year (int), total_songs (int), genre (str)}
  - songs: list of dict with keys {song_id (int), title (str), duration (int)}
- Navigation Mappings:
  - add-album-to-playlist-button -> form submission to add_album_to_playlist route

### 9. artists.html
- Template File Path: templates/artists.html
- Page Title:
  - <title>Artist Profiles</title>
  - (No explicit h1 specified, container div id="artists-page")
- Required Element IDs:
  - artists-page (Div)
  - artists-grid (Div) (contains multiple view-artist-button-{artist_id} Buttons dynamically)
  - search-artists (Input)
  - artists-sort (Dropdown)
  - view-artist-button-{artist_id} (Button) dynamic ids
- Context Variables:
  - artists: list of dict with keys {artist_id (int), name (str), genre (str), country (str)}
  - search_query: str
  - sort_by: str
- Navigation Mappings:
  - view-artist-button-{artist_id} -> artist_profile_page with artist_id

### 10. genres.html
- Template File Path: templates/genres.html
- Page Title:
  - <title>Genre Exploration</title>
  - (No explicit h1 specified, container div id="genres-page")
- Required Element IDs:
  - genres-page (Div)
  - genres-list (Div)
  - select-genre (Dropdown)
  - genre-songs (Div)
  - genre-artists (Div)
  - back-to-dashboard (Button)
- Context Variables:
  - genres: list of str
  - selected_genre: str
  - genre_songs: list of dict{song_id (int), title (str), artist_name (str), duration (int)}
  - genre_artists: list of dict{artist_id (int), name (str)}
- Navigation Mappings:
  - back-to-dashboard -> dashboard_page


---

## Section 3: Data File Schemas (For Backend Developer)

### 1. data/songs.txt
- File format: pipe-delimited (|)
- Fields:
  1. song_id (int): Unique identifier for song
  2. title (str): Title of the song
  3. artist_id (int): Reference to artist (foreign key from artists.txt)
  4. album_id (int): Reference to album (foreign key from albums.txt)
  5. genre (str): Genre name
  6. duration (int): Duration in seconds
  7. release_date (str): Release date in YYYY-MM-DD
  8. play_count (int): Number of times played
- Example rows:
  - 1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
  - 2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
  - 3|Shape of You|3|3|Pop|233|2017-01-06|4200000

### 2. data/artists.txt
- File format: pipe-delimited (|)
- Fields:
  1. artist_id (int): Unique identifier for artist
  2. name (str): Artist name
  3. genre (str): Primary genre
  4. country (str): Country of origin
  5. formation_year (int): Year band/artist formed
- Example rows:
  - 1|Queen|Rock|United Kingdom|1970
  - 2|The Weeknd|Synth-Pop|Canada|2010
  - 3|Ed Sheeran|Pop|United Kingdom|2005

### 3. data/albums.txt
- File format: pipe-delimited (|)
- Fields:
  1. album_id (int): Unique identifier for album
  2. title (str): Album title
  3. artist_id (int): Reference to artist (foreign key)
  4. release_year (int): Year of release
  5. total_songs (int): Number of songs in the album
  6. genre (str): Genre of album
- Example rows:
  - 1|A Night at the Opera|1|1975|11|Rock
  - 2|After Hours|2|2019|14|Synth-Pop
  - 3|Divide|3|2017|12|Pop

### 4. data/genres.txt
- File format: pipe-delimited (|)
- Fields:
  1. genre_id (int): Unique identifier for genre
  2. genre_name (str): Name of genre
  3. description (str): Description of genre
- Example rows:
  - 1|Rock|Guitar-driven music with strong beats and vocals
  - 2|Pop|Catchy mainstream music with broad appeal
  - 3|Hip-Hop|Rhythmic music with rap vocals and beat production

### 5. data/playlists.txt
- File format: pipe-delimited (|)
- Fields:
  1. playlist_id (int): Unique identifier for playlist
  2. title (str): Playlist title
  3. description (str): Description of playlist
  4. creation_date (str): Date created YYYY-MM-DD
  5. total_songs (int): Number of songs in playlist
- Example rows:
  - 1|Workout Mix|High energy songs for the gym|2025-01-15|25
  - 2|Chill Vibes|Relaxing music for study|2025-01-16|18
  - 3|Party Hits|Latest party tracks|2025-01-17|32

### 6. data/playlist_songs.txt
- File format: pipe-delimited (|)
- Fields:
  1. playlist_song_id (int): Unique identifier for playlist-song link
  2. playlist_id (int): Reference to playlist
  3. song_id (int): Reference to song
  4. added_date (str): Date added YYYY-MM-DD
- Example rows:
  - 1|1|2|2025-01-15
  - 2|1|3|2025-01-15
  - 3|2|1|2025-01-16

---

This specification document is intended to fully enable backend and frontend developers to build their respective parts independently and cohesively for the MusicStreaming application.