from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = 'data'

# Utility functions to load data from text files

def load_songs():
    songs = []
    path = os.path.join(DATA_DIR, 'songs.txt')
    if not os.path.exists(path):
        return songs
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) >= 8:
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
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) >= 5:
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
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) >= 6:
                    album = {
                        'album_id': int(parts[0]),
                        'title': parts[1],
                        'artist_id': int(parts[2]),
                        'release_year': parts[3],
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
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) >= 3:
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
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) >= 5:
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
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) >= 4:
                    pls = {
                        'playlist_song_id': int(parts[0]),
                        'playlist_id': int(parts[1]),
                        'song_id': int(parts[2]),
                        'added_date': parts[3]
                    }
                    playlist_songs.append(pls)
    return playlist_songs

# Utility function to write playlists and playlist_songs data after modifications

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


# Helper functions for navigation and data mapping

def find_artist_by_id(artist_id):
    artists = load_artists()
    for artist in artists:
        if artist['artist_id'] == artist_id:
            return artist
    return None


def find_album_by_id(album_id):
    albums = load_albums()
    for album in albums:
        if album['album_id'] == album_id:
            return album
    return None


def find_song_by_id(song_id):
    songs = load_songs()
    for song in songs:
        if song['song_id'] == song_id:
            return song
    return None


def find_playlist_by_id(playlist_id):
    playlists = load_playlists()
    for plist in playlists:
        if plist['playlist_id'] == playlist_id:
            return plist
    return None


# Route Implementations
@app.route('/')
def dashboard():
    songs = load_songs()
    # Select featured songs: for draft - most played top 5
    featured_songs = sorted(songs, key=lambda x: x['play_count'], reverse=True)[:5]

    artists = load_artists()
    # Trending artists: top 5 by number of total plays of all their songs
    artist_play_counts = {}
    for artist in artists:
        artist_play_counts[artist['artist_id']] = 0
    for song in songs:
        if song['artist_id'] in artist_play_counts:
            artist_play_counts[song['artist_id']] += song['play_count']
    trending_artists_ids = sorted(artist_play_counts, key=artist_play_counts.get, reverse=True)[:5]
    trending_artists = [artist for artist in artists if artist['artist_id'] in trending_artists_ids]

    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)


@app.route('/songs', methods=['GET', 'POST'])
def song_catalog():
    songs = load_songs()
    genres_data = load_genres()
    genres = [genre['genre_name'] for genre in genres_data]

    selected_genre = request.args.get('genre', '')
    search_query = request.args.get('search', '').strip().lower()

    # Filter by genre
    if selected_genre:
        songs = [song for song in songs if song['genre'].lower() == selected_genre.lower()]

    # Filter by search query matching title, artist name, or album title
    if search_query:
        artists = load_artists()
        albums = load_albums()
        def matches_search(song):
            if search_query in song['title'].lower():
                return True
            artist = find_artist_by_id(song['artist_id'])
            if artist and search_query in artist['name'].lower():
                return True
            album = find_album_by_id(song['album_id'])
            if album and search_query in album['title'].lower():
                return True
            return False
        songs = [song for song in songs if matches_search(song)]

    return render_template('song_catalog.html', songs=songs, genres=genres, selected_genre=selected_genre)


@app.route('/songs/<int:song_id>')
def song_details(song_id):
    song = find_song_by_id(song_id)
    if not song:
        return "Song not found", 404
    artist = find_artist_by_id(song['artist_id'])
    album = find_album_by_id(song['album_id'])
    return render_template('song_details.html', song=song, artist=artist, album=album)


@app.route('/playlists')
def playlists():
    playlists = load_playlists()
    return render_template('playlists.html', playlists=playlists)


@app.route('/playlists/<int:playlist_id>', methods=['GET', 'POST'])
def playlist_details(playlist_id):
    playlist = find_playlist_by_id(playlist_id)
    if not playlist:
        return "Playlist not found", 404

    playlist_songs = load_playlist_songs()
    songs = load_songs()

    songs_in_playlist = [
        {
            'song': find_song_by_id(pls['song_id']),
            'playlist_song_id': pls['playlist_song_id']
        }
        for pls in playlist_songs if pls['playlist_id'] == playlist_id
    ]

    if request.method == 'POST':
        # Remove song or delete playlist
        if 'remove_song_id' in request.form:
            remove_song_id = int(request.form['remove_song_id'])
            # Remove playlist_songs entry
            playlist_songs = [pls for pls in playlist_songs if not (pls['playlist_id'] == playlist_id and pls['song_id'] == remove_song_id)]
            save_playlist_songs(playlist_songs)
            # Update playlist total_songs
            playlists = load_playlists()
            for pl in playlists:
                if pl['playlist_id'] == playlist_id:
                    pl['total_songs'] = len([pls for pls in playlist_songs if pls['playlist_id'] == playlist_id])
            save_playlists(playlists)
            return redirect(url_for('playlist_details', playlist_id=playlist_id))

        if 'delete_playlist' in request.form:
            # Delete playlist and its entries
            playlists = load_playlists()
            playlists = [pl for pl in playlists if pl['playlist_id'] != playlist_id]
            save_playlists(playlists)
            playlist_songs = load_playlist_songs()
            playlist_songs = [pls for pls in playlist_songs if pls['playlist_id'] != playlist_id]
            save_playlist_songs(playlist_songs)
            return redirect(url_for('playlists'))

    # Pass songs_in_playlist with song details
    songs_in_playlist_list = []
    for entry in songs_in_playlist:
        if entry['song']:
            s = entry['song']
            songs_in_playlist_list.append({
                'song_id': s['song_id'],
                'title': s['title'],
                'artist': find_artist_by_id(s['artist_id']),
                'duration': s['duration'],
                'playlist_song_id': entry['playlist_song_id']
            })

    return render_template('playlist_details.html', playlist=playlist, songs_in_playlist=songs_in_playlist_list)


