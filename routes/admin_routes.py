import os
from flask import Blueprint, jsonify, make_response, render_template, request, redirect, session, current_app, url_for
from models import db
from models.user import User
from models.product import Product, ProductImage
from models.order import Order, OrderDetail
from models.category import SubCategory, Category
from models.feedback import Feedback
from utils.auth import admin_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
import time
# from werkzeug.security import generate_password_hash

# print(generate_password_hash("Admin@2112"))

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# ================= ADMIN LOGIN =================
@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        admin = User.query.filter_by(
            email=request.form["email"],
            role="Admin"
        ).first()

        if not admin or not check_password_hash(admin.password, request.form["password"]):
            return render_template("admin/login.html", error="Invalid admin login")

        session.clear()  
        session.permanent = True

        session["admin_id"] = admin.u_id
        session["role"] = "Admin"

        return redirect(url_for("admin.dashboard"))

    return render_template("admin/login.html")


#context processor
@admin_bp.app_context_processor
def inject_counts():
    return {
        "products_count": Product.query.count(),
        "orders_count": Order.query.count(),
        "users_count": User.query.filter_by(role="User").count()
    }


# ================= ADMIN DASHBOARD =================
@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    from datetime import datetime, timedelta
    
    # Get filter parameter (default: last 7 days)
    date_filter = request.args.get('filter', '7days')
    
    # Calculate date range
    today = datetime.now()
    if date_filter == '1days':
        start_date = today - timedelta(days=1)
        filter_label = "Last 1 Days"
    elif date_filter == '7days':
        start_date = today - timedelta(days=7)
        filter_label = "Last 7 Days"
    elif date_filter == '30days':
        start_date = today - timedelta(days=30)
        filter_label = "Last 30 Days"
    elif date_filter == '90days':
        start_date = today - timedelta(days=90)
        filter_label = "Last 90 Days"
    elif date_filter == 'all':
        start_date = datetime(2000, 1, 1)  # Far past date
        filter_label = "All Time"
    else:
        start_date = today - timedelta(days=7)
        filter_label = "Last 7 Days"
    
    # Get counts (all time)
    users_count = User.query.filter(User.role == "User", User.created_at >= start_date
    ).count()
    products_count = Product.query.filter(
        Product.created_at >= start_date
    ).count()
    
    # Get orders filtered by date
    orders_count = Order.query.filter(
        Order.created_at >= start_date
    ).count()
    
    # Get recent orders filtered by date
    recent_orders = Order.query\
        .options(
            joinedload(Order.user),
            joinedload(Order.order_details).joinedload(OrderDetail.product)
        )\
        .filter(Order.created_at >= start_date)\
        .order_by(Order.order_id.desc())\
        .limit(5)\
        .all()
    
    # Calculate total revenue for the period
    from sqlalchemy import func
    total_revenue = db.session.query(
        func.sum(Order.net_amount)
    ).filter(
        Order.created_at >= start_date
    ).scalar() or 0
    
    return render_template(
        "admin/dashboard.html",
        users=users_count,
        orders=orders_count,
        products_count=products_count,
        recent_orders=recent_orders,
        date_filter=date_filter,
        filter_label=filter_label,
        total_revenue=total_revenue
    )

#GET products
# ================= PRODUCTS LIST =================
@admin_bp.route("/products", methods=["GET"])
@admin_required
def products():
    products = Product.query.options(joinedload(Product.subcategory)).all()
    products_count = Product.query.count()
    subcategories = SubCategory.query.all()

    search = request.args.get("search", "")

    query = Product.query.options(joinedload(Product.subcategory))

    # SEARCH FILTER
    if search:
        query = query.filter(
            or_(
                Product.pro_name.ilike(f"%{search}%"),
                Product.brand.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%")
            )
        )


    return render_template(
        "admin/products.html",
        products=query.all(),
        products_count=products_count,
        subcategories=subcategories,
        search=search

    )


