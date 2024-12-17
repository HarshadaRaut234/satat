from django.shortcuts import render
from django.http import JsonResponse
from .decode import main

def ccsds_decoder(request):
    decoded_value = main()
    return JsonResponse(decoded_value, safe = False)