@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist():
    form_data = {'title': '', 'description': '', 'errors': {}}
    if request.method == 'POST':
        title = request.form.get('playlist_name', '').strip()
        description = request.form.get('playlist_description', '').strip()

        errors = {}
        if not title:
            errors['title'] = 'Playlist name is required.'
        # (Optional: more validations)

        if errors:
            form_data = {'title': title, 'description': description, 'errors': errors}
            return render_template('create_playlist.html', form_data=form_data)

        # Save new playlist
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

    # GET
    return render_template('create_playlist.html', form_data=form_data)


@app.route('/albums')
def album_browse():
    albums = load_albums()
    sort_option = request.args.get('sort', 'title').lower()
    search_query = request.args.get('search', '').strip().lower()

    if search_query:
        artists = load_artists()
        def matches_search(album):
            if search_query in album['title'].lower():
                return True
            artist = find_artist_by_id(album['artist_id'])
            if artist and search_query in artist['name'].lower():
                return True
            return False
        albums = [album for album in albums if matches_search(album)]

    # Sorting
    if sort_option == 'title':
        albums.sort(key=lambda x: x['title'].lower())
    elif sort_option == 'artist':
        albums.sort(key=lambda x: find_artist_by_id(x['artist_id'])['name'].lower() if find_artist_by_id(x['artist_id']) else '')
    elif sort_option == 'year':
        albums.sort(key=lambda x: int(x['release_year']) if x['release_year'].isdigit() else 0)
    else:
        # default title
        albums.sort(key=lambda x: x['title'].lower())

    return render_template('album_browse.html', albums=albums, sort_option=sort_option, search_query=search_query)


@app.route('/albums/<int:album_id>')
def album_details(album_id):
    album = find_album_by_id(album_id)
    if not album:
        return "Album not found", 404
    songs = load_songs()
    songs_in_album = [song for song in songs if song['album_id'] == album_id]
    return render_template('album_details.html', album=album, songs_in_album=songs_in_album)


@app.route('/artists')
def artist_profiles():
    artists = load_artists()
    sort_option = request.args.get('sort', 'name').lower()
    search_query = request.args.get('search', '').strip().lower()

    if search_query:
        artists = [artist for artist in artists if search_query in artist['name'].lower()]

    if sort_option == 'name':
        artists.sort(key=lambda x: x['name'].lower())
    elif sort_option == 'genre':
        artists.sort(key=lambda x: x['genre'].lower())
    else:
        artists.sort(key=lambda x: x['name'].lower())

    return render_template('artist_profiles.html', artists=artists, sort_option=sort_option, search_query=search_query)


@app.route('/artists/<int:artist_id>')
def artist_details(artist_id):
    artist = find_artist_by_id(artist_id)
    if not artist:
        return "Artist not found", 404

    songs = load_songs()
    albums = load_albums()

    songs_by_artist = [song for song in songs if song['artist_id'] == artist_id]
    albums_by_artist = [album for album in albums if album['artist_id'] == artist_id]

    return render_template('artist_details.html', artist=artist, songs_by_artist=songs_by_artist, albums_by_artist=albums_by_artist)


@app.route('/genres')
def genre_exploration():
    genres = load_genres()
    selected_genre_name = request.args.get('genre', '')

    genre_songs = []
    genre_artists = []

    if selected_genre_name:
        songs = load_songs()
        artists = load_artists()
        genre_songs = [song for song in songs if song['genre'].lower() == selected_genre_name.lower()]
        # artists for genre
        genre_artists = [artist for artist in artists if artist['genre'].lower() == selected_genre_name.lower()]

    return render_template('genre_exploration.html', genres=genres, selected_genre=selected_genre_name, genre_songs=genre_songs, genre_artists=genre_artists)


if __name__ == '__main__':
    app.run(debug=True)
