import requests

def get_routes(start, end, mode):
    if mode == "car":
        profile = "driving"
    elif mode == "bike":
        profile = "cycling"
    else:
        profile = "walking"

    url = f"http://router.project-osrm.org/route/v1/{profile}/{start};{end}"
    params = {
        "alternatives": "true",
        "overview": "full",
        "geometries": "geojson"
    }

    try:
        print("Calling OSRM API...")
        response = requests.get(url, params=params, timeout=5)
        print("OSRM response received")

        if response.status_code != 200:
            print("OSRM returned non-200 status:", response.status_code)
            return {"routes": []}

        return response.json()

    except Exception as e:
        print("ERROR calling OSRM:", e)
        return {"routes": []}