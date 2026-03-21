from app import create_app
from app.extensions import db
from app.models import Drone
from datetime import datetime

app = create_app()

with app.app_context():
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

    print("🚀 Seeded drones successfully!")