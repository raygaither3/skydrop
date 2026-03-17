from flask import Blueprint, render_template
from flask_login import login_required

from app.models.drone import Drone
from app.models.delivery import Delivery
from app.models.mission import Mission


map_bp = Blueprint("map", __name__, url_prefix="/map")


@map_bp.route("/")
@login_required
def operations_map():
    drones = Drone.query.all()
    deliveries = Delivery.query.all()
    missions = Mission.query.all()

    hub = {
        "name": "SkyDrop Hub - Lake Charles",
        "lat": 30.2266,
        "lng": -93.2174,
    }

    return render_template(
        "map/map.html",
        hub=hub,
        drones=drones,
        deliveries=deliveries,
        missions=missions,
    )