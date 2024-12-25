import requests
from django.http import JsonResponse
from .models import Satellite
from skyfield.api import load, EarthSatellite, utc
from datetime import datetime, timedelta
from django.utils import timezone

def get_satellite_position(request, satellite_id):
    try:
        # Ensure TLE data is up-to-date by calling update_tle
        satellite = update_tle(satellite_id)
        # satellite_tle = {
        #     "name": satellite_name,
        #     "line1": line1,
        #     "line2": line2
        # }

        positions = []
        for i in range(0, 24):  # Generate position for the next 24 hours
            ts = load.timescale()
            satellite_obj = EarthSatellite(satellite.tle_line1, satellite.tle_line2, satellite.name, ts)

            # Get the current UTC time for each hour and set UTC timezone
            current_time = datetime.utcnow() + timedelta(hours=i)
            current_time = current_time.replace(tzinfo=utc)  # Set the UTC timezone

            t = ts.utc(current_time.year, current_time.month, current_time.day, current_time.hour, 
                       current_time.minute, current_time.second)

            geocentric = satellite_obj.at(t)
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

def get_groundstation_position(request):
    return JsonResponse({
        'lat': 8.6265,
        'long': 77.0338
    })

def update_tle(satellite_id):
    # Check if the satellite's TLE is already in the database
    satellite = Satellite.objects.filter(norad_id=satellite_id).first()

    # If the satellite is not in the database, fetch and store the TLE
    if not satellite:
        print(f"Fetching TLE from CelesTrak for satellite ID: {satellite_id} (not found in DB)")
        return fetch_and_store_tle(satellite_id)

    # If the satellite is in the database, check if the TLE is outdated
    if satellite.last_updated < timezone.now() - timedelta(days=1):  # Adjust this threshold as needed
        print(f"Fetching TLE from CelesTrak for satellite ID: {satellite_id} (outdated TLE in DB)")
        return fetch_and_store_tle(satellite_id)
    
    print(f"Using cached TLE from database for satellite ID: {satellite_id}")
    return satellite

def fetch_and_store_tle(satellite_id):
    # Fetch TLE data from Celestrak
    url = f'https://celestrak.org/NORAD/elements/gp.php?CATNR={satellite_id}&FORMAT=tle'
    response = requests.get(url)
    response.raise_for_status()
    tle_data = response.text.strip().splitlines()

    if len(tle_data) < 2:
        raise ValueError("Invalid TLE data")

    # The TLE data should be two lines
    line1 = tle_data[1]
    line2 = tle_data[2]
    satellite_name = tle_data[0]  # Name from the first line

    # Store the TLE data in the database
    satellite = Satellite.objects.create(
        norad_id=satellite_id,
        name=satellite_name,
        tle_line1=line1,
        tle_line2=line2
    )

    return satellite
