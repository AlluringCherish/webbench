from flask import Flask, render_template, request, redirect, url_for, abort
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = 'data'

# Utility Functions for data loading and saving

def load_songs():
    songs = []
    file_path = os.path.join(DATA_DIR, 'songs.txt')
    if not os.path.exists(file_path):
        return songs
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
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
            except ValueError:
                continue
    return songs

def load_artists():
    artists = []
    file_path = os.path.join(DATA_DIR, 'artists.txt')
    if not os.path.exists(file_path):
        return artists
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            try:
                artist = {
                    'artist_id': int(parts[0]),
                    'name': parts[1],
                    'genre': parts[2],
                    'country': parts[3],
                    'formation_year': int(parts[4])
                }
                artists.append(artist)
            except ValueError:
                continue
    return artists

def load_albums():
    albums = []
    file_path = os.path.join(DATA_DIR, 'albums.txt')
    if not os.path.exists(file_path):
        return albums
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            try:
                album = {
                    'album_id': int(parts[0]),
                    'title': parts[1],
                    'artist_id': int(parts[2]),
                    'release_year': int(parts[3]),
                    'total_songs': int(parts[4]),
                    'genre': parts[5]
                }
                albums.append(album)
            except ValueError:
                continue
    return albums

def load_genres():
    genres = []
    file_path = os.path.join(DATA_DIR, 'genres.txt')
    if not os.path.exists(file_path):
        return genres
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            try:
                genre = {
                    'genre_id': int(parts[0]),
                    'genre_name': parts[1],
                    'description': parts[2]
                }
                genres.append(genre)
            except ValueError:
                continue
    return genres

def load_playlists():
    playlists = []
    file_path = os.path.join(DATA_DIR, 'playlists.txt')
    if not os.path.exists(file_path):
        return playlists
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            try:
                playlist = {
                    'playlist_id': int(parts[0]),
                    'title': parts[1],
                    'description': parts[2],
                    'creation_date': parts[3],
                    'total_songs': int(parts[4])
                }
                playlists.append(playlist)
            except ValueError:
                continue
    return playlists

def load_playlist_songs():
    playlist_songs = []
    file_path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    if not os.path.exists(file_path):
        return playlist_songs
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 4:
                continue
            try:
                psong = {
                    'playlist_song_id': int(parts[0]),
                    'playlist_id': int(parts[1]),
                    'song_id': int(parts[2]),
                    'added_date': parts[3]
                }
                playlist_songs.append(psong)
            except ValueError:
                continue
    return playlist_songs

def save_playlists(playlists):
    file_path = os.path.join(DATA_DIR, 'playlists.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        for p in playlists:
            line = f"{p['playlist_id']}|{p['title']}|{p['description']}|{p['creation_date']}|{p['total_songs']}\n"
            f.write(line)

def save_playlist_songs(playlist_songs):
    file_path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        for ps in playlist_songs:
            line = f"{ps['playlist_song_id']}|{ps['playlist_id']}|{ps['song_id']}|{ps['added_date']}\n"
            f.write(line)

# Helper: Map artist_id to artist dict

def map_artists_by_id():
    artists = load_artists()
    return {artist['artist_id']: artist for artist in artists}

# Helper: Map album_id to album dict

def map_albums_by_id():
    albums = load_albums()
    return {album['album_id']: album for album in albums}

# Helper: Map song_id to song dict

def map_songs_by_id():
    songs = load_songs()
    return {song['song_id']: song for song in songs}

# Root route redirect to dashboard
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

# /dashboard route GET
@app.route('/dashboard')
def dashboard_page():
    songs = load_songs()
    artists = load_artists()

    artists_map = {artist['artist_id']: artist for artist in artists}
    albums_map = map_albums_by_id()

    # Featured songs: Top 5 by play_count desc
    sorted_songs = sorted(songs, key=lambda s: s['play_count'], reverse=True)
    featured_songs = []
    for s in sorted_songs[:5]:
        artist_name = artists_map.get(s['artist_id'], {}).get('name', 'Unknown Artist')
        album_name = albums_map.get(s['album_id'], {}).get('title', 'Unknown Album')
        featured_songs.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_name,
            'album_name': album_name,
            'genre': s['genre'],
            'duration': s['duration']
        })

    # Trending artists: Top 5 by sum of play counts of their songs
    artist_play_counts = {artist['artist_id']: 0 for artist in artists}
    for s in songs:
        if s['artist_id'] in artist_play_counts:
            artist_play_counts[s['artist_id']] += s['play_count']

    trending_artists_sorted = sorted(artists, key=lambda a: artist_play_counts.get(a['artist_id'],0), reverse=True)[:5]
    trending_artists = []
    for a in trending_artists_sorted:
        trending_artists.append({
            'artist_id': a['artist_id'],
            'name': a['name'],
            'genre': a['genre']
        })

    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)

