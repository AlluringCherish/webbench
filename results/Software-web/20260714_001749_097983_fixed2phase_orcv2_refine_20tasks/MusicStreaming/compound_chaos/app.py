from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = 'data'

# Utility functions to load and save data from text files

def load_artists():
    artists = []
    try:
        with open(os.path.join(DATA_DIR, 'artists.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 5:
                    artists.append({
                        'artist_id': parts[0],
                        'name': parts[1],
                        'genre': parts[2],
                        'country': parts[3],
                        'formation_year': parts[4]
                    })
    except FileNotFoundError:
        pass
    return artists

def load_albums():
    albums = []
    try:
        with open(os.path.join(DATA_DIR, 'albums.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 6:
                    albums.append({
                        'album_id': parts[0],
                        'title': parts[1],
                        'artist_id': parts[2],
                        'release_year': int(parts[3]),
                        'total_songs': int(parts[4]),
                        'genre': parts[5]
                    })
    except FileNotFoundError:
        pass
    return albums

def load_songs():
    songs = []
    try:
        with open(os.path.join(DATA_DIR, 'songs.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 8:
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
    except FileNotFoundError:
        pass
    return songs

def load_genres():
    genres = []
    try:
        with open(os.path.join(DATA_DIR, 'genres.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 3:
                    genres.append({
                        'genre_id': parts[0],
                        'genre_name': parts[1],
                        'description': parts[2]
                    })
    except FileNotFoundError:
        pass
    return genres

def load_playlists():
    playlists = []
    try:
        with open(os.path.join(DATA_DIR, 'playlists.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 5:
                    playlists.append({
                        'playlist_id': parts[0],
                        'title': parts[1],
                        'description': parts[2],
                        'creation_date': parts[3],
                        'total_songs': int(parts[4])
                    })
    except FileNotFoundError:
        pass
    return playlists

def load_playlist_songs():
    playlist_songs = []
    try:
        with open(os.path.join(DATA_DIR, 'playlist_songs.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 4:
                    playlist_songs.append({
                        'playlist_song_id': parts[0],
                        'playlist_id': parts[1],
                        'song_id': parts[2],
                        'added_date': parts[3]
                    })
    except FileNotFoundError:
        pass
    return playlist_songs

def save_playlists(playlists):
    with open(os.path.join(DATA_DIR, 'playlists.txt'), 'w', encoding='utf-8') as f:
        for p in playlists:
            line = f"{p['playlist_id']}|{p['title']}|{p['description']}|{p['creation_date']}|{p['total_songs']}\n"
            f.write(line)

def save_playlist_songs(playlist_songs):
    with open(os.path.join(DATA_DIR, 'playlist_songs.txt'), 'w', encoding='utf-8') as f:
        for pls in playlist_songs:
            line = f"{pls['playlist_song_id']}|{pls['playlist_id']}|{pls['song_id']}|{pls['added_date']}\n"
            f.write(line)


@app.route('/')
def dashboard():
    genres = load_genres()
    artists = load_artists()
    playlists = load_playlists()
    # Sort artists by name for trending
    trending_artists = sorted(artists, key=lambda a: a['name'].lower())[:5]
    return render_template('dashboard.html', genres=genres, artists=artists, playlists=playlists, trending_artists=trending_artists)

@app.route('/artists')
def artists_route():
    artists = load_artists()
    sort_key = request.args.get('sort', 'Name').lower()
    search_query = request.args.get('search', '').lower()

    filtered_artists = [a for a in artists if search_query in a['name'].lower()]
    if sort_key == 'name':
        filtered_artists.sort(key=lambda x: x['name'].lower())
    elif sort_key == 'genre':
        filtered_artists.sort(key=lambda x: x['genre'].lower())
    return render_template('artists.html', artists=filtered_artists, sort_key=sort_key, search_query=search_query)

@app.route('/artists/<artist_id>')
def artist_profile(artist_id):
    artists = {a['artist_id']: a for a in load_artists()}
    artist = artists.get(artist_id)
    if not artist:
        return "Artist not found", 404
    songs = load_songs()
    artist_songs = [s for s in songs if s['artist_id'] == artist_id]
    return render_template('artist_profile.html', artist=artist, songs=artist_songs)

@app.route('/albums')
def albums():
    albums = load_albums()
    artists = {a['artist_id']: a for a in load_artists()}
    search_query = request.args.get('search', '').lower()
    genre_filter = request.args.get('genre', '')
    sort_key = request.args.get('sort', 'Title').lower()

    filtered_albums = []
    for album in albums:
        if (search_query in album['title'].lower() or not search_query) and (genre_filter == '' or genre_filter == album['genre']):
            filtered_albums.append(album)

    if sort_key == 'title':
        filtered_albums.sort(key=lambda x: x['title'].lower())
    elif sort_key == 'year':
        filtered_albums.sort(key=lambda x: x['release_year'])

    return render_template('albums.html', albums=filtered_albums, artists=artists, genre_filter=genre_filter, search_query=search_query, sort_key=sort_key)

@app.route('/albums/<album_id>')
def album_details(album_id):
    albums = {a['album_id']: a for a in load_albums()}
    artists = {a['artist_id']: a for a in load_artists()}
    songs = load_songs()
    album = albums.get(album_id)
    if not album:
        return "Album not found", 404
    album_songs = [s for s in songs if s['album_id'] == album_id]
    artist = artists.get(album['artist_id'])
    return render_template('album_details.html', album=album, artist=artist, songs=album_songs)

@app.route('/catalog')
def catalog():
    songs = load_songs()
    artists = {a['artist_id']: a for a in load_artists()}
    albums = {a['album_id']: a for a in load_albums()}

    search_query = request.args.get('search', '').lower()
    filtered_songs = [s for s in songs if search_query in s['title'].lower() or search_query in artists.get(s['artist_id'], {}).get('name', '').lower()]

    # Sort by title or artist
    sort_key = request.args.get('sort', 'Title').lower()
    if sort_key == 'title':
        filtered_songs.sort(key=lambda x: x['title'].lower())
    elif sort_key == 'artist':
        filtered_songs.sort(key=lambda x: artists.get(x['artist_id'], {}).get('name', '').lower())

    return render_template('catalog.html', songs=filtered_songs, artists=artists, albums=albums, search_query=search_query, sort_key=sort_key)

@app.route('/catalog/song/<song_id>')
def song_details(song_id):
    songs = {s['song_id']: s for s in load_songs()}
    artists = {a['artist_id']: a for a in load_artists()}
    albums = {a['album_id']: a for a in load_albums()}
    song = songs.get(song_id)
    if not song:
        return "Song not found", 404
    artist = artists.get(song['artist_id'])
    album = albums.get(song['album_id'])
    return render_template('song_details.html', song=song, artist=artist, album=album)

@app.route('/genres')
def genres():
    genres = load_genres()
    return render_template('genres.html', genres=genres)

@app.route('/playlists')
def playlists():
    playlists = load_playlists()
    search_query = request.args.get('search', '').lower()
    filtered_playlists = [p for p in playlists if search_query in p['title'].lower()] if search_query else playlists
    return render_template('playlists.html', playlists=filtered_playlists, search_query=search_query)

@app.route('/playlists/<playlist_id>')
def playlist_details(playlist_id):
    playlists = {p['playlist_id']: p for p in load_playlists()}
    songs = {s['song_id']: s for s in load_songs()}
    playlist_songs = load_playlist_songs()
    if playlist_id not in playlists:
        return "Playlist not found", 404
    playlist = playlists[playlist_id]
    songs_in_playlist = [songs[pls['song_id']] for pls in playlist_songs if pls['playlist_id'] == playlist_id and pls['song_id'] in songs]
    return render_template('playlist_details.html', playlist=playlist, songs=songs_in_playlist)

@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'POST':
        title = request.form.get('playlist-name-input', '').strip()
        description = request.form.get('playlist-description-input', '').strip()
        if not title:
            error = 'Title is required'
            return render_template('create_playlist.html', error=error)
        playlists = load_playlists()
        new_id = str(max([int(p['playlist_id']) for p in playlists], default=0) + 1)
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
        return redirect(url_for('playlists'))
    return render_template('create_playlist.html')

@app.route('/playlists/<playlist_id>/remove_song/<song_id>')
def remove_song_from_playlist(playlist_id, song_id):
    playlist_songs = load_playlist_songs()
    playlist_songs = [pls for pls in playlist_songs if not (pls['playlist_id'] == playlist_id and pls['song_id'] == song_id)]
    save_playlist_songs(playlist_songs)
    playlists = load_playlists()
    playlist = next((p for p in playlists if p['playlist_id'] == playlist_id), None)
    if playlist:
        playlist['total_songs'] = max(0, playlist['total_songs'] - 1)
        save_playlists(playlists)
    return redirect(url_for('playlist_details', playlist_id=playlist_id))

@app.route('/playlists/delete/<playlist_id>')
def delete_playlist(playlist_id):
    playlists = load_playlists()
    playlists = [p for p in playlists if p['playlist_id'] != playlist_id]
    save_playlists(playlists)
    playlist_songs = load_playlist_songs()
    playlist_songs = [pls for pls in playlist_songs if pls['playlist_id'] != playlist_id]
    save_playlist_songs(playlist_songs)
    return redirect(url_for('playlists'))

if __name__ == '__main__':
    app.run(debug=True)
