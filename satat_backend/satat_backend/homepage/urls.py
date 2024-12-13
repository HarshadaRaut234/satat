from django.urls import path, include
from .views import welcome

urlpatterns = [
    path('', welcome),
]
