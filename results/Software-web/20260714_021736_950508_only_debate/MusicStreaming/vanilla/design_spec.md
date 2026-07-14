# MusicStreaming Web Application Design Specification

---

## Section 1: Flask Routes and Views Specification

| Route Path                 | HTTP Methods | Template              | Context Variables (Name : Type)                                       |
|----------------------------|--------------|-----------------------|-----------------------------------------------------------------------|
| /                          | GET          | dashboard.html        | featured_songs : list[Song], trending_artists : list[Artist]          |
| /songs                     | GET, POST    | song_catalog.html     | songs : list[Song], genres : list[str], search_query : str, genre_filter : str |
| /songs/<int:song_id>       | GET          | song_details.html     | song : Song, artist : Artist, album : Album                           |
| /playlists                 | GET          | playlists.html        | playlists : list[Playlist]                                             |
| /playlists/<int:playlist_id> | GET, POST | playlist_details.html | playlist : Playlist, songs : list[Song]                               |
| /playlists/create          | GET, POST    | create_playlist.html  | None or validation errors                                             |
| /albums                    | GET, POST    | albums.html           | albums : list[Album], search_albums : str, sort_albums : str           |
| /albums/<int:album_id>     | GET          | album_details.html    | album : Album, songs : list[Song]                                     |
| /artists                   | GET, POST    | artists.html          | artists : list[Artist], search_artists : str, artists_sort : str       |
| /artists/<int:artist_id>   | GET          | artist_profile.html   | artist : Artist, songs : list[Song], albums : list[Album]             |
| /genres                    | GET, POST    | genres.html           | genres : list[str], selected_genre : str, genre_songs : list[Song], genre_artists : list[Artist] |

---

## Section 2: HTML Template Element IDs and Interactions

### 1. Dashboard Page (/)
- dashboard-page (Div)
- featured-songs (Div)
- browse-songs-button (Button) - navigate to /songs (GET)
- my-playlists-button (Button) - navigate to /playlists (GET)
- trending-artists-button (Button) - navigate to /artists (GET)

### 2. Song Catalog Page (/songs)
- catalog-page (Div)
- search-input (Input, name=search_query)
- genre-filter (Dropdown, name=genre_filter)
- songs-grid (Div)
- add-to-playlist-button-{song_id} (Button) - POST form button with field song_id, form action /songs
- Form method POST, action /songs

### 3. Song Details Page (/songs/<song_id>)
- song-details-page (Div)
- song-title (H1)
- artist-name (Div) with link to /artists/<artist_id>
- album-name (Div)
- duration-display (Div)
- play-button (Button) - no form (client action)

### 4. Playlist Page (/playlists)
- playlists-page (Div)
- playlists-grid (Div)
- create-playlist-button (Button) - navigate to /playlists/create
- view-playlist-button-{playlist_id} (Button) - navigate to /playlists/<playlist_id>
- back-to-dashboard (Button) - navigate to /

### 5. Playlist Details Page (/playlists/<playlist_id>)
- playlist-details-page (Div)
- playlist-title (H1)
- playlist-description (Div)
- songs-in-playlist (Table)
- remove-song-button-{song_id} (Button) - POST form button with field song_id, form action /playlists/<playlist_id>
- delete-playlist-button (Button) - POST form button, form action /playlists/<playlist_id>

### 6. Create Playlist Page (/playlists/create)
- create-playlist-page (Div)
- playlist-name-input (Input, name=playlist_name)
- playlist-description-input (Textarea, name=playlist_description)
- save-playlist-button (Button) - submits form POST to /playlists/create
- cancel-create-button (Button) - navigate to /playlists

### 7. Album Browse Page (/albums)
- albums-page (Div)
- albums-grid (Div)
- search-albums (Input, name=search_albums)
- sort-albums (Dropdown, name=sort_albums)
- view-album-button-{album_id} (Button) - navigate to /albums/<album_id>
- Form method POST, action /albums

### 8. Album Details Page (/albums/<album_id>)
- album-details-page (Div)
- album-title (H1)
- album-artist (Div)
- album-year (Div)
- album-songs-list (Div)
- add-album-to-playlist-button (Button) - POST form button with field album_id, form action /albums/<album_id>

### 9. Artist Profile Page (/artists)
- artists-page (Div)
- artists-grid (Div)
- search-artists (Input, name=search_artists)
- artists-sort (Dropdown, name=artists_sort)
- view-artist-button-{artist_id} (Button) - navigate to /artists/<artist_id>
- Form method POST, action /artists

### 10. Genre Exploration Page (/genres)
- genres-page (Div)
- genres-list (Div)
- select-genre (Dropdown, name=selected_genre)
- genre-songs (Div)
- genre-artists (Div)
- back-to-dashboard (Button) - navigate to /
- Form method POST, action /genres

---

## Section 3: Local Text File Data Schemas and Access

All data files are placed in the `data/` directory using pipe `|` delimiter.

### 1. `songs.txt`
- Fields: `song_id|title|artist_id|album_id|genre|duration|release_date|play_count`
- Example: `1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000`

### 2. `artists.txt`
- Fields: `artist_id|name|genre|country|formation_year`
- Example: `1|Queen|Rock|United Kingdom|1970`

### 3. `albums.txt`
- Fields: `album_id|title|artist_id|release_year|total_songs|genre`
- Example: `1|A Night at the Opera|1|1975|11|Rock`

### 4. `genres.txt`
- Fields: `genre_id|genre_name|description`
- Example: `1|Rock|Guitar-driven music with strong beats and vocals`

### 5. `playlists.txt`
- Fields: `playlist_id|title|description|creation_date|total_songs`
- Example: `1|Workout Mix|High energy songs for the gym|2025-01-15|25`

### 6. `playlist_songs.txt`
- Fields: `playlist_song_id|playlist_id|song_id|added_date`
- Example: `1|1|2|2025-01-15`

---

# End of Canonical Design Specification
