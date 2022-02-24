from pyexpat import model
from statistics import mode
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Rider(models.Model):
    OWNERSHIP_TYPE_CHOICES = [
        ('OWNER', 'Owner'),
        ('SHARER', 'Sharer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rideID = models.BigIntegerField(default=0)
    passengerNumber = models.PositiveIntegerField(default=0)
    ownership = models.CharField(max_length=20, choices = OWNERSHIP_TYPE_CHOICES, default = 'OWNER')

class Driver(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('ECO', 'Economy'),
        ('ECO XL', 'Economy XL'),
        ('LUX', 'Luxury'),
    ]

    user = models.OneToOneField(User, on_delete = models.CASCADE)  
    firstName = models.CharField(max_length = 50)
    lastName = models.CharField(max_length = 50)
    vehicleType = models.CharField(max_length=20, choices = VEHICLE_TYPE_CHOICES, default = 'ECO')
    licenseNumber = models.CharField(max_length=20)
    capacity = models.PositiveIntegerField(default=0)

class RideInfo(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('ECO', 'Economy'),
        ('ECO XL', 'Economy XL'),
        ('LUX', 'Luxury'),
    ]
    SHAREABLE_TYPE_CHOICES = [
        ('YES', 'Yes'),
        ('NO', 'No'),
    ]
    RIDESTATUS_TYPE_CHOICES = [
        ('OPEN', 'Open'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
    ]

    rideID = models.BigAutoField(primary_key=True)
    destination = models.CharField(max_length=50)
    arriveTime = models.DateTimeField(default=timezone.now)
    passengerNumber = models.PositiveIntegerField(default=0)
    vehicleType = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES, default='ECO')
    shareable = models.CharField(max_length=20, choices=SHAREABLE_TYPE_CHOICES, default='YES')
    rideStatus = models.CharField(max_length=20, choices=SHAREABLE_TYPE_CHOICES, default='OPEN')
    driver = models.ForeignKey(Driver, null=True, on_delete = models.CASCADE)