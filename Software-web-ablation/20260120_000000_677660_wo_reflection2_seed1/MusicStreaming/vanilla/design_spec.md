# MusicStreaming Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                    | Function Name           | HTTP Method(s) | Template File          | Context Variables                                                                                                 |
|-------------------------------|------------------------|----------------|------------------------|------------------------------------------------------------------------------------------------------------------|
| /                             | root_redirect           | GET            | N/A (redirect)          | None                                                                                                             |
| /dashboard                    | dashboard              | GET            | dashboard.html          | featured_songs: List[Dict] with keys {song_id:int, title:str, artist_name:str, duration:int}
  trending_artists: List[Dict] with keys {artist_id:int, name:str}                                                                                |
| /songs                       | song_catalog           | GET            | song_catalog.html       | songs: List[Dict] with keys {song_id:int, title:str, artist_name:str, album_name:str, genre:str, duration:int}
  genres: List[str] (genre names for filter dropdown)                                    |
| /songs/<int:song_id>         | song_details           | GET            | song_details.html       | song: Dict {song_id:int, title:str, artist_id:int, artist_name:str, album_id:int, album_name:str, duration:int}
  (Plus other song fields as needed for display)                                                               |
| /playlists                   | playlists_page         | GET            | playlists.html          | playlists: List[Dict] with keys {playlist_id:int, title:str, description:str, total_songs:int}                      |
| /playlists/create            | create_playlist        | GET, POST      | create_playlist.html    | (GET) None
(POST) Processing form data; if errors, pass error messages, else redirect                                      |
| /playlists/<int:playlist_id> | playlist_details       | GET            | playlist_details.html   | playlist: Dict {playlist_id:int, title:str, description:str}
  songs: List[Dict] with keys {song_id:int, title:str, artist_name:str, duration:int}                                                          |
| /albums                     | albums_page            | GET            | albums.html             | albums: List[Dict] with keys {album_id:int, title:str, artist_name:str, year:int}                                  |
| /albums/<int:album_id>       | album_details          | GET            | album_details.html      | album: Dict {album_id:int, title:str, artist_id:int, artist_name:str, release_year:int}
  songs: List[Dict] with keys {song_id:int, title:str, duration:int}                                                                |
| /artists                    | artists_page           | GET            | artists.html            | artists: List[Dict] with keys {artist_id:int, name:str, genre:str}                                                |
| /artists/<int:artist_id>      | artist_profile         | GET            | artist_profile.html     | artist: Dict {artist_id:int, name:str, genre:str, country:str, formation_year:int}                                 |
| /genres                     | genre_exploration      | GET            | genres.html             | genres: List[Dict] with keys {genre_id:int, genre_name:str, description:str}
  selected_genre_id: Optional[int] (if query parameter present)
  genre_songs: List[Dict] with keys {song_id:int, title:str, artist_name:str} (if genre selected)
  genre_artists: List[Dict] with keys {artist_id:int, name:str} (if genre selected)                                           |


---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. dashboard.html
- Template File Path: templates/dashboard.html
- Page Title: <title>Music Streaming Dashboard</title>
- <h1>: Music Streaming Dashboard
- Required Element IDs:
  - dashboard-page (Div)
  - featured-songs (Div)
  - browse-songs-button (Button)
  - my-playlists-button (Button)
  - trending-artists-button (Button)
- Context Variables:
  - featured_songs: List of song dicts with keys: song_id, title, artist_name, duration (int seconds)
  - trending_artists: List of artist dicts with keys: artist_id, name
- Navigation Mappings:
  - browse-songs-button -> song_catalog
  - my-playlists-button -> playlists_page
  - trending-artists-button -> artists_page


### 2. song_catalog.html
- Template File Path: templates/song_catalog.html
- Page Title: <title>Song Catalog</title>
- <h1>: Song Catalog
- Required Element IDs:
  - catalog-page (Div)
  - search-input (Input)
  - genre-filter (Dropdown)
  - songs-grid (Div)
  - add-to-playlist-button-{{ song.song_id }} (Button for each song card)
- Context Variables:
  - songs: List of dicts with {song_id, title, artist_name, album_name, genre, duration}
  - genres: List of genre strings for dropdown
