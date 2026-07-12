from flask import Flask, render_template, redirect, url_for, request, abort
from datetime import date
import os

app = Flask(__name__)

data_dir = 'data'

# ----------------------------------------------------------------------
# Helper functions to load all data files as lists/dicts

# Load songs.txt as list of dicts with all fields parsed
# song fields: song_id (int), title (str), artist_id (int), album_id (int), genre (str), duration (int), release_date (str), play_count (int)
def load_songs():
    songs = []
    filepath = os.path.join(data_dir, 'songs.txt')
    if not os.path.exists(filepath):
        return songs
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
            try:
                song_id = int(parts[0])
                title = parts[1]
                artist_id = int(parts[2])
                album_id = int(parts[3])
                genre = parts[4]
                duration = int(parts[5])
                release_date = parts[6]
                play_count = int(parts[7])
                songs.append({
                    'song_id': song_id,
                    'title': title,
                    'artist_id': artist_id,
                    'album_id': album_id,
                    'genre': genre,
                    'duration': duration,
                    'release_date': release_date,
                    'play_count': play_count
                })
            except:
                continue
    return songs

# Load artists.txt
# artist fields: artist_id (int), name (str), genre (str), country (str), formation_year (int)
def load_artists():
    artists = []
    filepath = os.path.join(data_dir, 'artists.txt')
    if not os.path.exists(filepath):
        return artists
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            try:
                artist_id = int(parts[0])
                name = parts[1]
                genre = parts[2]
                country = parts[3]
                formation_year = int(parts[4])
                artists.append({
                    'artist_id': artist_id,
                    'name': name,
                    'genre': genre,
                    'country': country,
                    'formation_year': formation_year
                })
            except:
                continue
    return artists

# Load albums.txt
# album fields: album_id (int), title (str), artist_id (int), release_year (int), total_songs (int), genre (str)
def load_albums():
    albums = []
    filepath = os.path.join(data_dir, 'albums.txt')
    if not os.path.exists(filepath):
        return albums
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            try:
                album_id = int(parts[0])
                title = parts[1]
                artist_id = int(parts[2])
                release_year = int(parts[3])
                total_songs = int(parts[4])
                genre = parts[5]
                albums.append({
                    'album_id': album_id,
                    'title': title,
                    'artist_id': artist_id,
                    'release_year': release_year,
                    'total_songs': total_songs,
                    'genre': genre
                })
            except:
                continue
    return albums

# Load genres.txt
# genre fields: genre_id (int), genre_name (str), description (str)
def load_genres():
    genres = []
    filepath = os.path.join(data_dir, 'genres.txt')
    if not os.path.exists(filepath):
        return genres
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            try:
                genre_id = int(parts[0])
                genre_name = parts[1]
                description = parts[2]
                genres.append({
                    'genre_id': genre_id,
                    'genre_name': genre_name,
                    'description': description
                })
            except:
                continue
    return genres

# Load playlists.txt
# playlist fields: playlist_id (int), title (str), description (str), creation_date (str), total_songs (int)
def load_playlists():
    playlists = []
    filepath = os.path.join(data_dir, 'playlists.txt')
    if not os.path.exists(filepath):
        return playlists
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            try:
                playlist_id = int(parts[0])
                title = parts[1]
                description = parts[2]
                creation_date = parts[3]
                total_songs = int(parts[4])
                playlists.append({
                    'playlist_id': playlist_id,
                    'title': title,
                    'description': description,
                    'creation_date': creation_date,
                    'total_songs': total_songs
                })
            except:
                continue
    return playlists

# Load playlist_songs.txt
# playlist_song fields: playlist_song_id (int), playlist_id (int), song_id (int), added_date (str)
def load_playlist_songs():
    playlist_songs = []
    filepath = os.path.join(data_dir, 'playlist_songs.txt')
    if not os.path.exists(filepath):
        return playlist_songs
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 4:
                continue
            try:
                playlist_song_id = int(parts[0])
                playlist_id = int(parts[1])
                song_id = int(parts[2])
                added_date = parts[3]
                playlist_songs.append({
                    'playlist_song_id': playlist_song_id,
                    'playlist_id': playlist_id,
                    'song_id': song_id,
                    'added_date': added_date
                })
            except:
                continue
    return playlist_songs


# Save playlists.txt from list of playlist dicts
# overwrite file completely

