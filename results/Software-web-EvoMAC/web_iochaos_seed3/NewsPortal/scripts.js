/*
JavaScript for NewsPortal frontend interactivity:
- Handle button clicks for navigation
- Handle filtering, searching, sorting on catalog, trending, comments, category pages
- Handle back to dashboard navigation
- Support dynamic elements with IDs as specified
*/
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
    // Article Catalog page: handle search and category filter
    const catalogPage = document.getElementById('catalog-page');
    if (catalogPage) {
        const searchInput = document.getElementById('search-input');
        const categoryFilter = document.getElementById('category-filter');
        function submitCatalogForm() {
            // Create a form and submit POST with search and category filter
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '/catalog';
            const searchInputField = document.createElement('input');
            searchInputField.type = 'hidden';
            searchInputField.name = 'search-input';
            searchInputField.value = searchInput.value;
            form.appendChild(searchInputField);
            const categoryFilterField = document.createElement('input');
            categoryFilterField.type = 'hidden';
            categoryFilterField.name = 'category-filter';
            categoryFilterField.value = categoryFilter.value;
            form.appendChild(categoryFilterField);
            document.body.appendChild(form);
            form.submit();
        }
        if (searchInput) {
            searchInput.addEventListener('keypress', function (e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    submitCatalogForm();
                }
            });
        }
        if (categoryFilter) {
            categoryFilter.addEventListener('change', function () {
                submitCatalogForm();
            });
        }
        // Add event listeners to all view-article buttons
        const articleButtons = catalogPage.querySelectorAll('[id^="view-article-button-"]');
        articleButtons.forEach(function (btn) {
            btn.addEventListener('click', function () {
                const articleId = btn.id.replace('view-article-button-', '');
                window.location.href = '/article/' + articleId;
            });
        });
    }
    // Article Details page: handle bookmark button
    const articleDetailsPage = document.getElementById('article-details-page');
    if (articleDetailsPage) {
        const bookmarkButton = document.getElementById('bookmark-button');
        if (bookmarkButton) {
            bookmarkButton.addEventListener('click', function () {
                // Submit the form containing the bookmark button
                // The button is inside a form with method POST
                bookmarkButton.closest('form').submit();
            });
        }
    }
    // Bookmarks page: handle remove and read bookmark buttons, back to dashboard
    const bookmarksPage = document.getElementById('bookmarks-page');
    if (bookmarksPage) {
        // Remove bookmark buttons
        const removeButtons = bookmarksPage.querySelectorAll('[id^="remove-bookmark-button-"]');
        removeButtons.forEach(function (btn) {
            btn.addEventListener('click', function () {
                // Submit form with the button's name
                btn.closest('form').submit();
            });
        });
        // Read bookmark buttons
        const readButtons = bookmarksPage.querySelectorAll('[id^="read-bookmark-button-"]');
        readButtons.forEach(function (btn) {
            btn.addEventListener('click', function () {
                btn.closest('form').submit();
            });
        });
        // Back to dashboard button
        const backBtn = document.getElementById('back-to-dashboard');
        if (backBtn) {
            backBtn.addEventListener('click', function () {
                backBtn.closest('form').submit();
            });
        }
    }
    // Comments page: handle write comment button, filter by article, back to dashboard
    const commentsPage = document.getElementById('comments-page');
    if (commentsPage) {
        const writeCommentBtn = document.getElementById('write-comment-button');
        if (writeCommentBtn) {
            writeCommentBtn.addEventListener('click', function () {
                writeCommentBtn.closest('form').submit();
            });
        }
        const filterByArticle = document.getElementById('filter-by-article');
        if (filterByArticle) {
            filterByArticle.addEventListener('change', function () {
                // Redirect with query param filter-by-article
                const selected = filterByArticle.value;
                const url = new URL(window.location.href);
                if (selected) {
                    url.searchParams.set('filter-by-article', selected);
                } else {
                    url.searchParams.delete('filter-by-article');
                }
                window.location.href = url.toString();
            });
        }
        const backBtn = document.getElementById('back-to-dashboard');
        if (backBtn) {
            backBtn.addEventListener('click', function () {
                backBtn.closest('form').submit();
            });
        }
    }
    // Write Comment page: handle submit comment button
    const writeCommentPage = document.getElementById('write-comment-page');
    if (writeCommentPage) {
        const submitCommentBtn = document.getElementById('submit-comment-button');
        if (submitCommentBtn) {
            submitCommentBtn.addEventListener('click', function () {
                submitCommentBtn.closest('form').submit();
            });
        }
    }
    // Trending Articles page: handle time period filter, view article buttons, back to dashboard
    const trendingPage = document.getElementById('trending-page');
    if (trendingPage) {
        const timePeriodFilter = document.getElementById('time-period-filter');
        if (timePeriodFilter) {
            timePeriodFilter.addEventListener('change', function () {
                // Redirect with query param time-period-filter
                const selected = timePeriodFilter.value;
                const url = new URL(window.location.href);
                if (selected) {
                    url.searchParams.set('time-period-filter', selected);
                } else {
                    url.searchParams.delete('time-period-filter');
                }
                window.location.href = url.toString();
            });
        }
        // View article buttons
        const viewArticleButtons = trendingPage.querySelectorAll('[id^="view-article-button-"]');
        viewArticleButtons.forEach(function (btn) {
            btn.addEventListener('click', function () {
                const articleId = btn.id.replace('view-article-button-', '');
                // Submit form with the button's name
                btn.closest('form').submit();
            });
        });
        // Back to dashboard button
        const backBtn = document.getElementById('back-to-dashboard');
        if (backBtn) {
            backBtn.addEventListener('click', function () {
                backBtn.closest('form').submit();
            });
        }
    }
    // Category page: handle sort buttons and back to dashboard
    const categoryPage = document.getElementById('category-page');
    if (categoryPage) {
        const sortByDateBtn = document.getElementById('sort-by-date');
        if (sortByDateBtn) {
            sortByDateBtn.addEventListener('click', function () {
                sortByDateBtn.closest('form').submit();
            });
        }
        const sortByPopularityBtn = document.getElementById('sort-by-popularity');
        if (sortByPopularityBtn) {
            sortByPopularityBtn.addEventListener('click', function () {
                sortByPopularityBtn.closest('form').submit();
            });
        }
        const backBtn = document.getElementById('back-to-dashboard');
        if (backBtn) {
            backBtn.addEventListener('click', function () {
                backBtn.closest('form').submit();
            });
        }
    }
    // Search Results page: handle view article buttons and back to dashboard
    const searchResultsPage = document.getElementById('search-results-page');
    if (searchResultsPage) {
        const viewArticleButtons = searchResultsPage.querySelectorAll('[id^="view-article-button-"]');
        viewArticleButtons.forEach(function (btn) {
            btn.addEventListener('click', function () {
                const articleId = btn.id.replace('view-article-button-', '');
                btn.closest('form').submit();
            });
        });
        const backBtn = document.getElementById('back-to-dashboard');
        if (backBtn) {
            backBtn.addEventListener('click', function () {
                backBtn.closest('form').submit();
            });
        }
    }
});