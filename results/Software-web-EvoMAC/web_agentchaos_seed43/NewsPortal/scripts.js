/*
JavaScript for NewsPortal web application.
Handles client-side interactivity including button actions and dynamic content updates.
*/
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Dashboard page buttons
    const browseArticlesBtn = document.getElementById('browse-articles-button');
    if (browseArticlesBtn) {
        browseArticlesBtn.addEventListener('click', function () {
            window.location.href = '/catalog';
        });
    }
    const viewBookmarksBtn = document.getElementById('view-bookmarks-button');
    if (viewBookmarksBtn) {
        viewBookmarksBtn.addEventListener('click', function () {
            window.location.href = '/bookmarks';
        });
    }
    const trendingArticlesBtn = document.getElementById('trending-articles-button');
    if (trendingArticlesBtn) {
        trendingArticlesBtn.addEventListener('click', function () {
            window.location.href = '/trending';
        });
    }
    // Article Catalog page: submit form on category filter change
    const categoryFilter = document.getElementById('category-filter');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', function () {
            // Submit the form to filter articles by category
            const form = categoryFilter.closest('form');
            if (form) {
                form.submit();
            }
        });
    }
    // Article Catalog page: search input enter key triggers form submit
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('keydown', function (event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                const form = searchInput.closest('form');
                if (form) {
                    form.submit();
                }
            }
        });
    }
    // Article Details page: bookmark button submits form
    const bookmarkButton = document.getElementById('bookmark-button');
    if (bookmarkButton) {
        bookmarkButton.addEventListener('click', function () {
            // Submit the form to bookmark the article
            const form = bookmarkButton.closest('form');
            if (form) {
                form.submit();
            }
        });
    }
    // Bookmarks page: buttons for remove and read bookmarks
    const bookmarksList = document.getElementById('bookmarks-list');
    if (bookmarksList) {
        bookmarksList.addEventListener('click', function (event) {
            const target = event.target;
            if (target.tagName === 'BUTTON') {
                // Buttons have IDs like remove-bookmark-button-{id} or read-bookmark-button-{id}
                const id = target.id;
                if (id.startsWith('remove-bookmark-button-') || id.startsWith('read-bookmark-button-')) {
                    // Submit the form with the button clicked
                    const form = target.closest('form');
                    if (form) {
                        form.submit();
                    }
                }
            }
        });
    }
    // Bookmarks page: back to dashboard button
    const backToDashboardBtnBookmarks = document.getElementById('back-to-dashboard');
    if (backToDashboardBtnBookmarks) {
        backToDashboardBtnBookmarks.addEventListener('click', function () {
            // Submit the form to go back to dashboard
            const form = backToDashboardBtnBookmarks.closest('form');
            if (form) {
                form.submit();
            }
        });
    }
    // Comments page: filter by article dropdown
    const filterByArticle = document.getElementById('filter-by-article');
    if (filterByArticle) {
        filterByArticle.addEventListener('change', function () {
            const form = filterByArticle.closest('form');
            if (form) {
                form.submit();
            }
        });
    }
    // Comments page: write comment button
    const writeCommentBtn = document.getElementById('write-comment-button');
    if (writeCommentBtn) {
        writeCommentBtn.addEventListener('click', function () {
            const form = writeCommentBtn.closest('form');
            if (form) {
                form.submit();
            }
        });
    }
    // Comments page: back to dashboard button
    const backToDashboardBtnComments = document.querySelector('#comments-page #back-to-dashboard');
    if (backToDashboardBtnComments) {
        backToDashboardBtnComments.addEventListener('click', function () {
            const form = backToDashboardBtnComments.closest('form');
            if (form) {
                form.submit();
            }
        });
    }
    // Write Comment page: no special JS needed for now
    // Trending Articles page: time period filter dropdown
    const timePeriodFilter = document.getElementById('time-period-filter');
    if (timePeriodFilter) {
        timePeriodFilter.addEventListener('change', function () {
            const form = timePeriodFilter.closest('form');
            if (form) {
                form.submit();
            }
        });
    }
    // Trending Articles page: view article buttons
    const trendingList = document.getElementById('trending-list');
    if (trendingList) {
        trendingList.addEventListener('click', function (event) {
            const target = event.target;
            if (target.tagName === 'BUTTON' && target.id.startsWith('view-article-button-')) {
                const form = target.closest('form');
                if (form) {
                    form.submit();
                }
            }
        });
    }
    // Trending Articles page: back to dashboard button
    const backToDashboardBtnTrending = document.getElementById('back-to-dashboard');
    if (backToDashboardBtnTrending) {
        backToDashboardBtnTrending.addEventListener('click', function () {
            const form = backToDashboardBtnTrending.closest('form');
            if (form) {
                form.submit();
            }
        });
    }
    // Category page: sort by date button
    const sortByDateBtn = document.getElementById('sort-by-date');
    if (sortByDateBtn) {
        sortByDateBtn.addEventListener('click', function () {
            const form = sortByDateBtn.closest('form');
            if (form) {
                form.submit();
            }
        });
    }
    // Category page: sort by popularity button
    const sortByPopularityBtn = document.getElementById('sort-by-popularity');
    if (sortByPopularityBtn) {
        sortByPopularityBtn.addEventListener('click', function () {
            const form = sortByPopularityBtn.closest('form');
            if (form) {
                form.submit();
            }
        });
    }
    // Category page: back to dashboard button
    const backToDashboardBtnCategory = document.getElementById('back-to-dashboard');
    if (backToDashboardBtnCategory) {
        backToDashboardBtnCategory.addEventListener('click', function () {
            const form = backToDashboardBtnCategory.closest('form');
            if (form) {
                form.submit();
            }
        });
    }
    // Search Results page: back to dashboard button
    const backToDashboardBtnSearch = document.getElementById('back-to-dashboard');
    if (backToDashboardBtnSearch) {
        backToDashboardBtnSearch.addEventListener('click', function () {
            const form = backToDashboardBtnSearch.closest('form');
            if (form) {
                form.submit();
            }
        });
    }
});