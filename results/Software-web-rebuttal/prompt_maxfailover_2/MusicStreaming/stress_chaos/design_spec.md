# MusicStreaming Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                     | Function Name           | HTTP Method(s) | Template File             | Context Variables                                                                                                    |
|-------------------------------|-------------------------|----------------|---------------------------|---------------------------------------------------------------------------------------------------------------------|
| /                             | root_redirect            | GET            | -                         | None (Redirects to `/dashboard`)                                                                                     |
| /dashboard                    | dashboard_page           | GET            | dashboard.html            | featured_songs: list of dict {song_id: int, title: str, artist_name: str, duration: int}
  trending_artists: list of dict {artist_id: int, name: str, genre: str}
|
| /songs                       | song_catalog             | GET            | song_catalog.html         | songs: list of dict {song_id: int, title: str, artist_name: str, album_name: str, genre: str, duration: int}
  genres: list of str (genre names)
  selected_genre: str or None (currently selected genre for filter or None if not filtered)
  search_query: str (search term or empty string)
|
| /songs/<int:song_id>         | song_details             | GET            | song_details.html         | song: dict {
    song_id: int,
    title: str,
    artist_id: int,
    artist_name: str,
    album_id: int,
    album_name: str,
    duration: int,
    genre: str
  }
|
| /playlists                   | playlists_page           | GET            | playlists.html            | playlists: list of dict {playlist_id: int, title: str, total_songs: int}
|
| /playlists/<int:playlist_id> | playlist_details         | GET            | playlist_details.html     | playlist: dict {playlist_id: int, title: str, description: str}
  songs_in_playlist: list of dict {song_id: int, title: str, artist_name: str, duration: int}
|
| /playlists/create            | create_playlist_page     | GET            | create_playlist.html      | None                                                                                                                |
| /playlists/create            | create_playlist_submit   | POST           | -                         | Form data: playlist_name: str, playlist_description: str
|
| /albums                     | albums_page              | GET            | albums.html               | albums: list of dict {album_id: int, title: str, artist_name: str, release_year: int}
  search_query: str (search term or empty string)
  sort_option: str (e.g., "By Title", "By Artist", "By Year")
|
| /albums/<int:album_id>       | album_details            | GET            | album_details.html        | album: dict {album_id: int, title: str, artist_id: int, artist_name: str, release_year: int, genre: str}
  album_songs: list of dict {song_id: int, title: str, duration: int}
|
| /artists                    | artists_page             | GET            | artists.html              | artists: list of dict {artist_id: int, name: str, genre: str, country: str}
  search_query: str (search term or empty string)
  sort_option: str (e.g., "By Name", "By Genre")
|
| /artists/<int:artist_id>     | artist_profile           | GET            | artist_profile.html       | artist: dict {artist_id: int, name: str, genre: str, country: str, formation_year: int}
  artist_songs: list of dict {song_id: int, title: str, album_name: str, duration: int}
  artist_albums: list of dict {album_id: int, title: str, release_year: int}
|
| /genres                     | genre_exploration_page   | GET            | genres.html               | genres: list of dict {genre_id: int, genre_name: str, description: str}
  selected_genre_id: int or None
  genre_songs: list of dict {song_id: int, title: str, artist_name: str, duration: int}
  genre_artists: list of dict {artist_id: int, name: str, genre: str}
|

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### Template: templates/dashboard.html
- Page Title:
  - &lt;title&gt;Music Streaming Dashboard&lt;/title&gt;
  - &lt;h1&gt;Music Streaming Dashboard&lt;/h1&gt;
- Required Element IDs:
  - dashboard-page (Div)
  - featured-songs (Div)
  - browse-songs-button (Button)
  - my-playlists-button (Button)
  - trending-artists-button (Button)
- Context Variables:
  - featured_songs: list of songs, each:
    * song_id (int)
    * title (str)
    * artist_name (str)
    * duration (int)
  - trending_artists: list of artists, each:
    * artist_id (int)
    * name (str)
    * genre (str)
- Navigation Mappings:
  - browse-songs-button -> function: song_catalog
  - my-playlists-button -> function: playlists_page
  - trending-artists-button -> function: artists_page

---

### Template: templates/song_catalog.html
- Page Title:
  - &lt;title&gt;Song Catalog&lt;/title&gt;
  - &lt;h1&gt;Song Catalog&lt;/h1&gt;
- Required Element IDs:
  - catalog-page (Div)
  - search-input (Input)
  - genre-filter (Dropdown)
  - songs-grid (Div)
  - add-to-playlist-button-{{ song.song_id }} (Button) (one per song, dynamic)
- Context Variables:
  - songs: list of songs, each:
    * song_id (int)
    * title (str)
    * artist_name (str)
    * album_name (str)
    * genre (str)
    * duration (int)
  - genres: list of genre names (str)
  - selected_genre: str or None
  - search_query: str
- Navigation Mappings:
  - add-to-playlist-button-{{ song.song_id }} -> function: add_song_to_playlist (this function, while not defined as route, represents the action triggered)

