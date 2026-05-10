/**
 * scripts.js
 * JavaScript for client-side interactivity in the MusicStreaming web application.
 * Handles button actions, dynamic content updates, and navigation.
 */
document.addEventListener('DOMContentLoaded', function () {
    // Navigation buttons on Dashboard
    const browseSongsBtn = document.getElementById('browse-songs-button');
    if (browseSongsBtn) {
        browseSongsBtn.addEventListener('click', () => {
            window.location.href = '/songs';
        });
    }
    const myPlaylistsBtn = document.getElementById('my-playlists-button');
    if (myPlaylistsBtn) {
        myPlaylistsBtn.addEventListener('click', () => {
            window.location.href = '/playlists';
        });
    }
    const trendingArtistsBtn = document.getElementById('trending-artists-button');
    if (trendingArtistsBtn) {
        trendingArtistsBtn.addEventListener('click', () => {
            // Trending artists are shown on dashboard, so redirect to dashboard
            window.location.href = '/';
        });
    }
    // Back to dashboard buttons (multiple pages)
    const backToDashboardBtns = document.querySelectorAll('#back-to-dashboard');
    backToDashboardBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            window.location.href = '/';
        });
    });
    // Add to playlist buttons on Song Catalog page
    const addToPlaylistButtons = document.querySelectorAll('[id^="add-to-playlist-button-"]');
    addToPlaylistButtons.forEach(button => {
        button.addEventListener('click', () => {
            const songId = button.id.replace('add-to-playlist-button-', '');
            // Show prompt to select playlist to add song to
            fetch('/playlists')
                .then(response => response.text())
                .then(html => {
                    // Parse playlists from the HTML response
                    // Since we don't have an API endpoint for playlists JSON,
                    // we will prompt user to enter playlist ID manually.
                    // Alternatively, this can be improved with a modal and API.
                    const playlistId = prompt('Enter Playlist ID to add this song:');
                    if (playlistId) {
                        // Redirect to a route that adds song to playlist
                        // We don't have a dedicated route for adding single song to playlist,
                        // so we can create a form and submit POST request via fetch.
                        addSongToPlaylist(songId, playlistId);
                    }
                });
        });
    });
    // Function to add a song to a playlist via POST request
    function addSongToPlaylist(songId, playlistId) {
        fetch('/playlists/add_song', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ song_id: songId, playlist_id: playlistId })
        })
        .then(response => {
            if (response.ok) {
                alert('Song added to playlist successfully.');
            } else {
                alert('Failed to add song to playlist.');
            }
        })
        .catch(() => {
            alert('Error occurred while adding song to playlist.');
        });
    }
    // Remove song buttons on Playlist Details page
    const removeSongButtons = document.querySelectorAll('[id^="remove-song-button-"]');
    removeSongButtons.forEach(button => {
        button.addEventListener('click', () => {
            const songId = button.id.replace('remove-song-button-', '');
            const playlistDetailsPage = document.getElementById('playlist-details-page');
            if (!playlistDetailsPage) return;
            const playlistId = playlistDetailsPage.getAttribute('data-playlist-id');
            if (!playlistId) return;
            if (confirm('Are you sure you want to remove this song from the playlist?')) {
                window.location.href = `/playlists/${playlistId}/remove_song/${songId}`;
            }
        });
    });
    // Delete playlist button on Playlist Details page
    const deletePlaylistButton = document.getElementById('delete-playlist-button');
    if (deletePlaylistButton) {
        deletePlaylistButton.addEventListener('click', () => {
            const playlistDetailsPage = document.getElementById('playlist-details-page');
            if (!playlistDetailsPage) return;
            const playlistId = playlistDetailsPage.getAttribute('data-playlist-id');
            if (!playlistId) return;
            if (confirm('Are you sure you want to delete this playlist? This action cannot be undone.')) {
                // Submit POST request to delete playlist
                fetch(`/playlists/${playlistId}/delete`, {
                    method: 'POST'
                })
                .then(response => {
                    if (response.redirected) {
                        window.location.href = response.url;
                    } else {
                        alert('Failed to delete playlist.');
                    }
                })
                .catch(() => {
                    alert('Error occurred while deleting playlist.');
                });
            }
        });
    }
    // Create playlist page buttons
    const savePlaylistButton = document.getElementById('save-playlist-button');
    if (savePlaylistButton) {
        savePlaylistButton.addEventListener('click', (e) => {
            // The form submission is handled by backend, so no extra JS needed here
            // But we can do client-side validation if desired
            const nameInput = document.getElementById('playlist-name-input');
            if (nameInput && nameInput.value.trim() === '') {
                e.preventDefault();
                alert('Playlist name is required.');
                nameInput.focus();
            }
        });
    }
    const cancelCreateButton = document.getElementById('cancel-create-button');
    if (cancelCreateButton) {
        cancelCreateButton.addEventListener('click', () => {
            window.location.href = '/playlists';
        });
    }
    // Album Details page: Add album to playlist button
    const addAlbumToPlaylistButton = document.getElementById('add-album-to-playlist-button');
    if (addAlbumToPlaylistButton) {
        addAlbumToPlaylistButton.addEventListener('click', () => {
            const albumDetailsPage = document.getElementById('album-details-page');
            if (!albumDetailsPage) return;
            const albumId = albumDetailsPage.getAttribute('data-album-id');
            if (!albumId) return;
            // Prompt user to enter playlist ID to add all songs
            const playlistId = prompt('Enter Playlist ID to add all songs from this album:');
            if (playlistId) {
                // Create a form and submit POST request to add album songs to playlist
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = `/albums/${albumId}/add_to_playlist`;
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'playlist_id';
                input.value = playlistId;
                form.appendChild(input);
                document.body.appendChild(form);
                form.submit();
            }
        });
    }
    // Genre Exploration page: select genre dropdown change
    const selectGenreDropdown = document.getElementById('select-genre');
    if (selectGenreDropdown) {
        selectGenreDropdown.addEventListener('change', () => {
            const selectedGenre = selectGenreDropdown.value;
            if (selectedGenre) {
                window.location.href = `/genres?genre=${encodeURIComponent(selectedGenre)}`;
            } else {
                window.location.href = '/genres';
            }
        });
    }
});