# 🔥 FitCheck – Features

---

## 👤 User Features

### 🔐 User Authentication
- Secure registration & login system  
- Password hashing using Werkzeug  

### 📧 OTP-Based Password Reset
- Email OTP verification  
- Secure session-based validation


- ### 🛍️ Product Browsing
- View all products with categories & subcategories  
- Search by product name, brand, or category

![home](screenshots/home.png)

![home-products](screenshots/home-products.png)

![category](screenshots/category.png)


### 👤 User Profile Management
- Update personal details (address, city, state, etc.)  
- Change password functionality
  
![profile](screenshots/profile.jpg)


### ❤️ Wishlist System
- Add/remove products to wishlist  
- View all saved items

![wishlist](screenshots/wishlist.jpg)


### 🛒 Shopping Cart
- Add, update, remove items  
- Dynamic quantity handling

![cart](screenshots/cart.png)


### 💳 Checkout System
- Place orders with shipping & pricing calculation

![checkout](screenshots/checkout-1.png)

![checkout](screenshots/checkout-2.png)

![checkout](screenshots/checkout-3.png)


### 📦 Order Management
- View order history  
- Track order status (pending, shipped, delivered, cancelled)  
- Cancel orders (if pending)

![my-order](screenshots/order-history.png)


### 🧾 Invoice Generation
- View invoice in browser  
- Download invoice as PDF

![invoice](screenshots/invoice.png)


### ⭐ Product Reviews & Ratings
- Write, edit, delete reviews  
- Only verified buyers can review  
- View all reviews with ratings  

![feedback-1](screenshots/feedback-1.png)

![feedback-2](screenshots/feedback-2.png)

![feedback-3](screenshots/feedback-3.png)


### 📩 Contact System
- Send messages via contact form (email integration)

![contact](screenshots/contact.png)


---

## 🛠️ Admin Features

### 🔐 Admin Authentication
- Secure admin login system  

### 📊 Dashboard Analytics
- View total users, products, orders  
- Revenue calculation  
- Date-based filtering (1, 7, 30, 90 days, all-time)  

![dashboard](screenshots/dashboard.png)

### 📦 Product Management
- Add new products  
- Edit product details  
- Upload multiple images  
- Replace/delete images  
- Delete products

![product](screenshots/product.png)

![add](screenshots/add.png)

![edit](screenshots/edit.png)


### 🗂️ Category & Subcategory Management
- Add, edit, delete categories  
- Add, edit, delete subcategories

![cat-2](screenshots/cat-2.png)

![cat-1](screenshots/cat-1.png)

![sub-1](screenshots/sub-1.png)

![sub-2](screenshots/sub-2.png)


### 👥 Customer Management
- View all registered users  

### 📦 Order Management
- View all orders  
- Update order status (pending → delivered)  
- Update payment status

![order](screenshots/order.png)


### 💳 Payment Handling
- Track payment status (pending, completed, failed)  

### ⭐ Review Management
- View all product reviews  
- Filter by rating  
- Delete inappropriate reviews

![feedback-1](screenshots/feedback-1.png)

![feedback-2](screenshots/feedback-2.png)

![feedback-3](screenshots/feedback-3.png)


---

## ⚙️ System Features

### ⚡ Full-Stack Architecture
- Backend: Flask (Python)  
- Database: SQLAlchemy ORM  

### 🗄️ Database Models
- User, Product, Category, Sub-category, Order, order-detail,  Payment, Cart, Wishlist, Feedback, state, city  

### 📂 Image Upload System
- Secure file handling using `secure_filename`  

### 🔄 AJAX-Based APIs
- Cart, Wishlist, Orders, Reviews (dynamic updates)  

### 🔐 Session Management
- Secure login sessions  

### 📱 Responsive UI
- Works across devices  

### 🧩 Modular Code Structure
- Blueprints (admin & user separation)  

---

## 🚀 Advanced Features (Interview Highlights 💯)

- OTP Email System using SMTP  
- Dynamic dashboard analytics with date filters  
- Multi-image product management (replace + delete + add)  
- PDF invoice generation using `xhtml2pdf`  
- Role-based authentication (Admin/User)  
- Review system with purchase validation  

---