---

### Template: templates/song_details.html
- Page Title:
  - &lt;title&gt;Song Details&lt;/title&gt;
  - &lt;h1 id="song-title"&gt;{{ song.title }}&lt;/h1&gt;
- Required Element IDs:
  - song-details-page (Div)
  - song-title (H1)
  - artist-name (Div)
  - album-name (Div)
  - duration-display (Div)
  - play-button (Button)
- Context Variables:
  - song: dict
    * song_id (int)
    * title (str)
    * artist_id (int)
    * artist_name (str)
    * album_id (int)
    * album_name (str)
    * duration (int)
    * genre (str)
- Navigation Mappings:
  - artist-name (Div with link) -> function: artist_profile (dynamic route /artists/&lt;artist_id&gt;)

---

### Template: templates/playlists.html
- Page Title:
  - &lt;title&gt;My Playlists&lt;/title&gt;
  - &lt;h1&gt;My Playlists&lt;/h1&gt;
- Required Element IDs:
  - playlists-page (Div)
  - playlists-grid (Div)
  - create-playlist-button (Button)
  - view-playlist-button-{{ playlist.playlist_id }} (Button) (dynamic per playlist)
  - back-to-dashboard (Button)
- Context Variables:
  - playlists: list of playlists, each:
    * playlist_id (int)
    * title (str)
    * total_songs (int)
- Navigation Mappings:
  - create-playlist-button -> function: create_playlist_page
  - view-playlist-button-{{ playlist.playlist_id }} -> function: playlist_details
  - back-to-dashboard -> function: dashboard_page

---

### Template: templates/playlist_details.html
- Page Title:
  - &lt;title&gt;Playlist Details&lt;/title&gt;
  - &lt;h1 id="playlist-title"&gt;{{ playlist.title }}&lt;/h1&gt;
- Required Element IDs:
  - playlist-details-page (Div)
  - playlist-title (H1)
  - playlist-description (Div)
  - songs-in-playlist (Table)
  - remove-song-button-{{ song.song_id }} (Button) (dynamic per song)
  - delete-playlist-button (Button)
- Context Variables:
  - playlist: dict
    * playlist_id (int)
    * title (str)
    * description (str)
  - songs_in_playlist: list of songs, each:
    * song_id (int)
    * title (str)
    * artist_name (str)
    * duration (int)
- Navigation Mappings:
  - remove-song-button-{{ song.song_id }} -> function: remove_song_from_playlist
  - delete-playlist-button -> function: delete_playlist

---

### Template: templates/create_playlist.html
- Page Title:
  - &lt;title&gt;Create New Playlist&lt;/title&gt;
  - &lt;h1&gt;Create New Playlist&lt;/h1&gt;
- Required Element IDs:
  - create-playlist-page (Div)
  - playlist-name-input (Input)
  - playlist-description-input (Textarea)
  - save-playlist-button (Button)
  - cancel-create-button (Button)
- Context Variables:
  - None
- Navigation Mappings:
  - save-playlist-button -> function: create_playlist_submit (form POST)
  - cancel-create-button -> function: playlists_page

---

### Template: templates/albums.html
- Page Title:
  - &lt;title&gt;Albums&lt;/title&gt;
  - &lt;h1&gt;Albums&lt;/h1&gt;
- Required Element IDs:
  - albums-page (Div)
  - albums-grid (Div)
  - search-albums (Input)
  - sort-albums (Dropdown)
  - view-album-button-{{ album.album_id }} (Button) (dynamic per album)
- Context Variables:
  - albums: list of albums, each:
    * album_id (int)
    * title (str)
    * artist_name (str)
    * release_year (int)
  - search_query: str
  - sort_option: str
- Navigation Mappings:
  - view-album-button-{{ album.album_id }} -> function: album_details

---

### Template: templates/album_details.html
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
  - album: dict
    * album_id (int)
    * title (str)
    * artist_id (int)
    * artist_name (str)
    * release_year (int)
    * genre (str)
  - album_songs: list of songs, each:
    * song_id (int)
    * title (str)
    * duration (int)
- Navigation Mappings:
  - add-album-to-playlist-button -> function: add_album_to_playlist

---

### Template: templates/artists.html
- Page Title:
  - &lt;title&gt;Artist Profiles&lt;/title&gt;
  - &lt;h1&gt;Artist Profiles&lt;/h1&gt;
- Required Element IDs:
  - artists-page (Div)
  - artists-grid (Div)
  - search-artists (Input)
  - artists-sort (Dropdown)
  - view-artist-button-{{ artist.artist_id }} (Button) (dynamic per artist)
- Context Variables:
  - artists: list of artists, each:
    * artist_id (int)
    * name (str)
    * genre (str)
    * country (str)
  - search_query: str
  - sort_option: str
- Navigation Mappings:
  - view-artist-button-{{ artist.artist_id }} -> function: artist_profile

---

### Template: templates/artist_profile.html
- Page Title:
  - &lt;title&gt;Artist Profiles&lt;/title&gt;
  - &lt;h1&gt;{{ artist.name }}&lt;/h1&gt;
