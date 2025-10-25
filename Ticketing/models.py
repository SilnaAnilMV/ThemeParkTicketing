from django.db import models

class Booking(models.Model):
    booking_name = models.CharField(max_length=255)
    phone        = models.CharField(max_length=20)
    location     = models.CharField(max_length=255)
    date         = models.DateField()
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking_name} - {self.date}"

class Guest(models.Model):
    booking     = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="guests")
    person_name = models.CharField(max_length=255)
    ride        = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.person_name} - {self.ride}"
