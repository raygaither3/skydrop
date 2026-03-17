from math import radians, sin, cos, sqrt, atan2

from app.models.drone import Drone


# Default hub location for now (Lake Charles example)
HUB_LAT = 30.2266
HUB_LNG = -93.2174


def haversine_distance_miles(lat1, lng1, lat2, lng2):
    """
    Calculate distance in miles between two latitude/longitude points.
    Returns None if any coordinate is missing.
    """
    if None in (lat1, lng1, lat2, lng2):
        return None

    earth_radius_miles = 3958.8

    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius_miles * c


def calculate_distance_miles(point_a, point_b):
    """
    Accepts:
        point_a = (lat, lng)
        point_b = (lat, lng)

    Returns:
        Rounded distance in miles, or None
    """
    if not point_a or not point_b:
        return None

    lat1, lng1 = point_a
    lat2, lng2 = point_b

    distance = haversine_distance_miles(lat1, lng1, lat2, lng2)
    if distance is None:
        return None

    return round(distance, 2)


def get_drone_position(drone):
    """
    Return the best available position for a drone.

    Priority:
    1. current_lat/current_lng
    2. home_lat/home_lng
    3. global hub coordinates
    """
    if drone.current_lat is not None and drone.current_lng is not None:
        return float(drone.current_lat), float(drone.current_lng)

    if drone.home_lat is not None and drone.home_lng is not None:
        return float(drone.home_lat), float(drone.home_lng)

    return HUB_LAT, HUB_LNG


def get_delivery_position(delivery):
    """
    Return delivery destination coordinates as a tuple.
    """
    if delivery.destination_lat is None or delivery.destination_lng is None:
        return None

    return float(delivery.destination_lat), float(delivery.destination_lng)


def can_assign_drone(delivery, drone):
    """
    Determine whether a drone is eligible to take a delivery.
    """
    if not drone.is_active:
        return False, "Drone is inactive."

    if drone.status != "idle":
        return False, "Drone is not idle."

    if delivery.destination_lat is None or delivery.destination_lng is None:
        return False, "Delivery is missing destination coordinates."

    if delivery.package_weight > drone.payload_capacity:
        return False, "Payload exceeds drone capacity."

    if drone.battery_level < 30:
        return False, "Battery too low."

    return True, "Eligible"


def calculate_dispatch_score(delivery, drone):
    """
    Calculate a dispatch score for a drone.
    Higher score = better candidate.
    """
    eligible, reason = can_assign_drone(delivery, drone)
    if not eligible:
        return -1, reason

    drone_position = get_drone_position(drone)
    delivery_position = get_delivery_position(delivery)

    distance = calculate_distance_miles(drone_position, delivery_position)

    score = 100.0
    notes = []

    if distance is not None:
        score -= distance * 8
        notes.append(f"Distance penalty applied ({distance:.1f} mi).")
    else:
        notes.append("No coordinates available, distance not factored.")

    score += drone.battery_level * 0.35
    notes.append(f"Battery bonus applied ({drone.battery_level}%).")

    payload_margin = drone.payload_capacity - delivery.package_weight
    score += payload_margin * 6
    notes.append(f"Payload margin bonus applied ({payload_margin:.1f} kg).")

    if delivery.priority == "urgent":
        score += 8
        notes.append("Urgent delivery bonus applied.")

    return round(score, 2), " ".join(notes)


def find_best_drone_for_delivery(delivery):
    """
    Find the best eligible drone for a delivery.
    """
    drones = Drone.query.filter_by(is_active=True).all()

    best_drone = None
    best_score = -1
    best_notes = "No suitable drone found."

    for drone in drones:
        score, notes = calculate_dispatch_score(delivery, drone)
        if score > best_score:
            best_drone = drone
            best_score = score
            best_notes = notes

    if best_score < 0:
        return None, None, "No eligible drone available."

    return best_drone, best_score, best_notes