# MusicStreaming Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                      | Function Name             | HTTP Method(s) | Template File           | Context Variables                                                                                                     |
|--------------------------------|---------------------------|----------------|-------------------------|-----------------------------------------------------------------------------------------------------------------------|
| /                              | root_redirect              | GET            | None (redirect)          | None                                                                                                                  |
| /dashboard                     | dashboard_page             | GET            | dashboard.html           | featured_songs (list of dict: {song_id:int, title:str, artist:str, duration:int}), trending_artists (list of dict: {artist_id:int, name:str}) |
| /songs                        | song_catalog_page          | GET            | song_catalog.html        | songs (list of dict: {song_id:int, title:str, artist:str, album:str, genre:str, duration:int}), genres (list of str)  |
| /songs/<int:song_id>          | song_details_page          | GET            | song_details.html        | song (dict: {song_id:int, title:str, artist:str, album:str, duration:int}), artist (dict: {artist_id:int, name:str})      |
| /playlists                    | playlists_page             | GET            | playlists.html           | playlists (list of dict: {playlist_id:int, title:str, song_count:int})                                              |
| /playlists/create             | create_playlist_page       | GET, POST      | create_playlist.html     | On GET: None; On POST: form data expected to create playlist                                                          |
| /playlists/<int:playlist_id>  | playlist_details_page      | GET            | playlist_details.html    | playlist (dict: {playlist_id:int, title:str, description:str}), songs_in_playlist (list of dict: {song_id:int, title:str, artist:str, duration:int}) |
| /playlists/<int:playlist_id>/delete | delete_playlist       | POST           | None                    | playlist_id (int) from URL to delete playlist                                                                         |
| /playlists/<int:playlist_id>/remove_song/<int:song_id> | remove_song_from_playlist | POST           | None                    | playlist_id (int), song_id (int) to remove from playlist                                                               |
| /albums                      | albums_page                | GET            | albums.html              | albums (list of dict: {album_id:int, title:str, artist:str, year:int})                                              |
| /albums/<int:album_id>        | album_details_page         | GET            | album_details.html       | album (dict: {album_id:int, title:str, artist:str, year:int}), songs_in_album (list of dict: {song_id:int, title:str, duration:int}) |
| /albums/<int:album_id>/add_to_playlist | add_album_songs_to_playlist | POST           | None                    | album_id (int) to add all songs of album to playlist                                                                   |
| /artists                     | artists_page               | GET            | artists.html             | artists (list of dict: {artist_id:int, name:str, genre:str})                                                           |
| /artists/<int:artist_id>      | artist_profile_page        | GET            | artist_profile.html      | artist (dict: {artist_id:int, name:str, genre:str, country:str, formation_year:int}), artist_songs (list of dict: {song_id:int, title:str, album:str, duration:int}) |
| /genres                      | genres_page                | GET            | genres.html              | genres (list of dict: {genre_id:int, genre_name:str, description:str}), genre_songs (list of dict: {song_id:int, title:str, artist:str}), genre_artists (list of dict: {artist_id:int, name:str}) |

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. Dashboard Page
- Template File Path: templates/dashboard.html
- Page Title:
  - <title>: Music Streaming Dashboard
  - <h1>: Music Streaming Dashboard
- Required Element IDs:
  - dashboard-page (Div)
  - featured-songs (Div)
  - browse-songs-button (Button)
  - my-playlists-button (Button)
  - trending-artists-button (Button)
- Context Variables:
  - featured_songs: list of dictionaries containing song_id (int), title (str), artist (str), duration (int)
  - trending_artists: list of dictionaries containing artist_id (int), name (str)
- Navigation Mappings:
  - browse-songs-button: song_catalog_page (route function)
  - my-playlists-button: playlists_page (route function)
  - trending-artists-button: artists_page (route function)

### 2. Song Catalog Page
- Template File Path: templates/song_catalog.html
- Page Title:
  - <title>: Song Catalog
  - <h1>: Song Catalog
- Required Element IDs:
  - catalog-page (Div)
  - search-input (Input)
  - genre-filter (Dropdown)
  - songs-grid (Div)
  - add-to-playlist-button-{{ song_id }} (Button) - dynamic per song
- Context Variables:
  - songs: list of dictionaries with keys song_id (int), title (str), artist (str), album (str), genre (str), duration (int)
  - genres: list of strings
