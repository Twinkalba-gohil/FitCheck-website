import os
from models import db
from flask import Blueprint, current_app, flash, jsonify, make_response, request, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import joinedload
from utils.auth import login_required
from models.user import User
from models.product import Product, ProductImage
from models.category import Category, SubCategory
from models.location import City, State
from models.order import Order, OrderDetail
from models.payment import Payment
from models.cart import Cart
from models.wishlist import Wishlist
import random
import time
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv


 
user_bp = Blueprint("user", __name__)
 
@user_bp.route('/registration', methods=['GET', 'POST'])
def registration():
    states = State.query.all()
 
    if request.method == "POST":
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        contact = request.form.get('contact', '').strip()
        address = request.form.get('address', '').strip()
        state_id = int(request.form.get('state_id'))
        city_id = int(request.form.get('city_id'))
        area_name = request.form.get('area_name', '').strip()
        pincode = request.form.get('pincode', '').strip()
 
        if not all([username, email, password, contact, address, state_id, city_id, area_name, pincode]):
            return render_template("user/registration.html", states=states, error="All fields are required!")
 
        if User.query.filter_by(email=email).first():
            return render_template("user/registration.html", states=states, error="Email already registered. Please login.")
 
        if User.query.filter_by(contact=contact).first():
            return render_template("user/registration.html", states=states, error="Contact number already registered.")
 
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            contact=contact,
            address=address,
            state_id=state_id,
            city_id=city_id,
            area_name=area_name,
            pincode=pincode
        )
 
        db.session.add(new_user)
        db.session.commit()
 
        return redirect(url_for("user.login"))
 
    return render_template("user/registration.html", states=states)
 
 
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
 
        if not email or not password:
            return render_template("user/login.html", error="Please enter both email and password.")
 
        user = User.query.filter_by(email=email).first()
 
        if user and check_password_hash(user.password, password):
            session['u_id'] = user.u_id
            session['username'] = user.username
            session.permanent = True
            next_page = request.args.get("next")
            return redirect(next_page or url_for("index"))        
        else:
            return render_template("user/login.html", error="Invalid email or password.")
 
    return render_template("user/login.html")

def send_email_otp(to_email, otp):
    try:
        load_dotenv()

        sender_email = os.getenv("EMAIL_USER")
        sender_password = os.getenv("EMAIL_PASS")  

        msg = MIMEText(f"Your OTP is: {otp}")
        msg['Subject'] = "Password Reset OTP"
        msg['From'] = sender_email
        msg['To'] = to_email

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        print("Email sent successfully")

    except Exception as e:
        print("Email Error:", str(e))



@user_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")

        #Check only by email
        user = User.query.filter_by(email=email).first()

        if not user:
            return render_template("user/forgot_password.html", error="Email not found")

        # Generate OTP
        otp = random.randint(100000, 999999)

        # Store in session
        session['reset_otp'] = otp
        session['reset_user'] = user.u_id
        session['otp_time'] = time.time()

        # Send EMAIL only
        send_email_otp(user.email, otp)

        return redirect(url_for('user.verify_otp'))

    return render_template("user/forgot_password.html")

@user_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == "POST":
        entered_otp = request.form.get("otp")

        #Expiry check (5 minutes)
        if time.time() - session.get('otp_time', 0) > 300:
            return render_template("user/verify_otp.html", error="OTP expired")

        # Match OTP
        if str(session.get('reset_otp')) == entered_otp:

            user = User.query.get(session.get('reset_user'))

            # Login user
            session['u_id'] = user.u_id
            session['username'] = user.username
            session.permanent = True

            #Clear session
            session.pop('reset_otp', None)
            session.pop('reset_user', None)
            session.pop('otp_time', None)

            return redirect(url_for('index'))

        else:
            return render_template("user/verify_otp.html", error="Invalid OTP")

    return render_template("user/verify_otp.html")


