# MusicStreaming Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path               | Function Name           | HTTP Method(s) | Template File             | Context Variables                                                                                                    |
|--------------------------|-------------------------|----------------|---------------------------|---------------------------------------------------------------------------------------------------------------------|
| /                        | root_redirect           | GET            | -                         | - Redirects to `/dashboard`                                                                                         |
| /dashboard               | dashboard_page          | GET            | dashboard.html            | featured_songs: list of dict {song_id: int, title: str, artist_name: str, album_name: str, duration: int}
trending_artists: list of dict {artist_id: int, name: str, genre: str} |
| /songs                   | song_catalog_page       | GET            | song_catalog.html         | songs: list of dict {song_id: int, title: str, artist_name: str, album_name: str, genre: str, duration: int}
genres: list of str (genre names for dropdown) |
| /songs/search            | song_catalog_search     | POST           | song_catalog.html         | songs: filtered list (same structure as `/songs` GET)
genres: list of str | 
| /songs/<int:song_id>     | song_details_page       | GET            | song_details.html         | song: dict {song_id: int, title: str, artist_id: int, artist_name: str, album_id: int, album_name: str, duration: int, genre: str, release_date: str}
 |
| /playlists               | playlists_page          | GET            | playlists.html            | playlists: list of dict {playlist_id: int, title: str, description: str, creation_date: str, total_songs: int}         |
| /playlists/create        | create_playlist_page    | GET            | create_playlist.html      | -                                                                                                                   |
| /playlists/create        | create_playlist_submit  | POST           | - (redirect after creation)| Form fields: title (str), description (str)                                                                           |
| /playlists/<int:playlist_id> | playlist_details_page  | GET            | playlist_details.html      | playlist: dict {playlist_id: int, title: str, description: str, creation_date: str, total_songs: int}
songs_in_playlist: list of dict {song_id: int, title: str, artist_name: str, duration: int} |
| /playlists/<int:playlist_id>/delete | delete_playlist | POST           | - (redirect after deletion) | playlist_id: int                                                                                                |
| /playlists/<int:playlist_id>/remove_song/<int:song_id> | remove_song_from_playlist | POST | - (redirect after removal) | playlist_id: int, song_id: int                                                                                       |
| /albums                  | albums_page             | GET            | albums.html               | albums: list of dict {album_id: int, title: str, artist_name: str, release_year: int, genre: str}                     |
| /albums/search           | albums_search           | POST           | albums.html               | albums: filtered list (same structure as `/albums` GET)                                                             |
| /albums/<int:album_id>   | album_details_page      | GET            | album_details.html        | album: dict {album_id: int, title: str, artist_id: int, artist_name: str, release_year: int, total_songs: int, genre: str}
songs_in_album: list of dict {song_id: int, title: str, duration: int} |
| /albums/<int:album_id>/add_all_to_playlist | add_album_to_playlist | POST | - (redirect after action) | album_id: int, playlist_id: int                                                                                      |
| /artists                 | artists_page            | GET            | artists.html              | artists: list of dict {artist_id: int, name: str, genre: str, country: str, formation_year: int}                       |
| /artists/search          | artists_search          | POST           | artists.html              | artists: filtered list (same structure as `/artists` GET)                                                           |
| /artists/<int:artist_id> | artist_profile_page     | GET            | artist_profile.html       | artist: dict {artist_id: int, name: str, genre: str, country: str, formation_year: int}
songs_by_artist: list of dict {song_id: int, title: str, album_name: str, duration: int} |
| /genres                  | genre_exploration_page  | GET            | genres.html               | genres: list of dict {genre_id: int, genre_name: str, description: str}
selected_genre_songs: list of dict {song_id: int, title: str, artist_name: str, duration: int} (optional)
selected_genre_artists: list of dict {artist_id: int, name: str, genre: str} (optional)
selected_genre: str (genre name, optional) |
| /genres/select           | genre_select            | POST           | genres.html               | Same as GET `/genres` plus selected_genre: str                                                                        |

---

## Section 2: HTML Template Specifications (For Frontend Developer)

