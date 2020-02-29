from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER, default='M')
    contact_no = models.CharField(max_length=30, blank=True)
    address = models.TextField(max_length=500, blank=True)
    room_manager = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
