from django.contrib import admin
from .models import *

admin.site.register(HkPacket)
admin.site.register(GmcPacket)
admin.site.register(CommsPacket)
admin.site.register(TempPacket)
admin.site.register(InitPacket)
