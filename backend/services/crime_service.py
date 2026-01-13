import random
from .crime_database import crime_db
from datetime import datetime

def get_crimes_near(lat, lng, time_of_day="day"):
    """
    Get crimes based on historical data + some randomness for realism
    """
    # Get historical crimes
    historical_crimes = crime_db.get_crimes_in_area(lat, lng)
    
    # Add some random crime based on time
    current_hour = datetime.now().hour
    
    # More crimes at night
    if 20 <= current_hour <= 5 or time_of_day == "night":
        night_crimes = [
            {"type": "poor_lighting", "severity": 3, "source": "time_based"},
            {"type": "isolated_area", "severity": 4, "source": "time_based"}
        ]
        historical_crimes.extend(night_crimes)
    
    # If no crimes found, maybe it's a safe area
    if not historical_crimes and random.random() < 0.3:
        historical_crimes.append({
            "type": "safe_zone", 
            "severity": -1,  # Negative for safe
            "source": "random_check"
        })
    
    return historical_crimes[:10]  # Limit to 10 crimes