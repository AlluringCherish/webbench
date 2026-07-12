# Design Specification for MusicStreaming Web Application

---

## Section 1: Flask Routes Specification

| Route Path                | Function Name           | HTTP Methods | Template Filename           | Context Variables Description |
|---------------------------|-------------------------|--------------|-----------------------------|-------------------------------|
| /                         | redirect_to_dashboard   | GET          | None (redirect)             | None                          |
| /dashboard                | dashboard               | GET          | dashboard.html              | {
  "featured_songs": List[Dict] (song_id: int, title: str, artist_name: str, duration: int, cover_art_url: str),
  "trending_artists": List[Dict] (artist_id: int, name: str, genre: str, photo_url: str)
} |
| /songs                   | song_catalog            | GET, POST    | song_catalog.html           | {
  "songs": List[Dict] (song_id: int, title: str, artist_name: str, album_name: str, genre: str, duration: int),
  "search_query": str (optional, from POST),
  "selected_genre": str (optional, from POST)
} |
| /songs/<int:song_id>      | song_details            | GET          | song_details.html           | {
  "song": Dict (song_id: int, title: str, artist_id: int, artist_name: str, album_id: int, album_name: str, genre: str, duration: int, release_date: str)
} |
| /playlists               | playlists               | GET          | playlists.html              | {
  "playlists": List[Dict] (playlist_id: int, title: str, description: str, total_songs: int)
} |
| /playlists/<int:playlist_id> | playlist_details     | GET          | playlist_details.html       | {
  "playlist": Dict (playlist_id: int, title: str, description: str),
  "songs": List[Dict] (song_id: int, title: str, artist_name: str, duration: int)
} |
| /playlists/create        | create_playlist          | GET, POST    | create_playlist.html        | None for GET; POST context includes validation messages and form data as needed |
| /albums                  | album_browse            | GET          | albums.html                 | {
  "albums": List[Dict] (album_id: int, title: str, artist_name: str, release_year: int, genre: str),
  "search_query": str (optional),
  "sort_option": str (optional: "title", "artist", "year")
} |
| /albums/<int:album_id>    | album_details           | GET          | album_details.html          | {
  "album": Dict (album_id: int, title: str, artist_name: str, release_year: int),
  "songs": List[Dict] (song_id: int, title: str, duration: int)
} |
| /artists                 | artist_profiles         | GET          | artists.html                | {
  "artists": List[Dict] (artist_id: int, name: str, genre: str, photo_url: str),
  "search_query": str (optional),
  "sort_option": str (optional: "name", "genre")
} |
| /artists/<int:artist_id>  | artist_profile          | GET          | artist_profile.html         | {
  "artist": Dict (artist_id: int, name: str, genre: str, country: str, formation_year: int),
  "songs": List[Dict] (song_id: int, title: str, album_name: str, duration: int)
} |
| /genres                  | genre_exploration       | GET, POST    | genres.html                 | {
  "genres": List[Dict] (genre_id: int, genre_name: str, description: str),
  "selected_genre": str (optional, from POST),
  "genre_songs": List[Dict] (song_id: int, title: str, artist_name: str, duration: int),
  "genre_artists": List[Dict] (artist_id: int, name: str, genre: str)
} |

---

## Section 2: HTML Template Specifications

### templates/dashboard.html
- Page Title: Music Streaming Dashboard
- Main Heading (<h1>): Music Streaming Dashboard
- Elements and IDs:
  - Div: dashboard-page
  - Div: featured-songs
  - Button: browse-songs-button
  - Button: my-playlists-button
  - Button: trending-artists-button
- Context Variables:
  - featured_songs: List of dict with keys (song_id: int, title: str, artist_name: str, duration: int, cover_art_url: str)
  - trending_artists: List of dict with keys (artist_id: int, name: str, genre: str, photo_url: str)
- Navigation IDs to Routes:
  - browse-songs-button -> song_catalog
  - my-playlists-button -> playlists
  - trending-artists-button -> artist_profiles

### templates/song_catalog.html
- Page Title: Song Catalog
- Main Heading (<h1>): Song Catalog
- Elements and IDs:
  - Div: catalog-page
  - Input: search-input
  - Dropdown: genre-filter
  - Div: songs-grid
  - Button: add-to-playlist-button-{{ song.song_id }} (dynamic per song)
- Context Variables:
  - songs: List of dict with keys (song_id: int, title: str, artist_name: str, album_name: str, genre: str, duration: int)
  - search_query: str
  - selected_genre: str
- Navigation IDs to Routes:
  - add-to-playlist-button-{{ song.song_id }} -> None (AJAX or backend add to playlist handler, no route specified in requirements)