- Navigation Mappings:
  - add-to-playlist-button-{{ song_id }} triggers adding that song to playlist (POST or JS action)


### 3. song_details.html
- Template File Path: templates/song_details.html
- Page Title: <title>Song Details</title>
- <h1>: song.title
- Required Element IDs:
  - song-details-page (Div)
  - song-title (H1)
  - artist-name (Div, clickable link to artist_profile)
  - album-name (Div)
  - duration-display (Div)
  - play-button (Button)
- Context Variables:
  - song: Dict with keys {song_id, title, artist_id, artist_name, album_id, album_name, duration}
- Navigation Mappings:
  - artist-name -> artist_profile(song.artist_id)


### 4. playlists.html
- Template File Path: templates/playlists.html
- Page Title: <title>My Playlists</title>
- <h1>: My Playlists
- Required Element IDs:
  - playlists-page (Div)
  - playlists-grid (Div)
  - create-playlist-button (Button)
  - view-playlist-button-{{ playlist.playlist_id }} (Button for each playlist card)
  - back-to-dashboard (Button)
- Context Variables:
  - playlists: List of dicts with {playlist_id, title, description, total_songs}
- Navigation Mappings:
  - create-playlist-button -> create_playlist(GET)
  - view-playlist-button-{{ playlist_id }} -> playlist_details(playlist_id)
  - back-to-dashboard -> dashboard


### 5. playlist_details.html
- Template File Path: templates/playlist_details.html
- Page Title: <title>Playlist Details</title>
- <h1>: playlist.title
- Required Element IDs:
  - playlist-details-page (Div)
  - playlist-title (H1)
  - playlist-description (Div)
  - songs-in-playlist (Table)
  - remove-song-button-{{ song.song_id }} (Button per song row)
  - delete-playlist-button (Button)
- Context Variables:
  - playlist: Dict {playlist_id, title, description}
  - songs: List of dicts {song_id, title, artist_name, duration}
- Navigation Mappings:
  - remove-song-button-{{ song_id }} triggers removal action
  - delete-playlist-button triggers playlist deletion


### 6. create_playlist.html
- Template File Path: templates/create_playlist.html
- Page Title: <title>Create New Playlist</title>
- <h1>: Create New Playlist
- Required Element IDs:
  - create-playlist-page (Div)
  - playlist-name-input (Input)
  - playlist-description-input (Textarea)
  - save-playlist-button (Button)
  - cancel-create-button (Button)
- Context Variables:
  - None or error messages on POST validation failures
- Navigation Mappings:
  - save-playlist-button triggers POST form submission
  - cancel-create-button navigates back (usually to playlists_page)


### 7. albums.html
- Template File Path: templates/albums.html
- Page Title: <title>Albums</title>
- <h1>: Albums
- Required Element IDs:
  - albums-page (Div)
  - albums-grid (Div)
  - search-albums (Input)
  - sort-albums (Dropdown)
  - view-album-button-{{ album.album_id }} (Button per album card)
- Context Variables:
  - albums: List of dicts {album_id, title, artist_name, year}
- Navigation Mappings:
  - view-album-button-{{ album_id }} -> album_details(album_id)


### 8. album_details.html
- Template File Path: templates/album_details.html
- Page Title: <title>Album Details</title>
- <h1>: album.title
- Required Element IDs:
  - album-details-page (Div)
  - album-title (H1)
  - album-artist (Div)
  - album-year (Div)
  - album-songs-list (Div)
  - add-album-to-playlist-button (Button)
- Context Variables:
  - album: Dict {album_id, title, artist_id, artist_name, release_year}
  - songs: List of dicts {song_id, title, duration}
- Navigation Mappings:
  - add-album-to-playlist-button triggers adding all album songs to playlist


### 9. artists.html
- Template File Path: templates/artists.html
- Page Title: <title>Artist Profiles</title>
- <h1>: Artist Profiles
- Required Element IDs:
  - artists-page (Div)
  - artists-grid (Div)
  - search-artists (Input)
  - artists-sort (Dropdown)
  - view-artist-button-{{ artist.artist_id }} (Button per artist card)
- Context Variables:
  - artists: List of dicts {artist_id, name, genre}
