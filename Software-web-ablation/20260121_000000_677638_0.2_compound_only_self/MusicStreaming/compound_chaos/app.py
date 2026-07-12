from flask import Flask, render_template, redirect, url_for, request, abort
from datetime import date
import os

app = Flask(__name__)

DATA_DIR = 'data'

# Utility loaders and savers

def load_songs():
    songs = []
    path = os.path.join(DATA_DIR, 'songs.txt')
    if not os.path.exists(path):
        return songs
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            try:
                song = {
                    'song_id': int(parts[0]),
                    'title': parts[1],
                    'artist_id': int(parts[2]),
                    'album_id': int(parts[3]),
                    'genre': parts[4],
                    'duration': int(parts[5]),
                    'release_date': parts[6],
                    'play_count': int(parts[7])
                }
                songs.append(song)
            except (IndexError, ValueError):
                # malformed line - skip
                continue
    return songs


def load_artists():
    artists = []
    path = os.path.join(DATA_DIR, 'artists.txt')
    if not os.path.exists(path):
        return artists
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            try:
                artist = {
                    'artist_id': int(parts[0]),
                    'name': parts[1],
                    'genre': parts[2],
                    'country': parts[3],
                    'formation_year': int(parts[4])
                }
                artists.append(artist)
            except (IndexError, ValueError):
                continue
    return artists


def load_albums():
    albums = []
    path = os.path.join(DATA_DIR, 'albums.txt')
    if not os.path.exists(path):
        return albums
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            try:
                album = {
                    'album_id': int(parts[0]),
                    'title': parts[1],
                    'artist_id': int(parts[2]),
                    'year': int(parts[3]),
                    'total_songs': int(parts[4]),
                    'genre': parts[5]
                }
                albums.append(album)
            except (IndexError, ValueError):
                continue
    return albums


def load_genres():
    genres = []
    path = os.path.join(DATA_DIR, 'genres.txt')
    if not os.path.exists(path):
        return genres
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            try:
                genre = {
                    'genre_id': int(parts[0]),
                    'genre_name': parts[1],
                    'description': parts[2]
                }
                genres.append(genre)
            except (IndexError, ValueError):
                continue
    return genres


def load_playlists():
    playlists = []
    path = os.path.join(DATA_DIR, 'playlists.txt')
    if not os.path.exists(path):
        return playlists
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            try:
                playlist = {
                    'playlist_id': int(parts[0]),
                    'title': parts[1],
                    'description': parts[2],
                    'creation_date': parts[3],
                    'total_songs': int(parts[4])
                }
                playlists.append(playlist)
            except (IndexError, ValueError):
                continue
    return playlists


def load_playlist_songs():
    playlist_songs = []
    path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    if not os.path.exists(path):
        return playlist_songs
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            try:
                entry = {
                    'playlist_song_id': int(parts[0]),
                    'playlist_id': int(parts[1]),
                    'song_id': int(parts[2]),
                    'added_date': parts[3]
                }
                playlist_songs.append(entry)
            except (IndexError, ValueError):
                continue
    return playlist_songs


def save_playlists(playlists):
    path = os.path.join(DATA_DIR, 'playlists.txt')
    lines = []
    for p in playlists:
        line = f"{p['playlist_id']}|{p['title']}|{p['description']}|{p['creation_date']}|{p['total_songs']}"
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n' if lines else '')


def save_playlist_songs(playlist_songs):
    path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    lines = []
    for ps in playlist_songs:
        line = f"{ps['playlist_song_id']}|{ps['playlist_id']}|{ps['song_id']}|{ps['added_date']}"
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n' if lines else '')


# Helper mappings

def get_artist_by_id(artist_id):
    for artist in load_artists():
        if artist['artist_id'] == artist_id:
            return artist
    return None


def get_album_by_id(album_id):
    for album in load_albums():
        if album['album_id'] == album_id:
            return album
    return None


def get_genre_by_name(genre_name):
    for genre in load_genres():
        if genre['genre_name'] == genre_name:
            return genre
    return None


def get_song_by_id(song_id):
    for song in load_songs():
        if song['song_id'] == song_id:
            return song
    return None


def get_playlist_by_id(playlist_id):
    for playlist in load_playlists():
        if playlist['playlist_id'] == playlist_id:
            return playlist
    return None


# Routes