- Navigation Mappings:
  - add-to-playlist-button-{{ song_id }}: add song to playlist action (POST handled via route)

### 3. Song Details Page
- Template File Path: templates/song_details.html
- Page Title:
  - <title>: Song Details
  - <h1>: Song Details
- Required Element IDs:
  - song-details-page (Div)
  - song-title (H1)
  - artist-name (Div)
  - album-name (Div)
  - duration-display (Div)
  - play-button (Button)
- Context Variables:
  - song: dict with keys song_id (int), title (str), artist (str), album (str), duration (int)
  - artist: dict with keys artist_id (int), name (str)
- Navigation Mappings:
  - artist-name link directs to artist_profile_page with artist_id
  - play-button triggers play action for the song

### 4. Playlist Page
- Template File Path: templates/playlists.html
- Page Title:
  - <title>: My Playlists
  - <h1>: My Playlists
- Required Element IDs:
  - playlists-page (Div)
  - playlists-grid (Div)
  - create-playlist-button (Button)
  - view-playlist-button-{{ playlist_id }} (Button) - dynamic per playlist
  - back-to-dashboard (Button)
- Context Variables:
  - playlists: list of dictionaries with playlist_id (int), title (str), song_count (int)
- Navigation Mappings:
  - create-playlist-button: create_playlist_page
  - view-playlist-button-{{ playlist_id }}: playlist_details_page with playlist_id
  - back-to-dashboard: dashboard_page

### 5. Playlist Details Page
- Template File Path: templates/playlist_details.html
- Page Title:
  - <title>: Playlist Details
  - <h1>: Playlist Details
- Required Element IDs:
  - playlist-details-page (Div)
  - playlist-title (H1)
  - playlist-description (Div)
  - songs-in-playlist (Table)
  - remove-song-button-{{ song_id }} (Button) - dynamic per song
  - delete-playlist-button (Button)
- Context Variables:
  - playlist: dict with keys playlist_id (int), title (str), description (str)
  - songs_in_playlist: list of dict with song_id (int), title (str), artist (str), duration (int)
- Navigation Mappings:
  - remove-song-button-{{ song_id }}: remove_song_from_playlist route with song_id and playlist_id
  - delete-playlist-button: delete_playlist route with playlist_id

### 6. Create Playlist Page
- Template File Path: templates/create_playlist.html
- Page Title:
  - <title>: Create New Playlist
  - <h1>: Create New Playlist
- Required Element IDs:
  - create-playlist-page (Div)
  - playlist-name-input (Input)
  - playlist-description-input (Textarea)
  - save-playlist-button (Button)
  - cancel-create-button (Button)
- Context Variables:
  - None for GET
- Navigation Mappings:
  - save-playlist-button: form submission to create_playlist_page (POST)
  - cancel-create-button: back to playlists_page

### 7. Album Browse Page
- Template File Path: templates/albums.html
- Page Title:
  - <title>: Albums
  - <h1>: Albums
- Required Element IDs:
  - albums-page (Div)
  - albums-grid (Div)
  - search-albums (Input)
  - sort-albums (Dropdown)
  - view-album-button-{{ album_id }} (Button) - dynamic per album
- Context Variables:
  - albums: list of dict with album_id (int), title (str), artist (str), year (int)
- Navigation Mappings:
  - view-album-button-{{ album_id }}: album_details_page with album_id

### 8. Album Details Page
- Template File Path: templates/album_details.html
- Page Title:
  - <title>: Album Details
  - <h1>: Album Details
- Required Element IDs:
  - album-details-page (Div)
  - album-title (H1)
  - album-artist (Div)
  - album-year (Div)
  - album-songs-list (Div)
  - add-album-to-playlist-button (Button)
- Context Variables:
  - album: dict with album_id (int), title (str), artist (str), year (int)
  - songs_in_album: list of dict with song_id (int), title (str), duration (int)
- Navigation Mappings:
  - add-album-to-playlist-button: POST to add_album_songs_to_playlist with album_id

### 9. Artist Profile Page
- Template File Path: templates/artists.html
- Page Title:
  - <title>: Artist Profiles
  - <h1>: Artist Profiles
