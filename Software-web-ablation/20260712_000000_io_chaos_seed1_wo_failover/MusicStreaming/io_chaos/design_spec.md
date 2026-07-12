# MusicStreaming Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                     | Function Name          | HTTP Method(s) | Template File           | Context Variables                                                                                          |
|-------------------------------|------------------------|----------------|-------------------------|-------------------------------------------------------------------------------------------------------------|
| /                             | root_redirect          | GET            | -                       | - Redirects to /dashboard                                                                                   |
| /dashboard                    | dashboard_page         | GET            | dashboard.html          | featured_songs: list of dicts {song_id:int, title:str, artist_name:str, album_name:str, duration:int}
  trending_artists: list of dicts {artist_id:int, name:str, genre:str}                                      |
| /songs                        | song_catalog           | GET            | song_catalog.html       | songs: list of dicts {song_id:int, title:str, artist_name:str, album_name:str, genre:str, duration:int}
  genres: list of str                                                                                          |
| /songs/<int:song_id>          | song_details           | GET            | song_details.html       | song: dict {song_id:int, title:str, artist_id:int, artist_name:str, album_id:int, album_name:str, duration:int, genre:str, release_date:str}
                                                                     |
| /playlists                   | playlists_page          | GET            | playlists.html          | playlists: list of dicts {playlist_id:int, title:str, description:str, total_songs:int}                       |
| /playlists/create             | create_playlist        | GET, POST     | create_playlist.html    | (GET) - no context variables
(POST) - validation results or redirect status                                   |
| /playlists/<int:playlist_id> | playlist_details       | GET            | playlist_details.html   | playlist: dict {playlist_id:int, title:str, description:str}
  songs_in_playlist: list of dicts {song_id:int, title:str, artist_name:str, duration:int}                           |
| /playlists/<int:playlist_id>/delete | delete_playlist  | POST           | -                       | - Redirect after delete                                                                                       |
| /playlists/<int:playlist_id>/remove_song/<int:song_id> | remove_song_from_playlist | POST | -                     | - Redirect after removal                                                                                      |
| /albums                      | albums_page             | GET            | albums.html             | albums: list of dicts {album_id:int, title:str, artist_name:str, release_year:int, genre:str}                  |
| /albums/<int:album_id>        | album_details          | GET            | album_details.html      | album: dict {album_id:int, title:str, artist_id:int, artist_name:str, release_year:int}
  album_songs: list of dicts {song_id:int, title:str, duration:int}                                           |
| /artists                     | artists_page            | GET            | artists.html            | artists: list of dicts {artist_id:int, name:str, genre:str, country:str}                                       |
| /artists/<int:artist_id>      | artist_profile         | GET            | artist_profile.html     | artist: dict {artist_id:int, name:str, genre:str, country:str, formation_year:int}
  artist_songs: list of dicts {song_id:int, title:str, album_name:str, duration:int}                          |
| /genres                      | genre_exploration       | GET            | genres.html             | genres: list of dicts {genre_id:int, genre_name:str, description:str}
  selected_genre: dict {genre_id:int, genre_name:str, description:str} or None
  genre_songs: list of dicts {song_id:int, title:str, artist_name:str, duration:int}
  genre_artists: list of dicts {artist_id:int, name:str, genre:str}                                          |

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. Dashboard Page
- Template File Path: templates/dashboard.html
- Page Title: <title>Music Streaming Dashboard</title>
- Main Header: <h1>Music Streaming Dashboard</h1>
- Required Element IDs:
  - dashboard-page (Div)
  - featured-songs (Div)
  - browse-songs-button (Button)
  - my-playlists-button (Button)
  - trending-artists-button (Button)
- Context Variables:
  - featured_songs: list of dicts with keys (song_id, title, artist_name, album_name, duration)
  - trending_artists: list of dicts with keys (artist_id, name, genre)
- Navigation Mappings:
  - browse-songs-button -> song_catalog_page
  - my-playlists-button -> playlists_page
  - trending-artists-button -> artists_page

### 2. Song Catalog Page
- Template File Path: templates/song_catalog.html
- Page Title: <title>Song Catalog</title>
- Main Header: <h1>Song Catalog</h1>
- Required Element IDs:
  - catalog-page (Div)
  - search-input (Input)
  - genre-filter (Dropdown)
  - songs-grid (Div)
  - add-to-playlist-button-{song_id} (Button, dynamic per song_id)
