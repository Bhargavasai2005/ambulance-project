from django.urls import path
from . import views

urlpatterns = [
    path("book_hospital/", views.book_hospital, name="book_hospital"),
    path("book_appointment/", views.book_appointment, name="book_appointment"),
    path("get_nearest_ambulance/", views.get_nearest_ambulance, name="get_nearest_ambulance"),
    path("get_optimized_ambulance_route/", views.get_optimized_ambulance_route, name="get_optimized_ambulance_route"),
    path("get_traffic_signal_status/", views.get_traffic_signal_status, name="get_traffic_signal_status"),
]