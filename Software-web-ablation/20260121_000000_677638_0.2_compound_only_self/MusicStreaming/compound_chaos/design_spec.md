# MusicStreaming Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                    | Function Name           | HTTP Method(s) | Template File             | Context Variables                                                                                                 |
|-------------------------------|------------------------|----------------|---------------------------|------------------------------------------------------------------------------------------------------------------|
| /                             | root_redirect           | GET            | N/A (redirect)             | None                                                                                                             |
| /dashboard                    | dashboard              | GET            | dashboard.html            | featured_songs: List[Dict] with keys {song_id:int, title:str, artist_name:str, duration:int}
  trending_artists: List[Dict] with keys {artist_id:int, name:str, genre:str}                                      |
| /songs                       | song_catalog           | GET            | song_catalog.html         | songs: List[Dict] with {song_id:int, title:str, artist_name:str, album_name:str, genre:str, duration:int}
  genres: List[str] for genre filter options                                                                     |
| /songs/<int:song_id>         | song_details           | GET            | song_details.html         | song: Dict with {song_id:int, title:str, artist_id:int, artist_name:str, album_id:int, album_name:str, genre:str, duration:int, release_date:str}
                                         |
| /playlists                   | my_playlists           | GET            | playlists.html            | playlists: List[Dict] with {playlist_id:int, title:str, description:str, total_songs:int}                                                         |
| /playlists/<int:playlist_id> | playlist_details       | GET            | playlist_details.html     | playlist: Dict with {playlist_id:int, title:str, description:str}
  songs_in_playlist: List[Dict] with {song_id:int, title:str, artist_name:str, duration:int}                                  |
| /playlists/create            | create_playlist        | GET            | create_playlist.html      | None                                                                                                             |
| /playlists/create            | save_playlist          | POST           | N/A (redirect or render)  | Form data: playlist_name:str, playlist_description:str                                                             |
| /albums                     | albums_browse          | GET            | albums.html               | albums: List[Dict] with {album_id:int, title:str, artist_name:str, year:int}
  sort_options: List[str] = ["By Title", "By Artist", "By Year"]                                                    |
| /albums/<int:album_id>       | album_details          | GET            | album_details.html        | album: Dict with {album_id:int, title:str, artist_name:str, year:int}
  album_songs: List[Dict] with {song_id:int, title:str, artist_name:str, duration:int}                                 |
| /artists                    | artist_profiles        | GET            | artists.html              | artists: List[Dict] with {artist_id:int, name:str, genre:str, country:str}
  sort_options: List[str] = ["By Name", "By Genre"]                                                      |
| /artists/<int:artist_id>     | artist_profile         | GET            | artist_profile.html       | artist: Dict with {artist_id:int, name:str, genre:str, country:str, formation_year:int}
  songs_by_artist: List[Dict] with {song_id:int, title:str, album_name:str, duration:int}                         |
| /genres                     | genre_exploration      | GET            | genres.html               | genres: List[Dict] with {genre_id:int, genre_name:str, description:str}
  selected_genre: Optional[str]
  genre_songs: List[Dict] with {song_id:int, title:str, artist_name:str, duration:int}
  genre_artists: List[Dict] with {artist_id:int, name:str, genre:str}                                                 |

---

## Section 2: HTML Template Specifications (For Frontend Developer)

1. **dashboard.html**
- Template File Path: templates/dashboard.html
- Page Title:
  - <title>Music Streaming Dashboard</title>
  - <h1>Music Streaming Dashboard</h1>
- Required Element IDs:
  - Div: dashboard-page
  - Div: featured-songs
  - Button: browse-songs-button
  - Button: my-playlists-button
  - Button: trending-artists-button
- Context Variables:
  - featured_songs: List of dictionaries with keys {song_id, title, artist_name, duration (int seconds)}
  - trending_artists: List of dictionaries with keys {artist_id, name, genre}
- Navigation Mappings:
  - Button ID browse-songs-button -> Flask route function: song_catalog
  - Button ID my-playlists-button -> Flask route function: my_playlists
  - Button ID trending-artists-button -> Flask route function: artist_profiles

2. **song_catalog.html**
- Template File Path: templates/song_catalog.html
- Page Title:
  - <title>Song Catalog</title>
  - <h1>Song Catalog</h1>
- Required Element IDs:
  - Div: catalog-page
  - Input: search-input
  - Dropdown: genre-filter
  - Div: songs-grid
  - Button: add-to-playlist-button-{song_id} (dynamic button per song)