- Context Variables:
  - songs: list of dicts with keys (song_id, title, artist_name, album_name, genre, duration)
  - genres: list of str (genre names)
- Navigation Mappings:
  - add-to-playlist-button-{song_id} -> add_song_to_playlist (POST route expected)

### 3. Song Details Page
- Template File Path: templates/song_details.html
- Page Title: <title>Song Details</title>
- Main Header: <h1 id="song-title">{{ song.title }}</h1>
- Required Element IDs:
  - song-details-page (Div)
  - song-title (H1)
  - artist-name (Div, includes link)
  - album-name (Div)
  - duration-display (Div)
  - play-button (Button)
- Context Variables:
  - song: dict with keys (song_id, title, artist_id, artist_name, album_id, album_name, duration, genre, release_date)
- Navigation Mappings:
  - artist-name (link) -> artist_profile
  - play-button -> play_song (functionality assumed backend route)

### 4. Playlist Page
- Template File Path: templates/playlists.html
- Page Title: <title>My Playlists</title>
- Main Header: <h1>My Playlists</h1>
- Required Element IDs:
  - playlists-page (Div)
  - playlists-grid (Div)
  - create-playlist-button (Button)
  - view-playlist-button-{playlist_id} (Button, dynamic per playlist_id)
  - back-to-dashboard (Button)
- Context Variables:
  - playlists: list of dicts with keys (playlist_id, title, description, total_songs)
- Navigation Mappings:
  - create-playlist-button -> create_playlist
  - view-playlist-button-{playlist_id} -> playlist_details
  - back-to-dashboard -> dashboard_page

### 5. Playlist Details Page
- Template File Path: templates/playlist_details.html
- Page Title: <title>Playlist Details</title>
- Main Header: <h1 id="playlist-title">{{ playlist.title }}</h1>
- Required Element IDs:
  - playlist-details-page (Div)
  - playlist-title (H1)
  - playlist-description (Div)
  - songs-in-playlist (Table)
  - remove-song-button-{song_id} (Button, dynamic per song_id)
  - delete-playlist-button (Button)
- Context Variables:
  - playlist: dict with keys (playlist_id, title, description)
  - songs_in_playlist: list of dicts with keys (song_id, title, artist_name, duration)
- Navigation Mappings:
  - remove-song-button-{song_id} -> remove_song_from_playlist (POST route)
  - delete-playlist-button -> delete_playlist (POST route)

### 6. Create Playlist Page
- Template File Path: templates/create_playlist.html
- Page Title: <title>Create New Playlist</title>
- Main Header: <h1>Create New Playlist</h1>
- Required Element IDs:
  - create-playlist-page (Div)
  - playlist-name-input (Input)
  - playlist-description-input (Textarea)
  - save-playlist-button (Button)
  - cancel-create-button (Button)
- Context Variables:
  - None (page is form entry)
- Navigation Mappings:
  - save-playlist-button -> create_playlist (POST route)
  - cancel-create-button -> playlists_page

### 7. Album Browse Page
- Template File Path: templates/albums.html
- Page Title: <title>Albums</title>
- Main Header: <h1>Albums</h1>
- Required Element IDs:
  - albums-page (Div)
  - albums-grid (Div)
  - search-albums (Input)
  - sort-albums (Dropdown)
  - view-album-button-{album_id} (Button, dynamic per album_id)
- Context Variables:
  - albums: list of dicts with keys (album_id, title, artist_name, release_year, genre)
- Navigation Mappings:
  - view-album-button-{album_id} -> album_details

### 8. Album Details Page
- Template File Path: templates/album_details.html
- Page Title: <title>Album Details</title>
- Main Header: <h1 id="album-title">{{ album.title }}</h1>
- Required Element IDs:
  - album-details-page (Div)
  - album-title (H1)
  - album-artist (Div)
  - album-year (Div)
  - album-songs-list (Div)
  - add-album-to-playlist-button (Button)
- Context Variables:
  - album: dict with keys (album_id, title, artist_id, artist_name, release_year)
  - album_songs: list of dicts with keys (song_id, title, duration)
- Navigation Mappings:
  - add-album-to-playlist-button -> add_album_songs_to_playlist (POST route expected)

### 9. Artist Profile Page
- Template File Path: templates/artists.html
- Page Title: <title>Artist Profiles</title>
- Main Header: <h1>Artist Profiles</h1>
- Required Element IDs:
  - artists-page (Div)
  - artists-grid (Div)
  - search-artists (Input)
  - artists-sort (Dropdown)
  - view-artist-button-{artist_id} (Button, dynamic per artist_id)
