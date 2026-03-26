# MusicStreaming Application Design Specification

---

## 1. Flask Routes Specification (Backend Developer Focus)

| Route Path                       | Flask Function Name           | HTTP Method(s) | Template Name           | Context Variables Passed to Template                                               |
|---------------------------------|------------------------------|----------------|-------------------------|------------------------------------------------------------------------------------|
| `/`                             | `root_redirect`               | GET            | None (Redirect)          | None (Redirects to `/dashboard`)                                                  |
| `/dashboard`                   | `dashboard`                  | GET            | `dashboard.html`         | `featured_songs`: List[Dict] (song_id: int, title: str, artist_name: str, duration: int)
`trending_artists`: List[Dict] (artist_id: int, name: str) |
| `/songs`                      | `song_catalog`               | GET            | `song_catalog.html`      | `songs`: List[Dict] (song_id: int, title: str, artist_name: str, album_name: str, genre: str, duration: int)
`genres`: List[str] (e.g., Pop, Rock, Hip-Hop)                                       |
| `/songs/<int:song_id>`          | `song_details`               | GET            | `song_details.html`      | `song`: Dict {
  song_id: int
  title: str
  artist_id: int
  artist_name: str
  album_id: int
  album_name: str
  genre: str
  duration: int
  release_date: str (YYYY-MM-DD)
  play_count: int
}                                                                                  |
| `/playlists`                   | `playlists`                  | GET            | `playlists.html`         | `playlists`: List[Dict] (playlist_id: int, title: str, description: str, total_songs: int)                                                        |
| `/playlists/<int:playlist_id>` | `playlist_details`           | GET            | `playlist_details.html`  | `playlist`: Dict {
  playlist_id: int
  title: str
  description: str
  creation_date: str (YYYY-MM-DD)
  total_songs: int
}
`songs_in_playlist`: List[Dict] (song_id: int, title: str, artist_name: str, duration: int)                                                  |
| `/playlists/create`            | `create_playlist`            | GET, POST     | `create_playlist.html`   | On GET: None
On POST: Possibly form data for creating playlist; on redisplay, on error, context with errors or submitted fields as needed      |
| `/albums`                     | `albums`                    | GET            | `albums.html`            | `albums`: List[Dict] (album_id: int, title: str, artist_name: str, year: int, genre: str)                                                        |
| `/albums/<int:album_id>`        | `album_details`              | GET            | `album_details.html`     | `album`: Dict {
  album_id: int
  title: str
  artist_id: int
  artist_name: str
  release_year: int
  genre: str
  total_songs: int
}
`songs_in_album`: List[Dict] (song_id: int, title: str, duration: int)                                                        |
| `/artists`                   | `artists`                   | GET            | `artists.html`           | `artists`: List[Dict] (artist_id: int, name: str, genre: str, country: str, formation_year: int)                                                 |
| `/artists/<int:artist_id>`      | `artist_profile`             | GET            | `artist_profile.html`    | `artist`: Dict {
  artist_id: int
  name: str
  genre: str
  country: str
  formation_year: int
}
`songs`: List[Dict] (song_id: int, title: str, album_name: str, duration: int)
`albums`: List[Dict] (album_id: int, title: str, release_year: int)
                                             |
| `/genres`                    | `genre_exploration`          | GET            | `genres.html`            | `genres`: List[Dict] (genre_id: int, genre_name: str, description: str)
`selected_genre`: Optional[str] (genre_name)
`genre_songs`: List[Dict] (song_id: int, title: str, artist_name: str, duration: int)
`genre_artists`: List[Dict] (artist_id: int, name: str)                                          |

---

## 2. HTML Template Specifications (Frontend Developer Focus)

### Template: `templates/dashboard.html`
- Title: "Music Streaming Dashboard"
- H1 content: "Music Streaming Dashboard"
- Element IDs:
  - `dashboard-page` (Div)
  - `featured-songs` (Div)
  - `browse-songs-button` (Button)
  - `my-playlists-button` (Button)
  - `trending-artists-button` (Button)
- Context Variables:
  - `featured_songs`: List of dictionaries with keys: `song_id` (int), `title` (str), `artist_name` (str), `duration` (int, seconds)
  - `trending_artists`: List of dictionaries with keys: `artist_id` (int), `name` (str)
