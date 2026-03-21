import os

from flask import Flask, render_template
from werkzeug.security import generate_password_hash

from config import Config
from .extensions import db, login_manager, migrate


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from .models import (
        User,
        Delivery,
        Drone,
        Mission,
        HighwayNode,
        HighwayEdge,
        NoFlyZone,
    )

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    # 🔥 ADMIN CLI
    @app.cli.command("create-admin")
    def create_admin():
        email = "raygaither3@gmail.com"
        password = "test123"

        existing = User.query.filter_by(email=email).first()

        if existing:
            existing.name = "Ray Gaither"
            existing.role = "admin"
            existing.password_hash = generate_password_hash(password)
            db.session.commit()
            print("✅ Existing user updated to admin")
            return

        user = User(
            name="Ray Gaither",
            email=email,
            password_hash=generate_password_hash(password),
            role="admin"
        )

        db.session.add(user)
        db.session.commit()

        print("✅ Admin created")

    # 🔥 HIGHWAY SEED CLI
    @app.cli.command("seed-highways")
    def seed_highways():
        from app.models import HighwayNode, HighwayEdge, NoFlyZone

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

        print("🚀 Highway system seeded")

    from .main.routes import main_bp
    from .auth.routes import auth_bp
    from .dashboard.routes import dashboard_bp
    from .deliveries.routes import deliveries_bp
    from .fleet.routes import fleet_bp
    from .dispatch.routes import dispatch_bp
    from .map.routes import map_bp
    from .admin.routes import admin_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(deliveries_bp)
    app.register_blueprint(fleet_bp)
    app.register_blueprint(dispatch_bp)
    app.register_blueprint(map_bp)

    return app