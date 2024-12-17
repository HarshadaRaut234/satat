# Data decoder for poem packages by Abhishek Verma
# imports
import pandas as pd
import numpy as np

# variables
valid_lengths = [136, 74, 104, 65, 52, 126]
valid_apids = [1, 2, 3, 4, 5, 6]
packet_names = {1:'hk_pkt', 2:'Gmc', 3:'Comms', 4:'thermistor_pkt', 5:'init', 6:'log'}
filename = r'e:\\PiLOT_G2_Software\\grace_data_decoder\\Pilot-PCOC-Checks.tm1PILOT2.tds.out'
#r'E:/Support/SEC1.txt_01.txt'
#
#r'E:/Support/SEC1.txt_01.txt'

#r'C:/Abhishek/pilot2_telemetry_decoder/pilot_img1_dpu.txt'

   
# definitions
def fletcher(packet):
    '''function to check whether the calculated fletcher of the packet is equal to the written fletcher or not'''
    sumA = sumB = temp = 0
    for i in range(packet.index[0],packet.index[0]+len(packet)-2):
        sumA = ((sumA + packet[i])%255)
        sumB = ((sumB+sumA)%255)
        temp = 255-((sumA+sumB)%255)
        sumB = 255-((sumA+temp)%255)
        checksum = ((sumB << 8) | temp)
        #original_checksum = packet[packet.index[0]+len(packet)-1] << 8 | packet[packet.index[0]+len(packet)-2]
    return checksum

def show_packet(data_df, report_df, index):
    '''fetch the packet on the given index'''
    packet = data_df[int(report_df['packet_start'][index]):int(report_df['packet_start'][index]+report_df['length'][index])]
    print("packet in decimal is :-", packet)
    print("bytestream of packet is :- ", packet.values)

def decode_header(packet):
    header_fields = {'CCSDSVER': 3, 'CCSDSTYPE': 1, 'CCSDSSHF': 1, 'CCSDSAPID': 11, 'CCSDSSEQFLAGS': 2, 'CCSDSSEQCNT': 14, 'CCSDSLENGTH': 16, 'SHCOARSE': 32, 'SHFINE': 32}
    decoded_header_fields = {}
    binary_packet = ''.join(format(byte, '08b') for byte in packet)
    current_bit_index = 0

    for field, bit_count in header_fields.items():
        field_bits = binary_packet[current_bit_index:current_bit_index + bit_count]
        
        if field in ('SHCOARSE', 'SHFINE'):
            field_bits = ''.join(reversed([field_bits[i:i + 8] for i in range(0, len(field_bits), 8)]))

        decoded_header_fields[field] = int(field_bits, 2)
        current_bit_index += bit_count

    return decoded_header_fields
    

def decode_packet_data(packet, fields):
    decoded_data_fields = {}
    packet_index = 0

    for field in fields.keys():
        byte_count = fields[field]
        bin_value = ''
        
        field_bytes = packet[packet_index:packet_index + byte_count]
        if isinstance(field_bytes, pd.Series):
            field_bytes = field_bytes.tolist()
            
        bin_value = ''.join(format(byte, '08b') for byte in reversed(field_bytes))
        decoded_data_fields[field] = int(bin_value, 2)
        packet_index += byte_count

    return decoded_data_fields

