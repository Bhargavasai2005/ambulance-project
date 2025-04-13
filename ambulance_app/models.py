from django.db import models

class Ambulance(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class Hospital(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    remaining_beds = models.IntegerField(default=0)  # Add this field

    def __str__(self):
        return self.name

class TrafficSignal(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(max_length=10, choices=[("GREEN", "Green"), ("RED", "Red")])

    def __str__(self):
        return self.name