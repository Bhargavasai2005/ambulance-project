from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from geopy.distance import geodesic
import threading
import time
import json
from django.shortcuts import get_object_or_404

# Sample data
clinics = {
    "City Hospital": {"location": (12.9716, 77.5946), "available_slots": 5},
    "Heart Care": {"location": (12.2958, 76.6394), "available_slots": 3},
    "General Clinic": {"location": (13.0827, 80.2707), "available_slots": 7},
    "Downtown Hospital": {"location": (12.9719, 77.6412), "available_slots": 2},
    "River Side Clinic": {"location": (13.0350, 77.5970), "available_slots": 4}
}
ambulances = {
    "Ambulance_1": {"location": [12.972, 77.595]},  # Matches Signal_1 location
    "Ambulance_2": {"location": [12.2958, 76.6394]},
    "Ambulance_3": {"location": [13.0827, 80.2707]}
}
traffic_signals = {
        "Signal_1": {"location": [12.972, 77.595], "status": "GREEN"},
        "Signal_2": {"location": [12.296, 76.64], "status": "RED"},
        "Signal_3": {"location": [13.083, 80.271], "status": "RED"}
}

hospitals = {
    "Metro Hospital": {"location": [12.9612, 77.6388], "capacity": 50, "occupied_beds": 40},
    "Green Valley Hospital": {"location": [13.0025, 77.6208], "capacity": 30, "occupied_beds": 25},
    "Sunrise Hospital": {"location": [12.9154, 77.6512], "capacity": 100, "occupied_beds": 75}
}

def update_traffic_signals():
    while True:
        for signal in traffic_signals:
            for ambulance in ambulances:
                distance = geodesic(ambulances[ambulance]["location"], traffic_signals[signal]["location"]).meters
                traffic_signals[signal]["status"] = "GREEN" if distance <= 10 else "RED"
        time.sleep(5)
threading.Thread(target=update_traffic_signals, daemon=True).start()

@csrf_exempt
def book_hospital(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_location = tuple(data.get("location"))
        available_hospitals = {
            hospital: {
                "distance": geodesic(user_location, hospitals[hospital]["location"]).km,
                "available_beds": hospitals[hospital]["capacity"] - hospitals[hospital]["occupied_beds"]
            }
            for hospital, data in hospitals.items() if hospitals[hospital]["capacity"] - hospitals[hospital]["occupied_beds"] > 0
        }
        if not available_hospitals:
            return JsonResponse({"error": "No available hospitals"})
        nearest_hospital = min(available_hospitals, key=lambda x: available_hospitals[x]["distance"])
        hospitals[nearest_hospital]["occupied_beds"] += 1
        return JsonResponse({
            "message": f"Hospital booked at {nearest_hospital}!",
            "location": hospitals[nearest_hospital]["location"],
            "remaining_beds": hospitals[nearest_hospital]["capacity"] - hospitals[nearest_hospital]["occupied_beds"]
        })

@csrf_exempt
def book_appointment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        clinic_name = data.get("clinic_name")
        if clinic_name not in clinics:
            return JsonResponse({"error": "Clinic not found"})
        if clinics[clinic_name]["available_slots"] > 0:
            clinics[clinic_name]["available_slots"] -= 1
            return JsonResponse({"message": f"Appointment booked at {clinic_name}!", "remaining_slots": clinics[clinic_name]["available_slots"]})
        return JsonResponse({"error": "No available slots"})

@csrf_exempt
def get_nearest_ambulance(request):
    user_location = tuple(json.loads(request.body).get("location"))
    nearest_ambulance = min(ambulances.keys(), key=lambda x: geodesic(user_location, ambulances[x]["location"]).km)
    return JsonResponse({"nearest_ambulance": nearest_ambulance, "location": ambulances[nearest_ambulance]["location"]})

def get_optimized_ambulance_route(request):
    emergency_location = tuple(json.loads(request.body).get("location"))
    nearest_ambulance = min(ambulances.keys(), key=lambda x: geodesic(emergency_location, ambulances[x]["location"]).km)
    return JsonResponse({"optimized_route": {"ambulance": nearest_ambulance, "start": ambulances[nearest_ambulance]["location"], "destination": emergency_location}})

def get_traffic_signal_status(request):
    return JsonResponse({"traffic_signals": traffic_signals})
