'''
app.py
Main Flask application implementing backend logic for the MusicStreaming app.
Handles routing for all pages, reads and writes local text files for data storage,
and integrates with frontend templates. Implements search, filtering, playlist
management, and navigation functionalities as specified in the requirements.
Includes an API endpoint to provide playlists as JSON for frontend usage.
'''
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
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
            psong = {
                'playlist_song_id': parts[0],
                'playlist_id': parts[1],
                'song_id': parts[2],
                'added_date': parts[3]
            }
            playlist_songs.append(psong)
    return playlist_songs
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
def get_artist_by_id(artist_id, artists):
    for artist in artists:
        if artist['artist_id'] == artist_id:
            return artist
    return None
def get_album_by_id(album_id, albums):
    for album in albums:
        if album['album_id'] == album_id:
            return album
    return None
def get_playlist_by_id(playlist_id, playlists):
    for playlist in playlists:
        if playlist['playlist_id'] == playlist_id:
            return playlist
    return None
def format_duration(seconds):
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"
def get_next_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            val = int(item[id_key])
            if val > max_id:
                max_id = val
        except ValueError:
            continue
    return str(max_id + 1)
@app.route('/')
def dashboard():
    songs = read_songs()
    artists = read_artists()
    albums = read_albums()
    genres = read_genres()
    # Calculate play counts per artist
    artist_play_counts = {}
    for song in songs:
        artist_play_counts[song['artist_id']] = artist_play_counts.get(song['artist_id'], 0) + song['play_count']
    # Get trending artists sorted by play count descending
    trending_artist_ids = sorted(artist_play_counts, key=artist_play_counts.get, reverse=True)[:5]
    trending_artists = []
    for aid in trending_artist_ids:
        artist = get_artist_by_id(aid, artists)
        if artist:
            trending_artists.append(artist)
    # Featured songs: top 5 by play count
    featured_songs = sorted(songs, key=lambda s: s['play_count'], reverse=True)[:5]
    for song in featured_songs:
        artist = get_artist_by_id(song['artist_id'], artists)
        album = get_album_by_id(song['album_id'], albums)
        song['artist_name'] = artist['name'] if artist else 'Unknown Artist'
        song['album_title'] = album['title'] if album else 'Unknown Album'
        song['duration_formatted'] = format_duration(song['duration'])
    return render_template('dashboard.html',
                           featured_songs=featured_songs,
                           trending_artists=trending_artists)
@app.route('/songs')
def song_catalog():
    songs = read_songs()
    artists = read_artists()
    albums = read_albums()
    genres = read_genres()
    search_query = request.args.get('search', '').strip().lower()
    genre_filter = request.args.get('genre', '')
    filtered_songs = []
    for song in songs:
        artist = get_artist_by_id(song['artist_id'], artists)
        album = get_album_by_id(song['album_id'], albums)
        searchable_text = f"{song['title']} {artist['name'] if artist else ''} {album['title'] if album else ''}".lower()
        if search_query and search_query not in searchable_text:
            continue
        if genre_filter and genre_filter != 'All' and song['genre'] != genre_filter:
            continue
        song_display = song.copy()
        song_display['artist_name'] = artist['name'] if artist else 'Unknown Artist'
        song_display['album_title'] = album['title'] if album else 'Unknown Album'
        song_display['duration_formatted'] = format_duration(song['duration'])
        filtered_songs.append(song_display)
    genre_names = [g['genre_name'] for g in genres]
    genre_names.insert(0, 'All')
    return render_template('song_catalog.html',
                           songs=filtered_songs,
                           genres=genres,
                           selected_genre=genre_filter,
                           genre_names=genre_names,
                           search_query=search_query)
@app.route('/songs/<song_id>')
def song_details(song_id):
    songs = read_songs()
    artists = read_artists()
    albums = read_albums()
    song = next((s for s in songs if s['song_id'] == song_id), None)
    if not song:
        return "Song not found", 404
    artist = get_artist_by_id(song['artist_id'], artists)
    album = get_album_by_id(song['album_id'], albums)
    song_display = song.copy()
    song_display['artist_name'] = artist['name'] if artist else 'Unknown Artist'
    song_display['album_title'] = album['title'] if album else 'Unknown Album'
    song_display['duration_formatted'] = format_duration(song['duration'])
    return render_template('song_details.html', song=song_display)
@app.route('/playlists')
def playlists():
    playlists = read_playlists()
    playlists.sort(key=lambda x: x['creation_date'], reverse=True)
    return render_template('playlists.html', playlists=playlists)
