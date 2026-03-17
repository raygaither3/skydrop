from datetime import datetime
from app.extensions import db


class Drone(db.Model):
    __tablename__ = "drones"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    model = db.Column(db.String(100), nullable=False)

    status = db.Column(db.String(50), default="idle", nullable=False, index=True)
    battery_level = db.Column(db.Integer, default=100, nullable=False)
    payload_capacity = db.Column(db.Float, nullable=False)

    current_lat = db.Column(db.Float, nullable=True)
    current_lng = db.Column(db.Float, nullable=True)

    home_lat = db.Column(db.Float, nullable=True)
    home_lng = db.Column(db.Float, nullable=True)

    is_active = db.Column(db.Boolean, default=True, nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    missions = db.relationship("Mission", back_populates="drone", lazy=True)

    def __repr__(self):
        return f"<Drone {self.name} - {self.status}>"