---

### Template: dashboard.html
- Template File Path: templates/dashboard.html
- Page Title: "Music Streaming Dashboard"
- `<title>` Content: "Music Streaming Dashboard"
- `<h1>` Content: "Music Streaming Dashboard"
- Required Element IDs and Types:
  - `dashboard-page` (Div)
  - `featured-songs` (Div)
  - `browse-songs-button` (Button)
  - `my-playlists-button` (Button)
  - `trending-artists-button` (Button)
- Context Variables:
  - `featured_songs`: List of dicts with keys: `song_id`(int), `title`(str), `artist_name`(str), `album_name`(str), `duration`(int seconds)
  - `trending_artists`: List of dicts with keys: `artist_id`(int), `name`(str), `genre`(str)
- Navigation Mappings:
  - `browse-songs-button` → `song_catalog_page`
  - `my-playlists-button` → `playlists_page`
  - `trending-artists-button` → `artists_page`

---

### Template: song_catalog.html
- Template File Path: templates/song_catalog.html
- Page Title: "Song Catalog"
- `<title>` Content: "Song Catalog"
- `<h1>` Content: "Song Catalog"
- Required Element IDs and Types:
  - `catalog-page` (Div)
  - `search-input` (Input)
  - `genre-filter` (Dropdown)
  - `songs-grid` (Div)
  - `add-to-playlist-button-{{ song.song_id }}` (Button) — dynamic, one per song card
- Context Variables:
  - `songs`: List of dicts, each with keys: `song_id`(int), `title`(str), `artist_name`(str), `album_name`(str), `genre`(str), `duration`(int)
  - `genres`: List of strings representing genre names for filter dropdown
- Navigation Mappings:
  - Button IDs follow pattern `add-to-playlist-button-<song_id>` → likely calls an action route to add that song

---

### Template: song_details.html
- Template File Path: templates/song_details.html
- Page Title: "Song Details"
- `<title>` Content: "Song Details"
- `<h1>` Content: (dynamic) `song.title` rendered in element with id `song-title`
- Required Element IDs and Types:
  - `song-details-page` (Div)
  - `song-title` (H1)
  - `artist-name` (Div) — includes a link to artist profile
  - `album-name` (Div)
  - `duration-display` (Div)
  - `play-button` (Button)
- Context Variables:
  - `song`: Dict with fields: `song_id`(int), `title`(str), `artist_id`(int), `artist_name`(str), `album_id`(int), `album_name`(str), `duration`(int), `genre`(str), `release_date`(str)
- Navigation Mappings:
  - `artist-name` link → `artist_profile_page` with `artist_id`
  - `play-button` triggers play action (likely JS, no route)

---

### Template: playlists.html
- Template File Path: templates/playlists.html
- Page Title: "My Playlists"
- `<title>` Content: "My Playlists"
- `<h1>` Content: "My Playlists"
- Required Element IDs and Types:
  - `playlists-page` (Div)
  - `playlists-grid` (Div)
  - `create-playlist-button` (Button)
  - `back-to-dashboard` (Button)
  - `view-playlist-button-{{ playlist.playlist_id }}` (Button) — dynamic per playlist
- Context Variables:
  - `playlists`: List of dicts with keys: `playlist_id`(int), `title`(str), `description`(str), `creation_date`(str), `total_songs`(int)
- Navigation Mappings:
  - `create-playlist-button` → `create_playlist_page`
  - `back-to-dashboard` → `dashboard_page`
  - Buttons with pattern `view-playlist-button-<playlist_id>` → `playlist_details_page` with `playlist_id`

---

### Template: playlist_details.html
- Template File Path: templates/playlist_details.html
- Page Title: "Playlist Details"
- `<title>` Content: "Playlist Details"
- `<h1>` Content: (dynamic) `playlist.title` rendered in element with id `playlist-title`
- Required Element IDs and Types:
  - `playlist-details-page` (Div)
  - `playlist-title` (H1)
  - `playlist-description` (Div)
  - `songs-in-playlist` (Table)
  - `remove-song-button-{{ song.song_id }}` (Button) — dynamic per song in playlist
  - `delete-playlist-button` (Button)
