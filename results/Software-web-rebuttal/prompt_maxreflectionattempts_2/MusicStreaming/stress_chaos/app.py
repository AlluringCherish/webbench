from flask import Flask, render_template, redirect, url_for, request, abort
import os
from datetime import datetime

app = Flask(__name__)

# Data file paths
SONGS_FILE = 'data/songs.txt'
ARTISTS_FILE = 'data/artists.txt'
ALBUMS_FILE = 'data/albums.txt'
GENRES_FILE = 'data/genres.txt'
PLAYLISTS_FILE = 'data/playlists.txt'
PLAYLIST_SONGS_FILE = 'data/playlist_songs.txt'

# Helper functions to read data from files

def read_songs():
    songs = []
    if not os.path.exists(SONGS_FILE):
        return songs
    with open(SONGS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
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
            except Exception:
                continue
    return songs

def read_artists():
    artists = []
    if not os.path.exists(ARTISTS_FILE):
        return artists
    with open(ARTISTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
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
            except Exception:
                continue
    return artists

def read_albums():
    albums = []
    if not os.path.exists(ALBUMS_FILE):
        return albums
    with open(ALBUMS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
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
            except Exception:
                continue
    return albums

def read_genres():
    genres = []
    if not os.path.exists(GENRES_FILE):
        return genres
    with open(GENRES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
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
            except Exception:
                continue
    return genres

def read_playlists():
    playlists = []
    if not os.path.exists(PLAYLISTS_FILE):
        return playlists
    with open(PLAYLISTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
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
            except Exception:
                continue
    return playlists

def read_playlist_songs():
    playlist_songs = []
    if not os.path.exists(PLAYLIST_SONGS_FILE):
        return playlist_songs
    with open(PLAYLIST_SONGS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
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
            except Exception:
                continue
    return playlist_songs

# Helper functions to write data

def write_playlists(playlists):
    with open(PLAYLISTS_FILE, 'w', encoding='utf-8') as f:
        for p in playlists:
            row = f"{p['playlist_id']}|{p['title']}|{p['description']}|{p['creation_date']}|{p['total_songs']}"
            f.write(row + '\n')


def write_playlist_songs(playlist_songs):
    with open(PLAYLIST_SONGS_FILE, 'w', encoding='utf-8') as f:
        for ps in playlist_songs:
            row = f"{ps['playlist_song_id']}|{ps['playlist_id']}|{ps['song_id']}|{ps['added_date']}"
            f.write(row + '\n')

# Helper to generate next ids

def get_next_playlist_id(playlists):
    if not playlists:
        return 1
    return max(p['playlist_id'] for p in playlists) + 1

def get_next_playlist_song_id(playlist_songs):
    if not playlist_songs:
        return 1
    return max(ps['playlist_song_id'] for ps in playlist_songs) + 1

# Utility functions

def get_artist_by_id(artist_id):
    artists = read_artists()
    for a in artists:
        if a['artist_id'] == artist_id:
            return a
    return None

def get_album_by_id(album_id):
    albums = read_albums()
    for a in albums:
        if a['album_id'] == album_id:
            return a
    return None

def get_song_by_id(song_id):
    songs = read_songs()
    for s in songs:
        if s['song_id'] == song_id:
            return s
    return None

# Route implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    songs = read_songs()
    artists = read_artists()
    albums = read_albums()

    # Featured songs: We pick top 5 played songs sorted by play_count descending
    top_songs = sorted(songs, key=lambda s: s['play_count'], reverse=True)[:5]
    featured_songs = []
    for s in top_songs:
        artist = get_artist_by_id(s['artist_id'])
        album = get_album_by_id(s['album_id'])
        if artist is None or album is None:
            continue
        featured_songs.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist['name'],
            'album_name': album['title'],
            'duration': s['duration']
        })

    # Trending artists: top 5 artists with highest total play counts on their songs
    artist_play_counts = {}
    for s in songs:
        if s['artist_id'] in artist_play_counts:
            artist_play_counts[s['artist_id']] += s['play_count']
        else:
            artist_play_counts[s['artist_id']] = s['play_count']

    trending_artists_ids = sorted(artist_play_counts, key=lambda aid: artist_play_counts[aid], reverse=True)[:5]
    trending_artists = []
    for aid in trending_artists_ids:
        artist = get_artist_by_id(aid)
        if artist is None:
            continue
        trending_artists.append({
            'artist_id': artist['artist_id'],
            'name': artist['name'],
            'genre': artist['genre']
        })

    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)

@app.route('/songs', methods=['GET'])
def song_catalog_page():
    songs = read_songs()
    artists = read_artists()
    albums = read_albums()
    genres = sorted(set(s['genre'] for s in songs))

    # Build songs list with artist_name and album_name
    songs_list = []
    for s in songs:
        artist = get_artist_by_id(s['artist_id'])
        album = get_album_by_id(s['album_id'])
        if artist is None or album is None:
            continue
        songs_list.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist['name'],
            'album_name': album['title'],
            'genre': s['genre'],
            'duration': s['duration']
        })

    return render_template('song_catalog.html', songs=songs_list, genres=genres)

@app.route('/songs/search', methods=['POST'])
def song_catalog_search():
    search_text = request.form.get('search_input', '').strip().lower()
    selected_genre = request.form.get('genre_filter', '')

    songs = read_songs()
    artists = read_artists()
    albums = read_albums()

    def song_matches(s):
        match_text = (s['title'].lower())
        if search_text and search_text not in match_text:
            return False
        if selected_genre and selected_genre != "All Genres" and s['genre'] != selected_genre:
            return False
        return True

    filtered = []
    for s in songs:
        if not song_matches(s):
            continue
        artist = get_artist_by_id(s['artist_id'])
        album = get_album_by_id(s['album_id'])
        if artist is None or album is None:
            continue
        filtered.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist['name'],
            'album_name': album['title'],
            'genre': s['genre'],
            'duration': s['duration']
        })

    genres = sorted(set(s['genre'] for s in songs))

    return render_template('song_catalog.html', songs=filtered, genres=genres)

