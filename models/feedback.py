from models import db

class Feedback(db.Model):
    __tablename__ = "feedback_table"

    f_id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey("user_table.u_id"))
    pro_id = db.Column(db.Integer, db.ForeignKey("product_table.pro_id"))
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)

    # Relationships
    user = db.relationship('User', backref='feedbacks')
    product = db.relationship('Product', backref='feedbacks')


