from flask import Flask, render_template, request, redirect, url_for, abort
import os

app = Flask(__name__)

# Data file paths
DATA_DIR = 'data'
SONGS_FILE = os.path.join(DATA_DIR, 'songs.txt')
ARTISTS_FILE = os.path.join(DATA_DIR, 'artists.txt')
ALBUMS_FILE = os.path.join(DATA_DIR, 'albums.txt')
GENRES_FILE = os.path.join(DATA_DIR, 'genres.txt')
PLAYLISTS_FILE = os.path.join(DATA_DIR, 'playlists.txt')
PLAYLIST_SONGS_FILE = os.path.join(DATA_DIR, 'playlist_songs.txt')

# Data loading functions

def load_songs():
    songs = []
    if not os.path.exists(SONGS_FILE):
        return songs
    with open(SONGS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
                continue
            song = {
                'song_id': parts[0],
                'title': parts[1],
                'artist_id': parts[2],
                'album_id': parts[3],
                'genre_id': parts[4],
                'year': parts[5]
            }
            songs.append(song)
    return songs


def load_artists():
    artists = []
    if not os.path.exists(ARTISTS_FILE):
        return artists
    with open(ARTISTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 2:
                continue
            artist = {
                'artist_id': parts[0],
                'name': parts[1]
            }
            artists.append(artist)
    return artists


def load_albums():
    albums = []
    if not os.path.exists(ALBUMS_FILE):
        return albums
    with open(ALBUMS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 3:
                continue
            album = {
                'album_id': parts[0],
                'title': parts[1],
                'artist_id': parts[2]
            }
            albums.append(album)
    return albums


def load_genres():
    genres = []
    if not os.path.exists(GENRES_FILE):
        return genres
    with open(GENRES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 2:
                continue
            genre = {
                'genre_id': parts[0],
                'name': parts[1]
            }
            genres.append(genre)
    return genres


def load_playlists():
    playlists = []
    if not os.path.exists(PLAYLISTS_FILE):
        return playlists
    with open(PLAYLISTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 2:
                continue
            playlist = {
                'playlist_id': parts[0],
                'name': parts[1]
            }
            playlists.append(playlist)
    return playlists


def load_playlist_songs():
    playlist_songs = []
    if not os.path.exists(PLAYLIST_SONGS_FILE):
        return playlist_songs
    with open(PLAYLIST_SONGS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 2:
                continue
            ps = {
                'playlist_id': parts[0],
                'song_id': parts[1]
            }
            playlist_songs.append(ps)
    return playlist_songs

# Data saving functions

def save_playlists(playlists):
    with open(PLAYLISTS_FILE, 'w', encoding='utf-8') as f:
        for pl in playlists:
            f.write(f"{pl['playlist_id']}|{pl['name']}\n")


def save_playlist_songs(playlist_songs):
    with open(PLAYLIST_SONGS_FILE, 'w', encoding='utf-8') as f:
        for ps in playlist_songs:
            f.write(f"{ps['playlist_id']}|{ps['song_id']}\n")

# Helper functions

def get_next_playlist_id(playlists):
    max_id = 0
    for pl in playlists:
        try:
            num = int(pl['playlist_id'])
            if num > max_id:
                max_id = num
        except ValueError:
            continue
    return str(max_id + 1)


def get_song_by_id(songs, song_id):
    for song in songs:
        if song['song_id'] == song_id:
            return song
    return None


def get_playlist_by_id(playlists, playlist_id):
    for pl in playlists:
        if pl['playlist_id'] == playlist_id:
            return pl
    return None

# Routes

@app.route('/')
def root():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()
    genres = load_genres()
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()

    # Aggregate statistics
    total_songs = len(songs)
    total_artists = len(artists)
    total_albums = len(albums)
    total_genres = len(genres)
    total_playlists = len(playlists)

    return render_template('dashboard.html', total_songs=total_songs, total_artists=total_artists, total_albums=total_albums, total_genres=total_genres, total_playlists=total_playlists)

@app.route('/songs')
def songs():
    songs = load_songs()
    artists = {artist['artist_id']: artist['name'] for artist in load_artists()}
    albums = {album['album_id']: album['title'] for album in load_albums()}
    genres = {genre['genre_id']: genre['name'] for genre in load_genres()}

    # enrich songs with artist name, album title, genre name
    for song in songs:
        song['artist_name'] = artists.get(song['artist_id'], 'Unknown')
        song['album_title'] = albums.get(song['album_id'], 'Unknown')
        song['genre_name'] = genres.get(song['genre_id'], 'Unknown')

    return render_template('songs.html', songs=songs)

@app.route('/playlists')
def playlists():
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()
    songs = load_songs()
    # Map song_id to song title for quick reference
    song_map = {song['song_id']: song['title'] for song in songs}

    # Build playlists with their songs
    playlists_data = []
    for pl in playlists:
        pl_songs = [song_map.get(ps['song_id'], 'Unknown') for ps in playlist_songs if ps['playlist_id'] == pl['playlist_id']]
        playlists_data.append({'playlist_id': pl['playlist_id'], 'name': pl['name'], 'songs': pl_songs})

    return render_template('playlists.html', playlists=playlists_data)

@app.route('/playlists/<playlist_id>', methods=['GET', 'POST'])
def playlist_detail(playlist_id):
    playlists = load_playlists()
    playlist = get_playlist_by_id(playlists, playlist_id)
    if playlist is None:
        abort(404)

    playlist_songs = load_playlist_songs()
    songs = load_songs()

    # Handle form submissions
    if request.method == 'POST':
        action = request.form.get('action')
        selected_song_id = request.form.get('song_id')
        if action == 'add':
            # Add song to playlist if not already there
            if selected_song_id and all(ps['song_id'] != selected_song_id or ps['playlist_id'] != playlist_id for ps in playlist_songs):
                playlist_songs.append({'playlist_id': playlist_id, 'song_id': selected_song_id})
                save_playlist_songs(playlist_songs)
        elif action == 'remove':
            # Remove song from playlist
            if selected_song_id:
                playlist_songs = [ps for ps in playlist_songs if not (ps['playlist_id'] == playlist_id and ps['song_id'] == selected_song_id)]
                save_playlist_songs(playlist_songs)
        # Redirect to GET after POST
        return redirect(url_for('playlist_detail', playlist_id=playlist_id))

    # For GET request, show playlist details
    song_map = {song['song_id']: song for song in songs}
    playlist_songs_list = [song_map[ps['song_id']] for ps in playlist_songs if ps['playlist_id'] == playlist_id and ps['song_id'] in song_map]
    # Songs not in playlist for adding
    songs_not_in_playlist = [song for song in songs if all(ps['song_id'] != song['song_id'] or ps['playlist_id'] != playlist_id for ps in playlist_songs)]

    return render_template('playlist_detail.html', playlist=playlist, playlist_songs=playlist_songs_list, songs_not_in_playlist=songs_not_in_playlist)

@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            # Flash or display error should template allow
            return render_template('create_playlist.html', error='Name is required')
        playlists = load_playlists()
        new_id = get_next_playlist_id(playlists)
        playlists.append({'playlist_id': new_id, 'name': name})
        save_playlists(playlists)
        return redirect(url_for('playlists'))
    return render_template('create_playlist.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
