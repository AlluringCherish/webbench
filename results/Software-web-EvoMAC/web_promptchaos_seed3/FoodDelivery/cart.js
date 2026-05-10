'''
JavaScript logic for Shopping Cart page in FoodDelivery web application.
Handles rendering cart items, updating quantities, removing items, calculating totals,
and proceeding to checkout. Data is loaded from localStorage for persistence.
'''
// Utility function to load cart data from localStorage or initialize empty array
function loadCartData() {
  const data = localStorage.getItem('fooddelivery_cart');
  if (data) {
    try {
      return JSON.parse(data);
    } catch (e) {
      console.error('Error parsing cart data from localStorage:', e);
      return [];
    }
  }
  return [];
}
// Utility function to save cart data to localStorage
function saveCartData(cartItems) {
  localStorage.setItem('fooddelivery_cart', JSON.stringify(cartItems));
}
// Utility function to fetch menus data from menus.txt (local text file)
// Returns a Promise resolving to an array of menu items
async function fetchMenusData() {
  try {
    const response = await fetch('data/menus.txt');
    if (!response.ok) throw new Error('Failed to fetch menus data');
    const text = await response.text();
    const lines = text.trim().split('\n');
    // Skip header if present (check if first line contains 'item_id')
    const startIndex = lines[0].startsWith('item_id') ? 1 : 0;
    const menus = lines.slice(startIndex).map(line => {
      const [item_id, restaurant_id, item_name, category, description, price, availability] = line.split('|');
      return {
        item_id: parseInt(item_id),
        restaurant_id: parseInt(restaurant_id),
        item_name,
        category,
        description,
        price: parseFloat(price),
        availability: availability === '1'
      };
    });
    return menus;
  } catch (error) {
    console.error('Error loading menus data:', error);
    return [];
  }
}
// Global cart items array
let cartItems = [];
// Global menus data array
let menusData = [];
// Function to render cart items in the table
function renderCartItems() {
  const tbody = document.getElementById('cart-items-body');
  tbody.innerHTML = ''; // Clear existing rows
  let total = 0;
  if (cartItems.length === 0) {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td colspan="7" style="text-align:center;">Your cart is empty.</td>`;
    tbody.appendChild(tr);
    document.getElementById('total-amount').textContent = '0.00';
    return;
  }
  cartItems.forEach(item => {
    // Find menu details for this item_id
    const menuItem = menusData.find(m => m.item_id === item.item_id);
    if (!menuItem) return; // Skip if menu item not found
    const subtotal = menuItem.price * item.quantity;
    total += subtotal;
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${menuItem.item_id.toString().padStart(5, '0')}</td>
      <td>${menuItem.item_name}</td>
      <td>${menuItem.description}</td>
      <td>$${menuItem.price.toFixed(2)}</td>
      <td>
        <input type="number" id="update-quantity-${menuItem.item_id}" min="1" value="${item.quantity}" aria-label="Quantity for ${menuItem.item_name}" style="width: 60px;">
      </td>
      <td>$${subtotal.toFixed(2)}</td>
      <td>
        <button id="remove-item-button-${menuItem.item_id}" aria-label="Remove ${menuItem.item_name} from cart">Remove</button>
      </td>
    `;
    tbody.appendChild(tr);
    // Add event listeners for quantity input change and remove button
    const quantityInput = document.getElementById(`update-quantity-${menuItem.item_id}`);
    quantityInput.addEventListener('change', () => updateQuantity(menuItem.item_id));
    const removeButton = document.getElementById(`remove-item-button-${menuItem.item_id}`);
    removeButton.addEventListener('click', () => removeItem(menuItem.item_id));
  });
  document.getElementById('total-amount').textContent = total.toFixed(2);
}
// Function to update quantity of an item
function updateQuantity(item_id) {
  const input = document.getElementById(`update-quantity-${item_id}`);
  let newQuantity = parseInt(input.value);
  if (isNaN(newQuantity) || newQuantity < 1) {
    alert('Please enter a valid quantity (1 or more).');
    // Reset to previous quantity
    const existingItem = cartItems.find(i => i.item_id === item_id);
    input.value = existingItem ? existingItem.quantity : 1;
    return;
  }
  const itemIndex = cartItems.findIndex(i => i.item_id === item_id);
  if (itemIndex !== -1) {
    cartItems[itemIndex].quantity = newQuantity;
    saveCartData(cartItems);
    renderCartItems();
  }
}
// Function to remove an item from the cart
function removeItem(item_id) {
  const index = cartItems.findIndex(i => i.item_id === item_id);
  if (index !== -1) {
    cartItems.splice(index, 1);
    saveCartData(cartItems);
    renderCartItems();
  }
}
// Event listener for proceed to checkout button
document.getElementById('proceed-checkout-button').addEventListener('click', () => {
  if (cartItems.length === 0) {
    alert('Your cart is empty.');
    return;
  }
  // Redirect to checkout page
  window.location.href = 'checkout.html'; // Adjust URL as needed
});
// Initialization function to load data and render cart
async function initCartPage() {
  cartItems = loadCartData();
  menusData = await fetchMenusData();
  renderCartItems();
}
// Run initialization on page load
window.addEventListener('DOMContentLoaded', initCartPage);