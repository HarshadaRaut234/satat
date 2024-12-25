from django.contrib import admin
from .models import *
import datetime

class HkAdmin(admin.ModelAdmin):
    list_display = ('Formatted_Time','Filename', 'Cmd_RS485_Succ_Counts', 'PIS_Current', 'PIS_Voltage', 'Image_ID', 'CLK_Rate')
    search_fields = ('Filename',)

    def Formatted_Time(self, obj):
        return datetime.datetime.fromtimestamp(float(obj.Time)).strftime('%Y-%m-%d %H:%M:%S')
    Formatted_Time.short_description = 'Formatted_Time'

class GmcAdmin(admin.ModelAdmin):
    list_display = ('Formatted_Time','Filename', 'GMC_Radiation_Counts', 'GMC_Radiation_Counts_Differential','GM_Tube_High_Voltage', 'HVDC_IC_Control_Voltage')
    search_fields = ('Filename',)

    def Formatted_Time(self, obj):
        return datetime.datetime.fromtimestamp(float(obj.Time)).strftime('%Y-%m-%d %H:%M:%S')
    Formatted_Time.short_description = 'Formatted_Time'

class CommsAdmin(admin.ModelAdmin):
    list_display = ('Formatted_Time','Filename', 'Comms_ADF_RSSI', 'Comms_ADF_CMD_Succ')
    search_fields = ('Filename',)

    def Formatted_Time(self, obj):
        return datetime.datetime.fromtimestamp(float(obj.Time)).strftime('%Y-%m-%d %H:%M:%S')
    Formatted_Time.short_description = 'Formatted_Time'

class TempAdmin(admin.ModelAdmin):
    list_display = ('Formatted_Time','Filename', 'GMC_Temperature', 'PIS_Temperature', 'CUB_Temperature', 'OBC_Temperature', 'Sun_Facing_Connector_Temp', 'Sun_Facing_Flat_Temp', 'Adjacent_Sun_Facing_Window_Temp', 'Base_Plate_Temp')
    search_fields = ('Filename',)

    def Formatted_Time(self, obj):
        return datetime.datetime.fromtimestamp(float(obj.Time)).strftime('%Y-%m-%d %H:%M:%S')
    Formatted_Time.short_description = 'Formatted_Time'


admin.site.register(HkPacket, HkAdmin)
admin.site.register(GmcPacket, GmcAdmin)
admin.site.register(CommsPacket, CommsAdmin)
admin.site.register(TempPacket, TempAdmin)
admin.site.register(InitPacket)
