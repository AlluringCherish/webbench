/*
Client-side JavaScript for MusicStreaming web application.
Handles button clicks, dynamic filtering, and navigation interactivity.
*/
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Example: Add event listeners for buttons if needed
    // Back to dashboard buttons
    const backToDashboardButtons = document.querySelectorAll('#back-to-dashboard');
    backToDashboardButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            window.location.href = '/dashboard';
        });
    });
    // Browse songs button on dashboard
    const browseSongsButton = document.getElementById('browse-songs-button');
    if (browseSongsButton) {
        browseSongsButton.addEventListener('click', function() {
            window.location.href = '/songs';
        });
    }
    // My playlists button on dashboard
    const myPlaylistsButton = document.getElementById('my-playlists-button');
    if (myPlaylistsButton) {
        myPlaylistsButton.addEventListener('click', function() {
            window.location.href = '/playlists';
        });
    }
    // Trending artists button on dashboard
    const trendingArtistsButton = document.getElementById('trending-artists-button');
    if (trendingArtistsButton) {
        trendingArtistsButton.addEventListener('click', function() {
            window.location.href = '/artists';
        });
    }
    // Genre filter on song catalog page: submit form on change
    const genreFilter = document.getElementById('genre-filter');
    if (genreFilter) {
        genreFilter.addEventListener('change', function() {
            this.form.submit();
        });
    }
    // Search input on song catalog page: submit form on Enter key
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                this.form.submit();
            }
        });
    }
    // Search and sort on albums page
    const searchAlbumsInput = document.getElementById('search-albums');
    if (searchAlbumsInput) {
        searchAlbumsInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                this.form.submit();
            }
        });
    }
    const sortAlbumsSelect = document.getElementById('sort-albums');
    if (sortAlbumsSelect) {
        sortAlbumsSelect.addEventListener('change', function() {
            this.form.submit();
        });
    }
    // Search and sort on artists page
    const searchArtistsInput = document.getElementById('search-artists');
    if (searchArtistsInput) {
        searchArtistsInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                this.form.submit();
            }
        });
    }
    const artistsSortSelect = document.getElementById('artists-sort');
    if (artistsSortSelect) {
        artistsSortSelect.addEventListener('change', function() {
            this.form.submit();
        });
    }
    // Genre selection on genre exploration page: submit form on change
    const selectGenre = document.getElementById('select-genre');
    if (selectGenre) {
        selectGenre.addEventListener('change', function() {
            this.form.submit();
        });
    }
    // Cancel create playlist button on create playlist page
    const cancelCreateButton = document.getElementById('cancel-create-button');
    if (cancelCreateButton) {
        cancelCreateButton.addEventListener('click', function() {
            window.location.href = '/playlists';
        });
    }
    // Play button on song details page: alert playing song
    const playButton = document.getElementById('play-button');
    if (playButton) {
        playButton.addEventListener('click', function() {
            alert('Playing ' + document.getElementById('song-title').textContent);
        });
    }
});