# MusicStreaming Web Application Design Specification - Revised

## Incorporation and Comparison with Peer Design

The following document builds upon the initial version of the design_debate_b.md incorporating and aligning with design_debate_a.md from peer review where it conforms exactly to the user specification. Any conflicts or deviations are resolved by adhering strictly to the original user specifications.

---

## Section 1: Flask Routes and Navigation Flow

| Route Path              | HTTP Methods      | Template                | Context Variables                             |
|-------------------------|-------------------|-------------------------|-----------------------------------------------|
| /                       | GET               | dashboard.html          | featured_songs: list, trending_artists: list |
| /songs                  | GET, POST         | song_catalog.html       | songs: list, genres: list, search_query: str, genre_filter: str |
| /songs/<int:song_id>    | GET               | song_details.html       | song, artist, album                           |
| /playlists              | GET               | playlists.html          | playlists: list                              |
| /playlists/<int:playlist_id> | GET, POST     | playlist_details.html   | playlist, songs                             |
| /playlists/create       | GET, POST         | create_playlist.html    | none or error messages                      |
| /albums                 | GET, POST         | albums.html             | albums: list, search_albums: str, sort_albums: str |
| /albums/<int:album_id>  | GET               | album_details.html      | album, songs                                |
| /artists                | GET, POST         | artists.html            | artists: list, search_artists: str, artists_sort: str |
| /artists/<int:artist_id>| GET               | artist_profile.html     | artist, songs, albums                       |
| /genres                 | GET, POST         | genres.html             | genres: list, selected_genre: str, genre_songs: list, genre_artists: list |


### Navigation Flows

- Dashboard (`/`) buttons:
  - `browse-songs-button` → `/songs`
  - `my-playlists-button` → `/playlists`
  - `trending-artists-button` → `/artists`

- Song Catalog:
  - Add to playlist buttons → POST `/songs` (with `song_id`)
  - Song title/cover → `/songs/<song_id>`

- Playlists:
  - Create Playlist → `/playlists/create`
  - View Playlist → `/playlists/<playlist_id>`
  - Back to Dashboard → `/`

- Playlist Details:
  - Remove song → POST `/playlists/<playlist_id>` (with `song_id`)
  - Delete playlist → POST `/playlists/<playlist_id>`

- Create Playlist:
  - Save playlist → POST `/playlists/create`
  - Cancel → `/playlists`

- Albums:
  - View album → `/albums/<album_id>`

- Album Details:
  - Add album's songs to playlist → POST `/albums/<album_id>` or designated handler

- Artists:
  - View artist → `/artists/<artist_id>`

- Genres:
  - Select genre → POST `/genres`
  - Back to Dashboard → `/`


## Section 2: HTML Elements, IDs, and Forms

### Element IDs and details from user spec and peer consensus summarized

