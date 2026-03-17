from datetime import datetime
from app.extensions import db


class Mission(db.Model):
    __tablename__ = "missions"

    id = db.Column(db.Integer, primary_key=True)

    delivery_id = db.Column(db.Integer, db.ForeignKey("deliveries.id"), nullable=False, unique=True)
    drone_id = db.Column(db.Integer, db.ForeignKey("drones.id"), nullable=False)

    status = db.Column(db.String(50), default="assigned", nullable=False, index=True)

    assigned_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    takeoff_time = db.Column(db.DateTime, nullable=True)
    delivered_time = db.Column(db.DateTime, nullable=True)
    return_time = db.Column(db.DateTime, nullable=True)

    dispatch_score = db.Column(db.Float, nullable=True)
    dispatch_notes = db.Column(db.String(255), nullable=True)

    delivery = db.relationship("Delivery", back_populates="mission")
    drone = db.relationship("Drone", back_populates="missions")

    def __repr__(self):
        return f"<Mission delivery={self.delivery_id} drone={self.drone_id} status={self.status}>"