- Navigation Mapping:
  - `browse-songs-button` => `song_catalog`
  - `my-playlists-button` => `playlists`
  - `trending-artists-button` => `artists`

---

### Template: `templates/song_catalog.html`
- Title: "Song Catalog"
- H1 content: Not explicitly defined; can be assumed as page container or heading inside `catalog-page` div if needed.
- Element IDs:
  - `catalog-page` (Div)
  - `search-input` (Input)
  - `genre-filter` (Dropdown)
  - `songs-grid` (Div)
  - `add-to-playlist-button-{{song_id}}` (Button) - dynamic per song, use Jinja2 template syntax for `song_id`
- Context Variables:
  - `songs`: List of dictionaries with keys: `song_id` (int), `title` (str), `artist_name` (str), `album_name` (str), `genre` (str), `duration` (int)
  - `genres`: List[str] of genre names
- Navigation Mapping:
  Not explicit beyond adding songs to playlist; can invoke backend action on button click, no route change specified.

---

### Template: `templates/song_details.html`
- Title: "Song Details"
- H1 content: The song title displayed dynamically (`song.title`)
- Element IDs:
  - `song-details-page` (Div)
  - `song-title` (H1)
  - `artist-name` (Div) - clickable, links to artist profile page
  - `album-name` (Div)
  - `duration-display` (Div)
  - `play-button` (Button)
- Context Variables:
  - `song`: Dictionary with fields:
    - `song_id` (int)
    - `title` (str)
    - `artist_id` (int)
    - `artist_name` (str)
    - `album_id` (int)
    - `album_name` (str)
    - `genre` (str)
    - `duration` (int)
    - `release_date` (str, YYYY-MM-DD)
    - `play_count` (int)
- Navigation Mapping:
  - `artist-name` element links to route `artist_profile` with `artist_id` = `song.artist_id` (Jinja2: `url_for('artist_profile', artist_id=song.artist_id)`)

---

### Template: `templates/playlists.html`
- Title: "My Playlists"
- H1 content: Not explicitly defined but implied for the page
- Element IDs:
  - `playlists-page` (Div)
  - `playlists-grid` (Div)
  - `create-playlist-button` (Button)
  - `view-playlist-button-{{playlist_id}}` (Button) - dynamic per playlist
  - `back-to-dashboard` (Button)
- Context Variables:
  - `playlists`: List of dictionaries with keys:
    - `playlist_id` (int)
    - `title` (str)
    - `description` (str)
    - `total_songs` (int)
- Navigation Mapping:
  - `create-playlist-button` => `create_playlist`
  - `back-to-dashboard` => `dashboard`
  - `view-playlist-button-{{playlist_id}}` => `playlist_details` (Jinja2: `url_for('playlist_details', playlist_id=playlist_id)`)

---

### Template: `templates/playlist_details.html`
- Title: "Playlist Details"
- H1 content: The playlist title (dynamic) displayed (e.g., playlist.title)
- Element IDs:
  - `playlist-details-page` (Div)
  - `playlist-title` (H1)
  - `playlist-description` (Div)
  - `songs-in-playlist` (Table)
  - `remove-song-button-{{song_id}}` (Button) - per song in playlist
  - `delete-playlist-button` (Button)
- Context Variables:
  - `playlist`: Dict with fields:
    - `playlist_id` (int)
    - `title` (str)
    - `description` (str)
    - `creation_date` (str, YYYY-MM-DD)
    - `total_songs` (int)
  - `songs_in_playlist`: List of dicts with keys:
    - `song_id` (int)
    - `title` (str)
    - `artist_name` (str)
    - `duration` (int)
- Navigation Mapping:
  - Actions like remove/delete handled by POST or AJAX; no additional navigation specified.

---

### Template: `templates/create_playlist.html`
- Title: "Create New Playlist"
- H1 content: Implied (not explicitly specified, page container is `create-playlist-page`)
- Element IDs:
  - `create-playlist-page` (Div)
  - `playlist-name-input` (Input)
  - `playlist-description-input` (Textarea)
  - `save-playlist-button` (Button)
  - `cancel-create-button` (Button)
