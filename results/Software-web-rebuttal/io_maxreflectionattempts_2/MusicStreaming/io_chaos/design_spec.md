# MusicStreaming Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path               | Function Name           | HTTP Method(s) | Template File             | Context Variables                                                                                                    |
|--------------------------|-------------------------|----------------|---------------------------|---------------------------------------------------------------------------------------------------------------------|
| /                        | root_redirect           | GET            | -                         | - Redirects to `/dashboard`                                                                                         |
| /dashboard               | dashboard_page          | GET            | dashboard.html            | featured_songs: list of dict {song_id: int, title: str, artist_name: str, album_name: str, duration: int}
trending_artists: list of dict {artist_id: int, name: str, genre: str}                                                |
| /songs                   | song_catalog_page       | GET            | song_catalog.html         | songs: list of dict {song_id: int, title: str, artist_name: str, album_name: str, genre: str, duration: int}
genres: list of str (genre names)                                                                                     |
| /songs/search            | song_search             | POST           | song_catalog.html         | songs: filtered list (same structure as `/songs` GET)
genres: list of str                                                                                                |
| /songs/<int:song_id>     | song_details_page       | GET            | song_details.html         | song: dict {
  song_id: int,
  title: str,
  artist_id: int,
  artist_name: str,
  album_id: int,
  album_name: str,
  duration: int,
  genre: str,
  release_date: str (YYYY-MM-DD),
  play_count: int
}                                                                                                               |
| /playlists               | playlists_page          | GET            | playlists.html            | playlists: list of dict {playlist_id: int, title: str, description: str, creation_date: str, total_songs: int}          |
| /playlists/create        | create_playlist_page    | GET            | create_playlist.html      | -                                                                                                                   |
| /playlists/create        | create_playlist_post    | POST           | - (redirect to `/playlists`) | form data: title (str), description (str)                                                                           |
| /playlists/<int:playlist_id> | playlist_details_page | GET            | playlist_details.html     | playlist: dict {playlist_id: int, title: str, description: str, creation_date: str, total_songs: int}
songs_in_playlist: list of dict {song_id: int, title: str, artist_name: str, duration: int}                           |
| /playlists/<int:playlist_id>/remove_song/<int:song_id> | remove_song_from_playlist | POST  | - (redirect to playlist details) | playlist_id: int, song_id: int                                                                                      |
| /playlists/<int:playlist_id>/delete | delete_playlist  | POST           | - (redirect to `/playlists`) | playlist_id: int                                                                                                     |
| /albums                  | albums_page             | GET            | albums.html               | albums: list of dict {album_id: int, title: str, artist_name: str, year: int, genre: str}                              |
| /albums/search           | album_search            | POST           | albums.html               | albums: filtered list (same structure as GET `/albums`)                                                              |
| /albums/<int:album_id>   | album_details_page      | GET            | album_details.html        | album: dict {album_id: int, title: str, artist_id: int, artist_name: str, release_year: int, total_songs: int, genre: str}
songs_in_album: list of dict {song_id: int, title: str, duration: int}                                                  |
| /albums/<int:album_id>/add_to_playlist | add_album_to_playlist  | POST           | - (redirect to playlists or previous) | album_id: int                                                                                                         |
| /artists                 | artists_page            | GET            | artists.html              | artists: list of dict {artist_id: int, name: str, genre: str, country: str, formation_year: int}                        |
| /artists/search          | artist_search           | POST           | artists.html              | artists: filtered list (same structure as GET `/artists`)                                                            |
| /artists/<int:artist_id> | artist_profile_page     | GET            | artist_profile.html       | artist: dict {artist_id: int, name: str, genre: str, country: str, formation_year: int}
songs_by_artist: list of dict {song_id: int, title: str, album_name: str, duration: int}                               |
| /genres                  | genres_page             | GET            | genres.html               | genres: list of dict {genre_id: int, genre_name: str, description: str}
featured_songs: list of dict {song_id: int, title: str, artist_name: str, duration: int}                                     
featured_artists: list of dict {artist_id: int, name: str, genre: str}                                                  |
| /genres/<int:genre_id>   | genre_detail_page       | GET            | genres.html               | genre: dict {genre_id: int, genre_name: str, description: str}
songs_in_genre: list of dict {song_id: int, title: str, artist_name: str, duration: int}
artists_in_genre: list of dict {artist_id: int, name: str, genre: str}                         |

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. dashboard.html
- Template File Path: templates/dashboard.html
- Page Title: 
  - `<title>`: Music Streaming Dashboard
  - `<h1>`: Music Streaming Dashboard
