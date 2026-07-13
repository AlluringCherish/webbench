from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)
DATA_DIR = 'data'

# Utility functions to load and save data

def load_songs():
    songs = []
    filepath = os.path.join(DATA_DIR, 'songs.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                songs.append({
                    'song_id': parts[0],
                    'title': parts[1],
                    'artist_id': parts[2],
                    'album_id': parts[3],
                    'genre': parts[4],
                    'duration': int(parts[5]),
                    'release_date': parts[6],
                    'play_count': int(parts[7])
                })
    return songs

def load_artists():
    artists = []
    filepath = os.path.join(DATA_DIR, 'artists.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                artists.append({
                    'artist_id': parts[0],
                    'name': parts[1],
                    'genre': parts[2],
                    'country': parts[3],
                    'formation_year': parts[4]
                })
    return artists

def load_albums():
    albums = []
    filepath = os.path.join(DATA_DIR, 'albums.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                albums.append({
                    'album_id': parts[0],
                    'title': parts[1],
                    'artist_id': parts[2],
                    'release_year': parts[3],
                    'total_songs': int(parts[4]),
                    'genre': parts[5]
                })
    return albums

def load_genres():
    genres = []
    filepath = os.path.join(DATA_DIR, 'genres.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                genres.append({
                    'genre_id': parts[0],
                    'genre_name': parts[1],
                    'description': parts[2]
                })
    return genres

def load_playlists():
    playlists = []
    filepath = os.path.join(DATA_DIR, 'playlists.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                playlists.append({
                    'playlist_id': parts[0],
                    'title': parts[1],
                    'description': parts[2],
                    'creation_date': parts[3],
                    'total_songs': int(parts[4])
                })
    return playlists

def load_playlist_songs():
    playlist_songs = []
    filepath = os.path.join(DATA_DIR, 'playlist_songs.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                playlist_songs.append({
                    'playlist_song_id': parts[0],
                    'playlist_id': parts[1],
                    'song_id': parts[2],
                    'added_date': parts[3]
                })
    return playlist_songs


def save_playlists(playlists):
    filepath = os.path.join(DATA_DIR, 'playlists.txt')
    with open(filepath, 'w') as f:
        for pl in playlists:
            line = f"{pl['playlist_id']}|{pl['title']}|{pl['description']}|{pl['creation_date']}|{pl['total_songs']}" + "\n"
            f.write(line)

def save_playlist_songs(playlist_songs):
    filepath = os.path.join(DATA_DIR, 'playlist_songs.txt')
    with open(filepath, 'w') as f:
        for pls in playlist_songs:
            line = f"{pls['playlist_song_id']}|{pls['playlist_id']}|{pls['song_id']}|{pls['added_date']}" + "\n"
            f.write(line)


# Helper to find next available ID

def next_id(items, id_field):
    max_id = 0
    for item in items:
        try:
            val = int(item[id_field])
            if val > max_id:
                max_id = val
        except:
            pass
    return str(max_id + 1)


# Dashboard Page
@app.route('/')
def dashboard():
    songs = load_songs()
    artists = load_artists()

    # Featured songs, top 5 by play_count
    featured_songs_raw = sorted(songs, key=lambda x: x['play_count'], reverse=True)[:5]

    # Attach artist name for template
    featured_songs = []
    artist_lookup = {a['artist_id']: a['name'] for a in artists}
    for s in featured_songs_raw:
        song = s.copy()
        song['artist_name'] = artist_lookup.get(s['artist_id'], 'Unknown')
        featured_songs.append(song)

    return render_template('dashboard.html',
                           featured_songs=featured_songs)


# Song Catalog Page
@app.route('/catalog', methods=['GET', 'POST'])
def song_catalog():
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()
    genres = load_genres()
    playlists = load_playlists()

    search_query = request.args.get('search', '').strip().lower()
    genre_filter = request.args.get('genre', '').strip()

    # Filtering
    filtered_songs = []
    for song in songs:
        title = song['title'].lower()
        # artist name lookup
        artist_name = next((a['name'].lower() for a in artists if a['artist_id'] == song['artist_id']), '')
        album_title = next((a['title'].lower() for a in albums if a['album_id'] == song['album_id']), '')

        if search_query:
            if search_query not in title and search_query not in artist_name and search_query not in album_title:
                continue
        if genre_filter and genre_filter != 'All' and song['genre'] != genre_filter:
            continue
        filtered_songs.append(song)

    return render_template('catalog.html', songs=filtered_songs, genres=genres, selected_genre=genre_filter, search_query=search_query, artists=artists, albums=albums, playlists=playlists)


