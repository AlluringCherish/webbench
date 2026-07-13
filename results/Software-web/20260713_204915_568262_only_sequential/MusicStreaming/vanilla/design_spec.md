# MusicStreaming Application Detailed Design Specification

## 1. Flask Routes

| Page Name           | Route Path                         | Function Name            | HTTP Methods | Template Filename           | Context Variables (Type)                                             |
|---------------------|----------------------------------|--------------------------|--------------|-----------------------------|----------------------------------------------------------------------|
| Dashboard           | `/`                              | dashboard                | GET          | dashboard.html              | featured_songs (list of dict), trending_artists (list of dict)        |
| Song Catalog        | `/songs`                         | song_catalog             | GET, POST    | song_catalog.html           | songs (list of dict), genres (list of str), selected_genre (str)      |
| Song Details        | `/songs/<int:song_id>`           | song_details             | GET          | song_details.html           | song (dict), artist (dict), album (dict)                             |
| Playlist            | `/playlists`                     | playlists                | GET          | playlists.html              | playlists (list of dict)                                              |
| Playlist Details    | `/playlists/<int:playlist_id>`   | playlist_details         | GET, POST    | playlist_details.html       | playlist (dict), songs_in_playlist (list of dict)                    |
| Create Playlist     | `/playlists/create`              | create_playlist          | GET, POST    | create_playlist.html        | none (on GET), form_data (dict on POST with validation results)       |
| Album Browse        | `/albums`                       | album_browse             | GET          | album_browse.html           | albums (list of dict), sort_option (str), search_query (str)           |
| Album Details       | `/albums/<int:album_id>`          | album_details            | GET          | album_details.html          | album (dict), songs_in_album (list of dict)                          |
| Artist Profiles     | `/artists`                      | artist_profiles          | GET          | artist_profiles.html        | artists (list of dict), sort_option (str), search_query (str)         |
| Artist Details      | `/artists/<int:artist_id>`        | artist_details           | GET          | artist_details.html         | artist (dict), songs_by_artist (list of dict), albums_by_artist (list of dict) |
| Genre Exploration   | `/genres`                      | genre_exploration        | GET          | genre_exploration.html      | genres (list of dict), selected_genre (str), genre_songs (list of dict), genre_artists (list of dict) |


## 2. Page Titles and Element IDs

### 1. Dashboard Page
- Page Title: Music Streaming Dashboard
- Element IDs:
  - `dashboard-page` (Div)
  - `featured-songs` (Div)
  - `browse-songs-button` (Button)
  - `my-playlists-button` (Button)
  - `trending-artists-button` (Button)

### 2. Song Catalog Page
- Page Title: Song Catalog
- Element IDs:
  - `catalog-page` (Div)
  - `search-input` (Input)
  - `genre-filter` (Dropdown)
  - `songs-grid` (Div)
  - `add-to-playlist-button-{song_id}` (Button, per song)

### 3. Song Details Page
- Page Title: Song Details
- Element IDs:
  - `song-details-page` (Div)
  - `song-title` (H1)
  - `artist-name` (Div)
  - `album-name` (Div)
  - `duration-display` (Div)
  - `play-button` (Button)

### 4. Playlist Page
- Page Title: My Playlists
- Element IDs:
  - `playlists-page` (Div)
  - `playlists-grid` (Div)
  - `create-playlist-button` (Button)
  - `view-playlist-button-{playlist_id}` (Button, per playlist)
  - `back-to-dashboard` (Button)

### 5. Playlist Details Page
- Page Title: Playlist Details
- Element IDs:
  - `playlist-details-page` (Div)
  - `playlist-title` (H1)
  - `playlist-description` (Div)
  - `songs-in-playlist` (Table)
  - `remove-song-button-{song_id}` (Button, per song)
  - `delete-playlist-button` (Button)

### 6. Create Playlist Page
- Page Title: Create New Playlist
- Element IDs:
  - `create-playlist-page` (Div)
  - `playlist-name-input` (Input)
  - `playlist-description-input` (Textarea)
  - `save-playlist-button` (Button)
  - `cancel-create-button` (Button)