# ================= ADD PRODUCT =================
@admin_bp.route("/add-product", methods=["GET", "POST"])
@admin_required
def add_product():
    
    if request.method == "POST":
        subcat_id = int(request.form.get("subcat_id"))
        name = request.form.get("name")
        description = request.form.get("description")
        sizes = request.form.getlist("size")
        size_string = ",".join(sizes)
        price = float(request.form.get("price"))
        brand = request.form.get("brand")
        image = request.files.get("image")
        discount = request.form.get("discount")


        if not image:
            return render_template("admin/add_product.html", error="Image required")


        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True)

        filename = secure_filename(image.filename)
        image_path = os.path.join(upload_folder, filename)
        image.save(image_path)

        # CREATE PRODUCT
        product = Product(
            subcat_id=subcat_id,
            pro_name=name,
            description=description,
            size=size_string,
            base_price=price,
            brand=brand,
            image=filename,
            discount=discount,

        )

        db.session.add(product)
        db.session.commit()

        # OTHER IMAGES
        images = request.files.getlist("images")

        for img in images:
            if img.filename:

                other_filename = secure_filename(img.filename)
                img.save(os.path.join(upload_folder, other_filename))

                product_image = ProductImage(
                    pro_id=product.pro_id,
                    image=other_filename
                )

                db.session.add(product_image)

        db.session.commit()

        return redirect(url_for("admin.products"))

    return render_template(
        "admin/add_product.html",
        Categories=Category.query.all(),
        subcategories=SubCategory.query.all()
    )


# ============================================
# EDIT PRODUCT ROUTE (COMPLETE VERSION)
# ============================================
 
@admin_bp.route("/product/edit/<int:pro_id>", methods=["GET", "POST"])
@admin_required
def edit_product(pro_id):
    """
    Edit product with complete image management:
    - Replace main image
    - Replace other images
    - Add more images
    - Delete existing images
    """
    
    product = Product.query.get_or_404(pro_id)
    subcategories = SubCategory.query.all()
 
    if request.method == "POST":
        try:
            # ============================================
            # UPDATE BASIC PRODUCT INFORMATION
            # ============================================
            product.pro_name = request.form["name"]
            product.description = request.form["description"]
            product.size = request.form["size"]
            product.base_price = float(request.form["price"])
            product.discount = int(request.form["discount"])
            product.brand = request.form["brand"]
            product.subcat_id = request.form["subcat_id"]
 
            # ============================================
            # HANDLE MAIN IMAGE REPLACEMENT
            # ============================================
            main_image = request.files.get("main_image")
            if main_image and main_image.filename != "":
                # Delete old main image file
                if product.image:
                    old_image_path = os.path.join("static/uploads/products", product.image)
                    if os.path.exists(old_image_path):
                        try:
                            os.remove(old_image_path)
                        except Exception as e:
                            print(f"Error deleting old main image: {e}")
                
                # Save new main image with timestamp
                filename = secure_filename(main_image.filename)
                filename = f"{int(time.time())}_{filename}"
                main_image.save(os.path.join("static/uploads/products", filename))
                product.image = filename
 

            # ============================================
