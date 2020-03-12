from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('setprofile/', views.setprofile, name='setprofile'),
    path('timeslot/delete/<uid>/', views.deleteTimeSlot, name='delete_ts'),
    path('booking/delete/<uid>/', views.deleteBooking, name='delete_booking'),
    path('ajax/booking_date_changed/', views.bookingDateChangedAJAX, name='booking_date_changed'),
    path('ajax/booking_room_changed/', views.bookingRoomChangedAJAX, name='booking_room_changed'),
    path('ajax/room_manager_details/', views.roomManagerDetailsAJAX, name='room_manager_details'),
    path('ajax/customer_details/', views.customerDetailsAJAX, name='customer_details'),
]