- Navigation Mappings:
  - view-artist-button-{{ artist_id }} -> artist_profile(artist_id)


### 10. genres.html
- Template File Path: templates/genres.html
- Page Title: <title>Genre Exploration</title>
- <h1>: Genre Exploration
- Required Element IDs:
  - genres-page (Div)
  - genres-list (Div)
  - select-genre (Dropdown)
  - genre-songs (Div)
  - genre-artists (Div)
  - back-to-dashboard (Button)
- Context Variables:
  - genres: List of dicts {genre_id, genre_name, description}
  - selected_genre_id: Optional[int]
  - genre_songs: List of dicts {song_id, title, artist_name} if genre selected
  - genre_artists: List of dicts {artist_id, name} if genre selected
- Navigation Mappings:
  - back-to-dashboard -> dashboard


---

## Section 3: Data File Schemas (For Backend Developer)

### 1. songs.txt
- Path: data/songs.txt
- Format: Pipe-delimited (|)
- Fields:
  1. song_id (int): Unique identifier for each song
  2. title (str): Song title
  3. artist_id (int): Foreign key to artists.txt artist_id
  4. album_id (int): Foreign key to albums.txt album_id
  5. genre (str): Genre name (e.g., Rock, Pop)
  6. duration (int): Duration in seconds
  7. release_date (str): Date in YYYY-MM-DD
  8. play_count (int): Number of times song played
- Example Rows:
  1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
  2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
  3|Shape of You|3|3|Pop|233|2017-01-06|4200000


### 2. artists.txt
- Path: data/artists.txt
- Format: Pipe-delimited (|)
- Fields:
  1. artist_id (int): Unique identifier for each artist
  2. name (str): Artist name
  3. genre (str): Primary genre
  4. country (str): Country of origin
  5. formation_year (int): Year band or artist formed
- Example Rows:
  1|Queen|Rock|United Kingdom|1970
  2|The Weeknd|Synth-Pop|Canada|2010
  3|Ed Sheeran|Pop|United Kingdom|2005


### 3. albums.txt
- Path: data/albums.txt
- Format: Pipe-delimited (|)
- Fields:
  1. album_id (int): Unique album identifier
  2. title (str): Album title
  3. artist_id (int): Foreign key to artists.txt artist_id
  4. release_year (int): Year album released
  5. total_songs (int): Number of songs in album
  6. genre (str): Genre of album
- Example Rows:
  1|A Night at the Opera|1|1975|11|Rock
  2|After Hours|2|2019|14|Synth-Pop
  3|Divide|3|2017|12|Pop


### 4. genres.txt
- Path: data/genres.txt
- Format: Pipe-delimited (|)
- Fields:
  1. genre_id (int): Unique genre ID
  2. genre_name (str): Name of genre
  3. description (str): Description of genre
- Example Rows:
  1|Rock|Guitar-driven music with strong beats and vocals
  2|Pop|Catchy mainstream music with broad appeal
  3|Hip-Hop|Rhythmic music with rap vocals and beat production


### 5. playlists.txt
- Path: data/playlists.txt
- Format: Pipe-delimited (|)
- Fields:
  1. playlist_id (int): Unique playlist ID
  2. title (str): Playlist title
  3. description (str): Description of playlist
  4. creation_date (str): Date playlist created (YYYY-MM-DD)
  5. total_songs (int): Number of songs in playlist
- Example Rows:
  1|Workout Mix|High energy songs for the gym|2025-01-15|25
  2|Chill Vibes|Relaxing music for study|2025-01-16|18
  3|Party Hits|Latest party tracks|2025-01-17|32


### 6. playlist_songs.txt
- Path: data/playlist_songs.txt
- Format: Pipe-delimited (|)
- Fields:
  1. playlist_song_id (int): Unique ID for the playlist-song relation
  2. playlist_id (int): Foreign key to playlists.txt playlist_id
  3. song_id (int): Foreign key to songs.txt song_id
  4. added_date (str): Date song was added (YYYY-MM-DD)
- Example Rows:
  1|1|2|2025-01-15
  2|1|3|2025-01-15
  3|2|1|2025-01-16


---

**End of Design Specification**
