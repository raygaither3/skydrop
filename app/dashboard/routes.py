from flask import Blueprint, render_template
from flask_login import current_user

from app.models.delivery import Delivery
from app.models.drone import Drone
from app.models.mission import Mission
from app.utils.decorators import role_required

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
@role_required("admin", "business_staff")
def home():
    pending_deliveries_count = Delivery.query.filter_by(status="pending").count()

    active_missions_count = Mission.query.filter(
        Mission.status.in_(["assigned", "in_flight"])
    ).count()

    available_drones_count = Drone.query.filter_by(status="idle", is_active=True).count()

    delivered_count = Delivery.query.filter_by(status="delivered").count()

    recent_deliveries = Delivery.query.order_by(Delivery.created_at.desc()).limit(5).all()
    recent_missions = Mission.query.order_by(Mission.assigned_at.desc()).limit(5).all()

    return render_template(
        "dashboard/dashboard.html",
        user=current_user,
        pending_deliveries_count=pending_deliveries_count,
        active_missions_count=active_missions_count,
        available_drones_count=available_drones_count,
        delivered_count=delivered_count,
        recent_deliveries=recent_deliveries,
        recent_missions=recent_missions,
    )