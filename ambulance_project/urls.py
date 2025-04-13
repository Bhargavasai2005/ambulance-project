from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Ambulance Routing API! Use /api/ endpoints to interact with the system.")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ambulance_app.urls')),
    path('', home, name='home'),
]