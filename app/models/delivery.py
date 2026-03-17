from datetime import datetime
from app.extensions import db


class Delivery(db.Model):
    __tablename__ = "deliveries"

    id = db.Column(db.Integer, primary_key=True)

    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_address = db.Column(db.String(200), nullable=False)
    customer_phone = db.Column(db.String(30), nullable=False)

    package_weight = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="pending", nullable=False, index=True)

    pickup_address = db.Column(db.String(200), nullable=True)
    pickup_lat = db.Column(db.Float, nullable=True)
    pickup_lng = db.Column(db.Float, nullable=True)

    destination_lat = db.Column(db.Float, nullable=True)
    destination_lng = db.Column(db.Float, nullable=True)

    priority = db.Column(db.String(20), default="standard", nullable=False)
    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    mission = db.relationship(
        "Mission",
        back_populates="delivery",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Delivery {self.order_number} - {self.status}>"