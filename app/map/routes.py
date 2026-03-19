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

    mission_map_data = []

    for mission in missions:
        mission_map_data.append({
            "id": mission.id,
            "status": mission.status,
            "route_data": mission.route_data or [],
            "drone": {
                "name": mission.drone.name if mission.drone else "Unknown",
                "model": mission.drone.model if mission.drone else "Unknown",
                "battery_level": mission.drone.battery_level if mission.drone else None,
                "current_lat": mission.drone.current_lat if mission.drone else None,
                "current_lng": mission.drone.current_lng if mission.drone else None,
            },
            "delivery": {
                "order_number": mission.delivery.order_number if mission.delivery else "Unknown",
                "customer_name": mission.delivery.customer_name if mission.delivery else "Unknown",
                "customer_address": mission.delivery.customer_address if mission.delivery else "Unknown",
                "destination_lat": mission.delivery.destination_lat if mission.delivery else None,
                "destination_lng": mission.delivery.destination_lng if mission.delivery else None,
            }
        })

    return render_template(
        "map/map.html",
        hub=hub,
        drones=drones,
        deliveries=deliveries,
        missions=missions,
        mission_map_data=mission_map_data,
    )