@user_bp.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("index"))
 
 
@user_bp.route('/profile')
@login_required
def profile():
    user_id = session.get("u_id")
    user = User.query.options(
        joinedload(User.city),
        joinedload(User.state),
        joinedload(User.orders)
    ).get_or_404(user_id)

    states = State.query.all()
    cities = City.query.filter_by(state_id=user.state_id).all()

    recent_orders = Order.query.filter_by(u_id=user_id)\
        .order_by(Order.created_at.desc())\
        .limit(3).all()

    return render_template(
        "user/profile.html",
        user=user,
        states=states,
        cities=cities,
        recent_orders=recent_orders
    )
 
 
@user_bp.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    user_id = session.get("u_id")
    user = User.query.get_or_404(user_id)
    
    user.contact = request.form.get('contact')
    user.address = request.form.get('address')
    user.area_name = request.form.get('area_name')
    user.pincode = request.form.get('pincode')
    user.state_id = request.form.get('state_id')
    user.city_id = request.form.get('city_id')

    
    db.session.commit()
    flash('Profile updated successfully', 'success')
    return redirect(url_for('user.profile'))
 
 

@user_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    user_id = session.get("u_id")
    user = User.query.get_or_404(user_id)

    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    # 1. Check current password
    if not check_password_hash(user.password, current_password):
        flash('Current password is incorrect', 'error')
        return redirect(url_for('user.profile'))

    # 2. Check confirm password
    if new_password != confirm_password:
        flash('New passwords do not match', 'error')
        return redirect(url_for('user.profile'))

    # 3. Update password
    user.password = generate_password_hash(new_password)

    db.session.commit()

    flash('Password changed successfully', 'success')
    return redirect(url_for('user.profile'))
 
 
@user_bp.route('/about')
def about():
    return render_template("user/about.html") 
 
 
@user_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        try:
            sender_email = os.getenv("EMAIL_USER")
            sender_password = os.getenv("EMAIL_PASS")

            msg = MIMEText(f"""
Name: {name}
Email: {email}

Message:
{message}
            """)

            msg['Subject'] = subject if subject else "New Contact Message"
            msg['From'] = sender_email
            msg['To'] = sender_email   # you receive message

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()

            flash("Message sent successfully!", "success")

        except Exception as e:
            print("Email Error:", e)
            flash("Failed to send message", "error")

    return render_template("user/contact.html")
 
# ========== WISHLIST ROUTES ==========
@user_bp.route('/wishlist')
@login_required
def wishlist():
    return render_template("user/wishlist.html")
 
 
@user_bp.route("/api/wishlist/add", methods=["POST"])
@login_required
def add_to_wishlist():
    data = request.get_json()
    user_id = session.get("u_id")
    pro_id = data.get("pro_id")
 
    existing = Wishlist.query.filter_by(u_id=user_id, pro_id=pro_id).first()
 
    if existing:
        return jsonify({"success": False, "message": "Already in wishlist"})
 
    item = Wishlist(u_id=user_id, pro_id=pro_id)
    db.session.add(item)
    db.session.commit()
 
    return jsonify({"success": True})
 
 
@user_bp.route("/api/wishlist/remove/<int:pro_id>", methods=["DELETE"])
@login_required
def remove_from_wishlist(pro_id):
    user_id = session.get("u_id")
    item = Wishlist.query.filter_by(u_id=user_id, pro_id=pro_id).first()
 
    if item:
        db.session.delete(item)
        db.session.commit()
 
    return jsonify({"success": True})
 
 
@user_bp.route("/api/wishlist")
@login_required
def get_wishlist():
    user_id = session.get("u_id")
 
    items = db.session.query(Product, Wishlist).join(
        Wishlist, Wishlist.pro_id == Product.pro_id
    ).filter(Wishlist.u_id == user_id).all()
 
    wishlist = []
 
    for product, w in items:
        wishlist.append({
            "id": product.pro_id,
            "name": product.pro_name,
            "brand": product.brand,
            "price": float(product.final_price) if product.discount > 0 else float(product.base_price),
            "basePrice": float(product.base_price),
            "discount": product.discount,
            "image": product.image
        })
 
    return jsonify(wishlist)
 
 
@user_bp.route("/api/wishlist/clear", methods=["DELETE"])
@login_required
def clear_wishlist():
    user_id = session.get("u_id")
    Wishlist.query.filter_by(u_id=user_id).delete()
    db.session.commit()
    return jsonify({"success": True})
 
 