- Context Variables:
  - songs: List of dicts with {song_id, title, artist_name, album_name, genre, duration}
  - genres: List of strings (genre names)
- Navigation Mappings:
  - For each add-to-playlist-button-{song_id}, trigger an action to add the song (backend POST or JS)

3. **song_details.html**
- Template File Path: templates/song_details.html
- Page Title:
  - <title>Song Details</title>
  - <h1 id="song-title">{{ song.title }}</h1>
- Required Element IDs:
  - Div: song-details-page
  - H1: song-title
  - Div: artist-name (artist name is a link to artist_profile route with artist_id)
  - Div: album-name
  - Div: duration-display
  - Button: play-button
- Context Variables:
  - song: Dict with keys {song_id, title, artist_id, artist_name, album_id, album_name, genre, duration, release_date}
- Navigation Mappings:
  - artist-name div contains link to artist_profile function with artist_id
  - play-button triggers song play functionality

4. **playlists.html**
- Template File Path: templates/playlists.html
- Page Title:
  - <title>My Playlists</title>
  - <h1>My Playlists</h1>
- Required Element IDs:
  - Div: playlists-page
  - Div: playlists-grid
  - Button: create-playlist-button
  - Button: view-playlist-button-{playlist_id} (dynamic per playlist)
  - Button: back-to-dashboard
- Context Variables:
  - playlists: List of dicts with {playlist_id, title, description, total_songs}
- Navigation Mappings:
  - create-playlist-button -> create_playlist
  - view-playlist-button-{playlist_id} -> playlist_details
  - back-to-dashboard -> dashboard

5. **playlist_details.html**
- Template File Path: templates/playlist_details.html
- Page Title:
  - <title>Playlist Details</title>
  - <h1 id="playlist-title">{{ playlist.title }}</h1>
- Required Element IDs:
  - Div: playlist-details-page
  - H1: playlist-title
  - Div: playlist-description
  - Table: songs-in-playlist
  - Button: remove-song-button-{song_id} (dynamic per song)
  - Button: delete-playlist-button
- Context Variables:
  - playlist: Dict with {playlist_id, title, description}
  - songs_in_playlist: List of dicts with {song_id, title, artist_name, duration}
- Navigation Mappings:
  - remove-song-button-{song_id} triggers removal of song from playlist
  - delete-playlist-button triggers playlist deletion

6. **create_playlist.html**
- Template File Path: templates/create_playlist.html
- Page Title:
  - <title>Create New Playlist</title>
  - <h1>Create New Playlist</h1>
- Required Element IDs:
  - Div: create-playlist-page
  - Input: playlist-name-input
  - Textarea: playlist-description-input
  - Button: save-playlist-button
  - Button: cancel-create-button
- Context Variables:
  - None (empty form)
- Navigation Mappings:
  - save-playlist-button triggers form submission POST to save_playlist
  - cancel-create-button redirects back to my_playlists

7. **albums.html**
- Template File Path: templates/albums.html
- Page Title:
  - <title>Albums</title>
  - <h1>Albums</h1>
- Required Element IDs:
  - Div: albums-page
  - Div: albums-grid
  - Input: search-albums
  - Dropdown: sort-albums
  - Button: view-album-button-{album_id} (dynamic per album)
- Context Variables:
  - albums: List of dicts with {album_id, title, artist_name, year}
  - sort_options: List[str] = ["By Title", "By Artist", "By Year"]
- Navigation Mappings:
  - view-album-button-{album_id} -> album_details

8. **album_details.html**
- Template File Path: templates/album_details.html
- Page Title:
  - <title>Album Details</title>
  - <h1 id="album-title">{{ album.title }}</h1>
- Required Element IDs:
  - Div: album-details-page
  - H1: album-title
  - Div: album-artist
  - Div: album-year
  - Div: album-songs-list
  - Button: add-album-to-playlist-button
- Context Variables:
  - album: Dict with {album_id, title, artist_name, year}
  - album_songs: List of dicts with {song_id, title, artist_name, duration}
- Navigation Mappings:
  - add-album-to-playlist-button triggers adding all songs to playlist

9. **artists.html**
- Template File Path: templates/artists.html
- Page Title:
  - <title>Artist Profiles</title>
  - <h1>Artist Profiles</h1>
