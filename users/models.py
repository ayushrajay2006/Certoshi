# models.py

from django.db import models
from django.contrib.auth.models import User

class TrustedContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # To associate contacts with a user
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    relationship = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"