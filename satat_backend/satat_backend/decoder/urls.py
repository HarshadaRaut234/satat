from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.file_input),
    path('submit/', views.input, name='submit'),  # Submit form URL
    path('progress/<str:task_id>/', views.get_progress, name='get_progress'),
]