def decode_packets(packet, packet_type):
    init_fields = {'img_id': 1, 'Temp_ADC_INIT': 1, 'ADF_Init': 1, 'ADF_Config_DEV': 1, 'GPS_Time_State_Vector': 32, 'Fletcher_Code': 2}
    gmc_fields = {'img_id': 1, 'GMC_Radiation_Counts': 4, 'GMC_Read_Free_Register': 4, 'GMC_Test_Voltage_ADC': 16, 'GMC_sd_dump': 1, 'GPS_Time_State_Vector': 32, 'Fletcher_Code': 2}
    therm_fields = {'Temperature_Values': 16, 'sd_dump': 1, 'GPS_Time_State_Vector': 32, 'Fletcher_Code': 2}
    comms_fields = {'img_id': 1, 'Comms_ADF_CMD_Rx': 1, 'Comms_ADF_CMD_Succ': 1, 'Comms_ADF_CMD_REJECT': 1, 'Comms_ADF_RSSI_CCA': 2, 'Comms_ADF_RSSI': 2, 'Comms_ADF_Preamble_Pattern': 1, 'Comms_ADF_Sync_Word': 4, 'Comms_ADF_Freq': 4, 'Comms_ADF_Read_REG_ADDR': 4, 'Comms_ADF_Read_REG_No_Double_Words': 1, 'Comms_ADF_Data': 32, 'Comms_ADF_State': 1, 'sd_dump': 1, 'GPS_Time_State_Vector': 32, 'Fletcher_Code': 2}
    hk_fields = {'Cmd_ADF_Counts': 1, 'Cmd_RS485_Succ_Counts': 1, 'Cmd_RS485_Fail_Counts': 1, 'Image_ID': 1, 'CLK_Rate': 2, 'Command_Loss_Timer': 4, 'Prev_CMD_Receive': 1, 'Latest_CodeWord_RCV': 1, 'Reset_Counts': 1, 'RTM': 16, 'Acceleration': 6, 'Angular_Rate': 6, 'IMU_Temp': 2, 'Voltage': 10, 'Current': 10, 'HK_Read_Pointer':4, 'HK_Write_Pointer': 4, 'Thermistor_Read_Pointer': 4, 'Thermistor_Write_Pointer': 4, 'Comms_Read_Pointer': 4, 'Comms_Write_Pointer': 4, 'sd_dump': 1, 'GPS_Time_State_Vector': 32, 'Fletcher_Code': 2}
    log_fields = {'TIMEL_1': 4, 'TIMEH_1': 4, 'TASKID_1': 1, 'TASK_STATUS_1': 2, 'TIMEL_2': 4, 'TIMEH_2': 4, 'TASKID_2': 1, 'TASK_STATUS_2': 2, 'TIMEL_3': 4, 'TIMEH_3': 4, 'TASKID_3': 1, 'TASK_STATUTS_3': 2, 'TIMEL_4': 4, 'TIMEH_4': 4, 'TASKID_4': 1, 'TASK_STATUS_4': 2, 'TIMEL_5': 4, 'TIMEH_5': 4, 'TASKID_5': 1, 'TASK_STATUS_5': 2, 'TIMEL_6': 4, 'TIMEH_6': 4, 'TASKID_6': 1, 'TASK_STATUS_6': 2, 'TIMEL_7': 4, 'TIMEH_7':4, 'TASKID_7': 1, 'TASK_STATUS_7': 2, 'TIMEL_8': 4, 'TIMEH_8': 4, 'TASKID_8': 1, 'TASK_STATUS_8': 2, 'TIMEL_9': 4, 'TIMEH_9': 4, 'TASKID_9': 1, 'TASK_STATUS_9': 2, 'TIMEL_10': 4, 'TIMEH_10': 4, 'TASKID_10': 1, 'TASK_STATUS_10': 2, 'Fletcher_Code': 2}
    decoded_header_fields = decode_header(packet[:14])
    
    if packet_type == 'init':
        decoded_data_fields = decode_packet_data(packet[14:], init_fields)
    elif packet_type == 'hk_pkt':
        decoded_data_fields = decode_packet_data(packet[14:], hk_fields)
    elif packet_type == 'Gmc':
        decoded_data_fields = decode_packet_data(packet[14:], gmc_fields)
    elif packet_type == 'Comms':
        decoded_data_fields = decode_packet_data(packet[14:], comms_fields)
    elif packet_type == 'thermistor_pkt':
        decoded_data_fields = decode_packet_data(packet[14:], therm_fields)
    elif packet_type == 'log':
        decoded_data_fields = decode_packet_data(packet[14:], log_fields)
    else:
        return None

    decoded_fields = decoded_header_fields | decoded_data_fields
    return decoded_fields
            

def packetiser(data_df, report_df):
    iterator = report_df.index
    count = 0
    decoded_values = []
    for i in iterator:
        packet = data_df[int(report_df['packet_start'][i]):int(report_df['packet_start'][i]+report_df['length'][i])].astype('uint8')
        decoded_values.append(decode_packets(packet, report_df['packet_type'][i]))
        if count > 10:
            break
        else:
            count += 1

    return decoded_values

def load_data(filename):
    byte_data = np.fromfile(filename, dtype=np.uint8)
    data_df = pd.Series(byte_data).iloc[::2].reset_index(drop=True)
    return data_df

def generate_report(data_df):
    index0x08 = data_df.where(data_df==0x08).dropna().index
    #print(index0x08)
    index0x08 = index0x08[:-1] #to elimate last packet which maybe incompleted
    valid_lengths_indexes = index0x08.where(data_df[index0x08+5].isin(valid_lengths)).dropna()
    valid_apids_indexes = index0x08.where(data_df[index0x08+1].isin(valid_apids)).dropna()
    valid_indexes = valid_apids_indexes.intersection(valid_lengths_indexes)
    report_df = pd.DataFrame({'packet_start': valid_indexes.astype('int'), 'apid': data_df[valid_indexes+1].values,'length': data_df[valid_indexes+5].values,}, index=valid_indexes)
    report_df.insert(1, "packet_type", data_df[valid_indexes+1].map(packet_names.get).values) #inserting packet_type column on the second column
    fletcher_byte_1 = data_df[report_df['packet_start']+report_df['length']-2]
    fletcher_byte_2 = data_df[report_df['packet_start']+report_df['length']-1]
    report_df['original_fletcher'] = (
    fletcher_byte_2.values.astype('int32') * 256 + fletcher_byte_1.values.astype('int32')).astype('int') #inserting original_fletcher column on the end of the columns
    report_df['calculated_fletcher'] = report_df.apply(lambda row: fletcher(data_df[row['packet_start']:row['packet_start']+row['length']]), axis=1)
    report_df['is_fletcher_correct'] = report_df.original_fletcher == report_df.calculated_fletcher #checking flether here
    report_df = report_df.reset_index(drop=True) #resetting index of fianl_df to 0 to n
    #final data_df is ready to export to files now
    # now we have processed and computed data in report_df and all raw data in data_df
    # both are equally important a report_df only have indexes of packets and lengths of those packets meanwhile data_df have the real data of  the whole file in bytes. 
    return report_df

def main():
    data = load_data(filename)
    print(data)
    report = generate_report(data)
    decoded_values = packetiser(data, report)

    return decoded_values