### templates/song_details.html
- Page Title: Song Details
- Main Heading (<h1>): Song Details
- Elements and IDs:
  - Div: song-details-page
  - H1: song-title
  - Div: artist-name (with link to artist_profile route)
  - Div: album-name
  - Div: duration-display
  - Button: play-button
- Context Variables:
  - song: dict with keys (song_id: int, title: str, artist_id: int, artist_name: str, album_id: int, album_name: str, genre: str, duration: int, release_date: str)
- Navigation IDs to Routes:
  - artist-name (link) -> artist_profile with artist_id=song.artist_id

### templates/playlists.html
- Page Title: My Playlists
- Main Heading (<h1>): My Playlists
- Elements and IDs:
  - Div: playlists-page
  - Div: playlists-grid
  - Button: create-playlist-button
  - Button: view-playlist-button-{{ playlist.playlist_id }} (dynamic per playlist)
  - Button: back-to-dashboard
- Context Variables:
  - playlists: List of dict with keys (playlist_id: int, title: str, description: str, total_songs: int)
- Navigation IDs to Routes:
  - create-playlist-button -> create_playlist
  - view-playlist-button-{{ playlist.playlist_id }} -> playlist_details with playlist_id
  - back-to-dashboard -> dashboard

### templates/playlist_details.html
- Page Title: Playlist Details
- Main Heading (<h1>): Playlist Details
- Elements and IDs:
  - Div: playlist-details-page
  - H1: playlist-title
  - Div: playlist-description
  - Table: songs-in-playlist
  - Button: remove-song-button-{{ song.song_id }} (dynamic per song)
  - Button: delete-playlist-button
- Context Variables:
  - playlist: dict (playlist_id: int, title: str, description: str)
  - songs: List of dict (song_id: int, title: str, artist_name: str, duration: int)
- Navigation IDs to Routes:
  - Buttons remove-song-button-{{ song.song_id }} -> None (action handler to remove song)
  - delete-playlist-button -> None (handler to delete playlist)

### templates/create_playlist.html
- Page Title: Create New Playlist
- Main Heading (<h1>): Create New Playlist
- Elements and IDs:
  - Div: create-playlist-page
  - Input: playlist-name-input
  - Textarea: playlist-description-input
  - Button: save-playlist-button
  - Button: cancel-create-button
- Context Variables:
  - None for GET; POST may have validation errors and form data
- Navigation IDs to Routes:
  - cancel-create-button -> playlists

### templates/albums.html
- Page Title: Albums
- Main Heading (<h1>): Albums
- Elements and IDs:
  - Div: albums-page
  - Div: albums-grid
  - Input: search-albums
  - Dropdown: sort-albums
  - Button: view-album-button-{{ album.album_id }} (dynamic per album)
- Context Variables:
  - albums: List of dict (album_id: int, title: str, artist_name: str, release_year: int, genre: str)
  - search_query: str
  - sort_option: str
- Navigation IDs to Routes:
  - view-album-button-{{ album.album_id }} -> album_details with album_id

### templates/album_details.html
- Page Title: Album Details
- Main Heading (<h1>): Album Details
- Elements and IDs:
  - Div: album-details-page
  - H1: album-title
  - Div: album-artist
  - Div: album-year
  - Div: album-songs-list
  - Button: add-album-to-playlist-button
- Context Variables:
  - album: dict (album_id: int, title: str, artist_name: str, release_year: int)
  - songs: List of dict (song_id: int, title: str, duration: int)
- Navigation IDs to Routes:
  - add-album-to-playlist-button -> None (handler to add all songs to playlist)

### templates/artists.html
- Page Title: Artist Profiles
- Main Heading (<h1>): Artist Profiles
- Elements and IDs:
  - Div: artists-page
  - Div: artists-grid
  - Input: search-artists
  - Dropdown: artists-sort
  - Button: view-artist-button-{{ artist.artist_id }} (dynamic per artist)
- Context Variables:
  - artists: List of dict (artist_id: int, name: str, genre: str, photo_url: str)
  - search_query: str
  - sort_option: str
- Navigation IDs to Routes:
  - view-artist-button-{{ artist.artist_id }} -> artist_profile with artist_id

### templates/artist_profile.html
- Page Title: Artist Profiles
- Main Heading (<h1>): Artist Profiles
- Elements and IDs:
  - Div: artist-profile-page
  - H1: artist-name
  - Div: artist-genre
  - Div: artist-country
  - Div: artist-formation-year
  - Div: artist-songs-list