# ========== CART ROUTES ==========
@user_bp.route('/cart')
@login_required
def cart():
    return render_template("user/cart.html")
 
 
@user_bp.route("/api/cart/add", methods=["POST"])
@login_required
def add_to_cart():
    data = request.get_json()
    user_id = session.get("u_id")
    pro_id = data.get("pro_id")
    quantity = data.get("quantity", 1)
 
    cart_item = Cart.query.filter_by(u_id=user_id, pro_id=pro_id).first()
 
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(
            u_id=user_id,
            pro_id=pro_id,
            quantity=quantity
        )
        db.session.add(cart_item)
 
    db.session.commit()
 
    return jsonify({"success": True})
 
 
@user_bp.route("/api/cart")
@login_required
def get_cart():
    user_id = session.get("u_id")
 
    items = db.session.query(Product, Cart).join(
        Cart, Cart.pro_id == Product.pro_id
    ).filter(Cart.u_id == user_id).all()
 
    cart = []
 
    for product, c in items:
        cart.append({
            "productId": product.pro_id,
            "productName": product.pro_name,
            "brand": product.brand,
            "price": float(product.final_price) if product.discount > 0 else float(product.base_price),
            "basePrice": float(product.base_price),
            "discount": product.discount,
            "image": product.image,
            "quantity": c.quantity
        })
 
    return jsonify(cart)
 
 
@user_bp.route("/api/cart/remove/<int:pro_id>", methods=["DELETE"])
@login_required
def remove_from_cart(pro_id):
    user_id = session.get("u_id")
    item = Cart.query.filter_by(u_id=user_id, pro_id=pro_id).first()
 
    if item:
        db.session.delete(item)
        db.session.commit()
 
    return jsonify({"success": True})
 
 
@user_bp.route("/api/cart/update/<int:pro_id>", methods=["PUT"])
@login_required
def update_cart_quantity(pro_id):
    user_id = session.get("u_id")
    data = request.get_json()
    quantity = data.get("quantity", 1)
 
    cart_item = Cart.query.filter_by(u_id=user_id, pro_id=pro_id).first()
 
    if cart_item:
        cart_item.quantity = quantity
        db.session.commit()
        return jsonify({"success": True})
 
    return jsonify({"success": False, "message": "Item not found"})
 
 
@user_bp.route("/api/cart/clear", methods=["DELETE"])
@login_required
def clear_cart():
    user_id = session.get("u_id")
    Cart.query.filter_by(u_id=user_id).delete()
    db.session.commit()
    return jsonify({"success": True})
 
 
# ========== PRODUCT ROUTES ==========
@user_bp.route("/products")
def products():
    search = request.args.get("search")
    category = request.args.get("category")
    subcategory = request.args.get("subcategory")
 
    products_query = Product.query.join(SubCategory).join(Category)
 
    if search:
        products_query = products_query.filter(
            Product.pro_name.ilike(f"%{search}%") |
            Product.brand.ilike(f"%{search}%") |
            Category.cat_name.ilike(f"%{search}%") |
            SubCategory.subcat_name.ilike(f"%{search}%")
        )
 
    if category:
        products_query = products_query.filter(Category.cat_name.ilike(category))
 
    if subcategory:
        products_query = products_query.filter(SubCategory.subcat_name.ilike(subcategory))
 
    products = products_query.all()
 
    return render_template("user/category_products.html", products=products)
 
 
@user_bp.route('/get-cities/<state_id>')
def get_cities(state_id):
    cities = City.query.filter_by(state_id=state_id).all()
    city_list = []
    for city in cities:
        city_list.append({
            "city_id": city.city_id,
            "city_name": city.city_name
        })
    return jsonify(city_list)
 
 
