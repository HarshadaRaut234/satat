import json
import requests
from django.http import JsonResponse
from skyfield.api import load, EarthSatellite, utc
from datetime import datetime, timedelta

def get_satellite_position(request, satellite_id):
    # Celestrak URL to fetch TLE for a specific satellite (e.g., ISS)
    url = f'https://celestrak.org/NORAD/elements/gp.php?CATNR={satellite_id}&FORMAT=tle'
    
    try:
        # Fetch TLE data from Celestrak
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        tle_data = response.text.strip().splitlines()

        if len(tle_data) < 2:
            return JsonResponse({'error': 'Invalid TLE data'}, status=400)

        # The TLE data should be two lines
        line1 = tle_data[1]
        line2 = tle_data[2]
        satellite_name = tle_data[0]  # Name from the first line
        
        satellite_tle = {
            "name": satellite_name,
            "line1": line1,
            "line2": line2
        }

        positions = []
        for i in range(0, 24):  # Generate position for the next 24 hours
            ts = load.timescale()
            satellite = EarthSatellite(satellite_tle['line1'], satellite_tle['line2'], satellite_tle['name'], ts)

            # Get the current UTC time for each hour and set UTC timezone
            current_time = datetime.utcnow() + timedelta(hours=i)
            current_time = current_time.replace(tzinfo=utc)  # Set the UTC timezone

            t = ts.utc(current_time.year, current_time.month, current_time.day, current_time.hour, 
                       current_time.minute, current_time.second)

            geocentric = satellite.at(t)
            subpoint = geocentric.subpoint()

            # Extract latitude, longitude, and altitude
            latitude = subpoint.latitude.degrees
            longitude = subpoint.longitude.degrees
            altitude = subpoint.elevation.m

            positions.append({
                'time': current_time.isoformat(),
                'lat': latitude,
                'lon': longitude,
                'alt': altitude
            })

        return JsonResponse(positions, safe=False)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