- Context Variables:
  - `playlist`: Dict with fields `playlist_id`(int), `title`(str), `description`(str), `creation_date`(str), `total_songs`(int)
  - `songs_in_playlist`: List of dicts, each with keys `song_id`(int), `title`(str), `artist_name`(str), `duration`(int)
- Navigation Mappings:
  - `delete-playlist-button` triggers route to delete playlist
  - Buttons with pattern `remove-song-button-<song_id>` trigger remove that song from playlist

---

### Template: create_playlist.html
- Template File Path: templates/create_playlist.html
- Page Title: "Create New Playlist"
- `<title>` Content: "Create New Playlist"
- `<h1>` Content: "Create New Playlist"
- Required Element IDs and Types:
  - `create-playlist-page` (Div)
  - `playlist-name-input` (Input)
  - `playlist-description-input` (Textarea)
  - `save-playlist-button` (Button)
  - `cancel-create-button` (Button)
- Context Variables: None (page for creating, no dynamic data needed)
- Navigation Mappings:
  - `cancel-create-button` → return to `playlists_page`

---

### Template: albums.html
- Template File Path: templates/albums.html
- Page Title: "Albums"
- `<title>` Content: "Albums"
- `<h1>` Content: "Albums"
- Required Element IDs and Types:
  - `albums-page` (Div)
  - `albums-grid` (Div)
  - `search-albums` (Input)
  - `sort-albums` (Dropdown)
  - `view-album-button-{{ album.album_id }}` (Button) — dynamic per album
- Context Variables:
  - `albums`: List of dicts with keys: `album_id`(int), `title`(str), `artist_name`(str), `release_year`(int), `genre`(str)
- Navigation Mappings:
  - Buttons with pattern `view-album-button-<album_id>` → `album_details_page` with `album_id`

---

### Template: album_details.html
- Template File Path: templates/album_details.html
- Page Title: "Album Details"
- `<title>` Content: "Album Details"
- `<h1>` Content: (dynamic) `album.title` in element with id `album-title`
- Required Element IDs and Types:
  - `album-details-page` (Div)
  - `album-title` (H1)
  - `album-artist` (Div)
  - `album-year` (Div)
  - `album-songs-list` (Div)
  - `add-album-to-playlist-button` (Button)
- Context Variables:
  - `album`: Dict with fields `album_id`(int), `title`(str), `artist_id`(int), `artist_name`(str), `release_year`(int), `total_songs`(int), `genre`(str)
  - `songs_in_album`: List of dicts with keys `song_id`(int), `title`(str), `duration`(int)
- Navigation Mappings:
  - `add-album-to-playlist-button` triggers POST to add all album songs to a playlist

---

### Template: artists.html
- Template File Path: templates/artists.html
- Page Title: "Artist Profiles"
- `<title>` Content: "Artist Profiles"
- `<h1>` Content: "Artist Profiles"
- Required Element IDs and Types:
  - `artists-page` (Div)
  - `artists-grid` (Div)
  - `search-artists` (Input)
  - `artists-sort` (Dropdown)
  - `view-artist-button-{{ artist.artist_id }}` (Button) — dynamic per artist
- Context Variables:
  - `artists`: List of dicts with keys: `artist_id`(int), `name`(str), `genre`(str), `country`(str), `formation_year`(int)
- Navigation Mappings:
  - Buttons with pattern `view-artist-button-<artist_id>` → `artist_profile_page` with `artist_id`

---

### Template: genres.html
- Template File Path: templates/genres.html
- Page Title: "Genre Exploration"
- `<title>` Content: "Genre Exploration"
- `<h1>` Content: "Genre Exploration"
- Required Element IDs and Types:
  - `genres-page` (Div)
  - `genres-list` (Div)
  - `select-genre` (Dropdown)
  - `genre-songs` (Div)
  - `genre-artists` (Div)
  - `back-to-dashboard` (Button)