- Context Variables:
  - None required on GET; possible form data or errors on POST redisplay (not explicitly defined)
- Navigation Mapping:
  - `cancel-create-button` => redirects (client side or backend) typically to `playlists`

---

### Template: `templates/albums.html`
- Title: "Albums"
- H1 content: Not explicitly defined but logically as container in `albums-page` div
- Element IDs:
  - `albums-page` (Div)
  - `albums-grid` (Div)
  - `search-albums` (Input)
  - `sort-albums` (Dropdown)
  - `view-album-button-{{album_id}}` (Button) - dynamic per album
- Context Variables:
  - `albums`: List of dicts with keys:
    - `album_id` (int)
    - `title` (str)
    - `artist_name` (str)
    - `year` (int)
    - `genre` (str)
- Navigation Mapping:
  - `view-album-button-{{album_id}}` => `album_details` (Jinja2: `url_for('album_details', album_id=album_id)`)

---

### Template: `templates/album_details.html`
- Title: "Album Details"
- H1 content: Dynamic album title (`album.title`)
- Element IDs:
  - `album-details-page` (Div)
  - `album-title` (H1)
  - `album-artist` (Div)
  - `album-year` (Div)
  - `album-songs-list` (Div)
  - `add-album-to-playlist-button` (Button)
- Context Variables:
  - `album`: Dict with fields:
    - `album_id` (int)
    - `title` (str)
    - `artist_id` (int)
    - `artist_name` (str)
    - `release_year` (int)
    - `genre` (str)
    - `total_songs` (int)
  - `songs_in_album`: List of dicts with keys:
    - `song_id` (int)
    - `title` (str)
    - `duration` (int)
- Navigation Mapping:
  Action for `add-album-to-playlist-button` handled server-side or via POST; no navigation specified

---

### Template: `templates/artists.html`
- Title: "Artist Profiles"
- H1 content: Not explicitly defined but assumed container in `artists-page` div
- Element IDs:
  - `artists-page` (Div)
  - `artists-grid` (Div)
  - `search-artists` (Input)
  - `artists-sort` (Dropdown)
  - `view-artist-button-{{artist_id}}` (Button) - dynamic per artist
- Context Variables:
  - `artists`: List of dicts with keys:
    - `artist_id` (int)
    - `name` (str)
    - `genre` (str)
    - `country` (str)
    - `formation_year` (int)
- Navigation Mapping:
  - `view-artist-button-{{artist_id}}` => `artist_profile` (Jinja2: `url_for('artist_profile', artist_id=artist_id)`)

---

### Template: `templates/genres.html`
- Title: "Genre Exploration"
- H1 content: Not explicitly specified, contained within `genres-page` div
- Element IDs:
  - `genres-page` (Div)
  - `genres-list` (Div)
  - `select-genre` (Dropdown)
  - `genre-songs` (Div)
  - `genre-artists` (Div)
  - `back-to-dashboard` (Button)
- Context Variables:
  - `genres`: List of dicts with keys:
    - `genre_id` (int)
    - `genre_name` (str)
    - `description` (str)
  - `selected_genre`: Optional[str], the currently selected genre name
  - `genre_songs`: List of dicts with keys:
    - `song_id` (int)
    - `title` (str)
    - `artist_name` (str)
    - `duration` (int)
  - `genre_artists`: List of dicts with keys:
    - `artist_id` (int)
    - `name` (str)
- Navigation Mapping:
  - `back-to-dashboard` => `dashboard`

---

## 3. Data File Schemas (Backend Developer Focus)

### 1. Songs Data
- Filename & Path: `data/songs.txt`
- Format: Pipe (`|`) delimited text file
- Fields (in order):
  1. `song_id`: int - Unique identifier for the song
  2. `title`: str - Title of the song
  3. `artist_id`: int - Foreign key referencing `artists.txt`'s `artist_id`
  4. `album_id`: int - Foreign key referencing `albums.txt`'s `album_id`
  5. `genre`: str - Genre category of the song
  6. `duration`: int - Duration of the song in seconds
  7. `release_date`: str - Release date in format YYYY-MM-DD
  8. `play_count`: int - Number of times song has been played
