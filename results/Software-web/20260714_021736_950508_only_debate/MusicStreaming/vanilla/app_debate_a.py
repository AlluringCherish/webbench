from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)
DATA_DIR = 'data'

# Data loading functions

def read_songs():
    songs = []
    path = os.path.join(DATA_DIR, 'songs.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 8:
                    song = {
                        'song_id': int(fields[0]),
                        'title': fields[1],
                        'artist_id': int(fields[2]),
                        'album_id': int(fields[3]),
                        'genre': fields[4],
                        'duration': int(fields[5]),
                        'release_date': fields[6],
                        'play_count': int(fields[7])
                    }
                    songs.append(song)
    return songs

def read_artists():
    artists = []
    path = os.path.join(DATA_DIR, 'artists.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 5:
                    artist = {
                        'artist_id': int(fields[0]),
                        'name': fields[1],
                        'genre': fields[2],
                        'country': fields[3],
                        'formation_year': fields[4]
                    }
                    artists.append(artist)
    return artists

def read_albums():
    albums = []
    path = os.path.join(DATA_DIR, 'albums.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 6:
                    album = {
                        'album_id': int(fields[0]),
                        'title': fields[1],
                        'artist_id': int(fields[2]),
                        'release_year': fields[3],
                        'total_songs': int(fields[4]),
                        'genre': fields[5]
                    }
                    albums.append(album)
    return albums

def read_genres():
    genres = []
    path = os.path.join(DATA_DIR, 'genres.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 3:
                    genre = {
                        'genre_id': int(fields[0]),
                        'genre_name': fields[1],
                        'description': fields[2]
                    }
                    genres.append(genre)
    return genres

def read_playlists():
    playlists = []
    path = os.path.join(DATA_DIR, 'playlists.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 5:
                    playlist = {
                        'playlist_id': int(fields[0]),
                        'title': fields[1],
                        'description': fields[2],
                        'creation_date': fields[3],
                        'total_songs': int(fields[4])
                    }
                    playlists.append(playlist)
    return playlists

def read_playlist_songs():
    playlist_songs = []
    path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 4:
                    pls = {
                        'playlist_song_id': int(fields[0]),
                        'playlist_id': int(fields[1]),
                        'song_id': int(fields[2]),
                        'added_date': fields[3]
                    }
                    playlist_songs.append(pls)
    return playlist_songs

# Data writing

def write_playlists(playlists):
    path = os.path.join(DATA_DIR, 'playlists.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for p in playlists:
            line = '|'.join([str(p['playlist_id']), p['title'], p['description'], p['creation_date'], str(p['total_songs'])])
            f.write(line + '\n')

def write_playlist_songs(playlist_songs):
    path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for ps in playlist_songs:
            line = '|'.join([str(ps['playlist_song_id']), str(ps['playlist_id']), str(ps['song_id']), ps['added_date']])
            f.write(line + '\n')

# Helpers

def get_next_id(items, key):
    if not items:
        return 1
    return max(item[key] for item in items) + 1

def find_artist_by_id(artist_id):
    artists = read_artists()
    for artist in artists:
        if artist['artist_id'] == artist_id:
            return artist
    return None

def find_album_by_id(album_id):
    albums = read_albums()
    for album in albums:
        if album['album_id'] == album_id:
            return album
    return None

def find_song_by_id(song_id):
    songs = read_songs()
    for song in songs:
        if song['song_id'] == song_id:
            return song
    return None

def find_playlist_by_id(playlist_id):
    playlists = read_playlists()
    for playlist in playlists:
        if playlist['playlist_id'] == playlist_id:
            return playlist
    return None

# Routes

@app.route('/')
def dashboard():
    songs = read_songs()
    artists = read_artists()
    featured_songs = sorted(songs, key=lambda s: s['play_count'], reverse=True)[:5]
    trending_artists = sorted(artists, key=lambda a: int(a['formation_year']), reverse=True)[:5]
    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)

@app.route('/songs', methods=['GET', 'POST'])
def songs():
    songs = read_songs()
    genres = [g['genre_name'] for g in read_genres()]
    search_query = ''
    genre_filter = ''

    if request.method == 'POST':
        # Spec does not mention a playlist selection for adding songs, so no action
        return redirect(url_for('songs'))

    else:
        search_query = request.args.get('search_query', '')
        genre_filter = request.args.get('genre_filter', '')
        filtered_songs = songs
        if search_query:
            filtered_songs = [s for s in filtered_songs if search_query.lower() in s['title'].lower()]
        if genre_filter:
            filtered_songs = [s for s in filtered_songs if s['genre'] == genre_filter]
        return render_template('song_catalog.html', songs=filtered_songs, genres=genres, search_query=search_query, genre_filter=genre_filter)

@app.route('/songs/<int:song_id>')
def song_details(song_id):
    song = find_song_by_id(song_id)
    if not song:
        return "Song not found", 404
    artist = find_artist_by_id(song['artist_id'])
    album = find_album_by_id(song['album_id'])
    return render_template('song_details.html', song=song, artist=artist, album=album)

@app.route('/playlists')
def playlists():
    playlists = read_playlists()
    return render_template('playlists.html', playlists=playlists)

@app.route('/playlists/<int:playlist_id>', methods=['GET', 'POST'])
def playlist_details(playlist_id):
    playlist = find_playlist_by_id(playlist_id)
    if not playlist:
        return "Playlist not found", 404
    playlist_songs = [pls for pls in read_playlist_songs() if pls['playlist_id'] == playlist_id]
    songs = []
    all_songs = read_songs()
    for pls in playlist_songs:
        song = next((s for s in all_songs if s['song_id'] == pls['song_id']), None)
        if song:
            songs.append(song)

    if request.method == 'POST':
        if 'remove_song_button' in request.form:
            song_id = int(request.form.get('song_id', 0))
            playlist_songs_full = read_playlist_songs()
            playlist_songs_full = [pls for pls in playlist_songs_full if not (pls['playlist_id'] == playlist_id and pls['song_id'] == song_id)]
            write_playlist_songs(playlist_songs_full)
            playlist['total_songs'] = max(0, playlist['total_songs'] - 1)
            playlists = read_playlists()
            for p in playlists:
                if p['playlist_id'] == playlist_id:
                    p['total_songs'] = playlist['total_songs']
            write_playlists(playlists)
            return redirect(url_for('playlist_details', playlist_id=playlist_id))
        elif 'delete_playlist_button' in request.form:
            playlists = read_playlists()
            playlists = [p for p in playlists if p['playlist_id'] != playlist_id]
            write_playlists(playlists)
            playlist_songs_full = read_playlist_songs()
            playlist_songs_full = [pls for pls in playlist_songs_full if pls['playlist_id'] != playlist_id]
            write_playlist_songs(playlist_songs_full)
            return redirect(url_for('playlists'))

    return render_template('playlist_details.html', playlist=playlist, songs=songs)

@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist():
    errors = None
    if request.method == 'POST':
        name = request.form.get('playlist_name', '').strip()
        description = request.form.get('playlist_description', '').strip()
        if not name:
            errors = ['Playlist name is required.']
        else:
            playlists = read_playlists()
            new_id = get_next_id(playlists, 'playlist_id')
            creation_date = datetime.now().strftime('%Y-%m-%d')
            new_playlist = {
                'playlist_id': new_id,
                'title': name,
                'description': description,
                'creation_date': creation_date,
                'total_songs': 0
            }
            playlists.append(new_playlist)
            write_playlists(playlists)
            return redirect(url_for('playlists'))
    return render_template('create_playlist.html', errors=errors)

@app.route('/albums', methods=['GET', 'POST'])
def albums():
    albums = read_albums()
    search_albums = ''
    sort_albums = ''
    if request.method == 'POST':
        search_albums = request.form.get('search_albums', '')
        sort_albums = request.form.get('sort_albums', '')
    else:
        search_albums = request.args.get('search_albums', '')
        sort_albums = request.args.get('sort_albums', '')
    filtered_albums = albums
    if search_albums:
        filtered_albums = [a for a in filtered_albums if search_albums.lower() in a['title'].lower()]
    if sort_albums:
        if sort_albums == 'title':
            filtered_albums = sorted(filtered_albums, key=lambda a: a['title'])
        elif sort_albums == 'release_year':
            filtered_albums = sorted(filtered_albums, key=lambda a: a['release_year'])

    return render_template('albums.html', albums=filtered_albums, search_albums=search_albums, sort_albums=sort_albums)

@app.route('/albums/<int:album_id>', methods=['GET', 'POST'])
def album_details(album_id):
    album = find_album_by_id(album_id)
    if not album:
        return "Album not found", 404
    songs = [s for s in read_songs() if s['album_id'] == album_id]

    if request.method == 'POST':
        # No playlist selection UI in spec, so ignore add to playlist
        return redirect(url_for('album_details', album_id=album_id))

    return render_template('album_details.html', album=album, songs=songs)

@app.route('/artists', methods=['GET', 'POST'])
def artists():
    artists = read_artists()
    search_artists = ''
    artists_sort = ''
    if request.method == 'POST':
        search_artists = request.form.get('search_artists', '')
        artists_sort = request.form.get('artists_sort', '')
    else:
        search_artists = request.args.get('search_artists', '')
        artists_sort = request.args.get('artists_sort', '')
    filtered_artists = artists
    if search_artists:
        filtered_artists = [a for a in filtered_artists if search_artists.lower() in a['name'].lower()]
    if artists_sort:
        if artists_sort == 'name':
            filtered_artists = sorted(filtered_artists, key=lambda a: a['name'])
        elif artists_sort == 'formation_year':
            filtered_artists = sorted(filtered_artists, key=lambda a: int(a['formation_year']))

    return render_template('artists.html', artists=filtered_artists, search_artists=search_artists, artists_sort=artists_sort)

@app.route('/artists/<int:artist_id>')
def artist_profile(artist_id):
    artist = find_artist_by_id(artist_id)
    if not artist:
        return "Artist not found", 404
    songs = [s for s in read_songs() if s['artist_id'] == artist_id]
    albums = [a for a in read_albums() if a['artist_id'] == artist_id]
    return render_template('artist_profile.html', artist=artist, songs=songs, albums=albums)

@app.route('/genres', methods=['GET', 'POST'])
def genres_view():
    genres = [g['genre_name'] for g in read_genres()]
    selected_genre = ''
    genre_songs = []
    genre_artists = []
    if request.method == 'POST':
        selected_genre = request.form.get('selected_genre', '')
        songs = read_songs()
        artists = read_artists()
        genre_songs = [s for s in songs if s['genre'] == selected_genre]
        genre_artists = [a for a in artists if a['genre'] == selected_genre]
    return render_template('genres.html', genres=genres, selected_genre=selected_genre, genre_songs=genre_songs, genre_artists=genre_artists)

if __name__ == '__main__':
    app.run(debug=True)