# HANDLE REPLACING EXISTING ADDITIONAL IMAGES
# ============================================

            for key, file in request.files.items():

                if key.startswith("replace_image_") and file.filename != "":

                    try:
                        img_id = int(key.split("_")[-1])

                        existing_image = ProductImage.query.get(img_id)

                        if existing_image:

                # delete old file
                            old_path = os.path.join("static/uploads/products", existing_image.image)

                            if os.path.exists(old_path):
                                os.remove(old_path)

                # save new image
                            filename = secure_filename(file.filename)
                            filename = f"{int(time.time())}_{filename}"

                            save_path = os.path.join("static/uploads/products", filename)
                            file.save(save_path)

                # update database
                            existing_image.image = filename

                    except Exception as e:
                        print("Replace image error:", e)
 
            # ============================================
            # HANDLE NEW ADDITIONAL IMAGES
            # ============================================
            extra_images = request.files.getlist("extra_images")
            for img in extra_images:
                if img and img.filename != "":
                    # Save new image with timestamp
                    filename = secure_filename(img.filename)
                    filename = f"{int(time.time())}_{filename}"
                    img.save(os.path.join("static/uploads/products", filename))
 
                    # Create new ProductImage record
                    new_img = ProductImage(
                        pro_id=product.pro_id,
                        image=filename
                    )
                    db.session.add(new_img)
 
            # Commit all changes
            db.session.commit()
            
            # flash("Product updated successfully!", "success")
            return redirect(url_for("admin.products"))
 
        except Exception as e:
            db.session.rollback()
            # flash(f"Error updating product: {str(e)}", "error")
            # print(f"Error updating product: {e}")
            return redirect(url_for("admin.edit_product", pro_id=pro_id))
 
    # GET request - load product with images
    return render_template(
        "admin/edit_product.html",
        product=product,
        subcategories=subcategories
    )
 
 
# ============================================
# DELETE PRODUCT IMAGE ROUTE (AJAX)
# ============================================
 
@admin_bp.route("/product/image/delete/<int:img_id>", methods=["POST"])
@admin_required
def delete_product_image(img_id):
    """
    Delete a product image via AJAX
    Called when user clicks the red X button
    """
    try:
        # Get the product image
        product_image = ProductImage.query.get_or_404(img_id)
        
        # Delete the image file from filesystem
        image_path = os.path.join("static/uploads/products", product_image.image)
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
            except Exception as e:
                print(f"Error deleting file: {e}")
        
        # Delete from database
        db.session.delete(product_image)
        db.session.commit()
        
        return jsonify({
            "success": True, 
            "message": "Image deleted successfully"
        })
    
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting image: {e}")
        return jsonify({
            "success": False, 
            "message": "Failed to delete image"
        }), 500


#delete product
@admin_bp.route("/product/delete/<int:pro_id>", methods=["POST"])
@admin_required
def delete_product(pro_id):
    product = Product.query.get_or_404(pro_id)

    # delete all images from product_image_table
    ProductImage.query.filter_by(pro_id=pro_id).delete()

    # delete product
    db.session.delete(product)

    db.session.commit()

    return redirect(url_for("admin.products"))

#================= ADMIN CATEGORIES =================
@admin_bp.route('/category', methods=['GET', 'POST'])
@admin_required
def category():

    if request.method == 'POST':

        # ADD CATEGORY
        if 'cat_name' in request.form:

            cat_name = request.form['cat_name']

            new_category = Category(cat_name=cat_name)
            db.session.add(new_category)
            db.session.commit()

        # ADD SUBCATEGORY
        elif 'subcat_name' in request.form:

            subcat_name = request.form['subcat_name']
            cat_id = request.form['cat_id']

            new_subcat = SubCategory(
                subcat_name=subcat_name,
                cat_id=cat_id
            )

            db.session.add(new_subcat)
            db.session.commit()

        return redirect(url_for('admin.category'))

    categories = Category.query.all()
    subcategories = SubCategory.query.all()

    for subcat in subcategories:
        subcat.products_count = len(subcat.products)

    for cat in categories:
        cat.products_count = sum(len(sub.products) for sub in subcategories if sub.cat_id == cat.cat_id)

    return render_template(
        'admin/category.html',
        categories=categories,
        subcategories=subcategories)



#================= EDIT CATEGORY =================
@admin_bp.route('/category/edit/<int:cat_id>', methods=['POST'])
@admin_required
def edit_category(cat_id):
    try:
        data = request.get_json()
        category = Category.query.get_or_404(cat_id)
        
        category.cat_name = data.get('cat_name')
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Category updated successfully'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


