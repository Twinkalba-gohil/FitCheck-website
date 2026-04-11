from models import db
from models.category import SubCategory

class Product(db.Model):
    __tablename__ = "product_table"

    pro_id = db.Column(db.Integer, primary_key=True)
    subcat_id = db.Column(db.Integer, db.ForeignKey("subcategory_table.subcat_id"))

    pro_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(255), nullable=False)
    size = db.Column(db.String(20))
    base_price = db.Column(db.Numeric(10, 2), nullable=False)
    brand = db.Column(db.String(90), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    discount = db.Column(db.Integer, default=0)   
    created_at = db.Column(db.DateTime, default=db.func.now())


    subcategory = db.relationship("SubCategory", backref="products")

    # relation with images
    images = db.relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")

    @property
    def final_price(self):
        if self.discount:
            return round(float(self.base_price) * (1 - self.discount / 100), 2)
        return float(self.base_price)

class ProductImage(db.Model):
    __tablename__ = "product_image_table"

    img_id = db.Column(db.Integer, primary_key=True)
    pro_id = db.Column(db.Integer, db.ForeignKey('product_table.pro_id'), nullable=False)

    image = db.Column(db.String(255), nullable=False)

    product = db.relationship("Product", back_populates="images")