@app.route('/')
def root_redirect():
    # Redirect to dashboard
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    songs = load_songs()
    artists = load_artists()

    # featured_songs: List[Dict] with keys {song_id, title, artist_name, duration}
    # For demonstration, pick top 5 songs by play_count
    songs_sorted = sorted(songs, key=lambda s: s.get('play_count', 0), reverse=True)
    featured_songs = []
    for song in songs_sorted[:5]:
        artist = get_artist_by_id(song['artist_id'])
        artist_name = artist['name'] if artist else 'Unknown'
        featured_songs.append({
            'song_id': song['song_id'],
            'title': song['title'],
            'artist_name': artist_name,
            'duration': song['duration']
        })

    # trending_artists: List[Dict] with keys {artist_id, name, genre}
    # We'll pick top 5 artists by total play_count of their songs
    artist_play_counts = {}
    for artist in artists:
        artist_play_counts[artist['artist_id']] = 0
    for song in songs:
        if song['artist_id'] in artist_play_counts:
            artist_play_counts[song['artist_id']] += song.get('play_count', 0)
    sorted_artists = sorted(artists, key=lambda a: artist_play_counts.get(a['artist_id'], 0), reverse=True)
    trending_artists = []
    for artist in sorted_artists[:5]:
        trending_artists.append({
            'artist_id': artist['artist_id'],
            'name': artist['name'],
            'genre': artist['genre']
        })

    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)


@app.route('/songs')
def song_catalog():
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()
    genres_data = load_genres()
    genres = [g['genre_name'] for g in genres_data]

    # Compose songs list context
    # Each song: {song_id, title, artist_name, album_name, genre, duration}
    artist_map = {a['artist_id']: a['name'] for a in artists}
    album_map = {al['album_id']: al['title'] for al in albums}

    songs_list = []
    for s in songs:
        artist_name = artist_map.get(s['artist_id'], 'Unknown')
        album_name = album_map.get(s['album_id'], 'Unknown')
        songs_list.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_name,
            'album_name': album_name,
            'genre': s['genre'],
            'duration': s['duration']
        })

    return render_template('song_catalog.html', songs=songs_list, genres=genres)


@app.route('/songs/<int:song_id>')
def song_details(song_id):
    song = get_song_by_id(song_id)
    if not song:
        abort(404)
    artist = get_artist_by_id(song['artist_id'])
    album = get_album_by_id(song['album_id'])

    # song: Dict with keys {song_id, title, artist_id, artist_name, album_id, album_name, genre, duration, release_date}
    song_context = {
        'song_id': song['song_id'],
        'title': song['title'],
        'artist_id': artist['artist_id'] if artist else None,
        'artist_name': artist['name'] if artist else 'Unknown',
        'album_id': album['album_id'] if album else None,
        'album_name': album['title'] if album else 'Unknown',
        'genre': song['genre'],
        'duration': song['duration'],
        'release_date': song['release_date']
    }
    return render_template('song_details.html', song=song_context)


@app.route('/playlists')
def my_playlists():
    playlists = load_playlists()

    # context playlists: List[Dict] with {playlist_id, title, description, total_songs}
    playlists_context = []
    for p in playlists:
        playlists_context.append({
            'playlist_id': p['playlist_id'],
            'title': p['title'],
            'description': p['description'],
            'total_songs': p['total_songs']
        })
    return render_template('playlists.html', playlists=playlists_context)


@app.route('/playlists/<int:playlist_id>')
def playlist_details(playlist_id):
    playlist = get_playlist_by_id(playlist_id)
    if not playlist:
        abort(404)
    playlist_songs_all = load_playlist_songs()
    songs = load_songs()
    artists = load_artists()

    # songs_in_playlist: List[Dict] with {song_id, title, artist_name, duration}
    songs_map = {s['song_id']: s for s in songs}
    artist_map = {a['artist_id']: a for a in artists}

    songs_in_playlist = []
    for entry in playlist_songs_all:
        if entry['playlist_id'] == playlist_id:
            song = songs_map.get(entry['song_id'])
            if song:
                artist_name = artist_map.get(song['artist_id'], {}).get('name', 'Unknown')
                songs_in_playlist.append({
                    'song_id': song['song_id'],
                    'title': song['title'],
                    'artist_name': artist_name,
                    'duration': song['duration']
                })

    playlist_context = {
        'playlist_id': playlist['playlist_id'],
        'title': playlist['title'],
        'description': playlist['description']
    }
    return render_template('playlist_details.html', playlist=playlist_context, songs_in_playlist=songs_in_playlist)


@app.route('/playlists/create', methods=['GET'])
def create_playlist():
    # Render empty form
    return render_template('create_playlist.html')


