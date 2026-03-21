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


@main_bp.route("/seed-drones-temp")
def seed_drones_temp():
    from datetime import datetime
    from app.models import Drone
    from app.extensions import db

    # Clear only drones (safe)
    db.session.query(Drone).delete()

    drones = [
        Drone(
            name="SkyDrop Alpha",
            model="Tarot X6",
            status="idle",
            battery_level=100,
            payload_capacity=2.5,
            current_lat=30.2266,
            current_lng=-93.2174,
            home_lat=30.2266,
            home_lng=-93.2174,
            is_active=True,
            last_seen=datetime.utcnow()
        ),
        Drone(
            name="SkyDrop Beta",
            model="Tarot X6",
            status="charging",
            battery_level=65,
            payload_capacity=2.5,
            current_lat=30.2300,
            current_lng=-93.2200,
            home_lat=30.2266,
            home_lng=-93.2174,
            is_active=True,
            last_seen=datetime.utcnow()
        ),
        Drone(
            name="SkyDrop Gamma",
            model="Tarot X6",
            status="in_transit",
            battery_level=78,
            payload_capacity=2.5,
            current_lat=30.2100,
            current_lng=-93.2000,
            home_lat=30.2266,
            home_lng=-93.2174,
            is_active=True,
            last_seen=datetime.utcnow()
        ),
        Drone(
            name="SkyDrop Delta",
            model="Tarot X6",
            status="maintenance",
            battery_level=40,
            payload_capacity=2.5,
            current_lat=30.2400,
            current_lng=-93.2300,
            home_lat=30.2266,
            home_lng=-93.2174,
            is_active=False,
            last_seen=datetime.utcnow()
        ),
    ]

    db.session.add_all(drones)
    db.session.commit()

    return "🚀 Drones seeded successfully"