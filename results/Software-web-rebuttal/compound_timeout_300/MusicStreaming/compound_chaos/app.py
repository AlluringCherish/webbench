from flask import Flask, render_template, redirect, url_for, request, abort
from datetime import datetime
import os

app = Flask(__name__)

data_folder = 'data'

# Global in-memory data storage
songs = {}
artists = {}
albums = {}
genres = {}
playlists = {}
playlist_songs = {}

# Helper functions for file operations

def load_songs():
    songs.clear()
    path = os.path.join(data_folder, 'songs.txt')
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            try:
                song_id = int(parts[0])
                title = parts[1]
                artist_id = int(parts[2])
                album_id = int(parts[3])
                genre = parts[4]
                duration = int(parts[5])
                release_date = parts[6]
                play_count = int(parts[7])
                songs[song_id] = {
                    'song_id': song_id,
                    'title': title,
                    'artist_id': artist_id,
                    'album_id': album_id,
                    'genre': genre,
                    'duration': duration,
                    'release_date': release_date,
                    'play_count': play_count
                }
            except (IndexError, ValueError):
                # ignore malformed lines
                pass

def save_songs():
    path = os.path.join(data_folder, 'songs.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for song in songs.values():
            line = f"{song['song_id']}|{song['title']}|{song['artist_id']}|{song['album_id']}|{song['genre']}|{song['duration']}|{song['release_date']}|{song['play_count']}"
            f.write(line + "\n")

def load_artists():
    artists.clear()
    path = os.path.join(data_folder, 'artists.txt')
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            try:
                artist_id = int(parts[0])
                name = parts[1]
                genre = parts[2]
                country = parts[3]
                formation_year = int(parts[4])
                artists[artist_id] = {
                    'artist_id': artist_id,
                    'name': name,
                    'genre': genre,
                    'country': country,
                    'formation_year': formation_year
                }
            except (IndexError, ValueError):
                pass

def save_artists():
    path = os.path.join(data_folder, 'artists.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for artist in artists.values():
            line = f"{artist['artist_id']}|{artist['name']}|{artist['genre']}|{artist['country']}|{artist['formation_year']}"
            f.write(line + "\n")

def load_albums():
    albums.clear()
    path = os.path.join(data_folder, 'albums.txt')
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            try:
                album_id = int(parts[0])
                title = parts[1]
                artist_id = int(parts[2])
                release_year = int(parts[3])
                total_songs = int(parts[4])
                genre = parts[5]
                albums[album_id] = {
                    'album_id': album_id,
                    'title': title,
                    'artist_id': artist_id,
                    'release_year': release_year,
                    'total_songs': total_songs,
                    'genre': genre
                }
            except (IndexError, ValueError):
                pass

def save_albums():
    path = os.path.join(data_folder, 'albums.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for album in albums.values():
            line = f"{album['album_id']}|{album['title']}|{album['artist_id']}|{album['release_year']}|{album['total_songs']}|{album['genre']}"
            f.write(line + "\n")

def load_genres():
    genres.clear()
    path = os.path.join(data_folder, 'genres.txt')
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            try:
                genre_id = int(parts[0])
                genre_name = parts[1]
                description = parts[2]
                genres[genre_id] = {
                    'genre_id': genre_id,
                    'genre_name': genre_name,
                    'description': description
                }
            except (IndexError, ValueError):
                pass

def save_genres():
    path = os.path.join(data_folder, 'genres.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for genre in genres.values():
            line = f"{genre['genre_id']}|{genre['genre_name']}|{genre['description']}"
            f.write(line + "\n")

def load_playlists():
    playlists.clear()
    path = os.path.join(data_folder, 'playlists.txt')
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            try:
                playlist_id = int(parts[0])
                title = parts[1]
                description = parts[2]
                creation_date = parts[3]
                total_songs = int(parts[4])
                playlists[playlist_id] = {
                    'playlist_id': playlist_id,
                    'title': title,
                    'description': description,
                    'creation_date': creation_date,
                    'total_songs': total_songs
                }
            except (IndexError, ValueError):
                pass

def save_playlists():
    path = os.path.join(data_folder, 'playlists.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for playlist in playlists.values():
            line = f"{playlist['playlist_id']}|{playlist['title']}|{playlist['description']}|{playlist['creation_date']}|{playlist['total_songs']}"
            f.write(line + "\n")

def load_playlist_songs():
    playlist_songs.clear()
    path = os.path.join(data_folder, 'playlist_songs.txt')
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            try:
                playlist_song_id = int(parts[0])
                playlist_id = int(parts[1])
                song_id = int(parts[2])
                added_date = parts[3]
                playlist_songs[playlist_song_id] = {
                    'playlist_song_id': playlist_song_id,
                    'playlist_id': playlist_id,
                    'song_id': song_id,
                    'added_date': added_date
                }
            except (IndexError, ValueError):
                pass

def save_playlist_songs():
    path = os.path.join(data_folder, 'playlist_songs.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for ps in playlist_songs.values():
            line = f"{ps['playlist_song_id']}|{ps['playlist_id']}|{ps['song_id']}|{ps['added_date']}"
            f.write(line + "\n")

# Loading all data at startup
load_songs()
load_artists()
load_albums()
load_genres()
load_playlists()
load_playlist_songs()

# Helper functions for lookup

def get_artist_name(artist_id):
    artist = artists.get(artist_id)
    return artist['name'] if artist else "Unknown Artist"

def get_album_name(album_id):
    album = albums.get(album_id)
    return album['title'] if album else "Unknown Album"

def get_playlist_song_ids(playlist_id):
    return [ps['playlist_song_id'] for ps in playlist_songs.values() if ps['playlist_id'] == playlist_id]

def get_playlist_song_ids_and_entries(playlist_id):
    result = []
    for ps in playlist_songs.values():
        if ps['playlist_id'] == playlist_id:
            result.append(ps)
    return result

# Root redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

# Dashboard route
@app.route('/dashboard')
def dashboard():
    # Featured songs: Let's pick top 5 by play_count descending
    featured_songs_list = sorted(songs.values(), key=lambda s: s['play_count'], reverse=True)[:5]
    featured_songs = []
    for s in featured_songs_list:
        artist_name = get_artist_name(s['artist_id'])
        featured_songs.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_name,
            'duration': s['duration']
        })

    # Trending artists: Let's pick top 5 artists by total play count of their songs
    artist_play_counts = {}
    for s in songs.values():
        artist_play_counts[s['artist_id']] = artist_play_counts.get(s['artist_id'], 0) + s['play_count']
    trending = sorted(artist_play_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    trending_artists = []
    for artist_id, _ in trending:
        if artist_id in artists:
            trending_artists.append({'artist_id': artist_id, 'name': artists[artist_id]['name']})

    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)

# Songs catalog
@app.route('/songs')
def song_catalog():
    genres_list = sorted(set(g['genre_name'] for g in genres.values()))
    songs_list = []
    for s in songs.values():
        artist_name = get_artist_name(s['artist_id'])
        album_name = get_album_name(s['album_id'])
        songs_list.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_name,
            'album_name': album_name,
            'genre': s['genre'],
            'duration': s['duration']
        })
    return render_template('song_catalog.html', songs=songs_list, genres=genres_list)

# Song details
@app.route('/songs/<int:song_id>')
def song_details(song_id):
    s = songs.get(song_id)
    if not s:
        abort(404)
    artist_name = get_artist_name(s['artist_id'])
    album_name = get_album_name(s['album_id'])
    song_info = {
        'song_id': s['song_id'],
        'title': s['title'],
        'artist_id': s['artist_id'],
        'artist_name': artist_name,
        'album_id': s['album_id'],
        'album_name': album_name,
        'genre': s['genre'],
        'duration': s['duration'],
        'release_date': s['release_date'],
        'play_count': s['play_count']
    }
    return render_template('song_details.html', song=song_info)

# Playlists listing
@app.route('/playlists')
def playlists_view():
    playlists_list = []
    for pl in playlists.values():
        playlists_list.append({
            'playlist_id': pl['playlist_id'],
            'title': pl['title'],
            'description': pl['description'],
            'total_songs': pl['total_songs']
        })
    return render_template('playlists.html', playlists=playlists_list)

# Playlist details
@app.route('/playlists/<int:playlist_id>')
def playlist_details(playlist_id):
    pl = playlists.get(playlist_id)
    if not pl:
        abort(404)
    songs_in_playlist_list = []
    ps_entries = get_playlist_song_ids_and_entries(playlist_id)
    for pse in ps_entries:
        song = songs.get(pse['song_id'])
        if not song:
            continue
        artist_name = get_artist_name(song['artist_id'])
        songs_in_playlist_list.append({
            'song_id': song['song_id'],
            'title': song['title'],
            'artist_name': artist_name,
            'duration': song['duration']
        })

    return render_template('playlist_details.html', playlist=pl, songs_in_playlist=songs_in_playlist_list)

# Create playlist
@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'GET':
        return render_template('create_playlist.html')

    # POST: create new playlist
    title = request.form.get('playlist-name-input', '').strip()
    description = request.form.get('playlist-description-input', '').strip()

    errors = {}
    if not title:
        errors['title_error'] = 'Title is required.'

    if errors:
        # Return with errors and previously submitted form data
        return render_template('create_playlist.html', errors=errors, title=title, description=description)

    # Assign new unique playlist_id
    if playlists:
        new_id = max(playlists.keys()) + 1
    else:
        new_id = 1

    creation_date = datetime.now().strftime('%Y-%m-%d')
    new_playlist = {
        'playlist_id': new_id,
        'title': title,
        'description': description,
        'creation_date': creation_date,
        'total_songs': 0
    }
    playlists[new_id] = new_playlist
    save_playlists()

    return redirect(url_for('playlist_details', playlist_id=new_id))

# Albums listing
@app.route('/albums')
def albums_view():
    albums_list = []
    for album in albums.values():
        artist_name = get_artist_name(album['artist_id'])
        albums_list.append({
            'album_id': album['album_id'],
            'title': album['title'],
            'artist_name': artist_name,
            'year': album['release_year'],
            'genre': album['genre']
        })
    return render_template('albums.html', albums=albums_list)

# Album details
@app.route('/albums/<int:album_id>')
def album_details(album_id):
    album = albums.get(album_id)
    if not album:
        abort(404)
    artist = artists.get(album['artist_id'])
    artist_name = artist['name'] if artist else 'Unknown Artist'
    # Find songs in album
    songs_in_album_list = []
    for song in songs.values():
        if song['album_id'] == album_id:
            songs_in_album_list.append({
                'song_id': song['song_id'],
                'title': song['title'],
                'duration': song['duration']
            })
    album_info = {
        'album_id': album['album_id'],
        'title': album['title'],
        'artist_id': album['artist_id'],
        'artist_name': artist_name,
        'release_year': album['release_year'],
        'genre': album['genre'],
        'total_songs': album['total_songs']
    }
    return render_template('album_details.html', album=album_info, songs_in_album=songs_in_album_list)

# Artists listing
@app.route('/artists')
def artists_view():
    artists_list = []
    for artist in artists.values():
        artists_list.append({
            'artist_id': artist['artist_id'],
            'name': artist['name'],
            'genre': artist['genre'],
            'country': artist['country'],
            'formation_year': artist['formation_year']
        })
    return render_template('artists.html', artists=artists_list)

# Artist profile
@app.route('/artists/<int:artist_id>')
def artist_profile(artist_id):
    artist = artists.get(artist_id)
    if not artist:
        abort(404)
    # songs by artist
    songs_list = []
    albums_list = []
    for song in songs.values():
        if song['artist_id'] == artist_id:
            album_name = get_album_name(song['album_id'])
            songs_list.append({
                'song_id': song['song_id'],
                'title': song['title'],
                'album_name': album_name,
                'duration': song['duration']
            })
    for album in albums.values():
        if album['artist_id'] == artist_id:
            albums_list.append({
                'album_id': album['album_id'],
                'title': album['title'],
                'release_year': album['release_year']
            })
    return render_template('artist_profile.html', artist=artist, songs=songs_list, albums=albums_list)

# Genres exploration
@app.route('/genres')
def genre_exploration():
    genres_list = list(genres.values())
    selected_genre = request.args.get('selected_genre')

    genre_songs_list = []
    genre_artists_list = []

    if selected_genre:
        selected_genre_lower = selected_genre.lower()
        # songs matching genre
        for s in songs.values():
            if s['genre'].lower() == selected_genre_lower:
                artist_name = get_artist_name(s['artist_id'])
                genre_songs_list.append({
                    'song_id': s['song_id'],
                    'title': s['title'],
                    'artist_name': artist_name,
                    'duration': s['duration']
                })
        # artists matching genre
        for a in artists.values():
            if a['genre'].lower() == selected_genre_lower:
                genre_artists_list.append({
                    'artist_id': a['artist_id'],
                    'name': a['name']
                })

    return render_template('genres.html', genres=genres_list, selected_genre=selected_genre,
                           genre_songs=genre_songs_list, genre_artists=genre_artists_list)

if __name__ == '__main__':
    # Run app on port 5000 with debug
    app.run(host='0.0.0.0', port=5000, debug=True)
