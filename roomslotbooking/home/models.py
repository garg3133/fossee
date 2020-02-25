from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_no = models.CharField(max_length=30, blank=True)
    address = models.TextField(max_length=500, blank=True)
    room_manager = models.BooleanField(default=False)
