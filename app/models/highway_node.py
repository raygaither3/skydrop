from app.extensions import db


class HighwayNode(db.Model):
    __tablename__ = "highway_nodes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    node_type = db.Column(db.String(50), nullable=False, default="waypoint")
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<HighwayNode {self.name}>"