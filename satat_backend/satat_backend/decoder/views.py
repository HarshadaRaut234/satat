from django.shortcuts import render
from django.http import JsonResponse

def ccsds_decoder(request):
    decoded_value = {}
    return JsonResponse(decoded_value)