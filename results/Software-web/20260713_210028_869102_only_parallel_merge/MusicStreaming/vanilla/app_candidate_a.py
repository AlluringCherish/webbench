from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'

# Utility functions for data loading

def load_songs():
    songs = []
    path = os.path.join(DATA_DIR, 'songs.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) >= 8:
                        song = {
                            'song_id': int(parts[0]),
                            'title': parts[1],
                            'artist_id': int(parts[2]) if parts[2].isdigit() else None,
                            'album_id': int(parts[3]) if parts[3].isdigit() else None,
                            'genre': parts[4],
                            'duration': int(parts[5]) if parts[5].isdigit() else 0,  # in seconds
                            'release_date': parts[6],
                            'play_count': int(parts[7]) if parts[7].isdigit() else 0
                        }
                        songs.append(song)
    return songs

def load_artists():
    artists = []
    path = os.path.join(DATA_DIR, 'artists.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) >=5:
                        artist = {
                            'artist_id': int(parts[0]),
                            'name': parts[1],
                            'genre': parts[2],
                            'country': parts[3],
                            'formation_year': parts[4]
                        }
                        artists.append(artist)
    return artists

def load_albums():
    albums = []
    path = os.path.join(DATA_DIR, 'albums.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) >=6:
                        album = {
                            'album_id': int(parts[0]),
                            'title': parts[1],
                            'artist_id': int(parts[2]) if parts[2].isdigit() else None,
                            'release_year': parts[3],
                            'total_songs': int(parts[4]) if parts[4].isdigit() else 0,
                            'genre': parts[5]
                        }
                        albums.append(album)
    return albums

def load_genres():
    genres = []
    path = os.path.join(DATA_DIR, 'genres.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) >=3:
                        genre = {
                            'genre_id': int(parts[0]),
                            'genre_name': parts[1],
                            'description': parts[2]
                        }
                        genres.append(genre)
    return genres

def load_playlists():
    playlists = []
    path = os.path.join(DATA_DIR, 'playlists.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) >=5:
                        playlist = {
                            'playlist_id': int(parts[0]),
                            'title': parts[1],
                            'description': parts[2],
                            'creation_date': parts[3],
                            'total_songs': int(parts[4]) if parts[4].isdigit() else 0
                        }
                        playlists.append(playlist)
    return playlists

def load_playlist_songs():
    playlist_songs = []
    path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) >=4:
                        pls = {
                            'playlist_song_id': int(parts[0]),
                            'playlist_id': int(parts[1]),
                            'song_id': int(parts[2]),
                            'added_date': parts[3]
                        }
                        playlist_songs.append(pls)
    return playlist_songs

# Helper to save playlists

def save_playlists(playlists):
    path = os.path.join(DATA_DIR, 'playlists.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for p in playlists:
            f.write(f"{p['playlist_id']}|{p['title']}|{p['description']}|{p['creation_date']}|{p['total_songs']}\n")

def save_playlist_songs(playlist_songs):
    path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for pls in playlist_songs:
            f.write(f"{pls['playlist_song_id']}|{pls['playlist_id']}|{pls['song_id']}|{pls['added_date']}\n")

# Helper functions for lookups

def get_artist_by_id(artist_id, artists):
    for a in artists:
        if a['artist_id'] == artist_id:
            return a
    return None

def get_album_by_id(album_id, albums):
    for a in albums:
        if a['album_id'] == album_id:
            return a
    return None

def get_playlist_by_id(playlist_id, playlists):
    for p in playlists:
        if p['playlist_id'] == playlist_id:
            return p
    return None

def get_song_by_id(song_id, songs):
    for s in songs:
        if s['song_id'] == song_id:
            return s
    return None

# Helpers for duration formatting

def format_duration(seconds):
    m = seconds // 60
    s = seconds % 60
    return f"{m}:{s:02d}"


# ROUTES

@app.route('/')
@app.route('/dashboard')
def dashboard():
    songs = load_songs()
    artists = load_artists()

    # Featured songs by top play counts (top 5)
    featured = sorted(songs, key=lambda x: x['play_count'], reverse=True)[:5]

    # Trending artists defined similarly by max play count of their songs
    artist_song_playcounts = {}
    for s in songs:
        if s['artist_id'] is not None:
            artist_song_playcounts[s['artist_id']] = artist_song_playcounts.get(s['artist_id'], 0) + s['play_count']
    trending_artists_ids = sorted(artist_song_playcounts, key=artist_song_playcounts.get, reverse=True)[:5]
    trending_artists = [get_artist_by_id(aid, artists) for aid in trending_artists_ids if get_artist_by_id(aid, artists)]

    return render_template('dashboard.html', featured_songs=featured, trending_artists=trending_artists)

@app.route('/songs')
def songs_catalog():
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()
    genres = load_genres()

    search = request.args.get('search', '').lower()
    genre_filter = request.args.get('genre', '')

    filtered_songs = []
    for s in songs:
        artist = get_artist_by_id(s['artist_id'], artists)
        album = get_album_by_id(s['album_id'], albums)
        if search:
            if search not in s['title'].lower() and (artist is None or search not in artist['name'].lower()) and (album is None or search not in album['title'].lower()):
                continue
        if genre_filter:
            if s['genre'].lower() != genre_filter.lower():
                continue
        filtered_songs.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist['name'] if artist else 'Unknown',
            'album_title': album['title'] if album else 'Unknown',
            'genre': s['genre'],
            'duration': format_duration(s['duration'])
        })

    return render_template('song_catalog.html', songs=filtered_songs, genres=genres, search_text=search, selected_genre=genre_filter)

@app.route('/songs/<int:song_id>')
def song_details(song_id):
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()

    song = get_song_by_id(song_id, songs)
    if not song:
        return "Song Not Found", 404
    artist = get_artist_by_id(song['artist_id'], artists)
    album = get_album_by_id(song['album_id'], albums)
    duration_formatted = format_duration(song['duration'])

    return render_template('song_details.html', song=song, artist=artist, album=album, duration=duration_formatted)

@app.route('/playlists')
def playlists():
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()

    # Count songs from playlist_songs instead of relying only on total_songs field
    playlist_song_counts = {}
    for pls in playlist_songs:
        playlist_song_counts[pls['playlist_id']] = playlist_song_counts.get(pls['playlist_id'], 0) + 1

    # Overwrite total_songs to match actual counts
    for p in playlists:
        p['total_songs'] = playlist_song_counts.get(p['playlist_id'], 0)

    return render_template('playlists.html', playlists=playlists)

@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'POST':
        title = request.form.get('playlist-name-input', '').strip()
        description = request.form.get('playlist-description-input', '').strip()
        if not title:
            # Just reload the page or could show error
            return render_template('create_playlist.html', error='Playlist name is required', title=title, description=description)

        playlists = load_playlists()
        # Generate new playlist_id
        new_id = 1
        if playlists:
            new_id = max(p['playlist_id'] for p in playlists) + 1

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

@app.route('/playlists/<int:playlist_id>')
def playlist_details(playlist_id):
    playlists = load_playlists()
    playlist = get_playlist_by_id(playlist_id, playlists)
    if not playlist:
        return "Playlist Not Found", 404

    playlist_songs = load_playlist_songs()
    songs = load_songs()
    artists = load_artists()

    # Filter songs in this playlist
    filtered_playlist_songs = [pls for pls in playlist_songs if pls['playlist_id'] == playlist_id]

    # Build song info
    songs_info = []
    for pls in filtered_playlist_songs:
        song = get_song_by_id(pls['song_id'], songs)
        if song:
            artist = get_artist_by_id(song['artist_id'], artists)
            songs_info.append({
                'song_id': song['song_id'],
                'title': song['title'],
                'artist_name': artist['name'] if artist else 'Unknown',
                'duration': format_duration(song['duration'])
            })

    return render_template('playlist_details.html', playlist=playlist, songs=songs_info)

@app.route('/playlists/<int:playlist_id>/delete', methods=['POST'])
def delete_playlist(playlist_id):
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()

    # Remove playlist
    playlists = [p for p in playlists if p['playlist_id'] != playlist_id]

    # Remove playlist songs
    playlist_songs = [pls for pls in playlist_songs if pls['playlist_id'] != playlist_id]

    save_playlists(playlists)
    save_playlist_songs(playlist_songs)

    return redirect(url_for('playlists'))

@app.route('/playlists/<int:playlist_id>/remove_song/<int:song_id>', methods=['POST'])
def remove_song_from_playlist(playlist_id, song_id):
    playlist_songs = load_playlist_songs()
    playlist_songs = [pls for pls in playlist_songs if not(pls['playlist_id'] == playlist_id and pls['song_id'] == song_id)]
    save_playlist_songs(playlist_songs)

    # Update total_songs count in playlists
    playlists = load_playlists()
    playlist_song_counts = {}
    for pls in playlist_songs:
        playlist_song_counts[pls['playlist_id']] = playlist_song_counts.get(pls['playlist_id'], 0) + 1

    for p in playlists:
        p['total_songs'] = playlist_song_counts.get(p['playlist_id'], 0)

    save_playlists(playlists)

    return redirect(url_for('playlist_details', playlist_id=playlist_id))

@app.route('/albums')
def albums():
    albums = load_albums()
    artists = load_artists()

    search = request.args.get('search', '').lower()
    sort_by = request.args.get('sort', '')

    filtered_albums = []
    for a in albums:
        artist = get_artist_by_id(a['artist_id'], artists)
        if search:
            if search not in a['title'].lower() and (artist is None or search not in artist['name'].lower()):
                continue
        filtered_albums.append({
            'album_id': a['album_id'],
            'title': a['title'],
            'artist_name': artist['name'] if artist else 'Unknown',
            'release_year': a['release_year']
        })

    if sort_by == 'title':
        filtered_albums.sort(key=lambda x: x['title'].lower())
    elif sort_by == 'artist':
        filtered_albums.sort(key=lambda x: x['artist_name'].lower())
    elif sort_by == 'year':
        filtered_albums.sort(key=lambda x: x['release_year'], reverse=True)

    return render_template('albums.html', albums=filtered_albums, search_text=search, sort_by=sort_by)

@app.route('/albums/<int:album_id>')
def album_details(album_id):
    albums = load_albums()
    artists = load_artists()
    songs = load_songs()

    album = get_album_by_id(album_id, albums)
    if not album:
        return "Album Not Found", 404
    artist = get_artist_by_id(album['artist_id'], artists)

    album_songs = [s for s in songs if s['album_id'] == album_id]
    songs_info = []
    for s in album_songs:
        songs_info.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'duration': format_duration(s['duration'])
        })

    return render_template('album_details.html', album=album, artist=artist, songs=songs_info)

@app.route('/artists')
def artists():
    artists = load_artists()

    search = request.args.get('search', '').lower()
    sort_by = request.args.get('sort', '')

    filtered_artists = []
    for a in artists:
        if search and search not in a['name'].lower():
            continue
        filtered_artists.append(a)

    if sort_by == 'name':
        filtered_artists.sort(key=lambda x: x['name'].lower())
    elif sort_by == 'genre':
        filtered_artists.sort(key=lambda x: x['genre'].lower())

    return render_template('artists.html', artists=filtered_artists, search_text=search, sort_by=sort_by)

@app.route('/genres')
def genres():
    genres = load_genres()
    songs = load_songs()
    artists = load_artists()

    selected_genre = request.args.get('genre', '')

    genre_songs = []
    genre_artists = []

    if selected_genre:
        genre_songs = [s for s in songs if s['genre'].lower() == selected_genre.lower()]
        genre_artists = [a for a in artists if a['genre'].lower() == selected_genre.lower()]

    return render_template('genres.html', genres=genres, selected_genre=selected_genre, genre_songs=genre_songs, genre_artists=genre_artists)

if __name__ == '__main__':
    app.run(debug=True)