| Page                     | Element ID Pattern                         | Type       | Notes/Form Details                                  |
|--------------------------|------------------------------------------|------------|----------------------------------------------------|
| Dashboard                | `dashboard-page`                          | Div        | Container                                          |
|                          | `featured-songs`                          | Div        |                                                    |
|                          | `browse-songs-button`                     | Button     | Navigates to `/songs`                              |
|                          | `my-playlists-button`                     | Button     | Navigates to `/playlists`                          |
|                          | `trending-artists-button`                 | Button     | Navigates to `/artists`                            |
| Song Catalog             | `catalog-page`                            | Div        | Container                                          |
|                          | `search-input`                            | Input      | name=`search_query`, form POST to `/songs`        |
|                          | `genre-filter`                            | Dropdown   | name=`genre_filter`                                |
|                          | `songs-grid`                             | Div        |                                                    |
|                          | `add-to-playlist-button-{song_id}`       | Button     | POST form field `song_id`                          |
| Song Details             | `song-details-page`                       | Div        | Container                                          |
|                          | `song-title`                             | H1         |                                                    |
|                          | `artist-name`                            | Div        | with link to `/artists/<artist_id>`                |
|                          | `album-name`                             | Div        |                                                    |
|                          | `duration-display`                       | Div        |                                                    |
|                          | `play-button`                           | Button     | client-side action                                 |
| Playlist Page            | `playlists-page`                        | Div        | Container                                          |
|                          | `playlists-grid`                        | Div        |                                                    |
|                          | `create-playlist-button`                 | Button     | navigates `/playlists/create`                      |
|                          | `view-playlist-button-{playlist_id}`     | Button     | navigates to `/playlists/<playlist_id>`           |
|                          | `back-to-dashboard`                      | Button     | navigates `/`                                      |
| Playlist Details         | `playlist-details-page`                  | Div        | Container                                          |
|                          | `playlist-title`                        | H1         |                                                    |
|                          | `playlist-description`                  | Div        |                                                    |
|                          | `songs-in-playlist`                     | Table      |                                                    |
|                          | `remove-song-button-{song_id}`           | Button     | POST form for removing song                         |
|                          | `delete-playlist-button`                 | Button     | POST form to delete playlist                        |
| Create Playlist          | `create-playlist-page`                   | Div        | Container                                          |
|                          | `playlist-name-input`                    | Input      | name=`playlist_name`                               |
|                          | `playlist-description-input`             | Textarea   | name=`playlist_description`                        |
|                          | `save-playlist-button`                    | Button     | form POST `/playlists/create`                      |
|                          | `cancel-create-button`                    | Button     | navigates `/playlists`                             |
| Album Browse             | `albums-page`                            | Div        | Container                                          |
|                          | `albums-grid`                           | Div        |                                                    |
|                          | `search-albums`                        | Input      | name=`search_albums`, form POST                     |
|                          | `sort-albums`                          | Dropdown   | name=`sort_albums`                                 |
|                          | `view-album-button-{album_id}`            | Button     | navigates to `/albums/<album_id>`                  |
| Album Details            | `album-details-page`                    | Div        |                                                    |
|                          | `album-title`                         | H1         |                                                    |
|                          | `album-artist`                        | Div        |                                                    |
|                          | `album-year`                          | Div        |                                                    |
|                          | `album-songs-list`                    | Div        |                                                    |
|                          | `add-album-to-playlist-button`          | Button     | POST form add all songs to playlist                |
| Artist Profile           | `artists-page`                         | Div        | Container                                          |
|                          | `artists-grid`                        | Div        |                                                    |
|                          | `search-artists`                      | Input      | name=`search_artists`, form POST                   |
|                          | `artists-sort`                       | Dropdown   | name=`artists_sort`                                |
|                          | `view-artist-button-{artist_id}`          | Button     | navigates `/artists/<artist_id>`                   |
| Genre Exploration        | `genres-page`                         | Div        | Container                                          |
|                          | `genres-list`                        | Div        |                                                    |
|                          | `select-genre`                      | Dropdown   | name=`selected_genre`, form POST                    |
|                          | `genre-songs`                      | Div        |                                                    |
|                          | `genre-artists`                    | Div        |                                                    |
|                          | `back-to-dashboard`                 | Button     | navigates `/`                                      |


## Section 3: Local Text File Data Schema and Access

All data files are placed in the `data/` directory using pipe `|` delimiter.

### 1. `songs.txt`
- Fields: `song_id|title|artist_id|album_id|genre|duration|release_date|play_count`
- Example: `1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000`
- Usage: For catalog, detail views, playlists, filtering, and searches.

### 2. `artists.txt`
- Fields: `artist_id|name|genre|country|formation_year`
- Example: `1|Queen|Rock|United Kingdom|1970`
- Usage: Artist profiles, linking from songs and albums.

### 3. `albums.txt`
- Fields: `album_id|title|artist_id|release_year|total_songs|genre`
- Example: `1|A Night at the Opera|1|1975|11|Rock`
- Usage: Album browsing, detail pages.

### 4. `genres.txt`
- Fields: `genre_id|genre_name|description`
- Example: `1|Rock|Guitar-driven music with strong beats and vocals`
- Usage: Genre filter, exploration.

### 5. `playlists.txt`
- Fields: `playlist_id|title|description|creation_date|total_songs`
- Example: `1|Workout Mix|High energy songs for the gym|2025-01-15|25`
- Usage: Playlists management and display.

### 6. `playlist_songs.txt`
- Fields: `playlist_song_id|playlist_id|song_id|added_date`
- Example: `1|1|2|2025-01-15`
- Usage: Songs in playlists, additions and removals.

---

# End of Updated Design Specification
