from models import db

class Payment(db.Model):
    __tablename__ = "payment_table"

    pay_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order_table.order_id"))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    method = db.Column(db.String(50), nullable=False, default="CASH")
    status = db.Column(db.String(20), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, default=db.func.now())


    order = db.relationship('Order', back_populates='payment')