from django.test import SimpleTestCase
from django.urls import reverse, resolve

from home.views import index, dashboard, setprofile, deleteTimeSlot, deleteBooking, bookingDateChangedAJAX, bookingRoomChangedAJAX, roomManagerDetailsAJAX, customerDetailsAJAX

class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, index)

    def test_dashboard_url_resolves(self):
        url = reverse('dashboard')
        self.assertEquals(resolve(url).func, dashboard)

    def test_setprofile_url_resolves(self):
        url = reverse('setprofile')
        self.assertEquals(resolve(url).func, setprofile)

    def test_delete_ts_url_resolves(self):
        url = reverse('delete_ts', args=[1])
        self.assertEquals(resolve(url).func, deleteTimeSlot)

    def test_delete_booking_url_resolves(self):
        url = reverse('delete_booking', args=[1])
        self.assertEquals(resolve(url).func, deleteBooking)

    def test_booking_date_changed_url_resolves(self):
        url = reverse('booking_date_changed')
        self.assertEquals(resolve(url).func, bookingDateChangedAJAX)

    def test_booking_room_changed_url_resolves(self):
        url = reverse('booking_room_changed')
        self.assertEquals(resolve(url).func, bookingRoomChangedAJAX)

    def test_room_manager_details_url_resolves(self):
        url = reverse('room_manager_details')
        self.assertEquals(resolve(url).func, roomManagerDetailsAJAX)

    def test_customer_details_url_resolves(self):
        url = reverse('customer_details')
        self.assertEquals(resolve(url).func, customerDetailsAJAX)
