/*
JavaScript for NewsPortal web application.
Handles UI behaviors such as navigation between pages,
dynamic filtering, sorting, and client-side interactivity.
*/
// Wait for DOM content to be loaded
document.addEventListener('DOMContentLoaded', function () {
    // Dashboard page buttons
    const browseArticlesBtn = document.getElementById('browse-articles-button');
    if (browseArticlesBtn) {
        browseArticlesBtn.addEventListener('click', function () {
            window.location.href = '/articles';
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
    // Article Catalog Page: search and category filter
    const searchInput = document.getElementById('search-input');
    const categoryFilter = document.getElementById('category-filter');
    if (searchInput || categoryFilter) {
        // On change or enter key, submit form or reload with query params
        function updateCatalog() {
            const searchVal = searchInput ? searchInput.value.trim() : '';
            const categoryVal = categoryFilter ? categoryFilter.value : '';
            let url = '/articles?';
            if (searchVal) {
                url += 'search=' + encodeURIComponent(searchVal) + '&';
            }
            if (categoryVal) {
                url += 'category=' + encodeURIComponent(categoryVal);
            }
            window.location.href = url;
        }
        if (searchInput) {
            searchInput.addEventListener('keydown', function (e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    updateCatalog();
                }
            });
        }
        if (categoryFilter) {
            categoryFilter.addEventListener('change', function () {
                updateCatalog();
            });
        }
    }
    // Article Catalog Page: view article buttons
    const articlesGrid = document.getElementById('articles-grid');
    if (articlesGrid) {
        articlesGrid.addEventListener('click', function (e) {
            if (e.target && e.target.tagName === 'BUTTON' && e.target.id.startsWith('view-article-button-')) {
                const articleId = e.target.id.replace('view-article-button-', '');
                window.location.href = '/article/' + articleId;
            }
        });
    }
    // Bookmarks Page: remove and read bookmark buttons
    const bookmarksList = document.getElementById('bookmarks-list');
    if (bookmarksList) {
        bookmarksList.addEventListener('click', function (e) {
            if (e.target && e.target.tagName === 'BUTTON') {
                const id = e.target.id;
                if (id.startsWith('remove-bookmark-button-')) {
                    const bookmarkId = id.replace('remove-bookmark-button-', '');
                    // Submit POST form to remove bookmark
                    removeBookmark(bookmarkId);
                } else if (id.startsWith('read-bookmark-button-')) {
                    const bookmarkId = id.replace('read-bookmark-button-', '');
                    window.location.href = '/bookmark/read/' + bookmarkId;
                }
            }
        });
    }
    // Comments Page: filter by article dropdown and write comment button
    const filterByArticle = document.getElementById('filter-by-article');
    if (filterByArticle) {
        filterByArticle.addEventListener('change', function () {
            const articleId = filterByArticle.value;
            let url = '/comments';
            if (articleId) {
                url += '?article=' + encodeURIComponent(articleId);
            }
            window.location.href = url;
        });
    }
    const writeCommentBtn = document.getElementById('write-comment-button');
    if (writeCommentBtn) {
        writeCommentBtn.addEventListener('click', function () {
            window.location.href = '/comments/write';
        });
    }
    // Write Comment Page: submit comment button
    const submitCommentBtn = document.getElementById('submit-comment-button');
    if (submitCommentBtn) {
        submitCommentBtn.addEventListener('click', function (e) {
            e.preventDefault();
            const form = submitCommentBtn.closest('form');
            if (form) {
                form.submit();
            }
        });
    }
    // Trending Articles Page: time period filter and view article buttons
    const timePeriodFilter = document.getElementById('time-period-filter');
    if (timePeriodFilter) {
        timePeriodFilter.addEventListener('change', function () {
            const period = timePeriodFilter.value;
            let url = '/trending';
            if (period) {
                url += '?period=' + encodeURIComponent(period);
            }
            window.location.href = url;
        });
    }
    const trendingList = document.getElementById('trending-list');
    if (trendingList) {
        trendingList.addEventListener('click', function (e) {
            if (e.target && e.target.tagName === 'BUTTON' && e.target.id.startsWith('view-article-button-')) {
                const articleId = e.target.id.replace('view-article-button-', '');
                window.location.href = '/article/' + articleId;
            }
        });
    }
    // Category Page: sort buttons and back to dashboard
    const sortByDateBtn = document.getElementById('sort-by-date');
    if (sortByDateBtn) {
        sortByDateBtn.addEventListener('click', function () {
            const urlParams = new URLSearchParams(window.location.search);
            urlParams.set('sort', 'date');
            window.location.search = urlParams.toString();
        });
    }
    const sortByPopularityBtn = document.getElementById('sort-by-popularity');
    if (sortByPopularityBtn) {
        sortByPopularityBtn.addEventListener('click', function () {
            const urlParams = new URLSearchParams(window.location.search);
            urlParams.set('sort', 'popularity');
            window.location.search = urlParams.toString();
        });
    }
    const backToDashboardBtns = document.querySelectorAll('#back-to-dashboard');
    backToDashboardBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            window.location.href = '/';
        });
    });
    // Search Results Page: back to dashboard button
    const backToDashboardBtnSearch = document.getElementById('back-to-dashboard');
    if (backToDashboardBtnSearch) {
        backToDashboardBtnSearch.addEventListener('click', function () {
            window.location.href = '/';
        });
    }
    // Article Details Page: bookmark button
    const bookmarkButton = document.getElementById('bookmark-button');
    if (bookmarkButton) {
        bookmarkButton.addEventListener('click', function () {
            const articleId = bookmarkButton.getAttribute('data-article-id');
            if (!articleId) return;
            // Create a form and submit POST to /bookmark/<article_id>
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '/bookmark/' + articleId;
            document.body.appendChild(form);
            form.submit();
        });
    }
    // Helper function to remove bookmark by POST
    function removeBookmark(bookmarkId) {
        // Create a form and submit POST to /bookmark/remove/<bookmark_id>
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/bookmark/remove/' + bookmarkId;
        document.body.appendChild(form);
        form.submit();
    }
});