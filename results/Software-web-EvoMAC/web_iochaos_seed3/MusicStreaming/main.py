'''
Main backend application for MusicStreaming web application.
Implements routing, business logic, and data management using local text files.
'''
import os
from flask import Flask, render_template, request, redirect, url_for, abort
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
# Utility functions to read and write data files
def read_songs():
    songs = []
    path = os.path.join(DATA_DIR, 'songs.txt')
    if not os.path.exists(path):
        return songs
    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 8:
                continue
            try:
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
            except ValueError:
                continue
    return songs
def read_artists():
    artists = []
    path = os.path.join(DATA_DIR, 'artists.txt')
    if not os.path.exists(path):
        return artists
    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
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
    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
                continue
            try:
                album = {
                    'album_id': parts[0],
                    'title': parts[1],
                    'artist_id': parts[2],
                    'release_year': parts[3],
                    'total_songs': int(parts[4]),
                    'genre': parts[5]
                }
                albums.append(album)
            except ValueError:
                continue
    return albums
def read_genres():
    genres = []
    path = os.path.join(DATA_DIR, 'genres.txt')
    if not os.path.exists(path):
        return genres
    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
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
    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 5:
                continue
            try:
                playlist = {
                    'playlist_id': parts[0],
                    'title': parts[1],
                    'description': parts[2],
                    'creation_date': parts[3],
                    'total_songs': int(parts[4])
                }
                playlists.append(playlist)
            except ValueError:
                continue
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
    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
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
def generate_new_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            current_id = int(item[id_key])
            if current_id > max_id:
                max_id = current_id
        except (ValueError, KeyError):
            continue
    return str(max_id + 1)
def format_duration(seconds):
    minutes = seconds // 60
    sec = seconds % 60
    return f"{minutes}:{sec:02d}"
# Routes implementation
@app.route('/')
def dashboard():
    # Featured songs: top 5 by play_count descending
    songs = read_songs()
    artists = read_artists()
    # Enrich songs with artist name
    artist_dict = {a['artist_id']: a['name'] for a in artists}
    for song in songs:
        song['artist_name'] = artist_dict.get(song['artist_id'], 'Unknown Artist')
    featured_songs = sorted(songs, key=lambda s: s['play_count'], reverse=True)[:5]
    # Trending artists: top 5 by total play_count of their songs
    artist_play_counts = {}
    for song in songs:
        artist_play_counts[song['artist_id']] = artist_play_counts.get(song['artist_id'], 0) + song['play_count']
    trending_artist_ids = sorted(artist_play_counts, key=artist_play_counts.get, reverse=True)[:5]
    trending_artists = [get_artist_by_id(aid) for aid in trending_artist_ids if get_artist_by_id(aid) is not None]
    return render_template('dashboard.html',
                           featured_songs=featured_songs,
                           trending_artists=trending_artists)
@app.route('/songs')
def song_catalog():
    songs = read_songs()
    artists = read_artists()
    albums = read_albums()
    genres = read_genres()
    # Enrich songs with artist name and album title
    artist_dict = {a['artist_id']: a['name'] for a in artists}
    album_dict = {al['album_id']: al['title'] for al in albums}
    for song in songs:
        song['artist_name'] = artist_dict.get(song['artist_id'], 'Unknown Artist')
        song['album_title'] = album_dict.get(song['album_id'], 'Unknown Album')
        song['duration_formatted'] = format_duration(song['duration'])
    # Search and filter
    search_query = request.args.get('search', '').strip().lower()
    genre_filter = request.args.get('genre', '').strip().lower()
    filtered_songs = []
    for song in songs:
        matches_search = True
        matches_genre = True
        if search_query:
            if (search_query not in song['title'].lower() and
                search_query not in song['artist_name'].lower() and
                search_query not in song['album_title'].lower()):
                matches_search = False
        if genre_filter and genre_filter != 'all':
            if song['genre'].lower() != genre_filter:
                matches_genre = False
        if matches_search and matches_genre:
            filtered_songs.append(song)
    # Prepare genre options for dropdown
    genre_names = [g['genre_name'] for g in genres]
    genre_names = sorted(genre_names)
    return render_template('song_catalog.html',
                           songs=filtered_songs,
                           search_query=search_query,
                           genre_filter=genre_filter,
                           genres=genre_names)
@app.route('/songs/<song_id>')
def song_details(song_id):
    song = get_song_by_id(song_id)
    if not song:
        abort(404)
    artist = get_artist_by_id(song['artist_id'])
    album = get_album_by_id(song['album_id'])
    song['duration_formatted'] = format_duration(song['duration'])
    return render_template('song_details.html',
                           song=song,
                           artist=artist,
                           album=album)
