from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'

# Helper functions to load data from text files

def load_songs():
    songs = []
    path = os.path.join(DATA_DIR, 'songs.txt')
    if not os.path.exists(path):
        return songs
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) == 8:
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
    return songs


def load_artists():
    artists = []
    path = os.path.join(DATA_DIR, 'artists.txt')
    if not os.path.exists(path):
        return artists
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) == 5:
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
    if not os.path.exists(path):
        return albums
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) == 6:
                    album = {
                        'album_id': int(parts[0]),
                        'title': parts[1],
                        'artist_id': int(parts[2]),
                        'release_year': parts[3],  # string?
                        'total_songs': int(parts[4]),
                        'genre': parts[5]
                    }
                    albums.append(album)
    return albums


def load_genres():
    genres = []
    path = os.path.join(DATA_DIR, 'genres.txt')
    if not os.path.exists(path):
        return genres
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) == 3:
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
    if not os.path.exists(path):
        return playlists
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) == 5:
                    playlist = {
                        'playlist_id': int(parts[0]),
                        'title': parts[1],
                        'description': parts[2],
                        'creation_date': parts[3],
                        'total_songs': int(parts[4])
                    }
                    playlists.append(playlist)
    return playlists


def load_playlist_songs():
    playlist_songs = []
    path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    if not os.path.exists(path):
        return playlist_songs
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) == 4:
                    playlist_song = {
                        'playlist_song_id': int(parts[0]),
                        'playlist_id': int(parts[1]),
                        'song_id': int(parts[2]),
                        'added_date': parts[3]
                    }
                    playlist_songs.append(playlist_song)
    return playlist_songs