@app.route('/playlists/<playlist_id>')
def playlist_details(playlist_id):
    playlists = read_playlists()
    playlist_songs = read_playlist_songs()
    songs = read_songs()
    artists = read_artists()
    playlist = get_playlist_by_id(playlist_id, playlists)
    if not playlist:
        return "Playlist not found", 404
    psongs = [ps for ps in playlist_songs if ps['playlist_id'] == playlist_id]
    psongs.sort(key=lambda x: x['added_date'])
    songs_in_playlist = []
    for ps in psongs:
        song = next((s for s in songs if s['song_id'] == ps['song_id']), None)
        if not song:
            continue
        artist = get_artist_by_id(song['artist_id'], artists)
        song_display = {
            'song_id': song['song_id'],
            'title': song['title'],
            'artist_name': artist['name'] if artist else 'Unknown Artist',
            'duration_formatted': format_duration(song['duration'])
        }
        songs_in_playlist.append(song_display)
    return render_template('playlist_details.html',
                           playlist=playlist,
                           songs=songs_in_playlist)
@app.route('/playlists/<playlist_id>/remove_song/<song_id>')
def remove_song_from_playlist(playlist_id, song_id):
    playlists = read_playlists()
    playlist_songs = read_playlist_songs()
    playlist = get_playlist_by_id(playlist_id, playlists)
    if not playlist:
        return "Playlist not found", 404
    original_len = len(playlist_songs)
    playlist_songs = [ps for ps in playlist_songs if not (ps['playlist_id'] == playlist_id and ps['song_id'] == song_id)]
    if len(playlist_songs) == original_len:
        # Song not found in playlist
        return redirect(url_for('playlist_details', playlist_id=playlist_id))
    # Update total songs count
    playlist['total_songs'] = max(0, playlist['total_songs'] - 1)
    # Write updated data
    write_playlist_songs(playlist_songs)
    write_playlists(playlists)
    return redirect(url_for('playlist_details', playlist_id=playlist_id))
@app.route('/playlists/<playlist_id>/delete', methods=['POST'])
def delete_playlist(playlist_id):
    playlists = read_playlists()
    playlist_songs = read_playlist_songs()
    playlists = [p for p in playlists if p['playlist_id'] != playlist_id]
    playlist_songs = [ps for ps in playlist_songs if ps['playlist_id'] != playlist_id]
    write_playlists(playlists)
    write_playlist_songs(playlist_songs)
    return redirect(url_for('playlists'))
@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'POST':
        title = request.form.get('playlist-name-input', '').strip()
        description = request.form.get('playlist-description-input', '').strip()
        if not title:
            error = "Playlist title is required."
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
    return render_template('create_playlist.html')
@app.route('/albums')
def albums():
    albums = read_albums()
    artists = read_artists()
    search_query = request.args.get('search', '').strip().lower()
    sort_option = request.args.get('sort', 'By Title')
    filtered_albums = []
    for album in albums:
        artist = get_artist_by_id(album['artist_id'], artists)
        searchable_text = f"{album['title']} {artist['name'] if artist else ''}".lower()
        if search_query and search_query not in searchable_text:
            continue
        album_display = album.copy()
        album_display['artist_name'] = artist['name'] if artist else 'Unknown Artist'
        filtered_albums.append(album_display)
    if sort_option == 'By Title':
        filtered_albums.sort(key=lambda x: x['title'].lower())
    elif sort_option == 'By Artist':
        filtered_albums.sort(key=lambda x: x['artist_name'].lower())
    elif sort_option == 'By Year':
        filtered_albums.sort(key=lambda x: x['release_year'])
    return render_template('albums.html',
                           albums=filtered_albums,
                           search_query=search_query,
                           sort_option=sort_option)
@app.route('/albums/<album_id>')
def album_details(album_id):
    albums = read_albums()
    artists = read_artists()
    songs = read_songs()
    album = get_album_by_id(album_id, albums)
    if not album:
        return "Album not found", 404
    artist = get_artist_by_id(album['artist_id'], artists)
    album_songs = [s for s in songs if s['album_id'] == album_id]
    album_songs.sort(key=lambda x: x['title'].lower())
    for song in album_songs:
        song['duration_formatted'] = format_duration(song['duration'])
        song['artist_name'] = artist['name'] if artist else 'Unknown Artist'
    album_display = album.copy()
    album_display['artist_name'] = artist['name'] if artist else 'Unknown Artist'
    return render_template('album_details.html',
                           album=album_display,
                           songs=album_songs)