- Required Element IDs:
  - `dashboard-page` (Div)
  - `featured-songs` (Div)
  - `browse-songs-button` (Button)
  - `my-playlists-button` (Button)
  - `trending-artists-button` (Button)
- Context Variables:
  - `featured_songs`: list of dict, each has keys: `song_id` (int), `title` (str), `artist_name` (str), `album_name` (str), `duration` (int - seconds)
  - `trending_artists`: list of dict, each has keys: `artist_id` (int), `name` (str), `genre` (str)
- Navigation Mappings:
  - Button ID `browse-songs-button` → function: `song_catalog_page`
  - Button ID `my-playlists-button` → function: `playlists_page`
  - Button ID `trending-artists-button` → function: `artists_page`

### 2. song_catalog.html
- Template File Path: templates/song_catalog.html
- Page Title:
  - `<title>`: Song Catalog
  - `<h1>`: Song Catalog
- Required Element IDs:
  - `catalog-page` (Div)
  - `search-input` (Input)
  - `genre-filter` (Dropdown)
  - `songs-grid` (Div)
  - `add-to-playlist-button-{{ song.song_id }}` (Button) - dynamic per song
- Context Variables:
  - `songs`: list of dict each containing `song_id` (int), `title` (str), `artist_name` (str), `album_name` (str), `genre` (str), `duration` (int)
  - `genres`: list of str for dropdown options
- Navigation Mappings:
  - No direct navigation buttons but `add-to-playlist-button-{{ song.song_id }}` triggers action to add song to playlist

### 3. song_details.html
- Template File Path: templates/song_details.html
- Page Title:
  - `<title>`: Song Details
  - `<h1>` (with id `song-title`): Song title text
- Required Element IDs:
  - `song-details-page` (Div)
  - `song-title` (H1)
  - `artist-name` (Div) with link (no id specified) to artist profile
  - `album-name` (Div)
  - `duration-display` (Div)
  - `play-button` (Button)
- Context Variables:
  - `song`: dict with keys: `song_id` (int), `title` (str), `artist_id` (int), `artist_name` (str), `album_id` (int), `album_name` (str), `duration` (int), `genre` (str), `release_date` (str), `play_count` (int)
- Navigation Mappings:
  - Clicking `artist-name` links to `artist_profile_page` with parameter `artist_id`
  - `play-button` triggers playback action

### 4. playlists.html
- Template File Path: templates/playlists.html
- Page Title:
  - `<title>`: My Playlists
  - `<h1>`: My Playlists
- Required Element IDs:
  - `playlists-page` (Div)
  - `playlists-grid` (Div)
  - `create-playlist-button` (Button)
  - `view-playlist-button-{{ playlist.playlist_id }}` (Button) - dynamic per playlist
  - `back-to-dashboard` (Button)
- Context Variables:
  - `playlists`: list of dict with keys: `playlist_id` (int), `title` (str), `description` (str), `creation_date` (str), `total_songs` (int)
- Navigation Mappings:
  - `create-playlist-button` → function: `create_playlist_page`
  - `view-playlist-button-{{ playlist.playlist_id }}` → function: `playlist_details_page` with param `playlist_id`
  - `back-to-dashboard` → function: `dashboard_page`

### 5. playlist_details.html
- Template File Path: templates/playlist_details.html
- Page Title:
  - `<title>`: Playlist Details
  - `<h1 id="playlist-title">`: Playlist title text
- Required Element IDs:
  - `playlist-details-page` (Div)
  - `playlist-title` (H1)
  - `playlist-description` (Div)
  - `songs-in-playlist` (Table)
  - `remove-song-button-{{ song.song_id }}` (Button) - dynamic per song
  - `delete-playlist-button` (Button)