@app.route('/songs/<int:song_id>')
def song_details_page(song_id):
    s = get_song_by_id(song_id)
    if s is None:
        abort(404)
    artist = get_artist_by_id(s['artist_id'])
    album = get_album_by_id(s['album_id'])
    if artist is None or album is None:
        abort(404)
    song = {
        'song_id': s['song_id'],
        'title': s['title'],
        'artist_id': artist['artist_id'],
        'artist_name': artist['name'],
        'album_id': album['album_id'],
        'album_name': album['title'],
        'duration': s['duration'],
        'genre': s['genre'],
        'release_date': s['release_date']
    }
    return render_template('song_details.html', song=song)

@app.route('/playlists')
def playlists_page():
    playlists = read_playlists()
    return render_template('playlists.html', playlists=playlists)

@app.route('/playlists/create', methods=['GET'])
def create_playlist_page():
    return render_template('create_playlist.html')

@app.route('/playlists/create', methods=['POST'])
def create_playlist_submit():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()

    if not title:
        # Simple validation: Require title
        return redirect(url_for('create_playlist_page'))

    playlists = read_playlists()
    playlist_songs = read_playlist_songs()

    new_id = get_next_playlist_id(playlists)
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

    # Redirect to playlist details page of the newly created playlist
    return redirect(url_for('playlist_details_page', playlist_id=new_id))

@app.route('/playlists/<int:playlist_id>')
def playlist_details_page(playlist_id):
    playlists = read_playlists()
    playlist = next((p for p in playlists if p['playlist_id'] == playlist_id), None)
    if playlist is None:
        abort(404)

    playlist_songs = read_playlist_songs()
    songs = read_songs()
    artists = read_artists()

    # Get songs in playlist
    songs_in_playlist = []
    # collect song_ids in playlist
    playlist_song_ids = [ps['song_id'] for ps in playlist_songs if ps['playlist_id'] == playlist_id]

    for song_id in playlist_song_ids:
        s = next((song for song in songs if song['song_id'] == song_id), None)
        if s is None:
            continue
        artist = get_artist_by_id(s['artist_id'])
        if artist is None:
            continue
        songs_in_playlist.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist['name'],
            'duration': s['duration']
        })

    return render_template('playlist_details.html', playlist=playlist, songs_in_playlist=songs_in_playlist)

@app.route('/playlists/<int:playlist_id>/delete', methods=['POST'])
def delete_playlist(playlist_id):
    playlists = read_playlists()
    playlist_songs = read_playlist_songs()

    # Remove playlist
    playlists = [p for p in playlists if p['playlist_id'] != playlist_id]
    write_playlists(playlists)

    # Remove all playlist songs entries for this playlist
    playlist_songs = [ps for ps in playlist_songs if ps['playlist_id'] != playlist_id]
    write_playlist_songs(playlist_songs)

    return redirect(url_for('playlists_page'))

@app.route('/playlists/<int:playlist_id>/remove_song/<int:song_id>', methods=['POST'])
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
        # Update playlist total songs count
        playlists = read_playlists()
        for p in playlists:
            if p['playlist_id'] == playlist_id:
                p['total_songs'] = max(0, p['total_songs'] - 1)
                break
        write_playlists(playlists)
        write_playlist_songs(new_playlist_songs)

    return redirect(url_for('playlist_details_page', playlist_id=playlist_id))

@app.route('/albums')
def albums_page():
    albums = read_albums()
    artists = read_artists()

    albums_list = []
    for album in albums:
        artist = get_artist_by_id(album['artist_id'])
        if artist is None:
            continue
        albums_list.append({
            'album_id': album['album_id'],
            'title': album['title'],
            'artist_name': artist['name'],
            'release_year': album['release_year'],
            'genre': album['genre']
        })

    return render_template('albums.html', albums=albums_list)

