# MusicStreaming Application Design Specifications

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path | Function Name | HTTP Method(s) | Template File | Context Variables |
|------------|---------------|----------------|---------------|-------------------|
| / | root_redirect | GET | None (redirect) | None |
| /dashboard | dashboard_page | GET | dashboard.html | featured_songs: list of dict {song_id: int, title: str, artist_name: str, album_name: str, duration: int}, trending_artists: list of dict {artist_id: int, name: str} |
| /songs | song_catalog_page | GET, POST | song_catalog.html | songs: list of dict {song_id: int, title: str, artist_name: str, album_name: str, duration: int, genre: str}, genres: list of str, search_query: str (from POST or GET), selected_genre: str or None |
| /songs/<int:song_id> | song_details_page | GET | song_details.html | song: dict {song_id: int, title: str, artist_id: int, artist_name: str, album_id: int, album_name: str, duration: int, genre: str, release_date: str, play_count: int} |
| /playlists | playlists_page | GET | playlists.html | playlists: list of dict {playlist_id: int, title: str, description: str, total_songs: int} |
| /playlists/<int:playlist_id> | playlist_details_page | GET | playlist_details.html | playlist: dict {playlist_id: int, title: str, description: str}, songs_in_playlist: list of dict {song_id: int, title: str, artist_name: str, duration: int} |
| /playlists/create | create_playlist_page | GET, POST | create_playlist.html | None or form data: playlist_name: str, playlist_description: str |
| /albums | albums_page | GET, POST | albums.html | albums: list of dict {album_id: int, title: str, artist_name: str, release_year: int, genre: str}, search_query: str (from POST or GET), sort_option: str (e.g., 'Title', 'Artist', 'Year') |
| /albums/<int:album_id> | album_details_page | GET | album_details.html | album: dict {album_id: int, title: str, artist_name: str, release_year: int}, songs_in_album: list of dict {song_id: int, title: str, duration: int} |
| /artists | artists_page | GET, POST | artists.html | artists: list of dict {artist_id: int, name: str, genre: str, country: str}, search_query: str (from POST or GET), sort_option: str (e.g., 'Name', 'Genre') |
| /artists/<int:artist_id> | artist_profile_page | GET | artist_profile.html | artist: dict {artist_id: int, name: str, genre: str, country: str, formation_year: int}, songs_by_artist: list of dict {song_id: int, title: str, album_name: str, duration: int} |
| /genres | genres_page | GET, POST | genres.html | genres: list of dict {genre_id: int, genre_name: str, description: str}, selected_genre: str or None, genre_songs: list of dict {song_id: int, title: str, artist_name: str, duration: int}, genre_artists: list of dict {artist_id: int, name: str} |

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. Dashboard Page
- Template File Path: templates/dashboard.html
- Page Title: <title>Music Streaming Dashboard</title>, <h1>Music Streaming Dashboard</h1>
- Required Element IDs:
  - dashboard-page (Div)
  - featured-songs (Div)
  - browse-songs-button (Button)
  - my-playlists-button (Button)
  - trending-artists-button (Button)
- Context Variables:
  - featured_songs: list of dict {song_id: int, title: str, artist_name: str, album_name: str, duration: int}
  - trending_artists: list of dict {artist_id: int, name: str}
- Navigation Mappings:
  - browse-songs-button -> song_catalog_page
  - my-playlists-button -> playlists_page
  - trending-artists-button -> artists_page

### 2. Song Catalog Page
- Template File Path: templates/song_catalog.html
- Page Title: <title>Song Catalog</title>, <h1>Song Catalog</h1>
- Required Element IDs:
  - catalog-page (Div)
  - search-input (Input)
  - genre-filter (Dropdown)
  - songs-grid (Div)
  - add-to-playlist-button-{{ song.song_id }} (Button) for each song card
- Context Variables:
  - songs: list of dict {song_id: int, title: str, artist_name: str, album_name: str, duration: int, genre: str}
  - genres: list of str
  - search_query: str
  - selected_genre: str or None
- Navigation Mappings:
  - add-to-playlist-button-{{ song.song_id }} -> add_song_to_playlist (POST or AJAX)

### 3. Song Details Page
- Template File Path: templates/song_details.html
- Page Title: <title>Song Details</title>, <h1 id="song-title">{{ song.title }}</h1>
- Required Element IDs:
  - song-details-page (Div)
  - song-title (H1)
  - artist-name (Div) with link to artist_profile_page
  - album-name (Div)
  - duration-display (Div)
  - play-button (Button)
