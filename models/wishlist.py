from models import db

class Wishlist(db.Model):
    __tablename__ = "wishlist_table"

    w_id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey("user_table.u_id"))
    pro_id = db.Column(db.Integer, db.ForeignKey("product_table.pro_id"))
