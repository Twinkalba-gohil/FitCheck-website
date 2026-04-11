from models import db

class Category(db.Model):
    __tablename__ = "category_table"

    cat_id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(50), nullable=False, unique=True)
    subcategories = db.relationship("SubCategory", backref="category", lazy=True)



class SubCategory(db.Model):
    __tablename__ = "subcategory_table"

    subcat_id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer, db.ForeignKey("category_table.cat_id"))
    subcat_name = db.Column(db.String(50), nullable=False)
