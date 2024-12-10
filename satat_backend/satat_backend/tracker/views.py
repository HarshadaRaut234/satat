import json
from django.http import JsonResponse, HttpResponse
from skyfield.api import load, EarthSatellite
from datetime import datetime, timedelta

def get_satellite_position(request, satellite_id):
    # Taking Inspire-Sat-1 for example will update to PiLOT-G2 in future and then geneic
    # INSPIRESAT-1            
    # 1 51657U 22013B   24344.03394000  .00028502  00000+0  84648-3 0  9997
    # 2 51657  97.5137   3.0182 0004944 268.9071  91.1605 15.34736037156290
    satellite_tle = {
        "name" : "INSPIRESAT-1",
        "line1": "1 51657U 22013B   24344.03394000  .00028502  00000+0  84648-3 0  9997",
        "line2": "2 51657  97.5137   3.0182 0004944 268.9071  91.1605 15.34736037156290"
    }

    positions = []
    for i in range(0, 24):
        ts = load.timescale()
        satellite = EarthSatellite(satellite_tle['line1'], satellite_tle['line2'], satellite_tle['name'], ts)
        current_time = datetime.utcnow() + timedelta(hours=i)
        t = ts.utc(tuple(current_time.timetuple())[:6])
        geocentric = satellite.at(t)

        r = geocentric.position.au

        lat = r[0][0] / 1000.0
        lon = r[1][0] / 1000.0
        alt = r[2][0] / 1000.0
        positions.append({
            'time': current_time.isoformat(),
            'lat': lat,
            'lon': lon,
            'alt': alt
        })

    return HttpResponse(str(positions)+'    '+str(current_time.timetuple()))