# /songs GET - song catalog page
@app.route('/songs', methods=['GET'])
def song_catalog():
    songs = load_songs()
    artists_map = map_artists_by_id()
    albums_map = map_albums_by_id()

    # Compose songs with required context keys
    songs_context = []
    for s in songs:
        artist_name = artists_map.get(s['artist_id'], {}).get('name', 'Unknown Artist')
        album_name = albums_map.get(s['album_id'], {}).get('title', 'Unknown Album')
        songs_context.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_name,
            'album_name': album_name,
            'genre': s['genre'],
            'duration': s['duration']
        })

    genres = sorted(set(s['genre'] for s in songs))

    return render_template('song_catalog.html', songs=songs_context, genres=genres)

# /songs/search POST - search songs
@app.route('/songs/search', methods=['POST'])
def search_songs():
    # Fix backend to accept form names matching frontend: 'search_query' and 'genre_filter'
    title_query = request.form.get('search_query', '').strip().lower()
    genre_filter = request.form.get('genre_filter', '').strip()

    songs = load_songs()
    artists_map = map_artists_by_id()
    albums_map = map_albums_by_id()

    filtered_songs = []

    for s in songs:
        artist_name = artists_map.get(s['artist_id'], {}).get('name', '')
        album_name = albums_map.get(s['album_id'], {}).get('title', '')
        # Filter by title
        if title_query and title_query not in s['title'].lower():
            continue
        # Filter by genre
        if genre_filter and genre_filter != s['genre']:
            continue
        filtered_songs.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_name,
            'album_name': album_name,
            'genre': s['genre'],
            'duration': s['duration']
        })

    genres = sorted(set(s['genre'] for s in songs))

    return render_template('song_catalog.html', songs=filtered_songs, genres=genres)

# /song/<int:song_id> GET - song details
@app.route('/song/<int:song_id>', methods=['GET'])
def song_details(song_id):
    songs_map = map_songs_by_id()
    song = songs_map.get(song_id)
    if not song:
        abort(404)

    artists_map = map_artists_by_id()
    albums_map = map_albums_by_id()

    artist_name = artists_map.get(song['artist_id'], {}).get('name', 'Unknown Artist')
    album_name = albums_map.get(song['album_id'], {}).get('title', 'Unknown Album')

    song_context = {
        'song_id': song['song_id'],
        'title': song['title'],
        'artist_name': artist_name,
        'album_name': album_name,
        'genre': song['genre'],
        'duration': song['duration'],
        'release_date': song['release_date']
    }
    return render_template('song_details.html', song=song_context)

# /playlists GET - list all playlists
@app.route('/playlists', methods=['GET'])
def playlists_page():
    playlists = load_playlists()

    playlist_songs = load_playlist_songs()
    playlist_song_counts = {}
    for psong in playlist_songs:
        pid = psong['playlist_id']
        playlist_song_counts[pid] = playlist_song_counts.get(pid, 0) + 1

    playlists_context = []
    for p in playlists:
        count = playlist_song_counts.get(p['playlist_id'], 0)
        playlists_context.append({
            'playlist_id': p['playlist_id'],
            'title': p['title'],
            'description': p['description'],
            'total_songs': count
        })

    return render_template('playlists.html', playlists=playlists_context)

