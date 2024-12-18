from django.shortcuts import render
from django.http import JsonResponse
from .decode import *

def file_input(request):
    return render(request, 'input_file.html')

def ccsds_decoder(request):
    # decoded_value = main()

    file = request.FILES['binary_input_file']
    data = file.read()
    byte_data = np.frombuffer(data, dtype=np.uint8)
    data_df = pd.Series(byte_data).iloc[::2].reset_index(drop=True)

    summary_df = summarize_data(data_df)

    decoded_values = packetiser(data_df, summary_df)
    
    return JsonResponse(decoded_values, safe = False)