# Song Details Page
@app.route('/song/<song_id>')
def song_details(song_id):
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()
    song = next((s for s in songs if s['song_id'] == song_id), None)
    if not song:
        return 'Song not found', 404

    artist = next((a for a in artists if a['artist_id'] == song['artist_id']), None)
    album = next((a for a in albums if a['album_id'] == song['album_id']), None)

    return render_template('song_details.html',
                           song=song,
                           artist=artist,
                           album=album)


# Playlist Page
@app.route('/playlists')
def playlists():
    playlists = load_playlists()
    return render_template('playlists.html', playlists=playlists)


# Playlist Details Page
@app.route('/playlist/<playlist_id>')
def playlist_details(playlist_id):
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()
    songs = load_songs()
    artists = load_artists()

    playlist = next((pl for pl in playlists if pl['playlist_id'] == playlist_id), None)
    if not playlist:
        return 'Playlist not found', 404

    # Songs in playlist
    playlist_song_entries = [ps for ps in playlist_songs if ps['playlist_id'] == playlist_id]
    # Include song details
    songs_in_playlist = []
    for entry in playlist_song_entries:
        song = next((s for s in songs if s['song_id'] == entry['song_id']), None)
        if song:
            artist = next((a for a in artists if a['artist_id'] == song['artist_id']), None)
            songs_in_playlist.append({
                'playlist_song_id': entry['playlist_song_id'],
                'song_id': song['song_id'],
                'title': song['title'],
                'artist_name': artist['name'] if artist else '',
                'duration': song['duration']
            })

    return render_template('playlist_details.html', playlist=playlist, songs_in_playlist=songs_in_playlist)


# Remove song from playlist
@app.route('/playlist/<playlist_id>/remove_song/<song_id>', methods=['POST'])
def remove_song_from_playlist(playlist_id, song_id):
    playlist_songs = load_playlist_songs()
    playlists = load_playlists()

    playlist_songs = [ps for ps in playlist_songs if not(ps['playlist_id'] == playlist_id and ps['song_id'] == song_id)]

    # Update playlist total songs count
    for pl in playlists:
        if pl['playlist_id'] == playlist_id:
            pl['total_songs'] = sum(1 for ps in playlist_songs if ps['playlist_id'] == playlist_id)

    save_playlist_songs(playlist_songs)
    save_playlists(playlists)

    return redirect(url_for('playlist_details', playlist_id=playlist_id))


# Delete entire playlist
@app.route('/playlist/<playlist_id>/delete', methods=['POST'])
def delete_playlist(playlist_id):
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()

    playlists = [pl for pl in playlists if pl['playlist_id'] != playlist_id]
    playlist_songs = [ps for ps in playlist_songs if ps['playlist_id'] != playlist_id]

    save_playlists(playlists)
    save_playlist_songs(playlist_songs)

    return redirect(url_for('playlists'))


# Create Playlist Page
@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'POST':
        name = request.form.get('playlist_name', '').strip()
        description = request.form.get('playlist_description', '').strip()
        if not name:
            return render_template('create_playlist.html', error='Playlist name is required')

        playlists = load_playlists()
        new_id = next_id(playlists, 'playlist_id')
        creation_date = datetime.today().strftime('%Y-%m-%d')
        new_playlist = {
            'playlist_id': new_id,
            'title': name,
            'description': description,
            'creation_date': creation_date,
            'total_songs': 0
        }
        playlists.append(new_playlist)
        save_playlists(playlists)
        return redirect(url_for('playlists'))

    return render_template('create_playlist.html')


# Album Browse Page
@app.route('/albums')
def albums():
    albums = load_albums()
    artists = load_artists()

    search_query = request.args.get('search', '').strip().lower()
    sort_key = request.args.get('sort', 'Title')

    filtered_albums = []
    for album in albums:
        album_title = album['title'].lower()
        artist_name = next((a['name'].lower() for a in artists if a['artist_id'] == album['artist_id']), '')

        if search_query:
            if search_query not in album_title and search_query not in artist_name:
                continue
        filtered_albums.append(album)

    # sorting
    if sort_key == 'Title':
        filtered_albums.sort(key=lambda x: x['title'])
    elif sort_key == 'Artist':
        filtered_albums.sort(key=lambda x: next((a['name'] for a in artists if a['artist_id'] == x['artist_id']), ''))
    elif sort_key == 'Year':
        filtered_albums.sort(key=lambda x: x['release_year'])

    return render_template('albums.html', albums=filtered_albums, artists=artists, search_query=search_query, sort_key=sort_key)


# Album Details Page
@app.route('/album/<album_id>')
def album_details(album_id):
    albums = load_albums()
    songs = load_songs()
    artists = load_artists()
    playlists = load_playlists()

    album = next((a for a in albums if a['album_id'] == album_id), None)
    if not album:
        return 'Album not found', 404

    album_artist = next((a for a in artists if a['artist_id'] == album['artist_id']), None)

    album_songs = [s for s in songs if s['album_id'] == album_id]

    return render_template('album_details.html', album=album, album_artist=album_artist, album_songs=album_songs, playlists=playlists)