- Context Variables:
  - `genres`: List of dicts with keys: `genre_id`(int), `genre_name`(str), `description`(str)
  - `selected_genre`: str (optional)
  - `selected_genre_songs`: List of dicts {song_id: int, title: str, artist_name: str, duration: int} (optional)
  - `selected_genre_artists`: List of dicts {artist_id: int, name: str, genre: str} (optional)
- Navigation Mappings:
  - `back-to-dashboard` → `dashboard_page`

---

## Section 3: Data File Schemas (For Backend Developer)

---

### 1. Songs Data
- Filename and Path: `data/songs.txt`
- File Format: Pipe-delimited `|`
- Fields (in order):
  1. `song_id` (int): Unique song identifier
  2. `title` (str): Title of the song
  3. `artist_id` (int): Reference to artist (foreign key from artists.txt)
  4. `album_id` (int): Reference to album (foreign key from albums.txt)
  5. `genre` (str): Genre name
  6. `duration` (int): Duration of song in seconds
  7. `release_date` (str): Release date in YYYY-MM-DD
  8. `play_count` (int): Number of times song has been played
- Example Rows:
```
1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
3|Shape of You|3|3|Pop|233|2017-01-06|4200000
```

---

### 2. Artists Data
- Filename and Path: `data/artists.txt`
- File Format: Pipe-delimited `|`
- Fields (in order):
  1. `artist_id` (int): Unique artist identifier
  2. `name` (str): Artist name
  3. `genre` (str): Primary genre
  4. `country` (str): Country of origin
  5. `formation_year` (int): Year artist/group was formed
- Example Rows:
```
1|Queen|Rock|United Kingdom|1970
2|The Weeknd|Synth-Pop|Canada|2010
3|Ed Sheeran|Pop|United Kingdom|2005
```

---

### 3. Albums Data
- Filename and Path: `data/albums.txt`
- File Format: Pipe-delimited `|`
- Fields (in order):
  1. `album_id` (int): Unique album identifier
  2. `title` (str): Album title
  3. `artist_id` (int): Reference to artist (foreign key from artists.txt)
  4. `release_year` (int): Year album was released
  5. `total_songs` (int): Number of songs in album
  6. `genre` (str): Genre of album
- Example Rows:
```
1|A Night at the Opera|1|1975|11|Rock
2|After Hours|2|2019|14|Synth-Pop
3|Divide|3|2017|12|Pop
```

---

### 4. Genres Data
- Filename and Path: `data/genres.txt`
- File Format: Pipe-delimited `|`
- Fields (in order):
  1. `genre_id` (int): Unique genre identifier
  2. `genre_name` (str): Genre name
  3. `description` (str): Short description
- Example Rows:
```
1|Rock|Guitar-driven music with strong beats and vocals
2|Pop|Catchy mainstream music with broad appeal
3|Hip-Hop|Rhythmic music with rap vocals and beat production
```

---

### 5. Playlists Data
- Filename and Path: `data/playlists.txt`
- File Format: Pipe-delimited `|`
- Fields (in order):
  1. `playlist_id` (int): Unique playlist identifier
  2. `title` (str): Playlist title
  3. `description` (str): Playlist description
  4. `creation_date` (str): Creation date in YYYY-MM-DD
  5. `total_songs` (int): Number of songs in playlist
- Example Rows:
```
1|Workout Mix|High energy songs for the gym|2025-01-15|25
2|Chill Vibes|Relaxing music for study|2025-01-16|18
3|Party Hits|Latest party tracks|2025-01-17|32
```

---

### 6. Playlist Songs Data
- Filename and Path: `data/playlist_songs.txt`
- File Format: Pipe-delimited `|`
- Fields (in order):
  1. `playlist_song_id` (int): Unique identifier for entry
  2. `playlist_id` (int): Reference to playlist (foreign key from playlists.txt)
  3. `song_id` (int): Reference to song (foreign key from songs.txt)
  4. `added_date` (str): Date song was added in YYYY-MM-DD
- Example Rows:
```
1|1|2|2025-01-15
2|1|3|2025-01-15
3|2|1|2025-01-16
```

---

# End of design_spec.md
