from flask_login import UserMixin
from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default="business_staff", nullable=False)

    deliveries = db.relationship("Delivery", backref="created_by", lazy=True)

    @staticmethod
    def normalize_email(email):
        return email.strip().lower() if email else email

    def __init__(self, **kwargs):
        if "email" in kwargs and kwargs["email"]:
            kwargs["email"] = self.normalize_email(kwargs["email"])
        super().__init__(**kwargs)

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_staff(self):
        return self.role in ["admin", "business_staff"]

    def __repr__(self):
        return f"<User {self.email}>"