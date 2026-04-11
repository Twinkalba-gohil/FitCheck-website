from models import db

class Cart(db.Model):
    __tablename__ = "cart_table"

    cart_id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey("user_table.u_id"))
    pro_id = db.Column(db.Integer, db.ForeignKey("product_table.pro_id"))
    quantity = db.Column(db.Integer, nullable=False)
