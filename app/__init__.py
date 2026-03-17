from flask import Flask
from config import Config
from .extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    import os
    os.makedirs("instance", exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    from .models import User, Delivery, Drone, Mission

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .main.routes import main_bp
    from .auth.routes import auth_bp
    from .dashboard.routes import dashboard_bp
    from .deliveries.routes import deliveries_bp
    from .fleet.routes import fleet_bp
    from .dispatch.routes import dispatch_bp
    from .map.routes import map_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(deliveries_bp)
    app.register_blueprint(fleet_bp)
    app.register_blueprint(dispatch_bp)
    app.register_blueprint(map_bp)

    return app