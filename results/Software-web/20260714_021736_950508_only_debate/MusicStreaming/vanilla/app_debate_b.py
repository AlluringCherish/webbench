from flask import Flask, render_template, request, redirect, url_for
from datetime import date
import os

app = Flask(__name__)
DATA_DIR = 'data'

# Utility Classes
class Song:
    def __init__(self, song_id, title, artist_id, album_id, genre, duration, release_date, play_count):
        self.song_id = int(song_id)
        self.title = title
        self.artist_id = int(artist_id)
        self.album_id = int(album_id)
        self.genre = genre
        self.duration = int(duration)
        self.release_date = release_date
        self.play_count = int(play_count)

class Artist:
    def __init__(self, artist_id, name, genre, country, formation_year):
        self.artist_id = int(artist_id)
        self.name = name
        self.genre = genre
        self.country = country
        self.formation_year = int(formation_year)

class Album:
    def __init__(self, album_id, title, artist_id, release_year, total_songs, genre):
        self.album_id = int(album_id)
        self.title = title
        self.artist_id = int(artist_id)
        self.release_year = release_year
        self.total_songs = int(total_songs)
        self.genre = genre

class Playlist:
    def __init__(self, playlist_id, title, description, creation_date, total_songs):
        self.playlist_id = int(playlist_id)
        self.title = title
        self.description = description
        self.creation_date = creation_date
        self.total_songs = int(total_songs)

class PlaylistSong:
    def __init__(self, playlist_song_id, playlist_id, song_id, added_date):
        self.playlist_song_id = int(playlist_song_id)
        self.playlist_id = int(playlist_id)
        self.song_id = int(song_id)
        self.added_date = added_date


# Data loading functions

