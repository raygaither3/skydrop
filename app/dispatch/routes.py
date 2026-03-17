from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from app.extensions import db
from app.models.delivery import Delivery
from app.models.drone import Drone
from app.models.mission import Mission
from app.services.dispatch_service import (
    HUB_LAT,
    HUB_LNG,
    calculate_distance_miles,
    can_assign_drone,
    find_best_drone_for_delivery,
    get_delivery_position,
    get_drone_position,
)

dispatch_bp = Blueprint("dispatch", __name__, url_prefix="/dispatch")


@dispatch_bp.route("/")
@login_required
def dispatch_board():
    pending_deliveries = (
        Delivery.query.filter_by(status="pending")
        .order_by(Delivery.created_at.asc())
        .all()
    )

    available_drones = (
        Drone.query.filter_by(status="idle", is_active=True)
        .order_by(Drone.name.asc())
        .all()
    )

    active_missions = Mission.query.order_by(Mission.assigned_at.desc()).all()

    delivery_drone_options = {}

    for delivery in pending_deliveries:
        options = []
        delivery_pos = get_delivery_position(delivery)

        for drone in available_drones:
            drone_pos = get_drone_position(drone)
            distance_miles = calculate_distance_miles(drone_pos, delivery_pos)

            options.append({
                "drone": drone,
                "distance_miles": distance_miles,
            })

        options.sort(
            key=lambda item: item["distance_miles"]
            if item["distance_miles"] is not None else 999999
        )

        delivery_drone_options[delivery.id] = options

    return render_template(
        "dispatch/dispatch_board.html",
        pending_deliveries=pending_deliveries,
        available_drones=available_drones,
        active_missions=active_missions,
        delivery_drone_options=delivery_drone_options,
    )


@dispatch_bp.route("/assign/<int:delivery_id>/<int:drone_id>")
@login_required
def assign_mission(delivery_id, drone_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    drone = Drone.query.get_or_404(drone_id)

    if delivery.status != "pending":
        flash("That delivery is not available for assignment.", "warning")
        return redirect(url_for("dispatch.dispatch_board"))

    if delivery.mission:
        flash("That delivery already has a mission.", "warning")
        return redirect(url_for("dispatch.dispatch_board"))

    eligible, reason = can_assign_drone(delivery, drone)
    if not eligible:
        flash(reason, "danger")
        return redirect(url_for("dispatch.dispatch_board"))

    mission = Mission(
        delivery_id=delivery.id,
        drone_id=drone.id,
        status="assigned",
        dispatch_notes="Manually assigned by dispatcher."
    )

    delivery.status = "assigned"
    drone.status = "assigned"

    db.session.add(mission)
    db.session.commit()

    flash("Mission assigned successfully.", "success")
    return redirect(url_for("dispatch.mission_detail", mission_id=mission.id))


@dispatch_bp.route("/auto-assign/<int:delivery_id>")
@login_required
def auto_assign_mission(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)

    if delivery.status != "pending":
        flash("That delivery is not pending.", "warning")
        return redirect(url_for("dispatch.dispatch_board"))

    if delivery.mission:
        flash("That delivery already has a mission.", "warning")
        return redirect(url_for("dispatch.dispatch_board"))

    best_drone, best_score, notes = find_best_drone_for_delivery(delivery)

    if not best_drone:
        flash("No suitable drone is currently available.", "warning")
        return redirect(url_for("dispatch.dispatch_board"))

    mission = Mission(
        delivery_id=delivery.id,
        drone_id=best_drone.id,
        status="assigned",
        dispatch_score=best_score,
        dispatch_notes=notes
    )

    delivery.status = "assigned"
    best_drone.status = "assigned"

    db.session.add(mission)
    db.session.commit()

    flash(
        f"Delivery auto-assigned to {best_drone.name} with dispatch score {best_score}.",
        "success"
    )
    return redirect(url_for("dispatch.mission_detail", mission_id=mission.id))


@dispatch_bp.route("/mission/<int:mission_id>")
@login_required
def mission_detail(mission_id):
    mission = Mission.query.get_or_404(mission_id)

    drone_pos = get_drone_position(mission.drone)
    delivery_pos = get_delivery_position(mission.delivery)
    distance_miles = calculate_distance_miles(drone_pos, delivery_pos)

    return render_template(
        "dispatch/mission_detail.html",
        mission=mission,
        drone_pos=drone_pos,
        delivery_pos=delivery_pos,
        distance_miles=distance_miles,
        hub_lat=HUB_LAT,
        hub_lng=HUB_LNG,
    )


@dispatch_bp.route("/mission/<int:mission_id>/launch")
@login_required
def launch_mission(mission_id):
    mission = Mission.query.get_or_404(mission_id)

    if mission.status != "assigned":
        flash("Only assigned missions can be launched.", "warning")
        return redirect(url_for("dispatch.mission_detail", mission_id=mission.id))

    mission.status = "in_flight"
    mission.delivery.status = "in_flight"
    mission.drone.status = "in_flight"
    mission.takeoff_time = datetime.utcnow()

    db.session.commit()

    flash("Mission launched.", "success")
    return redirect(url_for("dispatch.mission_detail", mission_id=mission.id))


@dispatch_bp.route("/mission/<int:mission_id>/complete")
@login_required
def complete_mission(mission_id):
    mission = Mission.query.get_or_404(mission_id)

    if mission.status != "in_flight":
        flash("Only in-flight missions can be completed.", "warning")
        return redirect(url_for("dispatch.mission_detail", mission_id=mission.id))

    mission.status = "delivered"
    mission.delivery.status = "delivered"
    mission.drone.status = "idle"

    now = datetime.utcnow()
    mission.delivered_time = now
    mission.return_time = now

    db.session.commit()

    flash("Mission completed.", "success")
    return redirect(url_for("dispatch.mission_detail", mission_id=mission.id))