def save_playlists(playlists):
    path = os.path.join(DATA_DIR, 'playlists.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for pl in playlists:
            line = f"{pl['playlist_id']}|{pl['title']}|{pl['description']}|{pl['creation_date']}|{pl['total_songs']}\n"
            f.write(line)


def save_playlist_songs(playlist_songs):
    path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for pls in playlist_songs:
            line = f"{pls['playlist_song_id']}|{pls['playlist_id']}|{pls['song_id']}|{pls['added_date']}\n"
            f.write(line)


def get_artist_by_id(artist_id):
    artists = load_artists()
    for artist in artists:
        if artist['artist_id'] == artist_id:
            return artist
    return None


def get_album_by_id(album_id):
    albums = load_albums()
    for album in albums:
        if album['album_id'] == album_id:
            return album
    return None


def get_song_by_id(song_id):
    songs = load_songs()
    for song in songs:
        if song['song_id'] == song_id:
            return song
    return None


@app.route('/')
@app.route('/dashboard')
def dashboard():
    songs = load_songs()
    artists = load_artists()
    # Featured songs - top 5 by play_count descending
    featured_songs = sorted(songs, key=lambda s: s['play_count'], reverse=True)[:5]
    # Trending artists - top 5 by sum of songs play count
    artist_play_counts = {}
    for song in songs:
        artist_play_counts[song['artist_id']] = artist_play_counts.get(song['artist_id'], 0) + song['play_count']
    trending_artists = sorted(load_artists(), key=lambda a: artist_play_counts.get(a['artist_id'],0), reverse=True)[:5]
    return render_template('templates_candidate_b/dashboard.html',
                           featured_songs=featured_songs,
                           trending_artists=trending_artists)


@app.route('/songs')
def song_catalog():
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()
    genres = load_genres()

    # Search and genre filter query parameters
    search_query = request.args.get('search', '').lower()
    genre_filter = request.args.get('genre', '')

    # Filter songs
    filtered_songs = []
    for song in songs:
        artist = get_artist_by_id(song['artist_id'])
        album = get_album_by_id(song['album_id'])
        if artist is None or album is None:
            continue
        matches_search = (search_query in song['title'].lower() or
                          search_query in artist['name'].lower() or
                          search_query in album['title'].lower())
        matches_genre = (genre_filter.lower() == song['genre'].lower() if genre_filter else True)
        if (not search_query or matches_search) and matches_genre:
            filtered_songs.append({
                'song': song,
                'artist': artist,
                'album': album
            })

    return render_template('templates_candidate_b/song_catalog.html',
                           songs=filtered_songs,
                           genres=genres,
                           selected_genre=genre_filter,
                           search_query=search_query)


@app.route('/songs/<int:song_id>')
def song_details(song_id):
    song = get_song_by_id(song_id)
    if not song:
        return "Song not found", 404
    artist = get_artist_by_id(song['artist_id'])
    album = get_album_by_id(song['album_id'])
    return render_template('templates_candidate_b/song_details.html',
                           song=song,
                           artist=artist,
                           album=album)


@app.route('/playlists')
def playlists():
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()
    # Calculate song count per playlist (use from playlists anyway, but keep consistent)
    return render_template('templates_candidate_b/playlists.html',
                           playlists=playlists)


@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'POST':
        title = request.form.get('playlist_name', '').strip()
        description = request.form.get('playlist_description', '').strip()
        if not title:
            return render_template('templates_candidate_b/create_playlist.html', error='Playlist name is required.')

        playlists = load_playlists()
        new_id = max([pl['playlist_id'] for pl in playlists], default=0) + 1
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
    return render_template('templates_candidate_b/create_playlist.html')


@app.route('/playlists/<int:playlist_id>')
def playlist_details(playlist_id):
    playlists = load_playlists()
    playlist = next((pl for pl in playlists if pl['playlist_id'] == playlist_id), None)
    if not playlist:
        return "Playlist not found", 404

    playlist_songs = load_playlist_songs()
    songs = load_songs()
    artists = load_artists()

    songs_in_playlist = []
    for pls in playlist_songs:
        if pls['playlist_id'] == playlist_id:
            song = next((s for s in songs if s['song_id'] == pls['song_id']), None)
            if song:
                artist = next((a for a in artists if a['artist_id'] == song['artist_id']), None)
                songs_in_playlist.append({'song': song, 'artist': artist})

    return render_template('templates_candidate_b/playlist_details.html',
                           playlist=playlist,
                           songs_in_playlist=songs_in_playlist)


@app.route('/playlists/<int:playlist_id>/delete', methods=['POST'])
def delete_playlist(playlist_id):
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()

    playlists = [pl for pl in playlists if pl['playlist_id'] != playlist_id]
    playlist_songs = [pls for pls in playlist_songs if pls['playlist_id'] != playlist_id]

    save_playlists(playlists)
    save_playlist_songs(playlist_songs)

    return redirect(url_for('playlists'))


@app.route('/playlists/<int:playlist_id>/remove_song/<int:song_id>', methods=['POST'])
def remove_song_from_playlist(playlist_id, song_id):
    playlist_songs = load_playlist_songs()
    playlist_songs = [pls for pls in playlist_songs if not (pls['playlist_id'] == playlist_id and pls['song_id'] == song_id)]
    save_playlist_songs(playlist_songs)

    # Update total_songs count in playlists
    playlists = load_playlists()
    for pl in playlists:
        if pl['playlist_id'] == playlist_id:
            pl_songs_count = sum(1 for pls in playlist_songs if pls['playlist_id'] == playlist_id)
            pl['total_songs'] = pl_songs_count
            break
    save_playlists(playlists)

    return redirect(url_for('playlist_details', playlist_id=playlist_id))


@app.route('/albums')
def albums():
    albums = load_albums()
    artists = load_artists()

    search_query = request.args.get('search', '').lower()
    sort_option = request.args.get('sort', '')

    filtered_albums = []
    for album in albums:
        artist = get_artist_by_id(album['artist_id'])
        if not artist:
            continue
        if search_query and (search_query not in album['title'].lower() and search_query not in artist['name'].lower()):
            continue
        filtered_albums.append({'album': album, 'artist': artist})

    if sort_option == 'Title':
        filtered_albums.sort(key=lambda x: x['album']['title'])
    elif sort_option == 'Artist':
        filtered_albums.sort(key=lambda x: x['artist']['name'])
    elif sort_option == 'Year':
        filtered_albums.sort(key=lambda x: x['album']['release_year'])

    return render_template('templates_candidate_b/albums.html',
                           albums=filtered_albums,
                           search_query=search_query,
                           sort_option=sort_option)


@app.route('/albums/<int:album_id>')
def album_details(album_id):
    album = get_album_by_id(album_id)
    if not album:
        return "Album not found", 404
    artist = get_artist_by_id(album['artist_id'])
    songs = load_songs()
    songs_in_album = [s for s in songs if s['album_id'] == album_id]
    return render_template('templates_candidate_b/album_details.html',
                           album=album,
                           artist=artist,
                           songs_in_album=songs_in_album)


@app.route('/artists')
def artists():
    artists = load_artists()

    search_query = request.args.get('search', '').lower()
    sort_option = request.args.get('sort', '')

    filtered_artists = []
    for artist in artists:
        if search_query and search_query not in artist['name'].lower():
            continue
        filtered_artists.append(artist)

    if sort_option == 'Name':
        filtered_artists.sort(key=lambda x: x['name'])
    elif sort_option == 'Genre':
        filtered_artists.sort(key=lambda x: x['genre'])

    return render_template('templates_candidate_b/artists.html',
                           artists=filtered_artists,
                           search_query=search_query,
                           sort_option=sort_option)


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

    return render_template('templates_candidate_b/genres.html',
                           genres=genres,
                           selected_genre=selected_genre,
                           genre_songs=genre_songs,
                           genre_artists=genre_artists)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
