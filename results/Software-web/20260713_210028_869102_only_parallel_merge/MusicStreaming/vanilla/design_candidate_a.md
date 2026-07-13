# MusicStreaming Application Design Specification

## Overview
This document provides a complete, detailed UI and backend interaction design for the MusicStreaming web application implemented in Flask. It enables front-end and back-end teams to work independent of each other by clearly defining routes, page elements, interactions, and data access for all 10 pages.

---

# 1. Flask Routes and Navigation Flow

## Base URL: `/`

### 1. Dashboard Page
- **Route:** `/dashboard`
- **Methods:** GET
- **Template:** `dashboard.html`
- **Description:** Entry point of the app showing featured songs, trending artists, and navigation buttons.

### 2. Song Catalog Page
- **Route:** `/songs`
- **Methods:** GET
- **Template:** `song_catalog.html`
- **Query Params:** `search`, `genre` (optional for filtering/search)

### 3. Song Details Page
- **Route:** `/song/<int:song_id>`
- **Methods:** GET
- **Template:** `song_details.html`

### 4. Playlist Page
- **Route:** `/playlists`
- **Methods:** GET
- **Template:** `playlists.html`

### 5. Playlist Details Page
- **Route:** `/playlist/<int:playlist_id>`
- **Methods:** GET
- **Template:** `playlist_details.html`

### 6. Create Playlist Page
- **Route:** `/playlists/create`
- **Methods:** GET, POST
- **Template:** `create_playlist.html`
- **POST:** Handles form submission to create playlist.

### 7. Album Browse Page
- **Route:** `/albums`
- **Methods:** GET
- **Template:** `albums.html`
- **Query Params:** `search`, `sort` (optional)

### 8. Album Details Page
- **Route:** `/album/<int:album_id>`
- **Methods:** GET
- **Template:** `album_details.html`

### 9. Artist Profile Page
- **Route:** `/artists`
- **Methods:** GET
- **Template:** `artists.html`
- **Query Params:** `search`, `sort` (optional)

### 10. Genre Exploration Page
- **Route:** `/genres`
- **Methods:** GET
- **Template:** `genres.html`
- **Query Params:** `selected_genre` (optional)


# 2. Detailed Page Specifications

---

## 1. Dashboard Page
- **Page Title:** Music Streaming Dashboard
- **Container:** `dashboard-page` (Div)

### UI Elements:
- `featured-songs` (Div): Displays featured songs with titles and brief info. Data read from `songs.txt` filtering top play_count songs.

- Buttons:
  - `browse-songs-button`: Navigates to `/songs`
  - `my-playlists-button`: Navigates to `/playlists`
  - `trending-artists-button`: Navigates to `/artists` and shows trending artists based on play_count statistics from `songs.txt`/`artists.txt`

### Interactions:
- Clicking any button sends the user to the respective page.

---

## 2. Song Catalog Page
- **Page Title:** Song Catalog
- **Container:** `catalog-page` (Div)

### UI Elements:
- `search-input` (Input): User types song/artist/album name for filtering.
- `genre-filter` (Dropdown): Options loaded from `genres.txt`.
- `songs-grid` (Div): Displays song cards each with:
  - Cover art (fetched via album or default)
  - Song title
  - Artist name
  - Duration
  - `add-to-playlist-button-{song_id}` (Button): To add song to playlists.

### Interaction:
- Search or select genre filters reload song list accordingly.
- Clicking `add-to-playlist-button-{song_id}` leads to modal or inline UI for selecting playlist to add this song.

### Data Access:
- Reads `songs.txt` for all songs.
- Reads `artists.txt` and `albums.txt` to resolve artist and album names.
- Filters by search text and genre.

---

## 3. Song Details Page
- **Page Title:** Song Details
- **Container:** `song-details-page` (Div)

### UI Elements:
- `song-title` (H1): Displays song title
- `artist-name` (Div): Displays artist name, clickable to `/artists` or to artist detail (not specified but link to artist page)
- `album-name` (Div): Album name
- `duration-display` (Div): Duration in seconds or formatted
- `play-button` (Button): Plays song (frontend effect)

### Data Access:
- Reads `songs.txt` by `song_id`.
- Reads `artists.txt` and `albums.txt` to resolve artist and album names.

---

## 4. Playlist Page
- **Page Title:** My Playlists
- **Container:** `playlists-page` (Div)

### UI Elements:
- `playlists-grid` (Div): Displays playlist cards with cover (optional or default), title, and song count
- Buttons:
  - `create-playlist-button`: Navigates to `/playlists/create`
  - `view-playlist-button-{playlist_id}`: Navigates to `/playlist/<playlist_id>`
  - `back-to-dashboard`: Navigates to `/dashboard`

### Data Access:
- Reads `playlists.txt` for playlist metadata.
- Reads `playlist_songs.txt` for song counts.

---

## 5. Playlist Details Page
- **Page Title:** Playlist Details
- **Container:** `playlist-details-page` (Div)

