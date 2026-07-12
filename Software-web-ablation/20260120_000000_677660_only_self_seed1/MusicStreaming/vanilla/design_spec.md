# MusicStreaming Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                    | Function Name           | HTTP Method(s) | Template File             | Context Variables                                                                                                 |
|------------------------------|------------------------|----------------|---------------------------|------------------------------------------------------------------------------------------------------------------|
| /                            | root_redirect           | GET            | N/A (redirect)             | None                                                                                                             |
| /dashboard                   | dashboard_page          | GET            | dashboard.html             | featured_songs: list of dict {song_id: int, title: str, artist_name: str, duration: int}, trending_artists: list of dict {artist_id: int, name: str} |
| /songs                       | song_catalog            | GET, POST      | song_catalog.html          | songs: list of dict {song_id: int, title: str, artist_name: str, album_title: str, genre: str, duration: int},
                                             filter_genre: str or None, search_query: str or None                                          |
| /songs/<int:song_id>         | song_details            | GET            | song_details.html          | song: dict {song_id: int, title: str, artist_id: int, artist_name: str, album_id: int, album_title: str, duration: int} |
| /playlists                   | playlists_page          | GET            | playlists.html             | playlists: list of dict {playlist_id: int, title: str, description: str, total_songs: int}                       |
| /playlists/<int:playlist_id> | playlist_details        | GET            | playlist_details.html      | playlist: dict {playlist_id: int, title: str, description: str}, songs: list of dict {song_id: int, title: str, artist_name: str, duration: int} |
| /playlists/create            | create_playlist         | GET            | create_playlist.html       | None                                                                                                             |
| /playlists/create            | save_new_playlist       | POST           | N/A (redirect after POST) | None (read from POST form data: title: str, description: str)                                                   |
| /albums                      | albums_page             | GET            | albums.html                | albums: list of dict {album_id: int, title: str, artist_name: str, release_year: int, genre: str}                |
| /albums/<int:album_id>       | album_details           | GET            | album_details.html         | album: dict {album_id: int, title: str, artist_id: int, artist_name: str, release_year: int, genre: str},
                                             songs: list of dict {song_id: int, title: str, duration: int}                                                 |
| /artists                     | artists_page            | GET            | artists.html               | artists: list of dict {artist_id: int, name: str, genre: str, country: str}                                       |
| /artists/<int:artist_id>     | artist_profile          | GET            | artist_profile.html        | artist: dict {artist_id: int, name: str, genre: str, country: str, formation_year: int}                          |
| /genres                      | genres_page             | GET            | genres.html                | genres: list of dict {genre_id: int, genre_name: str, description: str}, selected_genre_id: int or None,
                                             genre_songs: list of dict {song_id: int, title: str, artist_name: str, duration: int},
                                             genre_artists: list of dict {artist_id: int, name: str}                                                        |

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. dashboard.html
- Template File Path: templates/dashboard.html
- Page Title:
  - <title>: Music Streaming Dashboard
  - <h1> (implied in dashboard-page div, optional): Music Streaming Dashboard
- Required Element IDs:
  - dashboard-page (Div)
  - featured-songs (Div)
  - browse-songs-button (Button)
  - my-playlists-button (Button)
  - trending-artists-button (Button)
- Context Variables:
  - featured_songs: list of dict {song_id: int, title: str, artist_name: str, duration: int (seconds)}
  - trending_artists: list of dict {artist_id: int, name: str}
- Navigation Mappings:
  - browse-songs-button -> song_catalog
  - my-playlists-button -> playlists_page
  - trending-artists-button -> artists_page

### 2. song_catalog.html
- Template File Path: templates/song_catalog.html
- Page Title:
  - <title>: Song Catalog
  - <h1> (optional): Song Catalog
- Required Element IDs:
  - catalog-page (Div)
  - search-input (Input)
  - genre-filter (Dropdown)
  - songs-grid (Div)
  - add-to-playlist-button-{{ song.song_id }} (Button for each song card)
- Context Variables:
  - songs: list of dict {song_id: int, title: str, artist_name: str, album_title: str, genre: str, duration: int}
  - filter_genre: str or None
  - search_query: str or None
- Navigation Mappings:
  - add-to-playlist-button-{{ song.song_id }} -> (calls add-to-playlist backend handler, no page navigation)