- Context Variables:
  - `playlist`: dict with keys: `playlist_id` (int), `title` (str), `description` (str), `creation_date` (str), `total_songs` (int)
  - `songs_in_playlist`: list of dict with keys: `song_id` (int), `title` (str), `artist_name` (str), `duration` (int)
- Navigation Mappings:
  - `remove-song-button-{{ song.song_id }}`: triggers removal action
  - `delete-playlist-button`: triggers playlist deletion

### 6. create_playlist.html
- Template File Path: templates/create_playlist.html
- Page Title:
  - `<title>`: Create New Playlist
  - `<h1>`: Create New Playlist
- Required Element IDs:
  - `create-playlist-page` (Div)
  - `playlist-name-input` (Input)
  - `playlist-description-input` (Textarea)
  - `save-playlist-button` (Button)
  - `cancel-create-button` (Button)
- Context Variables:
  - None (page is a form)
- Navigation Mappings:
  - `save-playlist-button`: submits form POST to create playlist
  - `cancel-create-button`: navigates back (likely to playlists_page)

### 7. albums.html
- Template File Path: templates/albums.html
- Page Title:
  - `<title>`: Albums
  - `<h1>`: Albums
- Required Element IDs:
  - `albums-page` (Div)
  - `albums-grid` (Div)
  - `search-albums` (Input)
  - `sort-albums` (Dropdown)
  - `view-album-button-{{ album.album_id }}` (Button) - dynamic per album
- Context Variables:
  - `albums`: list of dict with keys: `album_id` (int), `title` (str), `artist_name` (str), `year` (int), `genre` (str)
- Navigation Mappings:
  - `view-album-button-{{ album.album_id }}` → function: `album_details_page` with param `album_id`

### 8. album_details.html
- Template File Path: templates/album_details.html
- Page Title:
  - `<title>`: Album Details
  - `<h1 id="album-title">`: album title text
- Required Element IDs:
  - `album-details-page` (Div)
  - `album-title` (H1)
  - `album-artist` (Div)
  - `album-year` (Div)
  - `album-songs-list` (Div)
  - `add-album-to-playlist-button` (Button)
- Context Variables:
  - `album`: dict with keys: `album_id` (int), `title` (str), `artist_id` (int), `artist_name` (str), `release_year` (int), `total_songs` (int), `genre` (str)
  - `songs_in_album`: list of dict with keys: `song_id` (int), `title` (str), `duration` (int)
- Navigation Mappings:
  - `add-album-to-playlist-button`: triggers POST to add album songs to playlist

### 9. artists.html
- Template File Path: templates/artists.html
- Page Title:
  - `<title>`: Artist Profiles
  - `<h1>`: Artist Profiles
- Required Element IDs:
  - `artists-page` (Div)
  - `artists-grid` (Div)
  - `search-artists` (Input)
  - `artists-sort` (Dropdown)
  - `view-artist-button-{{ artist.artist_id }}` (Button) - dynamic per artist
- Context Variables:
  - `artists`: list of dict with keys: `artist_id` (int), `name` (str), `genre` (str), `country` (str), `formation_year` (int)
- Navigation Mappings:
  - `view-artist-button-{{ artist.artist_id }}` → function: `artist_profile_page` with param `artist_id`

### 10. genres.html
- Template File Path: templates/genres.html
- Page Title:
  - `<title>`: Genre Exploration
  - `<h1>`: Genre Exploration
- Required Element IDs:
  - `genres-page` (Div)
  - `genres-list` (Div)
  - `select-genre` (Dropdown)
  - `genre-songs` (Div)
  - `genre-artists` (Div)
  - `back-to-dashboard` (Button)
- Context Variables:
  - `genres`: list of dict with keys: `genre_id` (int), `genre_name` (str), `description` (str)
  - `featured_songs`: list of dict with keys: `song_id` (int), `title` (str), `artist_name` (str), `duration` (int)
  - `featured_artists`: list of dict with keys: `artist_id` (int), `name` (str), `genre` (str)
- Navigation Mappings:
  - `back-to-dashboard`: function: `dashboard_page`
  - Selecting from `select-genre` dropdown loads data for that genre (routes handled by `/genres/<int:genre_id>`)

---

## Section 3: Data File Schemas (For Backend Developer)