def load_songs():
    songs = []
    path = os.path.join(DATA_DIR, 'songs.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    fields = line.split('|')
                    if len(fields) == 8:
                        song = Song(*fields)
                        songs.append(song)
    return songs

def load_artists():
    artists = []
    path = os.path.join(DATA_DIR, 'artists.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    fields = line.split('|')
                    if len(fields) == 5:
                        artist = Artist(*fields)
                        artists.append(artist)
    return artists


def load_albums():
    albums = []
    path = os.path.join(DATA_DIR, 'albums.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    fields = line.split('|')
                    if len(fields) == 6:
                        album = Album(*fields)
                        albums.append(album)
    return albums


def load_genres():
    genres = []
    path = os.path.join(DATA_DIR, 'genres.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    fields = line.split('|')
                    if len(fields) >= 2:
                        genres.append(fields[1])
    return genres


def load_playlists():
    playlists = []
    path = os.path.join(DATA_DIR, 'playlists.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    fields = line.split('|')
                    if len(fields) == 5:
                        playlist = Playlist(*fields)
                        playlists.append(playlist)
    return playlists


def load_playlist_songs():
    playlist_songs = []
    path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    fields = line.split('|')
                    if len(fields) == 4:
                        ps = PlaylistSong(*fields)
                        playlist_songs.append(ps)
    return playlist_songs

# Helper Functions

def get_artist_by_id(artist_id):
    artists = load_artists()
    for artist in artists:
        if artist.artist_id == artist_id:
            return artist
    return None


def get_album_by_id(album_id):
    albums = load_albums()
    for album in albums:
        if album.album_id == album_id:
            return album
    return None


def get_song_by_id(song_id):
    songs = load_songs()
    for song in songs:
        if song.song_id == song_id:
            return song
    return None


def get_playlist_by_id(playlist_id):
    playlists = load_playlists()
    for playlist in playlists:
        if playlist.playlist_id == playlist_id:
            return playlist
    return None


def get_next_id(file_path):
    max_id = 0
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts=line.split('|')
                    if parts[0].isdigit():
                        max_id = max(max_id, int(parts[0]))
    return max_id + 1

# Routes

@app.route('/')
def dashboard():
    songs = load_songs()
    songs_sorted = sorted(songs, key=lambda s: s.play_count, reverse=True)
    featured_songs = songs_sorted[:5]
    artists = load_artists()
    trending_artists = sorted(artists, key=lambda a: a.formation_year, reverse=True)[:5]
    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)

@app.route('/songs', methods=['GET', 'POST'])
def songs_catalog():
    songs = load_songs()
    genres = load_genres()
    search_query = ''
    genre_filter = ''

    if request.method == 'POST':
        song_id = request.form.get('song_id')
        playlist_id = request.form.get('playlist_id')
        if song_id and playlist_id:
            playlist_songs = load_playlist_songs()
            playlist_song_id = get_next_id(os.path.join(DATA_DIR, 'playlist_songs.txt'))
            added_date = date.today().isoformat()
            new_entry = f"{playlist_song_id}|{playlist_id}|{song_id}|{added_date}\n"
            with open(os.path.join(DATA_DIR, 'playlist_songs.txt'), 'a', encoding='utf-8') as f:
                f.write(new_entry)
        return redirect(url_for('songs_catalog'))
    else:
        search_query = request.args.get('search_query', '').strip()
        genre_filter = request.args.get('genre_filter', '').strip()
        filtered_songs = songs
        if search_query:
            filtered_songs = [s for s in filtered_songs if search_query.lower() in s.title.lower()]
        if genre_filter:
            filtered_songs = [s for s in filtered_songs if s.genre == genre_filter]
        return render_template('song_catalog.html', songs=filtered_songs, genres=genres, search_query=search_query, genre_filter=genre_filter)

@app.route('/songs/<int:song_id>')
def song_details(song_id):
    song = get_song_by_id(song_id)
    if not song:
        return 'Song not found', 404
    artist = get_artist_by_id(song.artist_id)
    album = get_album_by_id(song.album_id)
    return render_template('song_details.html', song=song, artist=artist, album=album)

@app.route('/playlists')
def playlists():
    playlists = load_playlists()
    return render_template('playlists.html', playlists=playlists)

@app.route('/playlists/<int:playlist_id>', methods=['GET', 'POST'])
def playlist_details(playlist_id):
    playlist = get_playlist_by_id(playlist_id)
    if not playlist:
        return 'Playlist not found', 404

    if request.method == 'POST':
        if 'song_id' in request.form:
            song_id = request.form.get('song_id')
            playlist_songs = load_playlist_songs()
            playlist_songs = [ps for ps in playlist_songs if not (ps.playlist_id == playlist_id and str(ps.song_id) == song_id)]
            with open(os.path.join(DATA_DIR, 'playlist_songs.txt'), 'w', encoding='utf-8') as f:
                for ps in playlist_songs:
                    f.write(f'{ps.playlist_song_id}|{ps.playlist_id}|{ps.song_id}|{ps.added_date}\n')
            # Update total songs count
            playlist_songs_filtered = [ps for ps in playlist_songs if ps.playlist_id == playlist_id]
            playlists = load_playlists()
            for p in playlists:
                if p.playlist_id == playlist_id:
                    p.total_songs = len(playlist_songs_filtered)
            with open(os.path.join(DATA_DIR, 'playlists.txt'), 'w', encoding='utf-8') as f:
                for p in playlists:
                    f.write(f'{p.playlist_id}|{p.title}|{p.description}|{p.creation_date}|{p.total_songs}\n')

        elif 'delete' in request.form:
            playlists = load_playlists()
            playlists = [p for p in playlists if p.playlist_id != playlist_id]
            with open(os.path.join(DATA_DIR, 'playlists.txt'), 'w', encoding='utf-8') as f:
                for p in playlists:
                    f.write(f'{p.playlist_id}|{p.title}|{p.description}|{p.creation_date}|{p.total_songs}\n')

            playlist_songs = load_playlist_songs()
            playlist_songs = [ps for ps in playlist_songs if ps.playlist_id != playlist_id]
            with open(os.path.join(DATA_DIR, 'playlist_songs.txt'), 'w', encoding='utf-8') as f:
                for ps in playlist_songs:
                    f.write(f'{ps.playlist_song_id}|{ps.playlist_id}|{ps.song_id}|{ps.added_date}\n')

            return redirect(url_for('playlists'))

        return redirect(url_for('playlist_details', playlist_id=playlist_id))

    else:
        playlist_songs = load_playlist_songs()
        songs = load_songs()
        songs_in_playlist = [s for ps in playlist_songs if ps.playlist_id == playlist_id for s in songs if s.song_id == ps.song_id]
        return render_template('playlist_details.html', playlist=playlist, songs=songs_in_playlist)

@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist():
    errors = None
    if request.method == 'POST':
        title = request.form.get('playlist_name', '').strip()
        description = request.form.get('playlist_description', '').strip()
        errors = {}
        if not title:
            errors['title'] = 'Playlist name cannot be empty.'
        if errors:
            return render_template('create_playlist.html', errors=errors)
        playlist_id = get_next_id(os.path.join(DATA_DIR, 'playlists.txt'))
        creation_date = date.today().isoformat()
        total_songs = 0
        new_entry = f"{playlist_id}|{title}|{description}|{creation_date}|{total_songs}\n"
        with open(os.path.join(DATA_DIR, 'playlists.txt'), 'a', encoding='utf-8') as f:
            f.write(new_entry)
        return redirect(url_for('playlists'))

    return render_template('create_playlist.html', errors=None)

@app.route('/albums', methods=['GET', 'POST'])
def albums():
    albums = load_albums()
    search_albums = ''
    sort_albums = ''

    if request.method == 'POST':
        # Spec does not define any POST modification here
        return redirect(url_for('albums'))
    else:
        search_albums = request.args.get('search_albums', '').strip()
        sort_albums = request.args.get('sort_albums', '').strip()
        filtered_albums = albums
        if search_albums:
            filtered_albums = [a for a in filtered_albums if search_albums.lower() in a.title.lower()]
        if sort_albums == 'title':
            filtered_albums = sorted(filtered_albums, key=lambda a: a.title)
        elif sort_albums == 'release_year':
            filtered_albums = sorted(filtered_albums, key=lambda a: a.release_year)

        return render_template('albums.html', albums=filtered_albums, search_albums=search_albums, sort_albums=sort_albums)

@app.route('/albums/<int:album_id>', methods=['GET', 'POST'])
def album_details(album_id):
    album = get_album_by_id(album_id)
    if not album:
        return 'Album not found', 404

    songs = load_songs()
    songs_in_album = [s for s in songs if s.album_id == album_id]

    if request.method == 'POST':
        playlist_id = request.form.get('playlist_id')
        if playlist_id:
            playlist_songs = load_playlist_songs()
            playlist_song_id = get_next_id(os.path.join(DATA_DIR, 'playlist_songs.txt'))
            added_date = date.today().isoformat()
            existing_pairs = set((ps.song_id, ps.playlist_id) for ps in playlist_songs)
            new_entries = []
            for song in songs_in_album:
                if (song.song_id, int(playlist_id)) not in existing_pairs:
                    new_entries.append(f"{playlist_song_id}|{playlist_id}|{song.song_id}|{added_date}\n")
                    playlist_song_id += 1
            with open(os.path.join(DATA_DIR, 'playlist_songs.txt'), 'a', encoding='utf-8') as f:
                for entry in new_entries:
                    f.write(entry)
        return redirect(url_for('album_details', album_id=album_id))

    return render_template('album_details.html', album=album, songs=songs_in_album)

@app.route('/artists', methods=['GET', 'POST'])
def artists():
    artists = load_artists()
    search_artists = ''
    artists_sort = ''
    if request.method == 'POST':
        # Spec does not define POST modifications here
        return redirect(url_for('artists'))
    else:
        search_artists = request.args.get('search_artists', '').strip()
        artists_sort = request.args.get('artists_sort', '').strip()
        filtered_artists = artists
        if search_artists:
            filtered_artists = [a for a in filtered_artists if search_artists.lower() in a.name.lower()]
        if artists_sort == 'name':
            filtered_artists = sorted(filtered_artists, key=lambda a: a.name)
        elif artists_sort == 'formation_year':
            filtered_artists = sorted(filtered_artists, key=lambda a: a.formation_year)
        return render_template('artists.html', artists=filtered_artists, search_artists=search_artists, artists_sort=artists_sort)

@app.route('/artists/<int:artist_id>')
def artist_profile(artist_id):
    artist = get_artist_by_id(artist_id)
    if not artist:
        return 'Artist not found', 404
    songs = load_songs()
    albums = load_albums()
    songs_of_artist = [s for s in songs if s.artist_id == artist_id]
    albums_of_artist = [a for a in albums if a.artist_id == artist_id]
    return render_template('artist_profile.html', artist=artist, songs=songs_of_artist, albums=albums_of_artist)

@app.route('/genres', methods=['GET', 'POST'])
def genres():
    genres = load_genres()
    selected_genre = ''
    genre_songs = []
    genre_artists = []

    if request.method == 'POST':
        selected_genre = request.form.get('selected_genre', '')
        songs = load_songs()
        artists = load_artists()
        genre_songs = [s for s in songs if s.genre == selected_genre]
        seen_artist_ids = set()
        genre_artists = []
        for artist in artists:
            if artist.genre == selected_genre and artist.artist_id not in seen_artist_ids:
                genre_artists.append(artist)
                seen_artist_ids.add(artist.artist_id)

    return render_template('genres.html', genres=genres, selected_genre=selected_genre, genre_songs=genre_songs, genre_artists=genre_artists)


if __name__ == '__main__':
    app.run(debug=True)
