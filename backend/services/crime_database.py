import json
from typing import List, Dict
from datetime import datetime, time

class CrimeDatabase:
    """
    Historical crime data for Delhi/NCR routes
    """
    
    # Delhi/NCR coordinates bounding box
    DELHI_BBOX = {
        "min_lat": 28.40,
        "max_lat": 28.90,
        "min_lng": 76.80,
        "max_lng": 77.40
    }
    
    # Crime hotspots in Delhi (real locations with their crime patterns)
    CRIME_HOTSPOTS = {
        # Format: (lat_range, lng_range): {crime_types}
        ((28.65, 28.67), (77.22, 77.25)): {  # Connaught Place area
            "theft": 8, "harassment": 6, "snatching": 7, "robbery": 5,
            "peak_hours": ["18:00-23:00"], "safety_score_day": 65, "safety_score_night": 40
        },
        ((28.53, 28.55), (77.25, 77.28)): {  # Noida Sector 18
            "harassment": 7, "eve_teasing": 6, "theft": 5,
            "peak_hours": ["20:00-02:00"], "safety_score_day": 70, "safety_score_night": 45
        },
        ((28.62, 28.64), (77.08, 77.12)): {  # Kashmere Gate ISBT
            "snatching": 9, "theft": 8, "harassment": 5,
            "peak_hours": ["19:00-01:00", "04:00-07:00"], "safety_score_day": 60, "safety_score_night": 35
        },
        ((28.70, 28.72), (77.10, 77.15)): {  # Delhi University North Campus
            "harassment": 6, "eve_teasing": 7, "theft": 4,
            "peak_hours": ["17:00-22:00"], "safety_score_day": 75, "safety_score_night": 50
        },
        ((28.55, 28.57), (77.18, 77.22)): {  # Mayur Vihar Phase-1
            "theft": 4, "snatching": 5, "harassment": 3,
            "peak_hours": ["21:00-03:00"], "safety_score_day": 80, "safety_score_night": 55
        },
        ((28.50, 28.52), (77.08, 77.12)): {  # Faridabad Sector 16
            "robbery": 6, "theft": 7, "harassment": 4,
            "peak_hours": ["20:00-04:00"], "safety_score_day": 65, "safety_score_night": 40
        },
        ((28.48, 28.50), (77.02, 77.05)): {  # Gurugram Cyber City
            "drunk_driving": 8, "harassment": 5, "theft": 6,
            "peak_hours": ["22:00-05:00"], "safety_score_day": 85, "safety_score_night": 60
        },
        ((28.67, 28.69), (77.05, 77.08)): {  # Karol Bagh
            "snatching": 8, "theft": 9, "harassment": 6,
            "peak_hours": ["18:00-23:00"], "safety_score_day": 60, "safety_score_night": 35
        },
        ((28.59, 28.61), (77.20, 77.24)): {  # Laxmi Nagar
            "eve_teasing": 7, "harassment": 8, "theft": 5,
            "peak_hours": ["19:00-01:00"], "safety_score_day": 70, "safety_score_night": 45
        },
        ((28.43, 28.45), (77.30, 77.34)): {  # Greater Noida
            "harassment": 4, "theft": 5, "snatching": 4,
            "peak_hours": ["21:00-03:00"], "safety_score_day": 85, "safety_score_night": 65
        }
    }
    
    # Busy/safe routes (main roads with good lighting and crowd)
    BUSY_ROUTES = [
        ((28.66, 28.68), (77.23, 77.26)),  # Rajpath area
        ((28.52, 28.54), (77.19, 77.23)),  # Noida Expressway
        ((28.69, 28.71), (77.14, 77.18)),  # Outer Ring Road
        ((28.50, 28.52), (77.09, 77.13)),  # NH19 (Faridabad)
        ((28.47, 28.49), (77.03, 77.07)),  # NH48 (Gurugram)
    ]
    
    # Police stations in Delhi/NCR
    POLICE_STATIONS = [
        {
            "name": "Connaught Place Police Station",
            "lat": 28.6305, "lng": 77.2177,
            "phone": "011-23412345",
            "type": "police"
        },
        {
            "name": "Noida Sector 20 Police Station",
            "lat": 28.5678, "lng": 77.3210,
            "phone": "0120-2451234",
            "type": "police"
        },
        {
            "name": "Kashmere Gate Police Station",
            "lat": 28.6652, "lng": 77.2301,
            "phone": "011-23862345",
            "type": "police"
        },
        {
            "name": "Delhi University Police Station",
            "lat": 28.6881, "lng": 77.2120,
            "phone": "011-27667222",
            "type": "police"
        },
        {
            "name": "Women Helpline Delhi",
            "lat": 28.6100, "lng": 77.2300,
            "phone": "1091",
            "type": "helpline"
        },
        {
            "name": "Women Helpline Noida",
            "lat": 28.5800, "lng": 77.3300,
            "phone": "0120-2456789",
            "type": "helpline"
        },
        {
            "name": "PCR Van Control Room",
            "lat": 28.7000, "lng": 77.1000,
            "phone": "100",
            "type": "emergency"
        },
        {
            "name": "Sector 49 Police Station Gurugram",
            "lat": 28.4300, "lng": 77.0500,
            "phone": "0124-2321000",
            "type": "police"
        },
        {
            "name": "Faridabad Police Commissionerate",
            "lat": 28.4100, "lng": 77.3100,
            "phone": "0129-2411000",
            "type": "police"
        }
    ]
    
    def get_crimes_in_area(self, lat: float, lng: float) -> List[Dict]:
        """Get crimes for a specific location based on historical data"""
        crimes = []
        
        # Check if in crime hotspot
        for (lat_range, lng_range), crime_data in self.CRIME_HOTSPOTS.items():
            if lat_range[0] <= lat <= lat_range[1] and lng_range[0] <= lng <= lng_range[1]:
                # Add crimes based on intensity
                for crime_type, intensity in crime_data.items():
                    if crime_type not in ['peak_hours', 'safety_score_day', 'safety_score_night']:
                        if intensity >= 5:  # Only add significant crimes
                            crimes.append({
                                "type": crime_type,
                                "severity": min(intensity // 2 + 1, 5),  # Scale to 1-5
                                "location": f"{lat:.4f},{lng:.4f}",
                                "source": "historical_data"
                            })
        
        # Check if on busy route (safer)
        for lat_range, lng_range in self.BUSY_ROUTES:
            if lat_range[0] <= lat <= lat_range[1] and lng_range[0] <= lng <= lng_range[1]:
                # Add positive safety indicators
                crimes.append({
                    "type": "well_lit_area",
                    "severity": -2,  # Negative severity means safer
                    "location": f"{lat:.4f},{lng:.4f}",
                    "source": "busy_route"
                })
                crimes.append({
                    "type": "crowded_area",
                    "severity": -3,
                    "location": f"{lat:.4f},{lng:.4f}",
                    "source": "busy_route"
                })
        
        return crimes
    
    def get_safety_score(self, lat: float, lng: float, time_of_day: str = "day") -> int:
        """Get safety score for a location"""
        base_score = 50
        
        # Check crime hotspots
        for (lat_range, lng_range), crime_data in self.CRIME_HOTSPOTS.items():
            if lat_range[0] <= lat <= lat_range[1] and lng_range[0] <= lng <= lng_range[1]:
                if time_of_day == "night":
                    base_score = crime_data.get("safety_score_night", 50)
                else:
                    base_score = crime_data.get("safety_score_day", 70)
        
        # Bonus for busy routes
        for lat_range, lng_range in self.BUSY_ROUTES:
            if lat_range[0] <= lat <= lat_range[1] and lng_range[0] <= lng <= lng_range[1]:
                base_score += 15
        
        # Ensure within bounds
        return max(0, min(100, base_score))
    
    def get_nearest_police_stations(self, lat: float, lng: float, limit: int = 3) -> List[Dict]:
        """Find nearest police stations"""
        import math
        
        def distance(lat1, lng1, lat2, lng2):
            return math.sqrt((lat2 - lat1)**2 + (lng2 - lng1)**2)
        
        stations_with_dist = []
        for station in self.POLICE_STATIONS:
            dist = distance(lat, lng, station["lat"], station["lng"])
            station_copy = station.copy()
            station_copy["distance_km"] = round(dist * 111, 2)  # approx km
            stations_with_dist.append(station_copy)
        
        # Sort by distance
        stations_with_dist.sort(key=lambda x: x["distance_km"])
        
        return stations_with_dist[:limit]

# Global instance
crime_db = CrimeDatabase()