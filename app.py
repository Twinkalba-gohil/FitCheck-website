from datetime import timedelta
import os
from urllib import response
from flask import Flask, redirect, render_template, session, request
from sqlalchemy import func
from config import Config
from models import db
from models.product import Product
from models.category import Category, SubCategory

def create_app():
    app = Flask(__name__)
       # Load config
    app.config.from_object(Config)

    # DEBUG: check secret key (remove later)
    print("SECRET KEY:", app.config["SECRET_KEY"])


    app.permanent_session_lifetime = timedelta(days=30)

    @app.context_processor
    def inject_categories():
        """Make categories and subcategories available to ALL templates"""
        categories = Category.query.all()
        subcategories = SubCategory.query.all()
        return dict(categories=categories, subcategories=subcategories)
    
    
    @app.route('/')
    @app.route('/index')
    def index():

        products_top = Product.query.order_by(func.rand()).limit(25).all()

        top_ids = [p.pro_id for p in products_top]

        products_bottom = Product.query.filter(
            ~Product.pro_id.in_(top_ids)
        ).order_by(func.rand()).limit(15).all()

        return render_template(
            'user/index.html',
            products_top=products_top,
            products_bottom=products_bottom
        )
    
    @app.route("/admin")
    def admin_root():
        return redirect("/admin/login")
    
    @app.after_request
    def admin_cache_control(response):
        response.headers["Cache-Control"] = "no-store"
        return response

    

    # CORRECT upload folder
    app.config["UPLOAD_FOLDER"] = os.path.join(
        app.root_path, "static", "uploads", "products"
    )
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5MB

    #AUTO CREATE FOLDER
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    #JWTManager(app)

    with app.app_context():
        db.create_all()
        print("Tables created successfully")


    from routes.user_routes import user_bp
    from routes.admin_routes import admin_bp


    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)