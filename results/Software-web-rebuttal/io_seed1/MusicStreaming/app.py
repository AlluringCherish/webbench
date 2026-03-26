'''
Backend implementation for MusicStreaming web application.
Provides routing and data handling for all pages and functionalities.
Data is stored in local text files under the 'data' directory.
The website starts at the Dashboard page ('/').
Ensures a default playlist with playlist_id='1' exists on startup for adding songs from song catalog.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
# Utility functions for reading and writing data files
def read_songs():
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
            if len(parts) != 8:
                continue
            song = {
                'song_id': parts[0],
                'title': parts[1],
                'artist_id': parts[2],
                'album_id': parts[3],
                'genre': parts[4],
                'duration': int(parts[5]),
                'release_date': parts[6],
                'play_count': int(parts[7])
            }
            songs.append(song)
    return songs
def write_songs(songs):
    path = os.path.join(DATA_DIR, 'songs.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for s in songs:
            line = '|'.join([
                s['song_id'],
                s['title'],
                s['artist_id'],
                s['album_id'],
                s['genre'],
                str(s['duration']),
                s['release_date'],
                str(s['play_count'])
            ])
            f.write(line + '\n')
def read_artists():
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
            if len(parts) != 5:
                continue
            artist = {
                'artist_id': parts[0],
                'name': parts[1],
                'genre': parts[2],
                'country': parts[3],
                'formation_year': parts[4]
            }
            artists.append(artist)
    return artists
def write_artists(artists):
    path = os.path.join(DATA_DIR, 'artists.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for a in artists:
            line = '|'.join([
                a['artist_id'],
                a['name'],
                a['genre'],
                a['country'],
                a['formation_year']
            ])
            f.write(line + '\n')
def read_albums():
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
            if len(parts) != 6:
                continue
            album = {
                'album_id': parts[0],
                'title': parts[1],
                'artist_id': parts[2],
                'release_year': parts[3],
                'total_songs': int(parts[4]),
                'genre': parts[5]
            }
            albums.append(album)
    return albums
def write_albums(albums):
    path = os.path.join(DATA_DIR, 'albums.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for a in albums:
            line = '|'.join([
                a['album_id'],
                a['title'],
                a['artist_id'],
                a['release_year'],
                str(a['total_songs']),
                a['genre']
            ])
            f.write(line + '\n')
def read_genres():
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
            if len(parts) != 3:
                continue
            genre = {
                'genre_id': parts[0],
                'genre_name': parts[1],
                'description': parts[2]
            }
            genres.append(genre)
    return genres
def write_genres(genres):
    path = os.path.join(DATA_DIR, 'genres.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for g in genres:
            line = '|'.join([
                g['genre_id'],
                g['genre_name'],
                g['description']
            ])
            f.write(line + '\n')
def read_playlists():
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
            if len(parts) != 5:
                continue
            playlist = {
                'playlist_id': parts[0],
                'title': parts[1],
                'description': parts[2],
                'creation_date': parts[3],
                'total_songs': int(parts[4])
            }
            playlists.append(playlist)
    return playlists
def write_playlists(playlists):
    path = os.path.join(DATA_DIR, 'playlists.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for p in playlists:
            line = '|'.join([
                p['playlist_id'],
                p['title'],
                p['description'],
                p['creation_date'],
                str(p['total_songs'])
            ])
            f.write(line + '\n')
def read_playlist_songs():
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
            if len(parts) != 4:
                continue
            ps = {
                'playlist_song_id': parts[0],
                'playlist_id': parts[1],
                'song_id': parts[2],
                'added_date': parts[3]
            }
            playlist_songs.append(ps)
    return playlist_songs
def write_playlist_songs(playlist_songs):
    path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for ps in playlist_songs:
            line = '|'.join([
                ps['playlist_song_id'],
                ps['playlist_id'],
                ps['song_id'],
                ps['added_date']
            ])
            f.write(line + '\n')
# Helper functions to get entities by id
def get_artist_by_id(artist_id):
    artists = read_artists()
    for artist in artists:
        if artist['artist_id'] == artist_id:
            return artist
    return None
def get_album_by_id(album_id):
    albums = read_albums()
    for album in albums:
        if album['album_id'] == album_id:
            return album
    return None
def get_song_by_id(song_id):
    songs = read_songs()
    for song in songs:
        if song['song_id'] == song_id:
            return song
    return None
def get_playlist_by_id(playlist_id):
    playlists = read_playlists()
    for playlist in playlists:
        if playlist['playlist_id'] == playlist_id:
            return playlist
    return None
def get_genre_by_name(genre_name):
    genres = read_genres()
    for genre in genres:
        if genre['genre_name'].lower() == genre_name.lower():
            return genre
    return None
def get_next_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            val = int(item[id_key])
            if val > max_id:
                max_id = val
        except:
            continue
    return str(max_id + 1)
def ensure_default_playlist():
    '''
    Ensure that a default playlist with playlist_id='1' exists.
    If not, create it with a default title and description.
    '''
    playlists = read_playlists()
    for p in playlists:
        if p['playlist_id'] == '1':
            return  # Exists
    # Create default playlist with id '1'
    creation_date = datetime.now().strftime('%Y-%m-%d')
    default_playlist = {
        'playlist_id': '1',
        'title': 'Default Playlist',
        'description': 'This is the default playlist.',
        'creation_date': creation_date,
        'total_songs': 0
    }
    playlists.append(default_playlist)
    write_playlists(playlists)
# Routes
@app.route('/')
def dashboard():
    # Show featured songs (top 5 by play_count)
    songs = read_songs()
    artists = read_artists()
    # Sort songs by play_count descending
    featured_songs = sorted(songs, key=lambda s: s['play_count'], reverse=True)[:5]
    # Add artist name to each song
    for song in featured_songs:
        artist = get_artist_by_id(song['artist_id'])
        song['artist_name'] = artist['name'] if artist else 'Unknown'
    # Trending artists (top 5 by total play_count of their songs)
    artist_play_counts = {}
    for song in songs:
        aid = song['artist_id']
        artist_play_counts[aid] = artist_play_counts.get(aid, 0) + song['play_count']
    trending_artist_ids = sorted(artist_play_counts, key=artist_play_counts.get, reverse=True)[:5]
    trending_artists = []
    for aid in trending_artist_ids:
        artist = get_artist_by_id(aid)
        if artist:
            trending_artists.append(artist)
    return render_template('dashboard.html',
                           featured_songs=featured_songs,
                           trending_artists=trending_artists)
@app.route('/songs', methods=['GET'])
def song_catalog():
    songs = read_songs()
    artists = read_artists()
    albums = read_albums()
    genres = read_genres()
    playlists = read_playlists()
    # Get search and filter parameters
    search_query = request.args.get('search', '').strip().lower()
    genre_filter = request.args.get('genre', '').strip()
    filtered_songs = []
    for song in songs:
        artist = get_artist_by_id(song['artist_id'])
        album = get_album_by_id(song['album_id'])
        # Check search filter
        if search_query:
            if (search_query not in song['title'].lower() and
                (artist is None or search_query not in artist['name'].lower()) and
                (album is None or search_query not in album['title'].lower())):
                continue
        # Check genre filter
        if genre_filter and genre_filter.lower() != song['genre'].lower():
            continue
        # Add artist and album names for display
        song['artist_name'] = artist['name'] if artist else 'Unknown'
        song['album_title'] = album['title'] if album else 'Unknown'
        filtered_songs.append(song)
    # Sort songs by title ascending
    filtered_songs.sort(key=lambda s: s['title'].lower())
    genre_names = [g['genre_name'] for g in genres]
    return render_template('song_catalog.html',
                           songs=filtered_songs,
                           genres=genre_names,
                           selected_genre=genre_filter,
                           search_query=search_query,
                           playlists=playlists)
@app.route('/songs/<song_id>', methods=['GET'])
def song_details(song_id):
    song = get_song_by_id(song_id)
    if not song:
        return "Song not found", 404
    artist = get_artist_by_id(song['artist_id'])
    album = get_album_by_id(song['album_id'])
    # Add artist and album names
    song['artist_name'] = artist['name'] if artist else 'Unknown'
    song['album_title'] = album['title'] if album else 'Unknown'
    return render_template('song_details.html', song=song)
@app.route('/playlists', methods=['GET'])
def playlists():
    playlists = read_playlists()
    # For each playlist, we can show cover (not specified, so skip), title, song count
    return render_template('playlists.html', playlists=playlists)
@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'POST':
        title = request.form.get('playlist-name-input', '').strip()
        description = request.form.get('playlist-description-input', '').strip()
        if not title:
            error = "Playlist name is required."
            return render_template('create_playlist.html', error=error, title=title, description=description)
        playlists = read_playlists()
        new_id = get_next_id(playlists, 'playlist_id')
        creation_date = datetime.now().strftime('%Y-%m-%d')
        new_playlist = {
            'playlist_id': new_id,
            'title': title,
            'description': description,
            'creation_date': creation_date,
            'total_songs': 0
        }
        playlists.append(new_playlist)
        write_playlists(playlists)
        return redirect(url_for('playlists'))
    else:
        return render_template('create_playlist.html')
@app.route('/playlists/<playlist_id>', methods=['GET'])
def playlist_details(playlist_id):
    playlist = get_playlist_by_id(playlist_id)
    if not playlist:
        return "Playlist not found", 404
    playlist_songs = read_playlist_songs()
    songs = read_songs()
    artists = read_artists()
    # Get songs in this playlist
    songs_in_playlist = []
    for ps in playlist_songs:
        if ps['playlist_id'] == playlist_id:
            song = get_song_by_id(ps['song_id'])
            if song:
                artist = get_artist_by_id(song['artist_id'])
                song_display = {
                    'song_id': song['song_id'],
                    'title': song['title'],
                    'artist_name': artist['name'] if artist else 'Unknown',
                    'duration': song['duration']
                }
                songs_in_playlist.append(song_display)
    return render_template('playlist_details.html',
                           playlist=playlist,
                           songs_in_playlist=songs_in_playlist)
@app.route('/playlists/<playlist_id>/delete', methods=['POST'])
def delete_playlist(playlist_id):
    playlists = read_playlists()
    playlist_songs = read_playlist_songs()
    playlists = [p for p in playlists if p['playlist_id'] != playlist_id]
    playlist_songs = [ps for ps in playlist_songs if ps['playlist_id'] != playlist_id]
    write_playlists(playlists)
    write_playlist_songs(playlist_songs)
    return redirect(url_for('playlists'))
@app.route('/playlists/<playlist_id>/remove_song/<song_id>', methods=['POST'])
def remove_song_from_playlist(playlist_id, song_id):
    playlist_songs = read_playlist_songs()
    new_playlist_songs = []
    removed = False
    for ps in playlist_songs:
        if ps['playlist_id'] == playlist_id and ps['song_id'] == song_id and not removed:
            removed = True
            continue
        new_playlist_songs.append(ps)
    if removed:
        write_playlist_songs(new_playlist_songs)
        # Update total_songs in playlists.txt
        playlists = read_playlists()
        for p in playlists:
            if p['playlist_id'] == playlist_id:
                p['total_songs'] = max(0, p['total_songs'] - 1)
                break
        write_playlists(playlists)
    return redirect(url_for('playlist_details', playlist_id=playlist_id))
@app.route('/playlists/<playlist_id>/add_song/<song_id>', methods=['POST'])
def add_song_to_playlist(playlist_id, song_id):
    # Check if playlist and song exist
    playlist = get_playlist_by_id(playlist_id)
    song = get_song_by_id(song_id)
    if not playlist or not song:
        return "Playlist or Song not found", 404
    playlist_songs = read_playlist_songs()
    # Check if song already in playlist
    for ps in playlist_songs:
        if ps['playlist_id'] == playlist_id and ps['song_id'] == song_id:
            # Already in playlist, do nothing
            return redirect(request.referrer or url_for('song_catalog'))
    new_id = get_next_id(playlist_songs, 'playlist_song_id')
    added_date = datetime.now().strftime('%Y-%m-%d')
    new_ps = {
        'playlist_song_id': new_id,
        'playlist_id': playlist_id,
        'song_id': song_id,
        'added_date': added_date
    }
    playlist_songs.append(new_ps)
    write_playlist_songs(playlist_songs)
    # Update total_songs in playlists.txt
    playlists = read_playlists()
    for p in playlists:
        if p['playlist_id'] == playlist_id:
            p['total_songs'] += 1
            break
    write_playlists(playlists)
    return redirect(request.referrer or url_for('song_catalog'))
@app.route('/albums', methods=['GET'])
def albums():
    albums = read_albums()
    artists = read_artists()
    search_query = request.args.get('search', '').strip().lower()
    sort_option = request.args.get('sort', 'By Title')
    filtered_albums = []
    for album in albums:
        artist = get_artist_by_id(album['artist_id'])
        if search_query:
            if (search_query not in album['title'].lower() and
                (artist is None or search_query not in artist['name'].lower())):
                continue
        album['artist_name'] = artist['name'] if artist else 'Unknown'
        filtered_albums.append(album)
    if sort_option == 'By Title':
        filtered_albums.sort(key=lambda a: a['title'].lower())
    elif sort_option == 'By Artist':
        filtered_albums.sort(key=lambda a: a['artist_name'].lower())
    elif sort_option == 'By Year':
        filtered_albums.sort(key=lambda a: a['release_year'])
    return render_template('albums.html',
                           albums=filtered_albums,
                           search_query=search_query,
                           sort_option=sort_option)
@app.route('/albums/<album_id>', methods=['GET'])
def album_details(album_id):
    album = get_album_by_id(album_id)
    if not album:
        return "Album not found", 404
    artist = get_artist_by_id(album['artist_id'])
    songs = read_songs()
    album_songs = [s for s in songs if s['album_id'] == album_id]
    # Add artist name to songs
    for s in album_songs:
        s['artist_name'] = artist['name'] if artist else 'Unknown'
    playlists = read_playlists()  # Added to provide playlists to template
    return render_template('album_details.html',
                           album=album,
                           artist=artist,
                           album_songs=album_songs,
                           playlists=playlists)  # Pass playlists to template
@app.route('/albums/<album_id>/add_to_playlist', methods=['POST'])
def add_album_to_playlist(album_id):
    playlist_id = request.form.get('playlist_id')
    if not playlist_id:
        return "Playlist ID required", 400
    album = get_album_by_id(album_id)
    playlist = get_playlist_by_id(playlist_id)
    if not album or not playlist:
        return "Album or Playlist not found", 404
    songs = read_songs()
    playlist_songs = read_playlist_songs()
    # Get songs in album
    album_songs = [s for s in songs if s['album_id'] == album_id]
    # Add songs to playlist if not already present
    existing_song_ids = set(ps['song_id'] for ps in playlist_songs if ps['playlist_id'] == playlist_id)
    added_count = 0
    next_id = int(get_next_id(playlist_songs, 'playlist_song_id'))
    added_date = datetime.now().strftime('%Y-%m-%d')
    for song in album_songs:
        if song['song_id'] not in existing_song_ids:
            ps = {
                'playlist_song_id': str(next_id),
                'playlist_id': playlist_id,
                'song_id': song['song_id'],
                'added_date': added_date
            }
            playlist_songs.append(ps)
            next_id += 1
            added_count += 1
    if added_count > 0:
        write_playlist_songs(playlist_songs)
        # Update total_songs in playlists.txt
        playlists = read_playlists()
        for p in playlists:
            if p['playlist_id'] == playlist_id:
                p['total_songs'] += added_count
                break
        write_playlists(playlists)
    return redirect(url_for('album_details', album_id=album_id))
@app.route('/artists', methods=['GET'])
def artists():
    artists = read_artists()
    search_query = request.args.get('search', '').strip().lower()
    sort_option = request.args.get('sort', 'By Name')
    filtered_artists = []
    for artist in artists:
        if search_query and search_query not in artist['name'].lower():
            continue
        filtered_artists.append(artist)
    if sort_option == 'By Name':
        filtered_artists.sort(key=lambda a: a['name'].lower())
    elif sort_option == 'By Genre':
        filtered_artists.sort(key=lambda a: a['genre'].lower())
    return render_template('artists.html',
                           artists=filtered_artists,
                           search_query=search_query,
                           sort_option=sort_option)
@app.route('/artists/<artist_id>', methods=['GET'])
def artist_profile(artist_id):
    artist = get_artist_by_id(artist_id)
    if not artist:
        return "Artist not found", 404
    songs = read_songs()
    albums = read_albums()
    artist_songs = [s for s in songs if s['artist_id'] == artist_id]
    artist_albums = [a for a in albums if a['artist_id'] == artist_id]
    return render_template('artists.html', artist=artist, artist_songs=artist_songs, artist_albums=artist_albums)
@app.route('/genres', methods=['GET'])
def genres():
    genres = read_genres()
    selected_genre_name = request.args.get('genre', '').strip()
    songs = read_songs()
    artists = read_artists()
    genre_songs = []
    genre_artists = []
    if selected_genre_name:
        # Filter songs by genre
        genre_songs = [s for s in songs if s['genre'].lower() == selected_genre_name.lower()]
        # Filter artists by genre
        genre_artists = [a for a in artists if a['genre'].lower() == selected_genre_name.lower()]
        # Add artist names to songs
        for s in genre_songs:
            artist = get_artist_by_id(s['artist_id'])
            s['artist_name'] = artist['name'] if artist else 'Unknown'
    genre_names = [g['genre_name'] for g in genres]
    return render_template('genres.html',
                           genres=genres,
                           genre_names=genre_names,
                           selected_genre=selected_genre_name,
                           genre_songs=genre_songs,
                           genre_artists=genre_artists)
# Navigation buttons redirect routes
@app.route('/dashboard')
def redirect_dashboard():
    return redirect(url_for('dashboard'))
@app.route('/back_to_dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard'))
# Ensure default playlist exists on startup
ensure_default_playlist()
# Run the app
if __name__ == '__main__':
    app.run(port=5000, debug=True)