@user_bp.route("/product/<int:pro_id>")
def product_details(pro_id):
    product = Product.query.options(
        joinedload(Product.subcategory),
        joinedload(Product.images)
    ).get_or_404(pro_id)
 
    similar_products = Product.query.filter(
        Product.subcat_id == product.subcat_id,
        Product.pro_id != product.pro_id
    ).limit(10).all()
    
    # Check if product is in wishlist (if user is logged in)
    in_wishlist = False
    has_purchased = False


    if session.get('u_id'):
        user_id = session.get('u_id')

        wishlist_item = Wishlist.query.filter_by(
            u_id=session.get('u_id'),
            pro_id=pro_id
        ).first()
        in_wishlist = wishlist_item is not None

        # Check if user has purchased this product
        has_purchased_order = db.session.query(Order).join(OrderDetail).filter(
            Order.u_id == user_id,
            OrderDetail.pro_id == pro_id,
            Order.status.in_(['delivered', 'confirmed', 'shipped', 'pending'])
        ).first()
        has_purchased = has_purchased_order is not None
 
    return render_template(
        "user/product_details.html",
        product=product,
        similar_products=similar_products,
        in_wishlist=in_wishlist,
        has_purchased=has_purchased

    )
 
 
@user_bp.route("/category/<int:cat_id>")
def category_products(cat_id):
    products = Product.query.join(SubCategory)\
        .filter(SubCategory.cat_id == cat_id).all()
 
    return render_template(
        "user/category_products.html",
        products=products
    )
 
 
# ========== CHECKOUT & ORDER ROUTES ==========
@user_bp.route("/checkout")
@login_required
def checkout():
    user_id = session.get("u_id")
    user = User.query.options(
        joinedload(User.city),
        joinedload(User.state)
    ).get_or_404(user_id)
    return render_template("user/checkout.html", user=user)
 
 
@user_bp.route("/api/place-order", methods=["POST"])
@login_required
def place_order():
    try:
        data = request.get_json()
        
        if not data or not data.get('items'):
            return jsonify({'success': False, 'message': 'Invalid order data'}), 400
        
        user_id = session.get('u_id')
        
        # Create Order
        new_order = Order(
            u_id=user_id,
            total_amount=data.get('total_amount'),
            discount=data.get('discount'),
            ship_amount=data.get('ship_amount'),
            net_amount=data.get('net_amount'),
            status='pending'
        )
        db.session.add(new_order)
        db.session.flush()
        
        # Create Order Details
        for item in data.get('items', []):
            order_detail = OrderDetail(
                order_id=new_order.order_id,
                pro_id=item.get('pro_id'),
                quantity=item.get('quantity'),
                price=item.get('price')
            )
            db.session.add(order_detail)
        
        # Create Payment Record
        payment = Payment(
            order_id=new_order.order_id,
            amount=data.get('net_amount'),
            method=data.get('payment_method', 'CASH'),
            status='pending' if data.get('payment_method') == 'CASH' else 'completed'
        )
        db.session.add(payment)
        
        # Clear user's cart after successful order
        Cart.query.filter_by(u_id=user_id).delete()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Order placed successfully',
            'order_id': new_order.order_id,
            'redirect_url': url_for('user.order_confirmation', order_id=new_order.order_id)

        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500
 
 
# ========== ORDER CONFIRMATION ==========
@user_bp.route("/order-confirmation/<int:order_id>")
@login_required
def order_confirmation(order_id):
    """Show order confirmation page after successful order"""
    order = Order.query.options(
        joinedload(Order.user).joinedload(User.city),
        joinedload(Order.user).joinedload(User.state),
        joinedload(Order.order_details).joinedload(OrderDetail.product),
        joinedload(Order.payment)
    ).filter_by(
        order_id=order_id,
        u_id=session.get("u_id")
    ).first_or_404()
    
    return render_template("user/order_confirmation.html", order=order)
 
 
# ========== MY ORDERS ==========
@user_bp.route("/my-orders")
@login_required
def my_orders():
    """Display all orders for logged-in user"""
    user_id = session.get("u_id")
    
    # Get all orders with related data
    orders = Order.query.options(
        joinedload(Order.order_details).joinedload(OrderDetail.product),
        joinedload(Order.payment)
    ).filter_by(u_id=user_id).order_by(Order.order_id.desc()).all()
    
    return render_template("user/my_orders.html", orders=orders)
 
 
