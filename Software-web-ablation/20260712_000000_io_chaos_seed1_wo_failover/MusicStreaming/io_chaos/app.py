from flask import Flask, render_template, redirect, url_for, request, abort
import os
import datetime

app = Flask(__name__)

# Data file paths
DATA_DIR = 'data'
SONGS_FILE = os.path.join(DATA_DIR, 'songs.txt')
ARTISTS_FILE = os.path.join(DATA_DIR, 'artists.txt')
ALBUMS_FILE = os.path.join(DATA_DIR, 'albums.txt')
GENRES_FILE = os.path.join(DATA_DIR, 'genres.txt')
PLAYLISTS_FILE = os.path.join(DATA_DIR, 'playlists.txt')
PLAYLIST_SONGS_FILE = os.path.join(DATA_DIR, 'playlist_songs.txt')

# Utility functions for loading data from files

def load_songs():
    songs = []
    try:
        with open(SONGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                song_id, title, artist_id, album_id, genre, duration, release_date, play_count = parts
                song = {
                    'song_id': int(song_id),
                    'title': title,
                    'artist_id': int(artist_id),
                    'album_id': int(album_id),
                    'genre': genre,
                    'duration': int(duration),
                    'release_date': release_date,
                    'play_count': int(play_count)
                }
                songs.append(song)
    except FileNotFoundError:
        pass
    return songs


def load_artists():
    artists = []
    try:
        with open(ARTISTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                artist_id, name, genre, country, formation_year = parts
                try:
                    artist = {
                        'artist_id': int(artist_id),
                        'name': name,
                        'genre': genre,
                        'country': country,
                        'formation_year': int(formation_year)
                    }
                    artists.append(artist)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return artists


def load_albums():
    albums = []
    try:
        with open(ALBUMS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                album_id, title, artist_id, release_year, total_songs, genre = parts
                try:
                    album = {
                        'album_id': int(album_id),
                        'title': title,
                        'artist_id': int(artist_id),
                        'release_year': int(release_year),
                        'total_songs': int(total_songs),
                        'genre': genre
                    }
                    albums.append(album)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return albums


def load_genres():
    genres = []
    try:
        with open(GENRES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 3:
                    continue
                genre_id, genre_name, description = parts
                try:
                    genre = {
                        'genre_id': int(genre_id),
                        'genre_name': genre_name,
                        'description': description
                    }
                    genres.append(genre)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return genres


def load_playlists():
    playlists = []
    try:
        with open(PLAYLISTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                playlist_id, title, description, creation_date, total_songs = parts
                try:
                    playlist = {
                        'playlist_id': int(playlist_id),
                        'title': title,
                        'description': description,
                        'creation_date': creation_date,
                        'total_songs': int(total_songs)
                    }
                    playlists.append(playlist)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return playlists


def load_playlist_songs():
    playlist_songs = []
    try:
        with open(PLAYLIST_SONGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 4:
                    continue
                playlist_song_id, playlist_id, song_id, added_date = parts
                try:
                    playlist_song = {
                        'playlist_song_id': int(playlist_song_id),
                        'playlist_id': int(playlist_id),
                        'song_id': int(song_id),
                        'added_date': added_date
                    }
                    playlist_songs.append(playlist_song)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return playlist_songs

# Utility functions for saving data to files

def save_playlists(playlists):
    with open(PLAYLISTS_FILE, 'w', encoding='utf-8') as f:
        for p in playlists:
            line = f"{p['playlist_id']}|{p['title']}|{p['description']}|{p['creation_date']}|{p['total_songs']}\n"
            f.write(line)


def save_playlist_songs(playlist_songs):
    with open(PLAYLIST_SONGS_FILE, 'w', encoding='utf-8') as f:
        for ps in playlist_songs:
            line = f"{ps['playlist_song_id']}|{ps['playlist_id']}|{ps['song_id']}|{ps['added_date']}\n"
            f.write(line)


# Route: / (root_redirect)
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


# Route: /dashboard (dashboard_page)
@app.route('/dashboard')
def dashboard_page():
    songs = load_songs()
    artists = load_artists()

    # featured_songs: list of dicts {song_id:int, title:str, artist_name:str, album_name:str, duration:int}
    albums = load_albums()
    album_dict = {album['album_id']: album['title'] for album in albums}
    artist_dict = {artist['artist_id']: artist['name'] for artist in artists}

    # Select featured songs: for simplicity top 5 by play_count descending
    featured_songs_raw = sorted(songs, key=lambda s: s['play_count'], reverse=True)[:5]
    featured_songs = []
    for song in featured_songs_raw:
        featured_songs.append({
            'song_id': song['song_id'],
            'title': song['title'],
            'artist_name': artist_dict.get(song['artist_id'], 'Unknown Artist'),
            'album_name': album_dict.get(song['album_id'], 'Unknown Album'),
            'duration': song['duration']
        })

    # trending_artists: list of dicts {artist_id:int, name:str, genre:str}
    # For simplicity, top 5 artists by summing play count of their songs
    artist_play_count = {}
    for song in songs:
        artist_play_count[song['artist_id']] = artist_play_count.get(song['artist_id'], 0) + song['play_count']
    trending_artist_ids = sorted(artist_play_count, key=lambda aid: artist_play_count[aid], reverse=True)[:5]
    trending_artists = []
    artist_map = {artist['artist_id']:artist for artist in artists}
    for aid in trending_artist_ids:
        artist = artist_map.get(aid)
        if artist:
            trending_artists.append({
                'artist_id': artist['artist_id'],
                'name': artist['name'],
                'genre': artist['genre']
            })

    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)


# Route: /songs (song_catalog)
@app.route('/songs')
def song_catalog():
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()
    genres = load_genres()

    artist_dict = {artist['artist_id']: artist['name'] for artist in artists}
    album_dict = {album['album_id']: album['title'] for album in albums}

    songs_out = []
    for song in songs:
        songs_out.append({
            'song_id': song['song_id'],
            'title': song['title'],
            'artist_name': artist_dict.get(song['artist_id'], 'Unknown Artist'),
            'album_name': album_dict.get(song['album_id'], 'Unknown Album'),
            'genre': song['genre'],
            'duration': song['duration']
        })

    genre_names = [g['genre_name'] for g in genres]

    return render_template('song_catalog.html', songs=songs_out, genres=genre_names)


# Route: /songs/<int:song_id> (song_details)
@app.route('/songs/<int:song_id>')
def song_details(song_id):
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()

    song = None
    for s in songs:
        if s['song_id'] == song_id:
            song = s
            break
    if not song:
        abort(404)

    artist = None
    for a in artists:
        if a['artist_id'] == song['artist_id']:
            artist = a
            break

    album = None
    for al in albums:
        if al['album_id'] == song['album_id']:
            album = al
            break

    song_dict = {
        'song_id': song['song_id'],
        'title': song['title'],
        'artist_id': artist['artist_id'] if artist else None,
        'artist_name': artist['name'] if artist else 'Unknown Artist',
        'album_id': album['album_id'] if album else None,
        'album_name': album['title'] if album else 'Unknown Album',
        'duration': song['duration'],
        'genre': song['genre'],
        'release_date': song['release_date']
    }

    return render_template('song_details.html', song=song_dict)


# Route: /playlists (playlists_page)
@app.route('/playlists')
def playlists_page():
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()

    playlists_out = []
    for playlist in playlists:
        # total_songs from file used
        playlists_out.append({
            'playlist_id': playlist['playlist_id'],
            'title': playlist['title'],
            'description': playlist['description'],
            'total_songs': playlist['total_songs']
        })

    return render_template('playlists.html', playlists=playlists_out)


# Route: /playlists/create (create_playlist) GET and POST
@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'GET':
        # Render form page
        return render_template('create_playlist.html')

    # POST method: process form submission
    title = request.form.get('playlist_name', '').strip()
    description = request.form.get('playlist_description', '').strip()

    errors = {}

    if not title:
        errors['title'] = 'Playlist name is required.'

    if errors:
        return render_template('create_playlist.html', errors=errors, playlist_name=title, playlist_description=description)

    # Load current playlists to determine new id
    playlists = load_playlists()
    if playlists:
        new_id = max(p['playlist_id'] for p in playlists) + 1
    else:
        new_id = 1

    creation_date = datetime.date.today().isoformat()
    new_playlist = {
        'playlist_id': new_id,
        'title': title,
        'description': description,
        'creation_date': creation_date,
        'total_songs': 0
    }
    playlists.append(new_playlist)

    # Save updated playlists
    save_playlists(playlists)

    return redirect(url_for('playlists_page'))


# Route: /playlists/<int:playlist_id> (playlist_details)
@app.route('/playlists/<int:playlist_id>')
def playlist_details(playlist_id):
    playlists = load_playlists()
    songs = load_songs()
    playlist_songs = load_playlist_songs()
    artists = load_artists()

    playlist = None
    for p in playlists:
        if p['playlist_id'] == playlist_id:
            playlist = p
            break
    if not playlist:
        abort(404)

    # Get songs in that playlist
    songs_in_playlist = []
    artist_dict = {a['artist_id']: a['name'] for a in artists}
    for ps in playlist_songs:
        if ps['playlist_id'] == playlist_id:
            # find corresponding song
            for song in songs:
                if song['song_id'] == ps['song_id']:
                    songs_in_playlist.append({
                        'song_id': song['song_id'],
                        'title': song['title'],
                        'artist_name': artist_dict.get(song['artist_id'], 'Unknown Artist'),
                        'duration': song['duration']
                    })

    return render_template('playlist_details.html', playlist=playlist, songs_in_playlist=songs_in_playlist)


# Route: /playlists/<int:playlist_id>/delete (delete_playlist) POST
@app.route('/playlists/<int:playlist_id>/delete', methods=['POST'])
def delete_playlist(playlist_id):
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()

    # Remove playlist from playlists
    playlists_new = [p for p in playlists if p['playlist_id'] != playlist_id]

    # Remove all playlist_songs for this playlist
    playlist_songs_new = [ps for ps in playlist_songs if ps['playlist_id'] != playlist_id]

    # Save updated data
    save_playlists(playlists_new)
    save_playlist_songs(playlist_songs_new)

    return redirect(url_for('playlists_page'))


# Route: /playlists/<int:playlist_id>/remove_song/<int:song_id> (remove_song_from_playlist) POST
@app.route('/playlists/<int:playlist_id>/remove_song/<int:song_id>', methods=['POST'])
def remove_song_from_playlist(playlist_id, song_id):
    playlist_songs = load_playlist_songs()
    playlists = load_playlists()

    # Filter out the song to remove
    playlist_songs_new = [ps for ps in playlist_songs if not(ps['playlist_id'] == playlist_id and ps['song_id'] == song_id)]

    # Update total_songs in playlists
    # Count songs in each playlist
    playlist_song_counts = {}
    for ps in playlist_songs_new:
        playlist_song_counts[ps['playlist_id']] = playlist_song_counts.get(ps['playlist_id'], 0) + 1

    for p in playlists:
        p['total_songs'] = playlist_song_counts.get(p['playlist_id'], 0)

    # Save updated data
    save_playlists(playlists)
    save_playlist_songs(playlist_songs_new)

    return redirect(url_for('playlist_details', playlist_id=playlist_id))


# Route: /albums (albums_page)
@app.route('/albums')
def albums_page():
    albums = load_albums()
    artists = load_artists()

    artist_dict = {a['artist_id']: a['name'] for a in artists}

    albums_out = []
    for album in albums:
        albums_out.append({
            'album_id': album['album_id'],
            'title': album['title'],
            'artist_name': artist_dict.get(album['artist_id'], 'Unknown Artist'),
            'release_year': album['release_year'],
            'genre': album['genre']
        })

    return render_template('albums.html', albums=albums_out)


# Route: /albums/<int:album_id> (album_details)
@app.route('/albums/<int:album_id>')
def album_details(album_id):
    albums = load_albums()
    artists = load_artists()
    songs = load_songs()

    album = None
    for al in albums:
        if al['album_id'] == album_id:
            album = al
            break
    if not album:
        abort(404)

    artist = None
    for a in artists:
        if a['artist_id'] == album['artist_id']:
            artist = a
            break

    album_songs = []
    for song in songs:
        if song['album_id'] == album_id:
            album_songs.append({
                'song_id': song['song_id'],
                'title': song['title'],
                'duration': song['duration']
            })

    album_dict = {
        'album_id': album['album_id'],
        'title': album['title'],
        'artist_id': artist['artist_id'] if artist else None,
        'artist_name': artist['name'] if artist else 'Unknown Artist',
        'release_year': album['release_year']
    }

    return render_template('album_details.html', album=album_dict, album_songs=album_songs)


# Route: /artists (artists_page)
@app.route('/artists')
def artists_page():
    artists = load_artists()

    artists_out = []
    for artist in artists:
        artists_out.append({
            'artist_id': artist['artist_id'],
            'name': artist['name'],
            'genre': artist['genre'],
            'country': artist['country']
        })

    return render_template('artists.html', artists=artists_out)


# Route: /artists/<int:artist_id> (artist_profile)
@app.route('/artists/<int:artist_id>')
def artist_profile(artist_id):
    artists = load_artists()
    songs = load_songs()
    albums = load_albums()

    artist = None
    for a in artists:
        if a['artist_id'] == artist_id:
            artist = a
            break
    if not artist:
        abort(404)

    # artist: dict {artist_id, name, genre, country, formation_year}
    artist_dict = {
        'artist_id': artist['artist_id'],
        'name': artist['name'],
        'genre': artist['genre'],
        'country': artist['country'],
        'formation_year': artist['formation_year']
    }

    # artist_songs: list of dicts {song_id, title, album_name, duration}
    album_dict = {album['album_id']: album['title'] for album in albums}
    artist_songs = []
    for song in songs:
        if song['artist_id'] == artist_id:
            artist_songs.append({
                'song_id': song['song_id'],
                'title': song['title'],
                'album_name': album_dict.get(song['album_id'], 'Unknown Album'),
                'duration': song['duration']
            })

    return render_template('artist_profile.html', artist=artist_dict, artist_songs=artist_songs)


# Route: /genres (genre_exploration)
@app.route('/genres')
def genre_exploration():
    genres = load_genres()

    selected_genre = None
    genre_songs = []
    genre_artists = []

    genre_name_filter = request.args.get('genre_name', '').strip()

    if genre_name_filter:
        # Find genre by name
        for genre in genres:
            if genre['genre_name'].lower() == genre_name_filter.lower():
                selected_genre = genre
                break

    songs = load_songs()
    artists = load_artists()

    if selected_genre:
        # Get songs of that genre
        genre_songs = [
            {
                'song_id': s['song_id'],
                'title': s['title'],
                'artist_name': next((a['name'] for a in artists if a['artist_id'] == s['artist_id']), 'Unknown Artist'),
                'duration': s['duration']
            }
            for s in songs if s['genre'].lower() == selected_genre['genre_name'].lower()
        ]

        # Get artists of that genre
        genre_artists = [
            {
                'artist_id': a['artist_id'],
                'name': a['name'],
                'genre': a['genre']
            }
            for a in artists if a['genre'].lower() == selected_genre['genre_name'].lower()
        ]

    return render_template('genres.html', genres=genres, selected_genre=selected_genre,
                           genre_songs=genre_songs, genre_artists=genre_artists)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
