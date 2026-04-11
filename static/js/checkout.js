// ========================================
// CHECKOUT.JS - FitCheck Dynamic Checkout
// Works with Database Cart (not localStorage)
// ========================================
 
// Global variables
let currentStep = 1;
let selectedPaymentMethod = null;
let cartItems = [];
let orderData = {};
 
// ========== INITIALIZATION ==========
document.addEventListener('DOMContentLoaded', function() {
    loadCartData();
});
 
// ========== LOAD CART DATA FROM DATABASE ==========
function loadCartData() {
    // Fetch cart from database API
    fetch('/api/cart')
        .then(response => response.json())
        .then(cart => {
            cartItems = cart;
            
            if (cartItems.length === 0) {
                alert('Your cart is empty. Please add items to proceed.');
                window.location.href = '/cart';
                return;
            }
            
            displayOrderItems();
            updatePriceSummary();
        })
        .catch(error => {
            console.error('Error loading cart:', error);
            alert('Failed to load cart. Please try again.');
        });
}
 
// ========== DISPLAY ORDER ITEMS IN STEP 2 ==========
function displayOrderItems() {
    const container = document.getElementById('orderItemsList');
    const itemCount = document.getElementById('orderItemCount');
    
    if (!container) return;
    
    itemCount.textContent = cartItems.length;
    
    container.innerHTML = cartItems.map(item => `
        <div class="order-item">
            <div class="order-item-image">
                <img src="/static/uploads/products/${item.image}" alt="${item.productName}">
            </div>
            <div class="order-item-details">
                <div class="order-item-brand">${item.brand || 'Brand'}</div>
                <div class="order-item-name">${item.productName}</div>
                <div class="order-item-info">
                    <span>Qty: ${item.quantity}</span>
                </div>
                <div class="order-item-price">
                    <span class="final-price">₹${parseFloat(item.price).toFixed(2)}</span>
                    ${item.basePrice && item.basePrice > item.price ? 
                        `<span class="mrp">₹${parseFloat(item.basePrice).toFixed(2)}</span>` : ''}
                    ${item.discount && item.discount > 0 ? 
                        `<span class="discount">(${item.discount}% OFF)</span>` : ''}
                </div>
            </div>
        </div>
    `).join('');
}
 
// ========== UPDATE PRICE SUMMARY ==========
function updatePriceSummary() {
    let totalMRP = 0;
    let totalDiscount = 0;
    
    cartItems.forEach(item => {
        const itemMRP = parseFloat(item.basePrice || item.price);
        const itemPrice = parseFloat(item.price);
        const quantity = parseInt(item.quantity) || 1;
        
        totalMRP += itemMRP * quantity;
        totalDiscount += (itemMRP - itemPrice) * quantity;
    });
    
    // Delivery charges logic: FREE for orders >= ₹1999
    const deliveryCharges = totalMRP >= 1999 ? 0 : 99;
    const totalAmount = totalMRP - totalDiscount + deliveryCharges;
    const totalSavings = totalDiscount;
    
    // Update summary display
    document.getElementById('summaryMRP').textContent = `₹${totalMRP.toFixed(2)}`;
    document.getElementById('summaryDiscount').textContent = `-₹${totalDiscount.toFixed(2)}`;
    document.getElementById('summaryDelivery').textContent = deliveryCharges === 0 ? 'FREE' : `₹${deliveryCharges}`;
    document.getElementById('summaryTotal').textContent = `₹${totalAmount.toFixed(2)}`;
    
    // Show savings badge if there's a discount
    if (totalSavings > 0) {
        document.getElementById('totalSavings').textContent = totalSavings.toFixed(2);
        document.getElementById('savingsBadge').style.display = 'flex';
    }
    
    // Store in orderData for later use
    orderData = {
        totalMRP: totalMRP.toFixed(2),
        discount: totalDiscount.toFixed(2),
        deliveryCharges: deliveryCharges,
        totalAmount: totalAmount.toFixed(2)
    };
}
 