1. **songs.txt** (data/songs.txt)
- Format: pipe-delimited (`|`)
- Fields:
  1. `song_id` (int): Unique numerical ID for the song
  2. `title` (str): Title of the song
  3. `artist_id` (int): Foreign key referencing `artists.txt` `artist_id`
  4. `album_id` (int): Foreign key referencing `albums.txt` `album_id`
  5. `genre` (str): Genre name of the song
  6. `duration` (int): Duration in seconds
  7. `release_date` (str): Release date in YYYY-MM-DD format
  8. `play_count` (int): Number of times the song has been played
- Example rows:
```
1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
3|Shape of You|3|3|Pop|233|2017-01-06|4200000
```

2. **artists.txt** (data/artists.txt)
- Format: pipe-delimited (`|`)
- Fields:
  1. `artist_id` (int): Unique numerical ID for the artist
  2. `name` (str): Name of the artist
  3. `genre` (str): Main genre associated with artist
  4. `country` (str): Country of origin
  5. `formation_year` (int): Year artist or band was formed
- Example rows:
```
1|Queen|Rock|United Kingdom|1970
2|The Weeknd|Synth-Pop|Canada|2010
3|Ed Sheeran|Pop|United Kingdom|2005
```

3. **albums.txt** (data/albums.txt)
- Format: pipe-delimited (`|`)
- Fields:
  1. `album_id` (int): Unique numerical ID for the album
  2. `title` (str): Album title
  3. `artist_id` (int): Foreign key referencing `artists.txt` `artist_id`
  4. `release_year` (int): Year album released
  5. `total_songs` (int): Number of songs in the album
  6. `genre` (str): Genre of the album
- Example rows:
```
1|A Night at the Opera|1|1975|11|Rock
2|After Hours|2|2019|14|Synth-Pop
3|Divide|3|2017|12|Pop
```

4. **genres.txt** (data/genres.txt)
- Format: pipe-delimited (`|`)
- Fields:
  1. `genre_id` (int): Unique numerical ID for the genre
  2. `genre_name` (str): Name of the genre
  3. `description` (str): Description of genre characteristics
- Example rows:
```
1|Rock|Guitar-driven music with strong beats and vocals
2|Pop|Catchy mainstream music with broad appeal
3|Hip-Hop|Rhythmic music with rap vocals and beat production
```

5. **playlists.txt** (data/playlists.txt)
- Format: pipe-delimited (`|`)
- Fields:
  1. `playlist_id` (int): Unique numerical ID for the playlist
  2. `title` (str): Title of the playlist
  3. `description` (str): Playlist description
  4. `creation_date` (str): Date playlist was created (YYYY-MM-DD)
  5. `total_songs` (int): Number of songs in playlist
- Example rows:
```
1|Workout Mix|High energy songs for the gym|2025-01-15|25
2|Chill Vibes|Relaxing music for study|2025-01-16|18
3|Party Hits|Latest party tracks|2025-01-17|32
```

6. **playlist_songs.txt** (data/playlist_songs.txt)
- Format: pipe-delimited (`|`)
- Fields:
  1. `playlist_song_id` (int): Unique ID for the playlist-song entry
  2. `playlist_id` (int): Foreign key referencing `playlists.txt` `playlist_id`
  3. `song_id` (int): Foreign key referencing `songs.txt` `song_id`
  4. `added_date` (str): Date the song was added to playlist (YYYY-MM-DD)
- Example rows:
```
1|1|2|2025-01-15
2|1|3|2025-01-15
3|2|1|2025-01-16
```

---

### Notes:
- All date strings use `YYYY-MM-DD` format.
- Foreign key relationships:
  - `songs.artist_id` → `artists.artist_id`
  - `songs.album_id` → `albums.album_id`
  - `albums.artist_id` → `artists.artist_id`
  - `playlist_songs.playlist_id` → `playlists.playlist_id`
  - `playlist_songs.song_id` → `songs.song_id`
- UI element ID dynamic patterns use Jinja2 expressions, e.g. `add-to-playlist-button-{{ song.song_id }}`

---

This specification document enables independent development of backend Flask routes and frontend HTML templates, and ensures backend data handling conforms to data schema expectations. No internal implementation details are included as per instructions.