- Required Element IDs:
  - Div: artists-page
  - Div: artists-grid
  - Input: search-artists
  - Dropdown: artists-sort
  - Button: view-artist-button-{artist_id} (dynamic per artist)
- Context Variables:
  - artists: List of dicts with {artist_id, name, genre, country}
  - sort_options: List[str] = ["By Name", "By Genre"]
- Navigation Mappings:
  - view-artist-button-{artist_id} -> artist_profile

10. **genres.html**
- Template File Path: templates/genres.html
- Page Title:
  - <title>Genre Exploration</title>
  - <h1>Genre Exploration</h1>
- Required Element IDs:
  - Div: genres-page
  - Div: genres-list
  - Dropdown: select-genre
  - Div: genre-songs
  - Div: genre-artists
  - Button: back-to-dashboard
- Context Variables:
  - genres: List of dicts with {genre_id, genre_name, description}
  - selected_genre: Optional[str] if any genre selected
  - genre_songs: List of dicts with {song_id, title, artist_name, duration}
  - genre_artists: List of dicts with {artist_id, name, genre}
- Navigation Mappings:
  - back-to-dashboard -> dashboard
  - select-genre dropdown triggers page reload or ajax filtered by genre

---

## Section 3: Data File Schemas (For Backend Developer)

1. **data/songs.txt**
- File format: pipe-delimited (|)
- Fields:
  1. song_id (int): Unique identifier for each song
  2. title (str): Song title
  3. artist_id (int): Foreign key referencing artists.txt artist_id
  4. album_id (int): Foreign key referencing albums.txt album_id
  5. genre (str): Genre name
  6. duration (int): Duration of the song in seconds
  7. release_date (str): Song release date in YYYY-MM-DD format
  8. play_count (int): Number of times the song has been played
- Example rows:
```
1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
3|Shape of You|3|3|Pop|233|2017-01-06|4200000
```

2. **data/artists.txt**
- File format: pipe-delimited (|)
- Fields:
  1. artist_id (int): Unique identifier for each artist
  2. name (str): Artist name
  3. genre (str): Music genre
  4. country (str): Country of origin
  5. formation_year (int): Year the artist or band was formed
- Example rows:
```
1|Queen|Rock|United Kingdom|1970
2|The Weeknd|Synth-Pop|Canada|2010
3|Ed Sheeran|Pop|United Kingdom|2005
```

3. **data/albums.txt**
- File format: pipe-delimited (|)
- Fields:
  1. album_id (int): Unique identifier for each album
  2. title (str): Album title
  3. artist_id (int): Foreign key referencing artists.txt artist_id
  4. release_year (int): Year album was released
  5. total_songs (int): Number of songs in the album
  6. genre (str): Album genre
- Example rows:
```
1|A Night at the Opera|1|1975|11|Rock
2|After Hours|2|2019|14|Synth-Pop
3|Divide|3|2017|12|Pop
```

4. **data/genres.txt**
- File format: pipe-delimited (|)
- Fields:
  1. genre_id (int): Unique identifier for each genre
  2. genre_name (str): Name of genre
  3. description (str): Description of the genre
- Example rows:
```
1|Rock|Guitar-driven music with strong beats and vocals
2|Pop|Catchy mainstream music with broad appeal
3|Hip-Hop|Rhythmic music with rap vocals and beat production
```

5. **data/playlists.txt**
- File format: pipe-delimited (|)
- Fields:
  1. playlist_id (int): Unique identifier for each playlist
  2. title (str): Playlist title
  3. description (str): Playlist description
  4. creation_date (str): Date playlist was created in YYYY-MM-DD format
  5. total_songs (int): Number of songs in the playlist
- Example rows:
```
1|Workout Mix|High energy songs for the gym|2025-01-15|25
2|Chill Vibes|Relaxing music for study|2025-01-16|18
3|Party Hits|Latest party tracks|2025-01-17|32
```

6. **data/playlist_songs.txt**
- File format: pipe-delimited (|)
- Fields:
  1. playlist_song_id (int): Unique identifier for each entry
  2. playlist_id (int): Foreign key referencing playlists.txt playlist_id
  3. song_id (int): Foreign key referencing songs.txt song_id
  4. added_date (str): Date song was added to playlist in YYYY-MM-DD format
- Example rows:
```
1|1|2|2025-01-15
2|1|3|2025-01-15
3|2|1|2025-01-16
```

---

*End of MusicStreaming Design Specification.*
