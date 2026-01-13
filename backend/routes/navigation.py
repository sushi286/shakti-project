from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from services.map_service import get_routes
from services.crime_service import get_crimes_near
from services.safety_engine import calculate_safety_score, calculate_crowd_factor
import datetime

router = APIRouter()

class NavigationRequest(BaseModel):
    source: str  # "lat,lng"
    destination: str  # "lat,lng"
    mode: str = "walk"
    time: Optional[str] = None
    prioritize: str = "safety"  # "safety" or "fastest"

class RouteResponse(BaseModel):
    coordinates: List[List[float]]
    safety_score: int
    crowd_factor: float  # 0-1 (higher = safer)
    risk_reason: str
    alert: Optional[str]
    distance: float  # in meters
    duration: float  # in seconds
    is_safest: bool = False

class NavigationResponse(BaseModel):
    status: str
    safest_route: RouteResponse
    all_routes: List[RouteResponse]
    nearest_police: List[dict]

@router.post("/navigate", response_model=NavigationResponse)
def navigate(data: NavigationRequest):
    print("---- /navigate API HIT ----")
    
    # Parse coordinates
    src_lat, src_lng = map(float, data.source.split(','))
    dest_lat, dest_lng = map(float, data.destination.split(','))
    
    # Determine time of day
    current_hour = datetime.datetime.now().hour
    if data.time:
        time_of_day = data.time
    elif 6 <= current_hour < 18:
        time_of_day = "day"
    elif 18 <= current_hour < 21:
        time_of_day = "evening"
    else:
        time_of_day = "night"
    
    print(f"From: {src_lat},{src_lng} To: {dest_lat},{dest_lng}")
    print(f"Mode: {data.mode}, Time: {time_of_day}")
    
    # Get routes from OSRM
    routes_data = get_routes(
        f"{src_lng},{src_lat}",
        f"{dest_lng},{dest_lat}",
        data.mode
    )
    
    results = []
    
    for idx, route in enumerate(routes_data.get("routes", [])):
        coords = route["geometry"]["coordinates"]
        total_crimes = []
        
        # Sample points along route
        sampled_points = coords[::20]  # Every 20th point
        
        # Calculate safety for this route
        route_safety_scores = []
        route_crowd_factors = []
        
        for point in sampled_points:
            lng, lat = point[0], point[1]
            crimes = get_crimes_near(lat, lng, time_of_day)
            total_crimes.extend(crimes)
            
            # Calculate safety at this point
            safety = calculate_safety_score(crimes, time_of_day, lat, lng)
            route_safety_scores.append(safety)
            
            # Calculate crowd factor
            crowd = calculate_crowd_factor(lat, lng)
            route_crowd_factors.append(crowd)
        
        # Average safety score for route
        avg_safety = sum(route_safety_scores) // len(route_safety_scores) if route_safety_scores else 50
        
        # Average crowd factor
        avg_crowd = sum(route_crowd_factors) / len(route_crowd_factors) if route_crowd_factors else 0.5
        
        # Adjust safety based on crowd (more crowded = safer)
        crowd_adjusted_safety = avg_safety + int(avg_crowd * 20)
        crowd_adjusted_safety = min(100, crowd_adjusted_safety)
        
        # Risk reason
        if crowd_adjusted_safety < 40:
            risk_reason = "High risk - avoid isolated areas"
        elif crowd_adjusted_safety < 60:
            risk_reason = "Moderate risk - stay alert"
        elif avg_crowd > 0.7:
            risk_reason = "Safer - well-lit crowded route"
        else:
            risk_reason = "Relatively safe route"
        
        # Alert
        alert = None
        if crowd_adjusted_safety < 40:
            alert = "⚠️ High risk! Consider alternate route or avoid traveling alone."
        elif crowd_adjusted_safety < 50 and time_of_day == "night":
            alert = "🌙 Caution: Night travel in medium risk area"
        
        results.append({
            "coordinates": coords,
            "safety_score": crowd_adjusted_safety,
            "crowd_factor": round(avg_crowd, 2),
            "risk_reason": risk_reason,
            "alert": alert,
            "distance": route.get("distance", 0),
            "duration": route.get("duration", 0),
            "route_index": idx
        })
    
    # Sort based on priority
    if data.prioritize == "safety":
        results.sort(key=lambda x: (x["safety_score"], -x["distance"]), reverse=True)
    else:  # fastest
        results.sort(key=lambda x: (x["duration"], x["safety_score"]))
    
    # Mark safest route
    if results:
        results[0]["is_safest"] = True
    
    # Get nearest police stations from destination
    from services.crime_database import crime_db
    nearest_police = crime_db.get_nearest_police_stations(dest_lat, dest_lng, 2)
    
    print(f"Found {len(results)} routes, safest: {results[0]['safety_score'] if results else 'N/A'}")
    
    return {
        "status": "success",
        "safest_route": results[0] if results else None,
        "all_routes": results,
        "nearest_police": nearest_police
    }