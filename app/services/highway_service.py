import heapq
import math

from app.models.highway_node import HighwayNode
from app.models.highway_edge import HighwayEdge
from app.models.no_fly_zone import NoFlyZone


def haversine_m(lat1, lng1, lat2, lng2):
    earth_radius_m = 6371000

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)

    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return earth_radius_m * c


def meters_per_degree_lat():
    return 111320.0


def meters_per_degree_lng(lat):
    return 111320.0 * math.cos(math.radians(lat))


def point_to_segment_distance_m(px, py, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return math.sqrt((px - x1) ** 2 + (py - y1) ** 2)

    t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
    t = max(0, min(1, t))

    closest_x = x1 + t * dx
    closest_y = y1 + t * dy

    return math.sqrt((px - closest_x) ** 2 + (py - closest_y) ** 2)


def segment_intersects_no_fly_zone(start_lat, start_lng, end_lat, end_lng, zone):
    avg_lat = (start_lat + end_lat + zone.center_lat) / 3.0

    x1 = 0.0
    y1 = 0.0
    x2 = (end_lng - start_lng) * meters_per_degree_lng(avg_lat)
    y2 = (end_lat - start_lat) * meters_per_degree_lat()

    px = (zone.center_lng - start_lng) * meters_per_degree_lng(avg_lat)
    py = (zone.center_lat - start_lat) * meters_per_degree_lat()

    distance = point_to_segment_distance_m(px, py, x1, y1, x2, y2)
    return distance <= zone.radius_m


def edge_is_blocked(edge, no_fly_zones):
    for zone in no_fly_zones:
        if segment_intersects_no_fly_zone(
            edge.start_node.latitude,
            edge.start_node.longitude,
            edge.end_node.latitude,
            edge.end_node.longitude,
            zone,
        ):
            return True
    return False


def build_highway_graph():
    nodes = HighwayNode.query.filter_by(is_active=True).all()
    edges = HighwayEdge.query.filter_by(is_active=True).all()
    no_fly_zones = NoFlyZone.query.filter_by(is_active=True).all()

    graph = {node.id: [] for node in nodes}
    node_lookup = {node.id: node for node in nodes}

    for edge in edges:
        if not edge.start_node or not edge.end_node:
            continue

        if edge_is_blocked(edge, no_fly_zones):
            continue

        cost = edge.distance_m * edge.priority

        graph[edge.start_node_id].append((edge.end_node_id, cost))

        if edge.is_bidirectional:
            graph[edge.end_node_id].append((edge.start_node_id, cost))

    return graph, node_lookup


def find_nearest_highway_node(lat, lng):
    nodes = HighwayNode.query.filter_by(is_active=True).all()
    if not nodes:
        return None

    return min(
        nodes,
        key=lambda node: haversine_m(lat, lng, node.latitude, node.longitude)
    )


def shortest_path_node_ids(start_node_id, end_node_id):
    graph, _ = build_highway_graph()

    queue = [(0, start_node_id, [])]
    visited = set()

    while queue:
        total_cost, current_node_id, path = heapq.heappop(queue)

        if current_node_id in visited:
            continue

        visited.add(current_node_id)
        path = path + [current_node_id]

        if current_node_id == end_node_id:
            return path

        for neighbor_id, edge_cost in graph.get(current_node_id, []):
            if neighbor_id not in visited:
                heapq.heappush(queue, (total_cost + edge_cost, neighbor_id, path))

    return []


def generate_highway_route(start_lat, start_lng, end_lat, end_lng):
    start_node = find_nearest_highway_node(start_lat, start_lng)
    end_node = find_nearest_highway_node(end_lat, end_lng)

    if not start_node or not end_node:
        return [
            {"lat": start_lat, "lng": start_lng, "type": "origin"},
            {"lat": end_lat, "lng": end_lng, "type": "destination"},
        ]

    node_ids = shortest_path_node_ids(start_node.id, end_node.id)

    if not node_ids:
        return [
            {"lat": start_lat, "lng": start_lng, "type": "origin"},
            {"lat": end_lat, "lng": end_lng, "type": "destination"},
        ]

    graph, node_lookup = build_highway_graph()

    route_points = [
        {"lat": start_lat, "lng": start_lng, "type": "origin"},
    ]

    for node_id in node_ids:
        node = node_lookup[node_id]
        route_points.append(
            {
                "lat": node.latitude,
                "lng": node.longitude,
                "type": node.node_type,
                "name": node.name,
                "node_id": node.id,
            }
        )

    route_points.append(
        {"lat": end_lat, "lng": end_lng, "type": "destination"},
    )

    return route_points


def calculate_route_distance_m(route_points):
    if not route_points or len(route_points) < 2:
        return 0.0

    total = 0.0

    for i in range(len(route_points) - 1):
        p1 = route_points[i]
        p2 = route_points[i + 1]
        total += haversine_m(p1["lat"], p1["lng"], p2["lat"], p2["lng"])

    return total