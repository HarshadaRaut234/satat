from django.urls import path
from . import views

urlpatterns = [
    path('', views.cme),
    path('groundstation/', views.get_groundstation_position),
    path('satellite/<int:satellite_id>/positions/', views.get_satellite_position, name='satellite_positions'),
    path('update-tle/', views.update_tle),
]
