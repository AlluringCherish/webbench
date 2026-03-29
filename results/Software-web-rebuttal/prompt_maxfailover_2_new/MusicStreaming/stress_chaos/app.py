from flask import Flask, render_template, redirect, url_for, request, abort
from datetime import datetime
import os

app = Flask(__name__)

data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

### Helper functions to load data from files ###

def load_songs():
    songs = []
    filepath = os.path.join(data_folder, 'songs.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
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
    except FileNotFoundError:
        pass
    return songs

def load_artists():
    artists = []
    filepath = os.path.join(data_folder, 'artists.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                artist = {
                    'artist_id': int(parts[0]),
                    'name': parts[1],
                    'genre': parts[2],
                    'country': parts[3],
                    'formation_year': int(parts[4])
                }
                artists.append(artist)
    except FileNotFoundError:
        pass
    return artists

def load_albums():
    albums = []
    filepath = os.path.join(data_folder, 'albums.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                album = {
                    'album_id': int(parts[0]),
                    'title': parts[1],
                    'artist_id': int(parts[2]),
                    'release_year': int(parts[3]),
                    'total_songs': int(parts[4]),
                    'genre': parts[5]
                }
                albums.append(album)
    except FileNotFoundError:
        pass
    return albums

def load_genres():
    genres = []
    filepath = os.path.join(data_folder, 'genres.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                genre = {
                    'genre_id': int(parts[0]),
                    'genre_name': parts[1],
                    'description': parts[2]
                }
                genres.append(genre)
    except FileNotFoundError:
        pass
    return genres

def load_playlists():
    playlists = []
    filepath = os.path.join(data_folder, 'playlists.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                playlist = {
                    'playlist_id': int(parts[0]),
                    'title': parts[1],
                    'description': parts[2],
                    'creation_date': parts[3],
                    'total_songs': int(parts[4])
                }
                playlists.append(playlist)
    except FileNotFoundError:
        pass
    return playlists

def load_playlist_songs():
    playlist_songs = []
    filepath = os.path.join(data_folder, 'playlist_songs.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=4:
                    continue
                ps = {
                    'playlist_song_id': int(parts[0]),
                    'playlist_id': int(parts[1]),
                    'song_id': int(parts[2]),
                    'added_date': parts[3]
                }
                playlist_songs.append(ps)
    except FileNotFoundError:
        pass
    return playlist_songs

### Helper functions to save playlists and playlist_songs data ###

def save_playlists(playlists):
    filepath = os.path.join(data_folder, 'playlists.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for p in playlists:
                line = f"{p['playlist_id']}|{p['title']}|{p['description']}|{p['creation_date']}|{p['total_songs']}\n"
                f.write(line)
    except Exception:
        pass

def save_playlist_songs(playlist_songs):
    filepath = os.path.join(data_folder, 'playlist_songs.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for ps in playlist_songs:
                line = f"{ps['playlist_song_id']}|{ps['playlist_id']}|{ps['song_id']}|{ps['added_date']}\n"
                f.write(line)
    except Exception:
        pass

### Helper to find max id for new entries ###
def get_next_id(items, id_field):
    if not items:
        return 1
    return max(item[id_field] for item in items) + 1

### Helper function to get artist name by id ###
def get_artist_name(artist_id, artists):
    for artist in artists:
        if artist['artist_id'] == artist_id:
            return artist['name']
    return 'Unknown Artist'

### Helper function to get album name by id ###
def get_album_name(album_id, albums):
    for album in albums:
        if album['album_id'] == album_id:
            return album['title']
    return 'Unknown Album'

### Helper function to get playlist by id ###
def get_playlist_by_id(playlist_id, playlists):
    for p in playlists:
        if p['playlist_id'] == playlist_id:
            return p
    return None

### Helper function to get song by id ###
def get_song_by_id(song_id, songs):
    for s in songs:
        if s['song_id'] == song_id:
            return s
    return None

### Helper function to get songs in a playlist ###
def get_songs_in_playlist(playlist_id, playlist_songs, songs):
    song_ids = [ps['song_id'] for ps in playlist_songs if ps['playlist_id'] == playlist_id]
    result_songs = []
    for sid in song_ids:
        song = get_song_by_id(sid, songs)
        if song:
            # Augment song info with artist_name and album_name
            artist_name = get_artist_name(song['artist_id'], load_artists())
            album_name = get_album_name(song['album_id'], load_albums())
            song_copy = dict(song)
            song_copy['artist_name'] = artist_name
            song_copy['album_name'] = album_name
            result_songs.append(song_copy)
    return result_songs

### Route Implementations ###

# / redirects to dashboard
@app.route('/')
def redirect_to_dashboard():
    return redirect(url_for('dashboard'))

# /dashboard
@app.route('/dashboard')
def dashboard():
    songs = load_songs()
    playlists = load_playlists()
    artists = load_artists()

    # Determine featured songs - let\'s take top 5 songs by play_count
    top_songs = sorted(songs, key=lambda s: s.get('play_count', 0), reverse=True)[:5]
    featured_songs = []
    for song in top_songs:
        artist_name = get_artist_name(song['artist_id'], artists)
        featured_songs.append({
            'id': song['song_id'],
            'title': song['title'],
            'artist_name': artist_name,
            'duration': song['duration']
        })

    # Featured playlists - top 5 by total_songs
    top_playlists = sorted(playlists, key=lambda p: p.get('total_songs', 0), reverse=True)[:5]
    featured_playlists = []
    for p in top_playlists:
        featured_playlists.append({
            'id': p['playlist_id'],
            'title': p['title'],
            'total_songs': p['total_songs']
        })

    # Trending artists - top 5 by formation_year descending (more recent) or by other heuristic (just formation_year reverse)
    trending = sorted(artists, key=lambda a: a.get('formation_year', 0), reverse=True)[:5]
    trending_artists = [{'id': a['artist_id'], 'name': a['name']} for a in trending]

    return render_template('dashboard.html', featured_songs=featured_songs, featured_playlists=featured_playlists, trending_artists=trending_artists)

# /songs
@app.route('/songs')
def song_catalog():
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()
    genres = load_genres()

    search_query = request.args.get('search', '').strip()
    genre_filter_raw = request.args.get('genre')
    genre_filter = None
    try:
        genre_filter = int(genre_filter_raw) if genre_filter_raw else None
    except ValueError:
        genre_filter = None

    # Prepare mapping genre_id to genre_name
    genre_id_to_name = {g['genre_id']: g['genre_name'] for g in genres}

    # Filter songs by search and genre
    filtered_songs = []
    for song in songs:
        artist_name = get_artist_name(song['artist_id'], artists)
        album_name = get_album_name(song['album_id'], albums)
        # Find genre_id for the song genre string from genres
        genre_id_for_song = None
        for g in genres:
            if g['genre_name'].lower() == song['genre'].lower():
                genre_id_for_song = g['genre_id']
                break

        # Filter by genre if requested
        if genre_filter is not None and genre_id_for_song != genre_filter:
            continue

        # Filter by search_query in title, artist_name, album_name
        match_query = True
        if search_query:
            low_query = search_query.lower()
            if low_query not in song['title'].lower() and low_query not in artist_name.lower() and low_query not in album_name.lower():
                match_query = False
        if match_query:
            filtered_songs.append({
                'id': song['song_id'],
                'title': song['title'],
                'artist_name': artist_name,
                'album_name': album_name,
                'duration': song['duration'],
                'genre': song['genre']
            })

    return render_template('songs.html', songs=filtered_songs, genres=genres, search_query=search_query, genre_filter=genre_filter)

# /songs/<int:song_id>
@app.route('/songs/<int:song_id>')
def song_details(song_id):
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()

    song = get_song_by_id(song_id, songs)
    if not song:
        abort(404)

    # Add detailed info including artist_id and album_id (already present)
    # Also pass artist_name and album_name
    artist_name = get_artist_name(song['artist_id'], artists)
    album_name = get_album_name(song['album_id'], albums)

    song_detail = dict(song)
    song_detail['artist_name'] = artist_name
    song_detail['album_name'] = album_name

    return render_template('song_detail.html', song=song_detail)

# /playlists
@app.route('/playlists')
def playlists():
    playlists = load_playlists()
    # Use all fields except creation_date is not needed in template
    playlists_display = []
    for p in playlists:
        playlists_display.append({
            'id': p['playlist_id'],
            'title': p['title'],
            'description': p['description'],
            'total_songs': p['total_songs']
        })
    return render_template('playlists.html', playlists=playlists_display)

# /playlists/<int:playlist_id>
@app.route('/playlists/<int:playlist_id>', methods=['GET', 'POST'])
def playlist_details(playlist_id):
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()
    songs = load_songs()

    playlist = get_playlist_by_id(playlist_id, playlists)
    if not playlist:
        abort(404)

    if request.method == 'POST':
        # Handle remove song or delete playlist
        if 'remove_song_id' in request.form:
            try:
                song_id_to_remove = int(request.form['remove_song_id'])
            except ValueError:
                song_id_to_remove = None

            if song_id_to_remove is not None:
                # Remove the entry for this song in this playlist
                playlist_songs = [ps for ps in playlist_songs if not (ps['playlist_id'] == playlist_id and ps['song_id'] == song_id_to_remove)]
                # Update total_songs count
                playlist['total_songs'] -= 1 if playlist['total_songs'] > 0 else 0
                # Save playlist songs and playlists
                save_playlist_songs(playlist_songs)
                # Update playlists file
                save_playlists(playlists)

        elif 'delete_playlist' in request.form:
            # Delete playlist and all playlist_songs
            playlists = [p for p in playlists if p['playlist_id'] != playlist_id]
            playlist_songs = [ps for ps in playlist_songs if ps['playlist_id'] != playlist_id]
            save_playlists(playlists)
            save_playlist_songs(playlist_songs)
            return redirect(url_for('playlists'))

        # After POST, reload playlist songs
        playlist_songs = load_playlist_songs()

    songs_in_playlist = get_songs_in_playlist(playlist_id, playlist_songs, songs)

    return render_template('playlist_detail.html', playlist=playlist, songs=songs_in_playlist)

# /playlists/create
@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'GET':
        return render_template('create_playlist.html')
    else:  # POST
        title = request.form.get('playlist-name-input', '').strip()
        description = request.form.get('playlist-description-input', '').strip()
        if not title:
            # simple validation: title required
            return render_template('create_playlist.html', error='Playlist title is required', playlist_name=title, playlist_description=description)

        playlists = load_playlists()
        new_id = get_next_id(playlists, 'playlist_id')
        creation_date = datetime.now().date().isoformat()

        new_playlist = {
            'playlist_id': new_id,
            'title': title,
            'description': description,
            'creation_date': creation_date,
            'total_songs': 0
        }

        playlists.append(new_playlist)
        save_playlists(playlists)

        return redirect(url_for('playlist_details', playlist_id=new_id))

# /albums
@app.route('/albums')
def albums_list():
    albums = load_albums()
    artists = load_artists()

    search_query = request.args.get('search', '').strip()
    sort_option = request.args.get('sort', 'title')

    filtered_albums = []
    for album in albums:
        artist_name = get_artist_name(album['artist_id'], artists)
        # Filter by search query in album title or artist name
        match_query = True
        if search_query:
            low_query = search_query.lower()
            if low_query not in album['title'].lower() and low_query not in artist_name.lower():
                match_query = False
        if match_query:
            album_copy = dict(album)
            album_copy['artist_name'] = artist_name
            filtered_albums.append(album_copy)

    # Sort albums by sort_option: title or release_year
    if sort_option == 'title':
        filtered_albums.sort(key=lambda a: a['title'].lower())
    elif sort_option == 'release_year':
        filtered_albums.sort(key=lambda a: a['release_year'])

    return render_template('albums.html', albums=filtered_albums, search_query=search_query, sort_option=sort_option)

# /albums/<int:album_id>
@app.route('/albums/<int:album_id>', methods=['GET', 'POST'])
def album_details(album_id):
    albums = load_albums()
    artists = load_artists()
    songs = load_songs()
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()

    album = None
    for a in albums:
        if a['album_id'] == album_id:
            album = a
            break
    if not album:
        abort(404)

    artist_name = get_artist_name(album['artist_id'], artists)
    album_copy = dict(album)
    album_copy['artist_name'] = artist_name

    # Get all songs in album
    album_songs = []
    for song in songs:
        if song['album_id'] == album_id:
            artist_name_song = get_artist_name(song['artist_id'], artists)
            song_copy = dict(song)
            song_copy['artist_name'] = artist_name_song
            album_songs.append(song_copy)

    if request.method == 'POST':
        # Adding all album songs to a playlist
        playlist_id_raw = request.form.get('playlist_id')
        try:
            playlist_id = int(playlist_id_raw)
        except (ValueError, TypeError):
            playlist_id = None

        if playlist_id is None or get_playlist_by_id(playlist_id, playlists) is None:
            # Invalid playlist id: ignore post
            return render_template('album_detail.html', album=album_copy, songs=album_songs)

        # Load current playlist songs
        existing_ps = [ps for ps in playlist_songs if ps['playlist_id'] == playlist_id]
        existing_song_ids = set(ps['song_id'] for ps in existing_ps)

        max_ps_id = get_next_id(playlist_songs, 'playlist_song_id')
        added_any = False
        for song in album_songs:
            if song['song_id'] not in existing_song_ids:
                new_ps = {
                    'playlist_song_id': max_ps_id,
                    'playlist_id': playlist_id,
                    'song_id': song['song_id'],
                    'added_date': datetime.now().date().isoformat()
                }
                playlist_songs.append(new_ps)
                max_ps_id += 1
                added_any = True

        if added_any:
            # Update playlist total_songs
            playlists_found = [p for p in playlists if p['playlist_id'] == playlist_id]
            if playlists_found:
                p = playlists_found[0]
                p['total_songs'] = p.get('total_songs', 0) + len(album_songs)

            save_playlist_songs(playlist_songs)
            save_playlists(playlists)

        return redirect(url_for('playlist_details', playlist_id=playlist_id))

    return render_template('album_detail.html', album=album_copy, songs=album_songs)

# /artists
@app.route('/artists')
def artists_list():
    artists = load_artists()
    search_query = request.args.get('search_query', '').strip()
    sort_option = request.args.get('sort_option', 'name')

    # Support filter parameter for trending (not explicitly in spec but from dashboard comments)
    filter_value = request.args.get('filter', '').lower()

    filtered_artists = []
    for artist in artists:
        # Filter by search
        match_query = True
        if search_query:
            if search_query.lower() not in artist['name'].lower():
                match_query = False

        # Filter by trending: take top 5 by formation_year descending
        if filter_value == 'trending':
            # We'll handle below by sorting and slicing
            pass
        if match_query:
            filtered_artists.append(artist)

    # Sort by sort_option
    if sort_option == 'name':
        filtered_artists.sort(key=lambda a: a['name'].lower())
    elif sort_option == 'formation_year':
        filtered_artists.sort(key=lambda a: a['formation_year'], reverse=True)

    if filter_value == 'trending':
        filtered_artists = sorted(filtered_artists, key=lambda a: a['formation_year'], reverse=True)[:5]

    return render_template('artists.html', artists=filtered_artists, search_query=search_query, sort_option=sort_option)

# /artists/<int:artist_id>
@app.route('/artists/<int:artist_id>')
def artist_profile(artist_id):
    artists = load_artists()
    albums = load_albums()
    songs = load_songs()

    artist = None
    for a in artists:
        if a['artist_id'] == artist_id:
            artist = a
            break
    if not artist:
        abort(404)

    # Albums of this artist
    artist_albums = [alb for alb in albums if alb['artist_id'] == artist_id]

    # Songs of this artist
    artist_songs = [s for s in songs if s['artist_id'] == artist_id]
    for s in artist_songs:
        s['artist_name'] = artist['name']
        album_name = get_album_name(s['album_id'], albums)
        s['album_name'] = album_name

    return render_template('artist_profile.html', artist=artist, albums=artist_albums, songs=artist_songs)

# /genres
@app.route('/genres')
def genres_page():
    genres = load_genres()

    selected_genre_id_raw = request.args.get('genre')
    selected_genre_id = None
    try:
        selected_genre_id = int(selected_genre_id_raw) if selected_genre_id_raw else None
    except ValueError:
        selected_genre_id = None

    genre = None
    genre_songs = []
    genre_artists = []

    if selected_genre_id is not None:
        # find genre
        for g in genres:
            if g['genre_id'] == selected_genre_id:
                genre = g
                break

    if genre:
        # Filter songs by genre name
        songs = load_songs()
        artists = load_artists()
        matching_songs = []
        artist_ids = set()
        for song in songs:
            if song['genre'].lower() == genre['genre_name'].lower():
                artist_ids.add(song['artist_id'])
                # Augment song info
                artist_name = get_artist_name(song['artist_id'], artists)
                song_copy = dict(song)
                song_copy['artist_name'] = artist_name
                matching_songs.append(song_copy)

        # Get artists matching
        all_artists = [a for a in load_artists() if a['artist_id'] in artist_ids]

        genre_songs = matching_songs
        genre_artists = all_artists

    return render_template('genres.html', genres=genres, selected_genre_id=selected_genre_id, genre_songs=genre_songs, genre_artists=genre_artists)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
