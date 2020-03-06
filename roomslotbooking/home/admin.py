from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Profile)
admin.site.register(models.RoomManager)
admin.site.register(models.Rooms)
admin.site.register(models.TimeSlot)
admin.site.register(models.PreBookingAllowance)
admin.site.register(models.Booking)