def save_playlists(playlists):
    filepath = os.path.join(data_dir, 'playlists.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for p in playlists:
            line = f"{p['playlist_id']}|{p['title']}|{p['description']}|{p['creation_date']}|{p['total_songs']}\n"
            f.write(line)

# Save playlist_songs.txt from list of playlist_song dicts
# overwrite file completely

def save_playlist_songs(playlist_songs):
    filepath = os.path.join(data_dir, 'playlist_songs.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for ps in playlist_songs:
            line = f"{ps['playlist_song_id']}|{ps['playlist_id']}|{ps['song_id']}|{ps['added_date']}\n"
            f.write(line)

# Utility to get artist dict by id

def get_artist_by_id(artist_id, artists):
    for a in artists:
        if a['artist_id'] == artist_id:
            return a
    return None

# Utility to get album dict by id

def get_album_by_id(album_id, albums):
    for a in albums:
        if a['album_id'] == album_id:
            return a
    return None

# Utility to get playlist by id

def get_playlist_by_id(playlist_id, playlists):
    for p in playlists:
        if p['playlist_id'] == playlist_id:
            return p
    return None

# Utility to get song by id

def get_song_by_id(song_id, songs):
    for s in songs:
        if s['song_id'] == song_id:
            return s
    return None

# ----------------------------------------------------------------------
# Routes Implementation

@app.route('/')
def root_redirect():
    # Redirect to /dashboard
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    # Display featured_songs: List[Dict] with keys (song_id:int, title:str, artist_name:str, duration:int)
    # and trending_artists: List[Dict] with keys (artist_id:int, name:str)

    songs = load_songs()
    artists = load_artists()

    # For featured songs, pick top 5 most played songs (sorted by play_count descending)
    songs_sorted = sorted(songs, key=lambda s: s['play_count'], reverse=True)
    top5_songs = songs_sorted[:5]
    # Map to required keys
    featured_songs = []
    for s in top5_songs:
        artist = get_artist_by_id(s['artist_id'], artists)
        if artist:
            featured_songs.append({
                'song_id': s['song_id'],
                'title': s['title'],
                'artist_name': artist['name'],
                'duration': s['duration']
            })

    # For trending artists, pick top 5 artists by sum of play_count of their songs
    artist_play_count = {}
    for s in songs:
        artist_play_count[s['artist_id']] = artist_play_count.get(s['artist_id'], 0) + s['play_count']
    top_artists_ids = sorted(artist_play_count.keys(), key=lambda aid: artist_play_count[aid], reverse=True)[:5]
    trending_artists = []
    for aid in top_artists_ids:
        artist = get_artist_by_id(aid, artists)
        if artist:
            trending_artists.append({
                'artist_id': artist['artist_id'],
                'name': artist['name']
            })

    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)

@app.route('/songs')
def song_catalog():
    songs_raw = load_songs()
    artists = load_artists()
    albums = load_albums()
    genres_obj = load_genres()

    genres = [g['genre_name'] for g in genres_obj]

    # songs: with keys (song_id:int, title:str, artist_name:str, album_name:str, genre:str, duration:int)
    songs = []
    for s in songs_raw:
        artist = get_artist_by_id(s['artist_id'], artists)
        album = get_album_by_id(s['album_id'], albums)
        if artist and album:
            songs.append({
                'song_id': s['song_id'],
                'title': s['title'],
                'artist_name': artist['name'],
                'album_name': album['title'],
                'genre': s['genre'],
                'duration': s['duration']
            })

    return render_template('song_catalog.html', songs=songs, genres=genres)

@app.route('/songs/<int:song_id>')
def song_details(song_id):
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()

    song = get_song_by_id(song_id, songs)
    if not song:
        abort(404)

    artist = get_artist_by_id(song['artist_id'], artists)
    album = get_album_by_id(song['album_id'], albums)

    if not artist or not album:
        abort(404)

    # Return song dictionary with keys (song_id:int, title:str, artist_name:str, album_name:str, duration:int)
    song_dict = {
        'song_id': song['song_id'],
        'title': song['title'],
        'artist_name': artist['name'],
        'album_name': album['title'],
        'duration': song['duration']
    }

    return render_template('song_details.html', song=song_dict)

@app.route('/playlists')
def playlists():
    playlists = load_playlists()

    # For each playlist, show playlist_id, title, description, total_songs
    return render_template('playlists.html', playlists=playlists)

@app.route('/playlists/<int:playlist_id>', methods=['GET', 'POST'])
def playlist_details(playlist_id):
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()
    songs_all = load_songs()
    artists = load_artists()

    playlist = get_playlist_by_id(playlist_id, playlists)
    if not playlist:
        abort(404)

    if request.method == 'POST':
        # POST may be remove song or delete playlist
        # Fix form field names to match frontend
        if 'remove_song_id' in request.form:
            remove_song_id = request.form.get('remove_song_id')
            try:
                remove_song_id = int(remove_song_id)
            except:
                abort(400)

            # Remove the song entry from playlist_songs
            new_playlist_songs = [ps for ps in playlist_songs if not (ps['playlist_id'] == playlist_id and ps['song_id'] == remove_song_id)]

            # Update playlists total_songs if changed
            old_count = sum(1 for ps in playlist_songs if ps['playlist_id'] == playlist_id)
            new_count = sum(1 for ps in new_playlist_songs if ps['playlist_id'] == playlist_id)

            for p in playlists:
                if p['playlist_id'] == playlist_id:
                    p['total_songs'] = new_count
                    break

            save_playlist_songs(new_playlist_songs)
            save_playlists(playlists)

            return redirect(url_for('playlist_details', playlist_id=playlist_id))
        elif 'delete_playlist' in request.form:
            # Remove playlist from playlists
            new_playlists = [p for p in playlists if p['playlist_id'] != playlist_id]
            # Remove all playlist_songs for that playlist
            new_playlist_songs = [ps for ps in playlist_songs if ps['playlist_id'] != playlist_id]

            save_playlists(new_playlists)
            save_playlist_songs(new_playlist_songs)

            return redirect(url_for('playlists'))
        else:
            abort(400)

    # GET: render page
    # songs in playlist
    # Get song ids from playlist_songs for this playlist
    song_ids_in_playlist = [ps['song_id'] for ps in playlist_songs if ps['playlist_id'] == playlist_id]

    # Build songs list as required keys (song_id:int, title:str, artist_name:str, duration:int)
    songs = []
    for sid in song_ids_in_playlist:
        song = get_song_by_id(sid, songs_all)
        if song:
            artist = get_artist_by_id(song['artist_id'], artists)
            if artist:
                songs.append({
                    'song_id': song['song_id'],
                    'title': song['title'],
                    'artist_name': artist['name'],
                    'duration': song['duration']
                })

    # playlist dictionary keys: playlist_id, title, description
    playlist_dict = {
        'playlist_id': playlist['playlist_id'],
        'title': playlist['title'],
        'description': playlist['description']
    }

    return render_template('playlist_details.html', playlist=playlist_dict, songs=songs)

@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'POST':
        # Handle form submission
        title = request.form.get('playlist_name_input') or request.form.get('playlist-name-input') or request.form.get('playlist_name') or request.form.get('playlist-name')
        description = request.form.get('playlist_description_input') or request.form.get('playlist-description-input') or request.form.get('playlist_description') or request.form.get('playlist-description')

        # Normalize keys, try multiple keys to find correct

        if not title:
            # Required field
            return render_template('create_playlist.html', error='Playlist title is required')

        if description is None:
            description = ''

        playlists = load_playlists()
        playlist_songs = load_playlist_songs()

        # Generate new unique playlist id
        max_pid = max((p['playlist_id'] for p in playlists), default=0)
        new_id = max_pid + 1

        today_str = date.today().isoformat()

        new_playlist = {
            'playlist_id': new_id,
            'title': title,
            'description': description,
            'creation_date': today_str,
            'total_songs': 0
        }

        playlists.append(new_playlist)
        save_playlists(playlists)

        # After create, redirect to playlists page
        return redirect(url_for('playlists'))

    # GET
    return render_template('create_playlist.html')

@app.route('/albums')
def albums():
    albums_raw = load_albums()
    artists = load_artists()

    # albums: List[Dict] with keys (album_id:int, title:str, artist_name:str, year:int)
    albums = []
    for a in albums_raw:
        artist = get_artist_by_id(a['artist_id'], artists)
        if artist:
            albums.append({
                'album_id': a['album_id'],
                'title': a['title'],
                'artist_name': artist['name'],
                'year': a['release_year']
            })

    return render_template('albums.html', albums=albums)

@app.route('/albums/<int:album_id>', methods=['GET', 'POST'])
def album_details(album_id):
    albums = load_albums()
    artists = load_artists()
    songs = load_songs()
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()

    album = get_album_by_id(album_id, albums)
    if not album:
        abort(404)

    artist = get_artist_by_id(album['artist_id'], artists)
    if not artist:
        abort(404)

    # songs in album
    songs_in_album = [s for s in songs if s['album_id'] == album_id]

    # map songs to required keys (song_id:int, title:str, duration:int)
    songs_list = []
    for s in songs_in_album:
        songs_list.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'duration': s['duration']
        })

    if request.method == 'POST':
        # POST handler: add album songs to a playlist
        playlist_id_str = request.form.get('playlist_id')
        if not playlist_id_str:
            abort(400)
        try:
            playlist_id = int(playlist_id_str)
        except:
            abort(400)

        # Validate playlist exists
        playlist = get_playlist_by_id(playlist_id, playlists)
        if not playlist:
            abort(404)

        # Add all songs_in_album to playlist_songs, avoid duplicates
        added_song_ids = [ps['song_id'] for ps in playlist_songs if ps['playlist_id'] == playlist_id]
        new_entries = []
        max_psid = max((ps['playlist_song_id'] for ps in playlist_songs), default=0)
        curr_psid = max_psid
        today_str = date.today().isoformat()

        for s in songs_in_album:
            if s['song_id'] not in added_song_ids:
                curr_psid += 1
                new_entries.append({
                    'playlist_song_id': curr_psid,
                    'playlist_id': playlist_id,
                    'song_id': s['song_id'],
                    'added_date': today_str
                })

        if new_entries:
            playlist_songs.extend(new_entries)
            save_playlist_songs(playlist_songs)

            # Update playlist total_songs
            count_new = sum(1 for ps in playlist_songs if ps['playlist_id'] == playlist_id)
            for p in playlists:
                if p['playlist_id'] == playlist_id:
                    p['total_songs'] = count_new
                    break
            save_playlists(playlists)

        return redirect(url_for('album_details', album_id=album_id))

    album_dict = {
        'album_id': album['album_id'],
        'title': album['title'],
        'artist_name': artist['name'],
        'year': album['release_year']
    }

    return render_template('album_details.html', album=album_dict, songs=songs_list)

