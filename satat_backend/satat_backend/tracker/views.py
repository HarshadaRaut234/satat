import json
from django.http import JsonResponse, HttpResponse
from skyfield.api import load, EarthSatellite
from datetime import datetime, timedelta
import time


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

    coordinates = {
        'ground_station': {
            'lat': 8.62572,
            'long': 77.03402
        },
        'satellite':{
            'lat': 0.0,
            'long': 0.0
        }
    }

    return JsonResponse(coordinates)


def get_satellite_position_series(requent, satellite):
    pass