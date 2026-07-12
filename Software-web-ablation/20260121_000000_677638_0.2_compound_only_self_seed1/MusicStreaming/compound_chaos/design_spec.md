# MusicStreaming Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                    | Function Name           | HTTP Method(s) | Template File          | Context Variables                                                                                                 |
|------------------------------|------------------------|----------------|------------------------|------------------------------------------------------------------------------------------------------------------|
| /                            | root_redirect           | GET            | N/A (redirect)          | None                                                                                                             |
| /dashboard                   | dashboard              | GET            | dashboard.html          | featured_songs: List[Dict] with keys (song_id:int, title:str, artist_name:str, duration:int),
                                          trending_artists: List[Dict] with keys (artist_id:int, name:str)                                         |
| /songs                      | song_catalog           | GET            | song_catalog.html       | songs: List[Dict] with keys (song_id:int, title:str, artist_name:str, album_name:str, genre:str, duration:int),
                                     genres: List[str]                                                                                            |
| /songs/search               | song_search_filter     | POST           | song_catalog.html       | songs: List[Dict] same as above after filtering/search,
                                     genres: List[str]                                                          |
| /songs/<int:song_id>         | song_details           | GET            | song_details.html       | song: Dict with keys {song_id:int, title:str, artist_id:int, artist_name:str, album_id:int, album_name:str, genre:str, duration:int}                 |
| /playlists                  | playlists              | GET            | playlists.html          | playlists: List[Dict] with keys (playlist_id:int, title:str, description:str, total_songs:int)                 |
| /playlists/create           | create_playlist        | GET            | create_playlist.html    | None                                                                                                             |
| /playlists/create           | create_playlist_post   | POST           | N/A (redirect to playlists or created playlist)           | None                                                                                                             |
| /playlists/<int:playlist_id>| playlist_details       | GET            | playlist_details.html   | playlist: Dict with keys (playlist_id:int, title:str, description:str),
                                songs: List[Dict] with keys (song_id:int, title:str, artist_name:str, duration:int)          |
| /playlists/<int:playlist_id>/delete | delete_playlist      | POST           | N/A (redirect back to playlists)            | None                                                                                                             |
| /playlists/<int:playlist_id>/remove_song/<int:song_id> | remove_song_from_playlist | POST           | N/A (redirect back to playlist details)   | None                                                                                                             |
| /albums                     | albums_browse          | GET            | albums.html             | albums: List[Dict] with keys (album_id:int, title:str, artist_name:str, year:int),
                                 sort_options: List[str] = ["By Title", "By Artist", "By Year"]                                      |
| /albums/search              | albums_search_sort     | POST           | albums.html             | albums: List[Dict] filtered and/or sorted,
                                 sort_options: List[str]                                                                   |
| /albums/<int:album_id>       | album_details          | GET            | album_details.html      | album: Dict with keys (album_id:int, title:str, artist_name:str, release_year:int),
                           songs: List[Dict] with keys (song_id:int, title:str, duration:int)                       |
| /albums/<int:album_id>/add_to_playlist | add_album_to_playlist | POST          | N/A (redirect or confirmation)               | None                                                                                                             |
| /artists                    | artists_page           | GET            | artists.html            | artists: List[Dict] with keys (artist_id:int, name:str, genre:str),
                                   sort_options: List[str] = ["By Name", "By Genre"]                                             |
| /artists/search_sort        | artists_search_sort    | POST           | artists.html            | artists: List[Dict] filtered/sorted,
                                   sort_options: List[str]                                                                    |
| /artists/<int:artist_id>     | artist_profile         | GET            | artist_profile.html     | artist: Dict with keys (artist_id:int, name:str, genre:str, country:str, formation_year:int)                     |
| /genres                     | genres_page            | GET            | genres.html             | genres: List[Dict] with keys (genre_id:int, genre_name:str, description:str),
                                 songs: List[Dict] (songs in selected genre with keys like song_id:int, title:str, artist_name:str),
                                 artists: List[Dict] (artists in selected genre with keys like artist_id:int, name:str)                    |
| /genres/select              | select_genre           | POST           | genres.html             | genres: List[Dict] same as above,
                                 songs: List[Dict] filtered by selected genre,
                                 artists: List[Dict] filtered by selected genre                                           |

---

## Section 2: HTML Template Specifications (For Frontend Developer)

---

### Template: dashboard.html
- Template File Path: templates/dashboard.html
- Page Title: <title>Music Streaming Dashboard</title>
- H1 Content: "Music Streaming Dashboard" (contained within div with ID: dashboard-page)
- Required Element IDs:
  - dashboard-page (Div)
  - featured-songs (Div)
  - browse-songs-button (Button)
  - my-playlists-button (Button)
  - trending-artists-button (Button)
- Context Variables:
  - featured_songs: List of dictionaries containing {
      song_id (int),
      title (str),
      artist_name (str),
      duration (int) seconds
    }
  - trending_artists: List of dictionaries containing {
      artist_id (int),
      name (str)
    }
- Navigation Mappings:
  - browse-songs-button --> song_catalog
  - my-playlists-button --> playlists
  - trending-artists-button --> artists_page

