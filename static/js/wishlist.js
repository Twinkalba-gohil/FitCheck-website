document.addEventListener("DOMContentLoaded", function () {

  loadWishlist();
  updateCartBadge();
  updateWishlistBadge();

});


function loadWishlist() {

  fetch("/api/wishlist")
    .then(res => res.json())
    .then(wishlist => {

      const grid = document.getElementById("wishlistGrid");
      const empty = document.getElementById("emptyWishlist");

      if (!wishlist.length) {

        grid.style.display = "none";
        empty.style.display = "block";
        return;

      }

      grid.style.display = "grid";
      empty.style.display = "none";

      grid.innerHTML = wishlist.map(item => `

        <div class="wishlist-card">

          <button class="remove-btn" onclick="removeFromWishlist(${item.id})">
            <i class="fas fa-times"></i>
          </button>

          <div class="wishlist-image">
            <a href="/product/${item.id}">
              <img src="/static/uploads/products/${item.image}">
            </a>
          </div>

          <div class="wishlist-info">

            <h3 class="product-brand">${item.brand}</h3>

            <p class="product-name">
              <a href="/product/${item.id}">
                ${item.name}
              </a>
            </p>

            <div class="product-price">
              <span class="final-price">₹${item.price}</span>
              <span class="original-price">₹${item.basePrice}</span>
            </div>

            <div class="wishlist-actions">
              <button onclick="moveToCart(${item.id})" class="btn-add-to-bag">
                Move to Bag
              </button>
            </div>

          </div>

        </div>

      `).join("");

    });

}


function removeFromWishlist(id) {

  fetch(`/api/wishlist/remove/${id}`, {
    method: "DELETE"
  })
    .then(res => res.json())
    .then(() => {

      loadWishlist();
      updateWishlistBadge();

    });

}


function moveToCart(id) {

  fetch("/api/cart/add", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      pro_id: id,
      quantity: 1
    })
  })
    .then(res => res.json())
    .then(data => {

      if (data.success) {

        removeFromWishlist(id);

        alert("Moved to Bag");

        updateCartBadge();

      }

    });

}