# MusicStreaming Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                    | Function Name           | HTTP Method(s) | Template File          | Context Variables                                                                                                 |
|-------------------------------|------------------------|----------------|------------------------|------------------------------------------------------------------------------------------------------------------|
| /                             | root_redirect           | GET            | N/A (redirect)          | None                                                                                                             |
| /dashboard                    | dashboard_page          | GET            | dashboard.html         | featured_songs: list of dict {song_id: int, title: str, artist_name: str, duration: int}, trending_artists: list of dict {artist_id: int, name: str} |
| /songs                       | song_catalog            | GET, POST      | song_catalog.html      | songs: list of dict {song_id: int, title: str, artist_name: str, album_name: str, genre: str, duration: int},
                                             selected_genre: str or None, search_query: str or None                                          |
| /songs/<int:song_id>         | song_details            | GET            | song_details.html      | song: dict {song_id: int, title: str, artist_id: int, artist_name: str, album_id: int, album_name: str, genre: str, duration: int},                        |
|                              |                        |                |                        | release_date: str (YYYY-MM-DD), play_count: int                                                               |
| /playlists                   | playlists               | GET            | playlists.html         | playlists: list of dict {playlist_id: int, title: str, description: str, total_songs: int}                         |
| /playlists/<int:playlist_id> | playlist_details        | GET            | playlist_details.html  | playlist: dict {playlist_id: int, title: str, description: str}, songs: list of dict {song_id: int, title: str, artist_name: str, duration: int}           |
| /playlists/create            | create_playlist         | GET, POST      | create_playlist.html   | None for GET; for POST POSTed data handled                                                                                      |
| /albums                     | albums                  | GET            | albums.html            | albums: list of dict {album_id: int, title: str, artist_name: str, release_year: int, genre: str}                   |
| /albums/<int:album_id>       | album_details           | GET            | album_details.html     | album: dict {album_id: int, title: str, artist_name: str, release_year: int}, songs: list of dict {song_id:int, title:str, duration:int}                     |
| /artists                    | artists                 | GET            | artists.html           | artists: list of dict {artist_id: int, name: str, genre: str, country: str}                                         |
| /artists/<int:artist_id>     | artist_profile          | GET            | artist_profile.html    | artist: dict {artist_id: int, name: str, genre: str, country: str, formation_year: int}, songs: list of dict {song_id: int, title: str, album_name: str}       |
| /genres                     | genres                  | GET            | genres.html            | genres: list of dict {genre_id: int, genre_name: str, description: str}, selected_genre: dict {genre_id:int, genre_name:str} or None,                          |
|                              |                        |                |                        | genre_songs: list of dict {song_id:int, title:str, artist_name:str}, genre_artists: list of dict {artist_id:int, name:str}|

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. Dashboard Page
- Template File Path: templates/dashboard.html
- Page Title: <title>Music Streaming Dashboard</title>
- <h1>Music Streaming Dashboard</h1>
- Required Element IDs:
  - dashboard-page (Div)
  - featured-songs (Div)
  - browse-songs-button (Button)
  - my-playlists-button (Button)
  - trending-artists-button (Button)
- Context Variables:
  - featured_songs: list of dict {song_id: int, title: str, artist_name: str, duration: int}
  - trending_artists: list of dict {artist_id: int, name: str}
- Navigation Mappings:
  - browse-songs-button => song_catalog
  - my-playlists-button => playlists
  - trending-artists-button => artists

### 2. Song Catalog Page
- Template File Path: templates/song_catalog.html
- Page Title: <title>Song Catalog</title>
- <h1>Song Catalog</h1>
- Required Element IDs:
  - catalog-page (Div)
  - search-input (Input)
  - genre-filter (Dropdown)
  - songs-grid (Div)
  - add-to-playlist-button-{{song.song_id}} (Button for each song in songs-grid)
- Context Variables:
  - songs: list of dict {song_id, title, artist_name, album_name, genre, duration}
  - selected_genre: str or None
  - search_query: str or None
- Navigation Mappings:
  - Dynamic add-to-playlist-button-{song_id} buttons will trigger backend actions (mapping not direct to a page but controlled by backend logic)