### 3. song_details.html
- Template File Path: templates/song_details.html
- Page Title:
  - <title>: Song Details
  - <h1>: song-title
- Required Element IDs:
  - song-details-page (Div)
  - song-title (H1)
  - artist-name (Div with link)
  - album-name (Div)
  - duration-display (Div)
  - play-button (Button)
- Context Variables:
  - song: dict {song_id: int, title: str, artist_id: int, artist_name: str, album_id: int, album_title: str, duration: int}
- Navigation Mappings:
  - artist-name (link) -> artist_profile with artist_id
  - play-button -> (play song action, no page navigation)

### 4. playlists.html
- Template File Path: templates/playlists.html
- Page Title:
  - <title>: My Playlists
  - <h1> (optional): My Playlists
- Required Element IDs:
  - playlists-page (Div)
  - playlists-grid (Div)
  - create-playlist-button (Button)
  - view-playlist-button-{{ playlist.playlist_id }} (Button for each playlist)
  - back-to-dashboard (Button)
- Context Variables:
  - playlists: list of dict {playlist_id: int, title: str, description: str, total_songs: int}
- Navigation Mappings:
  - create-playlist-button -> create_playlist
  - view-playlist-button-{{ playlist.playlist_id }} -> playlist_details with playlist_id
  - back-to-dashboard -> dashboard_page

### 5. playlist_details.html
- Template File Path: templates/playlist_details.html
- Page Title:
  - <title>: Playlist Details
  - <h1>: playlist-title
- Required Element IDs:
  - playlist-details-page (Div)
  - playlist-title (H1)
  - playlist-description (Div)
  - songs-in-playlist (Table)
  - remove-song-button-{{ song.song_id }} (Button for each song)
  - delete-playlist-button (Button)
- Context Variables:
  - playlist: dict {playlist_id: int, title: str, description: str}
  - songs: list of dict {song_id: int, title: str, artist_name: str, duration: int}
- Navigation Mappings:
  - remove-song-button-{{ song.song_id }} -> (remove song POST action, no page navigation)
  - delete-playlist-button -> (delete playlist POST action, no page navigation)

### 6. create_playlist.html
- Template File Path: templates/create_playlist.html
- Page Title:
  - <title>: Create New Playlist
  - <h1> (optional): Create New Playlist
- Required Element IDs:
  - create-playlist-page (Div)
  - playlist-name-input (Input)
  - playlist-description-input (Textarea)
  - save-playlist-button (Button)
  - cancel-create-button (Button)
- Context Variables:
  - None
- Navigation Mappings:
  - save-playlist-button -> save_new_playlist (POST)
  - cancel-create-button -> playlists_page

### 7. albums.html
- Template File Path: templates/albums.html
- Page Title:
  - <title>: Albums
  - <h1> (optional): Albums
- Required Element IDs:
  - albums-page (Div)
  - albums-grid (Div)
  - search-albums (Input)
  - sort-albums (Dropdown)
  - view-album-button-{{ album.album_id }} (Button for each album)
- Context Variables:
  - albums: list of dict {album_id: int, title: str, artist_name: str, release_year: int, genre: str}
- Navigation Mappings:
  - view-album-button-{{ album.album_id }} -> album_details with album_id

### 8. album_details.html
- Template File Path: templates/album_details.html
- Page Title:
  - <title>: Album Details
  - <h1>: album-title
- Required Element IDs:
  - album-details-page (Div)
  - album-title (H1)
  - album-artist (Div)
  - album-year (Div)
  - album-songs-list (Div)
  - add-album-to-playlist-button (Button)
- Context Variables:
  - album: dict {album_id: int, title: str, artist_id: int, artist_name: str, release_year: int, genre: str}
  - songs: list of dict {song_id: int, title: str, duration: int}
- Navigation Mappings:
  - add-album-to-playlist-button -> (action to add all songs, no page navigation)

### 9. artists.html
- Template File Path: templates/artists.html
- Page Title:
  - <title>: Artist Profiles
  - <h1> (optional): Artist Profiles
- Required Element IDs:
  - artists-page (Div)
  - artists-grid (Div)
  - search-artists (Input)
  - artists-sort (Dropdown)
  - view-artist-button-{{ artist.artist_id }} (Button for each artist)
