// ========================================
// PRODUCTS.JS - Product listing page logic
// ========================================

document.addEventListener('DOMContentLoaded', function() {
  // Get URL parameters
  const urlParams = new URLSearchParams(window.location.search);
  const gender = urlParams.get('gender');
  const category = urlParams.get('category');
  const subcategory = urlParams.get('subcategory');
  
  // Get container
  const productContainer = document.getElementById('product-grid');
  const pageTitle = document.getElementById('page-title');
  
  if (!productContainer) {
    console.error('Product container not found');
    return;
  }
  
  // Filter products based on URL parameters
  let filteredProducts = window.products || [];
  if (gender) {
    filteredProducts = filteredProducts.filter(p => p.gender === gender);
  }
  
  if (category) {
    filteredProducts = filteredProducts.filter(p => p.category === category);
  }
  
  if (subcategory) {
    filteredProducts = filteredProducts.filter(p => p.subcategory === subcategory);
  }
  
  // Update page title
  if (pageTitle) {
    let titleText = 'All Products';
    
    if (gender && category && subcategory) {
      titleText = `${capitalize(gender)} ${capitalize(subcategory)}`;
    } else if (gender && category) {
      titleText = `${capitalize(gender)} ${capitalize(category)}`;
    } else if (gender) {
      titleText = `${capitalize(gender)} Collection`;
    }
    pageTitle.textContent = titleText;
  }
  
  // Render products
  if (filteredProducts.length === 0) {
    productContainer.innerHTML = '<p class="no-products">No products found for this category.</p>';
    return;
  }
  
  filteredProducts.forEach(product => {
    const card = createProductCard(product);
    productContainer.appendChild(card);
  });
});

// ========== CREATE PRODUCT CARD ==========
function createProductCard(product) {
  const card = document.createElement('div');
  card.className = 'product-card';
  card.setAttribute('data-id', product.id);
  
  card.innerHTML = `
    <div class="product-img">
      <img src="${product.images[0]}" alt="${product.name}">
    </div>
    <div class="product-info">
      <h3>${product.brand}</h3>
      <p class="product-name">${product.name}</p>
      <p class="price">₹${product.price} <span>₹${product.mrp}</span></p>
      <p class="discount">${product.discount}</p>
    </div>
  `;
  
  // Add click event to navigate to product details
  card.addEventListener('click', function() {
    window.location.href = `/product/${product.id}`;
  });
  
  return card;
}

// ========== HELPER FUNCTION ==========
function capitalize(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}