### 3. Song Details Page
- Template File Path: templates/song_details.html
- Page Title: <title>Song Details</title>
- <h1 id="song-title">Song Title Here</h1>
- Required Element IDs:
  - song-details-page (Div)
  - song-title (H1)
  - artist-name (Div) — contains link with id artist-profile-link to artist profile page
  - album-name (Div)
  - duration-display (Div)
  - play-button (Button)
- Context Variables:
  - song: dict {song_id, title, artist_id, artist_name, album_id, album_name, genre, duration, release_date, play_count}
- Navigation Mappings:
  - artist-name clickable link with id "artist-profile-link" => artist_profile

### 4. Playlist Page
- Template File Path: templates/playlists.html
- Page Title: <title>My Playlists</title>
- <h1>My Playlists</h1>
- Required Element IDs:
  - playlists-page (Div)
  - playlists-grid (Div)
  - create-playlist-button (Button)
  - view-playlist-button-{{playlist.playlist_id}} (Button for each playlist)
  - back-to-dashboard (Button)
- Context Variables:
  - playlists: list of dict {playlist_id, title, description, total_songs}
- Navigation Mappings:
  - create-playlist-button => create_playlist
  - back-to-dashboard => dashboard_page
  - view-playlist-button-{playlist_id} => playlist_details

### 5. Playlist Details Page
- Template File Path: templates/playlist_details.html
- Page Title: <title>Playlist Details</title>
- <h1 id="playlist-title">Playlist Title</h1>
- Required Element IDs:
  - playlist-details-page (Div)
  - playlist-title (H1)
  - playlist-description (Div)
  - songs-in-playlist (Table)
  - remove-song-button-{{song.song_id}} (Button for each song in table)
  - delete-playlist-button (Button)
- Context Variables:
  - playlist: dict {playlist_id, title, description}
  - songs: list of dict {song_id, title, artist_name, duration}
- Navigation Mappings:
  - delete-playlist-button triggers backend delete playlist
  - remove-song-button-{song_id} triggers backend remove song from playlist

### 6. Create Playlist Page
- Template File Path: templates/create_playlist.html
- Page Title: <title>Create New Playlist</title>
- <h1>Create New Playlist</h1>
- Required Element IDs:
  - create-playlist-page (Div)
  - playlist-name-input (Input)
  - playlist-description-input (Textarea)
  - save-playlist-button (Button)
  - cancel-create-button (Button)
- Context Variables:
  - No context variables rendered for GET
- Navigation Mappings:
  - save-playlist-button submits form to create_playlist
  - cancel-create-button navigates back to playlists

### 7. Album Browse Page
- Template File Path: templates/albums.html
- Page Title: <title>Albums</title>
- <h1>Albums</h1>
- Required Element IDs:
  - albums-page (Div)
  - albums-grid (Div)
  - search-albums (Input)
  - sort-albums (Dropdown)
  - view-album-button-{{album.album_id}} (Button for each album)
- Context Variables:
  - albums: list of dict {album_id, title, artist_name, release_year, genre}
- Navigation Mappings:
  - view-album-button-{album_id} => album_details

### 8. Album Details Page
- Template File Path: templates/album_details.html
- Page Title: <title>Album Details</title>
- <h1 id="album-title">Album Title</h1>
- Required Element IDs:
  - album-details-page (Div)
  - album-title (H1)
  - album-artist (Div)
  - album-year (Div)
  - album-songs-list (Div)
  - add-album-to-playlist-button (Button)
- Context Variables:
  - album: dict {album_id, title, artist_name, release_year}
  - songs: list of dict {song_id, title, duration}
- Navigation Mappings:
  - add-album-to-playlist-button triggers backend playlist add

### 9. Artist Profile Page
- Template File Path: templates/artists.html
- Page Title: <title>Artist Profiles</title>
- <h1>Artist Profiles</h1>
- Required Element IDs:
  - artists-page (Div)
  - artists-grid (Div)
  - search-artists (Input)
  - artists-sort (Dropdown)
  - view-artist-button-{{artist.artist_id}} (Button for each artist)
