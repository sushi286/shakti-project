from .crime_database import crime_db

def calculate_safety_score(crimes, time_of_day="day", lat=None, lng=None):
    """
    Enhanced safety score calculation with crowd factor
    """
    base_score = 50
    
    if lat and lng:
        # Get base score from historical data
        base_score = crime_db.get_safety_score(lat, lng, time_of_day)
    
    if crimes:
        for crime in crimes:
            severity = crime.get("severity", 1)
            base_score -= severity * 5  # Each crime point reduces score
    
    # Adjust for time
    if time_of_day == "night":
        base_score -= 15
    elif time_of_day == "evening":
        base_score -= 5
    
    # Ensure score is within bounds
    if base_score < 0:
        base_score = 0
    if base_score > 100:
        base_score = 100
    
    return int(base_score)

def calculate_crowd_factor(lat, lng):
    """
    Calculate how busy/crowded an area is (safer if more crowded)
    """
    # Check if on busy route
    for lat_range, lng_range in crime_db.BUSY_ROUTES:
        if lat_range[0] <= lat <= lat_range[1] and lng_range[0] <= lng <= lng_range[1]:
            return 0.8  # 80% crowded
    
    # Check crime hotspots (less crowded)
    for (lat_range, lng_range), _ in crime_db.CRIME_HOTSPOTS.items():
        if lat_range[0] <= lat <= lat_range[1] and lng_range[0] <= lng <= lng_range[1]:
            return 0.3  # 30% crowded
    
    return 0.5  # Default