// ========== NAVIGATE BETWEEN STEPS ==========
function goToStep(stepNumber) {
    // Hide all steps
    document.querySelectorAll('.checkout-step-content').forEach(step => {
        step.style.display = 'none';
    });
    
    // Show selected step
    document.getElementById(`step${stepNumber}`).style.display = 'block';
    
    // Update step indicator
    document.querySelectorAll('.step').forEach((step, index) => {
        const num = index + 1;
        if (num < stepNumber) {
            step.classList.add('completed');
            step.classList.remove('active');
        } else if (num === stepNumber) {
            step.classList.add('active');
            step.classList.remove('completed');
        } else {
            step.classList.remove('active', 'completed');
        }
    });
    
    currentStep = stepNumber;
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
 
// ========== SELECT PAYMENT METHOD ==========
function selectPaymentMethod(method) {
    selectedPaymentMethod = method;
    
    // Update UI - remove all selected classes
    document.querySelectorAll('.payment-option').forEach(option => {
        option.classList.remove('selected');
    });
    
    // Add selected class to clicked option
    event.currentTarget.classList.add('selected');
    
    // Check the radio button
    document.querySelector(`input[value="${method}"]`).checked = true;
    
    // Enable place order button
    document.getElementById('placeOrderBtn').disabled = false;
}
 
// ========== PLACE ORDER (SEND TO BACKEND) ==========
function placeOrder() {
    if (!selectedPaymentMethod) {
        alert('Please select a payment method');
        return;
    }
    
    // Get user data from hidden inputs
    const userId = document.getElementById('userId').value;
    
    if (!userId) {
        alert('User not logged in. Please login to place order.');
        window.location.href = '/login';
        return;
    }
    
    // Prepare order items for backend
    const orderItems = cartItems.map(item => ({
        pro_id: parseInt(item.productId),
        quantity: parseInt(item.quantity),
        price: parseFloat(item.price)
    }));
    
    // Prepare complete order data
    const completeOrderData = {
        user_id: parseInt(userId),
        payment_method: selectedPaymentMethod,
        total_amount: parseFloat(orderData.totalMRP),
        discount: parseFloat(orderData.discount),
        ship_amount: parseFloat(orderData.deliveryCharges),
        net_amount: parseFloat(orderData.totalAmount),
        items: orderItems
    };
    
    console.log('Placing order:', completeOrderData);
    
    // Disable button and show loading
    const placeOrderBtn = document.getElementById('placeOrderBtn');
    placeOrderBtn.disabled = true;
    placeOrderBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    
    // Send order to backend
    fetch('/api/place-order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(completeOrderData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Cart is already cleared by backend
            
            // Update cart badge
            updateCartBadge();
            
            // Show success message
            alert(`Order placed successfully!\nOrder ID: ${data.order_id}\nTotal Amount: ₹${orderData.totalAmount}`);
            
            // Redirect to order confirmation or home
            window.location.href = data.redirect_url || '/';
        } else {
            // Show error
            alert('Error placing order: ' + (data.message || 'Unknown error'));
            
            // Reset button
            placeOrderBtn.disabled = false;
            placeOrderBtn.innerHTML = '<i class="fas fa-lock"></i> PLACE ORDER';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to place order. Please try again.');
        
        // Reset button
        placeOrderBtn.disabled = false;
        placeOrderBtn.innerHTML = '<i class="fas fa-lock"></i> PLACE ORDER';
    });
}
 
// ========== UPDATE CART BADGE ==========
function updateCartBadge() {
    fetch('/api/cart')
        .then(response => response.json())
        .then(cart => {
            const badge = document.querySelector('.bag-count');
            if (badge) {
                const total = cart.reduce((sum, item) => sum + item.quantity, 0);
                badge.textContent = total;
                badge.style.display = total > 0 ? 'flex' : 'none';
            }
        })
        .catch(error => console.error('Error updating cart badge:', error));
}
 
// ========== PROCEED TO CHECKOUT (from cart page) ==========
function proceedToCheckout() {
    window.location.href = '/checkout';
}