@app.route('/playlists')
def playlists():
    playlists = read_playlists()
    # Enrich playlists with cover art (from first song's album cover if possible)
    # For simplicity, we won't implement cover art here, just pass playlists
    return render_template('playlists.html', playlists=playlists)
@app.route('/playlists/<playlist_id>')
def playlist_details(playlist_id):
    playlist = get_playlist_by_id(playlist_id)
    if not playlist:
        abort(404)
    playlist_songs = read_playlist_songs()
    songs = read_songs()
    artists = read_artists()
    artist_dict = {a['artist_id']: a['name'] for a in artists}
    # Get songs in this playlist
    songs_in_playlist = []
    for ps in playlist_songs:
        if ps['playlist_id'] == playlist_id:
            song = get_song_by_id(ps['song_id'])
            if song:
                song_copy = song.copy()
                song_copy['duration_formatted'] = format_duration(song_copy['duration'])
                song_copy['artist_name'] = artist_dict.get(song_copy['artist_id'], 'Unknown Artist')
                songs_in_playlist.append(song_copy)
    return render_template('playlist_details.html',
                           playlist=playlist,
                           songs_in_playlist=songs_in_playlist)
@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'POST':
        title = request.form.get('playlist-name-input', '').strip()
        description = request.form.get('playlist-description-input', '').strip()
        if not title:
            error = "Playlist name is required."
            return render_template('create_playlist.html', error=error, title=title, description=description)
        playlists = read_playlists()
        new_id = generate_new_id(playlists, 'playlist_id')
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
    playlists = read_playlists()
    # Remove the song from playlist_songs
    playlist_songs = [ps for ps in playlist_songs if not (ps['playlist_id'] == playlist_id and ps['song_id'] == song_id)]
    write_playlist_songs(playlist_songs)
    # Update total_songs in playlists
    for p in playlists:
        if p['playlist_id'] == playlist_id:
            p['total_songs'] = sum(1 for ps in playlist_songs if ps['playlist_id'] == playlist_id)
            break
    write_playlists(playlists)
    return redirect(url_for('playlist_details', playlist_id=playlist_id))
@app.route('/songs/<song_id>/add_to_playlist/<playlist_id>', methods=['POST'])
def add_song_to_playlist(song_id, playlist_id):
    playlists = read_playlists()
    playlist_songs = read_playlist_songs()
    # Check if playlist exists
    playlist = get_playlist_by_id(playlist_id)
    if not playlist:
        abort(404)
    # Check if song already in playlist
    for ps in playlist_songs:
        if ps['playlist_id'] == playlist_id and ps['song_id'] == song_id:
            # Already in playlist, redirect back
            return redirect(request.referrer or url_for('song_catalog'))
    new_id = generate_new_id(playlist_songs, 'playlist_song_id')
    added_date = datetime.now().strftime('%Y-%m-%d')
    new_entry = {
        'playlist_song_id': new_id,
        'playlist_id': playlist_id,
        'song_id': song_id,
        'added_date': added_date
    }
    playlist_songs.append(new_entry)
    write_playlist_songs(playlist_songs)
    # Update total_songs in playlists
    for p in playlists:
        if p['playlist_id'] == playlist_id:
            p['total_songs'] = sum(1 for ps in playlist_songs if ps['playlist_id'] == playlist_id)
            break
    write_playlists(playlists)
    return redirect(request.referrer or url_for('song_catalog'))
@app.route('/albums')
def albums():
    albums = read_albums()
    artists = read_artists()
    artist_dict = {a['artist_id']: a['name'] for a in artists}
    # Enrich albums with artist name
    for album in albums:
        album['artist_name'] = artist_dict.get(album['artist_id'], 'Unknown Artist')
    search_query = request.args.get('search', '').strip().lower()
    sort_option = request.args.get('sort', 'By Title').lower()
    filtered_albums = []
    for album in albums:
        if search_query:
            if (search_query not in album['title'].lower() and
                search_query not in album['artist_name'].lower()):
                continue
        filtered_albums.append(album)
    if sort_option == 'by title':
        filtered_albums.sort(key=lambda a: a['title'].lower())
    elif sort_option == 'by artist':
        filtered_albums.sort(key=lambda a: a['artist_name'].lower())
    elif sort_option == 'by year':
        try:
            filtered_albums.sort(key=lambda a: int(a['release_year']))
        except ValueError:
            pass
    return render_template('albums.html',
                           albums=filtered_albums,
                           search_query=search_query,
                           sort_option=sort_option)