# Add all album songs to playlist
@app.route('/album/<album_id>/add_to_playlist', methods=['POST'])
def add_album_to_playlist(album_id):
    playlist_id = request.form.get('playlist_id', '').strip()
    if not playlist_id:
        return redirect(url_for('album_details', album_id=album_id))

    playlists = load_playlists()
    if not any(pl['playlist_id'] == playlist_id for pl in playlists):
        return redirect(url_for('album_details', album_id=album_id))

    songs = load_songs()
    playlist_songs = load_playlist_songs()

    # Get album songs
    album_song_ids = [s['song_id'] for s in songs if s['album_id'] == album_id]

    # Find max playlist_song_id for new IDs
    max_id = 0
    for ps in playlist_songs:
        try:
            val = int(ps['playlist_song_id'])
            if val > max_id:
                max_id = val
        except:
            pass

    new_id = max_id + 1
    added_date = datetime.today().strftime('%Y-%m-%d')

    for song_id in album_song_ids:
        # Check if song already in playlist
        if any(ps['playlist_id'] == playlist_id and ps['song_id'] == song_id for ps in playlist_songs):
            continue
        playlist_songs.append({
            'playlist_song_id': str(new_id),
            'playlist_id': playlist_id,
            'song_id': song_id,
            'added_date': added_date
        })
        new_id += 1

    # Update playlist total songs
    for pl in playlists:
        if pl['playlist_id'] == playlist_id:
            pl['total_songs'] = sum(1 for ps in playlist_songs if ps['playlist_id'] == playlist_id)

    save_playlist_songs(playlist_songs)
    save_playlists(playlists)

    return redirect(url_for('album_details', album_id=album_id))


# Artist Profile Page
@app.route('/artists')
def artists():
    artists = load_artists()

    search_query = request.args.get('search', '').strip().lower()
    sort_key = request.args.get('sort', 'Name')

    filtered_artists = []
    for artist in artists:
        if search_query and search_query not in artist['name'].lower():
            continue
        filtered_artists.append(artist)

    if sort_key == 'Name':
        filtered_artists.sort(key=lambda x: x['name'])
    elif sort_key == 'Genre':
        filtered_artists.sort(key=lambda x: x['genre'])

    return render_template('artists.html', artists=filtered_artists, search_query=search_query, sort_key=sort_key)


# Genre Exploration Page
@app.route('/genres', methods=['GET', 'POST'])
def genres():
    genres = load_genres()
    songs = load_songs()
    artists = load_artists()

    selected_genre = ''
    genre_songs = []
    genre_artists = []

    if request.method == 'POST':
        selected_genre = request.form.get('selected_genre', '')
        genre_songs = [s for s in songs if s['genre'] == selected_genre]
        # Unique artists in this genre
        artist_ids = {s['artist_id'] for s in genre_songs}
        genre_artists = [a for a in artists if a['artist_id'] in artist_ids]

    return render_template('genres.html', genres=genres, selected_genre=selected_genre, genre_songs=genre_songs, genre_artists=genre_artists)


# Add song to playlist
@app.route('/catalog/add_to_playlist/<song_id>', methods=['POST'])
def add_song_to_playlist(song_id):
    playlist_id = request.form.get('playlist_id', '').strip()
    if not playlist_id:
        # No playlist selected, redirect back
        return redirect(url_for('song_catalog'))

    playlists = load_playlists()
    if not any(pl['playlist_id'] == playlist_id for pl in playlists):
        return redirect(url_for('song_catalog'))

    playlist_songs = load_playlist_songs()
    max_id = 0
    for ps in playlist_songs:
        try:
            val = int(ps['playlist_song_id'])
            if val > max_id:
                max_id = val
        except:
            pass

    # Check if already in playlist
    if any(ps['playlist_id'] == playlist_id and ps['song_id'] == song_id for ps in playlist_songs):
        return redirect(url_for('song_catalog'))

    new_play_id = str(max_id + 1)
    added_date = datetime.today().strftime('%Y-%m-%d')

    playlist_songs.append({
        'playlist_song_id': new_play_id,
        'playlist_id': playlist_id,
        'song_id': song_id,
        'added_date': added_date
    })

    # Update total songs in playlist
    for pl in playlists:
        if pl['playlist_id'] == playlist_id:
            pl['total_songs'] += 1

    save_playlist_songs(playlist_songs)
    save_playlists(playlists)

    return redirect(url_for('song_catalog'))


if __name__ == '__main__':
    app.run(debug=True)
