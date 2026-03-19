from app.extensions import db


class NoFlyZone(db.Model):
    __tablename__ = "no_fly_zones"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    center_lat = db.Column(db.Float, nullable=False)
    center_lng = db.Column(db.Float, nullable=False)
    radius_m = db.Column(db.Float, nullable=False)

    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<NoFlyZone {self.name}>"