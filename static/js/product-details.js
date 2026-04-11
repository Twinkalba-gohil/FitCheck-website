document.addEventListener("DOMContentLoaded", function () {

  // ===== IMAGE SWITCH =====
  const thumbnails = document.querySelectorAll(".thumb-img");
  const changeImg = document.getElementById("changeImg");

  thumbnails.forEach(function (thumb) {
    thumb.addEventListener("click", function () {
      changeImg.src = this.src;
    });
  });


  // ===== ADD TO BAG =====
  const addBagBtn = document.getElementById("addBagBtn");

  if (addBagBtn) {

    addBagBtn.addEventListener("click", function () {

      const productId = this.dataset.id;
      const hasSize = this.dataset.hasSize === "true";

      let size = null;

      if (hasSize) {
        const selectedSize = document.querySelector('input[name="size"]:checked');

        if (!selectedSize) {
          alert("Please select size");
          return;
        }

        size = selectedSize.value;
      }

      fetch("/api/cart/add", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          pro_id: productId,
          quantity: 1,
          size: size
        })
      })
        .then(res => res.json())
        .then(data => {

          if (data.success) {

            alert("Added to Bag");

            updateCartBadge();

          } else {

            alert(data.message || "Error adding to bag");

          }

        });

    });

  }


  // ===== WISHLIST =====
  const wishBtn = document.getElementById("wishBtn");

  if (wishBtn) {

    const productId = wishBtn.dataset.id;

    wishBtn.addEventListener("click", function () {

      if (wishBtn.classList.contains("active")) {

        fetch(`/api/wishlist/remove/${productId}`, {
          method: "DELETE"
        })
          .then(res => res.json())
          .then(data => {

            if (data.success) {

              wishBtn.classList.remove("active");
              wishBtn.innerHTML = '<i class="fa-regular fa-heart"></i> WISHLIST';

              updateWishlistBadge();

            }

          });

      } else {

        fetch("/api/wishlist/add", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            pro_id: productId
          })
        })
          .then(res => res.json())
          .then(data => {

            if (data.success) {

              wishBtn.classList.add("active");
              wishBtn.innerHTML = '<i class="fas fa-heart"></i> WISHLISTED';

              updateWishlistBadge();

            }

          });

      }

    });

  }


  // ===== READ MORE =====
  const readMore = document.getElementById("readMore");
  const descBox = document.getElementById("desc");

  if (readMore) {

    readMore.addEventListener("click", function () {

      descBox.classList.toggle("expanded");

      readMore.textContent = descBox.classList.contains("expanded")
        ? "Read Less"
        : "Read More";

    });

  }

});