- Context Variables:
  - song: dict {song_id: int, title: str, artist_id: int, artist_name: str, album_id: int, album_name: str, duration: int, genre: str, release_date: str, play_count: int}
- Navigation Mappings:
  - artist-name (link) -> artist_profile_page
  - play-button -> play_song function

### 4. Playlists Page
- Template File Path: templates/playlists.html
- Page Title: <title>My Playlists</title>, <h1>My Playlists</h1>
- Required Element IDs:
  - playlists-page (Div)
  - playlists-grid (Div)
  - create-playlist-button (Button)
  - view-playlist-button-{{ playlist.playlist_id }} (Button) for each playlist
  - back-to-dashboard (Button)
- Context Variables:
  - playlists: list of dict {playlist_id: int, title: str, description: str, total_songs: int}
- Navigation Mappings:
  - create-playlist-button -> create_playlist_page
  - view-playlist-button-{{ playlist.playlist_id }} -> playlist_details_page
  - back-to-dashboard -> dashboard_page

### 5. Playlist Details Page
- Template File Path: templates/playlist_details.html
- Page Title: <title>Playlist Details</title>, <h1 id="playlist-title">{{ playlist.title }}</h1>
- Required Element IDs:
  - playlist-details-page (Div)
  - playlist-title (H1)
  - playlist-description (Div)
  - songs-in-playlist (Table)
  - remove-song-button-{{ song.song_id }} (Button) for each song
  - delete-playlist-button (Button)
- Context Variables:
  - playlist: dict {playlist_id: int, title: str, description: str}
  - songs_in_playlist: list of dict {song_id: int, title: str, artist_name: str, duration: int}
- Navigation Mappings:
  - remove-song-button-{{ song.song_id }} -> remove_song_from_playlist (POST or AJAX)
  - delete-playlist-button -> delete_playlist (POST)

### 6. Create Playlist Page
- Template File Path: templates/create_playlist.html
- Page Title: <title>Create New Playlist</title>, <h1>Create New Playlist</h1>
- Required Element IDs:
  - create-playlist-page (Div)
  - playlist-name-input (Input)
  - playlist-description-input (Textarea)
  - save-playlist-button (Button)
  - cancel-create-button (Button)
- Context Variables:
  - form inputs for playlist_name (str) and playlist_description (str)
- Navigation Mappings:
  - save-playlist-button -> create_playlist_page (POST)
  - cancel-create-button -> playlists_page

### 7. Album Browse Page
- Template File Path: templates/albums.html
- Page Title: <title>Albums</title>, <h1>Albums</h1>
- Required Element IDs:
  - albums-page (Div)
  - albums-grid (Div)
  - search-albums (Input)
  - sort-albums (Dropdown)
  - view-album-button-{{ album.album_id }} (Button) for each album
- Context Variables:
  - albums: list of dict {album_id: int, title: str, artist_name: str, release_year: int, genre: str}
  - search_query: str
  - sort_option: str
- Navigation Mappings:
  - view-album-button-{{ album.album_id }} -> album_details_page

### 8. Album Details Page
- Template File Path: templates/album_details.html
- Page Title: <title>Album Details</title>, <h1 id="album-title">{{ album.title }}</h1>
- Required Element IDs:
  - album-details-page (Div)
  - album-title (H1)
  - album-artist (Div)
  - album-year (Div)
  - album-songs-list (Div)
  - add-album-to-playlist-button (Button)
- Context Variables:
  - album: dict {album_id: int, title: str, artist_name: str, release_year: int}
  - songs_in_album: list of dict {song_id: int, title: str, duration: int}
- Navigation Mappings:
  - add-album-to-playlist-button -> add_album_to_playlist (POST or AJAX)

### 9. Artist Profile Page
- Template File Path: templates/artist_profile.html
- Page Title: <title>Artist Profiles</title>, <h1>Artist Profiles</h1>
- Required Element IDs:
  - artists-page (Div)
  - artists-grid (Div)
  - search-artists (Input)
  - artists-sort (Dropdown)
  - view-artist-button-{{ artist.artist_id }} (Button) for each artist
- Context Variables:
  - artists: list of dict {artist_id: int, name: str, genre: str, country: str}
  - search_query: str
  - sort_option: str