- Context Variables:
  - artists: list of dicts with keys (artist_id, name, genre, country)
- Navigation Mappings:
  - view-artist-button-{artist_id} -> artist_profile

### 10. Genre Exploration Page
- Template File Path: templates/genres.html
- Page Title: <title>Genre Exploration</title>
- Main Header: <h1>Genre Exploration</h1>
- Required Element IDs:
  - genres-page (Div)
  - genres-list (Div)
  - select-genre (Dropdown)
  - genre-songs (Div)
  - genre-artists (Div)
  - back-to-dashboard (Button)
- Context Variables:
  - genres: list of dicts (genre_id, genre_name, description)
  - selected_genre: dict or None
  - genre_songs: list of dicts (song_id, title, artist_name, duration)
  - genre_artists: list of dicts (artist_id, name, genre)
- Navigation Mappings:
  - back-to-dashboard -> dashboard_page

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. songs.txt
- Relative Path: data/songs.txt
- File Format: pipe-delimited (|)
- Fields:
  1. song_id (int): unique song identifier
  2. title (str): song title
  3. artist_id (int): foreign key referencing artists.txt
  4. album_id (int): foreign key referencing albums.txt
  5. genre (str): genre name
  6. duration (int): duration in seconds
  7. release_date (str): ISO date YYYY-MM-DD
  8. play_count (int): total play count
- Example Data:
  ```
  1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
  2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
  3|Shape of You|3|3|Pop|233|2017-01-06|4200000
  ```

### 2. artists.txt
- Relative Path: data/artists.txt
- File Format: pipe-delimited (|)
- Fields:
  1. artist_id (int): unique artist identifier
  2. name (str): artist name
  3. genre (str): primary genre
  4. country (str): country of origin
  5. formation_year (int): year the artist/band was formed
- Example Data:
  ```
  1|Queen|Rock|United Kingdom|1970
  2|The Weeknd|Synth-Pop|Canada|2010
  3|Ed Sheeran|Pop|United Kingdom|2005
  ```

### 3. albums.txt
- Relative Path: data/albums.txt
- File Format: pipe-delimited (|)
- Fields:
  1. album_id (int): unique album identifier
  2. title (str): album title
  3. artist_id (int): foreign key referencing artists.txt
  4. release_year (int): year of release
  5. total_songs (int): total number of songs in album
  6. genre (str): album genre
- Example Data:
  ```
  1|A Night at the Opera|1|1975|11|Rock
  2|After Hours|2|2019|14|Synth-Pop
  3|Divide|3|2017|12|Pop
  ```

### 4. genres.txt
- Relative Path: data/genres.txt
- File Format: pipe-delimited (|)
- Fields:
  1. genre_id (int): unique genre identifier
  2. genre_name (str): genre name
  3. description (str): genre description
- Example Data:
  ```
  1|Rock|Guitar-driven music with strong beats and vocals
  2|Pop|Catchy mainstream music with broad appeal
  3|Hip-Hop|Rhythmic music with rap vocals and beat production
  ```

### 5. playlists.txt
- Relative Path: data/playlists.txt
- File Format: pipe-delimited (|)
- Fields:
  1. playlist_id (int): unique playlist identifier
  2. title (str): playlist title
  3. description (str): playlist description
  4. creation_date (str): ISO date YYYY-MM-DD
  5. total_songs (int): total songs in playlist
- Example Data:
  ```
  1|Workout Mix|High energy songs for the gym|2025-01-15|25
  2|Chill Vibes|Relaxing music for study|2025-01-16|18
  3|Party Hits|Latest party tracks|2025-01-17|32
  ```

### 6. playlist_songs.txt
- Relative Path: data/playlist_songs.txt
- File Format: pipe-delimited (|)
- Fields:
  1. playlist_song_id (int): unique identifier for playlist-song mapping
  2. playlist_id (int): foreign key referencing playlists.txt
  3. song_id (int): foreign key referencing songs.txt
  4. added_date (str): ISO date YYYY-MM-DD when song was added
- Example Data:
  ```
  1|1|2|2025-01-15
  2|1|3|2025-01-15
  3|2|1|2025-01-16
  ```

---

This completes the comprehensive design specification to enable independent backend and frontend development for the MusicStreaming application.