from django.shortcuts import render, redirect
from django.http import JsonResponse
from .decode import *
from .models import *
from .decode import *  # Import the Celery task

def file_input(request):
    return render(request, 'input_file.html')

def input(request):
    if request.method == 'POST' and request.FILES.get('binary_input_file'):
        file = request.FILES['binary_input_file']
        file_data = file.read()
        file_name = file.name
        # Call the Celery task with the file name and data
        print("file input taken")
        ccsds_decoder(file_name, file_data)
        return redirect('http://localhost:3000/goto/TMXKr9IHR?orgId=1')
    return JsonResponse({"error": "No file provided"}, status=400)

