# MusicStreaming Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path | Function Name | HTTP Method(s) | Template File | Context Variables |
|------------|---------------|----------------|---------------|-------------------|
| / | root_redirect | GET | N/A (redirect) | None |
| /dashboard | dashboard_page | GET | dashboard.html | featured_songs: list of dict {song_id: int, title: str, artist_name: str, duration: int}
  trending_artists: list of dict {artist_id: int, name: str} |
| /songs | song_catalog | GET, POST | song_catalog.html | songs: list of dict {song_id: int, title: str, artist_name: str, album_name: str, genre: str, duration: int}
  genres: list of str (available genres for filter)
  search_query: str (search string from user, optional)
  selected_genre: str (genre filter selected, optional) |
| /songs/<int:song_id> | song_details | GET | song_details.html | song: dict {song_id: int, title: str, artist_name: str, album_name: str, duration: int}
|
| /playlists | playlists_page | GET | playlists.html | playlists: list of dict {playlist_id: int, title: str, description: str, total_songs: int} |
| /playlists/<int:playlist_id> | playlist_details | GET | playlist_details.html | playlist: dict {playlist_id: int, title: str, description: str}
  songs: list of dict {song_id: int, title: str, artist_name: str, duration: int}
|
| /playlists/create | create_playlist | GET, POST | create_playlist.html | None (for GET)
  form_data: dict {title: str, description: str} for POST if invalid input |
| /albums | album_browse | GET, POST | albums.html | albums: list of dict {album_id: int, title: str, artist_name: str, year: int, genre: str}
  search_query: str (optional)
  sort_option: str (optional, e.g. 'title', 'artist', 'year') |
| /albums/<int:album_id> | album_details | GET | album_details.html | album: dict {album_id: int, title: str, artist_name: str, year: int}
  songs: list of dict {song_id: int, title: str, duration: int}
|
| /artists | artist_profile | GET, POST | artists.html | artists: list of dict {artist_id: int, name: str, genre: str}
  search_query: str (optional)
  sort_option: str (optional, e.g. 'name', 'genre') |
| /artists/<int:artist_id> | artist_details | GET | artist_details.html | artist: dict {artist_id: int, name: str, genre: str, country: str, formation_year: int} |
| /genres | genre_exploration | GET, POST | genres.html | genres: list of dict {genre_id: int, genre_name: str, description: str}
  selected_genre_id: int (optional)
  genre_songs: list of dict {song_id: int, title: str, artist_name: str, duration: int} (for selected genre)
  genre_artists: list of dict {artist_id: int, name: str} (for selected genre)