# ========== ORDER DETAILS (Track Order) ==========
@user_bp.route("/order/<int:order_id>")
@login_required
def order_details(order_id):
    """View detailed order information"""
    order = Order.query.options(
        joinedload(Order.user).joinedload(User.city),
        joinedload(Order.user).joinedload(User.state),
        joinedload(Order.order_details).joinedload(OrderDetail.product),
        joinedload(Order.payment)
    ).filter_by(
        order_id=order_id,
        u_id=session.get("u_id")
    ).first_or_404()
    
    return render_template("user/order_details.html", order=order)
 
 
# ========== CANCEL ORDER ==========
@user_bp.route("/api/order/<int:order_id>/cancel", methods=["POST"])
@login_required
def cancel_order(order_id):
    """Cancel an order (only if pending)"""
    try:
        order = Order.query.filter_by(
            order_id=order_id,
            u_id=session.get("u_id")
        ).first_or_404()
        
        # Only allow cancellation if order is pending
        if order.status != 'pending':
            return jsonify({
                'success': False,
                'message': 'Order cannot be cancelled at this stage'
            }), 400
        
        order.status = 'cancelled'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Order cancelled successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
 
 
# ========== INVOICE GENERATION ==========
@user_bp.route("/invoice/<int:order_id>")
@login_required
def view_invoice(order_id):
    """View invoice in browser"""
    
    # Get order with all details
    order = Order.query.options(
        joinedload(Order.user).joinedload(User.city),
        joinedload(Order.user).joinedload(User.state),
        joinedload(Order.order_details).joinedload(OrderDetail.product),
        joinedload(Order.payment)
    ).filter_by(
        order_id=order_id,
        u_id=session.get("u_id")
    ).first_or_404()
    
    # Render invoice template
    return render_template('user/invoice.html', order=order, download=False)
 
 
@user_bp.route("/invoice/<int:order_id>/download")
@login_required
def download_invoice(order_id):
    """Generate and download PDF invoice using xhtml2pdf"""
    from xhtml2pdf import pisa
    from io import BytesIO
    
    # Get order with all details
    order = Order.query.options(
        joinedload(Order.user).joinedload(User.city),
        joinedload(Order.user).joinedload(User.state),
        joinedload(Order.order_details).joinedload(OrderDetail.product),
        joinedload(Order.payment)
    ).filter_by(
        order_id=order_id,
        u_id=session.get("u_id")
    ).first_or_404()
    
    # Render HTML template
    html_content = render_template('user/invoice.html', order=order, download=True)
    
    # Create PDF
    pdf_buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)
    
    # Check for errors
    if pisa_status.err:
        return "Error generating PDF", 500
    
    # Get PDF data
    pdf_data = pdf_buffer.getvalue()
    pdf_buffer.close()
    
    # Create invoices directory if it doesn't exist
    invoices_dir = os.path.join(current_app.root_path, 'static', 'invoices')
    os.makedirs(invoices_dir, exist_ok=True)
    
    # Save PDF to file
    filename = f"invoice_{order.order_id}_{order.user.u_id}.pdf"
    filepath = os.path.join(invoices_dir, filename)
    
    with open(filepath, 'wb') as f:
        f.write(pdf_data)
    
    # Return PDF as download
    response = make_response(pdf_data)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=FitCheck_Invoice_{order.order_id}.pdf'
    
    return response


    # ========================================
# USER FEEDBACK/REVIEW ROUTES
# Add to user_routes.py
# ========================================
 
# Add import at top
from models.feedback import Feedback
 
# ========================================
# MY REVIEWS PAGE
# ========================================
@user_bp.route('/my-reviews')
@login_required
def my_reviews():
    """Display all reviews submitted by the logged-in user"""
    user_id = session.get("u_id")
    
    reviews = Feedback.query.options(
        joinedload(Feedback.product)
    ).filter_by(u_id=user_id).order_by(Feedback.f_id.desc()).all()
    
    return render_template("user/my_reviews.html", reviews=reviews)
 
 