- Context Variables:
  - artist: dict (artist_id: int, name: str, genre: str, country: str, formation_year: int)
  - songs: List of dict (song_id: int, title: str, album_name: str, duration: int)
- Navigation IDs to Routes:
  - None specified

### templates/genres.html
- Page Title: Genre Exploration
- Main Heading (<h1>): Genre Exploration
- Elements and IDs:
  - Div: genres-page
  - Div: genres-list
  - Dropdown: select-genre
  - Div: genre-songs
  - Div: genre-artists
  - Button: back-to-dashboard
- Context Variables:
  - genres: List of dict (genre_id: int, genre_name: str, description: str)
  - selected_genre: str
  - genre_songs: List of dict (song_id: int, title: str, artist_name: str, duration: int)
  - genre_artists: List of dict (artist_id: int, name: str, genre: str)
- Navigation IDs to Routes:
  - back-to-dashboard -> dashboard

---

## Section 3: Data File Schemas

### 1. songs.txt
- Relative Path: data/songs.txt
- Format: Pipe-delimited text
- Fields and Order:
  1. song_id (int): Unique identifier for each song
  2. title (str): Song title
  3. artist_id (int): Foreign key link to artists.txt
  4. album_id (int): Foreign key link to albums.txt
  5. genre (str): Music genre
  6. duration (int): Duration in seconds
  7. release_date (str): YYYY-MM-DD format
  8. play_count (int): Number of times played
- Example Rows:
  ```
  1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
  2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
  3|Shape of You|3|3|Pop|233|2017-01-06|4200000
  ```
- Relationships:
  - artist_id references artists.txt
  - album_id references albums.txt

### 2. artists.txt
- Relative Path: data/artists.txt
- Format: Pipe-delimited text
- Fields and Order:
  1. artist_id (int): Unique identifier for artist
  2. name (str): Artist name
  3. genre (str): Primary genre
  4. country (str): Artist's country
  5. formation_year (int): Year founded
- Example Rows:
  ```
  1|Queen|Rock|United Kingdom|1970
  2|The Weeknd|Synth-Pop|Canada|2010
  3|Ed Sheeran|Pop|United Kingdom|2005
  ```
- Relationships:
  - referenced by songs.txt and albums.txt

### 3. albums.txt
- Relative Path: data/albums.txt
- Format: Pipe-delimited text
- Fields and Order:
  1. album_id (int): Unique album identifier
  2. title (str): Album title
  3. artist_id (int): Foreign key to artists.txt
  4. release_year (int): Year released
  5. total_songs (int): Number of songs in album
  6. genre (str): Album genre
- Example Rows:
  ```
  1|A Night at the Opera|1|1975|11|Rock
  2|After Hours|2|2019|14|Synth-Pop
  3|Divide|3|2017|12|Pop
  ```
- Relationships:
  - artist_id references artists.txt

### 4. genres.txt
- Relative Path: data/genres.txt
- Format: Pipe-delimited text
- Fields and Order:
  1. genre_id (int): Unique genre identifier
  2. genre_name (str): Name of the genre
  3. description (str): Description of the genre
- Example Rows:
  ```
  1|Rock|Guitar-driven music with strong beats and vocals
  2|Pop|Catchy mainstream music with broad appeal
  3|Hip-Hop|Rhythmic music with rap vocals and beat production
  ```
- Relationships:
  - genre_name used in songs.txt genre field

### 5. playlists.txt
- Relative Path: data/playlists.txt
- Format: Pipe-delimited text
- Fields and Order:
  1. playlist_id (int): Unique playlist identifier
  2. title (str): Playlist title
  3. description (str): Playlist description
  4. creation_date (str): YYYY-MM-DD date playlist created
  5. total_songs (int): Number of songs in playlist
- Example Rows:
  ```
  1|Workout Mix|High energy songs for the gym|2025-01-15|25
  2|Chill Vibes|Relaxing music for study|2025-01-16|18
  3|Party Hits|Latest party tracks|2025-01-17|32
  ```
- Relationships:
  - playlist_id referenced in playlist_songs.txt

### 6. playlist_songs.txt
- Relative Path: data/playlist_songs.txt
- Format: Pipe-delimited text
- Fields and Order:
  1. playlist_song_id (int): Unique identifier for playlist-song relation
  2. playlist_id (int): Foreign key to playlists.txt
  3. song_id (int): Foreign key to songs.txt
  4. added_date (str): Date song was added YYYY-MM-DD
- Example Rows:
  ```
  1|1|2|2025-01-15
  2|1|3|2025-01-15
  3|2|1|2025-01-16
  ```
- Relationships:
  - playlist_id references playlists.txt
  - song_id references songs.txt

---