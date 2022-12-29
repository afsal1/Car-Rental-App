from django.db import models
from authy.models import CustomUser
import uuid



class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle_station = models.CharField(max_length=50)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True
    )
 
    def __str__(self):
        return self.vehicle_station

class CarDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True
    )
    car_name = models.CharField(max_length=100, blank=True, null=True)
    day_price = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    car_image = models.ImageField(upload_to="car_image/", blank=False, null=False)
    vehicle_station = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.car_name


class RentCar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True
    )
    car = models.ForeignKey(
        CarDetails, on_delete=models.CASCADE, blank=True, null=True
    )
    rented_date = models.DateField(null=True)
    return_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.car