- Context Variables:
  - artists: list of dict {artist_id, name, genre, country}
- Navigation Mappings:
  - view-artist-button-{artist_id} => artist_profile

### 10. Genre Exploration Page
- Template File Path: templates/genres.html
- Page Title: <title>Genre Exploration</title>
- <h1>Genre Exploration</h1>
- Required Element IDs:
  - genres-page (Div)
  - genres-list (Div)
  - select-genre (Dropdown)
  - genre-songs (Div)
  - genre-artists (Div)
  - back-to-dashboard (Button)
- Context Variables:
  - genres: list of dict {genre_id, genre_name, description}
  - selected_genre: dict {genre_id, genre_name} or None
  - genre_songs: list of dict {song_id, title, artist_name}
  - genre_artists: list of dict {artist_id, name}
- Navigation Mappings:
  - back-to-dashboard => dashboard_page

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. Songs Data
- Filename: data/songs.txt
- File Format: pipe-delimited (|)
- Fields:
  1. song_id (int): Unique identifier for the song
  2. title (str): Song title
  3. artist_id (int): Foreign key referencing artists.txt
  4. album_id (int): Foreign key referencing albums.txt
  5. genre (str): Genre name the song belongs to
  6. duration (int): Duration of song in seconds
  7. release_date (str): Release date in YYYY-MM-DD format
  8. play_count (int): Number of times the song was played
- Example rows:
  ```
1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
3|Shape of You|3|3|Pop|233|2017-01-06|4200000
```

### 2. Artists Data
- Filename: data/artists.txt
- File Format: pipe-delimited (|)
- Fields:
  1. artist_id (int): Unique identifier for the artist
  2. name (str): Artist name
  3. genre (str): Genre associated with artist
  4. country (str): Country of origin
  5. formation_year (int): Year artist or band formed
- Example rows:
  ```
1|Queen|Rock|United Kingdom|1970
2|The Weeknd|Synth-Pop|Canada|2010
3|Ed Sheeran|Pop|United Kingdom|2005
```

### 3. Albums Data
- Filename: data/albums.txt
- File Format: pipe-delimited (|)
- Fields:
  1. album_id (int): Unique album identifier
  2. title (str): Album title
  3. artist_id (int): Foreign key referencing artists.txt
  4. release_year (int): Year album was released
  5. total_songs (int): Number of songs in album
  6. genre (str): Primary genre of album
- Example rows:
  ```
1|A Night at the Opera|1|1975|11|Rock
2|After Hours|2|2019|14|Synth-Pop
3|Divide|3|2017|12|Pop
```

### 4. Genres Data
- Filename: data/genres.txt
- File Format: pipe-delimited (|)
- Fields:
  1. genre_id (int): Unique genre identifier
  2. genre_name (str): Name of the genre
  3. description (str): Brief description of genre
- Example rows:
  ```
1|Rock|Guitar-driven music with strong beats and vocals
2|Pop|Catchy mainstream music with broad appeal
3|Hip-Hop|Rhythmic music with rap vocals and beat production
```

### 5. Playlists Data
- Filename: data/playlists.txt
- File Format: pipe-delimited (|)
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
- Filename: data/playlist_songs.txt
- File Format: pipe-delimited (|)
- Fields:
  1. playlist_song_id (int): Unique identifier for playlist-song entry
  2. playlist_id (int): Foreign key referencing playlists.txt
  3. song_id (int): Foreign key referencing songs.txt
  4. added_date (str): Date song was added to playlist (YYYY-MM-DD)
- Example rows:
  ```
1|1|2|2025-01-15
2|1|3|2025-01-15
3|2|1|2025-01-16
```

---

CRITICAL NOTES:
- All element IDs, route function names, and context variables are explicitly defined.
- Backend should implement routes and load data strictly according to data file schemas.
- Frontend to use exact IDs and variable names to enable seamless integration.
- Dynamic element IDs use Jinja2 template pattern, e.g., add-to-playlist-button-{{song.song_id}}.

This completes the complete design specification for the MusicStreaming app.