### 7. Album Browse Page
- Page Title: Albums
- Element IDs:
  - `albums-page` (Div)
  - `albums-grid` (Div)
  - `search-albums` (Input)
  - `sort-albums` (Dropdown)
  - `view-album-button-{album_id}` (Button, per album)

### 8. Album Details Page
- Page Title: Album Details
- Element IDs:
  - `album-details-page` (Div)
  - `album-title` (H1)
  - `album-artist` (Div)
  - `album-year` (Div)
  - `album-songs-list` (Div)
  - `add-album-to-playlist-button` (Button)

### 9. Artist Profile Page
- Page Title: Artist Profiles
- Element IDs:
  - `artists-page` (Div)
  - `artists-grid` (Div)
  - `search-artists` (Input)
  - `artists-sort` (Dropdown)
  - `view-artist-button-{artist_id}` (Button, per artist)

### 10. Genre Exploration Page
- Page Title: Genre Exploration
- Element IDs:
  - `genres-page` (Div)
  - `genres-list` (Div)
  - `select-genre` (Dropdown)
  - `genre-songs` (Div)
  - `genre-artists` (Div)
  - `back-to-dashboard` (Button)


## 3. Navigation Flow

### Starting Page: Dashboard (`/`)
- `browse-songs-button` → `/songs` (Song Catalog Page)
- `my-playlists-button` → `/playlists` (Playlist Page)
- `trending-artists-button` → `/artists` (Artist Profiles Page)

### From Song Catalog Page (`/songs`)
- Selecting/searching/filtering songs updates songs grid
- Each song card has `add-to-playlist-button-{song_id}` to add to playlist
- Selecting a song navigates to `/songs/<song_id>` (Song Details Page)

### From Playlist Page (`/playlists`)
- `create-playlist-button` → `/playlists/create` (Create Playlist Page)
- `view-playlist-button-{playlist_id}` → `/playlists/<playlist_id>` (Playlist Details Page)
- `back-to-dashboard` → `/` (Dashboard Page)

### From Playlist Details Page (`/playlists/<playlist_id>`)
- `remove-song-button-{song_id}` removes that song from playlist
- `delete-playlist-button` deletes entire playlist

### From Create Playlist Page (`/playlists/create`)
- `save-playlist-button` saves and redirects to `/playlists`
- `cancel-create-button` cancels and redirects to `/playlists`

### From Album Browse Page (`/albums`)
- Searching/sorting updates albums grid
- `view-album-button-{album_id}` → `/albums/<album_id>` (Album Details Page)

### From Album Details Page (`/albums/<album_id>`)
- `add-album-to-playlist-button` adds all album songs to playlist

### From Artist Profiles Page (`/artists`)
- Searching and sorting updates `artists-grid`
- `view-artist-button-{artist_id}` → `/artists/<artist_id>` (Artist Details Page)

### From Genre Exploration Page (`/genres`)
- `select-genre` updates displayed genre songs and artists
- `back-to-dashboard` → `/` (Dashboard Page)


## 4. Data Files and Format Contracts

### 1. songs.txt
- Fields (pipe delimited):
  `song_id|title|artist_id|album_id|genre|duration|release_date|play_count`
- Description: Stores all song records with unique IDs, attributes, and play counts.

### 2. artists.txt
- Fields (pipe delimited):
  `artist_id|name|genre|country|formation_year`
- Description: Stores artist information including genre and origin.

### 3. albums.txt
- Fields (pipe delimited):
  `album_id|title|artist_id|release_year|total_songs|genre`
- Description: Stores albums with artist association and metadata.

### 4. genres.txt
- Fields (pipe delimited):
  `genre_id|genre_name|description`
- Description: Stores genre information and descriptions.

### 5. playlists.txt
- Fields (pipe delimited):
  `playlist_id|title|description|creation_date|total_songs`
- Description: Stores user-created playlists.

### 6. playlist_songs.txt
- Fields (pipe delimited):
  `playlist_song_id|playlist_id|song_id|added_date`
- Description: Maps songs to playlists with timestamps.


---

This specification document should be used by backend and frontend teams as a definitive guide to implement the MusicStreaming application, ensuring all endpoints, UI elements, navigation flows, and data storage formats are consistent and complete.