from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

# File paths
DATA_PATHS = {
    'songs': 'data/songs.txt',
    'artists': 'data/artists.txt',
    'albums': 'data/albums.txt',
    'genres': 'data/genres.txt',
    'playlists': 'data/playlists.txt',
    'playlist_songs': 'data/playlist_songs.txt'
}

# ==========================
# Data Loading Helper Methods
# ==========================
def load_songs():
    songs = []
    try:
        with open(DATA_PATHS['songs'], 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue  # malformed line
                song_id, title, artist_id, album_id, genre_id, duration = parts
                songs.append({
                    'song_id': int(song_id),
                    'title': title,
                    'artist_id': int(artist_id),
                    'album_id': int(album_id),
                    'genre_id': int(genre_id),
                    'duration': int(duration)
                })
    except FileNotFoundError:
        pass
    return songs


def load_artists():
    artists = []
    try:
        with open(DATA_PATHS['artists'], 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                artist_id, name, genre_id, country, formation_year = parts
                artists.append({
                    'artist_id': int(artist_id),
                    'name': name,
                    'genre_id': int(genre_id),
                    'country': country,
                    'formation_year': int(formation_year)
                })
    except FileNotFoundError:
        pass
    return artists


def load_albums():
    albums = []
    try:
        with open(DATA_PATHS['albums'], 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                album_id, title, artist_id, year, genre_id = parts
                albums.append({
                    'album_id': int(album_id),
                    'title': title,
                    'artist_id': int(artist_id),
                    'year': int(year),
                    'genre_id': int(genre_id)
                })
    except FileNotFoundError:
        pass
    return albums


def load_genres():
    genres = []
    try:
        with open(DATA_PATHS['genres'], 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 3:
                    continue
                genre_id, genre_name, description = parts
                genres.append({
                    'genre_id': int(genre_id),
                    'genre_name': genre_name,
                    'description': description
                })
    except FileNotFoundError:
        pass
    return genres


def load_playlists():
    playlists = []
    try:
        with open(DATA_PATHS['playlists'], 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 3:
                    continue
                playlist_id, title, description = parts
                playlists.append({
                    'playlist_id': int(playlist_id),
                    'title': title,
                    'description': description
                })
    except FileNotFoundError:
        pass
    return playlists


def load_playlist_songs():
    playlist_songs = []
    try:
        with open(DATA_PATHS['playlist_songs'], 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 2:
                    continue
                playlist_id, song_id = parts
                playlist_songs.append({
                    'playlist_id': int(playlist_id),
                    'song_id': int(song_id)
                })
    except FileNotFoundError:
        pass
    return playlist_songs

# ======================
# Data Saving Helper Methods
# ======================
from functions import write_text_file

import os

def save_playlists(playlists):
    # Save playlists list of dict to file
    lines = []
    for p in playlists:
        line = f"{p['playlist_id']}|{p['title']}|{p['description']}"
        lines.append(line)
    content = "\n".join(lines)
    # Use the tool to write
    write_text_file(filename=DATA_PATHS['playlists'], content=content)


def save_playlist_songs(playlist_songs):
    # Save playlist_songs list of dict to file
    lines = []
    for ps in playlist_songs:
        line = f"{ps['playlist_id']}|{ps['song_id']}"
        lines.append(line)
    content = "\n".join(lines)
    write_text_file(filename=DATA_PATHS['playlist_songs'], content=content)

# ======================
# Utility lookup functions
# ======================
def get_artist_name_by_id(artists, artist_id):
    for artist in artists:
        if artist['artist_id'] == artist_id:
            return artist['name']
    return "Unknown Artist"

def get_album_name_by_id(albums, album_id):
    for album in albums:
        if album['album_id'] == album_id:
            return album['title']
    return "Unknown Album"

def get_genre_name_by_id(genres, genre_id):
    for genre in genres:
        if genre['genre_id'] == genre_id:
            return genre['genre_name']
    return "Unknown Genre"

def get_genre_desc_by_id(genres, genre_id):
    for genre in genres:
        if genre['genre_id'] == genre_id:
            return genre['description']
    return ""

# ==========================
# Flask Route Implementations
# ==========================

# 1) / root redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


# 2) /dashboard - GET
@app.route('/dashboard')
def dashboard_page():
    songs = load_songs()
    artists = load_artists()

    # featured_songs = list of dict {song_id, title, artist_name, duration}
    # Let's pick first 5 songs as featured, with artist names
    featured_songs = []
    for s in songs[:5]:
        artist_name = get_artist_name_by_id(artists, s['artist_id'])
        featured_songs.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_name,
            'duration': s['duration']
        })

    # trending_artists = first 5 artists, dict {artist_id, name}
    trending_artists = [{'artist_id': a['artist_id'], 'name': a['name']} for a in artists[:5]]

    return render_template('dashboard.html',
                           featured_songs=featured_songs,
                           trending_artists=trending_artists)


# 3) /songs GET, POST
@app.route('/songs', methods=['GET', 'POST'])
def song_catalog():
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()
    genres = load_genres()

    # Prepare songs with required fields for display
    # {song_id, title, artist_name, album_name, genre, duration}

    # Search and filter logic
    search_query = ''
    selected_genre = ''

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        selected_genre = request.form.get('selected_genre', '').strip()
    else:
        search_query = request.args.get('search_query', '').strip()
        selected_genre = request.args.get('selected_genre', '').strip()

    filtered_songs = []
    for s in songs:
        artist_name = get_artist_name_by_id(artists, s['artist_id'])
        album_name = get_album_name_by_id(albums, s['album_id'])
        genre_name = get_genre_name_by_id(genres, s['genre_id'])

        # Filter by search and genre
        if search_query and search_query.lower() not in s['title'].lower():
            continue
        if selected_genre and selected_genre != genre_name:
            continue

        filtered_songs.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_name,
            'album_name': album_name,
            'genre': genre_name,
            'duration': s['duration']
        })

    # Get all genres for filter selection
    genres_list = [g['genre_name'] for g in genres]

    return render_template('song_catalog.html',
                           songs=filtered_songs,
                           genres=genres_list,
                           search_query=search_query,
                           selected_genre=selected_genre)


# 4) /songs/<int:song_id> GET
@app.route('/songs/<int:song_id>')
def song_details(song_id):
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()

    song = None
    for s in songs:
        if s['song_id'] == song_id:
            artist_name = get_artist_name_by_id(artists, s['artist_id'])
            album_name = get_album_name_by_id(albums, s['album_id'])
            song = {
                'song_id': s['song_id'],
                'title': s['title'],
                'artist_name': artist_name,
                'album_name': album_name,
                'duration': s['duration']
            }
            break
    if song is None:
        abort(404)  # Not found

    return render_template('song_details.html', song=song)


# 5) /playlists GET
@app.route('/playlists')
def playlists_page():
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()

    # For playlists list, count total songs
    playlists_with_count = []
    for p in playlists:
        total_songs = sum(1 for ps in playlist_songs if ps['playlist_id'] == p['playlist_id'])
        playlists_with_count.append({
            'playlist_id': p['playlist_id'],
            'title': p['title'],
            'description': p['description'],
            'total_songs': total_songs
        })

    return render_template('playlists.html', playlists=playlists_with_count)


# 6) /playlists/<int:playlist_id> GET
@app.route('/playlists/<int:playlist_id>')
def playlist_details(playlist_id):
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()
    songs = load_songs()
    artists = load_artists()

    playlist = None
    for p in playlists:
        if p['playlist_id'] == playlist_id:
            playlist = p
            break
    if playlist is None:
        abort(404)

    # Get songs of this playlist
    songs_in_playlist = []
    for ps in playlist_songs:
        if ps['playlist_id'] == playlist_id:
            # Find song details
            for s in songs:
                if s['song_id'] == ps['song_id']:
                    artist_name = get_artist_name_by_id(artists, s['artist_id'])
                    songs_in_playlist.append({
                        'song_id': s['song_id'],
                        'title': s['title'],
                        'artist_name': artist_name,
                        'duration': s['duration']
                    })
                    break

    return render_template('playlist_details.html',
                           playlist=playlist,
                           songs=songs_in_playlist)

# 7) /playlists/create GET, POST
@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'GET':
        return render_template('create_playlist.html')

    # POST: create playlist
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()

    form_data = {'title': title, 'description': description}

    # Validate input - title required
    if not title:
        return render_template('create_playlist.html', form_data=form_data)

    # Load playlists
    playlists = load_playlists()

    # Generate new playlist ID
    existing_ids = [p['playlist_id'] for p in playlists]
    new_id = max(existing_ids) + 1 if existing_ids else 1

    # Add new playlist
    new_playlist = {'playlist_id': new_id, 'title': title, 'description': description}
    playlists.append(new_playlist)

    # Save playlists
    # Awaiting synchronous save with write_text_file
    save_playlists(playlists)

    # Redirect to playlist detail page
    return redirect(url_for('playlist_details', playlist_id=new_id))


# 8) /albums GET, POST
@app.route('/albums', methods=['GET', 'POST'])
def album_browse():
    albums = load_albums()
    artists = load_artists()

    search_query = ''
    sort_option = ''

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        sort_option = request.form.get('sort_option', '').strip()
    else:
        search_query = request.args.get('search_query', '').strip()
        sort_option = request.args.get('sort_option', '').strip()

    # Filter albums by search, which looks at album title
    filtered_albums = []
    for a in albums:
        artist_name = get_artist_name_by_id(artists, a['artist_id'])
        if search_query and search_query.lower() not in a['title'].lower():
            continue
        filtered_albums.append({
            'album_id': a['album_id'],
            'title': a['title'],
            'artist_name': artist_name,
            'year': a['year'],
            'genre': get_genre_name_by_id(load_genres(), a['genre_id'])
        })

    # Sorting
    def album_sort_key(a):
        if sort_option == 'title':
            return a['title'].lower()
        if sort_option == 'artist':
            return a['artist_name'].lower()
        if sort_option == 'year':
            return a['year']
        return 0

    filtered_albums.sort(key=album_sort_key)

    return render_template('albums.html',
                           albums=filtered_albums,
                           search_query=search_query,
                           sort_option=sort_option)


# 9) /albums/<int:album_id> GET
@app.route('/albums/<int:album_id>')
def album_details(album_id):
    albums = load_albums()
    artists = load_artists()
    songs = load_songs()

    album = None
    for a in albums:
        if a['album_id'] == album_id:
            artist_name = get_artist_name_by_id(artists, a['artist_id'])
            album = {
                'album_id': a['album_id'],
                'title': a['title'],
                'artist_name': artist_name,
                'year': a['year']
            }
            break

    if album is None:
        abort(404)

    # Get songs in album
    album_songs = []
    for s in songs:
        if s['album_id'] == album_id:
            album_songs.append({
                'song_id': s['song_id'],
                'title': s['title'],
                'duration': s['duration']
            })

    return render_template('album_details.html', album=album, songs=album_songs)


# 10) /artists GET, POST
@app.route('/artists', methods=['GET', 'POST'])
def artist_profile():
    artists = load_artists()
    genres = load_genres()

    search_query = ''
    sort_option = ''

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        sort_option = request.form.get('sort_option', '').strip()
    else:
        search_query = request.args.get('search_query', '').strip()
        sort_option = request.args.get('sort_option', '').strip()

    # Filter artists by name or genre
    filtered_artists = []
    for a in artists:
        genre_name = get_genre_name_by_id(genres, a['genre_id'])
        if search_query and search_query.lower() not in a['name'].lower():
            continue
        filtered_artists.append({
            'artist_id': a['artist_id'],
            'name': a['name'],
            'genre': genre_name
        })

    # Sort
    def artist_sort_key(a):
        if sort_option == 'name':
            return a['name'].lower()
        if sort_option == 'genre':
            return a['genre'].lower()
        return 0

    filtered_artists.sort(key=artist_sort_key)

    return render_template('artists.html',
                           artists=filtered_artists,
                           search_query=search_query,
                           sort_option=sort_option)


# 11) /artists/<int:artist_id> GET
@app.route('/artists/<int:artist_id>')
def artist_details(artist_id):
    artists = load_artists()

    artist = None
    for a in artists:
        if a['artist_id'] == artist_id:
            artist = {
                'artist_id': a['artist_id'],
                'name': a['name'],
                'genre': get_genre_name_by_id(load_genres(), a['genre_id']),
                'country': a['country'],
                'formation_year': a['formation_year']
            }
            break

    if artist is None:
        abort(404)

    return render_template('artist_details.html', artist=artist)


# 12) /genres GET, POST
@app.route('/genres', methods=['GET', 'POST'])
def genre_exploration():
    genres = load_genres()
    artists = load_artists()
    songs = load_songs()

    selected_genre_id = None
    genre_songs = []
    genre_artists = []

    if request.method == 'POST':
        try:
            selected_genre_id = int(request.form.get('selected_genre_id', '').strip())
        except ValueError:
            selected_genre_id = None
    else:
        try:
            selected_genre_id = int(request.args.get('selected_genre_id', '').strip())
        except (ValueError, AttributeError):
            selected_genre_id = None

    if selected_genre_id is not None:
        # Get songs and artists for selected genre
        genre_songs = []
        genre_artists_map = {}
        for s in songs:
            if s['genre_id'] == selected_genre_id:
                artist_name = get_artist_name_by_id(artists, s['artist_id'])
                genre_songs.append({
                    'song_id': s['song_id'],
                    'title': s['title'],
                    'artist_name': artist_name,
                    'duration': s['duration']
                })
                genre_artists_map[s['artist_id']] = True

        genre_artists = []
        for a in artists:
            if a['artist_id'] in genre_artists_map:
                genre_artists.append({
                    'artist_id': a['artist_id'],
                    'name': a['name']
                })

    return render_template('genres.html',
                           genres=genres,
                           selected_genre_id=selected_genre_id,
                           genre_songs=genre_songs,
                           genre_artists=genre_artists)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