---

### Template: song_catalog.html
- Template File Path: templates/song_catalog.html
- Page Title: <title>Song Catalog</title>
- H1 Content: "Song Catalog" (within catalog-page div)
- Required Element IDs:
  - catalog-page (Div)
  - search-input (Input)
  - genre-filter (Dropdown)
  - songs-grid (Div)
  - add-to-playlist-button-{{song.song_id}} (Button, dynamic per song)
- Context Variables:
  - songs: List of dictionaries with keys {
      song_id (int), title (str), artist_name (str), album_name (str), genre (str), duration (int)
    }
  - genres: List of genre strings
- Navigation Mappings:
  - Clicking add-to-playlist-button-{{song_id}} triggers adding that song to playlist (POST to handle in backend)

---

### Template: song_details.html
- Template File Path: templates/song_details.html
- Page Title: <title>Song Details</title>
- H1 Content: song title (id: song-title)
- Required Element IDs:
  - song-details-page (Div)
  - song-title (H1)
  - artist-name (Div)  (artist name should be clickable to artist_profile page)
  - album-name (Div)
  - duration-display (Div)
  - play-button (Button)
- Context Variables:
  - song: Dict with fields {
      song_id (int), title (str), artist_id (int), artist_name (str), album_id (int), album_name (str), genre (str), duration (int)
    }
- Navigation Mappings:
  - artist-name --> artist_profile (with artist_id)

---

### Template: playlists.html
- Template File Path: templates/playlists.html
- Page Title: <title>My Playlists</title>
- H1 Content: "My Playlists" (in playlists-page div)
- Required Element IDs:
  - playlists-page (Div)
  - playlists-grid (Div)
  - create-playlist-button (Button)
  - view-playlist-button-{{playlist.playlist_id}} (Button, dynamic per playlist)
  - back-to-dashboard (Button)
- Context Variables:
  - playlists: List of dictionaries with keys {
      playlist_id (int), title (str), description (str), total_songs (int)
    }
- Navigation Mappings:
  - create-playlist-button --> create_playlist
  - view-playlist-button-{{playlist_id}} --> playlist_details
  - back-to-dashboard --> dashboard

---

### Template: playlist_details.html
- Template File Path: templates/playlist_details.html
- Page Title: <title>Playlist Details</title>
- H1 Content: playlist title (id: playlist-title)
- Required Element IDs:
  - playlist-details-page (Div)
  - playlist-title (H1)
  - playlist-description (Div)
  - songs-in-playlist (Table)
  - remove-song-button-{{song.song_id}} (Button, dynamic per song)
  - delete-playlist-button (Button)
- Context Variables:
  - playlist: Dict with {
      playlist_id (int), title (str), description (str)
    }
  - songs: List of Dict with {
      song_id (int), title (str), artist_name (str), duration (int)
    }
- Navigation Mappings:
  - remove-song-button-{{song_id}} triggers POST to remove song
  - delete-playlist-button triggers POST to delete playlist

---

### Template: create_playlist.html
- Template File Path: templates/create_playlist.html
- Page Title: <title>Create New Playlist</title>
- H1 Content: "Create New Playlist" (in create-playlist-page div)
- Required Element IDs:
  - create-playlist-page (Div)
  - playlist-name-input (Input)
  - playlist-description-input (Textarea)
  - save-playlist-button (Button)
  - cancel-create-button (Button)
- Context Variables: None
- Navigation Mappings:
  - save-playlist-button triggers POST to create_playlist_post
  - cancel-create-button navigates back to playlists

---

### Template: albums.html
- Template File Path: templates/albums.html
- Page Title: <title>Albums</title>
- H1 Content: "Albums" (in albums-page div)
- Required Element IDs:
  - albums-page (Div)
  - albums-grid (Div)
  - search-albums (Input)
  - sort-albums (Dropdown)
  - view-album-button-{{album.album_id}} (Button, dynamic per album)
- Context Variables:
  - albums: List of Dict with {
      album_id (int), title (str), artist_name (str), year (int)
    }
  - sort_options: List[str] = ["By Title", "By Artist", "By Year"]
- Navigation Mappings:
  - view-album-button-{{album_id}} --> album_details

---

### Template: album_details.html
- Template File Path: templates/album_details.html
- Page Title: <title>Album Details</title>
- H1 Content: album title (id: album-title)
- Required Element IDs:
  - album-details-page (Div)
  - album-title (H1)
  - album-artist (Div)
  - album-year (Div)
  - album-songs-list (Div)
  - add-album-to-playlist-button (Button)
- Context Variables:
  - album: Dict with {
      album_id (int), title (str), artist_name (str), release_year (int)
    }
  - songs: List of Dict with {
      song_id (int), title (str), duration (int)
    }
- Navigation Mappings:
  - add-album-to-playlist-button triggers POST to add_album_to_playlist

---

### Template: artists.html
- Template File Path: templates/artists.html
- Page Title: <title>Artist Profiles</title>
- H1 Content: "Artist Profiles" (in artists-page div)
- Required Element IDs:
  - artists-page (Div)
  - artists-grid (Div)
  - search-artists (Input)
  - artists-sort (Dropdown)
  - view-artist-button-{{artist.artist_id}} (Button, dynamic per artist)