- Required Element IDs:
  - artist-profile-page (Div) (implied container for this page)
  - artist-name (H1) (can reuse artist.name in h1)
  - (Use appropriate Divs or Lists for songs and albums as per layout, but focusing on IDs below)
- Context Variables:
  - artist: dict
    * artist_id (int)
    * name (str)
    * genre (str)
    * country (str)
    * formation_year (int)
  - artist_songs: list of songs, each:
    * song_id (int)
    * title (str)
    * album_name (str)
    * duration (int)
  - artist_albums: list of albums, each:
    * album_id (int)
    * title (str)
    * release_year (int)
- Navigation Mappings:
  - Songs and albums clickable or linked as desired, typically linking to song_details and album_details routes respectively

---

### Template: templates/genres.html
- Page Title:
  - &lt;title&gt;Genre Exploration&lt;/title&gt;
  - &lt;h1&gt;Genre Exploration&lt;/h1&gt;
- Required Element IDs:
  - genres-page (Div)
  - genres-list (Div)
  - select-genre (Dropdown)
  - genre-songs (Div)
  - genre-artists (Div)
  - back-to-dashboard (Button)
- Context Variables:
  - genres: list of genres, each:
    * genre_id (int)
    * genre_name (str)
    * description (str)
  - selected_genre_id: int or None
  - genre_songs: list of songs, each:
    * song_id (int)
    * title (str)
    * artist_name (str)
    * duration (int)
  - genre_artists: list of artists, each:
    * artist_id (int)
    * name (str)
    * genre (str)
- Navigation Mappings:
  - back-to-dashboard -> function: dashboard_page

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. Songs Data
- Filename: data/songs.txt
- File format: pipe-delimited (|)
- Fields:
  1. song_id (int): Unique identifier for the song
  2. title (str): Title of the song
  3. artist_id (int): Foreign key referencing artists.txt artist_id
  4. album_id (int): Foreign key referencing albums.txt album_id
  5. genre (str): Genre name
  6. duration (int): Duration in seconds
  7. release_date (str): Date of release in YYYY-MM-DD
  8. play_count (int): Total play count
- Example rows:
  ```
  1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
  2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
  3|Shape of You|3|3|Pop|233|2017-01-06|4200000
  ```

### 2. Artists Data
- Filename: data/artists.txt
- File format: pipe-delimited (|)
- Fields:
  1. artist_id (int): Unique artist identifier
  2. name (str): Artist name
  3. genre (str): Primary genre
  4. country (str): Country of origin
  5. formation_year (int): Year artist/band formed
- Example rows:
  ```
  1|Queen|Rock|United Kingdom|1970
  2|The Weeknd|Synth-Pop|Canada|2010
  3|Ed Sheeran|Pop|United Kingdom|2005
  ```

### 3. Albums Data
- Filename: data/albums.txt
- File format: pipe-delimited (|)
- Fields:
  1. album_id (int): Unique album identifier
  2. title (str): Album title
  3. artist_id (int): Foreign key referencing artists.txt artist_id
  4. release_year (int): Year album released
  5. total_songs (int): Number of songs in album
  6. genre (str): Album genre
- Example rows:
  ```
  1|A Night at the Opera|1|1975|11|Rock
  2|After Hours|2|2019|14|Synth-Pop
  3|Divide|3|2017|12|Pop
  ```

### 4. Genres Data
- Filename: data/genres.txt
- File format: pipe-delimited (|)
- Fields:
  1. genre_id (int): Unique genre identifier
  2. genre_name (str): Name of the genre
  3. description (str): Description of the genre
- Example rows:
  ```
  1|Rock|Guitar-driven music with strong beats and vocals
  2|Pop|Catchy mainstream music with broad appeal
  3|Hip-Hop|Rhythmic music with rap vocals and beat production
  ```

### 5. Playlists Data
- Filename: data/playlists.txt
- File format: pipe-delimited (|)
- Fields:
  1. playlist_id (int): Unique playlist identifier
  2. title (str): Playlist title
  3. description (str): Playlist description
  4. creation_date (str): Date created in YYYY-MM-DD
  5. total_songs (int): Number of songs in the playlist
- Example rows:
  ```
  1|Workout Mix|High energy songs for the gym|2025-01-15|25
  2|Chill Vibes|Relaxing music for study|2025-01-16|18
  3|Party Hits|Latest party tracks|2025-01-17|32
  ```

### 6. Playlist Songs Data
- Filename: data/playlist_songs.txt
- File format: pipe-delimited (|)
- Fields:
  1. playlist_song_id (int): Unique identifier for playlist-song relation
  2. playlist_id (int): Foreign key referencing playlists.txt playlist_id
  3. song_id (int): Foreign key referencing songs.txt song_id
  4. added_date (str): Date song was added in YYYY-MM-DD
- Example rows:
  ```
  1|1|2|2025-01-15
  2|1|3|2025-01-15
  3|2|1|2025-01-16
  ```

---

# End of Design Specification