@app.route('/albums/<album_id>/add_to_playlist', methods=['POST'])
def add_album_to_playlist(album_id):
    playlists = read_playlists()
    playlist_songs = read_playlist_songs()
    songs = read_songs()
    playlist_id = request.form.get('playlist_id', '').strip()
    playlist = get_playlist_by_id(playlist_id, playlists)
    if not playlist:
        return "Playlist not found", 404
    album_songs = [s for s in songs if s['album_id'] == album_id]
    existing_song_ids = {ps['song_id'] for ps in playlist_songs if ps['playlist_id'] == playlist_id}
    max_ps_id = 0
    for ps in playlist_songs:
        try:
            val = int(ps['playlist_song_id'])
            if val > max_ps_id:
                max_ps_id = val
        except ValueError:
            continue
    added_count = 0
    for song in album_songs:
        if song['song_id'] in existing_song_ids:
            continue
        max_ps_id += 1
        new_ps = {
            'playlist_song_id': str(max_ps_id),
            'playlist_id': playlist_id,
            'song_id': song['song_id'],
            'added_date': datetime.now().strftime('%Y-%m-%d')
        }
        playlist_songs.append(new_ps)
        added_count += 1
    playlist['total_songs'] += added_count
    write_playlist_songs(playlist_songs)
    write_playlists(playlists)
    return redirect(url_for('album_details', album_id=album_id))
@app.route('/artists')
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
        filtered_artists.sort(key=lambda x: x['name'].lower())
    elif sort_option == 'By Genre':
        filtered_artists.sort(key=lambda x: x['genre'].lower())
    return render_template('artists.html',
                           artists=filtered_artists,
                           search_query=search_query,
                           sort_option=sort_option)
@app.route('/artists/<artist_id>')
def artist_profile(artist_id):
    artists = read_artists()
    songs = read_songs()
    albums = read_albums()
    artist = get_artist_by_id(artist_id, artists)
    if not artist:
        return "Artist not found", 404
    artist_songs = [s for s in songs if s['artist_id'] == artist_id]
    artist_songs.sort(key=lambda x: x['title'].lower())
    for song in artist_songs:
        album = get_album_by_id(song['album_id'], albums)
        song['album_title'] = album['title'] if album else 'Unknown Album'
        song['duration_formatted'] = format_duration(song['duration'])
    artist_albums = [a for a in albums if a['artist_id'] == artist_id]
    artist_albums.sort(key=lambda x: x['release_year'], reverse=True)
    return render_template('artist_profile.html',
                           artist=artist,
                           songs=artist_songs,
                           albums=artist_albums)
@app.route('/genres')
def genres():
    genres = read_genres()
    artists = read_artists()
    songs = read_songs()
    selected_genre = request.args.get('genre', '')
    genre_names = [g['genre_name'] for g in genres]
    genre_artists = []
    if selected_genre:
        genre_songs = [s for s in songs if s['genre'] == selected_genre]
        artist_ids = set(s['artist_id'] for s in genre_songs)
        genre_artists = [a for a in artists if a['artist_id'] in artist_ids]
        genre_artists.sort(key=lambda x: x['name'].lower())
    return render_template('genres.html',
                           genres=genres,
                           genre_names=genre_names,
                           selected_genre=selected_genre,
                           genre_artists=genre_artists)
@app.route('/dashboard_redirect')
def redirect_dashboard():
    return redirect(url_for('dashboard'))
@app.route('/trending_artists_redirect')
def redirect_trending_artists():
    return redirect(url_for('dashboard'))
@app.route('/genres_back_to_dashboard')
def genres_back_to_dashboard():
    return redirect(url_for('dashboard'))
# Added route to handle adding a single song to a playlist via POST JSON request
@app.route('/playlists/add_song', methods=['POST'])
def add_song_to_playlist_single():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
    song_id = data.get('song_id')
    playlist_id = data.get('playlist_id')
    if not song_id or not playlist_id:
        return jsonify({'error': 'Missing song_id or playlist_id'}), 400
    playlists = read_playlists()
    playlist_songs = read_playlist_songs()
    songs = read_songs()
    playlist = get_playlist_by_id(playlist_id, playlists)
    if not playlist:
        return jsonify({'error': 'Playlist not found'}), 404
    song = next((s for s in songs if s['song_id'] == song_id), None)
    if not song:
        return jsonify({'error': 'Song not found'}), 404
    # Check if song already in playlist
    for ps in playlist_songs:
        if ps['playlist_id'] == playlist_id and ps['song_id'] == song_id:
            return jsonify({'error': 'Song already in playlist'}), 400
    max_ps_id = 0
    for ps in playlist_songs:
        try:
            val = int(ps['playlist_song_id'])
            if val > max_ps_id:
                max_ps_id = val
        except ValueError:
            continue
    max_ps_id += 1
    new_ps = {
        'playlist_song_id': str(max_ps_id),
        'playlist_id': playlist_id,
        'song_id': song_id,
        'added_date': datetime.now().strftime('%Y-%m-%d')
    }
    playlist_songs.append(new_ps)
    playlist['total_songs'] += 1
    write_playlist_songs(playlist_songs)
    write_playlists(playlists)
    return jsonify({'message': 'Song added to playlist successfully'}), 200
# New API endpoint to provide playlists as JSON for frontend usage
@app.route('/api/playlists')
def api_playlists():
    playlists = read_playlists()
    return jsonify(playlists)
if __name__ == '__main__':
    app.run(debug=True)