from django.shortcuts import render, redirect
from django.http import JsonResponse
from .decode import *
from .models import *

def file_input(request):
    return render(request, 'input_file.html')

def get_packet_by_index(data_df, summary_df, index):
    packet = data_df[int(summary_df['packet_start'][index]):int(summary_df['packet_start'][index]+summary_df['length'][index])].astype('uint8')
    return decode_packets(packet, summary_df['packet_type'][index])

def differential(series):
    prev = series.iloc[0]['GMC_Radiation_Counts']
    for i in series:
        i['GMC_Radiation_Counts_Differential'] = i['GMC_Radiation_Counts'] - prev
        prev = i['GMC_Radiation_Counts']
    return series

def ccsds_decoder(request):
    # decoded_value = main()

    file = request.FILES['binary_input_file']
    data = file.read()
    byte_data = np.frombuffer(data, dtype=np.uint8)
    data_df = pd.Series(byte_data).iloc[::2].reset_index(drop=True)

    summary_df = summarize_data(data_df)

    # decoded_values = packetiser(data_df, summary_df)
    decoded_values_series = pd.Series()  #Empty list to store decoded values

    for i in range(len(summary_df)):
        decoded_values = get_packet_by_index(data_df, summary_df, i)
    
        decoded_values_series.loc[i]=decoded_values

    hk_packet_series = decoded_values_series[decoded_values_series.apply(lambda x: x["CCSDSAPID"] == 1)]
    gmc_packet_series = decoded_values_series[decoded_values_series.apply(lambda x: x["CCSDSAPID"] == 2)]
    gmc_packet_series = differential(gmc_packet_series)
    comms_packet_series = decoded_values_series[decoded_values_series.apply(lambda x: x["CCSDSAPID"] == 3)]
    temp_packet_series = decoded_values_series[decoded_values_series.apply(lambda x: x["CCSDSAPID"] == 4)]
    init_packet_series = decoded_values_series[decoded_values_series.apply(lambda x: x["CCSDSAPID"] == 5)]

    hk_packet_list = [HkPacket(Filename=file.name, **row)for _, row in hk_packet_series.items()]
    gmc_packet_list = [GmcPacket(Filename=file.name, **row)for _, row in gmc_packet_series.items()]
    comms_packet_list = [CommsPacket(Filename=file.name, **row)for _, row in comms_packet_series.items()]
    temp_packet_list = [TempPacket(Filename=file.name, **row)for _, row in temp_packet_series.items()]
    init_packet_list = [InitPacket(Filename=file.name, **row)for _, row in init_packet_series.items()]


    HkPacket.objects.bulk_create(hk_packet_list)
    GmcPacket.objects.bulk_create(gmc_packet_list)
    CommsPacket.objects.bulk_create(comms_packet_list)
    TempPacket.objects.bulk_create(temp_packet_list)
    InitPacket.objects.bulk_create(init_packet_list)

    decoded_values_list=decoded_values_series.tolist()

    # return JsonResponse(gmc_packet_series.tolist(), safe=False)
    return redirect('http://localhost:3000/goto/TMXKr9IHR?orgId=1')