# /playlist/<int:playlist_id> GET - playlist details
@app.route('/playlist/<int:playlist_id>', methods=['GET'])
def playlist_details(playlist_id):
    playlists = load_playlists()
    playlist = next((p for p in playlists if p['playlist_id'] == playlist_id), None)
    if not playlist:
        abort(404)

    playlist_songs = load_playlist_songs()
    psongs = [ps for ps in playlist_songs if ps['playlist_id'] == playlist_id]
    song_ids = [ps['song_id'] for ps in psongs]

    songs_map = map_songs_by_id()
    artists_map = map_artists_by_id()

    songs_context = []
    for sid in song_ids:
        song = songs_map.get(sid)
        if song:
            artist_name = artists_map.get(song['artist_id'], {}).get('name', 'Unknown Artist')
            songs_context.append({
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

    return render_template('playlist_details.html', playlist=playlist_context, songs=songs_context)

# /playlist/create GET - create playlist page
@app.route('/playlist/create', methods=['GET'])
def create_playlist():
    return render_template('create_playlist.html')

# /playlist/save POST - save playlist
@app.route('/playlist/save', methods=['POST'])
def save_playlist():
    # Fix: Accept form keys as per frontend form
    title = request.form.get('playlist_name', '').strip()
    description = request.form.get('playlist_description', '').strip()

    if not title or not description:
        return redirect(url_for('create_playlist'))

    playlists = load_playlists()
    existing_ids = [p['playlist_id'] for p in playlists]
    new_id = max(existing_ids) + 1 if existing_ids else 1
    creation_date = datetime.now().strftime('%Y-%m-%d')

    new_playlist = {
        'playlist_id': new_id,
        'title': title,
        'description': description,
        'creation_date': creation_date,
        'total_songs': 0
    }
    playlists.append(new_playlist)
    save_playlists(playlists)

    return redirect(url_for('playlists_page'))

# /albums GET - list albums
@app.route('/albums', methods=['GET'])
def albums_page():
    albums = load_albums()
    artists_map = map_artists_by_id()

    albums_context = []
    for a in albums:
        artist_name = artists_map.get(a['artist_id'], {}).get('name', 'Unknown Artist')
        albums_context.append({
            'album_id': a['album_id'],
            'title': a['title'],
            'artist_name': artist_name,
            'release_year': a['release_year'],
            'genre': a['genre']
        })

    return render_template('albums.html', albums=albums_context)

# /album/<int:album_id> GET
@app.route('/album/<int:album_id>', methods=['GET'])
def album_details(album_id):
    albums = load_albums()
    album = next((a for a in albums if a['album_id'] == album_id), None)
    if not album:
        abort(404)

    songs = load_songs()
    album_songs = [s for s in songs if s['album_id'] == album_id]
    songs_context = [{'song_id': s['song_id'], 'title': s['title'], 'duration': s['duration']} for s in album_songs]

    artists_map = map_artists_by_id()
    artist_name = artists_map.get(album['artist_id'], {}).get('name', 'Unknown Artist')

    album_context = {
        'album_id': album['album_id'],
        'title': album['title'],
        'artist_name': artist_name,
        'release_year': album['release_year']
    }

    return render_template('album_details.html', album=album_context, songs=songs_context)

# /artists GET - list artists
@app.route('/artists', methods=['GET'])
def artists_page():
    artists = load_artists()

    artists_context = []
    for a in artists:
        artists_context.append({
            'artist_id': a['artist_id'],
            'name': a['name'],
            'genre': a['genre'],
            'country': a['country']
        })

    return render_template('artists.html', artists=artists_context)

# /artist/<int:artist_id> GET - artist profile
@app.route('/artist/<int:artist_id>', methods=['GET'])
def artist_profile(artist_id):
    artists = load_artists()
    artist = next((a for a in artists if a['artist_id'] == artist_id), None)
    if not artist:
        abort(404)

    songs = load_songs()
    artist_songs = [s for s in songs if s['artist_id'] == artist_id]
    songs_context = [{'song_id': s['song_id'], 'title': s['title']} for s in artist_songs]

    artist_context = {
        'artist_id': artist['artist_id'],
        'name': artist['name'],
        'genre': artist['genre'],
        'country': artist['country'],
        'formation_year': artist['formation_year']
    }

    return render_template('artist_profile.html', artist=artist_context, songs=songs_context)

# /genres GET - genres page
@app.route('/genres', methods=['GET'])
def genres_page():
    genres = load_genres()

    songs = load_songs()
    artists = load_artists()

    # Featured songs: top 5 by play_count
    sorted_songs = sorted(songs, key=lambda s: s['play_count'], reverse=True)[:5]
    featured_songs = [{'song_id': s['song_id'], 'title': s['title']} for s in sorted_songs]

    # Featured artists: top 5 by total play_count of songs
    artist_play_counts = {a['artist_id']: 0 for a in artists}
    for s in songs:
        if s['artist_id'] in artist_play_counts:
            artist_play_counts[s['artist_id']] += s['play_count']

    sorted_artists = sorted(artists, key=lambda a: artist_play_counts.get(a['artist_id'], 0), reverse=True)[:5]
    featured_artists = [{'artist_id': a['artist_id'], 'name': a['name']} for a in sorted_artists]

    return render_template('genres.html', genres=genres, featured_songs=featured_songs, featured_artists=featured_artists)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