- Navigation Mappings:
  - view-artist-button-{{ artist.artist_id }} -> artist_profile_page

### 10. Genre Exploration Page
- Template File Path: templates/genres.html
- Page Title: <title>Genre Exploration</title>, <h1>Genre Exploration</h1>
- Required Element IDs:
  - genres-page (Div)
  - genres-list (Div)
  - select-genre (Dropdown)
  - genre-songs (Div)
  - genre-artists (Div)
  - back-to-dashboard (Button)
- Context Variables:
  - genres: list of dict {genre_id: int, genre_name: str, description: str}
  - selected_genre: str or None
  - genre_songs: list of dict {song_id: int, title: str, artist_name: str, duration: int}
  - genre_artists: list of dict {artist_id: int, name: str}
- Navigation Mappings:
  - back-to-dashboard -> dashboard_page

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. Songs Data
- Filename and Path: data/songs.txt
- File format: pipe-delimited (|)
- Fields:
  1. song_id (int): Unique song identifier
  2. title (str): Song title
  3. artist_id (int): Reference to artist_id in artists.txt
  4. album_id (int): Reference to album_id in albums.txt
  5. genre (str): Music genre
  6. duration (int): Duration in seconds
  7. release_date (str): Date in YYYY-MM-DD format
  8. play_count (int): Total number of plays
- Example rows:
  ```
  1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
  2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
  3|Shape of You|3|3|Pop|233|2017-01-06|4200000
  ```

### 2. Artists Data
- Filename and Path: data/artists.txt
- File format: pipe-delimited (|)
- Fields:
  1. artist_id (int): Unique artist identifier
  2. name (str): Artist name
  3. genre (str): Primary genre
  4. country (str): Country of origin
  5. formation_year (int): Year band/artist was formed
- Example rows:
  ```
  1|Queen|Rock|United Kingdom|1970
  2|The Weeknd|Synth-Pop|Canada|2010
  3|Ed Sheeran|Pop|United Kingdom|2005
  ```

### 3. Albums Data
- Filename and Path: data/albums.txt
- File format: pipe-delimited (|)
- Fields:
  1. album_id (int): Unique album identifier
  2. title (str): Album title
  3. artist_id (int): Reference to artist_id in artists.txt
  4. release_year (int): Year of release
  5. total_songs (int): Number of songs in album
  6. genre (str): Genre of the album
- Example rows:
  ```
  1|A Night at the Opera|1|1975|11|Rock
  2|After Hours|2|2019|14|Synth-Pop
  3|Divide|3|2017|12|Pop
  ```

### 4. Genres Data
- Filename and Path: data/genres.txt
- File format: pipe-delimited (|)
- Fields:
  1. genre_id (int): Unique genre identifier
  2. genre_name (str): Name of the genre
  3. description (str): Short description of the genre
- Example rows:
  ```
  1|Rock|Guitar-driven music with strong beats and vocals
  2|Pop|Catchy mainstream music with broad appeal
  3|Hip-Hop|Rhythmic music with rap vocals and beat production
  ```

### 5. Playlists Data
- Filename and Path: data/playlists.txt
- File format: pipe-delimited (|)
- Fields:
  1. playlist_id (int): Unique playlist identifier
  2. title (str): Playlist title
  3. description (str): Playlist description
  4. creation_date (str): Date playlist was created (YYYY-MM-DD)
  5. total_songs (int): Number of songs in playlist
- Example rows:
  ```
  1|Workout Mix|High energy songs for the gym|2025-01-15|25
  2|Chill Vibes|Relaxing music for study|2025-01-16|18
  3|Party Hits|Latest party tracks|2025-01-17|32
  ```

### 6. Playlist Songs Data
- Filename and Path: data/playlist_songs.txt
- File format: pipe-delimited (|)
- Fields:
  1. playlist_song_id (int): Unique ID for playlist-song entry
  2. playlist_id (int): Reference to playlist_id in playlists.txt
  3. song_id (int): Reference to song_id in songs.txt
  4. added_date (str): Date the song was added (YYYY-MM-DD)
- Example rows:
  ```
  1|1|2|2025-01-15
  2|1|3|2025-01-15
  3|2|1|2025-01-16
  ```

---

This concludes the comprehensive design specifications for the MusicStreaming application to guide backend and frontend development.