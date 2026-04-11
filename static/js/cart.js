// ========================================
// CART.JS - FitCheck Shopping Cart
// Database-backed with full functionality
// ========================================
 
document.addEventListener("DOMContentLoaded", function () {
    if (window.location.pathname.includes("/cart")) {
        loadCart();
    }
    updateCartBadge();
});
 
// ========== LOAD CART FROM DATABASE ==========
function loadCart() {
    fetch("/api/cart")
        .then(res => res.json())
        .then(cart => {
            const container = document.getElementById("cartItemsContainer");
            const emptyMessage = document.getElementById("emptyCartMessage");
            const itemCount = document.getElementById("cartItemCount");
 
            if (!cart.length) {
                container.style.display = "none";
                emptyMessage.style.display = "block";
                itemCount.textContent = "0 Items";
                updatePriceSummary([]);
                return;
            }
 
            container.style.display = "block";
            emptyMessage.style.display = "none";
            itemCount.textContent = `${cart.length} Item${cart.length > 1 ? 's' : ''}`;
 
            // Generate cart items HTML with proper structure matching CSS
            container.innerHTML = cart.map(item => `
                <div class="cart-item" data-product-id="${item.productId}">
                    <!-- Item Image -->
                    <div class="item-image">
                        <img src="/static/uploads/products/${item.image}" alt="${item.productName}">
                    </div>
 
                    <!-- Item Details -->
                    <div class="item-details">
                        <div class="item-brand">${item.brand}</div>
                        <div class="item-name">${item.productName}</div>
 
                        <!-- Price -->
                        <div class="item-price">
                            <span class="current-price">₹${parseFloat(item.price).toFixed(2)}</span>
                            ${item.basePrice > item.price ? 
                                `<span class="original-price">₹${parseFloat(item.basePrice).toFixed(2)}</span>` : ''}
                            ${item.discount > 0 ? 
                                `<span class="discount-badge">(${item.discount}% OFF)</span>` : ''}
                        </div>
 
                        <!-- Item Actions -->
                        <div class="item-actions">
                            <!-- Quantity Selector -->
                            <div class="quantity-selector">
                                <button class="qty-btn" onclick="updateQuantity(${item.productId}, ${item.quantity - 1})" 
                                    ${item.quantity <= 1 ? 'disabled' : ''}>
                                    <i class="fas fa-minus"></i>
                                </button>
                                <input type="text" class="qty-input" value="${item.quantity}" readonly>
                                <button class="qty-btn" onclick="updateQuantity(${item.productId}, ${item.quantity + 1})">
                                    <i class="fas fa-plus"></i>
                                </button>
                            </div>
 
                            <!-- Remove Button -->
                            <button class="remove-btn" onclick="removeFromCart(${item.productId})">
                                <i class="fas fa-trash-alt"></i> Remove
                            </button>
                        </div>
                    </div>
                </div>
            `).join("");
 
            // Update price summary
            updatePriceSummary(cart);
        })
        .catch(error => {
            console.error("Error loading cart:", error);
        });
}
 
// ========== UPDATE QUANTITY ==========
function updateQuantity(productId, newQuantity) {
    if (newQuantity < 1) return;
 
    fetch(`/api/cart/update/${productId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            quantity: newQuantity
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            loadCart();
            updateCartBadge();
        }
    })
    .catch(error => {
        console.error("Error updating quantity:", error);
    });
}
 
// ========== REMOVE FROM CART ==========
function removeFromCart(productId) {
    if (!confirm("Remove this item from your bag?")) {
        return;
    }
 
    fetch(`/api/cart/remove/${productId}`, {
        method: "DELETE"
    })
    .then(res => res.json())
    .then(() => {
        loadCart();
        updateCartBadge();
    })
    .catch(error => {
        console.error("Error removing item:", error);
    });
}
 
// ========== UPDATE PRICE SUMMARY ==========
function updatePriceSummary(cart) {
    let totalMRP = 0;
    let totalDiscount = 0;
 
    cart.forEach(item => {
        const itemMRP = parseFloat(item.basePrice);
        const itemPrice = parseFloat(item.price);
        const quantity = parseInt(item.quantity);
 
        totalMRP += itemMRP * quantity;
        totalDiscount += (itemMRP - itemPrice) * quantity;
    });
 
    // Delivery charges: FREE for orders >= ₹1999
    const deliveryCharges = totalMRP >= 1999 ? 0 : 99;
    const totalAmount = totalMRP - totalDiscount + deliveryCharges;
 
    // Update UI
    document.getElementById("totalMRP").textContent = `₹${totalMRP.toFixed(2)}`;
    document.getElementById("totalDiscount").textContent = `-₹${totalDiscount.toFixed(2)}`;
    
    const deliveryElement = document.getElementById("deliveryAmount");
    if (deliveryCharges === 0) {
        deliveryElement.textContent = "FREE";
        deliveryElement.parentElement.classList.add("free-text");
    } else {
        deliveryElement.textContent = `₹${deliveryCharges}`;
        deliveryElement.parentElement.classList.remove("free-text");
    }
    
    document.getElementById("totalAmount").textContent = `₹${totalAmount.toFixed(2)}`;
 
    // Enable/disable checkout button
    const checkoutBtn = document.querySelector(".checkout-btn");
    if (checkoutBtn) {
        checkoutBtn.disabled = cart.length === 0;
    }
}
 
// ========== UPDATE CART BADGE ==========
function updateCartBadge() {
    fetch("/api/cart")
        .then(res => res.json())
        .then(cart => {
            const badge = document.querySelector(".bag-count");
            
            if (!badge) return;
 
            // Calculate total items (sum of quantities)
            const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
            
            badge.textContent = totalItems;
            badge.style.display = totalItems > 0 ? "flex" : "none";
        })
        .catch(error => {
            console.error("Error updating cart badge:", error);
        });
}
 
// ========== UPDATE WISHLIST BADGE ==========
function updateWishlistBadge() {
    fetch("/api/wishlist")
        .then(res => res.json())
        .then(wishlist => {
            const badge = document.querySelector(".wishlist-count");
            
            if (!badge) return;
 
            badge.textContent = wishlist.length;
            badge.style.display = wishlist.length > 0 ? "flex" : "none";
        })
        .catch(error => {
            console.error("Error updating wishlist badge:", error);
        });
}
 
// ========== PROCEED TO CHECKOUT ==========
function proceedToCheckout() {
    window.location.href = "/checkout";
}
