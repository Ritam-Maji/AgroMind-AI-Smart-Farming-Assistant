def validate_coordinates(lat: float, lon: float) -> bool:
    """Validate if coordinates are within standard Earth bounds."""
    try:
        lat, lon = float(lat), float(lon)
    except (ValueError, TypeError):
        return False
        
    if not (-90.0 <= lat <= 90.0):
        return False
    if not (-180.0 <= lon <= 180.0):
        return False
    return True

def validate_soil_ph(ph: float) -> bool:
    """Validate if soil pH is physically possible and practically relevant."""
    try:
        ph = float(ph)
        # Normal soil pH ranges between 3.0 and 10.0 (anything outside is extreme/impossible to farm)
        return 3.0 <= ph <= 10.0
    except (ValueError, TypeError):
        return False

def validate_temperature(temp: float) -> bool:
    """Validate surface temperature in Celsius."""
    try:
        temp = float(temp)
        # Assuming earth surface farming bounds
        return -50.0 <= temp <= 60.0
    except (ValueError, TypeError):
        return False
