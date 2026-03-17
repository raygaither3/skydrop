from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required

from app.extensions import db
from app.models.drone import Drone

fleet_bp = Blueprint("fleet", __name__, url_prefix="/fleet")


@fleet_bp.route("/")
@login_required
def fleet_list():
    drones = Drone.query.order_by(Drone.name.asc()).all()
    return render_template("fleet/fleet_list.html", drones=drones)


@fleet_bp.route("/seed")
@login_required
def seed_drones():
    if Drone.query.count() > 0:
        flash("Drones already exist.", "warning")
        return redirect(url_for("fleet.fleet_list"))

    starter_drones = [
        Drone(
            name="SkyDrop-01",
            model="SD Courier Mk1",
            status="idle",
            battery_level=100,
            payload_capacity=5.0,
            current_lat=30.2266,
            current_lng=-93.2174,
        ),
        Drone(
            name="SkyDrop-02",
            model="SD Courier Mk1",
            status="charging",
            battery_level=62,
            payload_capacity=5.0,
            current_lat=30.2266,
            current_lng=-93.2174,
        ),
        Drone(
            name="SkyDrop-03",
            model="SD Heavy Lift",
            status="maintenance",
            battery_level=45,
            payload_capacity=10.0,
            current_lat=30.2266,
            current_lng=-93.2174,
        ),
    ]

    db.session.add_all(starter_drones)
    db.session.commit()

    flash("Starter drones created.", "success")
    return redirect(url_for("fleet.fleet_list"))