#================= DELETE CATEGORY =================
@admin_bp.route('/category/delete/<int:cat_id>', methods=['POST'])
@admin_required
def delete_category(cat_id):
    try:
        category = Category.query.get_or_404(cat_id)
        
        # Check if category has subcategories
        subcat_count = SubCategory.query.filter_by(cat_id=cat_id).count()
        if subcat_count > 0:
            return jsonify({
                'success': False,
                'message': f'Cannot delete category with {subcat_count} subcategories. Delete subcategories first.'
            }), 400
        
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Category deleted successfully'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


#================= EDIT SUBCATEGORY =================
@admin_bp.route('/subcategory/edit/<int:subcat_id>', methods=['POST'])
@admin_required
def edit_subcategory(subcat_id):
    try:
        data = request.get_json()
        subcategory = SubCategory.query.get_or_404(subcat_id)
        
        subcategory.subcat_name = data.get('subcat_name')
        subcategory.cat_id = data.get('cat_id')
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Subcategory updated successfully'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


#================= DELETE SUBCATEGORY =================
@admin_bp.route('/subcategory/delete/<int:subcat_id>', methods=['POST'])
@admin_required
def delete_subcategory(subcat_id):
    try:
        subcategory = SubCategory.query.get_or_404(subcat_id)
        
        # Check if subcategory has products
        product_count = Product.query.filter_by(subcat_id=subcat_id).count()
        if product_count > 0:
            return jsonify({
                'success': False,
                'message': f'Cannot delete subcategory with {product_count} products. Delete or reassign products first.'
            }), 400
        
        db.session.delete(subcategory)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Subcategory deleted successfully'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


