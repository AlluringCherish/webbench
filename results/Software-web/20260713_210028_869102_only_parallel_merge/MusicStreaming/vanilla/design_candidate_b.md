# MusicStreaming Application - Design Specification (Alternative)

---

## 1. URL Routing and Navigation

### Routes Overview

| Route                    | HTTP Method | Purpose / Page                         |
|--------------------------|-------------|--------------------------------------|
| `/`                      | GET         | Dashboard Page                       |
| `/songs`                 | GET         | Song Catalog Page                    |
| `/songs/<int:song_id>`   | GET         | Song Details Page                    |
| `/playlists`             | GET         | My Playlists Page                    |
| `/playlists/create`      | GET, POST   | Create Playlist Page (GET: form, POST: save) |
| `/playlists/<int:playlist_id>` | GET    | Playlist Details Page                |
| `/playlists/<int:playlist_id>/delete` | POST| Delete playlist action            |
| `/playlists/<int:playlist_id>/remove_song/<int:song_id>` | POST | Remove song from playlist        |
| `/albums`                | GET         | Album Browse Page                   |
| `/albums/<int:album_id>` | GET         | Album Details Page                  |
| `/artists`               | GET         | Artist Profile Page                 |
| `/artists/<int:artist_id>` | GET       | Specific Artist Profile Page       |
| `/genres`                | GET         | Genre Exploration Page             |

### Navigation Button Mappings

- On Dashboard (`/`):
  - Button `browse-songs-button` -> `/songs`
  - Button `my-playlists-button` -> `/playlists`
  - Button `trending-artists-button` -> `/artists`

- On Song Catalog (`/songs`):
  - Add to playlist buttons: `add-to-playlist-button-{song_id}` trigger modal or redirect to playlist selection
  - Clicking song title or artist redirects to `/songs/<song_id>` or `/artists/<artist_id>` respectively

- On Playlists (`/playlists`):
  - Create new playlist: Button `create-playlist-button` -> `/playlists/create`
  - View playlist details: Button `view-playlist-button-{playlist_id}` -> `/playlists/<playlist_id>`
  - Back to dashboard: Button `back-to-dashboard` -> `/`

- On Playlist Details (`/playlists/<playlist_id>`):
  - Remove song: Button `remove-song-button-{song_id}` posts to `/playlists/<playlist_id>/remove_song/<song_id>`
  - Delete playlist: Button `delete-playlist-button` posts to `/playlists/<playlist_id>/delete`

- On Create Playlist (`/playlists/create`):
  - Save: Button `save-playlist-button` posts to same route
  - Cancel: Button `cancel-create-button` redirects to `/playlists`

- On Albums (`/albums`):
  - View album details: Button `view-album-button-{album_id}` -> `/albums/<album_id>`

- On Album Details (`/albums/<album_id>`):
  - Add all songs to playlist: Button `add-album-to-playlist-button` triggers playlist song addition modal or action

- On Artists (`/artists`):
  - View artist profile: Button `view-artist-button-{artist_id}` -> `/artists/<artist_id>`

- On Genre Exploration (`/genres`):
  - Select genre: Dropdown `select-genre` triggers update of `genre-songs` and `genre-artists`
  - Back to dashboard: Button `back-to-dashboard` -> `/`

---

## 2. UI Components and Stable Element IDs

### 1. Dashboard Page
- **URL**: `/`
- **Title**: "Music Streaming Dashboard"
- **Elements:**
  - `dashboard-page`: Div container wrapping entire dashboard
  - `featured-songs`: Div showing highlighted/recommended songs
  - `browse-songs-button`: Button navigating to `/songs`
  - `my-playlists-button`: Button navigating to `/playlists`
  - `trending-artists-button`: Button navigating to `/artists`

### 2. Song Catalog Page
- **URL**: `/songs`
- **Title**: "Song Catalog"
- **Elements:**
  - `catalog-page`: Main container div
  - `search-input`: Text input for search queries (search by title, artist, album)
  - `genre-filter`: Dropdown to filter by genre (populated dynamically from genres data file)
  - `songs-grid`: Div grid containing song cards
  - `add-to-playlist-button-{song_id}`: For each song card; triggers addition to playlist

### 3. Song Details Page
- **URL**: `/songs/<int:song_id>`
- **Title**: "Song Details"
- **Elements:**
  - `song-details-page`: Container div
  - `song-title`: H1 element showing song title
  - `artist-name`: Div with artist name, clickable to `/artists/<artist_id>`
  - `album-name`: Div showing album name
  - `duration-display`: Div showing song duration in mm:ss
  - `play-button`: Button to play song

### 4. Playlist Page
- **URL**: `/playlists`
- **Title**: "My Playlists"
- **Elements:**
  - `playlists-page`: Container div
  - `playlists-grid`: Div grid listing playlist cards
  - `create-playlist-button`: Button navigates to `/playlists/create`
  - `view-playlist-button-{playlist_id}`: Button on each playlist card views playlist details
  - `back-to-dashboard`: Button navigates back to `/`

