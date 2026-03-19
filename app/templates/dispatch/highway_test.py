{% extends "base.html" %}

{% block content %}
<div class="container py-4">
    <h2 class="mb-2">Drone Highway Test</h2>
    <p class="text-muted">Planned route distance: {{ "%.1f"|format(route_distance_m) }} meters</p>

    <div id="map" style="height: 600px; border-radius: 12px;"></div>
</div>

<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css">
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

<script>
    const routeData = {{ route_data|tojson }};

    const map = L.map("map").setView([routeData[0].lat, routeData[0].lng], 13);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
    }).addTo(map);

    const latlngs = routeData.map(point => [point.lat, point.lng]);

    L.polyline(latlngs, { weight: 5 }).addTo(map);

    routeData.forEach(point => {
        const label = point.name ? `${point.type}: ${point.name}` : point.type;
        L.marker([point.lat, point.lng]).addTo(map).bindPopup(label);
    });

    map.fitBounds(latlngs);
</script>
{% endblock %}