@app.route('/artists')
def artists():
    from flask import url_for
    artists_raw = load_artists()

    # Provide fallback photo url to fix broken images on artists page
    fallback_photo_url = url_for('static', filename='img/default_artist.png')

    artists_list = []
    for a in artists_raw:
        artists_list.append({
            'artist_id': a['artist_id'],
            'name': a['name'],
            'genre': a['genre'],
            'photo_url': fallback_photo_url
        })

    return render_template('artists.html', artists=artists_list)

@app.route('/artists/<int:artist_id>')
def artist_profile(artist_id):
    artists = load_artists()
    songs_all = load_songs()
    albums = load_albums()

    artist = get_artist_by_id(artist_id, artists)
    if not artist:
        abort(404)

    # songs by artist
    songs_by_artist = [s for s in songs_all if s['artist_id'] == artist_id]

    # For songs: keys (song_id:int, title:str, album_name:str, duration:int)
    artist_songs = []
    for s in songs_by_artist:
        album = get_album_by_id(s['album_id'], albums)
        if album:
            artist_songs.append({
                'song_id': s['song_id'],
                'title': s['title'],
                'album_name': album['title'],
                'duration': s['duration']
            })

    # artist: keys (artist_id:int, name:str, genre:str, country:str, formation_year:int)
    artist_dict = {
        'artist_id': artist['artist_id'],
        'name': artist['name'],
        'genre': artist['genre'],
        'country': artist['country'],
        'formation_year': artist['formation_year']
    }

    return render_template('artist_profile.html', artist=artist_dict, songs=artist_songs)

@app.route('/genres')
def genres():
    genres_obj = load_genres()
    songs = load_songs()
    artists = load_artists()

    # genres: List[Dict] with keys (genre_id:int, genre_name:str, description:str)
    genres_list = genres_obj

    # songs with keys (song_id:int, title:str, artist_name:str)
    songs_list = []
    for s in songs:
        artist = get_artist_by_id(s['artist_id'], artists)
        if artist:
            songs_list.append({
                'song_id': s['song_id'],
                'title': s['title'],
                'artist_name': artist['name']
            })

    # artists with keys (artist_id:int, name:str)
    artists_list = [{'artist_id': a['artist_id'], 'name': a['name']} for a in artists]

    return render_template('genres.html', genres=genres_list, songs=songs_list, artists=artists_list)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