- Context Variables:
  - artists: List of Dict with {
      artist_id (int), name (str), genre (str)
    }
  - sort_options: List[str] = ["By Name", "By Genre"]
- Navigation Mappings:
  - view-artist-button-{{artist_id}} --> artist_profile

---

### Template: artist_profile.html
- Template File Path: templates/artist_profile.html
- Page Title: <title>Artist Profiles</title>
- H1 Content: artist name (id not specified but shown as primary heading)
- Required Element IDs:
  - No specific container ID specified in user doc for artist profile page.
- Context Variables:
  - artist: Dict with {
      artist_id (int), name (str), genre (str), country (str), formation_year (int)
    }
- Navigation Mappings: None explicitly given except usual navigation controls

---

### Template: genres.html
- Template File Path: templates/genres.html
- Page Title: <title>Genre Exploration</title>
- H1 Content: "Genre Exploration" (in genres-page div)
- Required Element IDs:
  - genres-page (Div)
  - genres-list (Div)
  - select-genre (Dropdown)
  - genre-songs (Div)
  - genre-artists (Div)
  - back-to-dashboard (Button)
- Context Variables:
  - genres: List of Dict with {
      genre_id (int), genre_name (str), description (str)
    }
  - songs: List of Dict with {
      song_id (int), title (str), artist_name (str)
    } filtered by selected genre
  - artists: List of Dict with {
      artist_id (int), name (str)
    } filtered by selected genre
- Navigation Mappings:
  - back-to-dashboard --> dashboard

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. songs.txt
- Relative Path: data/songs.txt
- File Format: Pipe-delimited (|)
- Field Order and Descriptions:
  1. song_id (int): Unique identifier for song
  2. title (str): Song title
  3. artist_id (int): Reference to artist_id in artists.txt
  4. album_id (int): Reference to album_id in albums.txt
  5. genre (str): Genre of the song
  6. duration (int): Duration of the song in seconds
  7. release_date (str): Release date in YYYY-MM-DD format
  8. play_count (int): Number of times the song has been played
- Example Rows:
  ```
  1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
  2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
  3|Shape of You|3|3|Pop|233|2017-01-06|4200000
  ```

### 2. artists.txt
- Relative Path: data/artists.txt
- File Format: Pipe-delimited (|)
- Field Order and Descriptions:
  1. artist_id (int): Unique identifier for artist
  2. name (str): Artist name
  3. genre (str): Primary genre
  4. country (str): Country of origin
  5. formation_year (int): Year artist or band formed
- Example Rows:
  ```
  1|Queen|Rock|United Kingdom|1970
  2|The Weeknd|Synth-Pop|Canada|2010
  3|Ed Sheeran|Pop|United Kingdom|2005
  ```

### 3. albums.txt
- Relative Path: data/albums.txt
- File Format: Pipe-delimited (|)
- Field Order and Descriptions:
  1. album_id (int): Unique album identifier
  2. title (str): Album title
  3. artist_id (int): Reference to artist_id in artists.txt
  4. release_year (int): Year album was released
  5. total_songs (int): Number of songs in album
  6. genre (str): Album genre
- Example Rows:
  ```
  1|A Night at the Opera|1|1975|11|Rock
  2|After Hours|2|2019|14|Synth-Pop
  3|Divide|3|2017|12|Pop
  ```

### 4. genres.txt
- Relative Path: data/genres.txt
- File Format: Pipe-delimited (|)
- Field Order and Descriptions:
  1. genre_id (int): Unique genre identifier
  2. genre_name (str): Name of genre
  3. description (str): Description about the genre
- Example Rows:
  ```
  1|Rock|Guitar-driven music with strong beats and vocals
  2|Pop|Catchy mainstream music with broad appeal
  3|Hip-Hop|Rhythmic music with rap vocals and beat production
  ```

### 5. playlists.txt
- Relative Path: data/playlists.txt
- File Format: Pipe-delimited (|)
- Field Order and Descriptions:
  1. playlist_id (int): Unique playlist identifier
  2. title (str): Playlist title
  3. description (str): Playlist description
  4. creation_date (str): Date playlist was created (YYYY-MM-DD)
  5. total_songs (int): Number of songs in playlist
- Example Rows:
  ```
  1|Workout Mix|High energy songs for the gym|2025-01-15|25
  2|Chill Vibes|Relaxing music for study|2025-01-16|18
  3|Party Hits|Latest party tracks|2025-01-17|32
  ```

### 6. playlist_songs.txt
- Relative Path: data/playlist_songs.txt
- File Format: Pipe-delimited (|)
- Field Order and Descriptions:
  1. playlist_song_id (int): Unique identifier for the record
  2. playlist_id (int): Reference to playlists.txt (playlist_id)
  3. song_id (int): Reference to songs.txt (song_id)
  4. added_date (str): Date song added to playlist (YYYY-MM-DD)
- Example Rows:
  ```
  1|1|2|2025-01-15
  2|1|3|2025-01-15
  3|2|1|2025-01-16
  ```

---

*End of Design Specification*