@app.route('/playlists/create', methods=['POST'])
def save_playlist():
    playlist_name = request.form.get('playlist_name', '').strip()
    playlist_description = request.form.get('playlist_description', '').strip()

    if not playlist_name:
        # Render back with error or redirect? Spec does not mention error display, use redirect with note
        return render_template('create_playlist.html', error='Playlist name required')

    playlists = load_playlists()
    # Generate new unique playlist_id
    existing_ids = [p['playlist_id'] for p in playlists]
    new_id = max(existing_ids, default=0) + 1

    new_playlist = {
        'playlist_id': new_id,
        'title': playlist_name,
        'description': playlist_description,
        'creation_date': date.today().isoformat(),
        'total_songs': 0
    }
    playlists.append(new_playlist)
    save_playlists(playlists)

    # Redirect to my_playlists page
    return redirect(url_for('my_playlists'))


@app.route('/albums')
def albums_browse():
    albums = load_albums()
    artists = load_artists()

    sort_options = ["By Title", "By Artist", "By Year"]

    # Prepare albums context list: {album_id, title, artist_name, year}
    artist_map = {a['artist_id']: a['name'] for a in artists}
    albums_list = []
    for album in albums:
        artist_name = artist_map.get(album['artist_id'], 'Unknown')
        albums_list.append({
            'album_id': album['album_id'],
            'title': album['title'],
            'artist_name': artist_name,
            'year': album['year']
        })

    # Sorting can be by any means - spec does not require sorting by query, so just default by title
    albums_list.sort(key=lambda a: a['title'])

    return render_template('albums.html', albums=albums_list, sort_options=sort_options)


@app.route('/albums/<int:album_id>')
def album_details(album_id):
    album = get_album_by_id(album_id)
    if not album:
        abort(404)

    songs = load_songs()
    artists = load_artists()
    artist = get_artist_by_id(album['artist_id'])

    album_songs = []
    for song in songs:
        if song['album_id'] == album_id:
            song_artist = get_artist_by_id(song['artist_id'])
            album_songs.append({
                'song_id': song['song_id'],
                'title': song['title'],
                'artist_name': song_artist['name'] if song_artist else 'Unknown',
                'duration': song['duration']
            })

    album_context = {
        'album_id': album['album_id'],
        'title': album['title'],
        'artist_name': artist['name'] if artist else 'Unknown',
        'year': album['year']
    }
    return render_template('album_details.html', album=album_context, album_songs=album_songs)


@app.route('/artists')
def artist_profiles():
    artists = load_artists()

    sort_options = ["By Name", "By Genre"]

    artists_list = []
    for artist in artists:
        artists_list.append({
            'artist_id': artist['artist_id'],
            'name': artist['name'],
            'genre': artist['genre'],
            'country': artist['country']
        })

    # Default sorting by Name
    artists_list.sort(key=lambda a: a['name'])

    return render_template('artists.html', artists=artists_list, sort_options=sort_options)


@app.route('/artists/<int:artist_id>')
def artist_profile(artist_id):
    artist = get_artist_by_id(artist_id)
    if not artist:
        abort(404)

    songs = load_songs()
    albums = load_albums()

    # songs_by_artist: List[Dict] with {song_id, title, album_name, duration}
    album_map = {al['album_id']: al['title'] for al in albums}
    songs_by_artist = []
    for song in songs:
        if song['artist_id'] == artist_id:
            album_name = album_map.get(song['album_id'], 'Unknown')
            songs_by_artist.append({
                'song_id': song['song_id'],
                'title': song['title'],
                'album_name': album_name,
                'duration': song['duration']
            })

    artist_context = {
        'artist_id': artist['artist_id'],
        'name': artist['name'],
        'genre': artist['genre'],
        'country': artist['country'],
        'formation_year': artist['formation_year']
    }
    return render_template('artist_profile.html', artist=artist_context, songs_by_artist=songs_by_artist)


@app.route('/genres')
def genre_exploration():
    genres = load_genres()
    songs = load_songs()
    artists = load_artists()

    selected_genre = request.args.get('selected_genre')

    genre_songs = []
    genre_artists = []
    if selected_genre:
        # songs in the genre
        for song in songs:
            if song['genre'] == selected_genre:
                artist = get_artist_by_id(song['artist_id'])
                genre_songs.append({
                    'song_id': song['song_id'],
                    'title': song['title'],
                    'artist_name': artist['name'] if artist else 'Unknown',
                    'duration': song['duration']
                })

        # artists who have songs in genre
        artists_in_genre_ids = set(s['artist_id'] for s in songs if s['genre'] == selected_genre)
        for artist in artists:
            if artist['artist_id'] in artists_in_genre_ids:
                genre_artists.append({
                    'artist_id': artist['artist_id'],
                    'name': artist['name'],
                    'genre': artist['genre']
                })

    return render_template('genres.html', genres=genres, selected_genre=selected_genre,
                           genre_songs=genre_songs, genre_artists=genre_artists)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
