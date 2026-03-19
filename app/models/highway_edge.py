from app.extensions import db


class HighwayEdge(db.Model):
    __tablename__ = "highway_edges"

    id = db.Column(db.Integer, primary_key=True)

    start_node_id = db.Column(
        db.Integer,
        db.ForeignKey("highway_nodes.id"),
        nullable=False,
    )
    end_node_id = db.Column(
        db.Integer,
        db.ForeignKey("highway_nodes.id"),
        nullable=False,
    )

    distance_m = db.Column(db.Float, nullable=False)
    max_speed_mps = db.Column(db.Float, nullable=False, default=12.0)
    priority = db.Column(db.Integer, nullable=False, default=1)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_bidirectional = db.Column(db.Boolean, nullable=False, default=True)

    start_node = db.relationship(
        "HighwayNode",
        foreign_keys=[start_node_id],
        backref="outgoing_highway_edges",
    )
    end_node = db.relationship(
        "HighwayNode",
        foreign_keys=[end_node_id],
        backref="incoming_highway_edges",
    )

    def __repr__(self):
        return f"<HighwayEdge {self.start_node_id}->{self.end_node_id}>"