from app import create_app
from app.extensions import db
from app.models.highway_node import HighwayNode
from app.models.highway_edge import HighwayEdge
from app.services.highway_service import haversine_m

app = create_app()

with app.app_context():
    hub = HighwayNode(name="Main Hub", latitude=30.2266, longitude=-93.2174, node_type="hub")
    north = HighwayNode(name="North Corridor", latitude=30.2400, longitude=-93.2170, node_type="waypoint")
    east = HighwayNode(name="East Corridor", latitude=30.2260, longitude=-93.1900, node_type="waypoint")
    south = HighwayNode(name="South Corridor", latitude=30.2050, longitude=-93.2170, node_type="waypoint")
    west = HighwayNode(name="West Corridor", latitude=30.2260, longitude=-93.2450, node_type="waypoint")

    db.session.add_all([hub, north, east, south, west])
    db.session.commit()

    edges = [
        HighwayEdge(
            start_node_id=hub.id,
            end_node_id=north.id,
            distance_m=haversine_m(hub.latitude, hub.longitude, north.latitude, north.longitude),
        ),
        HighwayEdge(
            start_node_id=hub.id,
            end_node_id=east.id,
            distance_m=haversine_m(hub.latitude, hub.longitude, east.latitude, east.longitude),
        ),
        HighwayEdge(
            start_node_id=hub.id,
            end_node_id=south.id,
            distance_m=haversine_m(hub.latitude, hub.longitude, south.latitude, south.longitude),
        ),
        HighwayEdge(
            start_node_id=hub.id,
            end_node_id=west.id,
            distance_m=haversine_m(hub.latitude, hub.longitude, west.latitude, west.longitude),
        ),
    ]

    db.session.add_all(edges)
    db.session.commit()