### UI Elements:
- `playlist-title` (H1): Shows playlist title
- `playlist-description` (Div): Shows description
- `songs-in-playlist` (Table): Columns - Song Title, Artist, Duration, Remove Button
- `remove-song-button-{song_id}` (Button): Removes song from playlist
- `delete-playlist-button` (Button): Deletes entire playlist

### Interactions:
- Remove buttons update `playlist_songs.txt` to delete entries.
- Delete playlist updates/deletes `playlists.txt` and corresponding `playlist_songs.txt` entries.

### Data Access:
- Reads `playlists.txt` for playlist info.
- Reads `playlist_songs.txt` for songs in this playlist.
- Reads `songs.txt`, `artists.txt` for song and artist details.

---

## 6. Create Playlist Page
- **Page Title:** Create New Playlist
- **Container:** `create-playlist-page` (Div)

### UI Elements:
- `playlist-name-input` (Input): User inputs playlist name
- `playlist-description-input` (Textarea): Playlist description
- `save-playlist-button` (Button): Submits POST to create playlist
- `cancel-create-button` (Button): Navigates back to `/playlists`

### Interactions:
- On save, validate data, append new record to `playlists.txt` and redirect to `/playlists`.
- Cancel discards and navigates back.

---

## 7. Album Browse Page
- **Page Title:** Albums
- **Container:** `albums-page` (Div)

### UI Elements:
- `albums-grid` (Div): Displays album cards with cover, title, artist, year
- `search-albums` (Input): Search albums by title or artist
- `sort-albums` (Dropdown): Options: By Title, By Artist, By Year
- `view-album-button-{album_id}` (Button): Navigates to `/album/<album_id>`

### Data Access:
- Reads `albums.txt` and `artists.txt` for display.
- Supports filtering and sorting.

---

## 8. Album Details Page
- **Page Title:** Album Details
- **Container:** `album-details-page` (Div)

### UI Elements:
- `album-title` (H1)
- `album-artist` (Div)
- `album-year` (Div)
- `album-songs-list` (Div): Shows all songs in album with title and duration
- `add-album-to-playlist-button` (Button): Adds all album songs to selected playlist (UI to select playlist or modal)

### Data Access:
- Reads `albums.txt` for album info
- Reads `songs.txt` filtered by `album_id` for songs
- Reads `artists.txt` for artist name

---

## 9. Artist Profile Page
- **Page Title:** Artist Profiles
- **Container:** `artists-page` (Div)

### UI Elements:
- `artists-grid` (Div): Displays artist cards with photo (if exists), name, genre
- `search-artists` (Input): Search artists by name
- `artists-sort` (Dropdown): Sort options: By Name, By Genre
- `view-artist-button-{artist_id}` (Button): View detailed artist profile (if implemented, could link to songs or albums by artist)

### Data Access:
- Reads `artists.txt` for all artists

---

## 10. Genre Exploration Page
- **Page Title:** Genre Exploration
- **Container:** `genres-page` (Div)

### UI Elements:
- `genres-list` (Div): List of all genre names from `genres.txt`
- `select-genre` (Dropdown): Select a genre to view details
- `genre-songs` (Div): Displays songs filtered by selected genre
- `genre-artists` (Div): Displays artists filtered by selected genre
- `back-to-dashboard` (Button): Navigates to `/dashboard`

### Data Access:
- Reads `genres.txt` for genres
- Reads `songs.txt` and `artists.txt` filtered by genre


# 3. Data Files and Access Patterns Summary

| Data File           | Usage                                          | Pages Accessing                    |
|---------------------|------------------------------------------------|----------------------------------|
| `songs.txt`          | Master song data; filter, search, duration, play counts | Dashboard, Song Catalog, Song Details, Playlist Details, Album Details, Genre Exploration |
| `artists.txt`        | Artist metadata for display and filtering      | Dashboard, Song Catalog, Song Details, Album Browse, Artist Profile, Playlist Details, Genre Exploration |
| `albums.txt`         | Album metadata, filtering, and sorting          | Song Catalog (to resolve album info), Album Browse, Album Details  |
| `genres.txt`         | Genre list and descriptions for filtering      | Song Catalog, Genre Exploration             |
| `playlists.txt`      | Playlist metadata, creation, deletion          | Playlist Page, Playlist Details, Create Playlist        |
| `playlist_songs.txt` | Song-to-playlist mappings, song addition/removal | Playlist Details, Playlist Page, Add to Playlist actions |


---

# Appendix: Element ID Naming Conventions

- Buttons specific to entities follow the template with exact IDs, e.g., `add-to-playlist-button-{song_id}`, `view-playlist-button-{playlist_id}`, `remove-song-button-{song_id}` etc.
- Containers have descriptive IDs like `dashboard-page`, `catalog-page`, `playlist-details-page`.
- Inputs and selectors use `search-input`, `genre-filter`, `select-genre` IDs.

---

This design specification stands as a single source of truth for implementing the MusicStreaming app's frontend and backend interfaces with Flask and local text file data management.