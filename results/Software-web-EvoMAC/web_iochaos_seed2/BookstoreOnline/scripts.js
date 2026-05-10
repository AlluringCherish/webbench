/*
JavaScript for BookstoreOnline web application
Handles client-side interactivity such as button actions, filtering, and dynamic content updates
*/
// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
  // Dashboard page buttons
  const browseCatalogBtn = document.getElementById("browse-catalog-button");
  if (browseCatalogBtn) {
    browseCatalogBtn.addEventListener("click", () => {
      window.location.href = "/catalog";
    });
  }
  const viewCartBtn = document.getElementById("view-cart-button");
  if (viewCartBtn) {
    viewCartBtn.addEventListener("click", () => {
      window.location.href = "/cart";
    });
  }
  const bestsellersBtn = document.getElementById("bestsellers-button");
  if (bestsellersBtn) {
    bestsellersBtn.addEventListener("click", () => {
      window.location.href = "/bestsellers";
    });
  }
  // Catalog page: search and category filter
  const searchInput = document.getElementById("search-input");
  const categoryFilter = document.getElementById("category-filter");
  const booksGrid = document.getElementById("books-grid");
  if (searchInput && categoryFilter && booksGrid) {
    // Attach event listeners for filtering
    searchInput.addEventListener("input", filterBooks);
    categoryFilter.addEventListener("change", filterBooks);
  }
  // Reviews page: filter by rating
  const filterByRating = document.getElementById("filter-by-rating");
  if (filterByRating) {
    filterByRating.addEventListener("change", filterReviews);
  }
  // Reviews page: write review button
  const writeReviewBtn = document.getElementById("write-review-button");
  if (writeReviewBtn) {
    writeReviewBtn.addEventListener("click", () => {
      window.location.href = "/write_review";
    });
  }
  // Reviews page and Bestsellers page: back to dashboard buttons
  const backToDashboardBtns = document.querySelectorAll("#back-to-dashboard");
  backToDashboardBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      window.location.href = "/";
    });
  });
  // Bestsellers page: time period filter
  const timePeriodFilter = document.getElementById("time-period-filter");
  if (timePeriodFilter) {
    timePeriodFilter.addEventListener("change", () => {
      // Reload page with selected period as query param
      const period = timePeriodFilter.value;
      const url = new URL(window.location.href);
      url.searchParams.set("period", period);
      window.location.href = url.toString();
    });
  }
  // Book Catalog page: attach event listeners to view book buttons dynamically
  if (booksGrid) {
    booksGrid.addEventListener("click", (event) => {
      if (event.target && event.target.matches("button[id^='view-book-button-']")) {
        const bookId = event.target.id.replace("view-book-button-", "");
        window.location.href = `/book/${bookId}`;
      }
    });
  }
  // Bestsellers page: attach event listeners to view book buttons dynamically
  const bestsellersList = document.getElementById("bestsellers-list");
  if (bestsellersList) {
    bestsellersList.addEventListener("click", (event) => {
      if (event.target && event.target.matches("button[id^='view-book-button-']")) {
        const bookId = event.target.id.replace("view-book-button-", "");
        window.location.href = `/book/${bookId}`;
      }
    });
  }
  // Book Details page: add to cart button
  const addToCartBtn = document.getElementById("add-to-cart-button");
  if (addToCartBtn) {
    addToCartBtn.addEventListener("click", () => {
      const bookId = addToCartBtn.getAttribute("data-book-id");
      if (!bookId) return;
      // Send POST request to add to cart
      fetch("/cart/add", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ book_id: bookId }),
      })
        .then((response) => {
          if (response.ok) {
            alert("Book added to cart!");
          } else {
            alert("Failed to add book to cart.");
          }
        })
        .catch(() => {
          alert("Error adding book to cart.");
        });
    });
  }
  // Shopping Cart page: update quantity and remove item buttons
  const cartItemsTable = document.getElementById("cart-items-table");
  if (cartItemsTable) {
    cartItemsTable.addEventListener("change", (event) => {
      if (event.target && event.target.matches("input[id^='update-quantity-']")) {
        const itemId = event.target.id.replace("update-quantity-", "");
        const newQuantity = parseInt(event.target.value);
        if (isNaN(newQuantity) || newQuantity < 1) {
          alert("Quantity must be at least 1");
          event.target.value = 1;
          return;
        }
        // Send POST request to update quantity
        fetch("/cart/update", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ cart_id: itemId, quantity: newQuantity }),
        })
          .then((response) => {
            if (response.ok) {
              // Reload cart page to update totals
              window.location.reload();
            } else {
              alert("Failed to update quantity.");
            }
          })
          .catch(() => {
            alert("Error updating quantity.");
          });
      }
    });
    cartItemsTable.addEventListener("click", (event) => {
      if (event.target && event.target.matches("button[id^='remove-item-button-']")) {
        const itemId = event.target.id.replace("remove-item-button-", "");
        if (!confirm("Are you sure you want to remove this item from the cart?")) return;
        // Send POST request to remove item
        fetch("/cart/remove", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ cart_id: itemId }),
        })
          .then((response) => {
            if (response.ok) {
              // Reload cart page to update
              window.location.reload();
            } else {
              alert("Failed to remove item.");
            }
          })
          .catch(() => {
            alert("Error removing item.");
          });
      }
    });
  }
  // Shopping Cart page: proceed to checkout button
  const proceedCheckoutBtn = document.getElementById("proceed-checkout-button");
  if (proceedCheckoutBtn) {
    proceedCheckoutBtn.addEventListener("click", () => {
      window.location.href = "/checkout";
    });
  }
  // Write Review page: submit review button
  const submitReviewBtn = document.getElementById("submit-review-button");
  if (submitReviewBtn) {
    submitReviewBtn.addEventListener("click", () => {
      const selectBook = document.getElementById("select-book");
      const ratingSelect = document.getElementById("rating-select");
      const reviewText = document.getElementById("review-text");
      if (!selectBook || !ratingSelect || !reviewText) return;
      const bookId = selectBook.value;
      const rating = ratingSelect.value;
      const review = reviewText.value.trim();
      if (!bookId) {
        alert("Please select a book to review.");
        return;
      }
      if (!rating) {
        alert("Please select a rating.");
        return;
      }
      if (!review) {
        alert("Please write a review.");
        return;
      }
      // Send POST request to submit review
      fetch("/reviews/submit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          book_id: bookId,
          rating: rating,
          review_text: review,
        }),
      })
        .then((response) => {
          if (response.ok) {
            alert("Review submitted successfully!");
            window.location.href = "/reviews";
          } else {
            alert("Failed to submit review.");
          }
        })
        .catch(() => {
          alert("Error submitting review.");
        });
    });
  }
});
/**
 * Filter books in the catalog page based on search input and category filter
 */
