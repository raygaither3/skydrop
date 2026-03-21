from flask import Blueprint, render_template
from werkzeug.security import generate_password_hash
from app.extensions import db
from app.models import User, HighwayNode, HighwayEdge, NoFlyZone

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("home.html")


@main_bp.route("/health")
def health():
    return "ok", 200


# 🔥 TEMP: CREATE / PROMOTE ADMIN
@main_bp.route("/setup-admin-temp")
def setup_admin_temp():
    email = "raygaither3@gmail.com"
    password = "test123"

    existing = User.query.filter_by(email=email).first()

    if existing:
        existing.name = "Ray Gaither"
        existing.role = "admin"
        existing.password_hash = generate_password_hash(password)
        db.session.commit()
        return "✅ Existing user updated to admin"

    user = User(
        name="Ray Gaither",
        email=email,
        password_hash=generate_password_hash(password),
        role="admin"
    )

    db.session.add(user)
    db.session.commit()

    return "✅ Admin created"


# 🔥 TEMP: SEED HIGHWAYS
@main_bp.route("/seed-highways-temp")
def seed_highways_temp():
    db.session.query(HighwayEdge).delete()
    db.session.query(HighwayNode).delete()
    db.session.query(NoFlyZone).delete()

    nodes = [
        HighwayNode(name="Hub", latitude=30.2266, longitude=-93.2174, node_type="hub", is_active=True),
        HighwayNode(name="Downtown", latitude=30.2230, longitude=-93.2160, node_type="waypoint", is_active=True),
        HighwayNode(name="Mall", latitude=30.2050, longitude=-93.2400, node_type="waypoint", is_active=True),
        HighwayNode(name="Hospital", latitude=30.2105, longitude=-93.2210, node_type="priority", is_active=True),
    ]

    db.session.add_all(nodes)
    db.session.commit()

    edges = [
        HighwayEdge(start_node_id=nodes[0].id, end_node_id=nodes[1].id, distance_m=400, max_speed_mps=15, priority=1, is_active=True, is_bidirectional=True),
        HighwayEdge(start_node_id=nodes[1].id, end_node_id=nodes[2].id, distance_m=2500, max_speed_mps=15, priority=2, is_active=True, is_bidirectional=True),
        HighwayEdge(start_node_id=nodes[0].id, end_node_id=nodes[3].id, distance_m=1800, max_speed_mps=20, priority=1, is_active=True, is_bidirectional=True),
    ]

    db.session.add_all(edges)

    zone = NoFlyZone(
        name="Airport Zone",
        center_lat=30.1266,
        center_lng=-93.2230,
        radius_m=3000,
        is_active=True
    )

    db.session.add(zone)
    db.session.commit()

    return "🚀 Highway system seeded"