- Required Element IDs:
  - artists-page (Div)
  - artists-grid (Div)
  - search-artists (Input)
  - artists-sort (Dropdown)
  - view-artist-button-{{ artist_id }} (Button) - dynamic per artist
- Context Variables:
  - artists: list of dict with artist_id (int), name (str), genre (str)
- Navigation Mappings:
  - view-artist-button-{{ artist_id }}: artist_profile_page with artist_id

### 10. Genre Exploration Page
- Template File Path: templates/genres.html
- Page Title:
  - <title>: Genre Exploration
  - <h1>: Genre Exploration
- Required Element IDs:
  - genres-page (Div)
  - genres-list (Div)
  - select-genre (Dropdown)
  - genre-songs (Div)
  - genre-artists (Div)
  - back-to-dashboard (Button)
- Context Variables:
  - genres: list of dict with genre_id (int), genre_name (str), description (str)
  - genre_songs: list of dict with song_id (int), title (str), artist (str)
  - genre_artists: list of dict with artist_id (int), name (str)
- Navigation Mappings:
  - back-to-dashboard: dashboard_page

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. Songs Data
- Filename and Path: data/songs.txt
- File Format: Pipe-delimited (|)
- Fields (in order):
  - song_id (int): Unique song identifier
  - title (str): Title of the song
  - artist_id (int): Reference to artist in artists.txt
  - album_id (int): Reference to album in albums.txt
  - genre (str): Genre name
  - duration (int): Duration in seconds
  - release_date (str, ISO YYYY-MM-DD): Song release date
  - play_count (int): Number of times song has been played
- Example Rows:
  1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
  2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
  3|Shape of You|3|3|Pop|233|2017-01-06|4200000

### 2. Artists Data
- Filename and Path: data/artists.txt
- File Format: Pipe-delimited (|)
- Fields (in order):
  - artist_id (int): Unique artist identifier
  - name (str): Artist's name
  - genre (str): Primary genre
  - country (str): Country of origin
  - formation_year (int): Year artist/band formed
- Example Rows:
  1|Queen|Rock|United Kingdom|1970
  2|The Weeknd|Synth-Pop|Canada|2010
  3|Ed Sheeran|Pop|United Kingdom|2005

### 3. Albums Data
- Filename and Path: data/albums.txt
- File Format: Pipe-delimited (|)
- Fields (in order):
  - album_id (int): Unique album identifier
  - title (str): Album title
  - artist_id (int): Reference to artist in artists.txt
  - release_year (int): Year album was released
  - total_songs (int): Number of songs on album
  - genre (str): Genre of album
- Example Rows:
  1|A Night at the Opera|1|1975|11|Rock
  2|After Hours|2|2019|14|Synth-Pop
  3|Divide|3|2017|12|Pop

### 4. Genres Data
- Filename and Path: data/genres.txt
- File Format: Pipe-delimited (|)
- Fields (in order):
  - genre_id (int): Unique genre identifier
  - genre_name (str): Name of genre
  - description (str): Genre description
- Example Rows:
  1|Rock|Guitar-driven music with strong beats and vocals
  2|Pop|Catchy mainstream music with broad appeal
  3|Hip-Hop|Rhythmic music with rap vocals and beat production

### 5. Playlists Data
- Filename and Path: data/playlists.txt
- File Format: Pipe-delimited (|)
- Fields (in order):
  - playlist_id (int): Unique playlist identifier
  - title (str): Playlist title
  - description (str): Playlist description
  - creation_date (str, ISO YYYY-MM-DD): Date playlist was created
  - total_songs (int): Number of songs in playlist
- Example Rows:
  1|Workout Mix|High energy songs for the gym|2025-01-15|25
  2|Chill Vibes|Relaxing music for study|2025-01-16|18
  3|Party Hits|Latest party tracks|2025-01-17|32

### 6. Playlist Songs Data
- Filename and Path: data/playlist_songs.txt
- File Format: Pipe-delimited (|)
- Fields (in order):
  - playlist_song_id (int): Unique identifier for playlist-song link
  - playlist_id (int): Reference to playlist in playlists.txt
  - song_id (int): Reference to song in songs.txt
  - added_date (str, ISO YYYY-MM-DD): Date song was added to playlist
- Example Rows:
  1|1|2|2025-01-15
  2|1|3|2025-01-15
  3|2|1|2025-01-16

---

_End of MusicStreaming Application Design Specifications_