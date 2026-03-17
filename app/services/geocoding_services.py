from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from geopy.geocoders import Nominatim


geolocator = Nominatim(user_agent="skydrop_app")


def get_coordinates_from_address(address: str):
    """
    Convert a street address into latitude and longitude.

    Returns:
        tuple[float | None, float | None]:
            (latitude, longitude) if found, otherwise (None, None)
    """
    if not address or not address.strip():
        return None, None

    try:
        location = geolocator.geocode(address.strip())

        if location is None:
            return None, None

        return float(location.latitude), float(location.longitude)

    except (GeocoderTimedOut, GeocoderServiceError):
        return None, None