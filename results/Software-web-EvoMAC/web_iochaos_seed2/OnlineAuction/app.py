


JavaScript OnlineAuction
Handles filtering, pages.
*/

// Wait for DOM fully
document.addEventListener('DOMContentLoaded', function () {

    // Dashboard Page Buttons
    const browseAuctionsBtn = document.getElementById('browse-auctions-button');
    if (browseAuctionsBtn) {
        browseAuctionsBtn.addEventListener('click', () => {
            window.location.href = '/auction_catalog';
        });


=
{
        viewBidsBtn.addEventListener('click', () => {
            window.location.href = '/bid_history';
        });


= document.getElementById('trending-auctions-button');
(trendingAuctionsBtn) {
        trendingAuctionsBtn.addEventListener('click', () => {
            window.location.href = '/trending_auctions';
        });


// Auction Search Category
const =
categoryFilter =
= document.getElementById('auctions-grid');

categoryFilter && {
        // Attach event listeners for filtering
        searchInput.addEventListener('input', filterAuctions);
        categoryFilter.addEventListener('change', filterAuctions);
    }

filter auction based on category
{
        const searchTerm = searchInput.value.toLowerCase();
        const selectedCategory = categoryFilter.value;

        const auctionCards = auctionsGrid.querySelectorAll('[id^="view-auction-button-"]');
        // Each auction card button has id view-auction-button-{auction_id}
// We need to the to

auctionCards.forEach(button => {
            const card = button.closest('.auction-card');
            if (!card) return;

            const titleElem = card.querySelector('.auction-title');
            const descElem = card.querySelector('.auction-description');
            const categoryElem = card.getAttribute('data-category') || '';

            const titleText = titleElem ? titleElem.textContent.toLowerCase() : '';
            const descText = descElem ? descElem.textContent.toLowerCase() : '';
            const categoryText = categoryElem.toLowerCase();

            // Check if search term matches title, description, or auction id
            const auctionId = button.id.replace('view-auction-button-', '');
            const matchesSearch = titleText.includes(searchTerm) || descText.includes(searchTerm) || auctionId.includes(searchTerm);

            // Check if category matches or if 'All' is selected
            const matchesCategory = (selectedCategory === 'All' || selectedCategory === '' || categoryText === selectedCategory.toLowerCase());

            if (matchesSearch && matchesCategory) {
                card.style.display = '';
            } {
                card.style.display = 'none';
            }

}

Page: View Buttons
if {
        auctionsGrid.addEventListener('click', function (event) {
            if (event.target && event.target.id.startsWith('view-auction-button-')) {
                const auctionId = event.target.id.replace('view-auction-button-', '');
                window.location.href = `/auction_details/${auctionId}`;
}



Auction Details Bid

if {
        placeBidBtn.addEventListener('click', () => {
            const auctionId = placeBidBtn.getAttribute('data-auction-id');
            if (auctionId) {
                window.location.href = `/place_bid/${auctionId}`;




Page:

(submitBidBtn) {
        submitBidBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const bidderNameInput = document.getElementById('bidder-name');
            const bidAmountInput = document.getElementById('bid-amount');
            const auctionId = submitBidBtn.getAttribute('data-auction-id');

            if (!bidderNameInput || !bidAmountInput || !auctionId) {
                alert('Missing bid information.');
                return;
            }

bidderName
parseFloat(bidAmountInput.value);

(bidderName === '') {
                alert('Please enter your name.');
                return;
            }
{
                alert('Please enter a valid bid amount.');
                return;
            }

bid via form or AJAX
// Here the

{
                form.submit();
            }
});


Bid by Auction Dropdown
= document.getElementById('filter-by-auction');
const
if {
        filterByAuction.addEventListener('change', () => {
            const selectedAuction = filterByAuction.value.toLowerCase();
            const rows = bidsTable.querySelectorAll('tbody tr');

            rows.forEach(row => {
                const auctionNameCell = row.querySelector('td:nth-child(2)');
                if (!auctionNameCell) return;
                const auctionName = auctionNameCell.textContent.toLowerCase();

                if (selectedAuction === 'all' || selectedAuction === '' || auctionName === selectedAuction) {
                    row.style.display = '';
                } {
                    row.style.display = 'none';
                }




Page: by Button
sortByAmountBtn document.getElementById('sort-by-amount');
bidsTable) {
        sortByAmountBtn.addEventListener('click', () => {
            const tbody = bidsTable.querySelector('tbody');
            if (!tbody) return;

            // Get rows as array
            const rowsArray = Array.from(tbody.querySelectorAll('tr'));

            // Determine current sort order from button data attribute
            let ascending = sortByAmountBtn.getAttribute('data-ascending') === 'true';
            ascending = !ascending; // Toggle order
            sortByAmountBtn.setAttribute('data-ascending', ascending);

            // Sort rows by bid amount (4th column)
            rowsArray.sort((a, b) => {
                const aAmount = parseFloat(a.querySelector('td:nth-child(4)').textContent) || 0;
                const bAmount = parseFloat(b.querySelector('td:nth-child(4)').textContent) || 0;
                return ascending ? aAmount - bAmount : bAmount - aAmount;
            });

sorted rows to




// Page: View
= document.getElementById('categories-list');
{
        categoriesList.addEventListener('click', (event) => {
            if (event.target && event.target.id.startsWith('view-category-button-')) {
                const categoryId = event.target.id.replace('view-category-button-', '');
                window.location.href = `/auction_catalog?category_id=${categoryId}`;




Winners Filter
filterByWinnerInput document.getElementById('filter-by-winner');
winnersList
{
        filterByWinnerInput.addEventListener('input', () => {
            const filterText = filterByWinnerInput.value.toLowerCase();
            const winnerCards = winnersList.querySelectorAll('[id^="winner-card-"]');

            winnerCards.forEach(card => {
                const winnerNameElem = card.querySelector('.winner-name');
                if (!winnerNameElem) return;
                const winnerName = winnerNameElem.textContent.toLowerCase();

                if (winnerName.includes(filterText)) {
                    card.style.display = '';
                } {
                    card.style.display = 'none';
                }
});

}

// Time
const
const trendingList document.getElementById('trending-list');
(timeRangeFilter && {
        timeRangeFilter.addEventListener('change', () => {
            const selectedRange = timeRangeFilter.value;

            const trendingItems = trendingList.querySelectorAll('li');
            trendingItems.forEach(item => {
                const timePeriod = item.getAttribute('data-time-period');
                if (!timePeriod) return;

                if (selectedRange === 'All Time' || selectedRange === '' || timePeriod === selectedRange) {
                    item.style.display = '';
                } {
                    item.style.display = 'none';
                }
});
});
}

// Trending Auctions Auction
(trendingList) {
        trendingList.addEventListener('click', function (event) {
            if (event.target && event.target.id.startsWith('view-auction-button-')) {
                const auctionId = event.target.id.replace('view-auction-button-', '');
                window.location.href = `/auction_details/${auctionId}`;




//
const document.getElementById('status-filter');
document.getElementById('status-table');
{
        statusFilter.addEventListener('change', () => {
            const selectedStatus = statusFilter.value.toLowerCase();
            const rows = statusTable.querySelectorAll('tbody tr');

            rows.forEach(row => {
                const statusCell = row.querySelector('td:nth-child(2)');
                if (!statusCell) return;
                const statusText = statusCell.textContent.toLowerCase();

                if (selectedStatus === 'all' || selectedStatus === '' || statusText === selectedStatus) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
});

}

Auction Status
const
{
        refreshStatusBtn.addEventListener('click', () => {
            // Reload the page to refresh auction statuses
            location.reload();
        });


to Buttons
=
=> {
        button.addEventListener('click', () => {
            window.location.href = '/';
        });
});