- Context Variables:
  - artists: list of dict {artist_id: int, name: str, genre: str, country: str}
- Navigation Mappings:
  - view-artist-button-{{ artist.artist_id }} -> artist_profile with artist_id

### 10. genres.html
- Template File Path: templates/genres.html
- Page Title:
  - <title>: Genre Exploration
  - <h1> (optional): Genre Exploration
- Required Element IDs:
  - genres-page (Div)
  - genres-list (Div)
  - select-genre (Dropdown)
  - genre-songs (Div)
  - genre-artists (Div)
  - back-to-dashboard (Button)
- Context Variables:
  - genres: list of dict {genre_id: int, genre_name: str, description: str}
  - selected_genre_id: int or None
  - genre_songs: list of dict {song_id: int, title: str, artist_name: str, duration: int}
  - genre_artists: list of dict {artist_id: int, name: str}
- Navigation Mappings:
  - back-to-dashboard -> dashboard_page

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. data/songs.txt
- File format: pipe-delimited (|)
- Fields:
  1. song_id (int): Unique identifier for the song
  2. title (str): Song title
  3. artist_id (int): Foreign key referencing artists.txt artist_id
  4. album_id (int): Foreign key referencing albums.txt album_id
  5. genre (str): Genre name (must match genre_name in genres.txt)
  6. duration (int): Duration in seconds
  7. release_date (str): Release date in YYYY-MM-DD format
  8. play_count (int): Number of times played
- Example Rows:
  ```
  1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
  2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
  3|Shape of You|3|3|Pop|233|2017-01-06|4200000
  ```

### 2. data/artists.txt
- File format: pipe-delimited (|)
- Fields:
  1. artist_id (int): Unique identifier for the artist
  2. name (str): Artist name
  3. genre (str): Primary genre
  4. country (str): Country of origin
  5. formation_year (int): Year the artist/band was formed
- Example Rows:
  ```
  1|Queen|Rock|United Kingdom|1970
  2|The Weeknd|Synth-Pop|Canada|2010
  3|Ed Sheeran|Pop|United Kingdom|2005
  ```

### 3. data/albums.txt
- File format: pipe-delimited (|)
- Fields:
  1. album_id (int): Unique identifier for the album
  2. title (str): Album title
  3. artist_id (int): Foreign key referencing artists.txt artist_id
  4. release_year (int): Year album was released
  5. total_songs (int): Number of songs in the album
  6. genre (str): Album genre
- Example Rows:
  ```
  1|A Night at the Opera|1|1975|11|Rock
  2|After Hours|2|2019|14|Synth-Pop
  3|Divide|3|2017|12|Pop
  ```

### 4. data/genres.txt
- File format: pipe-delimited (|)
- Fields:
  1. genre_id (int): Unique identifier for the genre
  2. genre_name (str): Genre name
  3. description (str): Textual description of the genre
- Example Rows:
  ```
  1|Rock|Guitar-driven music with strong beats and vocals
  2|Pop|Catchy mainstream music with broad appeal
  3|Hip-Hop|Rhythmic music with rap vocals and beat production
  ```

### 5. data/playlists.txt
- File format: pipe-delimited (|)
- Fields:
  1. playlist_id (int): Unique identifier for the playlist
  2. title (str): Playlist title
  3. description (str): Playlist description
  4. creation_date (str): Date playlist created in YYYY-MM-DD
  5. total_songs (int): Number of songs in playlist
- Example Rows:
  ```
  1|Workout Mix|High energy songs for the gym|2025-01-15|25
  2|Chill Vibes|Relaxing music for study|2025-01-16|18
  3|Party Hits|Latest party tracks|2025-01-17|32
  ```

### 6. data/playlist_songs.txt
- File format: pipe-delimited (|)
- Fields:
  1. playlist_song_id (int): Unique identifier for playlist-song link
  2. playlist_id (int): Foreign key referencing playlists.txt playlist_id
  3. song_id (int): Foreign key referencing songs.txt song_id
  4. added_date (str): Date the song was added to playlist YYYY-MM-DD
- Example Rows:
  ```
  1|1|2|2025-01-15
  2|1|3|2025-01-15
  3|2|1|2025-01-16
  ```

---

*End of Design Specification.*