@app.route('/albums/<album_id>')
def album_details(album_id):
    album = get_album_by_id(album_id)
    if not album:
        abort(404)
    songs = read_songs()
    artists = read_artists()
    artist = get_artist_by_id(album['artist_id'])
    # Get songs in this album
    album_songs = []
    for song in songs:
        if song['album_id'] == album_id:
            song_copy = song.copy()
            song_copy['duration_formatted'] = format_duration(song_copy['duration'])
            album_songs.append(song_copy)
    return render_template('album_details.html',
                           album=album,
                           artist=artist,
                           album_songs=album_songs)
@app.route('/albums/<album_id>/add_to_playlist/<playlist_id>', methods=['POST'])
def add_album_to_playlist(album_id, playlist_id):
    playlist = get_playlist_by_id(playlist_id)
    if not playlist:
        abort(404)
    songs = read_songs()
    playlist_songs = read_playlist_songs()
    # Get all songs in album
    album_songs = [s for s in songs if s['album_id'] == album_id]
    # Add songs to playlist if not already present
    existing_song_ids = {ps['song_id'] for ps in playlist_songs if ps['playlist_id'] == playlist_id}
    new_entries = []
    max_id = 0
    for ps in playlist_songs:
        try:
            sid = int(ps['playlist_song_id'])
            if sid > max_id:
                max_id = sid
        except ValueError:
            continue
    added_date = datetime.now().strftime('%Y-%m-%d')
    for song in album_songs:
        if song['song_id'] not in existing_song_ids:
            max_id += 1
            new_entries.append({
                'playlist_song_id': str(max_id),
                'playlist_id': playlist_id,
                'song_id': song['song_id'],
                'added_date': added_date
            })
    playlist_songs.extend(new_entries)
    write_playlist_songs(playlist_songs)
    # Update total_songs in playlists
    playlists = read_playlists()
    for p in playlists:
        if p['playlist_id'] == playlist_id:
            p['total_songs'] = sum(1 for ps in playlist_songs if ps['playlist_id'] == playlist_id)
            break
    write_playlists(playlists)
    return redirect(url_for('playlist_details', playlist_id=playlist_id))
@app.route('/artists')
def artists():
    artists = read_artists()
    search_query = request.args.get('search', '').strip().lower()
    sort_option = request.args.get('sort', 'By Name').lower()
    filtered_artists = []
    for artist in artists:
        if search_query:
            if search_query not in artist['name'].lower():
                continue
        filtered_artists.append(artist)
    if sort_option == 'by name':
        filtered_artists.sort(key=lambda a: a['name'].lower())
    elif sort_option == 'by genre':
        filtered_artists.sort(key=lambda a: a['genre'].lower())
    return render_template('artists.html',
                           artists=filtered_artists,
                           search_query=search_query,
                           sort_option=sort_option)
@app.route('/artists/<artist_id>')
def artist_profile(artist_id):
    artist = get_artist_by_id(artist_id)
    if not artist:
        abort(404)
    songs = read_songs()
    albums = read_albums()
    # Songs by this artist
    artist_songs = [s for s in songs if s['artist_id'] == artist_id]
    for song in artist_songs:
        song['duration_formatted'] = format_duration(song['duration'])
    # Albums by this artist
    artist_albums = [al for al in albums if al['artist_id'] == artist_id]
    return render_template('artist_profile.html',
                           artist=artist,
                           songs=artist_songs,
                           albums=artist_albums)
@app.route('/genres')
def genres():
    genres = read_genres()
    songs = read_songs()
    artists = read_artists()
    # Prepare genre list for dropdown and display
    genre_names = [g['genre_name'] for g in genres]
    genre_names = sorted(genre_names)
    selected_genre = request.args.get('genre', '').strip()
    genre_songs = []
    genre_artists = []
    if selected_genre:
        # Filter songs by genre
        genre_songs = [s for s in songs if s['genre'].lower() == selected_genre.lower()]
        # Enrich songs with artist name
        artist_dict = {a['artist_id']: a['name'] for a in artists}
        for song in genre_songs:
            song['artist_name'] = artist_dict.get(song['artist_id'], 'Unknown Artist')
            song['duration_formatted'] = format_duration(song['duration'])
        # Filter artists by genre (case-insensitive match)
        genre_artists = [a for a in artists if a['genre'].lower() == selected_genre.lower()]
    return render_template('genres.html',
                           genres=genre_names,
                           selected_genre=selected_genre,
                           genre_songs=genre_songs,
                           genre_artists=genre_artists)
if __name__ == '__main__':
    app.run(debug=True)