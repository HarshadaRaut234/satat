from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.cache import cache
import threading
from .decode import *
from .models import *
from .decode import *  # Import the Celery task
import time
from datetime import datetime
import os

def unix(date, time):
    # Combine the date and time inputs in the correct order
    combined_input = f"{date} {time}:00"  # Add seconds as ":00"
    
    # Parse the combined string to a datetime object
    dt = datetime.strptime(combined_input, "%Y-%m-%d %H:%M:%S")
    
    # Convert the datetime object to a Unix timestamp
    unix_time = int(dt.timestamp())
    print(f"Unix time: {unix_time}")
    return unix_time

def file_input(request):
    return render(request, 'input_file.html')

def input(request):
    if request.method == 'POST' and request.FILES.get('binary_input_file'):
        file = request.FILES['binary_input_file']

        #to check if file with correct extension is uploaded
        file_name = file.name
        file_extension = os.path.splitext(file_name)[1].lower()
        # Allowed file extensions
        allowed_extensions = {'.out', '.bin', '.txt'}

        start_time = request.POST['start_time']
        start_date = request.POST['start_date']
        filetype = request.POST['filetype']
        print(filetype)
        unix_time = unix(start_date, start_time)

        data_df = None

        if filetype == 'txt':
            print('inside true')
            data_df = pd.read_csv(file, header=9, delimiter='\t', usecols=[f'CH-{3}']).drop(0).reset_index(drop=True)
            data_df=data_df.dropna()
            data_df = data_df[f'CH-{3}'].apply(lambda x: int(str(x)[0:4], 16))

        if file_extension in allowed_extensions:
            # Create a unique task ID for tracking progress
            task_id = str(time.time()).replace('.', '')

            # Reset progress
            cache.set(f"progress_{task_id}", 0)

            # Run the decoder in a background thread
            threading.Thread(target=ccsds_decoder, args=(file, task_id, unix_time, data_df, filetype)).start()

            # Return the task ID to the client for tracking
            return HttpResponse(f"""
                                Your file has been captured successfully. It is under processing and will be updated in database soon under task:
                                task_id: {task_id} <br>
                                For interactive graphs <a href="http://localhost:3000/goto/TMXKr9IHR?orgId=1"> visit here </a>
                                """)#JsonResponse({"task_id": task_id})
        else:
            return JsonResponse({"error": f"Invalid file extension: {file_extension}. Allowed extensions are .out, .bin, .txt"}, status=400)
    return JsonResponse({"error": "No file provided"}, status=400)

def get_progress(request, task_id):
    # Retrieve progress from the cache
    progress = cache.get(f"progress_{task_id}", None)
    
    if progress is None:
        return JsonResponse({"error": "Task ID not found"}, status=404)
    
    return JsonResponse({"progress": progress})