# ========================================
# WRITE REVIEW PAGE (For specific product)
# ========================================
@user_bp.route('/write-review/<int:pro_id>')
@login_required
def write_review(pro_id):
    """Page to write a review for a specific product"""
    user_id = session.get("u_id")
    
    # Check if user has purchased this product
    has_purchased = db.session.query(Order).join(OrderDetail).filter(
        Order.u_id == user_id,
        OrderDetail.pro_id == pro_id,
        Order.status.in_(['delivered', 'confirmed', 'shipped'])
    ).first()
    
    # Check if user already reviewed this product
    existing_review = Feedback.query.filter_by(
        u_id=user_id,
        pro_id=pro_id
    ).first()
    
    # Get product details
    product = Product.query.get_or_404(pro_id)
    
    return render_template("user/write_review.html",
                         product=product,
                         has_purchased=has_purchased,
                         existing_review=existing_review)
 
 
# ========================================
# SUBMIT REVIEW (POST)
# ========================================
@user_bp.route('/api/submit-review', methods=['POST'])
@login_required
def submit_review():
    """Submit a product review"""
    try:
        data = request.get_json()
        user_id = session.get("u_id")
        
        pro_id = data.get('pro_id')
        rating = data.get('rating')
        comment = data.get('comment', '').strip()
        
        # Validation
        if not pro_id or not rating:
            return jsonify({'success': False, 'message': 'Product and rating are required'}), 400
        
        if not comment:
            return jsonify({'success': False, 'message': 'Please write a review comment'}), 400
        
        if rating < 1 or rating > 5:
            return jsonify({'success': False, 'message': 'Rating must be between 1 and 5'}), 400
        
        # Check if already reviewed
        existing = Feedback.query.filter_by(u_id=user_id, pro_id=pro_id).first()
        if existing:
            return jsonify({'success': False, 'message': 'You have already reviewed this product'}), 400
        
        # Create review
        review = Feedback(
            u_id=user_id,
            pro_id=pro_id,
            rating=rating,
            comment=comment
        )
        
        db.session.add(review)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Review submitted successfully!',
            'review_id': review.f_id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
 
 
# ========================================
# UPDATE REVIEW (POST)
# ========================================
@user_bp.route('/api/update-review/<int:f_id>', methods=['POST'])
@login_required
def update_review(f_id):
    """Update an existing review"""
    try:
        data = request.get_json()
        user_id = session.get("u_id")
        
        review = Feedback.query.filter_by(f_id=f_id, u_id=user_id).first_or_404()
        
        rating = data.get('rating')
        comment = data.get('comment', '').strip()
        
        if rating:
            review.rating = rating
        if comment:
            review.comment = comment
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Review updated successfully!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
 
 
# ========================================
# DELETE REVIEW (DELETE)
# ========================================
@user_bp.route('/api/delete-review/<int:f_id>', methods=['DELETE'])
@login_required
def delete_review(f_id):
    """Delete a review"""
    try:
        user_id = session.get("u_id")
        
        review = Feedback.query.filter_by(f_id=f_id, u_id=user_id).first_or_404()
        
        db.session.delete(review)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Review deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
 
 
# ========================================
# GET PRODUCT REVIEWS (For product details page)
# ========================================
@user_bp.route('/api/product-reviews/<int:pro_id>')
def get_product_reviews(pro_id):
    """Get all reviews for a specific product (public)"""
    
    reviews = Feedback.query.options(
        joinedload(Feedback.user)
    ).filter_by(pro_id=pro_id).order_by(Feedback.f_id.desc()).all()
    
    reviews_data = []
    for review in reviews:
        reviews_data.append({
            'f_id': review.f_id,
            'rating': review.rating,
            'comment': review.comment,
            'user_name': review.user.username if review.user else 'Anonymous',
            'user_id': review.u_id
        })
    
    # Calculate average rating
    avg_rating = db.session.query(db.func.avg(Feedback.rating)).filter_by(pro_id=pro_id).scalar() or 0
    total_reviews = len(reviews)
    
    return jsonify({
        'reviews': reviews_data,
        'avg_rating': round(avg_rating, 1),
        'total_reviews': total_reviews
    })