- Example Rows:
  ```
  1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
  2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
  3|Shape of You|3|3|Pop|233|2017-01-06|4200000
  ```
- Foreign Key Relationships:
  - `artist_id` references `artists.txt` field `artist_id`
  - `album_id` references `albums.txt` field `album_id`

---

### 2. Artists Data
- Filename & Path: `data/artists.txt`
- Format: Pipe (`|`) delimited text file
- Fields (in order):
  1. `artist_id`: int - Unique identifier for the artist
  2. `name`: str - Name of the artist or band
  3. `genre`: str - Primary genre associated with the artist
  4. `country`: str - Country of origin
  5. `formation_year`: int - Year the artist or band was formed
- Example Rows:
  ```
  1|Queen|Rock|United Kingdom|1970
  2|The Weeknd|Synth-Pop|Canada|2010
  3|Ed Sheeran|Pop|United Kingdom|2005
  ```
- Foreign Key Relationships:
  - None explicitly, but referenced by `songs.txt` and `albums.txt` via `artist_id`

---

### 3. Albums Data
- Filename & Path: `data/albums.txt`
- Format: Pipe (`|`) delimited text file
- Fields (in order):
  1. `album_id`: int - Unique identifier for the album
  2. `title`: str - Title of the album
  3. `artist_id`: int - Foreign key referencing `artists.txt`'s `artist_id`
  4. `release_year`: int - Year the album was released
  5. `total_songs`: int - Number of songs in the album
  6. `genre`: str - Genre category of the album
- Example Rows:
  ```
  1|A Night at the Opera|1|1975|11|Rock
  2|After Hours|2|2019|14|Synth-Pop
  3|Divide|3|2017|12|Pop
  ```
- Foreign Key Relationships:
  - `artist_id` references `artists.txt` field `artist_id`

---

### 4. Genres Data
- Filename & Path: `data/genres.txt`
- Format: Pipe (`|`) delimited text file
- Fields (in order):
  1. `genre_id`: int - Unique identifier for the genre
  2. `genre_name`: str - Name of the genre (e.g., Rock, Pop, Hip-Hop)
  3. `description`: str - Short description of the genre
- Example Rows:
  ```
  1|Rock|Guitar-driven music with strong beats and vocals
  2|Pop|Catchy mainstream music with broad appeal
  3|Hip-Hop|Rhythmic music with rap vocals and beat production
  ```
- Foreign Key Relationships:
  - None explicit

---

### 5. Playlists Data
- Filename & Path: `data/playlists.txt`
- Format: Pipe (`|`) delimited text file
- Fields (in order):
  1. `playlist_id`: int - Unique identifier for the playlist
  2. `title`: str - Title of the playlist
  3. `description`: str - Description of the playlist
  4. `creation_date`: str - Date the playlist was created (YYYY-MM-DD)
  5. `total_songs`: int - Number of songs in the playlist
- Example Rows:
  ```
  1|Workout Mix|High energy songs for the gym|2025-01-15|25
  2|Chill Vibes|Relaxing music for study|2025-01-16|18
  3|Party Hits|Latest party tracks|2025-01-17|32
  ```
- Foreign Key Relationships:
  - None explicit; referenced by `playlist_songs.txt` via `playlist_id`

---

### 6. Playlist Songs Data
- Filename & Path: `data/playlist_songs.txt`
- Format: Pipe (`|`) delimited text file
- Fields (in order):
  1. `playlist_song_id`: int - Unique identifier for record
  2. `playlist_id`: int - Foreign key referencing `playlists.txt`'s `playlist_id`
  3. `song_id`: int - Foreign key referencing `songs.txt`'s `song_id`
  4. `added_date`: str - Date song was added to playlist (YYYY-MM-DD)
- Example Rows:
  ```
  1|1|2|2025-01-15
  2|1|3|2025-01-15
  3|2|1|2025-01-16
  ```
- Foreign Key Relationships:
  - `playlist_id` references `playlists.txt` field `playlist_id`
  - `song_id` references `songs.txt` field `song_id`

---

<!-- End of design_spec.md -->
