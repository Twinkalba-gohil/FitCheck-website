from models import db

class Order(db.Model):
    __tablename__ = "order_table"

    order_id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey("user_table.u_id"))

    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Numeric(10, 2), nullable=False)
    ship_amount = db.Column(db.Numeric(10, 2), nullable=False)
    net_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum("pending", "confirmed", "shipped", "delivered", "cancelled"), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship("User", back_populates="orders")
    order_details = db.relationship("OrderDetail", backref="order")
    payment = db.relationship('Payment', uselist=False, back_populates='order')


class OrderDetail(db.Model):
    __tablename__ = "order_detail_table"

    od_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order_table.order_id"))
    pro_id = db.Column(db.Integer, db.ForeignKey("product_table.pro_id"))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    product = db.relationship("Product", backref="order_details")