### 5. Playlist Details Page
- **URL**: `/playlists/<int:playlist_id>`
- **Title**: "Playlist Details"
- **Elements:**
  - `playlist-details-page`: Container div
  - `playlist-title`: H1 playlist name
  - `playlist-description`: Div showing playlist description
  - `songs-in-playlist`: Table displaying songs with columns (Title, Artist, Duration, Remove)
  - `remove-song-button-{song_id}`: Button for each song to remove it from playlist
  - `delete-playlist-button`: Button to delete entire playlist

### 6. Create Playlist Page
- **URL**: `/playlists/create`
- **Title**: "Create New Playlist"
- **Elements:**
  - `create-playlist-page`: Container div
  - `playlist-name-input`: Input field for playlist title
  - `playlist-description-input`: Textarea for description
  - `save-playlist-button`: Button to submit form
  - `cancel-create-button`: Button to cancel (navigate back to `/playlists`)

### 7. Album Browse Page
- **URL**: `/albums`
- **Title**: "Albums"
- **Elements:**
  - `albums-page`: Container div
  - `albums-grid`: Div grid showing album cards
  - `search-albums`: Input field for searching albums by title or artist
  - `sort-albums`: Dropdown with sorting options: "By Title", "By Artist", "By Year"
  - `view-album-button-{album_id}`: Button viewing album details

### 8. Album Details Page
- **URL**: `/albums/<int:album_id>`
- **Title**: "Album Details"
- **Elements:**
  - `album-details-page`: Container div
  - `album-title`: H1 displaying album title
  - `album-artist`: Div showing album artist
  - `album-year`: Div showing release year
  - `album-songs-list`: Div listing songs in album, with add-to-playlist buttons
  - `add-album-to-playlist-button`: Button to add all album songs to playlist

### 9. Artist Profile Page
- **URL**: `/artists`
- **Title**: "Artist Profiles"
- **Elements:**
  - `artists-page`: Container div
  - `artists-grid`: Div grid displaying artist cards
  - `search-artists`: Input to search artists by name
  - `artists-sort`: Dropdown to sort artists "By Name", "By Genre"
  - `view-artist-button-{artist_id}`: Button for each artist to view profile

### 10. Genre Exploration Page
- **URL**: `/genres`
- **Title**: "Genre Exploration"
- **Elements:**
  - `genres-page`: Container div
  - `genres-list`: Div listing all genre names (clickable or info)
  - `select-genre`: Dropdown to select genre, triggers filtering
  - `genre-songs`: Div showing songs for selected genre
  - `genre-artists`: Div showing artists for selected genre
  - `back-to-dashboard`: Button to return `/`

---

## 3. Data Interaction and File Handling

### File Locations
- All data files stored under folder: `data/`

### Data Files and Usage

1. **songs.txt**
   - Loaded fully or filtered by genre (song catalog, genre exploration)
   - Fields parsed as: song_id, title, artist_id, album_id, genre, duration, release_date, play_count

2. **artists.txt**
   - Used to populate artist names, genres, and details
   - Supports searching by name and sorting by name or genre

3. **albums.txt**
   - Provides album details for browse and album detail pages
   - Supports search by title or artist and sorting (title, artist, year)

4. **genres.txt**
   - Populates genre dropdowns and lists
   - Each genre has description shown in genre exploration or tooltips

5. **playlists.txt**
   - Playlist metadata loaded to display all playlists
   - Includes playlist_id, title, description, creation_date, total_songs

6. **playlist_songs.txt**
   - Files link songs to playlists
   - Used to fetch songs for playlist details page

### Filtering and Sorting

- **Song Catalog Page:**
  - Filtering by `genre-filter` dropdown triggers filtering displayed songs client-side or server-side
  - Search input `search-input` filters songs by matching title, artist name, or album name

- **Album Browse Page:**
  - Search by album title or artist uses `search-albums` input
  - Sorting dropdown `sort-albums` allows sorting albums alphabetically by title, artist, or numerically by year

- **Artist Profile Page:**
  - Search by artist name uses `search-artists` input
  - Sorting uses `artists-sort` dropdown with options for name and genre

- **Genre Exploration Page:**
  - Genre selected via `select-genre` dropdown filters `genre-songs` and `genre-artists` dynamically

### Updating Data
- Creating playlists and adding/removing songs writes to `playlists.txt` and `playlist_songs.txt` respectively
- Deleting playlists or songs updates these files accordingly

---

## Summary
This design specification prioritizes stable and semantic element IDs that support dynamic content rendering and user interaction flows. It defines clean RESTful routes for navigation, clear mapping between UI elements and actions, and comprehensive data access utilizing local text files. This flexible UI design facilitates filtering and sorting features ensuring a responsive and user-friendly MusicStreaming application.
