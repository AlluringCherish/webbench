/*
JavaScript file for OnlineAuction web application.
Implements client-side interactivity such as button actions,
filtering, sorting, and dynamic content updates without full page reloads.
*/
// Wait for DOM content to be loaded
document.addEventListener('DOMContentLoaded', function () {
    // Dashboard page buttons
    const browseAuctionsBtn = document.getElementById('browse-auctions-button');
    if (browseAuctionsBtn) {
        browseAuctionsBtn.addEventListener('click', function () {
            window.location.href = '/catalog';
        });
    }
    const viewBidsBtn = document.getElementById('view-bids-button');
    if (viewBidsBtn) {
        viewBidsBtn.addEventListener('click', function () {
            window.location.href = '/bid_history';
        });
    }
    const trendingAuctionsBtn = document.getElementById('trending-auctions-button');
    if (trendingAuctionsBtn) {
        trendingAuctionsBtn.addEventListener('click', function () {
            window.location.href = '/trending';
        });
    }
    // Back to dashboard buttons on various pages
    const backToDashboardBtns = document.querySelectorAll('#back-to-dashboard');
    backToDashboardBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            window.location.href = '/';
        });
    });
    // Auction Catalog page: search and category filter
    const searchInput = document.getElementById('search-input');
    const categoryFilter = document.getElementById('category-filter');
    if (searchInput && categoryFilter) {
        // On search input enter key press, submit form or reload with query params
        searchInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                applyCatalogFilters();
            }
        });
        // On category change, apply filters
        categoryFilter.addEventListener('change', function () {
            applyCatalogFilters();
        });
    }
    // Function to apply catalog filters by reloading page with query params
    function applyCatalogFilters() {
        const searchVal = searchInput.value.trim();
        const categoryVal = categoryFilter.value;
        let url = '/catalog?';
        if (searchVal) {
            url += 'search=' + encodeURIComponent(searchVal) + '&';
        }
        if (categoryVal && categoryVal.toLowerCase() !== 'all') {
            url += 'category=' + encodeURIComponent(categoryVal) + '&';
        }
        // Remove trailing &
        url = url.replace(/&$/, '');
        window.location.href = url;
    }
    // Auction Catalog and Trending Auctions: view auction buttons
    const viewAuctionButtons = document.querySelectorAll('[id^="view-auction-button-"]');
    viewAuctionButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const auctionId = btn.id.replace('view-auction-button-', '');
            if (auctionId) {
                window.location.href = '/auction/' + auctionId;
            }
        });
    });
    // Auction Categories page: view category buttons
    const viewCategoryButtons = document.querySelectorAll('[id^="view-category-button-"]');
    viewCategoryButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const categoryId = btn.id.replace('view-category-button-', '');
            if (categoryId) {
                window.location.href = '/category/' + categoryId;
            }
        });
    });
    // Bid History page: filter by auction dropdown and sort by amount button
    const filterByAuctionDropdown = document.getElementById('filter-by-auction');
    const sortByAmountBtn = document.getElementById('sort-by-amount');
    if (filterByAuctionDropdown) {
        filterByAuctionDropdown.addEventListener('change', function () {
            applyBidHistoryFilters();
        });
    }
    if (sortByAmountBtn) {
        sortByAmountBtn.addEventListener('click', function () {
            // Toggle sort state stored in data attribute
            let currentSort = sortByAmountBtn.getAttribute('data-sorted');
            if (currentSort === 'true') {
                sortByAmountBtn.setAttribute('data-sorted', 'false');
                sortByAmountBtn.textContent = 'Sort by Amount';
            } else {
                sortByAmountBtn.setAttribute('data-sorted', 'true');
                sortByAmountBtn.textContent = 'Sort by Amount (Desc)';
            }
            applyBidHistoryFilters();
        });
    }
    function applyBidHistoryFilters() {
        const auctionId = filterByAuctionDropdown ? filterByAuctionDropdown.value : '';
        const sortByAmount = (sortByAmountBtn && sortByAmountBtn.getAttribute('data-sorted') === 'true') ? 'true' : 'false';
        let url = '/bid_history?';
        if (auctionId) {
            url += 'filter_by_auction=' + encodeURIComponent(auctionId) + '&';
        }
        url += 'sort_by_amount=' + sortByAmount;
        window.location.href = url;
    }
    // Winners page: filter by winner input field
    const filterByWinnerInput = document.getElementById('filter-by-winner');
    if (filterByWinnerInput) {
        filterByWinnerInput.addEventListener('input', function () {
            // Debounce input to avoid too many reloads
            if (filterByWinnerInput._timeout) {
                clearTimeout(filterByWinnerInput._timeout);
            }
            filterByWinnerInput._timeout = setTimeout(function () {
                const filterVal = filterByWinnerInput.value.trim();
                let url = '/winners';
                if (filterVal) {
                    url += '?filter_by_winner=' + encodeURIComponent(filterVal);
                }
                window.location.href = url;
            }, 500);
        });
    }
    // Trending Auctions page: time range filter dropdown
    const timeRangeFilter = document.getElementById('time-range-filter');
    if (timeRangeFilter) {
        timeRangeFilter.addEventListener('change', function () {
            const selectedRange = timeRangeFilter.value;
            let url = '/trending?time_range=' + encodeURIComponent(selectedRange);
            window.location.href = url;
        });
    }
    // Auction Status page: status filter dropdown and refresh button
    const statusFilter = document.getElementById('status-filter');
    const refreshStatusBtn = document.getElementById('refresh-status-button');
    if (statusFilter) {
        statusFilter.addEventListener('change', function () {
            const selectedStatus = statusFilter.value;
            let url = '/status?status=' + encodeURIComponent(selectedStatus);
            window.location.href = url;
        });
    }
    if (refreshStatusBtn) {
        refreshStatusBtn.addEventListener('click', function () {
            // Reload current page to refresh statuses
            window.location.reload();
        });
    }
});