@app.route('/albums/search', methods=['POST'])
def albums_search():
    search_text = request.form.get('search_albums', '').strip().lower()
    albums = read_albums()
    artists = read_artists()

    filtered = []
    for album in albums:
        if search_text and search_text not in album['title'].lower():
            continue
        artist = get_artist_by_id(album['artist_id'])
        if artist is None:
            continue
        filtered.append({
            'album_id': album['album_id'],
            'title': album['title'],
            'artist_name': artist['name'],
            'release_year': album['release_year'],
            'genre': album['genre']
        })

    return render_template('albums.html', albums=filtered)

@app.route('/albums/<int:album_id>')
def album_details_page(album_id):
    album = get_album_by_id(album_id)
    if album is None:
        abort(404)
    artist = get_artist_by_id(album['artist_id'])
    if artist is None:
        abort(404)

    songs = read_songs()
    songs_in_album = []
    for s in songs:
        if s['album_id'] == album_id:
            songs_in_album.append({
                'song_id': s['song_id'],
                'title': s['title'],
                'duration': s['duration']
            })

    album_dict = {
        'album_id': album['album_id'],
        'title': album['title'],
        'artist_id': artist['artist_id'],
        'artist_name': artist['name'],
        'release_year': album['release_year'],
        'total_songs': album['total_songs'],
        'genre': album['genre']
    }

    return render_template('album_details.html', album=album_dict, songs_in_album=songs_in_album)

@app.route('/albums/<int:album_id>/add_all_to_playlist', methods=['POST'])
def add_album_to_playlist(album_id):
    playlist_id = request.form.get('playlist_id', type=int)
    if playlist_id is None:
        # Bad request
        abort(400)

    album = get_album_by_id(album_id)
    if album is None:
        abort(404)

    playlists = read_playlists()
    playlist = next((p for p in playlists if p['playlist_id'] == playlist_id), None)
    if playlist is None:
        abort(404)

    songs = read_songs()
    playlist_songs = read_playlist_songs()

    # Find all songs in album
    album_songs = [s for s in songs if s['album_id'] == album_id]

    # Current song_ids in playlist
    current_song_ids = set(ps['song_id'] for ps in playlist_songs if ps['playlist_id'] == playlist_id)

    next_ps_id = get_next_playlist_song_id(playlist_songs)
    added_today = datetime.now().strftime('%Y-%m-%d')

    # Add all album songs that are not yet in playlist
    for s in album_songs:
        if s['song_id'] not in current_song_ids:
            playlist_songs.append({
                'playlist_song_id': next_ps_id,
                'playlist_id': playlist_id,
                'song_id': s['song_id'],
                'added_date': added_today
            })
            next_ps_id += 1
            playlist['total_songs'] += 1

    write_playlist_songs(playlist_songs)
    write_playlists(playlists)

    return redirect(url_for('album_details_page', album_id=album_id))

@app.route('/artists')
def artists_page():
    artists = read_artists()
    return render_template('artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def artists_search():
    search_text = request.form.get('search_artists', '').strip().lower()
    artists = read_artists()

    filtered = []
    for artist in artists:
        if search_text and search_text not in artist['name'].lower():
            continue
        filtered.append(artist)

    return render_template('artists.html', artists=filtered)

@app.route('/artists/<int:artist_id>')
def artist_profile_page(artist_id):
    artist = get_artist_by_id(artist_id)
    if artist is None:
        abort(404)

    songs = read_songs()
    albums = read_albums()
    songs_by_artist = []
    for s in songs:
        if s['artist_id'] == artist_id:
            album = get_album_by_id(s['album_id'])
            album_name = album['title'] if album else ''
            songs_by_artist.append({
                'song_id': s['song_id'],
                'title': s['title'],
                'album_name': album_name,
                'duration': s['duration']
            })

    return render_template('artist_profile.html', artist=artist, songs_by_artist=songs_by_artist)

@app.route('/genres')
def genre_exploration_page():
    genres = read_genres()

    # No selected genre on GET
    return render_template('genres.html',
        genres=genres,
        selected_genre=None,
        selected_genre_songs=None,
        selected_genre_artists=None)

@app.route('/genres/select', methods=['POST'])
def genre_select():
    selected_genre = request.form.get('select_genre', '').strip()
    genres = read_genres()

    # Filter songs and artists by selected genre
    songs = read_songs()
    artists = read_artists()

    selected_songs = []
    selected_artists = []

    if selected_genre:
        for s in songs:
            if s['genre'].lower() == selected_genre.lower():
                artist = get_artist_by_id(s['artist_id'])
                if artist:
                    selected_songs.append({
                        'song_id': s['song_id'],
                        'title': s['title'],
                        'artist_name': artist['name'],
                        'duration': s['duration']
                    })
        for a in artists:
            if a['genre'].lower() == selected_genre.lower():
                selected_artists.append({
                    'artist_id': a['artist_id'],
                    'name': a['name'],
                    'genre': a['genre']
                })

    return render_template('genres.html', genres=genres, selected_genre=selected_genre,
                           selected_genre_songs=selected_songs, selected_genre_artists=selected_artists)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
