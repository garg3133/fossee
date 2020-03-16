from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

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

    def save(self, *args, **kwargs):
        if self.room_manager is True:
            prev_man = RoomManager.objects.filter(tenure_end=None)
            if prev_man.exists():
                prev_man = prev_man[0]
                if self.user != prev_man.manager:
                    # room_manager = False in previous manager profile
                    prev_man_profile = Profile.objects.get(user = prev_man.manager)
                    prev_man_profile.room_manager = False
                    prev_man_profile.save()
                    # Update tenure_end in previous manager's Room Manager
                    prev_man.tenure_end = datetime.now()
                    prev_man.save()
                    # Create new Room Manager Instance
                    room_man = RoomManager(manager=self.user)
                    room_man.save()
            else:
                room_man = RoomManager(manager=self.user)
                room_man.save()
        super(Profile, self).save(*args, **kwargs)

class RoomManager(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    tenure_start = models.DateTimeField(auto_now_add=True)
    tenure_end = models.DateTimeField(null=True)

    def __str__(self):
        return self.manager.username

class Rooms(models.Model):
    rooms = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField(null=True)

    class Meta:
        verbose_name_plural = 'Rooms'

    def __str__(self):
        return str(self.rooms)

class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField()
    end_date = models.DateField(null=True)

    def __str__(self):
        return str(self.start_time) + " - " + str(self.end_time)

class PreBookingAllowance(models.Model):
    days = models.IntegerField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.days)

class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    room = models.IntegerField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    booked_on = models.DateTimeField(auto_now_add=True)
    room_manager = models.ForeignKey(RoomManager, on_delete=models.CASCADE)
    cancelled = models.BooleanField(default=False)

    def __str__(self):
        return self.customer.username

