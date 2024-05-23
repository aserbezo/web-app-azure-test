from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('latest-coordinates/', views.latest_coordinates, name='latest_coordinates'),
]