function filterBooks() {
  const searchInput = document.getElementById("search-input");
  const categoryFilter = document.getElementById("category-filter");
  const booksGrid = document.getElementById("books-grid");
  if (!searchInput || !categoryFilter || !booksGrid) return;
  const searchTerm = searchInput.value.toLowerCase();
  const selectedCategory = categoryFilter.value;
  // Each book card should have data attributes for title, author, isbn, category
  const bookCards = booksGrid.querySelectorAll(".book-card");
  bookCards.forEach((card) => {
    const title = card.getAttribute("data-title").toLowerCase();
    const author = card.getAttribute("data-author").toLowerCase();
    const isbn = card.getAttribute("data-isbn").toLowerCase();
    const category = card.getAttribute("data-category");
    const matchesSearch =
      title.includes(searchTerm) || author.includes(searchTerm) || isbn.includes(searchTerm);
    const matchesCategory = selectedCategory === "All" || category === selectedCategory;
    if (matchesSearch && matchesCategory) {
      card.style.display = "";
    } else {
      card.style.display = "none";
    }
  });
}
/**
 * Filter reviews by rating on the reviews page
 */
function filterReviews() {
  const filterByRating = document.getElementById("filter-by-rating");
  const reviewsList = document.getElementById("reviews-list");
  if (!filterByRating || !reviewsList) return;
  const selectedRating = filterByRating.value;
  // Each review item should have data-rating attribute
  const reviewItems = reviewsList.querySelectorAll(".review-item");
  reviewItems.forEach((item) => {
    const rating = item.getAttribute("data-rating");
    if (selectedRating === "All" || rating === selectedRating) {
      item.style.display = "";
    } else {
      item.style.display = "none";
    }
  });
}