from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "user_table"

    u_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(35), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum("Admin", "User"), default="User")
    contact = db.Column(db.String(10), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False)
    area_name = db.Column(db.String(255), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey("city_table.city_id"))
    state_id = db.Column(db.Integer, db.ForeignKey("state_table.state_id"))
    pincode = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())


    city = db.relationship("City", backref="users")
    state = db.relationship("State", backref="users")

    orders = db.relationship("Order", back_populates="user")
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)