#================= GET CATEGORY DETAILS (for edit modal) =================
@admin_bp.route('/api/category/<int:cat_id>')
@admin_required
def get_category(cat_id):
    try:
        category = Category.query.get_or_404(cat_id)
        return jsonify({
            'success': True,
            'category': {
                'cat_id': category.cat_id,
                'cat_name': category.cat_name
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


#================= GET SUBCATEGORY DETAILS (for edit modal) =================
@admin_bp.route('/api/subcategory/<int:subcat_id>')
@admin_required
def get_subcategory(subcat_id):
    try:
        subcategory = SubCategory.query.get_or_404(subcat_id)
        return jsonify({
            'success': True,
            'subcategory': {
                'subcat_id': subcategory.subcat_id,
                'subcat_name': subcategory.subcat_name,
                'cat_id': subcategory.cat_id
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500




#========================= ADMIN CUSTOMERS =================
@admin_bp.route("/customers")
@admin_required
def customers():
    customers = User.query.filter_by(role="User").all()
    return render_template("admin/customer.html", customers=customers)



# ================= ORDER MANAGEMENT =================
# Add these routes to your existing admin_routes.py file
 
@admin_bp.route('/orders')
@admin_required
def orders():
    """View all orders with filtering"""
    status_filter = request.args.get('status', 'all')
    
    orders_query = Order.query.options(
        joinedload(Order.user),
        joinedload(Order.order_details).joinedload(OrderDetail.product),
        joinedload(Order.payment)
    )
    
    if status_filter != 'all':
        orders_query = orders_query.filter_by(status=status_filter)
    
    orders = orders_query.order_by(Order.order_id.desc()).all()
    
    return render_template('admin/orders.html', 
                         orders=orders, 
                         status_filter=status_filter)
 
 
@admin_bp.route('/orders/<int:order_id>')
@admin_required
def order_details(order_id):
    """View single order details"""
    order = Order.query.options(
        joinedload(Order.user).joinedload(User.city),
        joinedload(Order.user).joinedload(User.state),
        joinedload(Order.order_details).joinedload(OrderDetail.product),
        joinedload(Order.payment)
    ).get_or_404(order_id)
    
    return render_template('admin/order_details.html', order=order)
 
 
@admin_bp.route('/api/orders/<int:order_id>/update-status', methods=['POST'])
@admin_required
def update_order_status(order_id):
    """Update order status via AJAX"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        # Validate status
        valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
        if new_status not in valid_statuses:
            return jsonify({'success': False, 'message': 'Invalid status'}), 400
        
        order = Order.query.get_or_404(order_id)
        order.status = new_status
        
        # Update payment status if order is delivered
        if new_status == 'delivered' and order.payment:
            order.payment.status = 'completed'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Order status updated to {new_status}',
            'new_status': new_status
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating order status: {str(e)}")  # Debug print
        return jsonify({'success': False, 'message': str(e)}), 500


@admin_bp.route('/api/orders/<int:order_id>/update-payment', methods=['POST'])
@admin_required
def update_payment_status(order_id):
    """Update payment status via AJAX"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        # Validate status
        valid_statuses = ['pending', 'completed', 'failed']
        if new_status not in valid_statuses:
            return jsonify({'success': False, 'message': 'Invalid status'}), 400
        
        order = Order.query.get_or_404(order_id)
        
        if not order.payment:
            return jsonify({'success': False, 'message': 'Payment record not found'}), 404
        
        order.payment.status = new_status
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Payment status updated to {new_status}',
            'new_status': new_status
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating payment status: {str(e)}")  # Debug print
        return jsonify({'success': False, 'message': str(e)}), 500

 
# ========================================
# VIEW ALL REVIEWS
# ========================================
@admin_bp.route('/reviews')
@admin_required
def reviews():
    """View all customer product reviews"""
    
    # Get all reviews with user and product info
    reviews = Feedback.query.options(
        joinedload(Feedback.user),
        joinedload(Feedback.product)
    ).order_by(Feedback.f_id.desc()).all()
    
    # Calculate stats
    total_reviews = Feedback.query.count()
    avg_rating = db.session.query(db.func.avg(Feedback.rating)).scalar() or 0
    five_star = Feedback.query.filter_by(rating=5).count()
    
    return render_template('admin/reviews.html', 
                         reviews=reviews,
                         total_reviews=total_reviews,
                         avg_rating=round(avg_rating, 1),
                         five_star=five_star)
 
 
# ========================================
# VIEW SINGLE REVIEW DETAILS
# ========================================
@admin_bp.route('/reviews/<int:f_id>')
@admin_required
def review_details(f_id):
    """View single review details"""
    review = Feedback.query.options(
        joinedload(Feedback.user),
        joinedload(Feedback.product)
    ).get_or_404(f_id)
    
    return render_template('admin/review_details.html', review=review)
 
 
# ========================================
# DELETE REVIEW
# ========================================
@admin_bp.route('/api/reviews/<int:f_id>/delete', methods=['POST'])
@admin_required
def delete_review(f_id):
    """Delete a review"""
    try:
        review = Feedback.query.get_or_404(f_id)
        
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
# FILTER REVIEWS BY RATING
# ========================================
@admin_bp.route('/reviews/filter/<int:rating>')
@admin_required
def reviews_by_rating(rating):
    """Filter reviews by star rating"""
    
    reviews = Feedback.query.options(
        joinedload(Feedback.user),
        joinedload(Feedback.product)
    ).filter_by(rating=rating).order_by(Feedback.f_id.desc()).all()
    
    total_reviews = Feedback.query.count()
    avg_rating = db.session.query(db.func.avg(Feedback.rating)).scalar() or 0
    five_star = Feedback.query.filter_by(rating=5).count()
    
    return render_template('admin/reviews.html', 
                         reviews=reviews,
                         total_reviews=total_reviews,
                         avg_rating=round(avg_rating, 1),
                         five_star=five_star,
                         filter_rating=rating)





# ================= ADMIN LOGOUT =================
@admin_bp.route("/logout")
# @admin_required
def logout():
    session.clear()
    return redirect(url_for("admin.admin_login"))


